import time

from httmock import HTTMock, response, urlmatch
from unittest.mock import patch, Mock

from app.utilities.schema import (
    CIR_RETRIEVE_COLLECTION_INSTRUMENT_URL,
    get_schema_path_map,
)
from tests.integration.create_token import PAYLOAD_V2_BUSINESS
from tests.integration.integration_test_case import IntegrationTestCase

SCHEMA_PATH_MAP = get_schema_path_map(include_test_schemas=True)

# pylint: disable-next=line-too-long
DATA = "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJraWQiOiJkZjg4ZmRhZDI2MTJhZTFlODA1NzExMjBlNmM2MzcxZjU1ODk2Njk3In0.lssJXsMUE3dhWtQRUt7DTaZJvx4DpNdLW98cu8g4NijYX9TFpJiOFyzPxUlpFZb-fMa4zW9q6qZofQeQTbl_Ae3QAwGhuWF7v9NMdWM1aH377byyJJyJpdqlU4t-P03evRWZqAG2HtsNE2Zn1ORXn80Dc9IRkzutgrziLI8OBIZeO6-XEgbVCapsQApWkyux7QRdFH95wfda75nVvGqTbBOYvQiMTKd8KzpH2Vl200IOqEpmrcjUCE-yqdTupzcr88hwNI2ZYdv-pTNowJw1FPODZ7V_sE4Ac-JYv3yBTDcXdz3I5-rX8i2HXqz-g3VhveZiAl9q0AgklPkaO_oNWJzjrCb7DZGL4DjiGYuOcw8OSdOpKLXwkExMlado-wigxy1IWoCzFu2E5tWpmLc0WWcjKuBgD7-4tcn059F7GcwhX2uMRESCmc39pblvseM2UnmmQnwr8GvD7gqWdFwtBsECyXQ5UXAxWLJor_MtU8lAFZxiorRcrXZJwAivroPO9iEB-1Mvt2zZFWI_vMgpJCAIpETscotDKMVCG0UMfkKckJqLnmQpvF4oYTr77w1COBX5bi-AV8UrLJ7sVVktSXOBc_KCGRpoImA5cE67hW7mFUdJi1EHA39qt0tTqZD7izpu8sSLxsiuCkfsqrd4uAedcDdQm4QGxXOPD4pxois.wfWsetB3M0x9qfw5.43Wns86lGlbHj63b0ZxE2bxBQVus6FIqelb9LfSbvopLn5oR8FM4vDEnDp_rIyvjmV9YAZJ6HAHaYaWoNyIO0EorgamrB4R3-LqInANoe9c8xLZ9wl_QpE9aWnxsmFGZUWLO3q2fVTPnwBtA_LxK8FD0vjdLL9eHGYEmPVCGVX0BJX04TVW9aoemsx9Yn3ZtfvmQHuROiB-GcA5wOSb-GvhzfplY09GQr7g7221MiYCHYimmEJyxLV5clWPXu6izzVLDyG9l2ewCifiuBLD0O1U_fPlahHTmidwHKJEAEn39biNw5E_dr8WyZ3xBvJa9dP50m0xeyN4COR-xlYcEbuDcKoqN6BnY0bMNDxQYlBO--QcPLQ6h48uTJszwzsmNIwHoi0xy5dQah7c9Nt2lpMuNt1Wix-O8JWYCqaiCKxjwt9G8kabMbzhp1n3LetWweoyV7qJTbiB13Byv6SZwMO9M.8j8wtvwBAHzqRhv5Ii9jjQ",


