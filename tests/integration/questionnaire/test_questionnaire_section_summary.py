from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireCalculatedSummary(IntegrationTestCase):
    def test_calculated_summary_headers_with_change_link(self):
        self.launchSurvey("test_section_summary")
        self.post()
        self.post()
        self.post()
        self.post()
        self.assertInBody("<th>Question</th>")
        self.assertInBody("<th>Answer given</th>")
        self.assertInBody("<th>Change answer</th>")

    def test_calculated_summary_headers_without_change_link(self):
        self.launchSurvey("test_view_submitted_response")
        self.post()
        self.post()
        self.post()
        self.get("/submitted/view-response/")
        self.assertInBody("<th>Question</th>")
        self.assertInBody("<th>Answer given</th>")
        self.assertNotInBody("<th>Change answer</th>")
