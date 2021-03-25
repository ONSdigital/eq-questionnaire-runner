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

    def test_options_request_on_root_url(self):
        self.launchSurvey("test_hub_and_spoke")
        self.options("/questionnaire/")
        self.assertStatusOK()

    def test_options_request_on_section_url(self):
        self.launchSurvey("test_hub_and_spoke")
        self.options("/questionnaire/sections/employment-section")
        self.assertStatusCode(200)

    def test_options_request_on_block_url(self):
        self.launchSurvey("test_textfield")
        self.options("/questionnaire/name-block")
        self.assertStatusOK()

    def test_options_request_on_block_with_optional_date_answer(self):
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
        self.options("/questionnaire/date-non-mandatory-block/")
        self.assertStatusOK()
