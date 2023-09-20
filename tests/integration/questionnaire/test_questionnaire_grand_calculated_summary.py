from . import QuestionnaireTestCase


class TestQuestionnaireGrandCalculatedSummary(QuestionnaireTestCase):
    BASE_URL = "/questionnaire/"

    def test_grand_calculated_summary(self):
        self.launchSurvey("test_grand_calculated_summary")
        # section-1 two types of unit questions
        self.post({"q1-a1": 20, "q1-a2": 5})
        self.post({"q2-a1": 100, "q2-a2": 3})
        self.post()
        self.post()
        # section-2 two more of each question type
        self.post({"q3-a1": 40, "q3-a2": 2})
        self.post({"q4-a1": 10, "q4-a2": 3})
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
        """
        Use the repeating answers schema to test the grand calculated summary which uses calculated summaries in multiple different sections
        """
        self.launchSurvey("test_grand_calculated_summary_repeating_answers")
        # section 1
        self.post()
        self.post({"q1-a1": 10, "q1-a2": 20})
        self.post({"q2-a1": 30, "q2-a2": 40})
        self.post()
        self.post({"q3-a1": 50, "q3-a2": 60})
        self.post()
        # confirm calculated and grand calculated summary
        self.assertInBody(
            "Calculated summary for food and clothing is calculated to be £210.00. Is this correct?"
        )
        self.post()
        self.assertInBody(
            "Grand Calculated Summary which should match the previous calculated summary is calculated to be £210.00. Is this correct?"
        )
        self.post()
        self.post()
        # section 2
        self.post()
        self.post({"q4-a1": 100, "q4-a2": 200})
        self.post()
        # grand calculated summary section with calculated summaries from multiple sections
        self.post()
        self.assertInBody(
            "Grand Calculated Summary for shopping and entertainment is calculated to be £510.00. Is this correct?"
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
            "We calculate your total monthly expenditure on household bills to be £90.00. Is this correct?"
        )
        self.post()
        self.post()
        # Complete the second section
        self.post()
        self.post({"third-number-answer-part-a": "70"})

    def test_grand_calculated_summary_cross_section_dependencies_with_skip(self):
        self.launchSurvey("test_grand_calculated_summary_cross_section_dependencies")
        self._complete_upto_grand_calculated_summary_cross_section_dependencies()

        # skip the calculated summary
        self.post({"skip-answer-2": "Yes"})
        self.post({"tv-choice-answer": "Television"})
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
        self.post({"tv-choice-answer": "Television"})
        self.post()

        # grand calculated summary will now include the previous calculated summary
        self.post()
        self.assertInBody(
            "The grand calculated summary is calculated to be £160.00. Is this correct?"
        )

    def test_grand_calculated_summary_cross_section_dependencies_extra_question(self):
        self.launchSurvey("test_grand_calculated_summary_cross_section_dependencies")
        self._complete_upto_grand_calculated_summary_cross_section_dependencies()

        # edit question to unlock the extra one
        self.previous()
        self.post(
            {"third-number-answer-part-a": "70", "third-number-answer-part-b": "20"}
        )
        self.post({"fourth-number-answer": "40"})
        self.post({"skip-answer-2": "No"})
        self.post()
        self.post({"tv-choice-answer": "Television"})
        self.post()

        # grand calculated summary will now include the extra question answer
        self.post()
        self.assertInBody(
            "The grand calculated summary is calculated to be £220.00. Is this correct?"
        )

    def _complete_upto_grand_calculated_summary_overlapping_answers(
        self, radio_answer: str
    ):
        self.post()
        self.post()
        self.post({"q1-a1": "100", "q1-a2": "200"})
        self.post({"q2-a1": "10", "q2-a2": "20"})
        self.post()
        self.post()
        self.post({"radio-extra": radio_answer})
        if radio_answer != "No":
            # in the no overlap case, the calculated summary is skipped entirely
            self.post()
        self.post()
        self.post()

    def test_grand_calculated_summary_overlapping_answers_full_overlap(self):
        self.launchSurvey("test_grand_calculated_summary_overlapping_answers")
        self._complete_upto_grand_calculated_summary_overlapping_answers(
            "Yes, I am going to buy two of everything"
        )
        self.assertInBody(
            "Grand Calculated Summary of purchases this week comes to £660.00. Is this correct?"
        )

    def test_grand_calculated_summary_overlapping_answers_partial_overlap(self):
        self.launchSurvey("test_grand_calculated_summary_overlapping_answers")
        self._complete_upto_grand_calculated_summary_overlapping_answers(
            "Yes, extra bread and cheese"
        )
        self.assertInBody(
            "Grand Calculated Summary of purchases this week comes to £360.00. Is this correct?"
        )

    def test_grand_calculated_summary_overlapping_answers_no_overlap(self):
        self.launchSurvey("test_grand_calculated_summary_overlapping_answers")
        self._complete_upto_grand_calculated_summary_overlapping_answers("No")
        self.assertInBody(
            "Grand Calculated Summary of purchases this week comes to £330.00. Is this correct?"
        )

    def test_grand_calculated_summary_default_decimal_places(self):
        """
        When multiple decimal limits are set in the schema but no decimals
        are entered then we should default to two decimal places on the grand calculated summary page
        """
        self.launchSurvey("test_calculated_and_grand_calculated_summary_decimals")
        self.post({"first-number-answer": "10"})
        self.post(
            {
                "second-number-answer": "20",
                "second-number-answer-also-in-total": "20",
            }
        )
        self.post({"third-number-answer": "30"})
        self.post({"fourth-number-answer": "40"})
        self.post()
        self.post()
        self.post({"fifth-number-answer": "50"})
        self.post({"sixth-number-answer": "60"})
        self.assertInBody(
            "We calculate the total of currency values entered to be £110.00. Is this correct?"
        )

    def test_grand_calculated_summary_with_varying_decimal_places(self):
        """
        When multiple decimal limits are set in the schema and a mixture of decimal
        places are entered then we should use the largest number of decimal places that are below the decimal limit
        on the grand calculated summary page
        """
        self.launchSurvey("test_calculated_and_grand_calculated_summary_decimals")
        self.post({"first-number-answer": "10.1"})
        self.post(
            {
                "second-number-answer": "20.12",
                "second-number-answer-also-in-total": "20.123",
            }
        )
        self.post({"third-number-answer": "30.1234"})
        self.post({"fourth-number-answer": "40.12345"})
        self.post()
        self.post()
        self.post({"fifth-number-answer": "50"})
        self.post({"sixth-number-answer": "60"})
        self.post()
        self.assertInBody(
            "We calculate the grand total to be £230.58985. Is this correct?"
        )

    def test_grand_calculated_summary_inside_repeating_section(self):
        """
        Happy path for a grand calculated summary inside a repeating section
        """
        self.launchSurvey("test_grand_calculated_summary_inside_repeating_section")
        self.post()
        self.post({"any-cost-answer": "No"})
        self.post({"finance-cost-answer": "150"})
        self.post()
        self.post()
        self.post()
        self.post({"any-vehicle-answer": "Yes"})
        self.post({"vehicle-name": "Car"})
        self.post({"list-collector-answer": "Yes"})
        self.post({"vehicle-name": "Motorbike"})
        self.post({"list-collector-answer": "No"})
        self.post()
        self.post()
        self.post({"vehicle-maintenance-cost": "100"})
        self.post({"vehicle-fuel-cost": "80"})
        self.assertInBody(
            "We calculate the monthly running costs of your Car to be £180.00. Is this correct?"
        )
        self.post()
        self.assertInBody(
            "The total cost of owning and running your Car is calculated to be £330.00. Is this correct?"
        )
        self.post()
        self.post()
        self.post()
        self.post({"vehicle-maintenance-cost": "40"})
        self.post({"vehicle-fuel-cost": "35"})
        self.assertInBody(
            "We calculate the monthly running costs of your Motorbike to be £75.00. Is this correct?"
        )
        self.post()
        self.assertInBody(
            "The total cost of owning and running your Motorbike is calculated to be £225.00. Is this correct?"
        )
