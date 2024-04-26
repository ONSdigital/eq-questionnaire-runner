from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireProgressValueSource(IntegrationTestCase):
    def john_doe_link(self):
        return self.getHtmlSoup().find("a", {"data-qa": "hub-row-section-3-1-link"})[
            "href"
        ]

    def james_bond_link(self):
        return self.getHtmlSoup().find("a", {"data-qa": "hub-row-section-3-2-link"})[
            "href"
        ]

    def section_one_link(self):
        return self.getHtmlSoup().find("a", {"data-qa": "hub-row-section-1-link"})[
            "href"
        ]

    def add_person(self, first_name, last_name):
        self.assertEqualUrl("/questionnaire/people/add-person/")
        self.post({"first-name": first_name, "last-name": last_name})

    def assert_section_status(self, section_index, status, other_labels=None):
        self.assertInSelector(status, self.row_selector(section_index))
        if other_labels and len(other_labels) > 0:
            for other_label in other_labels:
                self.assertInSelector(other_label, self.row_selector(section_index))

    def answer_dob(self, payload=None):
        if not payload:
            payload = {
                "date-of-birth-answer-year": "1998",
                "date-of-birth-answer-month": "12",
                "date-of-birth-answer-day": 12,
            }
        self.post(payload)

    def go_to_section(self, section_id):
        self.get(f"/questionnaire/sections/{section_id}/")

    def go_to_hub(self):
        self.get("/questionnaire/")

    # pylint: disable=locally-disabled, too-many-statements
    def test_happy_path(self):
        self.launchSurveyV2(schema_name="test_progress_value_source_calculated_summary")

        self.assertInBody("Choose another section to complete")
        self.assertInBody("Calculated Summary")
        self.assertInBody("Skippable random question + List collector")

        # 1. Complete the first section
        self.go_to_section("section-1")
        self.assertInUrl("/questionnaire/first-number-block/")
        self.assertInBody("First Number Question Title")
        self.post({"first-number-answer": 1})

        self.assertInUrl("/questionnaire/second-number-block")
        self.assertInBody("Second Number Question Title")
        self.post({"second-number-answer": 1})

        # 2. Should be on the calculated summary page
        self.assertEqualUrl("/questionnaire/calculated-summary-block/")

        self.assertInSelector("First answer label", self.row_selector(1))
        self.assertInSelector("£1.00", self.row_selector(1))
        self.assertInSelector("Change", self.row_selector(1))

        self.assertInSelector("Second answer label", self.row_selector(2))
        self.assertInSelector("£1.00", self.row_selector(2))
        self.assertInSelector("Change", self.row_selector(2))

        self.post()
        self.post()

        # 3. Should be on the hub page
        self.assertEqualUrl("/questionnaire/")
        self.assertInBody("Choose another section to complete")

        # 4. 1st section should be marked as complete
        self.assert_section_status(1, "Completed", ["View answers"])

        # 5. Complete the second section
        # 6. Random question shows
        self.go_to_section("section-2")
        self.assertInUrl("/questionnaire/s2-b1/")
        self.assertInBody("Skippable random question")
        self.post({"s2-b1-q1-a1": 1})

        # 7. Add two people
        self.assertEqualUrl("/questionnaire/list-collector/")
        self.post({"anyone-else": "Yes"})
        self.add_person("John", "Doe")

        self.assertEqualUrl("/questionnaire/list-collector/")
        self.post({"anyone-else": "Yes"})
        self.add_person("James", "Bond")

        self.post({"anyone-else": "No"})

        # 8. Two new sections should be available on the hub
        self.assert_section_status(3, "Not started", ["John Doe"])
        self.assert_section_status(4, "Not started", ["James Bond"])

        # 9. Complete the John Doe section, random question shows
        self.get(self.john_doe_link())

        self.assertInBody("John Doe")

        self.answer_dob()

        self.assertInBody("Random question about")
        self.post({"other-answer": 1})

        self.assertInBody("Another random question about")
        self.post({"other-answer-2": 1})

        self.assertInUrl("/questionnaire/sections/section-3/")

        self.post()

        # 10. John Doe section should be marked as complete
        self.assert_section_status(3, "Completed", ["John Doe"])
        self.assert_section_status(4, "Not started", ["James Bond"])

        # 11. Complete the James Bond section, random question shows
        self.get(self.james_bond_link())

        self.assertInBody("James Bond")

        self.answer_dob()

        self.assertInBody("Random question about")
        self.post({"other-answer": 1})

        self.assertInBody("Another random question about")
        self.post({"other-answer-2": 1})

        self.assertInUrl("/questionnaire/sections/section-3/")

        self.post()

        # 12. James Bond section should be marked as complete
        self.assert_section_status(4, "Completed", ["James Bond"])

    # pylint: disable=locally-disabled, too-many-statements
    def test_calculated_summary_first_incomplete_then_complete(self):
        self.launchSurveyV2(schema_name="test_progress_value_source_calculated_summary")

        # 1. Start completing the first section
        self.go_to_section("section-1")
        self.post({"first-number-answer": 1})

        self.post({"second-number-answer": 1})

        self.assertEqualUrl("/questionnaire/calculated-summary-block/")

        # 2. Go back to the hub BEFORE completing the section
        self.go_to_hub()

        # 3. Section 1 should show as partially complete
        self.assert_section_status(1, "Partially completed", ["Continue with section"])

        # 4. Complete the second section
        self.go_to_section("section-2")

        self.assertNotInBody("Skippable random question")
        self.assertEqualUrl("/questionnaire/list-collector/")

        self.post({"anyone-else": "Yes"})
        self.add_person("John", "Doe")
        self.post({"anyone-else": "Yes"})
        self.add_person("James", "Bond")
        self.post({"anyone-else": "No"})

        # 5. Section 2 should show as complete
        self.assert_section_status(2, "Completed")

        # 6. Complete the John Doe section. Random question DOES NOT show because section 1 is not complete
        self.get(self.john_doe_link())

        self.answer_dob()

        self.assertNotInBody("Random question about")
        self.post()

        self.assertEqualUrl("/questionnaire/")

        # 7. On the hub, John Doe section shows as completted
        self.assert_section_status(3, "Completed", ["John Doe"])

        # 8. Complete the James Bond section. Random question DOES NOT show because section 1 is not complete
        self.get(self.james_bond_link())

        self.assertInBody("James Bond")

        self.answer_dob()

        self.assertNotInBody("Random question about")
        self.post()

        self.assertEqualUrl("/questionnaire/")

        # 9. On the hub, James Bond section shows as completed
        self.assert_section_status(4, "Completed", ["James Bond"])

        # 10. Go back to calculated summary (section 1) and complete it
        self.get("/questionnaire/calculated-summary-block/?resume=True")
        self.assertInBody("We calculate the total of currency values entered to be")
        self.post()
        self.post()

        # 11. Dependent sections should have been updated to partially completed
        self.assert_section_status(1, "Completed")
        self.assert_section_status(
            2, "Partially completed", ["Skippable random question + List collector"]
        )
        self.assert_section_status(3, "Partially completed", ["John Doe"])
        self.assert_section_status(4, "Partially completed", ["James Bond"])

        # 12. Go back to section 2 and complete it
        # Random question SHOWS because section 1 is now completed
        self.go_to_section("section-2")
        self.assertInBody("Skippable random question")
        self.post({"s2-b1-q1-a1": 1})

        # 13. Section 2 shows as completed on the hub
        self.assertEqualUrl("/questionnaire/")
        self.assertInBody("Choose another section to complete")

        self.assert_section_status(2, "Completed")

        # 14. Go back to John Doe section and complete it
        # Random questions show because section 1 is now complete
        self.get(self.john_doe_link())
        self.assertInBody("Random question about")
        self.post({"other-answer": 1})
        self.assertInBody("Another random question about")
        self.post({"other-answer-2": 1})
        self.post()

        self.assertEqualUrl("/questionnaire/")

        # 15. Go back to James Bond section and complete it
        # Random questions show because section 1 is now complete
        self.get(self.james_bond_link())
        self.assertInBody("Random question about")
        self.post({"other-answer": 1})
        self.assertInBody("Another random question about")
        self.post({"other-answer-2": 1})
        self.post()

        self.assertEqualUrl("/questionnaire/")

        # 16. All sections should show as completed on the hub
        self.assert_section_status(3, "Completed", ["John Doe"])
        self.assert_section_status(4, "Completed", ["James Bond"])

    def test_happy_path_then_make_calculated_summary_incomplete(self):
        self.launchSurveyV2(schema_name="test_progress_value_source_calculated_summary")

        # 1. Complete section 1
        self.go_to_section("section-1")
        self.post({"first-number-answer": 1})

        self.post({"second-number-answer": 1})

        self.post()
        self.post()

        # 2. Complete section 2 and add two people
        self.go_to_section("section-2")
        self.post({"s2-b1-q1-a1": 1})

        self.post({"anyone-else": "Yes"})
        self.add_person("John", "Doe")

        self.post({"anyone-else": "Yes"})
        self.add_person("James", "Bond")

        self.post({"anyone-else": "No"})

        # 3. Complete John Doe section
        self.get(self.john_doe_link())

        self.answer_dob()

        self.post({"other-answer": 1})

        self.post({"other-answer-2": 1})

        self.post()

        # 4. Complete James Bond section
        self.get(self.james_bond_link())

        self.answer_dob()

        self.post({"other-answer": 1})

        self.post({"other-answer-2": 1})

        self.post()

        # END OF HAPPY PATH

        # 5. Go back to calculated summary and make it incomplete
        self.get("/questionnaire/calculated-summary-block/")
        # Edit first answer
        first_answer_link = self.getHtmlSoup().find(
            "a", {"data-qa": "first-number-answer-edit"}
        )["href"]
        self.get(first_answer_link)
        self.post({"first-number-answer": 2})

        # Don't complete the calculated summary, go back to the hub
        self.go_to_hub()

        # 6. Section 1 should show as partially completed on the hub
        # Other sections should show as completed
        self.assert_section_status(1, "Partially completed")
        self.assert_section_status(2, "Completed")
        self.assert_section_status(3, "Completed")
        self.assert_section_status(4, "Completed")

        self.get("/questionnaire/sections/section-2/")
        # No random question
        self.assertInBody("Does anyone else live here?")

        self.go_to_hub()

        self.get(self.john_doe_link())
        self.assertNotInBody("Random question about")

        self.go_to_hub()

        self.get(self.james_bond_link())
        self.assertNotInBody("Random question about")

    def test_progress_value_source_with_backward_chained_dependencies(self):
        self.launchSurveyV2(
            schema_name="test_progress_value_source_calculated_summary_extended"
        )
        self.post()

        # 1. Complete section 7
        self.go_to_section("section-7")
        self.post({"s7-b3-q1-a1": 1})

        # Check the section is complete
        self.assertEqualUrl("/questionnaire/")
        self.assert_section_status(6, "Completed")

        # 2. Complete section 5, will change the status of section 7 to partially completed
        self.go_to_section("section-5")
        self.post({"s5-b2-q1-a1": 1})

        # Check the section is complete
        self.assertEqualUrl("/questionnaire/")
        self.assert_section_status(4, "Completed")
        self.assert_section_status(6, "Partially completed")

        # 2. Complete section 1, this will change the status of section 5 to partially completed
        # and section 7 should once again be complete
        self.go_to_section("section-1")
        self.post({"first-number-answer": 1})

        self.post({"second-number-answer": 1})

        self.post()

        # Check the section is complete
        self.assertEqualUrl("/questionnaire/")
        self.assert_section_status(1, "Completed")
        self.assert_section_status(4, "Partially completed")
        self.assert_section_status(6, "Completed")

    def test_progress_value_source_with_chained_dependencies(self):
        self.launchSurveyV2(
            schema_name="test_progress_value_source_calculated_summary_extended"
        )
        self.post()

        # 1. Complete section 8, 9, 10, 11 and 12
        self.go_to_section("section-12")
        self.post({"s12-b2-q1-a1": 1})

        self.go_to_section("section-11")
        self.post({"s11-b2-q1-a1": 1})

        self.go_to_section("section-8")
        self.post({"s8-b3-q1-a1": 1})

        self.go_to_section("section-9")
        self.post({"s9-b2-q1-a1": 1})

        self.go_to_section("section-10")
        self.post({"s10-b2-q1-a1": 1})

        # Check that sections 8, 9 and 10 are complete, and 11 and 12 are partially complete
        self.assertEqualUrl("/questionnaire/")
        self.assert_section_status(7, "Completed")
        self.assert_section_status(8, "Completed")
        self.assert_section_status(9, "Completed")
        self.assert_section_status(10, "Partially completed")
        self.assert_section_status(11, "Partially completed")

        # 2. Update the second section, this should make sections
        self.go_to_section("section-2")
        self.post({"s2-b1-q1-a1": 1})
        self.post({"anyone-else": "No"})

        # Check that section 11 and 12 are complete, and 8, 9 and 10 are partially complete
        self.assertEqualUrl("/questionnaire/")
        self.assert_section_status(2, "Completed")
        self.assert_section_status(7, "Partially completed")
        self.assert_section_status(8, "Partially completed")
        self.assert_section_status(9, "Partially completed")
        self.assert_section_status(10, "Completed")
        self.assert_section_status(11, "Completed")
