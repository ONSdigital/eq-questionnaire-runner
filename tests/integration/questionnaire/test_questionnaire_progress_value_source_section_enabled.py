from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireProgressValueSource(IntegrationTestCase):
    def assert_section_status(self, section_index, status, other_labels=None):
        self.assertInSelector(status, self.row_selector(section_index))
        if other_labels and len(other_labels) > 0:
            for other_label in other_labels:
                self.assertInSelector(other_label, self.row_selector(section_index))

    def go_to_section(self, section_id):
        self.get(f"/questionnaire/sections/{section_id}/")

    def go_to_hub(self):
        self.get("/questionnaire/")

    def test_enable_section_by_progress_linear_flow(self):
        """
        Test that a section is enabled by progress value source
        In a linear flow with no hub
        """

        self.launchSurveyV2(
            schema_name="test_progress_value_source_section_enabled_no_hub"
        )

        self.assertInBody("Section 1 Question 1")
        self.post({"s1-b1-q1-a1": 1})

        self.assertInBody("Section 1 Question 2")
        self.post({"s1-b2-q1-a1": 1})

        self.assertInBody("Section 2 Question 1")
        self.post({"s2-b1-q1-a1": 1})

    def test_enable_section_by_progress_hub_flow(self):
        """
        Test that a section is enabled by progress value source
        In a hub flow
        """

        self.launchSurveyV2(
            schema_name="test_progress_value_source_section_enabled_hub"
        )

        # 1. Only section 1 shows on the hub
        self.assertInBody("Choose another section to complete")
        self.assertInBody("Section 1")
        self.assertNotInBody("Section 2")

        # 2. Complete section 1
        self.go_to_section("section-1")
        self.assertInBody("Section 1 Question 1")
        self.post({"s1-b1-q1-a1": 1})

        self.assertInUrl("/questionnaire/s1-b2")
        self.post({"s1-b2-q1-a1": 1})

        # 3. Assert section 1 completed on the hub
        self.assertEqualUrl("/questionnaire/")

        self.assert_section_status(1, "Completed", ["View answers"])

        # 4. Assert section 2 is now available on the hub
        self.assert_section_status(2, "Not started", ["Start section"])

        # 5. Complete section 2
        self.go_to_section("section-2")
        self.assertInUrl("/questionnaire/s2-b1")
        self.post({"s2-b1-q1-a1": 1})

        self.assertEqualUrl("/questionnaire/")

        # 6. Assert section 2 completed on the hub
        self.assert_section_status(1, "Completed", ["View answers"])
        self.assert_section_status(2, "Completed", ["View answers"])

        self.assertInBody("Submit survey")

    def test_value_source_dependency_enable_section_by_progress_hub_flow(self):
        """
        Test that dependencies that rely on a section's progress
        are updated when the section progress changes
        """

        self.launchSurveyV2(
            schema_name="test_progress_value_source_section_enabled_hub"
        )

        self.assertInBody("Choose another section to complete")
        self.assertInBody("Section 1")
        self.assertNotInBody("Section 2")

        # 1. Start section 1
        self.go_to_section("section-1")
        self.assertInBody("Section 1 Question 1")
        self.post({"s1-b1-q1-a1": 1})

        self.assertInBody("Section 1 Question 2")

        # 2. Leave section 1 incomplete
        self.get("/questionnaire/")

        # 3. Assert that section 2 is not enabled
        self.assertNotInBody("Section 2")

        # 4. Assert section 1 is in progress
        self.assert_section_status(1, "Partially completed", ["Continue with section"])

        # 5. Go back to section 1 and complete it
        self.get("/questionnaire/sections/section-1/?resume=True")

        self.assertInBody("Section 1 Question 2")
        self.post({"s1-b2-q1-a1": 1})

        self.assertEqualUrl("/questionnaire/")

        # 6. Assert section 1 completed on the hub
        self.assert_section_status(1, "Completed", ["View answers"])

        # 7. Assert that section 2 is now enabled
        self.assert_section_status(2, "Not started", ["Start section"])

    def test_enable_section_by_progress_hub_complex_happy_path(self):
        self.launchSurveyV2(
            schema_name="test_progress_value_source_section_enabled_hub_complex"
        )

        self.assertInBody("Choose another section to complete")
        self.assertInBody("Section 1")
        self.assertInBody("Section 3")
        self.assertNotInBody("Section 2")

        # 1. Complete section 1
        self.go_to_section("section-1")
        self.assertInBody("Section 1 Question 1")
        self.post({"s1-b1-q1-a1": 1})

        self.assertInBody("Section 1 Question 2")
        self.post({"s1-b2-q1-a1": 1})

        # 2. Complete section 2 with all the questions
        self.assertInBody("Choose another section to complete")
        self.assertInBody("Section 2")
        self.go_to_section("section-2")

        self.assertInBody("Section 2 Question 1")
        self.post({"s2-b1-q1-a1": 1})

        self.assertInBody("Section 2 Question 2")
        self.post({"s2-b2-q1-a1": 0})

        self.assertInBody("Section 2 Question 3")
        self.post({"s2-b3-q1-a1": 0})

        # 3. Assert section 3 is on the path
        self.assertInBody("Choose another section to complete")
        self.assertInBody("Section 3")
        self.go_to_section("section-3")
        self.assertInUrl("/questionnaire/s3-b1")

        # 4. Complete section 3
        self.assertInBody("Section 3 Question 1")
        self.post({"s3-b1-q1-a1": 0})

        # 5. Complete section 4
        self.assertInBody("Choose another section to complete")
        self.assertInBody("Section 4")
        self.go_to_section("section-4")
        self.assertInUrl("/questionnaire/s4-b1")

        self.assertInBody("Section 4 Question 1")
        self.post({"s4-b1-q1-a1": 0})

        # 6. Assert all sections have been completed

        for sel in (
            self.row_selector(1),
            self.row_selector(2),
            self.row_selector(3),
            self.row_selector(4),
        ):
            self.assertInSelector("Completed", sel)
            self.assertInSelector("View answers", sel)
