from unittest.mock import Mock

from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import HUB_URL, THANK_YOU_URL

FINAL_SUMMARY = "/questionnaire/summary/"
FINAL_CONFIRMATION = "/questionnaire/confirmation/"


class SubmissionTestCase(IntegrationTestCase):
    @property
    def retry_url(self):
        return (
            self.getHtmlSoup().find("p", {"data-qa": "retry"}).find("a").attrs["href"]
        )

    def _mock_submission_failure(self):
        submitter = self._application.eq["submitter"]
        submitter.send_message = Mock(return_value=False)


class TestQuestionnaireSubmissionFinalConfirmation(SubmissionTestCase):
    def _launch_and_submit_questionnaire(self):
        # Launch questionnaire
        self.launchSurvey("test_final_confirmation")

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
        self.assertInUrl(THANK_YOU_URL)

    def test_unsuccessful_submission(self):
        self._mock_submission_failure()

        # Given I launch and answer a questionnaire, When I submit but the submissions fails
        self._launch_and_submit_questionnaire()

        # Then I should see an error page
        self.assertStatusCode(500)
        self.assertEqualPageTitle("Sorry, there is a problem - Census 2021")

        self.get(self.retry_url)
        self.assertInUrl(FINAL_CONFIRMATION)


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
        self.post({"relationships-answer": "No"})
        self.post()
        self.post()

    def test_successful_submission(self):
        # Given I launch and answer a questionnaire, When I submit and the submissions succeeds
        self._launch_and_submit_questionnaire()

        # Then I should see the thank you page
        self.assertInBody(
            "Your answers were submitted for <span>Integration Testing</span>"
        )
        self.assertEqualUrl(THANK_YOU_URL)

    def test_unsuccessful_submission(self):
        self._mock_submission_failure()

        # Given I launch and answer a questionnaire, When I submit but the submissions fails
        self._launch_and_submit_questionnaire()

        # Then I should see an error page
        self.assertStatusCode(500)
        self.assertEqualPageTitle("Sorry, there is a problem - Census 2021")

        self.get(self.retry_url)
        self.assertInUrl(HUB_URL)


class TestQuestionnaireSubmissionFinalSummary(SubmissionTestCase):
    def _launch_and_submit_questionnaire(self):
        # Launch questionnaire
        self.launchSurvey("test_summary")

        # Answer questions and submit survey
        self.post()
        self.post()
        self.post()
        self.post()

    def test_successful_submission(self):
        # Given I launch and answer a questionnaire, When I submit and the submissions succeeds
        self._launch_and_submit_questionnaire()

        # Then I should see the thank you page
        self.assertInBody(
            "Your answers were submitted for <span>Integration Testing</span>"
        )
        self.assertInUrl(THANK_YOU_URL)

    def test_unsuccessful_submission(self):
        self._mock_submission_failure()

        # Given I launch and answer a questionnaire, When I submit but the submissions fails
        self.launchSurvey("test_summary")
        self.post()
        self.post()
        self.post()
        self.post()

        # Then I should see an error page
        self.assertStatusCode(500)
        self.assertEqualPageTitle("Sorry, there is a problem - Census 2021")

        self.get(self.retry_url)
        self.assertInUrl(FINAL_SUMMARY)
