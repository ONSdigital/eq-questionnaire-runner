from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaire(IntegrationTestCase):
    def test_head_request_on_optional_date(self):
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
        self.assertStatusCode(200)
