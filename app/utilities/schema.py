from functools import lru_cache
from glob import glob
from pathlib import Path
from typing import List, Mapping, Optional

import requests
import simplejson as json
from structlog import get_logger
from werkzeug.exceptions import NotFound

from app.questionnaire.questionnaire_schema import (
    DEFAULT_LANGUAGE_CODE,
    QuestionnaireSchema,
)

logger = get_logger()

SCHEMA_DIR = "schemas"
TEST_SCHEMA_DIR = "test_schemas"
LANGUAGE_CODES = ("en", "cy", "ga", "eo")

LANGUAGES_MAP = {
    "test_language": [["en", "cy"], ["en", "ga"]],
    "ccs_household_gb_wls": [["en", "cy"]],
    "census_household_gb_wls": [["en", "cy"]],
    "census_individual_gb_wls": [["en", "cy"]],
    "census_household_gb_nir": [["en"], ["en", "ga"], ["en", "eo"]],
    "census_individual_gb_nir": [["en"], ["en", "ga"], ["en", "eo"]],
    "census_communal_establishment_gb_wls": [["en", "cy"]],
}


@lru_cache(maxsize=None)
def get_schema_list(language_code: str = DEFAULT_LANGUAGE_CODE) -> List:
    return list(get_schema_path_map(include_test_schemas=True)[language_code].keys())


@lru_cache(maxsize=None)
def get_schema_path_map(include_test_schemas: Optional[bool] = False) -> Mapping:
    dirs = [SCHEMA_DIR]
    if include_test_schemas:
        dirs.append(TEST_SCHEMA_DIR)

    return {
        language_code: {
            Path(schema_file).with_suffix("").name: schema_file
            for schema_dir in dirs
            for schema_file in glob(f"{schema_dir}/{language_code}/*.json")
        }
        for language_code in LANGUAGE_CODES
    }


def _schema_exists(language_code, schema_name):
    schema_path_map = get_schema_path_map(include_test_schemas=True)
    return (
        language_code in schema_path_map
        and schema_name in schema_path_map[language_code]
    )


def get_allowed_languages(schema_name, launch_language):
    for language_combination in LANGUAGES_MAP.get(schema_name, []):
        if launch_language in language_combination:
            return language_combination
    return [DEFAULT_LANGUAGE_CODE]


def load_schema_from_metadata(metadata):
    if metadata.get("survey_url"):
        return load_schema_from_url(
            metadata["survey_url"], metadata.get("language_code")
        )

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


def transform_form_type(form_type):
    census_form_types = {
        "H": "household",
        "I": "individual",
        "C": "communal_establishment",
    }

    return census_form_types[form_type]


def transform_region_code(region_code_input):
    return region_code_input.lower().replace("-", "_")


def transform_survey(survey_input):
    return survey_input.lower()


def get_schema_name_from_census_params(survey, form_type, region_code):
    try:
        form_type_transformed = transform_form_type(form_type)
    except KeyError:
        raise ValueError(
            "Invalid form_type parameter was specified. Must be one of `H`, `I`, `C`"
        )

    region_code_transformed = transform_region_code(region_code)
    survey_transformed = transform_survey(survey)

    schema_name = (
        f"{survey_transformed}_{form_type_transformed}_{region_code_transformed}"
    )
    return schema_name


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

    schema_path = get_schema_path_map(include_test_schemas=True)[language_code][
        schema_name
    ]

    logger.info(
        "loading schema",
        schema_name=schema_name,
        language_code=language_code,
        schema_path=schema_path,
    )

    with open(schema_path, encoding="utf8") as json_file:
        return json.load(json_file, use_decimal=True)


@lru_cache(maxsize=None)
def load_schema_from_url(survey_url, language_code):
    language_code = language_code or DEFAULT_LANGUAGE_CODE
    logger.info(
        "loading schema from URL", survey_url=survey_url, language_code=language_code
    )

    constructed_survey_url = "{}?language={}".format(survey_url, language_code)

    req = requests.get(constructed_survey_url)
    schema_response = req.content.decode()

    if req.status_code == 404:
        logger.error("no schema exists", survey_url=constructed_survey_url)
        raise NotFound

    return QuestionnaireSchema(json.loads(schema_response), language_code)


def cache_questionnaire_schemas():
    for language_code, schemas in get_schema_path_map().items():
        for schema in schemas:
            load_schema_from_name(schema, language_code)
