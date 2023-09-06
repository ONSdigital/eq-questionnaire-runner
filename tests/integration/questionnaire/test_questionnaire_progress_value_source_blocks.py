from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.questionnaire import SUBMIT_URL_PATH


class TestQuestionnaireProgressValueSourceBlocks(IntegrationTestCase):
    def go_to_section(self, section_id):
        self.get(f"/questionnaire/sections/{section_id}/")

    def test_skip_condition_block_not_complete(self):
        """
        Test that a block is skipped if the progress value source is not complete
        """

        self.launchSurvey("test_progress_value_source_blocks")

        self.assertInBody("Section 1 Question 1")
        self.post({"s1-b1-q1-a1": 0})

        # Routes to block 3 because answer to block 1 is 0
        self.assertInBody("Section 1 Question 3")
        self.post({"s1-b3-q1-a1": 1})

        # Block 4 is skipped because block 2 is not complete
        self.assertInBody("Section 1 Question 5")

    def test_routing_condition_block_not_complete(self):
        """
        Test that routes to proper block if the progress value source is not complete
        """

        self.launchSurvey("test_progress_value_source_blocks")

        self.assertInBody("Section 1 Question 1")
        self.post({"s1-b1-q1-a1": 0})

        # Routes to block 3 because answer to block 1 is 0
        self.assertInBody("Section 1 Question 3")
        self.post({"s1-b3-q1-a1": 1})

        # Block 4 is skipped because block 2 is not complete
        self.assertInBody("Section 1 Question 5")
        self.post({"s1-b5-q1-a1": 1})

        # Routes to block 7 because answer to block 2 is not complete
        self.assertInBody("Section 1 Question 7")
        self.post({"s1-b7-q1-a1": 1})

    def test_block_value_source_dependencies_updated(self):
        """
        Test that the block value source dependencies are updated when a dependent block progress changes
        """

        self.launchSurvey("test_progress_value_source_blocks")

        self.assertInBody("Section 1 Question 1")
        self.post({"s1-b1-q1-a1": 0})

        # Routes to block 3 because answer to block 1 is 0
        self.assertInBody("Section 1 Question 3")
        self.post({"s1-b3-q1-a1": 1})

        # Block 4 is skipped because block 2 is not complete
        self.assertInBody("Section 1 Question 5")
        self.post({"s1-b5-q1-a1": 1})

        # Routes to block 7 because answer to block 2 is not complete
        self.assertInBody("Section 1 Question 7")
        self.post({"s1-b7-q1-a1": 1})

        self.assertInBody("Check your answers and submit")

        # Change block 1 answer to 1
        self.get(
            "/questionnaire/s1-b1/?return_to=final-summary&return_to_answer_id=s1-b1-q1-a1#s1-b1-q1-a1"
        )
        self.assertInBody("Section 1 Question 1")
        self.post({"s1-b1-q1-a1": 1})

        # Routes to block 2 because answer to block 1 is now 1
        self.assertInBody("Section 1 Question 2")
        self.post({"s1-b2-q1-a1": 1})

        # Routes to block 4 as it is the next incomplete block and no longer skipped because answer to block 1 is now 1.
        self.assertInBody("Section 1 Question 4")
        self.post({"s1-b4-q1-a1": 1})

        # Routes to block 6 as its the next incomplete block and no longer skipped because block 4 is answered
        self.assertInBody("Section 1 Question 6")
        self.post({"s1-b6-q1-a1": 1})

        # Redirects to the hub
        self.assertInUrl(SUBMIT_URL_PATH)

        # Question 2, 4 and 6 are now visible because block 2 is complete (dependencies updated)

        self.assertInSelector("Section 1 Question 2", self.row_selector(2))
        self.assertInSelector("1", self.row_selector(2))
        self.assertInSelector("Change", self.row_selector(2))

        self.assertInSelector("Section 1 Question 4", self.row_selector(4))
        self.assertInSelector("1", self.row_selector(4))
        self.assertInSelector("Change", self.row_selector(4))

        self.assertInSelector("Section 1 Question 6", self.row_selector(6))
        self.assertInSelector("1", self.row_selector(6))
        self.assertInSelector("Change", self.row_selector(6))

    def test_block_value_source_dependencies_removed_from_path(self):
        """
        Test that the block value source dependencies are updated when a dependent block progress changes and gets removed from path
        """

        self.launchSurvey("test_progress_value_source_blocks")

        self.assertInBody("Section 1 Question 1")
        self.post({"s1-b1-q1-a1": 1})

        self.assertInBody("Section 1 Question 2")
        self.post({"s1-b2-q1-a1": 1})

        self.assertInBody("Section 1 Question 3")
        self.post({"s1-b3-q1-a1": 1})

        self.assertInBody("Section 1 Question 4")
        self.post({"s1-b4-q1-a1": 1})

        self.assertInBody("Section 1 Question 5")
        self.post({"s1-b5-q1-a1": 1})

        self.assertInBody("Section 1 Question 6")
        self.post({"s1-b6-q1-a1": 1})

        self.assertInBody("Section 1 Question 7")
        self.post({"s1-b7-q1-a1": 1})

        self.assertInBody("Check your answers and submit")

        # Change block 1 answer to 0
        self.get(
            "/questionnaire/s1-b1/?return_to=final-summary&return_to_answer_id=s1-b1-q1-a1#s1-b1-q1-a1"
        )
        self.assertInBody("Section 1 Question 1")
        self.post({"s1-b1-q1-a1": 0})

        # Redirects to the hub
        self.assertInUrl(SUBMIT_URL_PATH)

        # Questions 2, 4 and 6 are not visible because they aren't on the path anymore although they've been answered earlier
        self.assertNotInBody("Section 1 Question 2")
        self.assertNotInBody("Section 1 Question 4")
        self.assertNotInBody("Section 1 Question 6")

    def test_block_value_source_cross_section_dependencies_removed_from_path(self):
        """
        Test that the block value source dependencies are updated when a dependent block progress changes and gets removed from path
        """

        self.launchSurvey("test_progress_value_source_blocks_cross_section")

        self.post()

        self.assertInBody("Section 1 Question 1")
        self.post({"s1-b1-q1-a1": 1})

        self.assertInBody("Section 1 Question 2")
        self.post({"s1-b2-q1-a1": 1})

        self.assertInBody("Section 1 Question 3")
        self.post({"s1-b3-q1-a1": 1})

        self.assertInBody("Section 1 Question 4")
        self.post({"s1-b4-q1-a1": 1})

        self.post()
        self.post()

        self.assertInBody("Section 2 Question 5")
        self.post({"s2-b5-q1-a1": 1})

        self.assertInBody("Section 2 Question 6")
        self.post({"s2-b6-q1-a1": 1})

        self.assertInBody("Section 2 Question 7")
        self.post({"s2-b7-q1-a1": 1})

        self.post()
        self.assertEqualUrl("/questionnaire/")

        # Change block 1 answer to 0
        self.get("/questionnaire/s1-b1/")
        self.assertInBody("Section 1 Question 1")
        self.post({"s1-b1-q1-a1": 0})

        # Questions 2, 4 in Section 1 are not visible because they aren't on the path anymore
        self.assertEqualUrl("/questionnaire/sections/section-1/")
        self.assertNotInBody("Section 1 Question 2")
        self.assertNotInBody("Section 1 Question 4")
        self.post()

        # Redirects to the hub
        self.assertEqualUrl("/questionnaire/")

        # Question 6 in Section 2 is not visible because it is not on the path anymore
        self.go_to_section("section-2")
        self.assertEqualUrl("/questionnaire/sections/section-2/")
        self.assertNotInBody("Section 2 Question 6")
