import random
import string
from tests.integration.integration_test_case import IntegrationTestCase


class TestLastViewedGuidance(IntegrationTestCase):
    def test_last_viewed_question_guidance_not_shown_on_survey_launch(self):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance")

        # Then last viewed question guidance should not be shown
        self._last_viewed_question_guidance_not_shown_assertion()

    def test_last_viewed_question_guidance_not_shown_on_linear_journey(self):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance")

        # When I complete the journey as normal, without resuming
        self.post()

        # Then last viewed question guidance should not be shown
        self._last_viewed_question_guidance_not_shown_assertion()

    def test_last_viewed_question_guidance_not_shown_on_section_resume_first_block_in_new_section(
        self
    ):

        # Given
        response_id = self._random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out and resume on the first block of a new section
        self.post()
        self._post_address_confirmation_answer()
        self._post_you_live_here_answer()
        self._post_list_collector_answers()
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed question guidance is not shown
        self.assertInUrl("/questionnaire/relationship-interstitial/")
        self._last_viewed_question_guidance_not_shown_assertion()

    def test_last_viewed_question_guidance_not_shown_on_resume_section_not_started(
        self
    ):
        # Given
        response_id = self._random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out without starting the section and I resume the survey
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed question guidance should not be shown
        self.assertInUrl("/questionnaire/household-interstitial/")
        self._last_viewed_question_guidance_not_shown_assertion()

    def test_last_viewed_question_guidance_shown_on_resume_section_in_progress(self):

        # Given
        response_id = self._random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out after I have started the section and I resume the survey
        self.post()
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed guidance should be shown
        self.assertInUrl(
            "/questionnaire/address-confirmation/?last_viewed_question_guidance=True"
        )
        self._last_viewed_question_guidance_shown_assertion(
            "/questionnaire/household-interstitial/"
        )

    def test_last_viewed_question_guidance_shown_on_section_in_progress_resume_primary_person_list_collector(
        self
    ):

        # Given
        response_id = self._random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out and resume on a primary person list collector
        self.post()
        self._post_address_confirmation_answer()
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed guidance is shown
        self.assertInUrl(
            "/questionnaire/primary-person-list-collector/?last_viewed_question_guidance=True"
        )
        self._last_viewed_question_guidance_shown_assertion(
            "/questionnaire/household-interstitial/"
        )

    def test_last_viewed_question_guidance_shown_on_section_in_progress_resume_primary_person_list_collector_add_person(
        self
    ):

        # Given
        response_id = self._random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out and resume on a primary person list collector add person page
        self.post()
        self._post_address_confirmation_answer()
        self._post_you_live_here_answer()
        self.post(action="sign_out")

        # Then the last viewed guidance is shown on the parent page
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)
        self.assertInUrl(
            "/questionnaire/primary-person-list-collector/?last_viewed_question_guidance=True"
        )
        self._last_viewed_question_guidance_shown_assertion(
            "/questionnaire/household-interstitial/"
        )

    def test_last_viewed_question_guidance_shown_on_section_in_progress_resume_list_collector(
        self
    ):

        # Given
        response_id = self._random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out and resume on a list collector
        self.post()
        self._post_address_confirmation_answer()
        self._post_you_live_here_answer()
        self._post_primary_person_answer()
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed guidance is shown
        self.assertInUrl(
            "/questionnaire/list-collector/?last_viewed_question_guidance=True"
        )
        self._last_viewed_question_guidance_shown_assertion(
            "/questionnaire/household-interstitial/"
        )

    def test_last_viewed_question_guidance_shown_on_section_in_progress_resume_list_collector_add_person(
        self
    ):

        # Given
        response_id = self._random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out and resume on a list collector add person
        self.post()
        self._post_address_confirmation_answer()
        self._post_you_live_here_answer()
        self._post_primary_person_answer()
        self.post({"anyone-else": "Yes"})
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed guidance is shown on the parent page
        self.assertInUrl(
            "/questionnaire/list-collector/?last_viewed_question_guidance=True"
        )
        self._last_viewed_question_guidance_shown_assertion(
            "/questionnaire/household-interstitial/"
        )

    def test_last_viewed_question_guidance_shown_on_section_in_progress_resume_relationships(
        self
    ):

        # Given
        response_id = self._random_respondent_id()
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # When I sign out and resume on a relationship question
        self.post()
        self._post_address_confirmation_answer()
        self._post_you_live_here_answer()
        self._post_primary_person_answer()
        self._post_list_collector_answers()
        self.post()
        self.post()
        self.post(action="sign_out")
        self.launchSurvey("test_last_viewed_question_guidance", reponse_id=response_id)

        # Then the last viewed guidance is shown
        self.assertInUrl("/questionnaire/relationships/")
        self.assertInUrl("?last_viewed_question_guidance=True")
        self._last_viewed_question_guidance_shown_assertion(
            "/questionnaire/relationship-interstitial/"
        )

    def test_last_viewed_question_guidance_not_shown_on_survey_launch_hub_not_available(
        self
    ):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance_hub")

        # When the hub is not available, then last viewed guidance should not be shown
        self._last_viewed_question_guidance_not_shown_assertion()

    def test_last_viewed_question_guidance_not_shown_on_section_not_started_hub(self):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance_hub")

        # When clicking on a link from the hub to a section not started
        self._posts_for_hub_required_section_to_complete()
        self.get("/questionnaire/sections/education-section/")

        # Then last viewed guidance should not be shown
        self._last_viewed_question_guidance_not_shown_assertion()

    def test_last_viewed_question_guidance_shown_on_section_in_progress_hub_using_link_from_hub(
        self
    ):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance_hub")

        # When clicking on a link from the hub to a section that is in progress
        self._posts_for_hub_required_section_to_complete()
        self.get("/questionnaire/sections/education-section/")
        self._post_gcse_answer()
        self.get("/questionnaire/sections/education-section/")

        # Then last viewed guidance should be shown
        self.assertInUrl("?last_viewed_question_guidance=True")
        self._last_viewed_question_guidance_shown_assertion("/questionnaire/gcses/")

    def test_last_viewed_question_guidance_shown_on_section_in_progress_hub_using_continue_from_hub(
        self
    ):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance_hub")

        # When clicking on continue from the hub to a section that is in progress
        self._posts_for_hub_required_section_to_complete()
        self.get("/questionnaire/sections/education-section/")
        self._post_gcse_answer()
        self.get("/questionnaire/")
        self.post()

        # Then last viewed guidance should be shown
        self.assertInUrl("?last_viewed_question_guidance=True")
        self._last_viewed_question_guidance_shown_assertion("/questionnaire/gcses/")

    def _last_viewed_question_guidance_shown_assertion(self, link):
        selector = "#section-start-link"
        selected = self.getHtmlSoup().select(selector)
        self.assertInBody("This is the last viewed question in this section")
        self.assertEqual(selected[0].get("href"), link)

    def _last_viewed_question_guidance_not_shown_assertion(self):
        self.assertNotInUrl("last_viewed_question_guidance=True")
        self.assertNotInBody("This is the last viewed question in this section")

    def _post_address_confirmation_answer(self):
        self.post({"address-confirmation-answer": "Yes"})

    def _post_you_live_here_answer(self):
        self.post({"you-live-here": "Yes"})

    def _post_primary_person_answer(self):
        self.post({"first-name": "John", "last-name": "Smith"})

    def _post_list_collector_answers(self):
        self.post({"first-name": "Maggie", "last-name": "Smith"})
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": "Emily", "last-name": "Smith"})
        self.post({"anyone-else": "No"})

    def _post_gcse_answer(self):
        self.post({"gcse-answer": "Yes"})

    def _posts_for_hub_required_section_to_complete(self):
        self.post()
        self.post({"paid-work-answer": "Yes"})
        self.post({"unpaid-work-answer": "Yes"})

    @staticmethod
    def _random_respondent_id():
        return random.choices(string.digits, k=16)
