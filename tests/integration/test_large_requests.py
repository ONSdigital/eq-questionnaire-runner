from tests.integration.integration_test_case import IntegrationTestCase


class TestLargeRequests(IntegrationTestCase):
    def test_large_request_under_limit(self):
        self.launchSurveyV2(schema_name="test_percentage")
        number = "1" + ("1" * 110_000) + "1"
        self.post({"answer": number})
        self.assertStatusOK()

    def test_large_request_over_limit(self):
        self.launchSurveyV2(schema_name="test_percentage")
        number = "1" + ("1" * 130_000) + "1"
        self.post({"answer": number})
        self.assertException()
