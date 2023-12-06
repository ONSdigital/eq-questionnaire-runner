import time
import uuid

from httmock import HTTMock, urlmatch
from mock import patch

from app.utilities.schema import (
    CIR_RETRIEVE_COLLECTION_INSTRUMENT_URL,
    get_schema_path_map,
)
from tests.app.parser.conftest import get_response_expires_at
from tests.integration.integration_test_case import IntegrationTestCase

SCHEMA_PATH_MAP = get_schema_path_map(include_test_schemas=True)


class TestFlushData(IntegrationTestCase):
    def setUp(self):
        self.submitter_patcher = patch("app.setup.LogSubmitter")
        mock_submitter_class = self.submitter_patcher.start()
        self.submitter_instance = mock_submitter_class.return_value
        self.submitter_instance.send_message.return_value = True

        self.encrypter_patcher = patch("app.routes.flush.encrypt")
        mock_encrypter_class = self.encrypter_patcher.start()
        self.encrypt_instance = mock_encrypter_class

        super().setUp()
        self.launchSurvey("test_textfield")

        form_data = {"name-answer": "Joe Bloggs"}
        self.post(form_data)

    def tearDown(self):
        self.submitter_patcher.stop()
        self.encrypter_patcher.stop()

        super().tearDown()

    @staticmethod
    @urlmatch(netloc=r"eq-survey-register", path=r"\/my-test-schema")
    def schema_url_mock(_url, _request):
        schema_path = SCHEMA_PATH_MAP["test"]["en"]["test_textfield"]

        with open(schema_path, encoding="utf8") as json_data:
            return json_data.read()

    @staticmethod
    @urlmatch(
        path=CIR_RETRIEVE_COLLECTION_INSTRUMENT_URL,
        query="guid=f0519981-426c-8b93-75c0-bfc40c66fe25",
    )
    def cir_url_mock(_url, _request):
        schema_path = SCHEMA_PATH_MAP["test"]["en"]["test_textarea"]

        with open(schema_path, encoding="utf8") as json_data:
            return json_data.read()

    def test_flush_data_successful(self):
        self.post(
            url="/flush?token="
            + self.token_generator.generate_token(self.get_payload())
        )
        self.assertStatusOK()

    def test_no_data_to_flush(self):
        payload = self.get_payload()
        # Made up response_id
        payload["response_id"] = "0000000000000000"

        self.post(url="/flush?token=" + self.token_generator.generate_token(payload))
        self.assertStatusCode(404)

    def test_no_permission_to_flush(self):
        payload = self.get_payload()
        # A role with no flush permissions
        payload["roles"] = ["test"]

        self.post(url="/flush?token=" + self.token_generator.generate_token(payload))
        self.assertStatusForbidden()

    def test_no_role_on_token(self):
        payload = self.get_payload()
        # Payload with no roles
        del payload["roles"]

        self.post(url="/flush?token=" + self.token_generator.generate_token(payload))
        self.assertStatusForbidden()

    def test_double_flush(self):
        self.post(
            url="/flush?token="
            + self.token_generator.generate_token(self.get_payload())
        )

        # Once the data has been flushed it is wiped.
        # It can't be flushed again and should return 404 no data on second flush
        self.post(
            url="/flush?token="
            + self.token_generator.generate_token(self.get_payload())
        )
        self.assertStatusCode(404)

    def test_no_token_passed_to_flush(self):
        self.post(url="/flush")
        self.assertStatusForbidden()

    def test_invalid_token_passed_to_flush(self):
        self.post(url="/flush?token=test")
        self.assertStatusForbidden()

    def test_flush_errors_when_submission_fails(self):
        self.submitter_instance.send_message.return_value = False

        self.post(
            url="/flush?token="
            + self.token_generator.generate_token(self.get_payload())
        )
        self.assertStatusCode(500)

    def test_flush_sets_flushed_flag_to_true(self):
        self.post(
            url="/flush?token="
            + self.token_generator.generate_token(self.get_payload())
        )

        self.encrypt_instance.assert_called_once()
        args = self.encrypt_instance.call_args[0]

        self.assertTrue('"flushed": true' in args[0])

    @staticmethod
    def get_payload():
        return {
            "jti": str(uuid.uuid4()),
            "iat": time.time(),
            "exp": time.time() + 1000,
            "response_id": "1234567890123456",
            "roles": ["flusher"],
        }

    @patch("app.routes.flush.convert_answers_v2")
    @patch("app.routes.flush.convert_answers")
    def test_flush_data_successful_v1(
        self, mock_convert_answers, mock_convert_answers_v2
    ):
        mock_convert_answer_payload = {
            "case_id": "7e0fd167-36af-4506-806d-421e5ba3544b",
            "tx_id": "5432e910-c6ef-418a-abcc-a8de8c23b0f9",
            "type": "uk.gov.ons.edc.eq:surveyresponse",
            "version": "0.0.3",
            "origin": "uk.gov.ons.edc.eq",
            "survey_id": "001",
            "flushed": True,
            "submitted_at": "2023-02-07T11:41:12.126783+00:00",
            "collection": {
                "exercise_sid": "f9fb5e81-9820-44cc-a2c3-16bf382b4d8d",
                "schema_name": "test_textfield",
                "period": "201605",
            },
            "metadata": {"user_id": "UNKNOWN", "ru_ref": "12346789012A"},
            "launch_language_code": "en",
            "data": {
                "answers": [{"answer_id": "name-answer", "value": "sdfsdaf"}],
                "lists": [],
            },
            "started_at": "2023-02-07T11:40:46.845149+00:00",
        }
        mock_convert_answers.return_value = mock_convert_answer_payload
        self.post(
            url="/flush?token="
            + self.token_generator.generate_token(self.get_payload())
        )
        self.assertStatusOK()
        mock_convert_answers.assert_called_once()
        mock_convert_answers_v2.assert_not_called()

    @patch("app.routes.flush.convert_answers_v2")
    @patch("app.routes.flush.convert_answers")
    def test_flush_data_successful_v2(
        self, mock_convert_answers, mock_convert_answers_v2
    ):
        mock_convert_answer_payload = {
            "case_id": "19300487-87e7-42df-9330-718efb08e660",
            "tx_id": "5d8b97f7-c8bd-42e1-88c9-e7721388463b",
            "type": "uk.gov.ons.edc.eq:surveyresponse",
            "version": "v2",
            "data_version": "0.0.3",
            "origin": "uk.gov.ons.edc.eq",
            "collection_exercise_sid": "1eeb58ec-bae7-414d-a02e-5c3c23052dc7",
            "schema_name": "test_textfield",
            "flushed": True,
            "submitted_at": "2023-02-07T11:42:59.575214+00:00",
            "launch_language_code": "en",
            "survey_metadata": {
                "survey_id": "001",
                "period_id": "201605",
                "ru_name": "ESSENTIAL ENTERPRISE LTD.",
                "user_id": "UNKNOWN",
                "ru_ref": "12346789012A",
            },
            "data": {
                "answers": [{"answer_id": "name-answer", "value": "sdfsdf"}],
                "lists": [],
            },
            "started_at": "2023-02-07T11:42:32.380784+00:00",
            "response_expires_at": get_response_expires_at(),
        }
        self.launchSurveyV2("test_textfield")
        form_data = {"name-answer": "Joe Bloggs"}
        self.post(form_data)
        mock_convert_answers_v2.return_value = mock_convert_answer_payload
        self.post(
            url="/flush?token="
            + self.token_generator.generate_token(self.get_payload())
        )
        self.assertStatusOK()
        mock_convert_answers_v2.assert_called_once()
        mock_convert_answers.assert_not_called()

    def test_flush_logs_output(self):
        with self.assertLogs() as logs:
            self.post(
                url=f"/flush?token={self.token_generator.create_token(schema_name='test_textfield', payload=self.get_payload())}"
            )

            flush_log = logs.output[5]

            self.assertIn("successfully flushed answers", flush_log)
            self.assertIn("tx_id", flush_log)
            self.assertIn("ce_id", flush_log)
            self.assertIn("schema_name", flush_log)
            self.assertNotIn("schema_url", flush_log)

    def test_flush_logs_output_schema_url(self):
        schema_url = "http://eq-survey-register.url/my-test-schema"
        token = self.token_generator.create_token_with_schema_url(
            "test_textfield", schema_url
        )
        with HTTMock(self.schema_url_mock):
            self.get(url=f"/session?token={token}")
            self.assertStatusOK()
            with self.assertLogs() as logs:
                self.post(
                    url=f"/flush?token={self.token_generator.create_token_with_schema_url('test_textfield', schema_url, payload=self.get_payload())}"
                )

                flush_log = logs.output[5]

                self.assertIn("successfully flushed answers", flush_log)
                self.assertIn("tx_id", flush_log)
                self.assertIn("ce_id", flush_log)
                self.assertIn("schema_name", flush_log)
                self.assertIn("schema_url", flush_log)

    def test_flush_logs_output_cir_instrument_id(self):
        token = self.token_generator.create_token_with_cir_instrument_id(
            cir_instrument_id="f0519981-426c-8b93-75c0-bfc40c66fe25"
        )
        with HTTMock(self.cir_url_mock):
            self.get(url=f"/session?token={token}")
            self.assertStatusOK()
            with self.assertLogs() as logs:
                token_with_flush_role = (
                    self.token_generator.create_token_with_cir_instrument_id(
                        cir_instrument_id="f0519981-426c-8b93-75c0-bfc40c66fe25",
                        payload=self.get_payload(),
                    )
                )
                self.post(url=f"/flush?token={token_with_flush_role}")

                flush_log = logs.output[6]

                self.assertIn("successfully flushed answers", flush_log)
                self.assertIn("tx_id", flush_log)
                self.assertIn("ce_id", flush_log)
                self.assertIn("cir_instrument_id", flush_log)
