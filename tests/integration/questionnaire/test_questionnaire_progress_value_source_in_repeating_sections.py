from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireProgressValueSourceInRepeatingSections(IntegrationTestCase):
    def answer_dob(self, payload=None):
        if not payload:
            payload = {
                "date-of-birth-answer-year": "1998",
                "date-of-birth-answer-month": "12",
                "date-of-birth-answer-day": 12,
            }
        self.post(payload)

    def answer_dob_second_repeat(self, payload=None):
        if not payload:
            payload = {
                "second-date-of-birth-answer-year": "1998",
                "second-date-of-birth-answer-month": "12",
                "second-date-of-birth-answer-day": 12,
            }
        self.post(payload)

    def john_doe_link(self):
        return self.getHtmlSoup().find("a", {"data-qa": "hub-row-section-2-1-link"})[
            "href"
        ]

    def james_bond_link(self):
        return self.getHtmlSoup().find("a", {"data-qa": "hub-row-section-2-2-link"})[
            "href"
        ]

    def jane_doe_link(self):
        return self.getHtmlSoup().find("a", {"data-qa": "hub-row-section-4-1-link"})[
            "href"
        ]

    def add_person(self, first_name, last_name):
        self.assertInBody("What is the name of the person?")
        self.post({"first-name": first_name, "last-name": last_name})

    def add_person_second_list_collector(self, first_name, last_name):
        self.assertInBody("What is the name of the person?")
        self.post({"second-first-name": first_name, "second-last-name": last_name})

    def assert_section_status(self, section_index, status, other_labels=None):
        self.assertInSelector(status, self.row_selector(section_index))
        if other_labels and len(other_labels):
            for other_label in other_labels:
                self.assertInSelector(other_label, self.row_selector(section_index))

    def go_to_section(self, section_id):
        self.get(f"/questionnaire/sections/{section_id}/")

    def go_to_hub(self):
        self.get("/questionnaire/")

    def test_disable_block_in_repeating_section_if_block_source_progress_not_completed(
        self,
    ):
        """
        Test that a block inside a repeating section is disabled if the progress value source
        from a block in another section is not completed
        """

        self.launchSurvey("test_progress_block_value_source_repeating_sections")

        self.assertInBody("Choose another section to complete")

        # 1. First section shows as not started
        self.assertInSelector("List collector + random question", self.row_selector(1))
        self.assert_section_status(1, "Not started")

        # 2. Start completing section 1 and add 2 people
        # Don't answer the random question enabler
        self.go_to_section("section-1")
        self.assertInBody("Does anyone else live here?")
        self.post({"anyone-else": "Yes"})

        self.add_person("John", "Doe")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("John Doe", self.row_selector(1))
        self.post({"anyone-else": "Yes"})

        self.add_person("James", "Bond")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("James Bond", self.row_selector(2))
        self.post({"anyone-else": "No"})

        self.post()

        # 3. Assert random question is there
        self.assertInBody("Random question enabler")

        # 4. Go back to the hub and leave random question block incomplete
        self.go_to_hub()

        # 5. The two repeating sections should show as "not started"
        self.assertInBody("Choose another section to complete")
        self.assert_section_status(2, "Not started", ["John Doe"])
        self.assert_section_status(3, "Not started", ["James Bond"])

        # 5. Complete John Doe section
        # Random question doesn't show
        self.get(self.john_doe_link())
        self.assertInBody("John Doe")
        self.answer_dob()

        # Assert random question not there
        self.assertNotInBody("Random question about")

    def test_disable_block_in_repeating_section_if_section_source_progress_not_completed(
        self,
    ):
        """
        Test that a block inside a repeating section is disabled if the progress value source
        from a block in another section is not completed
        """

        self.launchSurvey("test_progress_section_value_source_repeating_sections")

        self.assertInBody("Choose another section to complete")

        # 1. First section shows as not started
        self.assertInSelector("List collector + random question", self.row_selector(1))
        self.assert_section_status(1, "Not started")

        # 2. Start completing section 1 and add 2 people
        # Don't answer the random question enabler
        self.go_to_section("section-1")
        self.assertInBody("Does anyone else live here?")
        self.post({"anyone-else": "Yes"})

        self.add_person("John", "Doe")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("John Doe", self.row_selector(1))
        self.post({"anyone-else": "Yes"})

        self.add_person("James", "Bond")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("James Bond", self.row_selector(2))
        self.post({"anyone-else": "No"})

        self.post()

        # 3. Assert random question is there
        self.assertInBody("Random question enabler")

        # 4. Go back to the hub and leave random question block incomplete
        self.go_to_hub()

        # 5. The two repeating sections should show as "not started"
        self.assertInBody("Choose another section to complete")
        self.assert_section_status(2, "Not started", ["John Doe"])
        self.assert_section_status(3, "Not started", ["James Bond"])

        # 5. Complete John Doe section
        # Random question doesn't show
        self.get(self.john_doe_link())
        self.assertInBody("John Doe")
        self.answer_dob()

        # Assert random question not there
        self.assertNotInBody("Random question about")

    def test_enable_block_in_repeating_section_if_block_source_progress_is_completed(
        self,
    ):
        """
        Test that a block inside a repeating section is enabled if the progress value source
        from a block in another section is completeted
        """

        self.launchSurvey("test_progress_block_value_source_repeating_sections")

        self.assertInBody("Choose another section to complete")

        # 1. Complete 1st section and add 2 people
        # And answer the random question enabler
        self.go_to_section("section-1")
        self.assertInBody("Does anyone else live here?")
        self.post({"anyone-else": "Yes"})

        self.add_person("John", "Doe")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("John Doe", self.row_selector(1))
        self.post({"anyone-else": "Yes"})

        self.add_person("James", "Bond")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("James Bond", self.row_selector(2))
        self.post({"anyone-else": "No"})

        self.post()

        self.assertInBody("Random question enabler")
        self.post({"random-question-enabler-answer": 1})

        # Go back to the hub
        self.go_to_hub()
        self.assertInBody("Choose another section to complete")

        # Assert first section completed
        self.assert_section_status(1, "Completed", ["List collector + random question"])

        # 2. Complete John Doe section
        self.get(self.john_doe_link())
        self.assertInBody("John Doe")
        self.answer_dob()

        # 3. Assert random question shows up
        self.assertInBody("Random question")

    def test_enable_block_in_repeating_section_if_section_source_progress_is_completed(
        self,
    ):
        """
        Test that a block inside a repeating section is enabled if the progress value source
        from a block in another section is completeted
        """
        self.launchSurvey("test_progress_section_value_source_repeating_sections")

        self.assertInBody("Choose another section to complete")

        # 1. Complete 1st section and add 2 people
        # And answer the random question enabler
        self.go_to_section("section-1")
        self.assertInBody("Does anyone else live here?")
        self.post({"anyone-else": "Yes"})

        self.add_person("John", "Doe")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("John Doe", self.row_selector(1))
        self.post({"anyone-else": "Yes"})

        self.add_person("James", "Bond")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("James Bond", self.row_selector(2))
        self.post({"anyone-else": "No"})

        self.post()

        self.assertInBody("Random question enabler")
        self.post({"random-question-enabler-answer": 1})

        self.post()

        # Go back to the hub
        self.go_to_hub()
        self.assertInBody("Choose another section to complete")

        # Assert first section completed
        self.assert_section_status(1, "Completed", ["List collector + random question"])

        # 2. Complete John Doe section
        self.get(self.john_doe_link())
        self.assertInBody("John Doe")
        self.answer_dob()

        # 3. Assert random question shows up
        self.assertInBody("Random question")

    def test_block_progress_dependencies_updated_in_repeating_sections(self):
        """
        Test that dependency blocks inside repeating sections are updated properly
        """

        self.launchSurvey("test_progress_block_value_source_repeating_sections")

        self.assertInBody("Choose another section to complete")

        # 1. Complete 1st section and add 2 people
        # Don't answer the random question enabler
        self.go_to_section("section-1")
        self.assertInBody("Does anyone else live here?")
        self.post({"anyone-else": "Yes"})

        self.add_person("John", "Doe")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("John Doe", self.row_selector(1))
        self.post({"anyone-else": "Yes"})

        self.add_person("James", "Bond")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("James Bond", self.row_selector(2))
        self.post({"anyone-else": "No"})

        self.post()

        self.assertInBody("Random question enabler")

        # 2. Go back to the hub and leave random question block incomplete
        self.go_to_hub()

        # 3. Repeating sections show as "Not started"
        self.assertInBody("Choose another section to complete")
        self.assert_section_status(2, "Not started", ["John Doe"])
        self.assert_section_status(3, "Not started", ["James Bond"])

        # 4. Complete John Doe section
        self.get(self.john_doe_link())
        self.assertInBody("John Doe")
        self.answer_dob()

        # 5. Assert random question not there
        self.assertNotInBody("Random question about")

        # 6. Go back to section 1 and complete random question
        self.go_to_section("section-1")
        self.assertInBody("Random question enabler")
        self.post({"random-question-enabler-answer": 1})

        # 7. Go back to the hub
        self.go_to_hub()

        # 8. Assert sections 1 is completed and repeating sections are partially completed
        self.assertInBody("Choose another section to complete")
        self.assert_section_status(1, "Completed", ["List collector + random question"])
        self.assert_section_status(
            2, "Partially completed", ["John Doe", "Continue with section"]
        )
        self.assert_section_status(3, "Not started", ["James Bond"])

        # 9. Go back to John Doe section
        self.get(self.john_doe_link())

        # 10. Assert prompts for random question
        self.assertInBody("Random question about")
        self.post({"other-answer": 1})

        # 12. Assert it goes to the section summary
        self.assertInUrl("questionnaire/sections/section-2")

        # 13. Assert answer was provided
        self.assertInSelector("Random question about", self.row_selector(2))
        self.assertNotInSelector("No answer provided", self.row_selector(2))

        # 14. Go back to summary
        self.go_to_hub()

        # 15. Assert John Doe section is completed
        self.assert_section_status(2, "Completed", ["John Doe"])

        # 15. Edit James Bond section
        self.get(self.james_bond_link())
        self.assertInBody("James Bond")
        self.answer_dob()

        # 16. Assert random question shows up
        self.assertInBody("Random question about")

    def test_section_progress_dependencies_updated_in_repeating_sections(self):
        """
        Test that dependency blocks inside repeating sections are updated properly
        """

        self.launchSurvey("test_progress_section_value_source_repeating_sections")

        self.assertInBody("Choose another section to complete")

        # 1. Complete 1st section and add 2 people
        # Don't answer the random question enabler
        self.go_to_section("section-1")
        self.assertInBody("Does anyone else live here?")
        self.post({"anyone-else": "Yes"})

        self.add_person("John", "Doe")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("John Doe", self.row_selector(1))
        self.post({"anyone-else": "Yes"})

        self.add_person("James", "Bond")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("James Bond", self.row_selector(2))
        self.post({"anyone-else": "No"})

        self.post()

        self.assertInBody("Random question enabler")

        # 2. Go back to the hub and leave random question block incomplete
        self.go_to_hub()

        # 3. Repeating sections show as "Not started"
        self.assertInBody("Choose another section to complete")
        self.assert_section_status(2, "Not started", ["John Doe"])
        self.assert_section_status(3, "Not started", ["James Bond"])

        # 4. Complete John Doe section
        self.get(self.john_doe_link())
        self.assertInBody("John Doe")
        self.answer_dob()

        # 5. Assert random question not there
        self.assertNotInBody("Random question about")

        # 6. Go back to section 1 and complete random question
        self.go_to_section("section-1")
        self.assertInBody("Random question enabler")
        self.post({"random-question-enabler-answer": 1})

        # 7. Go back to the hub
        self.go_to_hub()

        # 8. Assert sections 1 is completed and repeating sections are partially completed
        self.assertInBody("Choose another section to complete")
        self.assert_section_status(1, "Completed", ["List collector + random question"])
        self.assert_section_status(
            2, "Partially completed", ["John Doe", "Continue with section"]
        )
        self.assert_section_status(3, "Not started", ["James Bond"])

        # 9. Go back to John Doe section
        self.get(self.john_doe_link())

        # 10. Assert prompts for random question
        self.assertInBody("Random question about")
        self.post({"other-answer": 1})

        # 12. Assert it goes to the section summary
        self.assertInUrl("questionnaire/sections/section-2")

        # 13. Assert answer was provided
        self.assertInSelector("Random question about", self.row_selector(2))
        self.assertNotInSelector("No answer provided", self.row_selector(2))

        # 14. Go back to summary
        self.go_to_hub()

        # 15. Assert John Doe section is completed
        self.assert_section_status(2, "Completed", ["John Doe"])

        # 15. Edit James Bond section
        self.get(self.james_bond_link())
        self.assertInBody("James Bond")
        self.answer_dob()

        # 16. Assert random question shows up
        self.assertInBody("Random question about")

    def test_section_progress_dependencies_updated_in_repeating_sections_with_chained_dependencies(
        self,
    ):
        """
        Test that dependency blocks inside repeating sections are updated properly when there are chained dependencies
        """
        self.launchSurvey(
            "test_progress_value_source_repeating_sections_chained_dependencies"
        )

        self.assertInBody("Choose another section to complete")

        # 1. Complete 3rd section and add 2 people
        # And answer the random question enabler
        self.go_to_section("section-3")
        self.assertInBody("Does anyone else live here?")
        self.post({"second-anyone-else": "Yes"})

        self.add_person_second_list_collector("Jane", "Doe")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("Jane Doe", self.row_selector(1))
        self.post({"second-anyone-else": "Yes"})

        self.add_person_second_list_collector("Marie", "Clare")

        self.assertInBody("Does anyone else live here?")
        self.assertInSelector("Marie Clare", self.row_selector(2))
        self.post({"second-anyone-else": "No"})

        self.post()

        self.assertInBody("Random question enabler")
        self.post({"second-random-question-enabler-answer": 1})

        self.post()

        # Go back to the hub
        self.go_to_hub()

        # 2. The two repeating sections should show as "not started"
        self.assertInBody("Choose another section to complete")
        self.assert_section_status(4, "Not started", ["Jane Doe"])
        self.assert_section_status(5, "Not started", ["Marie Clare"])

        # 3. Complete Jane Doe section
        self.get(self.jane_doe_link())
        self.assertInBody("Jane Doe")
        self.answer_dob_second_repeat()
        self.post({"second-other-answer": 1})

        # Go back to the hub
        self.go_to_hub()

        # 4. The Jane Doe section should now be Complete
        self.assertInBody("Choose another section to complete")
        self.assert_section_status(4, "Completed", ["Jane Doe"])
        self.assert_section_status(5, "Not started", ["Marie Clare"])

        # 5. Complete section 2
        self.go_to_section("section-2")
        self.post({"s2-b2-q1-a1": 1})

        # 6. Section-2 and should be complete but the Jane Doe section should be partially completed
        self.assertInBody("Choose another section to complete")
        self.assert_section_status(2, "Completed")
        self.assert_section_status(4, "Partially completed", ["Jane Doe"])
        self.assert_section_status(5, "Not started", ["Marie Clare"])

        # 5. Complete section 1
        self.go_to_section("section-1")
        self.post({"s1-b1-q1-a1": 1})

        # 6. Section 1 and the Jane Doe section should now be but complete
        # but Section-2 should be partially completed
        self.assertInBody("Choose another section to complete")
        self.assert_section_status(1, "Completed")
        self.assert_section_status(2, "Partially completed")
        self.assert_section_status(4, "Completed", ["Jane Doe"])
        self.assert_section_status(5, "Not started", ["Marie Clare"])
