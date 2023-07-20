import pytest
import responses
from flask import Flask, current_app
from requests import RequestException

from app.services.supplementary_data import (
    SUPPLEMENTARY_DATA_REQUEST_MAX_RETRIES,
    SupplementaryDataRequestFailed,
    get_supplementary_data_v1,
)
from tests.app.utilities.test_schema import get_mocked_make_request

TEST_SDS_URL = "http://test.domain"

mock_supplementary_data_payload = {
    "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
    "survey_id": "123",
    "data": {
        "schema_version": "v1",
        "identifier": "12346789012A",
        "items": {
            "local_units": [
                {
                    "identifier": "0001",
                    "lu_name": "TEST NAME. 1",
                    "lu_address": [
                        "FIRST ADDRESS 1",
                        "FIRST ADDRESS 2",
                        "TOWN",
                        "COUNTY",
                        "POST CODE",
                    ],
                },
                {
                    "identifier": "0002",
                    "lu_name": "TEST NAME 2",
                    "lu_address": [
                        "SECOND ADDRESS 1",
                        "SECOND ADDRESS 1",
                        "TOWN",
                        "COUNTY",
                        "POSTCODE",
                    ],
                },
            ]
        },
    },
}


@responses.activate
def test_get_supplementary_data_v1_200(app: Flask):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL

        responses.add(
            responses.GET,
            f"{TEST_SDS_URL}/v1/unit_data",
            json=mock_supplementary_data_payload,
            status=200,
        )
        loaded_supplementary_data = get_supplementary_data_v1(
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            unit_id="12346789012A",
            survey_id="123",
        )

    assert loaded_supplementary_data == mock_supplementary_data_payload


@pytest.mark.parametrize(
    "status_code",
    [401, 403, 404, 501, 511],
)
@responses.activate
def test_get_supplementary_data_v1_non_200(app: Flask, status_code):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL

        responses.add(
            responses.GET,
            f"{TEST_SDS_URL}/v1/unit_data",
            json=mock_supplementary_data_payload,
            status=status_code,
        )

        with pytest.raises(SupplementaryDataRequestFailed) as exc:
            get_supplementary_data_v1(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                unit_id="12346789012A",
                survey_id="123",
            )

    assert str(exc.value) == "Supplementary Data request failed"


@responses.activate
def test_get_supplementary_data_v1_request_failed(app: Flask):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL

        responses.add(responses.GET, TEST_SDS_URL, body=RequestException())
        with pytest.raises(SupplementaryDataRequestFailed) as exc:
            get_supplementary_data_v1(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                unit_id="12346789012A",
                survey_id="123",
            )

    assert str(exc.value) == "Supplementary Data request failed"


def test_get_supplementary_data_v1_retries_timeout_error(
        app: Flask, mocker, mocked_make_request_with_timeout
):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL
        mocker.patch(
            "app.services.supplementary_data.validate_supplementary_data",
            return_value=mock_supplementary_data_payload,
        )

        try:
            supplementary_data = get_supplementary_data_v1(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                unit_id="12346789012A",
                survey_id="123",
            )
        except SupplementaryDataRequestFailed:
            return pytest.fail("Supplementary data request unexpectedly failed")

    assert supplementary_data == mock_supplementary_data_payload

    expected_call = (
            SUPPLEMENTARY_DATA_REQUEST_MAX_RETRIES + 1
    )  # Max retries + the initial request
    assert mocked_make_request_with_timeout.call_count == expected_call


@pytest.mark.usefixtures("mocked_response_content")
def test_get_supplementary_data_v1_retries_transient_error(app: Flask, mocker):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL
        mocked_make_request = get_mocked_make_request(
            mocker, status_codes=[500, 500, 200]
        )

        mocker.patch(
            "app.services.supplementary_data.validate_supplementary_data",
            return_value=mock_supplementary_data_payload,
        )

        try:
            supplementary_data = get_supplementary_data_v1(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                unit_id="12346789012A",
                survey_id="123",
            )
        except SupplementaryDataRequestFailed:
            return pytest.fail("Supplementary data request unexpectedly failed")

        assert supplementary_data == mock_supplementary_data_payload

        expected_call = (
                SUPPLEMENTARY_DATA_REQUEST_MAX_RETRIES + 1
        )  # Max retries + the initial request

    assert mocked_make_request.call_count == expected_call


def test_get_supplementary_data_v1_max_retries(app: Flask, mocker):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL

        mocked_make_request = get_mocked_make_request(
            mocker, status_codes=[500, 500, 500, 500]
        )

        with pytest.raises(SupplementaryDataRequestFailed) as exc:
            get_supplementary_data_v1(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                unit_id="12346789012A",
                survey_id="123",
            )

    assert str(exc.value) == "Supplementary Data request failed"
    assert mocked_make_request.call_count == 3
