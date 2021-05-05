from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import SUBMIT_URL_PATH, THANK_YOU_URL_PATH


class TestQuestionnairePreviousLink(IntegrationTestCase):
    def test_previous_link_doesnt_appear_on_introduction(self):
        # Given
        self.launchSurvey("test_final_confirmation")
        # When we open the introduction
        # Then previous link does not appear
        self.assertNotInBody("Previous")

    def test_previous_link_appears_on_the_final_confirmation_submit_page(self):
        # Given
        self.launchSurvey("test_final_confirmation")

        # When we proceed through the questionnaire
        self.post(action="start_questionnaire")
        self.assertInBody("Previous")
        self.post({"breakfast-answer": "Bacon"})
        self.assertInUrl(SUBMIT_URL_PATH)
        self.assertInBody("Previous")

    def test_previous_link_appears_on_the_final_summary_submit_page(self):
        # Given
        self.launchSurvey("test_summary")

        # When we proceed through the questionnaire
        self.post()
        self.post({"dessert-answer": "Cake"})
        self.post({"dessert-confirmation-answer": "Yes"})
        self.post()
        self.assertInUrl(SUBMIT_URL_PATH)
        self.assertInBody("Previous")

    def test_previous_link_doesnt_appear_on_thank_you(self):
        # Given
        self.launchSurvey("test_final_confirmation")

        # When ee proceed through the questionnaire
        self.post(action="start_questionnaire")
        self.post({"breakfast-answer": "Eggs"})
        self.post()
        self.assertInUrl(THANK_YOU_URL_PATH)
        self.assertNotInUrl("Previous")

    def test_previous_link_appears_on_questions_preceded_by_another_question(self):

        # Given a survey with multiple questions
        self.launchSurvey("test_checkbox")

        # When I answer a question
        self.assertInUrl("mandatory-checkbox")
        self.post({"mandatory-checkbox-answer": "None"})

        # Then there should be a previous link on the current page
        self.assertInBody("Previous")

    def test_previous_link_appears_on_the_first_question_preceded_by_the_hub(self):

        # Given a survey with a hub enabled
        self.launchSurvey("test_hub_and_spoke")

        # When I answer go to the first question in a section
        self.assertInUrl("/")
        self.post()

        # Then there should be a previous link on the current page
        self.assertInBody("Previous")
