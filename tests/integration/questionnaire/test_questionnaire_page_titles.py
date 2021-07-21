from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnairePageTitles(IntegrationTestCase):
    def test_introduction_has_introduction_in_page_title(self):
        # Given, When
        self.launchSurvey("test_submit_with_custom_submission_text")
        # Then
        self.assertEqualPageTitle("Introduction - Submit without summary")

    def test_should_have_question_in_page_title_when_loading_questionnaire(self):
        # Given
        self.launchSurvey("test_submit_with_custom_submission_text")
        # When
        self.post(action="start_questionnaire")
        # Then
        self.assertEqualPageTitle(
            "What is your favourite breakfast food - Submit without summary"
        )

    def test_should_have_question_in_page_title_on_submit_page(self):
        # Given
        self.launchSurvey("test_submit_with_custom_submission_text")
        # When
        self.post(action="start_questionnaire")
        self.post({"breakfast-answer": ""})
        # Then
        self.assertEqualPageTitle("Submit your questionnaire - Submit without summary")

    def test_should_have_question_in_page_title_on_submit_page_with_summary(self):
        # Given
        self.launchSurvey("test_percentage")
        # When
        self.post({"answer": ""})
        # Then
        self.assertEqualPageTitle(
            "Check your answers and submit - Percentage Field Demo"
        )

    def test_should_have_survey_in_page_title_on_thank_you(self):
        # Given
        self.launchSurvey("test_submit_with_custom_submission_text")
        self.post(action="start_questionnaire")
        self.post({"breakfast-answer": ""})
        # When submit
        self.post()
        # Then
        self.assertEqualPageTitle(
            "We’ve received your answers - Submit without summary"
        )

    def test_session_timed_out_page_title(self):
        # Given
        self.launchSurvey("test_submit_with_custom_submission_text")
        # When
        self.get("/session-expired")
        # Then
        self.assertEqualPageTitle("Session timed out - Submit without summary")

    def test_should_have_content_title_in_page_title_on_interstitial(self):
        # Given
        self.launchSurvey("test_interstitial_page")
        self.post(action="start_questionnaire")
        # When
        self.post({"favourite-breakfast": ""})
        # Then
        self.assertEqualPageTitle("Breakfast interstitial - Interstitial Pages")

    def test_html_stripped_from_page_titles(self):
        # Given
        self.launchSurvey("test_markup")
        # When
        # Then
        self.assertEqualPageTitle("This is a title with emphasis - Markup test")

    def test_should_have_question_title_in_page_title_on_question(self):
        # Given
        self.launchSurvey("test_checkbox")
        # When
        # Then
        self.assertEqualPageTitle(
            "Which pizza toppings would you like? - Other input fields"
        )

    def test_should_not_use_names_in_question_page_titles(self):
        # Given
        self.launchSurvey(
            "test_placeholder_full", display_address="68 Abingdon Road, Goathill"
        )
        # When
        self.post({"first-name": "Kevin", "last-name": "Bacon"})
        # Then
        self.assertEqualPageTitle("What is … date of birth? - Placeholder Test")

    def test_content_page_should_use_nested_content_text_in_page_title_if_it_exists(
        self,
    ):
        # Given
        self.launchSurvey("test_interstitial_page_title")
        # When
        # Then
        self.assertEqualPageTitle(
            "This is the content title … - Interstitial Page Titles"
        )

    def test_should_have_error_in_page_title_when_fail_validation(self):
        # Given
        self.launchSurvey("test_checkbox")
        # When
        self.post()
        # Then
        self.assertEqualPageTitle(
            "Error: Which pizza toppings would you like? - Other input fields"
        )
