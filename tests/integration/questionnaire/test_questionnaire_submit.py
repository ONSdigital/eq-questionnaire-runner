from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import SUBMIT_URL_PATH, THANK_YOU_URL_PATH


class TestQuestionnaireSubmit(IntegrationTestCase):
    def _launch_and_complete_questionnaire(self, schema):
        self.launchSurvey(schema)
        self.post({"test-skipping-answer": "No"})

    def test_submit_page_not_accessible_when_hub_enabled(self):
        # Given I launch a hub questionnaire
        self.launchSurvey("test_hub_and_spoke")

        # When I try access the submit page
        for method in [self.get, self.post]:
            with self.subTest(method=method):
                method(url=SUBMIT_URL_PATH)

                # Then I am shown a 404 page
                self.assertStatusNotFound()

    def test_invalid_block_once_questionnaire_complete_raises_404(self):
        # Given I launch questionnaire
        self.launchSurvey("test_final_confirmation")

        # When I proceed through the questionnaire
        self.post(action="start_questionnaire")
        self.post({"breakfast-answer": "Bacon"})
        self.assertInUrl(SUBMIT_URL_PATH)

        # And try going to an invalid block
        self.get(url="/questionnaire/invalid")

        # Then I am shown a 404 page
        self.assertStatusNotFound()

    def test_submit_page_not_available_after_invalidating_section(self):
        # Given I launch and complete the questionnaire
        for schema in [
            "test_skipping_to_questionnaire_end_single_section",
            "test_skipping_to_questionnaire_end_multiple_sections",
        ]:
            with self.subTest(schema=schema):
                self.launchSurvey(schema)
                self.post({"test-skipping-answer": "No"})
                self.assertInUrl(SUBMIT_URL_PATH)

                # When I invalidate a block and try access the submit page
                self.get(
                    "questionnaire/test-skipping-forced/?return_to=final-summary#test-skipping-answer"
                )
                self.post({"test-skipping-answer": "Yes"})

                self.get(SUBMIT_URL_PATH)

                # Then I am redirected to the first incomplete question
                self.assertInUrl("/test-skipping-optional")


class TestQuestionnaireSubmitWithSummary(IntegrationTestCase):
    def test_accessing_submit_page_redirects_to_first_incomplete_question_when_questionnaire_incomplete(
        self,
    ):
        # Given a partially completed questionnaire
        self.launchSurvey("test_skipping_to_questionnaire_end_single_section")
        self.post({"test-skipping-answer": "Yes"})

        # When I make a GET or POST request to the submit page
        for method in [self.get, self.post]:
            with self.subTest(method=method):
                method(url=SUBMIT_URL_PATH)

                # Then I am redirected to the first incomplete question
                self.assertInUrl("/test-skipping-optional")

    def test_final_summary_shown_at_end_of_questionnaire(self):
        # Given I launch a questionnaire
        self.launchSurvey("test_skipping_to_questionnaire_end_multiple_sections")

        # When I complete the questionnaire
        self.post({"test-skipping-answer": "Yes"})
        self.post({"test-skipping-optional-answer": "I am a completionist"})

        # Then I am presented with the final summary which I am able to submit
        self.assertInUrl(SUBMIT_URL_PATH)
        self.assertInBody("Section 1")
        self.assertInBody("Section 2")
        self.assertInBody("Would you like to complete section 2?")
        self.assertInBody("Why did you choose to complete this section?")
        self.assertInBody("Submit answers")

        self.post()
        self.assertInUrl(THANK_YOU_URL_PATH)


class TestQuestionnaireSubmitWithoutSummary(IntegrationTestCase):
    def test_accessing_submit_page_redirects_to_first_incomplete_question_when_questionnaire_incomplete(
        self,
    ):
        # Given a partially completed questionnaire
        self.launchSurvey("test_final_confirmation")
        self.post(action="start_questionnaire")
        self.assertInBody("What is your favourite breakfast food")

        # When I make a GET or POST request to the submit page
        for method in [self.get, self.post]:
            with self.subTest(method=method):
                method(url=SUBMIT_URL_PATH)

                # Then I am redirected to the first incomplete question
                self.assertInUrl("/breakfast")

    def test_final_confirmation_asked_at_end_of_questionnaire(self):
        # Given I launch a questionnaire
        self.launchSurvey("test_final_confirmation")

        # When I complete the questionnaire
        self.post(action="start_questionnaire")
        self.assertInBody("What is your favourite breakfast food")
        self.post({"breakfast-answer": "Bacon"})

        # Then I am presented with a confirmation page which I am able to submit
        self.assertInUrl(SUBMIT_URL_PATH)
        self.assertNotInBody("What is your favourite breakfast food")
        self.assertInBody("Thank you for your answers, submit this to complete it")
        self.assertInBody("Submit")

        self.post()
        self.assertInUrl(THANK_YOU_URL_PATH)
