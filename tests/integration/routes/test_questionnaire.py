from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaire(IntegrationTestCase):
    def test_head_request_on_root_url(self):
        self.launchSurveyV2(schema_name="test_hub_and_spoke")
        self.head("/questionnaire/")
        self.assertStatusOK()

    def test_head_request_on_section_url(self):
        self.launchSurveyV2(schema_name="test_hub_and_spoke")
        self.head("/questionnaire/sections/employment-section")
        self.assertStatusCode(302)

    def test_head_request_on_block_url(self):
        self.launchSurveyV2(schema_name="test_textfield")
        self.head("/questionnaire/name-block")
        self.assertStatusOK()

    def test_head_request_on_block_with_optional_date_answer(self):
        self.launchSurveyV2(schema_name="test_dates")
        self.post(
            {
                "date-range-from-answer-day": "1",
                "date-range-from-answer-month": "1",
                "date-range-from-answer-year": "1900",
                "date-range-to-answer-day": "1",
                "date-range-to-answer-month": "1",
                "date-range-to-answer-year": "1901",
            }
        )
        self.post(
            {
                "month-year-answer-month": "1",
                "month-year-answer-year": "1900",
            }
        )
        self.post(
            {
                "single-date-answer-day": "1",
                "single-date-answer-month": "1",
                "single-date-answer-year": "1900",
            }
        )
        self.head("/questionnaire/date-non-mandatory-block/")
        self.assertStatusOK()

    def test_options_request_before_request(self):
        self.launchSurveyV2(schema_name="test_hub_and_spoke")
        with self.assertLogs() as logs:
            self.options("/questionnaire/")
            self.assertStatusOK()

        for output in logs.output:
            self.assertNotIn("questionnaire request", output)

    def test_get_request_logs_output(self):
        self.launchSurveyV2(schema_name="test_hub_and_spoke")
        with self.assertLogs() as logs:
            self.get("/questionnaire/")
            self.assertStatusOK()

            request_log = logs.output[0]
            questionnaire_request_log = logs.output[1]

            self.assertNotIn("tx_id", request_log)
            self.assertNotIn("ce_id", request_log)
            self.assertNotIn("schema_name", request_log)
            self.assertIn("url_path", request_log)
            self.assertIn("request_id", request_log)
            self.assertIn("method", request_log)

            self.assertIn("tx_id", questionnaire_request_log)
            self.assertIn("ce_id", questionnaire_request_log)
            self.assertIn("schema_name", questionnaire_request_log)
            self.assertIn("url_path", questionnaire_request_log)
            self.assertIn("request_id", questionnaire_request_log)
            self.assertIn("method", questionnaire_request_log)
