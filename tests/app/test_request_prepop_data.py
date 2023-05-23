import pytest
import responses
from requests import RequestException

from app.routes.session import (
    PREPOP_REQUEST_MAX_RETRIES,
    PrepopRequestFailed,
    get_prepop_data,
)
from tests.app.utilities.test_schema import get_mocked_make_request

TEST_SDS_URL = "http://test.domain/v1/unit_data"

mock_prepop_payload = {
    "dataset_id": "001",
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
def test_get_prepop_data_200():
    responses.add(responses.GET, TEST_SDS_URL, json=mock_prepop_payload, status=200)
    loaded_prepop_data = get_prepop_data(
        prepop_url=TEST_SDS_URL, dataset_id="001", ru_ref="12346789012A"
    )

    assert loaded_prepop_data == mock_prepop_payload


@pytest.mark.parametrize(
    "status_code",
    [401, 403, 404, 501, 511],
)
@responses.activate
def test_get_prepop_data_non_200(status_code):
    responses.add(
        responses.GET, TEST_SDS_URL, json=mock_prepop_payload, status=status_code
    )

    with pytest.raises(PrepopRequestFailed) as exc:
        get_prepop_data(
            prepop_url=TEST_SDS_URL, dataset_id="001", ru_ref="12346789012A"
        )

    assert str(exc.value) == "Prepop request failed"


@responses.activate
def test_get_prepop_data_request_failed():
    responses.add(responses.GET, TEST_SDS_URL, body=RequestException())
    with pytest.raises(PrepopRequestFailed) as exc:
        get_prepop_data(
            prepop_url=TEST_SDS_URL, dataset_id="001", ru_ref="12346789012A"
        )

    assert str(exc.value) == "Prepop request failed"


def test_get_prepop_data_retries_timeout_error(
    mocker, mocked_make_request_with_timeout
):
    mocker.patch(
        "app.routes.session.validate_prepop_data", return_value=mock_prepop_payload
    )

    try:
        prepop_data = get_prepop_data(
            prepop_url=TEST_SDS_URL, dataset_id="001", ru_ref="12346789012A"
        )
    except PrepopRequestFailed:
        return pytest.fail("Prepop request unexpectedly failed")

    assert prepop_data == mock_prepop_payload

    expected_call = PREPOP_REQUEST_MAX_RETRIES + 1  # Max retries + the initial request
    assert mocked_make_request_with_timeout.call_count == expected_call


@pytest.mark.usefixtures("mocked_response_content")
def test_get_prepop_data_retries_transient_error(mocker):
    mocked_make_request = get_mocked_make_request(mocker, status_codes=[500, 500, 200])

    mocker.patch(
        "app.routes.session.validate_prepop_data", return_value=mock_prepop_payload
    )

    try:
        prepop_data = get_prepop_data(
            prepop_url=TEST_SDS_URL, dataset_id="001", ru_ref="12346789012A"
        )
    except PrepopRequestFailed:
        return pytest.fail("Prepop request unexpectedly failed")

    assert prepop_data == mock_prepop_payload

    expected_call = PREPOP_REQUEST_MAX_RETRIES + 1  # Max retries + the initial request
    assert mocked_make_request.call_count == expected_call


def test_get_prepop_data_max_retries(mocker):
    mocked_make_request = get_mocked_make_request(
        mocker, status_codes=[500, 500, 500, 500]
    )

    with pytest.raises(PrepopRequestFailed) as exc:
        get_prepop_data(
            prepop_url=TEST_SDS_URL, dataset_id="001", ru_ref="12346789012A"
        )

    assert str(exc.value) == "Prepop request failed"
    assert mocked_make_request.call_count == 3
