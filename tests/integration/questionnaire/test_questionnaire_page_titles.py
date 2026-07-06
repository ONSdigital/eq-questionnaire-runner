from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnairePageTitles(IntegrationTestCase):
    def test_introduction_has_introduction_in_page_title(self):
        # Given, When
        self.launchSurveyV2(schema_name="test_submit_with_custom_submission_text")
        # Then
        self.assertEqualPageTitle(
            "Introduction - Test Submit with Custom Submission Text"
        )

    def test_should_have_question_in_page_title_when_loading_questionnaire(self):
        # Given
        self.launchSurveyV2(schema_name="test_submit_with_custom_submission_text")
        # When
        self.post(action="start_questionnaire")
        # Then
        self.assertEqualPageTitle(
            "What is your favourite breakfast food - Test Submit with Custom Submission Text"
        )

    def test_should_have_question_in_page_title_on_submit_page(self):
        # Given
        self.launchSurveyV2(schema_name="test_submit_with_custom_submission_text")
        # When
        self.post(action="start_questionnaire")
        self.post({"breakfast-answer": ""})
        # Then
        self.assertEqualPageTitle(
            "Submit your questionnaire - Test Submit with Custom Submission Text"
        )

    def test_should_have_question_in_page_title_on_submit_page_with_summary(self):
        # Given
        self.launchSurveyV2(schema_name="test_percentage")
        # When
        self.post({"answer": ""})
        self.post({"answer-decimal": ""})
        # Then
        self.assertEqualPageTitle("Check your answers and submit - Test Percentage")

    def test_should_have_survey_in_page_title_on_thank_you(self):
        # Given
        self.launchSurveyV2(schema_name="test_submit_with_custom_submission_text")
        self.post(action="start_questionnaire")
        self.post({"breakfast-answer": ""})
        # When submit
        self.post()
        # Then
        self.assertEqualPageTitle(
            "We’ve received your answers - Test Submit with Custom Submission Text"
        )

    def test_session_timed_out_page_title(self):
        # Given
        self.launchSurveyV2(schema_name="test_submit_with_custom_submission_text")
        # When
        self.get("/session-expired")
        # Then
        self.assertEqualPageTitle(
            "Page is not available - Test Submit with Custom Submission Text"
        )

    def test_should_have_content_title_in_page_title_on_interstitial(self):
        # Given
        self.launchSurveyV2(schema_name="test_interstitial_page")
        self.post(action="start_questionnaire")
        # When
        self.post({"favourite-breakfast": ""})
        # Then
        self.assertEqualPageTitle("Breakfast interstitial - Test Interstitial Page")

    def test_html_stripped_from_page_titles(self):
        # Given
        self.launchSurveyV2(schema_name="test_markup")
        # When
        # Then
        self.assertEqualPageTitle("This is a title with emphasis - Test Markup")

    def test_should_have_question_title_in_page_title_on_question(self):
        # Given
        self.launchSurveyV2(schema_name="test_checkbox")
        # When
        # Then
        self.assertEqualPageTitle(
            "Which pizza toppings would you like? - Test Checkbox"
        )

    def test_should_not_use_names_in_question_page_titles(self):
        # Given
        self.launchSurveyV2(
            schema_name="test_placeholder_full",
            display_address="68 Abingdon Road, Goathill",
        )
        # When
        self.post({"first-name": "Kevin", "last-name": "Bacon"})
        # Then
        self.assertEqualPageTitle("What is … date of birth? - Test Placeholder Full")

    def test_content_page_should_use_nested_content_text_in_page_title_if_it_exists(
        self,
    ):
        # Given
        self.launchSurveyV2(schema_name="test_interstitial_page_title")
        # When
        # Then
        self.assertEqualPageTitle("Your RU name: … - Test Interstitial Page Title")

    def test_should_have_error_in_page_title_when_fail_validation(self):
        # Given
        self.launchSurveyV2(schema_name="test_checkbox")
        # When
        self.post()
        # Then
        self.assertEqualPageTitle(
            "Error: Which pizza toppings would you like? - Test Checkbox"
        )
