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
EXPECTED_SDS_DECRYPTION_VALIDATION_ERROR = "Supplementary data response cannot be decrypted without the key 'data'"

decrypted_mock_supplementary_data_payload = {
    "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
    "survey_id": "123",
    "encryption_key_id": "df88fdad2612ae1e80571120e6c6371f55896696",
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

encrypted_mock_supplementary_data_payload = {
    "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
    "survey_id": "123",
    "encryption_key_id": "df88fdad2612ae1e80571120e6c6371f55896696",
    # pylint: disable-next=line-too-long
    "data": "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJraWQiOiJkZjg4ZmRhZDI2MTJhZTFlODA1NzExMjBlNmM2MzcxZjU1ODk2Njk2In0.HXHbiTFa2XCuaKfSX4HfONLAVfZxEZo6_072A-ilMwhQKVhmQzqhDOX9dRID1yeoJnYxcdVGRDPwD5QvVHY2qsIOGkO3Brh59GHvSVASSCR21od7DBvlv0LoCDGAVcPt5bwwMbmziGQNkyfNnZG1EwAFk09lWfXwapJDsKbu1uhbW-F8HOOFZT7vR3paUmeTS0ekITwod-eZTD-B7KwUnDhJSm12cl9ob8MHirCaTE3jB64iQe_GvgdSUs1n5HZnX1f7rDQEpWm0OeuxPbEDrFmU-9wBV6LAjszypxPhQ0pv76TMu-VhjNBgf5Xm0cMO8ycmubdBdyWZiVUcmG0or9Mw0QvDYA9th27RChZPs5Le0w9oTnp5p5qzQexpPdzcS9Niqwabwx-NyUvTYkkFWc9poGNtrane4Ei4AFlV1-nQ4A8wMSIuOOSteYVombw-FEo9FhIhnuU8qyHoy0EaW5D1PMcdsphSb2ybTsiEJfdwwpxWDiuMDUpW6c2It_uSEpLCFHj51pQ8_Ez44gDyRE41NpSVvOB6h-nOggICQKggBDimtAuOyunZ5jhQWlKAeX4vAwM4iUEJ82c9lLTb8EDmQDOj6os9PCmyrZku5FHRXXDDvyuQAEqB-ARRnWT47LZOmaeTn4RI92qcejOqTNSG80mCUMY1PPu1fqxOiG8.5ukQQc5IT8fHgMRJ.jDXFWkIV9PIIrAC6EnVu5joGNdlmM52xgEqXCocUvZflvT8xMNocGGDUD1S0_FbQlpSP8FJcby4-B88yzxLgwil7mBqGtE7kWjALPGgnV9DsjEs-OblFFUIY9dVaKMTwaXhSxpjEt4j9NUOo-uyKOQIg-ZT745_zbkFZhlScuHz0u1YYaZGN04Md-eDI38erkTrS3pe2aovjbrwc9s_FMbrHEKlnuAUwxGPUxLTJXpTavHdmhhWriaI6a9ymng6mcefKqpNfWXc-3MIY2k10JCoo2KlVyYRN0up6T4OW56mAoXf7dUNSC8PtcZ5J3rpJ4XUnLZNVSL6Kz9BAmXY5SpZlU9zIBxHsirG9fS8gV6bI_MeMwbMawMCylcArlINVGVwDnUIvNXIJplVgm1OTHL0TiZzEFvnqkro3mzvVL-ElFeYO0uegqN8cDGkcv_lpAHH33j-IPdG-8CYerTCSVrT9.vWWMrdJFFLTVBSiv3KhbiQ",
}

mock_supplementary_data_payload_invalid_kid_in_data = {
    "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
    "survey_id": "123",
    # pylint: disable-next=line-too-long
    "data": "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJraWQiOiJkZjg4ZmRhZDI2MTJhZTFlODA1NzExMjBlNmM2MzcxZjU1ODk2Njk3In0=.lssJXsMUE3dhWtQRUt7DTaZJvx4DpNdLW98cu8g4NijYX9TFpJiOFyzPxUlpFZb-fMa4zW9q6qZofQeQTbl_Ae3QAwGhuWF7v9NMdWM1aH377byyJJyJpdqlU4t-P03evRWZqAG2HtsNE2Zn1ORXn80Dc9IRkzutgrziLI8OBIZeO6-XEgbVCapsQApWkyux7QRdFH95wfda75nVvGqTbBOYvQiMTKd8KzpH2Vl200IOqEpmrcjUCE-yqdTupzcr88hwNI2ZYdv-pTNowJw1FPODZ7V_sE4Ac-JYv3yBTDcXdz3I5-rX8i2HXqz-g3VhveZiAl9q0AgklPkaO_oNWJzjrCb7DZGL4DjiGYuOcw8OSdOpKLXwkExMlado-wigxy1IWoCzFu2E5tWpmLc0WWcjKuBgD7-4tcn059F7GcwhX2uMRESCmc39pblvseM2UnmmQnwr8GvD7gqWdFwtBsECyXQ5UXAxWLJor_MtU8lAFZxiorRcrXZJwAivroPO9iEB-1Mvt2zZFWI_vMgpJCAIpETscotDKMVCG0UMfkKckJqLnmQpvF4oYTr77w1COBX5bi-AV8UrLJ7sVVktSXOBc_KCGRpoImA5cE67hW7mFUdJi1EHA39qt0tTqZD7izpu8sSLxsiuCkfsqrd4uAedcDdQm4QGxXOPD4pxois.wfWsetB3M0x9qfw5.43Wns86lGlbHj63b0ZxE2bxBQVus6FIqelb9LfSbvopLn5oR8FM4vDEnDp_rIyvjmV9YAZJ6HAHaYaWoNyIO0EorgamrB4R3-LqInANoe9c8xLZ9wl_QpE9aWnxsmFGZUWLO3q2fVTPnwBtA_LxK8FD0vjdLL9eHGYEmPVCGVX0BJX04TVW9aoemsx9Yn3ZtfvmQHuROiB-GcA5wOSb-GvhzfplY09GQr7g7221MiYCHYimmEJyxLV5clWPXu6izzVLDyG9l2ewCifiuBLD0O1U_fPlahHTmidwHKJEAEn39biNw5E_dr8WyZ3xBvJa9dP50m0xeyN4COR-xlYcEbuDcKoqN6BnY0bMNDxQYlBO--QcPLQ6h48uTJszwzsmNIwHoi0xy5dQah7c9Nt2lpMuNt1Wix-O8JWYCqaiCKxjwt9G8kabMbzhp1n3LetWweoyV7qJTbiB13Byv6SZwMO9M.8j8wtvwBAHzqRhv5Ii9jjQ",
}

mock_supplementary_data_payload_missing_data = {
    "dataset_id": "44f1b432-9421-49e5-bd26-e63e18a30b69",
    "survey_id": "123",
    "encryption_key_id": "df88fdad2612ae1e80571120e6c6371f55896696",
}


@responses.activate
def test_get_supplementary_data_200(app: Flask):
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
            unit_id="12346789012A",
            survey_id="123",
        )

    assert loaded_supplementary_data == decrypted_mock_supplementary_data_payload


