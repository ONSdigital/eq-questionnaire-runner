import json
from urllib.parse import urlencode

from flask import current_app
from requests import RequestException
from structlog import get_logger

from app.utilities.request_session import get_retryable_session

CIR_REQUEST_TIMEOUT = 3
logger = get_logger()


class CIRRequestFailed(Exception):
    pass


def get_collection_instrument_v1(cir_instrument_id: str) -> dict:
    cir_url = (
        f"{current_app.config['CIR_API_BASE_URL']}/v2/retrieve_collection_instrument"
    )
    encoded_parameters = urlencode({"guid": cir_instrument_id})
    constructed_cir_url = f"{cir_url}?{encoded_parameters}"

    session = get_retryable_session()

    try:
        response = session.get(
            constructed_cir_url,
            timeout=CIR_REQUEST_TIMEOUT,
        )
    except RequestException as exc:
        logger.exception(
            "Error requesting collection instrument",
            cir_url=constructed_cir_url,
        )
        raise CIRRequestFailed from exc

    if response.status_code == 200:
        cir_response_content = response.content.decode()
        return json.loads(cir_response_content)

    logger.error(
        "got a non-200 response for collection instrument request",
        status_code=response.status_code,
        schema_url=constructed_cir_url,
    )

    raise CIRRequestFailed("Collection instrument request failed")
