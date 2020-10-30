from tests.integration.integration_test_case import IntegrationTestCase


class TestFeedback(IntegrationTestCase):
    SEND_FEEDBACK_URL = "/submitted/feedback/send"
    SENT_FEEDBACK_URL = "/submitted/feedback/sent"

    def test_questionnaire_not_completed(self):
        # Given I launch the test_feedback questionnaire
        self.launchSurvey("test_feedback")

        # When I try to view the feedback page without completing the questionnaire
        self.get(self.SEND_FEEDBACK_URL)

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_questionnaire_not_completed_post(self):
        # Given I launch the test_feedback questionnaire
        self.launchSurvey("test_feedback")

        # When I try to POST to the feedback page without completing the questionnaire
        self.post(url=self.SEND_FEEDBACK_URL)

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_feedback_sent_page_without_feedback_submitted(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()

        # When I try to view the feedback sent page without submitting feedback
        self.get(self.SENT_FEEDBACK_URL)

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_feedback_flag_not_set_in_schema(self):
        # Given I launch the test_textfield questionnaire
        self.launchSurvey("test_textfield")
        self.post()
        self.post()

        # When I complete the questionnaire and try to view the feedback page
        self.get(self.SEND_FEEDBACK_URL)

        # Then I get shown a 404 error
        self.assertStatusNotFound()

    def test_valid_feedback(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()
        self.get(self.SEND_FEEDBACK_URL)

        # When I enter a valid feedback and submit
        self.post(
            {"feedback-type": "Page design and structure", "feedback-text": "Feedback"}
        )

        # Then I get the feedback sent page
        self.assertInUrl(self.SENT_FEEDBACK_URL)
        self.assertInBody("Thank you for your feedback")

    def test_eleventh_submission_errors(self):
        # Given I launch and complete the test_feedback questionnaire, and provide feedback 11 times
        self._launch_and_complete_questionnaire()

        for _ in range(0, 11):
            self.get(self.SEND_FEEDBACK_URL)
            self.post(
                {
                    "feedback-type": "Page design and structure",
                    "feedback-text": "Feedback",
                }
            )

        # When I view the feedback sent page
        self.assertInUrl(self.SEND_FEEDBACK_URL)

        # Then an appropriate error is shown
        self.assertInBody(
            "You have reached the maximum number of times for submitting feedback"
        )

    def test_multiple_submissions(self):
        # Given I launch and complete the test_feedback questionnaire, and provide feedback
        self._launch_and_complete_questionnaire()
        self.get(self.SEND_FEEDBACK_URL)
        self.post(
            {"feedback-type": "Page design and structure", "feedback-text": "Feedback"}
        )
        self.assertInUrl(self.SENT_FEEDBACK_URL)

        # When I go to the feedback send page again
        self.get(self.SEND_FEEDBACK_URL)

        # Then I go to the feedback send page
        self.assertInUrl(self.SEND_FEEDBACK_URL)

    def test_feedback_type_missing(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()
        self.get(self.SEND_FEEDBACK_URL)

        # When I fail to select a feedback type from the radio boxes
        self.post({"feedback-text": "Feedback"})

        # Then I stay on the send page and am presented with an error
        self.assertInUrl(self.SEND_FEEDBACK_URL)
        self.assertInBody("There is a problem with your feedback")
        self.assertInBody("Select what your feedback is about")
        self.assertEqualPageTitle("Error: Feedback - Census 2021")

    def test_feedback_text_missing(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()
        self.get(self.SEND_FEEDBACK_URL)

        # When I fail to enter feedback text
        self.post({"feedback-type": "Page design and structure"})

        # Then I stay on the send page and am presented with an error
        self.assertInUrl(self.SEND_FEEDBACK_URL)
        self.assertInBody("There is a problem with your feedback")
        self.assertInBody("Enter your feedback")
        self.assertEqualPageTitle("Error: Feedback - Census 2021")

    def test_feedback_type_and_text_missing(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()
        self.get(self.SEND_FEEDBACK_URL)

        # When I submit without selecting a feedback type or provide text
        self.post()

        # Then I stay on the send page and am presented with an error
        self.assertInUrl(self.SEND_FEEDBACK_URL)
        self.assertInBody("There are 2 problems with your feedback")
        self.assertInBody("Select what your feedback is about")
        self.assertInBody("Enter your feedback")
        self.assertEqualPageTitle("Error: Feedback - Census 2021")

    def test_feedback_page_previous(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()
        self.get(self.SEND_FEEDBACK_URL)

        # When I choose previous
        self.previous()

        # Then I should be taken to the thank you page
        self.assertInUrl("/submitted/thank-you")

    def test_feedback_call_to_action_shown(self):
        # Given I launch and complete the test_feedback questionnaire
        self.launchSurvey("test_feedback")
        self.post({"answer_id": "Yes"})

        # When I view the thank you page
        self.post()

        # Then I should see the feedback call to action
        self.assertInBody("What do you think about this service?")
        self.assertInSelectorCSS("/submitted/feedback/send", class_="feedback__link")

    def _launch_and_complete_questionnaire(self):
        self.launchSurvey("test_feedback")
        self.post({"answer_id": "Yes"})
        self.post()
