from app.utilities.json import json_loads
from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireEndpoints(IntegrationTestCase):
    BASE_URL = "/questionnaire"

    def test_invalid_section_id_raises_404(self):
        # Given
        self.launchSurveyV2(schema_name="test_hub_and_spoke")

        # When I navigate to the url for a section that does not exist
        self.get(f"{self.BASE_URL}/sections/invalid-section/")

        # Then I am shown a 404 page
        self.assertStatusNotFound()

    def test_get_invalid_questionnaire_location_raises_404(self):
        # Given
        self.launchSurveyV2(schema_name="test_introduction")

        # When
        self.get(f"{self.BASE_URL}/test")

        # Then
        self.assertStatusNotFound()

    def test_post_invalid_questionnaire_location_raises_404(self):
        # Given
        self.launchSurveyV2(schema_name="test_introduction")

        # When
        self.post(url=f"{self.BASE_URL}/test")

        # Then I am shown a 404 page
        self.assertStatusNotFound()

    def test_post_on_questionnaire_route_without_hub_redirects_to_first_incomplete_location(
        self,
    ):
        # Given
        self.launchSurveyV2(schema_name="test_textfield")

        # When
        self.post(url="/questionnaire/")

        # Then
        self.assertInUrl("name-block")

    def test_get_thank_you_data_not_deleted_when_questionnaire_is_not_complete(self):
        # Given we start a survey
        self.launchSurveyV2(schema_name="test_percentage", roles=["dumper"])
        self.post({"answer": "99"})

        # When we request the thank you page (without submitting the survey)
        self.get("submitted/thank-you")

        # Then the answers are not deleted
        self.get("/dump/debug")
        answers = json_loads(self.getResponseData())
        self.assertEqual(1, len(answers["ANSWERS"]))

    def test_get_thank_you_raises_404_when_questionnaire_is_not_complete(self):
        # Given we start a survey
        self.launchSurveyV2(schema_name="test_percentage", roles=["dumper"])

        # When we request the thank you page (without submitting the survey)
        self.get("submitted/thank-you")

        # Then we are shown a 404 page
        self.assertStatusNotFound()

    def test_when_on_thank_you_get_thank_you_returns_thank_you(self):
        # Given we complete the test_percentage survey and are on the thank you page
        self.launchSurveyV2(schema_name="test_percentage", roles=["dumper"])
        self.post({"answer": "99"})
        self.post()

        # When we try to get the thank-you page
        self.get("submitted/thank-you")

        # Then we get the thank-you page
        self.assertInUrl("submitted/thank-you")

    def test_when_no_session_thank_you_returns_unauthorised(self):
        # When we try to request the thank-you page with no session
        self.get(url="submitted/thank-you")

        # Then we get the unauthorised page
        self.assertStatusUnauthorised()
