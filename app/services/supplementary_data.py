import json
from typing import Mapping, MutableMapping
from urllib.parse import urlencode

from flask import current_app
from marshmallow import ValidationError
from requests import RequestException
from sdc.crypto.jwe_helper import InvalidTokenException, JWEHelper
from sdc.crypto.key_store import KeyStore
from structlog import get_logger

from app.keys import KEY_PURPOSE_SDS
from app.utilities.request_session import get_retryable_session
from app.utilities.supplementary_data_parser import validate_supplementary_data_v1

SUPPLEMENTARY_DATA_REQUEST_BACKOFF_FACTOR = 0.2
SUPPLEMENTARY_DATA_REQUEST_MAX_RETRIES = 2  # Totals no. of request should be 3. The initial request + SUPPLEMENTARY_DATA_REQUEST_MAX_RETRIES
SUPPLEMENTARY_DATA_REQUEST_TIMEOUT = 3
SUPPLEMENTARY_DATA_REQUEST_RETRY_STATUS_CODES = [
    408,
    429,
    500,
    502,
    503,
    504,
]

logger = get_logger()


class SupplementaryDataRequestFailed(Exception):
    def __str__(self) -> str:
        return "Supplementary Data request failed"


class MissingSupplementaryDataKey(Exception):
    pass


class InvalidSupplementaryData(Exception):
    pass


def get_supplementary_data(*, dataset_id: str, identifier: str, survey_id: str) -> dict:
    # Type ignore: current_app is a singleton in this application and has the key_store key in its eq attribute.
    key_store = current_app.eq["key_store"]  # type: ignore
    if not key_store.get_key(purpose=KEY_PURPOSE_SDS, key_type="private"):
        raise MissingSupplementaryDataKey

    supplementary_data_url = current_app.config["SDS_API_BASE_URL"]

    parameters = {"dataset_id": dataset_id, "identifier": identifier}

    encoded_parameters = urlencode(parameters)
    constructed_supplementary_data_url = (
        f"{supplementary_data_url}?{encoded_parameters}"
    )

    session = get_retryable_session(
        max_retries=SUPPLEMENTARY_DATA_REQUEST_MAX_RETRIES,
        retry_status_codes=SUPPLEMENTARY_DATA_REQUEST_RETRY_STATUS_CODES,
        backoff_factor=SUPPLEMENTARY_DATA_REQUEST_BACKOFF_FACTOR,
    )

    try:
        response = session.get(
            constructed_supplementary_data_url,
            timeout=SUPPLEMENTARY_DATA_REQUEST_TIMEOUT,
        )
    except RequestException as exc:
        logger.exception(
            "Error requesting supplementary data",
            supplementary_data_url=constructed_supplementary_data_url,
        )
        raise SupplementaryDataRequestFailed from exc

    if response.status_code == 200:
        supplementary_data_response_content = response.content.decode()
        supplementary_data = decrypt_supplementary_data(
            key_store=key_store,
            supplementary_data=json.loads(supplementary_data_response_content),
        )

        return validate_supplementary_data(
            supplementary_data=supplementary_data,
            dataset_id=dataset_id,
            identifier=identifier,
            survey_id=survey_id,
        )

    logger.error(
        "got a non-200 response for supplementary data request",
        status_code=response.status_code,
        schema_url=constructed_supplementary_data_url,
    )

    raise SupplementaryDataRequestFailed


def decrypt_supplementary_data(
    *, key_store: KeyStore, supplementary_data: MutableMapping
) -> Mapping:
    if encrypted_data := supplementary_data.get("data"):
        try:
            decrypted_data = JWEHelper.decrypt(
                encrypted_data, key_store=key_store, purpose=KEY_PURPOSE_SDS
            )
            supplementary_data["data"] = json.loads(decrypted_data)
            return supplementary_data
        except InvalidTokenException as e:
            raise InvalidSupplementaryData from e

    raise ValidationError("Supplementary data has no data to decrypt")


def validate_supplementary_data(
    supplementary_data: Mapping, dataset_id: str, identifier: str, survey_id: str
) -> dict:
    try:
        return validate_supplementary_data_v1(
            supplementary_data=supplementary_data,
            dataset_id=dataset_id,
            identifier=identifier,
            survey_id=survey_id,
        )
    except ValidationError as e:
        raise ValidationError("Invalid supplementary data") from e
