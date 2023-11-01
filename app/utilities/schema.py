import os
import time
from functools import lru_cache
from glob import glob
from pathlib import Path
from typing import Any

from requests import RequestException
from structlog import get_logger

from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire.questionnaire_schema import (
    DEFAULT_LANGUAGE_CODE,
    QuestionnaireSchema,
)
from app.services.collection_instrument_registry import get_collection_instrument_v1
from app.utilities.json import json_load, json_loads
from app.utilities.request_session import get_retryable_session

logger = get_logger()

SCHEMA_DIR = "schemas"
LANGUAGE_CODES = ("en", "cy")

LANGUAGES_MAP = {
    "test_language": [["en", "cy"]],
    "cris_0001": [["en", "cy"]],
    "phm_0001": [["en", "cy"]],
}

SCHEMA_REQUEST_BACKOFF_FACTOR = 0.2
SCHEMA_REQUEST_MAX_RETRIES = 2  # Totals no. of request should be 3. The initial request + SCHEMA_REQUEST_MAX_RETRIES
SCHEMA_REQUEST_TIMEOUT = 3
SCHEMA_REQUEST_RETRY_STATUS_CODES = [
    408,
    429,
    500,
    502,
    503,
    504,
]


class SchemaRequestFailed(Exception):
    def __str__(self) -> str:
        return str("schema request failed")


@lru_cache(maxsize=None)
def get_schema_list(language_code: str = DEFAULT_LANGUAGE_CODE) -> dict[str, list]:
    return {
        survey_type: list(schemas_by_language[language_code])
        for survey_type, schemas_by_language in get_schema_path_map(
            include_test_schemas=True
        ).items()
        for lang in schemas_by_language
        if lang == language_code
    }


@lru_cache(maxsize=None)
def get_schema_path(language_code: str, schema_name: str) -> str | None:
    for schemas_by_language in get_schema_path_map(include_test_schemas=True).values():
        schema_path = schemas_by_language.get(language_code, {}).get(schema_name)
        if schema_path:
            return schema_path


@lru_cache(maxsize=None)
def get_schema_path_map(
    include_test_schemas: bool = False,
) -> dict[str, dict[str, dict[str, str]]]:
    schemas = {}
    for survey_type in os.listdir(SCHEMA_DIR):
        if not include_test_schemas and survey_type == "test":
            continue

        schemas[survey_type] = {
            language_code: {
                Path(schema_file).with_suffix("").name: schema_file
                for schema_file in glob(
                    f"{SCHEMA_DIR}/{survey_type}/{language_code}/*.json"
                )
            }
            for language_code in LANGUAGE_CODES
        }

    return schemas


def _schema_exists(language_code: str, schema_name: str) -> bool:
    schema_path_map = get_schema_path_map(include_test_schemas=True)
    return any(
        True
        for survey_type, schemas_by_lang in schema_path_map.items()
        if language_code in schemas_by_lang
        and schema_name in schemas_by_lang[language_code]
    )


def get_allowed_languages(schema_name: str | None, launch_language: str):
    if schema_name:
        for language_combination in LANGUAGES_MAP.get(schema_name, []):
            if launch_language in language_combination:
                return language_combination
    return [DEFAULT_LANGUAGE_CODE]


def load_schema_from_metadata(
    metadata: MetadataProxy, *, language_code: str | None
) -> QuestionnaireSchema:
    if schema_url := metadata.schema_url:
        # :TODO: Remove before production uses schema_url
        # This is temporary and is only for development/integration purposes.
        # This should not be used in production.

        start = time.time()
        schema = load_schema_from_url(schema_url, language_code)
        duration_in_milliseconds = (time.time() - start) * 1_000

        cache_info = (
            load_schema_from_url.cache_info()  # pylint: disable=no-value-for-parameter
        )
        logger.info(
            f"load_schema_from_url took {duration_in_milliseconds:.6f} milliseconds",
            schema_url=schema_url,
            currsize=cache_info.currsize,
            hits=cache_info.hits,
            misses=cache_info.misses,
            pid=os.getpid(),
        )
        return schema

    if cir_instrument_id := metadata.cir_instrument_id:
        return _load_schema_from_instrument_id(cir_instrument_id, language_code)

    return load_schema_from_name(
        # Type ignore: Metadata is validated to have either schema_name or schema_url populated.
        # This code runs only if schema_url was not present, thus schema_name is present (not None).
        metadata.schema_name,  # type: ignore
        language_code=language_code,
    )