@pytest.mark.parametrize(
    "status_code",
    [401, 403, 404, 501, 511],
)
@responses.activate
def test_get_supplementary_data_non_200(app: Flask, status_code):
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
                unit_id="12346789012A",
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
                unit_id="12346789012A",
                survey_id="123",
            )

    assert str(exc.value) == "Supplementary Data request failed"


def test_get_supplementary_data_retries_timeout_error(
        app: Flask, mocker, mocked_make_request_with_timeout
):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL
        mocker.patch(
            "app.services.supplementary_data.decrypt_supplementary_data",
            return_value=decrypted_mock_supplementary_data_payload,
        )
        mocker.patch(
            "app.services.supplementary_data.validate_supplementary_data",
            return_value=decrypted_mock_supplementary_data_payload,
        )

        try:
            supplementary_data = get_supplementary_data(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                unit_id="12346789012A",
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
def test_get_supplementary_data_retries_transient_error(app: Flask, mocker):
    with app.app_context():
        current_app.config["SDS_API_BASE_URL"] = TEST_SDS_URL
        mocked_make_request = get_mocked_make_request(
            mocker, status_codes=[500, 500, 200]
        )

        mocker.patch(
            "app.services.supplementary_data.decrypt_supplementary_data",
            return_value=decrypted_mock_supplementary_data_payload,
        )
        mocker.patch(
            "app.services.supplementary_data.validate_supplementary_data",
            return_value=decrypted_mock_supplementary_data_payload,
        )

        try:
            supplementary_data = get_supplementary_data(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                unit_id="12346789012A",
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
                unit_id="12346789012A",
                survey_id="123",
            )

    assert str(exc.value) == "Supplementary Data request failed"
    assert mocked_make_request.call_count == 3


def test_decrypt_supplementary_data_decrypts_when_encrypted_payload_is_valid(
        app: Flask,
):
    with app.app_context():
        result = decrypt_supplementary_data(encrypted_mock_supplementary_data_payload)
        assert result == decrypted_mock_supplementary_data_payload


def test_decrypt_supplementary_data_raises_validation_error_when_encrypted_payload_missing_data(
        app: Flask,
):
    with app.app_context():
        with pytest.raises(ValidationError) as e:
            decrypt_supplementary_data(mock_supplementary_data_payload_missing_data)
        assert EXPECTED_SDS_DECRYPTION_VALIDATION_ERROR in str(e.value)


def test_decrypt_supplementary_data_raises_invalid_token_error_when_encrypted_data_kid_invalid(
        app: Flask,
):
    with app.app_context():
        with pytest.raises(InvalidSupplementaryData):
            decrypt_supplementary_data(mock_supplementary_data_payload_invalid_kid_in_data)


def test_get_supplementary_data_raises_missing_supplementary_data_key_error_when_key_is_missing(
        app: Flask, mocker
):
    with app.app_context():
        mocker.patch(
            "app.services.supplementary_data.get_key_store",
            return_value=KeyStore({"keys": {}}),
        )

        with pytest.raises(MissingSupplementaryDataKey):
            get_supplementary_data(
                dataset_id="44f1b432-9421-49e5-bd26-e63e18a30b69",
                unit_id="12346789012A",
                survey_id="123",
            )
