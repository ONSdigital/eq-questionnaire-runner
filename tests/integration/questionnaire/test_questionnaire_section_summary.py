from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireCalculatedSummary(IntegrationTestCase):
    def test_calculated_summary_headers_with_change_link(self):
        self.launchSurvey("test_section_summary")
        self.post()
        self.post()
        self.post()
        self.post()
        self.assertInBody(
            "<tr><th>Question</th><th>Answer given</th><th>Change answer</th></tr>"
        )

    def test_calculated_summary_headers_without_change_link(self):
        self.launchSurvey("test_view_submitted_response")
        self.post()
        self.post()
        self.post()
        self.get("/submitted/view-response/")
        self.assertInBody("<tr><th>Question</th><th>Answer given</th></tr>")
