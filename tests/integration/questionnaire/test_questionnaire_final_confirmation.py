from unittest.mock import Mock

from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireFinalConfirmation(IntegrationTestCase):
    def test_final_confirmation_asked_at_end_of_questionnaire(self):
        # Given
        self.launchSurvey("test_final_confirmation")

        # When we proceed through the questionnaire
        self.post(action="start_questionnaire")
        self.assertInBody("What is your favourite breakfast food")
        self.post({"breakfast-answer": "Bacon"})

        # Then we are presented with a confirmation page
        self.assertInUrl("confirmation")
        self.assertInBody("Thank you for your answers, do you wish to submit")
        self.assertInBody("Submit answers")

    def test_requesting_final_confirmation_before_finished_raises_404(self):
        # Given
        self.launchSurvey("test_final_confirmation")

        # When we proceed through the questionnaire
        self.post(action="start_questionnaire")
        self.assertInBody("What is your favourite breakfast food")

        # And try posting straight to the confirmation screen
        self.post(url="/questionnaire/confirmation")

        # Then we are shown a 404 page
        self.assertStatusNotFound()

    def test_invalid_block_once_survey_complete_raises_404(self):
        # Given
        self.launchSurvey("test_final_confirmation")

        # When we proceed through the questionnaire
        self.post(action="start_questionnaire")
        self.post({"breakfast-answer": "Bacon"})

        # And try going to an invalid block
        self.get(url="/questionnaire/invalid")

        # Then we are shown a 404 page
        self.assertStatusNotFound()

    def test_unsuccessful_survey_submission_raises_500(self):
        submitter = self._application.eq["submitter"]
        submitter.send_message = Mock(return_value=False)

        # Given I launch a survey with a final confirmation, When I submit the survey but submission fails
        self.launchSurvey("test_final_confirmation")
        self.post(action="start_questionnaire")
        self.post()
        self.post()

        # Then I should see an error page
        self.assertStatusCode(500)
        self.assertEqualPageTitle("Sorry, there is a problem - Census 2021")

        retry_url = (
            self.getHtmlSoup().find("p", {"data-qa": "retry"}).find("a").attrs["href"]
        )
        self.get(retry_url)
        self.assertInUrl("questionnaire/confirmation/")
