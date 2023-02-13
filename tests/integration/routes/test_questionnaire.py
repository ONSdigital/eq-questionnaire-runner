from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaire(IntegrationTestCase):
    def test_head_request_on_root_url(self):
        self.launchSurvey("test_hub_and_spoke")
        self.head("/questionnaire/")
        self.assertStatusOK()

    def test_head_request_on_section_url(self):
        self.launchSurvey("test_hub_and_spoke")
        self.head("/questionnaire/sections/employment-section")
        self.assertStatusCode(302)

    def test_head_request_on_block_url(self):
        self.launchSurvey("test_textfield")
        self.head("/questionnaire/name-block")
        self.assertStatusOK()

    def test_head_request_on_block_with_optional_date_answer(self):
        self.launchSurvey("test_dates")
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
        self.launchSurvey("test_hub_and_spoke")
        with self.assertLogs() as logs:
            self.options("/questionnaire/")
            self.assertStatusOK()

        for output in logs.output:
            self.assertNotIn("questionnaire request", output)

    def test_get_request_logs_output(self):
        self.launchSurvey("test_hub_and_spoke")
        with self.assertLogs() as logs:
            self.get("/questionnaire/")
            self.assertStatusOK()

        for output in logs.output:
            self.assertIn("tx_id", output)
            self.assertIn("ce_id", output)
            self.assertIn("schema_name", output)
            self.assertIn("request_id", output)
