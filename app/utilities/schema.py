import os
import time
from functools import lru_cache
from glob import glob
from pathlib import Path
from typing import Mapping, Optional

import requests
from structlog import get_logger
from werkzeug.exceptions import NotFound

from app.questionnaire.questionnaire_schema import (
    DEFAULT_LANGUAGE_CODE,
    QuestionnaireSchema,
)
from app.utilities.json import json_load, json_loads

logger = get_logger()

SCHEMA_DIR = "schemas"
LANGUAGE_CODES = ("en", "cy")

LANGUAGES_MAP = {"test_language": [["en", "cy"]]}


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
def get_schema_path(language_code, schema_name):
    for schemas_by_language in get_schema_path_map(include_test_schemas=True).values():
        schema_path = schemas_by_language.get(language_code, {}).get(schema_name)
        if schema_path:
            return schema_path


@lru_cache(maxsize=None)
def get_schema_path_map(include_test_schemas: Optional[bool] = False) -> Mapping:
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


def _schema_exists(language_code, schema_name):
    schema_path_map = get_schema_path_map(include_test_schemas=True)
    return any(
        True
        for survey_type, schemas_by_lang in schema_path_map.items()
        if language_code in schemas_by_lang
        and schema_name in schemas_by_lang[language_code]
    )


def get_allowed_languages(schema_name, launch_language):
    for language_combination in LANGUAGES_MAP.get(schema_name, []):
        if launch_language in language_combination:
            return language_combination
    return [DEFAULT_LANGUAGE_CODE]


def load_schema_from_metadata(metadata):
    if survey_url := metadata.get("survey_url"):
        # :TODO: Remove before production uses survey_url
        # This is temporary and is only for development/integration purposes.
        # This should not be used in production.

        start = time.time()
        schema = load_schema_from_url(survey_url, metadata.get("language_code"))
        duration_in_milliseconds = (time.time() - start) * 1_000

        cache_info = (
            load_schema_from_url.cache_info()  # pylint: disable=no-value-for-parameter
        )
        logger.info(
            f"load_schema_from_url took {duration_in_milliseconds:.6f} milliseconds",
            survey_url=survey_url,
            currsize=cache_info.currsize,
            hits=cache_info.hits,
            misses=cache_info.misses,
            pid=os.getpid(),
        )
        return schema

    return load_schema_from_name(
        metadata.get("schema_name"), language_code=metadata.get("language_code")
    )


def load_schema_from_session_data(session_data):
    return load_schema_from_metadata(vars(session_data))


def load_schema_from_name(schema_name, language_code=DEFAULT_LANGUAGE_CODE):
    return _load_schema_from_name(schema_name, language_code)


@lru_cache(maxsize=None)
def _load_schema_from_name(schema_name, language_code):
    schema_json = _load_schema_file(schema_name, language_code)

    return QuestionnaireSchema(schema_json, language_code)


def get_schema_name_from_params(eq_id, form_type):
    return f"{eq_id}_{form_type}"


def _load_schema_file(schema_name, language_code):
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

    with open(schema_path, encoding="utf8") as json_file:
        return json_load(json_file)


@lru_cache(maxsize=None)
def load_schema_from_url(survey_url, language_code):
    language_code = language_code or DEFAULT_LANGUAGE_CODE
    pid = os.getpid()
    logger.info(
        "loading schema from URL",
        survey_url=survey_url,
        language_code=language_code,
        pid=pid,
    )

    constructed_survey_url = f"{survey_url}?language={language_code}"

    req = requests.get(constructed_survey_url)
    schema_response = req.content.decode()
    response_duration_in_milliseconds = req.elapsed.total_seconds() * 1000

    logger.info(
        f"schema request took {response_duration_in_milliseconds:.2f} milliseconds",
        pid=pid,
    )

    if req.status_code == 404:
        logger.error("no schema exists", survey_url=constructed_survey_url)
        raise NotFound

    return QuestionnaireSchema(json_loads(schema_response), language_code)


def cache_questionnaire_schemas():
    for schemas_by_language in get_schema_path_map().values():
        for language_code, schemas in schemas_by_language.items():
            for schema in schemas:
                load_schema_from_name(schema, language_code)
