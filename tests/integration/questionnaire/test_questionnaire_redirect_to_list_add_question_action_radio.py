from tests.integration.questionnaire import QuestionnaireTestCase


class TestQuestionnaireListCollector(QuestionnaireTestCase):
    def test_add_list_question_displayed_before_list_collector_and_return_to_in_url(
        self,
    ):
        # Given
        self.launchSurveyV2(
            schema_name="test_answer_action_redirect_to_list_add_block_radio"
        )

        # When
        self.post({"anyone-usually-live-at-answer": "Yes"})

        # Then
        self.assertInUrl(
            "/questionnaire/people/add-person/?previous=anyone-usually-live-at"
        )

    def test_previous_link_when_list_empty_with_return_to_query_string(self):
        # Given
        self.launchSurveyV2(
            schema_name="test_answer_action_redirect_to_list_add_block_radio"
        )
        self.post({"anyone-usually-live-at-answer": "Yes"})

        # When
        self.previous()

        # Then
        self.assertInUrl("/questionnaire/anyone-usually-live-at/")

    def test_previous_link_when_list_not_empty(self):
        # Given
        self.launchSurveyV2(
            schema_name="test_answer_action_redirect_to_list_add_block_radio"
        )
        self.post({"anyone-usually-live-at-answer": "Yes"})
        self.add_person("John", "Doe")
        self.post({"anyone-else-live-at-answer": "Yes"})

        # When
        self.previous()

        # Then
        self.assertInUrl("/questionnaire/anyone-else-live-at/")

    def test_previous_link_return_to_list_collector_when_invalid_return_to_block_id(
        self,
    ):
        # Given
        self.launchSurveyV2(
            schema_name="test_answer_action_redirect_to_list_add_block_radio"
        )
        self.post({"anyone-usually-live-at-answer": "Yes"})

        url_with_invalid_return_to = self.last_url + "-invalid"

        self.get(url_with_invalid_return_to)

        self.assertInUrl("?previous=anyone-usually-live-at-invalid")

        # When
        self.previous()

        # Then
        self.assertInUrl("/questionnaire/anyone-else-live-at/")
