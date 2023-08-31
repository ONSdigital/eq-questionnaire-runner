from tests.integration.questionnaire import QuestionnaireTestCase


class TestQuestionnaireCalculatedSummary(QuestionnaireTestCase):
    BASE_URL = "/questionnaire/"

    def _add_list_items(self):
        self.post()
        self.post({"you-live-here": "Yes"})
        self.add_person("Marie Claire", "Doe")
        self.post({"anyone-else": "Yes"})
        self.add_person("John", "Doe")
        self.post({"anyone-else": "No"})
        self.post()

    def _complete_calculated_summary_path_with_skip(self):
        self.post({"first-number-answer": "10"})
        self.post(
            {
                "second-number-answer": "20",
                "second-number-answer-unit-total": "20",
                "second-number-answer-also-in-total": "20",
            }
        )
        self.post({"third-number-answer": "30"})
        self.post({"third-and-a-half-number-answer-unit-total": "30"})
        self.post({"skip-fourth-block-answer": "Yes"})
        self.post({"fifth-percent-answer": "50", "fifth-number-answer": "50"})
        self.post({"sixth-percent-answer": "60", "sixth-number-answer": "60"})

    def _complete_calculated_summary_path_no_skip(self):
        self.post({"first-number-answer": "10"})
        self.post(
            {
                "second-number-answer": "20",
                "second-number-answer-unit-total": "20",
                "second-number-answer-also-in-total": "20",
            }
        )
        self.post({"third-number-answer": "30"})
        self.post({"third-and-a-half-number-answer-unit-total": "30"})
        self.post({"skip-fourth-block-answer": "No"})
        self.post({"fourth-number-answer": "50"})
        self.post({"fourth-and-a-half-number-answer-also-in-total": "50"})
        self.post({"fifth-percent-answer": "50", "fifth-number-answer": "50"})
        self.post({"sixth-percent-answer": "60", "sixth-number-answer": "60"})

    def test_calculated_summary(self):
        self.launchSurvey("test_calculated_summary")
        self._complete_calculated_summary_path_with_skip()
        self.assertInBody(
            "We calculate the total of currency values entered to be £80.00"
        )

    def test_calculated_summary_no_skip(self):
        self.launchSurvey("test_calculated_summary")
        self._complete_calculated_summary_path_no_skip()
        self.assertInBody(
            "We calculate the total of currency values entered to be £180.00"
        )

    def test_new_calculated_summary(self):
        self.launchSurvey("test_new_calculated_summary")
        self._complete_calculated_summary_path_with_skip()
        self.assertInBody(
            "We calculate the total of currency values entered to be £80.00"
        )

    def test_calculated_summary_total_playback(self):
        self.launchSurvey("test_new_calculated_summary")
        self._complete_calculated_summary_path_with_skip()
        self.post()
        self.post()
        self.post()
        self.post()
        self.assertInBody("Total currency values: <em>£80.00</em>")

    def test_new_calculated_summary_no_skip(self):
        self.launchSurvey("test_new_calculated_summary")
        self._complete_calculated_summary_path_no_skip()
        self.assertInBody(
            "We calculate the total of currency values entered to be £180.00"
        )

    def test_new_calculated_summary_repeating_section(self):
        self.launchSurvey("test_new_calculated_summary_repeating_section")
        self._add_list_items()
        self.post()

        self._complete_calculated_summary_path_with_skip()
        self.assertInBody(
            "We calculate the total of currency values entered to be £80.00"
        )

    def test_new_calculated_summary_no_skip_repeating_section(self):
        self.launchSurvey("test_new_calculated_summary_repeating_section")
        self._add_list_items()
        self.post()

        self._complete_calculated_summary_path_no_skip()
        self.assertInBody(
            "We calculate the total of currency values entered to be £180.00"
        )

    def test_calculated_summary_value_sources_across_sections(self):
        self.launchSurvey("test_calculated_summary_cross_section_dependencies")

        # Complete the first section
        self.post()
        self.post({"skip-first-block-answer": "No"})
        self.post({"first-number-answer": "10"})
        self.post({"first-and-a-half-number-answer-also-in-total": "20"})
        self.post({"second-number-answer-also-in-total": "30"})
        self.assertInBody(
            "We calculate the total of currency values entered to be £60.00"
        )
        self.post()
        self.post()
        self.post()

        # Complete the second section
        self.post(
            {
                "third-number-answer": "20",
                "third-number-answer-also-in-total": "20",
            }
        )
        self.assertInBody(
            "We calculate the total of currency values entered to be £40.00"
        )

        # Check calculated summary value sources are displayed correctly for both the current and previous
        # sections
        self.post()
        self.assertInBody("60 - calculated summary answer (previous section)")
        self.assertInBody("40 - calculated summary answer (current section)")
        self.post()

        self.assertInBody(
            "Set minimum and maximum values based on your calculated summary total of £60"
        )
        self.post(
            {
                "set-minimum-answer": "40",
                "set-maximum-answer": "70",
            }
        )
        self.assertInBody("Enter an answer more than or equal to £60.00")

    def test_calculated_summary_value_sources_across_sections_repeating(self):
        self.launchSurvey(
            "test_new_calculated_summary_cross_section_dependencies_repeating"
        )

        # Add  household members
        self._add_list_items()

        # Complete the first section
        self.post({"skip-first-block-answer": "No"})
        self.post({"first-number-answer": "10"})
        self.post({"first-and-a-half-number-answer-also-in-total": "20"})
        self.post({"second-number-answer-also-in-total": "30"})
        self.assertInBody(
            "We calculate the total of currency values entered to be £60.00"
        )
        self.post()
        self.post()
        self.post()

        # Complete the second section
        self.post(
            {
                "third-number-answer": "20",
                "third-number-answer-also-in-total": "20",
            }
        )
        self.assertInBody(
            "We calculate the total of currency values entered to be £40.00"
        )

        # Check calculated summary value sources are displayed correctly for both the current and previous
        # sections
        self.post()
        self.assertInBody("60 - calculated summary answer (previous section)")
        self.assertInBody("40 - calculated summary answer (current section)")
        self.post()

        self.assertInBody(
            "Set minimum and maximum values based on your calculated summary total of £60"
        )
        self.post(
            {
                "set-minimum-answer": "40",
                "set-maximum-answer": "70",
            }
        )
        self.assertInBody("Enter an answer more than or equal to £60.00")

    def test_calculated_summary_repeating_answers_only(self):
        """
        Tests a calculated summary with a dynamic answer source resolving to a list of repeating answers
        """
        self.launchSurvey("test_new_calculated_summary_repeating_answers_only")

        self.post({"any-transport-answer": "Yes"})
        self.post({"transport-name": "Bus"})
        self.post({"list-collector-answer": "Yes"})
        self.post({"transport-name": "Tube"})

        # get the ids before finishing the collector
        list_item_ids = self.get_list_item_ids()
        assert len(list_item_ids) == 2
        self.post({"list-collector-answer": "No"})

        self.post(
            {
                f"cost-of-transport-{list_item_ids[0]}": "100",
                f"cost-of-transport-{list_item_ids[1]}": "200",
            }
        )
        self.assertInBody(
            "We calculate the total monthly spending on public transport to be £300.00. Is this correct?"
        )

    def test_new_calculated_summary_repeating_blocks(self):
        """
        Tests a calculated summary with a repeating block answer id source resolving to a list of answers
        """
        self.launchSurvey("test_new_calculated_summary_repeating_blocks")
        self.post({"answer-car": "100"})
        self.post({"answer-skip": "No"})
        self.post({"list-collector-answer": "Yes"})
        self.post({"transport-name": "Bus"})
        self.post(
            {
                "transport-company": "First",
                "transport-cost": "30",
                "transport-additional-cost": "5",
            }
        )
        self.post({"transport-count": "10"})
        self.post({"list-collector-answer": "Yes"})
        self.post({"transport-name": "Plane"})
        self.post(
            {
                "transport-company": "EasyJet",
                "transport-cost": "0",
                "transport-additional-cost": "265",
            }
        )
        self.post({"transport-count": "2"})
        list_item_ids = self.get_list_item_ids()
        self.post({"list-collector-answer": "No"})
        self.assertInBody(
            "We calculate the total monthly expenditure on transport to be £400.00. Is this correct?"
        )
        self.post()
        self.assertInBody(
            "We calculate the total journeys made per month to be 12. Is this correct?"
        )

        # check that using a change link and editing an answer takes you straight back to the relevant calculated summary
        change_link = self.get_list_item_change_link(
            "transport-count", list_item_ids[1]
        )
        self.get(change_link)
        self.post({"transport-count": "4"})
        self.assertInUrl("/calculated-summary-count/")
        self.assertInBody(
            "We calculate the total journeys made per month to be 14. Is this correct?"
        )
        self.previous()

        # likewise for the other calculated summary
        change_link = self.get_list_item_change_link("transport-cost", list_item_ids[0])
        self.get(change_link)
        self.post(
            {
                "transport-company": "First",
                "transport-cost": "300",
                "transport-additional-cost": "50",
            }
        )
        self.assertInUrl("/calculated-summary-spending/")
        self.assertInBody(
            "We calculate the total monthly expenditure on transport to be £715.00. Is this correct?"
        )

        # check that removing the list collector from the path updates the calculated summary correctly
        self.previous()
        self.previous()
        self.post({"answer-skip": "Yes"})

        # calculated summary count should now not be on the path
        self.assertInUrl("/calculated-summary-spending/")
        self.assertInBody(
            "We calculate the total monthly expenditure on transport to be £100.00. Is this correct?"
        )
        # no list items should be there
        self.assertNotInBody("Give details of your expenditure travelling by")
        self.post()
        # should be absent from section summary too
        self.assertInUrl("/sections/section-1")
        self.assertNotInBody("Name of transport")

    def test_calculated_summary_default_decimal_places(self):
        # When multiple decimal limits are set in the schema but no decimals
        # are entered then we should default to two decimal places on the calculated summary page
        # and the playback page
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
        self.assertInBody(
            "We calculate the total of currency values entered to be £120.00"
        )
        self.post()
        self.assertInBody("Total currency values: <em>£120.00</em>")

    def test_calculated_summary_with_varying_decimal_places(self):
        # When multiple decimal limits are set in the schema and a mixture of decimal
        # places are entered then we should use the largest number of decimal places that are below the decimal limit
        # on the calculated summary page and the playback page
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
        self.assertInBody(
            "We calculate the total of currency values entered to be £120.58985"
        )
        self.post()
        self.assertInBody("Total currency values: <em>£120.58985</em>")
