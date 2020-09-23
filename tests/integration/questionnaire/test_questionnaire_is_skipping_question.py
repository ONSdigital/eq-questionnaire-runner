from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireChangeAnswer(IntegrationTestCase):
    def test_final_summary_not_available_if_any_question_incomplete(self):

        # Given I launched a survey and have not answered any questions
        self.launchSurvey("test_is_skipping_to_end")

        # When I try access the final summary
        self.get("questionnaire/summary")

        # Then I am shown a 404 page
        self.assertStatusNotFound()

    def test_final_summary_not_available_after_invalidating_section(self):

        # Given I launched a survey and have answered all questions
        self.launchSurvey("test_is_skipping_to_end")
        self.post({"test-skipping-answer": "No"})
        self.assertInBody("Were you forced to complete section 1?")
        self.post()

        self.post({"test-skipping-answer-2": "No"})
        self.assertInBody("Were you forced to complete section 2?")
        self.post()

        self.assertInBody("Please submit this survey to complete it")
        self.assertInBody("Were you forced to complete section 1?")
        self.assertInBody("Were you forced to complete section 2?")
        self.assertInBody("Submit answers")

        # When I invalidate any block and try access the final summary
        self.get("questionnaire/test-skipping-forced-2#test-skipping-answer-2")
        self.post({"test-skipping-answer-2": "Yes"})

        self.get("questionnaire/test-skipping-forced#test-skipping-answer")
        self.post({"test-skipping-answer": "Yes"})

        self.get("questionnaire/summary")

        # Then I am shown a 404 page
        self.assertStatusNotFound()