def load_schema_from_name(
    schema_name: str, language_code: str | None = DEFAULT_LANGUAGE_CODE
) -> QuestionnaireSchema:
    language_code = language_code or DEFAULT_LANGUAGE_CODE
    return _load_schema_from_name(schema_name, language_code)


@lru_cache(maxsize=None)
def _load_schema_from_instrument_id(
    cir_instrument_id: str, language_code: str | None
) -> QuestionnaireSchema:
    schema_json = get_collection_instrument_v1(cir_instrument_id)
    language_code = language_code or DEFAULT_LANGUAGE_CODE

    return QuestionnaireSchema(schema_json, language_code)


@lru_cache(maxsize=None)
def _load_schema_from_name(schema_name: str, language_code: str) -> QuestionnaireSchema:
    schema_json = _load_schema_file(schema_name, language_code)

    return QuestionnaireSchema(schema_json, language_code)


def get_schema_name_from_params(eq_id, form_type) -> str:
    return f"{eq_id}_{form_type}"


def _load_schema_file(schema_name: str, language_code: str) -> Any:
    """
    Load a schema, optionally for a specified language.
    :param schema_name: The name of the schema e.g. census_household
    :param language_code: ISO 2-character code for language e.g. 'en', 'cy'
    """
    if language_code != DEFAULT_LANGUAGE_CODE and not _schema_exists(
        language_code, schema_name
    ):
        language_code = DEFAULT_LANGUAGE_CODE
        logger.info(
            "couldn't find requested language schema, falling back to 'en'",
            schema_file=schema_name,
            language_code=language_code,
        )

    if not _schema_exists(language_code, schema_name):
        logger.error(
            "no schema file exists",
            schema_name=schema_name,
            language_code=language_code,
        )
        raise FileNotFoundError

    schema_path = get_schema_path(language_code, schema_name)

    logger.info(
        "loading schema",
        schema_name=schema_name,
        language_code=language_code,
        schema_path=schema_path,
    )

    # Type ignore: Existence of the file is checked prior to call for the path
    with open(schema_path, encoding="utf8") as json_file:  # type: ignore
        return json_load(json_file)


@lru_cache(maxsize=None)
def load_schema_from_url(
    schema_url: str, language_code: str | None
) -> QuestionnaireSchema:
    language_code = language_code or DEFAULT_LANGUAGE_CODE
    pid = os.getpid()
    logger.info(
        "loading schema from URL",
        schema_url=schema_url,
        language_code=language_code,
        pid=pid,
    )

    constructed_schema_url = f"{schema_url}?language={language_code}"

    session = get_retryable_session(
        max_retries=SCHEMA_REQUEST_MAX_RETRIES,
        retry_status_codes=SCHEMA_REQUEST_RETRY_STATUS_CODES,
        backoff_factor=SCHEMA_REQUEST_BACKOFF_FACTOR,
    )

    try:
        req = session.get(constructed_schema_url, timeout=SCHEMA_REQUEST_TIMEOUT)
    except RequestException as exc:
        logger.exception(
            "schema request errored",
            schema_url=constructed_schema_url,
        )
        raise SchemaRequestFailed from exc

    if req.status_code == 200:
        schema_response = req.content.decode()
        response_duration_in_milliseconds = req.elapsed.total_seconds() * 1000

        logger.info(
            f"schema request took {response_duration_in_milliseconds:.2f} milliseconds",
            pid=pid,
        )

        return QuestionnaireSchema(json_loads(schema_response), language_code)

    logger.error(
        "got a non-200 response for schema url request",
        status_code=req.status_code,
        schema_url=constructed_schema_url,
    )

    raise SchemaRequestFailed


def cache_questionnaire_schemas():
    for schemas_by_language in get_schema_path_map().values():
        for language_code, schemas in schemas_by_language.items():
            for schema in schemas:
                load_schema_from_name(schema, language_code)
