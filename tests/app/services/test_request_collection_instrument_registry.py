import pytest
import responses
from flask import Flask, current_app
from requests import RequestException

from app.services.collection_instrument_registry import (
    CIRRequestFailed,
    get_collection_instrument_v1,
)

TEST_CIR_URL = "http://test.domain"


@responses.activate
def tset_get_collection_instrument_200(
    app: Flask,
    mock_cir_payload,
):
    with app.app_context():
        current_app.config["CIR_API_BASE_URL"] = TEST_CIR_URL

        responses.add(
            responses.GET,
            f"{TEST_CIR_URL}/v2/retrieve_collection_instrument",
            json=mock_cir_payload,
            status=200,
        )
        loaded_supplementary_data = get_collection_instrument_v1(
            cir_instrument_id="f0519981-426c-8b93-75c0-bfc40c66fe25"
        )

    assert loaded_supplementary_data == mock_cir_payload


@pytest.mark.parametrize(
    "status_code",
    [401, 403, 404, 501, 511],
)
@responses.activate
def test_get_cir_v1_non_200(app: Flask, status_code, mock_cir_payload):
    with app.app_context():
        current_app.config["CIR_API_BASE_URL"] = TEST_CIR_URL

        responses.add(
            responses.GET,
            f"{TEST_CIR_URL}/v2/retrieve_collection_instrument",
            json=mock_cir_payload,
            status=status_code,
        )

        with pytest.raises(CIRRequestFailed) as exc:
            get_collection_instrument_v1(
                cir_instrument_id="f0519981-426c-8b93-75c0-bfc40c66fe25"
            )

    assert str(exc.value) == "Collection instrument request failed"


@responses.activate
def test_get_cir_v1_request_failed(app: Flask):
    with app.app_context():
        current_app.config["CIR_API_BASE_URL"] = TEST_CIR_URL

        responses.add(responses.GET, TEST_CIR_URL, body=RequestException())
        with pytest.raises(CIRRequestFailed):
            get_collection_instrument_v1(
                cir_instrument_id="f0519981-426c-8b93-75c0-bfc40c66fe25"
            )
