from datetime import date

from ..integration_test_case import IntegrationTestCase

# pylint: disable=too-many-public-methods


class TestQuestionnaireListCollectorRepeatingBlocks(IntegrationTestCase):
    def launch_repeating_blocks_test_survey(self):
        self.launchSurvey("test_list_collector_repeating_blocks_section_summary")
        self.post({"responsible-party-answer": "Yes"})

    def add_company(self, company_name: str):
        self.assertInUrl("/companies/add-company/")
        self.post({"company-or-branch-name": company_name})

    def add_company_from_list_collector(
        self, company_name: str, is_driving: bool = False
    ):
        if is_driving:
            self.assertInUrl("/questionnaire/any-companies-or-branches/")
            self.post({"any-companies-or-branches-answer": "Yes"})
        else:
            self.assertInUrl("/questionnaire/any-other-companies-or-branches/")
            self.post({"any-other-companies-or-branches-answer": "Yes"})
        self.add_company(company_name)

    def post_repeating_block_1(self, registration_number: int, registration_date: date):
        self.assertInUrl("/companies/")
        self.assertInUrl("/companies-repeating-block-1/")
        self.post(
            {
                "registration-number": registration_number,
                "registration-date-day": registration_date.day,
                "registration-date-month": registration_date.month,
                "registration-date-year": registration_date.year,
            }
        )

    def post_repeating_block_2(self, trader_uk: str, trader_eu: str | None = None):
        self.assertInUrl("/companies/")
        self.assertInUrl("/companies-repeating-block-2/")
        self.post(
            {
                "authorised-trader-uk-radio": trader_uk,
                "authorised-trader-eu-radio": trader_eu,
            }
        )

    def add_company_and_repeating_blocks(
        self,
        company_name: str,
        registration_number: int,
        registration_date: date,
        trader_uk: str,
        trader_eu: str | None = None,
        is_driving: bool = False,
    ):
        self.add_company_from_list_collector(
            company_name=company_name, is_driving=is_driving
        )
        self.post_repeating_block_1(
            registration_number=registration_number, registration_date=registration_date
        )
        self.post_repeating_block_2(trader_uk=trader_uk, trader_eu=trader_eu)

    def assert_company_completed(self, company_number: int, label_number: int):
        selector = f"[data-qa='list-item-{label_number}-label']"
        self.assertInSelector(f"Company{company_number}", selector)
        self.assertInSelector("ons-summary__item-title-icon--check", selector)

    def assert_company_incomplete(self, company_number: int, label_number: int):
        selector = f"[data-qa='list-item-{label_number}-label']"
        self.assertInSelector(f"Company{company_number}", selector)
        self.assertNotInSelector("ons-summary__item-title-icon--check", selector)

    def assert_list_item_answers_in_summary(self):
        self.assertInSelector("Company1", "[class='ons-summary__item']")

    def get_list_item_link(self, action, position):
        selector = f"[data-qa='list-item-{action}-{position}-link']"
        selected = self.getHtmlSoup().select(selector)
        return selected[0].get("href")

    def get_link(self, selector: str):
        return self.getHtmlSoup().select(selector)[0]["href"]

    def get_list_item_ids(self):
        result = self.getHtmlSoup().select("[data-list-item-id]")
        return [list_item["data-list-item-id"] for list_item in result]

    def click_edit_link(self, answer_id: str, position: int):
        list_item_ids = self.get_list_item_ids()
        selector = f"[data-qa='{answer_id}-{list_item_ids[position]}-edit']"
        selected = self.getHtmlSoup().select(selector)
        edit_link = selected[0]["href"]
        self.get(edit_link)

    def click_add_link(self):
        add_link = self.get_link("[data-qa='add-item-link']")
        self.get(add_link)

    def click_cancel_link(self):
        cancel_link = self.get_link("[id='cancel-and-return']")
        self.get(cancel_link)

    def add_three_companies(self):
        # Add first company
        self.add_company_and_repeating_blocks(
            company_name="Company1",
            registration_number=123,
            registration_date=date(2023, 1, 1),
            trader_uk="Yes",
            trader_eu="Yes",
            is_driving=True,
        )

        # Add second company
        self.add_company_and_repeating_blocks(
            company_name="Company2",
            registration_number=456,
            registration_date=date(2023, 2, 2),
            trader_uk="Yes",
        )

        # Add third company
        self.add_company_and_repeating_blocks(
            company_name="Company3",
            registration_number=789,
            registration_date=date(2023, 3, 3),
            trader_uk="No",
            trader_eu="Yes",
        )

        self.assert_company_completed(1, 1)
        self.assert_company_completed(2, 2)
        self.assert_company_completed(3, 3)

    def test_invalid_invalid_list_item_id(self):
        self.launch_repeating_blocks_test_survey()
        self.get(
            "/questionnaire/companies/non-existing-list-item-id/companies-repeating-block-1/"
        )
        self.assertStatusNotFound()

    def test_happy_path(self):
        self.launch_repeating_blocks_test_survey()

        # Add some items to the list
        self.add_three_companies()

        # Remove item 2
        remove_link = self.get_list_item_link("remove", 2)
        self.get(remove_link)
        self.assertInBody("Are you sure you want to remove this company or UK branch?")

        # Cancel
        self.post({"remove-confirmation": "No"})
        self.assertEqualUrl("/questionnaire/any-other-companies-or-branches/")

        # Remove again
        self.get(remove_link)
        self.post({"remove-confirmation": "Yes"})

        # Check list item 3 has moved to second position
        self.assert_company_completed(3, 2)

        # Test the previous link
        edit_link_1 = self.get_list_item_link("change", 1)
        remove_link_1 = self.get_list_item_link("remove", 1)

        self.get(edit_link_1)
        self.assertInUrl("/edit-company/")
        self.previous()
        self.assertEqualUrl("/questionnaire/any-other-companies-or-branches/")

        self.get(remove_link_1)
        self.assertInUrl("/remove-company/")
        self.previous()
        self.assertEqualUrl("/questionnaire/any-other-companies-or-branches/")

        # Submit survey
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post({"any-other-trading-details-answer": "No other details"})
        self.post()
        self.post()
        self.assertInBody(
            "Thank you for completing the Test a List Collector with Repeating Blocks and Section Summary Items"
        )

    def test_incomplete_repeating_blocks(self):
        self.launch_repeating_blocks_test_survey()

        # Add first company - only add block and first repeating block
        self.add_company_from_list_collector(company_name="Company1", is_driving=True)
        self.post_repeating_block_1(
            registration_number=123, registration_date=date(2023, 1, 1)
        )
        self.previous()  # return to previous repeating block
        self.previous()  # return to edit block
        self.previous()  # return to list collector

        # Add second company - complete
        self.add_company_and_repeating_blocks(
            company_name="Company2",
            registration_number=456,
            registration_date=date(2023, 2, 2),
            trader_uk="Yes",
        )

        # Add third company - only the add block
        self.add_company_from_list_collector(company_name="Company3")
        self.click_cancel_link()  # Return to edit block
        self.click_cancel_link()  # Return to the list collector

        # Add fourth company - complete
        self.add_company_and_repeating_blocks(
            company_name="Company4",
            registration_number=101,
            registration_date=date(2023, 4, 4),
            trader_uk="No",
        )

        # Assert completeness
        self.assert_company_incomplete(1, 1)
        self.assert_company_completed(2, 2)
        self.assert_company_incomplete(3, 3)
        self.assert_company_completed(4, 4)

        # Attempt to move along path after list collector - will route to first incomplete block of first incomplete item
        self.post({"any-other-companies-or-branches-answer": "No"})

        # Should be routed to incomplete block 2 of item 1
        self.post_repeating_block_2(trader_uk="Yes", trader_eu="Yes")
        self.assert_company_completed(1, 1)
        self.post({"any-other-companies-or-branches-answer": "No"})

        # Should be routed to incomplete block 1 of item 3
        self.post_repeating_block_1(
            registration_number=789, registration_date=date(2023, 3, 3)
        )
        self.post_repeating_block_2(trader_uk="Yes", trader_eu="No")
        self.assert_company_completed(3, 3)

        # Can now submit the survey as all items are complete
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post({"any-other-trading-details-answer": "No other details"})
        self.post()
        self.post()
        self.assertInBody(
            "Thank you for completing the Test a List Collector with Repeating Blocks and Section Summary Items"
        )

    def test_adding_from_the_summary_page_adds_the_return_to_param_to_the_url(
        self,
    ):
        self.launch_repeating_blocks_test_survey()

        # Add first company
        self.add_company_and_repeating_blocks(
            company_name="Company1",
            registration_number=123,
            registration_date=date(2023, 1, 1),
            trader_uk="Yes",
            trader_eu="Yes",
            is_driving=True,
        )

        # Assert list items complete
        self.assert_company_completed(1, 1)

        # Navigate to section summary
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post({"any-other-trading-details-answer": "No other details"})
        self.assertInUrl("/sections/section-companies/")

        # Add second company - from section summary
        self.click_add_link()
        self.assertInUrl("?return_to=section-summary")
        self.add_company(company_name="Company2")
        self.post_repeating_block_1(
            registration_number=456, registration_date=date(2023, 2, 2)
        )
        self.post_repeating_block_2(trader_uk="Yes", trader_eu="No")
        self.assert_company_completed(2, 2)

        # Navigate to the submit page summary
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post()
        self.assertInUrl("/submit/")
        self.click_add_link()
        self.assertInUrl("?return_to=section-summary")

        # Add third company - from submit summary
        self.add_company(company_name="Company3")
        self.post_repeating_block_1(
            registration_number=789, registration_date=date(2023, 3, 3)
        )
        self.post_repeating_block_2(trader_uk="No")
        self.assert_company_completed(3, 3)

        # Submit
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post({"any-other-trading-details-answer": "No other details"})
        self.post()
        self.post()
        self.assertInBody(
            "Thank you for completing the Test a List Collector with Repeating Blocks and Section Summary Items"
        )

    def test_removing_from_the_summary_page_adds_the_return_to_param_to_the_url(
        self,
    ):
        self.launch_repeating_blocks_test_survey()

        # Add some items to the list
        self.add_three_companies()

        # Navigate to section summary
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post({"any-other-trading-details-answer": "No other details"})

        # Remove item 3
        remove_link = self.get_list_item_link("remove", 3)
        self.get(remove_link)
        self.assertInUrl("?return_to=section-summary")
        self.assertInBody("Are you sure you want to remove this company or UK branch?")
        self.post({"remove-confirmation": "Yes"})

        # Navigate to submit summary
        self.assertInUrl("/sections/section-companies/")
        self.post()

        # Remove item 2
        remove_link = self.get_list_item_link("remove", 2)
        self.get(remove_link)
        self.assertInUrl("?return_to=section-summary")
        self.assertInBody("Are you sure you want to remove this company or UK branch?")
        self.post({"remove-confirmation": "Yes"})

        # Submit
        self.post()
        self.post()
        self.assertInBody(
            "Thank you for completing the Test a List Collector with Repeating Blocks and Section Summary Items"
        )

    def test_edit_repeating_block_from_the_summary_page_adds_the_return_to_param_to_the_url(
        self,
    ):
        self.launch_repeating_blocks_test_survey()

        # Add some items to the list
        self.add_three_companies()

        # Navigate to section summary
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post({"any-other-trading-details-answer": "No other details"})
        self.assertInUrl("/sections/section-companies/")

        # Edit item 3
        self.click_edit_link("registration-number", 2)
        self.assertInUrl("?return_to=section-summary")
        self.post_repeating_block_1(
            registration_number=000, registration_date=date(2023, 5, 5)
        )
        self.assertInUrl("/sections/section-companies/")

        # Remove item 2
        self.click_edit_link("authorised-trader-uk-radio", 2)
        self.assertInUrl("?return_to=section-summary")
        self.post_repeating_block_2(trader_uk="No", trader_eu="No")
        self.assertInUrl("/sections/section-companies/")

        # Submit
        self.post()
        self.post()
        self.assertInBody(
            "Thank you for completing the Test a List Collector with Repeating Blocks and Section Summary Items"
        )

    def test_edit_incomplete_repeating_block_from_summary_page_routes_to_next_repeating_block(
        self,
    ):
        self.launch_repeating_blocks_test_survey()

        # add incomplete item with answers for first repeating block
        self.add_company_from_list_collector(company_name="Company4", is_driving=True)
        self.post_repeating_block_1(
            registration_number=123, registration_date=date(2023, 1, 1)
        )

        # go back to edit block and change the name
        self.click_cancel_link()
        self.click_cancel_link()
        self.assertInUrl("/edit-company/")
        self.post({"company-or-branch-name": "Company5"})

        # should jump straight to repeating block 2 as this is the first incomplete one
        self.assertInUrl("/companies-repeating-block-2/")

    def test_adding_incomplete_list_item_from_summary_returns_to_list_collector_not_summary(
        self,
    ):
        self.launch_repeating_blocks_test_survey()

        # Add some items to the list
        self.add_three_companies()

        # Navigate to section summary
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post({"any-other-trading-details-answer": "No other details"})
        self.assertInUrl("/sections/section-companies/")

        # Add incomplete item from section summary add link
        self.click_add_link()
        self.add_company(company_name="Company4")
        self.click_cancel_link()  # cancel and go back to edit block
        self.click_cancel_link()  # cancel and go back to list collector
        self.assertInUrl("/any-other-companies-or-branches/")
        self.assert_company_incomplete(4, 4)

        # Complete the incomplete item
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post_repeating_block_1(
            registration_number=101, registration_date=date(2023, 4, 4)
        )
        self.post_repeating_block_2(trader_uk="Yes", trader_eu="Yes")
        self.assert_company_completed(4, 4)

        # Navigate to submit summary
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post()

        # Add incomplete item from submit summary add link
        self.click_add_link()
        self.add_company(company_name="Company5")
        self.click_cancel_link()
        self.click_cancel_link()
        self.assertInUrl("/any-other-companies-or-branches/")
        self.assert_company_incomplete(5, 5)

        # Complete the incomplete item
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post_repeating_block_1(
            registration_number=121, registration_date=date(2023, 5, 5)
        )
        self.post_repeating_block_2(trader_uk="No", trader_eu="No")
        self.assert_company_completed(5, 5)

        # Submit
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post()
        self.post()
        self.assertInBody(
            "Thank you for completing the Test a List Collector with Repeating Blocks and Section Summary Items"
        )
