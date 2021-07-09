from unittest.mock import Mock

from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import HUB_URL_PATH, THANK_YOU_URL_PATH

SUBMIT_URL_PATH = "/questionnaire/submit"


class SubmissionTestCase(IntegrationTestCase):
    @property
    def retry_url(self):
        return (
            self.getHtmlSoup().find("p", {"data-qa": "retry"}).find("a").attrs["href"]
        )

    def _mock_submission_failure(self):
        submitter = self._application.eq["submitter"]
        submitter.send_message = Mock(return_value=False)


class TestQuestionnaireSubmission(SubmissionTestCase):
    def _launch_and_submit_questionnaire(self):
        # Launch questionnaire
        self.launchSurvey("test_submit_with_custom_submission_text")

        # Answer questions and submit survey
        self.post(action="start_questionnaire")
        self.post()
        self.post()

    def test_successful_submission(self):
        # Given I launch and answer a questionnaire, When I submit and the submissions succeeds
        self._launch_and_submit_questionnaire()

        # Then I should see the thank you page
        self.assertInBody(
            "Your answers were submitted for <span>Integration Testing</span>"
        )
        self.assertInUrl(THANK_YOU_URL_PATH)

    def test_unsuccessful_submission(self):
        self._mock_submission_failure()

        # Given I launch and answer a questionnaire, When I submit but the submissions fails
        self._launch_and_submit_questionnaire()

        # Then I should see an error page
        self.assertStatusCode(500)
        self.assertEqualPageTitle("Sorry, there is a problem - Submit without summary")

        self.get(self.retry_url)
        self.assertInUrl(SUBMIT_URL_PATH)


class TestQuestionnaireSubmissionHub(SubmissionTestCase):
    def _launch_and_submit_questionnaire(self):
        # Launch questionnaire
        self.launchSurvey("test_hub_and_spoke")

        # Answer questions and submit questionnaire
        self.post()
        self.post({"employment-status-answer": "Working as an employee"})
        self.post()
        self.post()
        self.post()
        self.post()
        self.post({"does-anyone-live-here-answer": "No"})
        self.post()
        self.post()
        self.post({"anyone-related-answer": "No"})
        self.post()
        self.post()

    def test_successful_submission(self):
        # Given I launch and answer a questionnaire, When I submit and the submissions succeeds
        self._launch_and_submit_questionnaire()

        # Then I should see the thank you page
        self.assertInBody(
            "Your answers were submitted for <span>Integration Testing</span>"
        )
        self.assertEqualUrl(THANK_YOU_URL_PATH)

    def test_unsuccessful_submission(self):
        self._mock_submission_failure()

        # Given I launch and answer a questionnaire, When I submit but the submissions fails
        self._launch_and_submit_questionnaire()

        # Then I should see an error page
        self.assertStatusCode(500)
        self.assertEqualPageTitle("Sorry, there is a problem - Hub & Spoke")

        self.get(self.retry_url)
        self.assertInUrl(HUB_URL_PATH)


class TestQuestionnaireSubmissionWithSummary(SubmissionTestCase):
    def _launch_and_submit_questionnaire(self):
        # Launch questionnaire
        self.launchSurvey("test_submit_with_summary")

        # Answer questions and submit survey
        self.post()
        self.post({"dessert-answer": "Cake"})
        self.post({"dessert-confirmation-answer": "Yes"})
        self.post()
        self.post()

    def test_successful_submission(self):
        # Given I launch and answer a questionnaire, When I submit and the submissions succeeds
        self._launch_and_submit_questionnaire()

        # Then I should see the thank you page
        self.assertInBody(
            "Your answers were submitted for <span>Integration Testing</span>"
        )
        self.assertInUrl(THANK_YOU_URL_PATH)

    def test_unsuccessful_submission(self):
        self._mock_submission_failure()

        # Given I launch and answer a questionnaire, When I submit but the submissions fails
        self.launchSurvey("test_submit_with_summary")
        self.post()
        self.post({"dessert-answer": "Cake"})
        self.post({"dessert-confirmation-answer": "Yes"})
        self.post()
        self.post()

        # Then I should see an error page
        self.assertStatusCode(500)
        self.assertEqualPageTitle("Sorry, there is a problem - Other input fields")

        self.get(self.retry_url)
        self.assertInUrl(SUBMIT_URL_PATH)
