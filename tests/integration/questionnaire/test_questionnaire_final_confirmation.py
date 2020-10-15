from tests.integration.integration_test_case import IntegrationTestCase

FINAL_CONFIRMATION = "/questionnaire/confirmation/"


class TestQuestionnaireFinalConfirmation(IntegrationTestCase):
    def test_final_confirmation_asked_at_end_of_questionnaire(self):
        # Given
        self.launchSurvey("test_final_confirmation")

        # When we proceed through the questionnaire
        self.post(action="start_questionnaire")
        self.assertInBody("What is your favourite breakfast food")
        self.post({"breakfast-answer": "Bacon"})

        # Then we are presented with a confirmation page
        self.assertInUrl(FINAL_CONFIRMATION)
        self.assertInBody("Thank you for your answers, do you wish to submit")
        self.assertInBody("Submit answers")

    def test_requesting_final_confirmation_before_finished_raises_404(self):
        # Given
        self.launchSurvey("test_final_confirmation")

        # When we proceed through the questionnaire
        self.post(action="start_questionnaire")
        self.assertInBody("What is your favourite breakfast food")

        # And try posting straight to the confirmation screen
        self.post(url=FINAL_CONFIRMATION)

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
