import pytest
import responses
from flask import Flask, current_app
from marshmallow import ValidationError
from requests import RequestException
from sdc.crypto.key_store import KeyStore

from app.services.supplementary_data import (
    SUPPLEMENTARY_DATA_REQUEST_MAX_RETRIES,
    InvalidSupplementaryData,
    MissingSupplementaryDataKey,
    SupplementaryDataRequestFailed,
    decrypt_supplementary_data,
    get_supplementary_data,
)
from tests.app.utilities.test_schema import get_mocked_make_request

TEST_SDS_URL = "http://test.domain/v1/unit_data"
EXPECTED_SDS_DECRYPTION_VALIDATION_ERROR = "Supplementary data has no data to decrypt"


@responses.activate
def test_get_supplementary_data_200(
    app: Flask,
    encrypted_mock_supplementary_data_payload,
    decrypted_mock_supplementary_data_payload,
):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL

        responses.add(
            responses.GET,
            TEST_SDS_URL,
            json=encrypted_mock_supplementary_data_payload,
            status=200,
        )
        loaded_supplementary_data = get_supplementary_data(
            dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
            identifier="12346789012A",
            survey_id="123",
        )

    assert loaded_supplementary_data == decrypted_mock_supplementary_data_payload


@pytest.mark.parametrize(
    "status_code",
    [401, 403, 404, 501, 511],
)
@responses.activate
def test_get_supplementary_data_non_200(
    app: Flask, status_code, encrypted_mock_supplementary_data_payload
):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL

        responses.add(
            responses.GET,
            TEST_SDS_URL,
            json=encrypted_mock_supplementary_data_payload,
            status=status_code,
        )

        with pytest.raises(SupplementaryDataRequestFailed) as exc:
            get_supplementary_data(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                identifier="12346789012A",
                survey_id="123",
            )

    assert str(exc.value) == "Supplementary Data request failed"


@responses.activate
def test_get_supplementary_data_request_failed(app: Flask):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL

        responses.add(responses.GET, TEST_SDS_URL, body=RequestException())
        with pytest.raises(SupplementaryDataRequestFailed) as exc:
            get_supplementary_data(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                identifier="12346789012A",
                survey_id="123",
            )

    assert str(exc.value) == "Supplementary Data request failed"


def test_get_supplementary_data_retries_timeout_error(
    app: Flask,
    mocker,
    mocked_make_request_with_timeout,
    decrypted_mock_supplementary_data_payload,
):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL
        mocker.patch(
            "app.services.supplementary_data.decrypt_supplementary_data",
            return_value=decrypted_mock_supplementary_data_payload,
        )

        try:
            supplementary_data = get_supplementary_data(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                identifier="12346789012A",
                survey_id="123",
            )
        except SupplementaryDataRequestFailed:
            return pytest.fail("Supplementary data request unexpectedly failed")

    assert supplementary_data == decrypted_mock_supplementary_data_payload

    expected_call = (
        SUPPLEMENTARY_DATA_REQUEST_MAX_RETRIES + 1
    )  # Max retries + the initial request
    assert mocked_make_request_with_timeout.call_count == expected_call


@pytest.mark.usefixtures("mocked_response_content")
def test_get_supplementary_data_retries_transient_error(
    app: Flask, mocker, decrypted_mock_supplementary_data_payload
):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL
        mocked_make_request = get_mocked_make_request(
            mocker, status_codes=[500, 500, 200]
        )

        mocker.patch(
            "app.services.supplementary_data.decrypt_supplementary_data",
            return_value=decrypted_mock_supplementary_data_payload,
        )

        try:
            supplementary_data = get_supplementary_data(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                identifier="12346789012A",
                survey_id="123",
            )
        except SupplementaryDataRequestFailed:
            return pytest.fail("Supplementary data request unexpectedly failed")

        assert supplementary_data == decrypted_mock_supplementary_data_payload

        expected_call = (
            SUPPLEMENTARY_DATA_REQUEST_MAX_RETRIES + 1
        )  # Max retries + the initial request

    assert mocked_make_request.call_count == expected_call


def test_get_supplementary_data_max_retries(app: Flask, mocker):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL

        mocked_make_request = get_mocked_make_request(
            mocker, status_codes=[500, 500, 500, 500]
        )

        with pytest.raises(SupplementaryDataRequestFailed) as exc:
            get_supplementary_data(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                identifier="12346789012A",
                survey_id="123",
            )

    assert str(exc.value) == "Supplementary Data request failed"
    assert mocked_make_request.call_count == 3


def test_decrypt_supplementary_data_decrypts_when_encrypted_payload_is_valid(
    app: Flask,
    encrypted_mock_supplementary_data_payload,
    decrypted_mock_supplementary_data_payload,
):
    with app.app_context():
        result = decrypt_supplementary_data(
            key_store=app.eq["key_store"],
            supplementary_data=encrypted_mock_supplementary_data_payload,
        )
        assert result == decrypted_mock_supplementary_data_payload


def test_decrypt_supplementary_data_raises_validation_error_when_encrypted_payload_missing_data(
    app: Flask, mock_supplementary_data_payload_missing_data
):
    with app.app_context():
        with pytest.raises(ValidationError) as e:
            decrypt_supplementary_data(
                key_store=app.eq["key_store"],
                supplementary_data=mock_supplementary_data_payload_missing_data,
            )
        assert EXPECTED_SDS_DECRYPTION_VALIDATION_ERROR in e.value.messages


def test_decrypt_supplementary_data_raises_invalid_token_error_when_encrypted_data_kid_invalid(
    app: Flask, mock_supplementary_data_payload_invalid_kid_in_data
):
    with app.app_context():
        with pytest.raises(InvalidSupplementaryData):
            decrypt_supplementary_data(
                key_store=app.eq["key_store"],
                supplementary_data=mock_supplementary_data_payload_invalid_kid_in_data,
            )


def test_get_supplementary_data_raises_missing_supplementary_data_key_error_when_key_is_missing(
    app: Flask, mocker
):
    with app.app_context():
        mocker.patch.dict(
            "app.services.supplementary_data.current_app.eq",
            {"key_store": KeyStore({"keys": {}})},
        )

        with pytest.raises(MissingSupplementaryDataKey):
            get_supplementary_data(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                identifier="12346789012A",
                survey_id="123",
            )
