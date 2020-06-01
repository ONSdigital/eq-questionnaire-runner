import random
import string
from tests.integration.integration_test_case import IntegrationTestCase


class TestLastViewedGuidance(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        self.response_id = random.choices(string.digits, k=16)
        super().__init__(*args, **kwargs)

    def test_not_shown_on_survey_launch(self):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance")

        # Then last viewed question guidance should not be shown
        self._assert_last_viewed_question_guidance_not_shown()

    def test_not_shown_on_linear_journey(self):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance")

        # When I complete the journey as normal, without resuming
        self.post()

        # Then last viewed question guidance should not be shown
        self._assert_last_viewed_question_guidance_not_shown()

    def test_not_shown_on_section_resume_first_block_in_new_section(self):

        # Given
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # When I sign out and resume on the first block of a new section
        self.post()
        self._post_address_confirmation_answer()
        self._post_you_live_here_answer()
        self._post_list_collector_answers()
        self.post(action="sign_out")
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # Then the last viewed question guidance is not shown
        self._assert_last_viewed_question_guidance_not_shown()

    def test_not_shown_on_resume_section_not_started(self):
        # Given
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # When I sign out without starting the section and I resume the survey
        self.post(action="sign_out")
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # Then the last viewed question guidance should not be shown
        self._assert_last_viewed_question_guidance_not_shown()

    def test_shown_on_resume_section_in_progress(self):

        # Given
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # When I sign out after I have started the section and I resume the survey
        self.post()
        self.post(action="sign_out")
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # Then the last viewed guidance should be shown
        self._assert_last_viewed_question_guidance_link(
            "/questionnaire/household-interstitial/"
        )
        self._assert_last_viewed_question_guidance_shown()

    def test_shown_on_section_in_progress_resume_primary_person_list_collector(self):

        # Given
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # When I sign out and resume on a primary person list collector
        self.post()
        self._post_address_confirmation_answer()
        self.post(action="sign_out")
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # Then the last viewed guidance is shown
        self._assert_last_viewed_question_guidance_link(
            "/questionnaire/household-interstitial/"
        )
        self._assert_last_viewed_question_guidance_shown()

    def test_shown_on_section_in_progress_resume_primary_person_list_collector_add_person(
        self,
    ):

        # Given
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # When I sign out and resume on a primary person list collector add person page
        self.post()
        self._post_address_confirmation_answer()
        self._post_you_live_here_answer()
        self.post(action="sign_out")
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # Then the last viewed guidance is shown on the parent page
        self._assert_last_viewed_question_guidance_link(
            "/questionnaire/household-interstitial/"
        )
        self._assert_last_viewed_question_guidance_shown()

    def test_shown_on_section_in_progress_resume_list_collector(self):

        # Given
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # When I sign out and resume on a list collector
        self.post()
        self._post_address_confirmation_answer()
        self._post_you_live_here_answer()
        self._post_primary_person_answer()
        self.post(action="sign_out")
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # Then the last viewed guidance is shown
        self._assert_last_viewed_question_guidance_link(
            "/questionnaire/household-interstitial/"
        )
        self._assert_last_viewed_question_guidance_shown()

    def test_shown_on_section_in_progress_resume_list_collector_add_person(self):

        # Given
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # When I sign out and resume on a list collector add person
        self.post()
        self._post_address_confirmation_answer()
        self._post_you_live_here_answer()
        self._post_primary_person_answer()
        self.post({"anyone-else": "Yes"})
        self.post(action="sign_out")
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # Then the last viewed guidance is shown on the parent page
        self._assert_last_viewed_question_guidance_link(
            "/questionnaire/household-interstitial/"
        )
        self._assert_last_viewed_question_guidance_shown()

    def test_shown_on_section_in_progress_resume_relationships(self):
        # Given
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # When I sign out and resume on a relationship question
        self.post()
        self._post_address_confirmation_answer()
        self._post_you_live_here_answer()
        self._post_primary_person_answer()
        self._post_list_collector_answers()
        self.post()
        self.post()
        self.post(action="sign_out")
        self.launchSurvey(
            "test_last_viewed_question_guidance", reponse_id=self.response_id
        )

        # Then the last viewed guidance is shown
        self._assert_last_viewed_question_guidance_link(
            "/questionnaire/relationship-interstitial/"
        )
        self._assert_last_viewed_question_guidance_shown()

    def test_not_shown_on_survey_launch_hub_not_available(self):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance_hub")

        # When the hub is not available, then last viewed guidance should not be shown
        self._assert_last_viewed_question_guidance_not_shown()

    def test_not_shown_on_section_not_started_hub(self):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance_hub")

        # When clicking on a link from the hub to a section not started
        self._posts_for_hub_required_section_to_complete()
        self.get("/questionnaire/sections/education-section/")

        # Then last viewed guidance should not be shown
        self._assert_last_viewed_question_guidance_not_shown()

    def test_shown_on_section_in_progress_hub_using_link_from_hub(self):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance_hub")

        # When clicking on a link from the hub to a section that is in progress
        self._posts_for_hub_required_section_to_complete()
        self.get("/questionnaire/sections/education-section/")
        self._post_gcse_answer()
        self.get("/questionnaire/sections/education-section/")

        # Then last viewed guidance should be shown
        self._assert_last_viewed_question_guidance_shown()

    def test_shown_on_section_in_progress_hub_using_continue_from_hub(self):
        # Given
        self.launchSurvey("test_last_viewed_question_guidance_hub")

        # When clicking on continue from the hub to a section that is in progress
        self._posts_for_hub_required_section_to_complete()
        self.get("/questionnaire/sections/education-section/")
        self._post_gcse_answer()
        self.get("/questionnaire/")
        self.post()

        # Then last viewed guidance should be shown
        self._assert_last_viewed_question_guidance_shown()

    def _assert_last_viewed_question_guidance_link(self, link):
        selected = self._get_html_element("#section-start-link")
        self.assertEqual(selected[0].get("href"), link)

    def _assert_last_viewed_question_guidance_shown(self):
        self.assertInUrl("resume=True")
        selected = self._get_html_element("#last-viewed-question-guidance")
        self.assertTrue(selected)

    def _assert_last_viewed_question_guidance_not_shown(self):
        self.assertNotInUrl("resume=True")
        selected = self._get_html_element("#last-viewed-question-guidance")
        self.assertFalse(selected)

    def _get_html_element(self, selector_id):
        return self.getHtmlSoup().select(selector_id)

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
