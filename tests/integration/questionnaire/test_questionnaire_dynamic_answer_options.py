from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireDynamicAnswerOptionsFunctionDriven(IntegrationTestCase):
    def answer_checkbox_question(self, answer_value):
        self.post({"dynamic-checkbox-answer": answer_value})

    def answer_radio_question(self, answer_value):
        self.post({"dynamic-radio-answer": answer_value})

    def answer_dropdown_question(self, answer_value):
        self.post({"dynamic-dropdown-answer": answer_value})

    def answer_mutually_exclusive_question(self, answer_value, exclusive=False):
        answer_id = (
            "dynamic-mutually-exclusive-static-answer"
            if exclusive
            else "dynamic-mutually-exclusive-dynamic-answer"
        )
        self.post({answer_id: answer_value})

    def complete_reference_date_question(self):
        self.post(
            {
                "reference-date-answer-day": "1",
                "reference-date-answer-month": "1",
                "reference-date-answer-year": "2021",
            }
        )

    def assert_dynamic_answer_options(self, schema_name):
        # Given I launch a schema with dynamic options with additional static option
        self.launchSurveyV2(schema_name=schema_name)

        # When I answer the questions using the dynamic options
        self.complete_reference_date_question()
        self.answer_checkbox_question(["2020-12-30", "2020-12-31"])
        self.answer_radio_question("2020-12-29")
        self.answer_dropdown_question("2021-01-02")
        self.answer_mutually_exclusive_question(["2020-12-28", "2021-01-03"])

        # Then my answers should be displayed on the summary page

        # Assert Checkbox answer
        self.assertAnswerInSummary(
            ["Wednesday 30 December 2020", "Thursday 31 December 2020"],
            answer_id="dynamic-checkbox-answer",
        )

        # Assert Radio answer
        self.assertAnswerInSummary(
            "Tuesday 29 December 2020", answer_id="dynamic-radio-answer"
        )

        # Assert Dropdown answer
        self.assertAnswerInSummary(
            "Saturday 2 January 2021", answer_id="dynamic-dropdown-answer"
        )

        # Assert Mutually Exclusive Checkbox answer
        self.assertAnswerInSummary(
            ["Monday 28 December 2020", "Sunday 3 January 2021"],
            answer_id="dynamic-mutually-exclusive-dynamic-answer",
        )

    def assert_dynamic_answer_options_no_answer_provided(self, schema_name):
        # Given I launch a schema with dynamic options with additional static option
        self.launchSurveyV2(schema_name=schema_name, roles=["dumper"])

        # When I Save and continue without answering any questions
        self.complete_reference_date_question()
        self.post()
        self.post()
        self.post()
        self.post()

        # Then for each question "No answer provided" should be displayed on the summary page

        # Assert Checkbox answer
        self.assertAnswerInSummary(
            "No answer provided",
            answer_id="dynamic-checkbox-answer",
        )

        # Assert Radio answer
        self.assertAnswerInSummary(
            "No answer provided", answer_id="dynamic-radio-answer"
        )

        # Assert Dropdown answer
        self.assertAnswerInSummary(
            "No answer provided", answer_id="dynamic-dropdown-answer"
        )

        # Assert Mutually Exclusive Checkbox answer
        self.assertAnswerInSummary(
            "No answer provided",
            answer_id="dynamic-mutually-exclusive-dynamic-answer",
        )

    def assert_questionnaire_submission(self):
        # Ensure we can submit
        self.post()
        self.assertInUrl("/thank-you")
        self.assertInBody("Your answers have been submitted")

    def test_dynamic_answer_options(self):
        for schema_name in [
            "test_dynamic_answer_options_function_driven_with_static_options",
            "test_dynamic_answer_options_function_driven",
        ]:
            with self.subTest(schema_name=schema_name):
                self.setUp()
                self.assert_dynamic_answer_options(schema_name=schema_name)
                self.assert_questionnaire_submission()

    def test_dynamic_answer_options_no_answer_provided(self):
        for schema_name in [
            "test_dynamic_answer_options_function_driven_with_static_options",
            "test_dynamic_answer_options_function_driven",
        ]:
            with self.subTest(schema_name=schema_name):
                self.setUp()
                self.assert_dynamic_answer_options_no_answer_provided(
                    schema_name=schema_name
                )
                self.assert_questionnaire_submission()

    def test_static_answer_options(self):
        # Given I launch a schema with dynamic options with additional static option
        self.launchSurveyV2(
            schema_name="test_dynamic_answer_options_function_driven_with_static_options"
        )

        # When I answer the questions using the static options
        self.complete_reference_date_question()
        self.answer_checkbox_question(["I did not work"])
        self.answer_radio_question("I did not work")
        self.answer_dropdown_question("I did not work")
        self.answer_mutually_exclusive_question(["I did not work"], exclusive=True)

        # Then my answers should be displayed on the summary page which I am able to submit

        # Assert Checkbox answer
        self.assertAnswerInSummary(
            "I did not work",
            answer_id="dynamic-checkbox-answer",
        )

        # Assert Radio answer
        self.assertAnswerInSummary("I did not work", answer_id="dynamic-radio-answer")

        # Assert Dropdown answer
        self.assertAnswerInSummary(
            "I did not work", answer_id="dynamic-dropdown-answer"
        )

        # Assert Mutually Exclusive Checkbox answer
        self.assertAnswerInSummary(
            "I did not work",
            answer_id="dynamic-mutually-exclusive-static-answer",
        )

        self.assert_questionnaire_submission()

    def test_dynamic_options_answer_cleared_on_dependency_change(self):
        # Given I launch a schema and submit an answer for a question which has dynamic options
        self.launchSurveyV2(
            schema_name="test_dynamic_answer_options_function_driven_with_static_options"
        )
        self.complete_reference_date_question()
        self.answer_checkbox_question(["2020-12-29", "2020-12-30"])
        self.previous()

        assert self.is_input_checked("dynamic-checkbox-answer-1")
        assert self.is_input_checked("dynamic-checkbox-answer-2")

        # When I change the answer which the dynamic options is dependent on
        self.previous()
        self.post(
            {
                "reference-date-answer-day": "2",
                "reference-date-answer-month": "1",
                "reference-date-answer-year": "2021",
            }
        )

        # Then the answers provided in the dynamic options question are removed
        assert not self.is_input_checked("dynamic-checkbox-answer-1")
        assert not self.is_input_checked("dynamic-checkbox-answer-2")

    def is_input_checked(self, element_id):
        return self.getHtmlSoup().find("input", {"id": element_id}).has_attr("checked")
