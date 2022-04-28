import os
from unittest.mock import Mock, patch

import pytest
import responses
from werkzeug.exceptions import NotFound

from app.questionnaire import QuestionnaireSchema
from app.setup import create_app
from app.utilities.schema import (
    _load_schema_from_name,
    cache_questionnaire_schemas,
    get_allowed_languages,
    get_schema_list,
    get_schema_name_from_params,
    get_schema_path_map,
    load_schema_from_metadata,
    load_schema_from_name,
    load_schema_from_url,
)

TEST_SCHEMA_URL = "http://test.domain/schema.json"


def test_valid_schema_names_from_params():
    assert get_schema_name_from_params("mbs", "0253") == "mbs_0253"


@pytest.mark.parametrize(
    "schema_name, launch_language, expected",
    [
        ("invalid_schema_name", "en", ["en"]),
        ("test_language", "invalid_language", ["en"]),
        ("test_language", None, ["en"]),
    ],
)
def test_get_allowed_languages(schema_name, launch_language, expected):
    assert get_allowed_languages(schema_name, launch_language) == expected


def test_get_schema_path_map():
    schema_path_map = get_schema_path_map(include_test_schemas=True)

    # assert there is a test schemas folder
    assert "test" in schema_path_map
    test_schemas_by_language = schema_path_map["test"]
    # assert in the test schemas folder is en and cy folders
    assert all(lang in test_schemas_by_language for lang in ["en", "cy"])

    for path_by_schemas in test_schemas_by_language.values():
        for schema_name, schema_path in path_by_schemas.items():
            # for each schema in the list assert schema file exists
            assert os.path.exists(schema_path)
            assert os.path.basename(schema_path).replace(".json", "") == schema_name


def test_get_schema_list():
    expected_output = {
        survey_type: list(schemas_by_language["en"])
        for survey_type, schemas_by_language in get_schema_path_map(
            include_test_schemas=True
        ).items()
    }
    assert get_schema_list() == expected_output


# pylint: disable=no-value-for-parameter
def test_schema_cache_on_function_call():
    _load_schema_from_name.cache_clear()

    # load first schema into cache
    load_schema_from_name("test_language", "en")
    cache_info = _load_schema_from_name.cache_info()
    assert cache_info.currsize == 1
    assert cache_info.misses == 1
    assert cache_info.hits == 0

    # same schema in same language loads from cache
    load_schema_from_name("test_language", "en")
    cache_info = _load_schema_from_name.cache_info()
    assert cache_info.currsize == 1
    assert cache_info.misses == 1
    assert cache_info.hits == 1

    # same schema in same language as keyword argument loads from cache
    load_schema_from_name("test_language", language_code="en")
    cache_info = _load_schema_from_name.cache_info()
    assert cache_info.currsize == 1
    assert cache_info.misses == 1
    assert cache_info.hits == 2

    # same schema in different language adds to cache
    load_schema_from_name("test_language", "cy")
    cache_info = _load_schema_from_name.cache_info()
    assert cache_info.currsize == 2
    assert cache_info.misses == 2
    assert cache_info.hits == 2

    # loading a different schema adds to cache
    load_schema_from_name("test_textfield", "en")
    cache_info = _load_schema_from_name.cache_info()
    assert cache_info.currsize == 3
    assert cache_info.misses == 3
    assert cache_info.hits == 2


@patch(
    "app.utilities.schema.get_schema_path_map",
    Mock(return_value=get_schema_path_map(include_test_schemas=True)),
)
def test_schema_cache_on_app_start_up():
    _load_schema_from_name.cache_clear()
    cache_info = _load_schema_from_name.cache_info()
    assert cache_info.currsize == 0
    assert cache_info.misses == 0
    assert cache_info.hits == 0

    # create app and load schemas into cache
    create_app()

    total_schemas = sum(
        len(schemas)
        for schemas_by_language in get_schema_path_map(
            include_test_schemas=True
        ).values()
        for schemas in schemas_by_language.values()
    )
    cache_info = _load_schema_from_name.cache_info()
    assert cache_info.currsize > 0 and cache_info.currsize == total_schemas
    assert cache_info.misses == total_schemas
    assert cache_info.hits == 0

    # loads schema again to fetch from cache
    cache_questionnaire_schemas()
    cache_info = _load_schema_from_name.cache_info()
    assert cache_info.currsize == total_schemas
    assert cache_info.misses == total_schemas
    assert cache_info.hits == total_schemas


@responses.activate
def test_load_schema_from_url_200():
    load_schema_from_url.cache_clear()

    mock_schema = QuestionnaireSchema({}, language_code="cy")
    responses.add(responses.GET, TEST_SCHEMA_URL, json=mock_schema.json, status=200)
    loaded_schema = load_schema_from_url(schema_url=TEST_SCHEMA_URL, language_code="cy")

    assert loaded_schema.json == mock_schema.json
    assert loaded_schema.language_code == mock_schema.language_code

    cache_info = load_schema_from_url.cache_info()
    assert cache_info.currsize == 1
    assert cache_info.misses == 1
    assert cache_info.hits == 0


@responses.activate
def test_load_schema_from_url_404():
    load_schema_from_url.cache_clear()

    mock_schema = QuestionnaireSchema({})
    responses.add(responses.GET, TEST_SCHEMA_URL, json=mock_schema.json, status=404)

    with pytest.raises(NotFound):
        load_schema_from_url(schema_url=TEST_SCHEMA_URL, language_code="en")

    cache_info = load_schema_from_url.cache_info()
    assert cache_info.currsize == 0
    assert cache_info.misses == 1
    assert cache_info.hits == 0


@responses.activate
def test_load_schema_from_url_uses_cache():
    load_schema_from_url.cache_clear()

    mock_schema = QuestionnaireSchema({}, language_code="cy")
    responses.add(responses.GET, TEST_SCHEMA_URL, json=mock_schema.json, status=200)

    # First load: Add to cache, no hits
    load_schema_from_url(schema_url=TEST_SCHEMA_URL, language_code="cy")

    cache_info = load_schema_from_url.cache_info()
    assert cache_info.currsize == 1
    assert cache_info.misses == 1
    assert cache_info.hits == 0

    # Second load: Read from cache, 1 hit
    load_schema_from_url(schema_url=TEST_SCHEMA_URL, language_code="cy")

    cache_info = load_schema_from_url.cache_info()
    assert cache_info.currsize == 1
    assert cache_info.misses == 1
    assert cache_info.hits == 1


@responses.activate
def test_load_schema_from_metadata_with_schema_url():
    load_schema_from_url.cache_clear()

    metadata = {"schema_url": TEST_SCHEMA_URL, "language_code": "cy"}
    mock_schema = QuestionnaireSchema({}, language_code="cy")
    responses.add(responses.GET, TEST_SCHEMA_URL, json=mock_schema.json, status=200)
    loaded_schema = load_schema_from_metadata(metadata=metadata)

    assert loaded_schema.json == mock_schema.json
    assert loaded_schema.language_code == mock_schema.language_code