class TestLoginWithGetRequest(IntegrationTestCase):
    def test_login_with_no_token_should_be_unauthorized(self):
        # Given
        token = ""

        # When
        self.get(url=f"/session?token={token}")

        # Then
        self.assertStatusUnauthorised()

    def test_login_with_invalid_token_should_be_forbidden(self):
        # Given
        token = "123"

        # When
        self.get(url=f"/session?token={token}")

        # Then
        self.assertStatusForbidden()

    def test_login_with_valid_v2_business_token_should_redirect_to_survey(self):
        # Given
        token = self.token_generator.create_token_v2(schema_name="test_checkbox")

        # When
        self.get(url=f"/session?token={token}")

        # Then
        self.assertStatusOK()
        self.assertInUrl("/questionnaire")

    def test_login_with_valid_v2_social_token_should_redirect_to_survey(self):
        # Given
        token = self.token_generator.create_token_v2(
            schema_name="test_theme_social", theme="social"
        )

        # When
        self.get(url=f"/session?token={token}")

        # Then
        self.assertStatusOK()
        self.assertInUrl("/questionnaire")

    def test_login_with_token_twice_is_unauthorised_when_same_jti_provided(self):
        # Given
        token = self.token_generator.create_token_v2("test_checkbox")
        self.get(url=f"/session?token={token}")

        # When
        self.get(url=f"/session?token={token}")

        # Then
        self.assertStatusUnauthorised()

    def test_login_without_jti_in_token_is_unauthorised(self):
        # Given
        token = self.token_generator.create_token_without_jti("test_checkbox")
        self.get(url=f"/session?token={token}")

        # Then
        self.assertStatusForbidden()

    def test_login_with_valid_v2_business_token_no_schema_name(self):
        # Given
        token = self.token_generator.create_token_v2(schema_name="")

        # When
        self.get(url=f"/session?token={token}")

        # Then
        self.assertStatusForbidden()

    def test_login_with_valid_v2_social_token_no_schema_name(self):
        # Given
        token = self.token_generator.create_token_v2(schema_name="", theme="social")

        # When
        self.get(url=f"/session?token={token}")

        # Then
        self.assertStatusForbidden()

    def test_http_head_request_to_login_returns_successfully_and_get_still_works(self):
        # Given
        token = self.token_generator.create_token_v2("test_checkbox")

        # When
        self.head("/session?token=" + token)
        self.get(url=f"/session?token={token}")

        # Then
        self.assertStatusOK()
        self.assertInUrl("/questionnaire")

    def test_login_with_missing_mandatory_claims_should_be_forbidden(self):
        # Given
        payload_vars = PAYLOAD_V2_BUSINESS.copy()
        payload_vars["iat"] = time.time()
        payload_vars["exp"] = payload_vars["iat"] + float(3600)  # one hour from now

        token = self.token_generator.generate_token(payload_vars)

        # When
        self.get(url=f"/session?token={token}")

        # Then
        self.assertStatusForbidden()

    def test_login_with_invalid_questionnaire_claims_should_be_forbidden_v2_get(self):
        # flag_1 should be a boolean
        token = self.token_generator.create_token_v2(
            "test_metadata_routing", flag_1=123
        )

        self.get(url=f"/session?token={token}")

        self.assertStatusForbidden()

    def test_login_with_invalid_version_should_be_forbidden(self):
        token = self.token_generator.create_token_invalid_version("test_checkbox")

        self.get(url=f"/session?token={token}")

        self.assertStatusForbidden()

    def test_login_token_with_schema_url_should_redirect_to_survey(self):
        schema_url = "http://eq-survey-register.url/my-test-schema"

        # Given
        token = self.token_generator.create_token_with_schema_url(schema_url)

        # When
        with HTTMock(self._schema_url_mock):
            self.get(url=f"/session?token={token}")

        self.assertStatusOK()
        self.assertInUrl("/questionnaire")

    def test_login_token_with_incorrect_schema_url_results_in_500(self):
        schema_url = "http://eq-survey-register.url/my-test-schema-not-found"

        # Given
        token = self.token_generator.create_token_with_schema_url(schema_url)

        # When
        with HTTMock(self._schema_url_mock_500):
            self.get(url=f"/session?token={token}")

        # Then
        self.assertException()

    @staticmethod
    @urlmatch(netloc=r"eq-survey-register", path=r"\/my-test-schema")
    def _schema_url_mock(_url, _request):
        schema_path = SCHEMA_PATH_MAP["test"]["en"]["test_textarea"]

        with open(schema_path, encoding="utf8") as json_data:
            return json_data.read()

    @staticmethod
    @urlmatch(netloc=r"eq-survey-register", path=r"\/my-test-schema-not-found")
    def _schema_url_mock_500(_url, _request):
        return response(500)


