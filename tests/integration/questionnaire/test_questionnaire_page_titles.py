from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnairePageTitles(IntegrationTestCase):
    def test_introduction_has_introduction_in_page_title(self):
        # Given, When
        self.launchSurvey("test_final_confirmation")
        # Then
        self.assertEqualPageTitle("Introduction - Census 2021")

    def test_should_have_question_in_page_title_when_loading_questionnaire(self):
        # Given
        self.launchSurvey("test_final_confirmation")
        # When
        self.post(action="start_questionnaire")
        # Then
        self.assertEqualPageTitle("What is your favourite breakfast food - Census 2021")

    def test_should_have_question_in_page_title_when_loading_confirmation(self):
        # Given
        self.launchSurvey("test_final_confirmation")
        # When
        self.post(action="start_questionnaire")
        self.post({"breakfast-answer": ""})
        # Then
        self.assertEqualPageTitle("Submit your questionnaire - Census 2021")

    def test_should_have_question_in_page_title_when_loading_summary(self):
        # Given
        self.launchSurvey("test_percentage")
        # When
        self.post({"answer": ""})
        # Then
        self.assertEqualPageTitle("Check your answers and submit - Census 2021")

    def test_should_have_survey_in_page_title_when_thank_you(self):
        # Given
        self.launchSurvey("test_final_confirmation")
        self.post(action="start_questionnaire")
        self.post({"breakfast-answer": ""})
        # When submit
        self.post()
        # Then
        self.assertEqualPageTitle("We’ve received your answers - Census 2021")

    def test_session_timed_out_page_title(self):
        # Given
        self.launchSurvey("test_final_confirmation")
        # When
        self.get("/session-expired")
        # Then
        self.assertEqualPageTitle("Session timed out - Census 2021")

    def test_should_have_content_title_in_page_title_when_interstitial(self):
        # Given
        self.launchSurvey("test_interstitial_page")
        self.post(action="start_questionnaire")
        # When
        self.post({"favourite-breakfast": ""})
        # Then
        self.assertEqualPageTitle("Breakfast interstitial - Census 2021")

    def test_html_stripped_from_page_titles(self):
        # Given
        self.launchSurvey("test_markup")
        # When
        # Then
        self.assertEqualPageTitle("This is a title with emphasis - Census 2021")

    def test_should_have_question_title_in_page_title_when_question(self):
        # Given
        self.launchSurvey("test_checkbox")
        # When
        # Then
        self.assertEqualPageTitle("Which pizza toppings would you like? - Census 2021")

    def test_should_not_use_names_in_question_page_titles(self):
        # Given
        self.launchSurvey(
            "test_placeholder_full", display_address="68 Abingdon Road, Goathill"
        )
        # When
        self.post({"first-name": "Kevin", "last-name": "Bacon"})
        # Then
        self.assertEqualPageTitle("What is … date of birth? - Census 2021")

    def test_content_page_should_use_nested_content_text_in_page_title_if_it_exists(
        self,
    ):
        # Given
        self.launchSurvey("test_interstitial_page_title")
        # When
        # Then
        self.assertEqualPageTitle("This is the content title … - Census 2021")

    def test_should_have_error_in_page_title_when_fail_validation(self):
        # Given
        self.launchSurvey("test_checkbox")
        # When
        self.post()
        # Then
        self.assertEqualPageTitle(
            "Error: Which pizza toppings would you like? - Census 2021"
        )
