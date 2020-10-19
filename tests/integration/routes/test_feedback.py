from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class TestFeedback(IntegrationTestCase):
    def test_questionnaire_not_completed(self):
        # Given I launch the test_feedback questionnaire
        self.launchSurvey("test_feedback")

        # When I try to view the feedback page without completing the questionnaire
        self.get("/submitted/feedback/send")

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_questionnaire_not_completed_post(self):
        # Given I launch the test_feedback questionnaire
        self.launchSurvey("test_feedback")

        # When I try to POST to the feedback page without completing the questionnaire
        self.post(url="/submitted/feedback/send")

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_feedback_sent_page_without_feedback_submitted(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()

        # When I try to view the feedback sent page without submitting feedback
        self.get("/submitted/feedback/sent")

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_feedback_flag_not_set_in_schema(self):
        # Given I launch the test_textfield questionnaire
        self.launchSurvey("test_textfield")
        self.post()
        self.post()

        # When I complete the questionnaire and try to view the feedback page
        self.get("/submitted/feedback/send")

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_valid_feedback(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()
        self.get("/submitted/feedback/send")

        # When I enter a valid feedback and submit
        self.post(
            {"feedback-type": "Page design and structure", "feedback-text": "Feedback"}
        )

        # Then I get the feedback sent page
        self.assertInUrl("feedback/sent")
        self.assertInBody("Thank you for your feedback")

    def test_second_submission(self):
        # Given I launch and complete the test_feedback questionnaire, and provide feedback
        self._launch_and_complete_questionnaire()
        self.get("/submitted/feedback/send")
        self.post(
            {"feedback-type": "Page design and structure", "feedback-text": "Feedback"}
        )
        self.assertInUrl("feedback/sent")

        # When I go to the feedback send page again
        self.get("/submitted/feedback/send")

        # Then I get redirected to the sent page
        self.assertInUrl("feedback/sent")

    def test_feedback_type_missing(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()
        self.get("/submitted/feedback/send")

        # When I fail to select a feedback type from the radio boxes
        self.post({"feedback-text": "Feedback"})

        # Then I stay on the send page and am presented with an error
        self.assertInUrl("feedback/send")
        self.assertInBody("There is a problem with your answer")
        self.assertInBody("Select what your feedback is about")
        self.assertEqualPageTitle("Error: Feedback - Census 2021")

    def test_feedback_text_missing(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()
        self.get("/submitted/feedback/send")

        # When I fail to enter feedback text
        self.post({"feedback-type": "Page design and structure"})

        # Then I stay on the send page and am presented with an error
        self.assertInUrl("feedback/send")
        self.assertInBody("There is a problem with your answer")
        self.assertInBody("Enter your feedback")
        self.assertEqualPageTitle("Error: Feedback - Census 2021")

    def test_feedback_type_and_text_missing(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()
        self.get("/submitted/feedback/send")

        # When I submit without selecting a feedback type or provide text
        self.post()

        # Then I stay on the send page and am presented with an error
        self.assertInUrl("feedback/send")
        self.assertInBody("There are 2 problems with your answer")
        self.assertInBody("Select what your feedback is about")
        self.assertInBody("Enter your feedback")
        self.assertEqualPageTitle("Error: Feedback - Census 2021")

    def test_feedback_page_previous(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()
        self.get("/submitted/feedback/send")

        # When I choose previous
        self.previous()

        # Then I should be taken to the thank you page
        self.assertInUrl("/submitted/thank-you")

    def _launch_and_complete_questionnaire(self):
        self.launchSurvey("test_feedback")
        self.post({"answer_id": "Yes"})
        self.post()