class TestLoginWithPostRequest(IntegrationTestCase):
    def test_login_with_no_token_should_be_unauthorized(self):
        # Given
        token = ""

        # When
        self.post(url=f"/session?token={token}")

        # Then
        self.assertStatusUnauthorised()

    def test_login_with_invalid_token_should_be_forbidden(self):
        # Given
        token = "123"

        # When
        self.post(url=f"/session?token={token}")

        # Then
        self.assertStatusForbidden()

    def test_login_with_valid_token_should_redirect_to_survey(self):
        # Given
        token = self.token_generator.create_token_v2("test_checkbox")

        # When
        self.post(url=f"/session?token={token}")

        # Then
        self.assertStatusOK()
        self.assertInUrl("/questionnaire")

    def test_login_with_token_twice_is_unauthorised_when_same_jti_provided(self):
        # Given
        token = self.token_generator.create_token_v2("test_checkbox")
        self.post(url=f"/session?token={token}")

        # When
        self.post(url=f"/session?token={token}")

        # Then
        self.assertStatusUnauthorised()

    def test_login_without_jti_in_token_is_unauthorised(self):
        # Given
        token = self.token_generator.create_token_without_jti("test_checkbox")
        self.post(url=f"/session?token={token}")

        # Then
        self.assertStatusForbidden()

    def test_http_head_request_to_login_returns_successfully_and_post_still_works(self):
        # Given
        token = self.token_generator.create_token_v2("test_checkbox")

        # When
        self.head(f"/session?token={token}")
        self.post(url=f"/session?token={token}")

        # Then
        self.assertStatusOK()
        self.assertInUrl("/questionnaire")

    def test_login_with_missing_mandatory_claims_should_be_forbidden(self):
        # Given
        payload_vars = PAYLOAD_V2_BUSINESS.copy()
        payload_vars["iat"] = time.time()
        payload_vars["exp"] = payload_vars["iat"] + float(3600)  # one hour from now

        token = self.token_generator.generate_token(payload_vars)

        # When
        self.post(url=f"/session?token={token}")

        # Then
        self.assertStatusForbidden()

    def test_login_with_invalid_questionnaire_claims_should_be_forbidden_v2_post(self):
        # flag_1 should be a boolean
        token = self.token_generator.create_token_v2(
            "test_metadata_routing", flag_1=123
        )

        self.get(url=f"/session?token={token}")

        self.assertStatusForbidden()

    def test_v2_business_login_with_invalid_questionnaire_claims_should_be_forbidden(
        self,
    ):
        # flag_1 should be a boolean
        token = self.token_generator.create_token_v2(
            "test_metadata_routing", flag_1=123
        )

        self.post(url=f"/session?token={token}")

        self.assertStatusForbidden()

    def test_v2_social_login_with_invalid_questionnaire_claims_should_be_forbidden(
        self,
    ):
        token = self.token_generator.create_token_v2(
            schema_name="test_address", theme="social"
        )

        self.post(url=f"/session?token={token}")

        self.assertStatusForbidden()

    def test_v2_social_login_with_invalid_receipting_key_should_be_forbidden(self):
        token = (
            self.token_generator.create_token_v2_social_token_invalid_receipting_key(
                "test_theme_social"
            )
        )

        self.post(url=f"/session?token={token}")

        self.assertStatusForbidden()

    def test_login_token_with_schema_url_should_redirect_to_survey(self):
        schema_url = "http://eq-survey-register.url/my-test-schema"

        # Given
        token = self.token_generator.create_token_with_schema_url(schema_url)

        # When
        with HTTMock(self._schema_url_mock):
            self.post(url=f"/session?token={token}")

        self.assertStatusOK()
        self.assertInUrl("/questionnaire")

    def test_login_token_with_incorrect_schema_url_results_in_404(self):
        schema_url = "http://eq-survey-register.url/my-test-schema-not-found"

        # Given
        token = self.token_generator.create_token_with_schema_url(schema_url)

        # When
        with HTTMock(self._schema_url_mock_500):
            self.post(url=f"/session?token={token}")

        # Then
        self.assertException()

    def test_login_without_case_id_in_token_is_unauthorised(self):
        # Given
        token = self.token_generator.create_token_without_case_id("test_textfield")
        self.post(url=f"/session?token={token}")

        # Then
        self.assertStatusForbidden()

    def test_login_token_with_cir_instrument_id_should_redirect_to_survey(self):
        cir_instrument_id = "f0519981-426c-8b93-75c0-bfc40c66fe25"

        # Given
        token = self.token_generator.create_token_with_cir_instrument_id(
            cir_instrument_id=cir_instrument_id
        )

        # When
        with HTTMock(self._cir_url_mock):
            self.post(url=f"/session?token={token}")

        # Then
        self.assertStatusOK()
        self.assertInUrl("/questionnaire")

    def test_login_token_with_invalid_cir_instrument_id_results_in_500(self):
        cir_instrument_id = "a0df1208-dff5-4a3d-b35d-f9620c4a48ef"

        # Given
        token = self.token_generator.create_token_with_cir_instrument_id(
            cir_instrument_id=cir_instrument_id
        )

        # When
        with HTTMock(self._cir_url_mock_500):
            self.post(url=f"/session?token={token}")

        # Then
        self.assertException()

    @staticmethod
    @urlmatch(netloc=r"eq-survey-register", path=r"\/my-test-schema")
    def _schema_url_mock(_url, _request):
        schema_path = SCHEMA_PATH_MAP["test"]["en"]["test_textarea"]

        with open(schema_path, encoding="utf8") as json_data:
            return json_data.read()

    @staticmethod
    @urlmatch(
        path=CIR_RETRIEVE_COLLECTION_INSTRUMENT_URL,
        query="guid=f0519981-426c-8b93-75c0-bfc40c66fe25",
    )
    def _cir_url_mock(_url, _request):
        schema_path = SCHEMA_PATH_MAP["test"]["en"]["test_textarea"]

        with open(schema_path, encoding="utf8") as json_data:
            return json_data.read()

    @staticmethod
    @urlmatch(
        path=CIR_RETRIEVE_COLLECTION_INSTRUMENT_URL,
        query="guid=a0df1208-dff5-4a3d-b35d-f9620c4a48ef",
    )
    def _cir_url_mock_500(_url, _request):
        return response(500)

    @staticmethod
    @urlmatch(netloc=r"eq-survey-register", path=r"\/my-test-schema-not-found")
    def _schema_url_mock_500(_url, _request):
        return response(500)
