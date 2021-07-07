from unittest.mock import Mock

from app import settings
from app.settings import EQ_FEEDBACK_LIMIT
from tests.integration.integration_test_case import IntegrationTestCase


class TestFeedback(IntegrationTestCase):
    SEND_FEEDBACK_URL = "/submitted/feedback/send"
    SENT_FEEDBACK_URL = "/submitted/feedback/sent"

    def setUp(self):
        settings.EQ_FEEDBACK_LIMIT = 2
        super().setUp()

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

    def test_valid_feedback_with_question_category(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()
        self.get(self.SEND_FEEDBACK_URL)
        # When I enter a valid feedback and submit
        self.post(
            {
                "feedback-type": "The census questions",
                "feedback-type-question-category": "Visitors",
                "feedback-text": "Feedback",
            }
        )
        # Then I get the feedback sent page
        self.assertInUrl(self.SENT_FEEDBACK_URL)
        self.assertInBody("Thank you for your feedback")

    def _test_feedback_show_warning(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()
        self.get(self.SEND_FEEDBACK_URL)

        # When I enter a valid feedback and submit
        self.post(
            {"feedback-type": "Page design and structure", "feedback-text": "Feedback"}
        )

        # Then I get a sign out warning
        self.assertInUrl(self.SENT_FEEDBACK_URL)
        self.assertInBody(
            'Make sure you <a href="/sign-out">leave this page</a> or close your browser if using a shared device'
        )

    def test_feedback_error_message_on_get_when_limit_reached(self):
        # Given I launch and complete the test_feedback questionnaire, and provide
        # feedback the maximum number of times
        self._launch_and_complete_questionnaire()

        for _ in range(0, EQ_FEEDBACK_LIMIT):
            self.get(self.SEND_FEEDBACK_URL)
            self.post(
                {
                    "feedback-type": "Page design and structure",
                    "feedback-text": "Feedback",
                }
            )

        # When I get the send feedback url
        self.get(self.SEND_FEEDBACK_URL)

        # Then an appropriate error is shown
        self.assertInBody(
            "You have reached the maximum number of times for submitting feedback"
        )

    def test_feedback_error_message_on_post_when_limit_reached(self):
        # Given I launch and complete the test_feedback questionnaire, and provide
        # feedback the maximum number of times
        self._launch_and_complete_questionnaire()

        for _ in range(0, EQ_FEEDBACK_LIMIT):
            self.get(self.SEND_FEEDBACK_URL)
            self.post(
                {
                    "feedback-type": "Page design and structure",
                    "feedback-text": "Feedback",
                }
            )

        self.get(self.SEND_FEEDBACK_URL)

        # When I post more feedback
        self.post(
            {
                "feedback-type": "Page design and structure",
                "feedback-text": "Feedback",
            }
        )

        # Then I should see an appropriate error
        self.assertInBody(
            "You have reached the maximum number of times for submitting feedback"
        )

    def test_send_feedback_back_breadcrumb(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()

        # When I view the send feedback page
        self.get(self.SEND_FEEDBACK_URL)

        # Then I should see the Back breadcrumb
        selector = "[id=top-previous]"
        self.assertInSelector("Back", selector)

    def test_submission(self):
        # Given I launch and complete the test_feedback questionnaire, and provide
        # feedback
        self._launch_and_complete_questionnaire()
        self.get(self.SEND_FEEDBACK_URL)
        self.post(
            {"feedback-type": "Page design and structure", "feedback-text": "Feedback"}
        )
        self.assertInUrl(self.SENT_FEEDBACK_URL)

    def test_multiple_submissions(self):
        # Given I launch and complete the test_feedback questionnaire, and provide
        # multiple feedback submissions
        self._launch_and_complete_questionnaire()
        self.get(self.SEND_FEEDBACK_URL)
        self.post(
            {"feedback-type": "Page design and structure", "feedback-text": "Feedback"}
        )
        self.get(self.SEND_FEEDBACK_URL)
        self.post(
            {"feedback-type": "Page design and structure", "feedback-text": "Feedback"}
        )

        self.assertInUrl("/submitted/feedback/sent")

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
        self.assertEqualPageTitle("Error: Feedback - Feedback test schema")

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
        self.assertEqualPageTitle("Error: Feedback - Feedback test schema")

    def test_feedback_question_category_missing(self):
        # Given I launch and complete the test_feedback questionnaire
        self._launch_and_complete_questionnaire()
        self.get(self.SEND_FEEDBACK_URL)

        # When I submit without selecting a feedback topic
        self.post(
            {"feedback-type": "The census questions", "feedback-text": "Feedback"}
        )

        # Then I stay on the send page and am presented with an error
        self.assertInUrl(self.SEND_FEEDBACK_URL)
        self.assertInBody("There is a problem with your feedback")
        self.assertInBody("Select an option")
        self.assertEqualPageTitle("Error: Feedback - Feedback test schema")

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
        self.assertEqualPageTitle("Error: Feedback - Feedback test schema")

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
        self._launch_and_complete_questionnaire()

        # Then I should see the feedback call to action
        self.assertInBody("What do you think about this service?")
        self.assertInSelectorCSS("/submitted/feedback/send", class_="feedback__link")

    def test_feedback_submission(self):
        # Given I submit the email confirmation form
        self.launchSurvey("test_feedback_email_confirmation")
        self.post({"answer_id": "Yes"})
        self.post()
        self.post({"email": "email@example.com"})

        # When I request the feedback page
        self.get("/submitted/feedback/send")

        # Then I am able to submit feedback
        self.post(
            {"feedback-type": "Page design and structure", "feedback-text": "Feedback"}
        )
        self.assertInUrl("/submitted/feedback/sent")

    def test_feedback_call_to_action_visible_on_email_confirmation(self):
        # Given I complete the survey
        self.launchSurvey("test_feedback_email_confirmation")
        self.post({"answer_id": "Yes"})
        self.post()

        # When I submit the email confirmation form
        self.post({"email": "email@example.com"})
        self.post({"confirm-email": "Yes, send the confirmation email"})

        # Then I should see the feedback call to action
        self.assertInBody("What do you think about this service?")

    def test_feedback_submission_from_email_confirmation(self):
        # Given I submit the email confirmation form
        self.launchSurvey("test_feedback_email_confirmation")
        self.post({"answer_id": "Yes"})
        self.post()
        self.post({"email": "email@example.com"})

        # When I request the feedback page
        self.get("/submitted/feedback/send")

        # Then I am able to submit feedback
        self.post(
            {"feedback-type": "Page design and structure", "feedback-text": "Feedback"}
        )
        self.assertInUrl("/submitted/feedback/sent")

    def test_feedback_back_breadcrumb_after_email_confirmation(self):
        # Given I submit the email confirmation form
        self.launchSurvey("test_feedback_email_confirmation")
        self.post({"answer_id": "Yes"})
        self.post()
        self.post({"email": "email@example.com"})

        # When I request the feedback send page
        self.get("/submitted/feedback/send")

        # Then the back breadcrumb should navigate to the thank you page
        selector = "[id=top-previous]"
        self.assertInSelector("/submitted/thank-you", selector)

    def test_feedback_submitted_done_button_after_email_confirmation(self):
        # Given I submit the email confirmation form after submitting feedback
        self.launchSurvey("test_feedback_email_confirmation")
        self.post({"answer_id": "Yes"})
        self.post()
        self.get("/submitted/feedback/send")
        self.post(
            {"feedback-type": "Page design and structure", "feedback-text": "Feedback"}
        )
        self.post()
        self.post({"email": "email@example.com"})

        # When I request the feedback sent page
        self.get("/submitted/feedback/sent")

        # Then the done button should navigate to the thank you page
        selector = "[data-qa='btn-done']"
        self.assertInSelector("/submitted/thank-you", selector)

    def test_feedback_upload_failed(self):
        # Given I launch and complete the test_feedback question, mocking the upload to return false
        feedback = self._application.eq["feedback_submitter"]
        feedback.upload = Mock(return_value=False)
        self._launch_and_complete_questionnaire()
        self.get("/submitted/feedback/send")

        # When I post my feedback
        self.post(
            {"feedback-type": "Page design and structure", "feedback-text": "Feedback"}
        )

        # Then I should see an error page
        self.assertStatusCode(500)
        self.assertEqualPageTitle("Sorry, there is a problem - Feedback test schema")
        self.assertInBody("submit your feedback again")

        retry_url = (
            self.getHtmlSoup().find("p", {"data-qa": "retry"}).find("a").attrs["href"]
        )
        self.get(retry_url)
        self.assertInUrl("/submitted/feedback/send")

    def test_head_request_on_feedback(self):
        self._launch_and_complete_questionnaire()
        self.head("/submitted/feedback/send")
        self.assertStatusOK()

    def test_head_request_on_feedback_sent(self):
        self._launch_and_complete_questionnaire()
        self.get("/submitted/feedback/send")
        self.post(
            {
                "feedback-type": "General feedback about this service",
                "feedback-text": "Some feedback",
            }
        )
        self.head("/submitted/feedback/sent")
        self.assertStatusOK()

    def _launch_and_complete_questionnaire(self):
        self.launchSurvey("test_feedback")
        self.post({"answer_id": "Yes"})
        self.post()
