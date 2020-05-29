import random
import string
from tests.integration.integration_test_case import IntegrationTestCase


class TestLastViewedGuidance(IntegrationTestCase):
    def test_last_viewed_question_guidance_not_shown_on_survey_launch(self):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance")

        # Then last viewed guidance should not be shown
        self.last_viewed_question_guidance_not_shown_assertion()

    def test_last_viewed_question_guidance_not_shown_on_linear_journey(self):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance")

        # When I complete the journey as normal, without resuming
        self.post()

        # Then last viewed guidance should not be shown
        self.last_viewed_question_guidance_not_shown_assertion()

    def test_last_viewed_question_guidance_not_shown_on_section_resume_first_block_in_new_section(
        self
    ):

        # Given
        response_id = self.random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out and resume on the first block of a new section
        self.post()
        self.post_address_confirmation_answer()
        self.post_you_live_here_answer()
        self.post_list_collector_answers()
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed guidance is not shown
        self.assertInUrl("/questionnaire/relationship-interstitial/")
        self.last_viewed_question_guidance_not_shown_assertion()

    def test_last_viewed_question_guidance_not_shown_on_resume_section_not_started(
        self
    ):
        # Given
        response_id = self.random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out without starting the section and I resume the survey
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed guidance should not be shown
        self.assertInUrl("/questionnaire/household-interstitial/")
        self.last_viewed_question_guidance_not_shown_assertion()

    def test_last_viewed_question_guidance_shown_on_resume_section_in_progress(self):

        response_id = self.random_respondent_id()

        # Given
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out after I have started the section and I resume the survey
        self.post()
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed guidance should be shown
        self.assertInUrl(
            "/questionnaire/address-confirmation/?last_viewed_question_guidance=True"
        )
        self.last_viewed_question_guidance_shown_assertion(
            "/questionnaire/household-interstitial/"
        )

    def test_last_viewed_question_guidance_shown_on_section_in_progress_resume_primary_person_list_collector(
        self
    ):

        # Given
        response_id = self.random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out and resume on a primary person list collector
        self.post()
        self.post_address_confirmation_answer()
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed guidance is shown
        self.assertInUrl(
            "/questionnaire/primary-person-list-collector/?last_viewed_question_guidance=True"
        )
        self.last_viewed_question_guidance_shown_assertion(
            "/questionnaire/household-interstitial/"
        )

    def test_last_viewed_question_guidance_shown_on_section_in_progress_resume_primary_person_list_collector_add_person(
        self
    ):

        # Given
        response_id = self.random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out and resume on a primary person list collector add person page
        self.post()
        self.post_address_confirmation_answer()
        self.post_you_live_here_answer()
        self.post(action="sign_out")

        # Then the last viewed guidance is shown on the parent page
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)
        self.assertInUrl(
            "/questionnaire/primary-person-list-collector/?last_viewed_question_guidance=True"
        )
        self.last_viewed_question_guidance_shown_assertion(
            "/questionnaire/household-interstitial/"
        )

    def test_last_viewed_question_guidance_shown_on_section_in_progress_resume_list_collector(
        self
    ):

        # Given
        response_id = self.random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out and resume on a list collector
        self.post()
        self.post_address_confirmation_answer()
        self.post_you_live_here_answer()
        self.post_primary_person_answer()
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed guidance is shown
        self.assertInUrl(
            "/questionnaire/list-collector/?last_viewed_question_guidance=True"
        )
        self.last_viewed_question_guidance_shown_assertion(
            "/questionnaire/household-interstitial/"
        )

    def test_last_viewed_question_guidance_shown_on_section_in_progress_resume_list_collector_add_person(
        self
    ):

        # Given
        response_id = self.random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out and resume on a list collector add person
        self.post()
        self.post_address_confirmation_answer()
        self.post_you_live_here_answer()
        self.post_primary_person_answer()
        self.post({"anyone-else": "Yes"})
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed guidance is shown on the parent page
        self.assertInUrl(
            "/questionnaire/list-collector/?last_viewed_question_guidance=True"
        )
        self.last_viewed_question_guidance_shown_assertion(
            "/questionnaire/household-interstitial/"
        )

    def test_last_viewed_question_guidance_shown_on_section_in_progress_resume_relationships(
        self
    ):

        # Given
        response_id = self.random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out and resume on a relationship question
        self.post()
        self.post_address_confirmation_answer()
        self.post_you_live_here_answer()
        self.post_primary_person_answer()
        self.post_list_collector_answers()
        self.post()
        self.post()
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed guidance is shown
        self.assertInUrl("/questionnaire/relationships/")
        self.assertInUrl("?last_viewed_question_guidance=True")
        self.last_viewed_question_guidance_shown_assertion(
            "/questionnaire/relationship-interstitial/"
        )

    def last_viewed_question_guidance_shown_assertion(self, link):
        selector = "#section-start-link"
        selected = self.getHtmlSoup().select(selector)
        self.assertInBody("This is the last viewed question in this section")
        self.assertEqual(selected[0].get("href"), link)

    def last_viewed_question_guidance_not_shown_assertion(self):
        self.assertNotInUrl("last_viewed_question_guidance=True")
        self.assertNotInBody("This is the last viewed question in this section")

    def post_address_confirmation_answer(self):
        self.post({"address-confirmation-answer": "Yes"})

    def post_you_live_here_answer(self):
        self.post({"you-live-here": "Yes"})

    def post_primary_person_answer(self):
        self.post({"first-name": "John", "last-name": "Smith"})

    def post_list_collector_answers(self):
        self.post({"first-name": "Maggie", "last-name": "Smith"})
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": "Emily", "last-name": "Smith"})
        self.post({"anyone-else": "No"})

    @staticmethod
    def random_respondent_id():
        return random.choices(string.digits, k=16)
