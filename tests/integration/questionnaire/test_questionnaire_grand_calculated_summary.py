from . import QuestionnaireTestCase


class TestQuestionnaireGrandCalculatedSummary(QuestionnaireTestCase):
    BASE_URL = "/questionnaire/"

    def test_grand_calculated_summary(self):
        self.launchSurvey("test_grand_calculated_summary")
        # section-1 two types of unit questions
        self.post({"q1-a1": 20, "q1-a2": 5})
        self.post({"q2-a1": 100, "q2-a2": 3})
        # confirm the two calculated summaries
        self.post()
        self.post()
        # section-2 two more of each question type
        self.post({"q3-a1": 40, "q3-a2": 2})
        self.post({"q4-a1": 10, "q4-a2": 3})
        # confirm the two calculated summaries
        self.post()
        self.post()
        # check the two grand calculated summaries
        self.assertInBody(
            "We calculate the grand total weekly distance travelled to be 170 mi. Is this correct?"
        )
        self.post()
        self.assertInBody(
            "We calculate the grand total journeys per week to be 13. Is this correct?"
        )

    def test_grand_calculated_summary_multiple_sections(self):
        self.launchSurvey("test_grand_calculated_summary_multiple_sections")
        # open section 1 and complete two questions with calculated summary confirmation
        self.post()
        self.post({"q1-a1": 10, "q1-a2": 20})
        self.post({"q2-a1": 30, "q2-a2": 40})
        self.post()
        self.post({"q3-a1": 50, "q3-a2": 60})
        self.post()
        # confirm calculated and grand calculated summary
        self.assertInBody(
            "Calculated summary for section 1 is calculated to be £210.00. Is this correct?"
        )
        self.post()
        self.assertInBody(
            "Grand Calculated Summary which should match the previous calculated summary is calculated to be £210.00. Is this correct?"
        )
        self.post()
        # section summary then start section 2
        self.post()
        self.post()
        # another question with grand calculated summary and section summary
        self.post({"q4-a1": 100, "q4-a2": 200})
        self.post()
        self.post()
        # grand calculated summary section
        self.post()
        self.assertInBody(
            "Grand Calculated Summary for section 1 and 2 is calculated to be £510.00. Is this correct?"
        )

    def _complete_upto_grand_calculated_summary_cross_section_dependencies(self):
        """
        Completes first two sections of the schema testing grand calculated summaries
        depending on calculated summaries in other sections
        """
        # Complete the first section
        self.post()
        self.post({"skip-answer-1": "Yes"})
        self.post({"second-number-answer-a": "30", "second-number-answer-b": "60"})
        self.assertInBody(
            "We calculate the total of currency values entered to be £90.00. Is this correct?"
        )
        self.post()
        self.post()

        # Complete the second section
        self.post()
        self.post(
            {"third-number-answer-part-a": "30", "third-number-answer-part-b": "40"}
        )

    def test_grand_calculated_summary_cross_section_dependencies_with_skip(self):
        self.launchSurvey("test_grand_calculated_summary_cross_section_dependencies")
        self._complete_upto_grand_calculated_summary_cross_section_dependencies()

        # skip the calculated summary and go straight to section summary
        self.post({"skip-answer-2": "Yes"})
        self.post()

        # grand calculated summary which doesn't include skipped calculated summary
        self.post()
        self.assertInBody(
            "The grand calculated summary is calculated to be £90.00. Is this correct?"
        )

    def test_grand_calculated_summary_cross_section_dependencies_no_skip(self):
        self.launchSurvey("test_grand_calculated_summary_cross_section_dependencies")
        self._complete_upto_grand_calculated_summary_cross_section_dependencies()

        # don't skip calculated summary, confirm it, and go to section summary
        self.post({"skip-answer-2": "No"})
        self.post()
        self.post()

        # grand calculated summary will now include the previous calculated summary
        self.post()
        self.assertInBody(
            "The grand calculated summary is calculated to be £160.00. Is this correct?"
        )
