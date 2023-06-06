from datetime import date

from ..integration_test_case import IntegrationTestCase


# pylint: disable=too-many-public-methods


class TestQuestionnaireListCollector(IntegrationTestCase):
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

    def assert_company_completed(self, company_name: str, selector: str):
        self.assertInSelector(company_name, selector)
        self.assertInSelector("ons-summary__item-title-icon--check", selector)

    def assert_company_incomplete(self, company_name: str, selector: str):
        self.assertInSelector(company_name, selector)
        self.assertNotInSelector("ons-summary__item-title-icon--check", selector)

    def assert_list_item_answers_in_summary(self):
        self.assertInSelector("Company1", "[class='ons-summary__item']")

    def get_list_item_link(self, action, position):
        selector = f"[data-qa='list-item-{action}-{position}-link']"
        selected = self.getHtmlSoup().select(selector)
        return selected[0].get("href")

    def get_link(self, selector: str):
        return self.get_links(selector)[0]

    def get_links(self, selector: str):
        selected = self.getHtmlSoup().select(selector)
        return [element["href"] for element in selected]

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

        self.assert_company_completed(
            company_name="Company1", selector="[data-qa='list-item-1-label']"
        )
        self.assert_company_completed(
            company_name="Company2", selector="[data-qa='list-item-2-label']"
        )
        self.assert_company_completed(
            company_name="Company3", selector="[data-qa='list-item-3-label']"
        )

    def test_invalid_invalid_list_item_id(self):
        self.launchSurvey("test_list_collector_repeating_blocks_section_summary")

        self.get(
            "/questionnaire/companies/non-existing-list-item-id/companies-repeating-block-1/"
        )

        self.assertStatusNotFound()

    def test_happy_path(self):
        self.launchSurvey("test_list_collector_repeating_blocks_section_summary")

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

        self.assert_company_completed(
            company_name="Company3", selector="[data-qa='list-item-2-label']"
        )

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
        self.post()
        self.post()
        self.assertInBody(
            "Thank you for completing the Test a List Collector with Repeating Blocks and Section Summary Items"
        )

    def test_incomplete_repeating_blocks(self):
        self.launchSurvey("test_list_collector_repeating_blocks_section_summary")

        # Add first company - only add block and first repeating block

        self.add_company_from_list_collector(company_name="Company1", is_driving=True)
        self.post_repeating_block_1(
            registration_number=123, registration_date=date(2023, 1, 1)
        )
        self.previous()  # Return to the list collector via previous button

        # Add second company - complete

        self.add_company_and_repeating_blocks(
            company_name="Company2",
            registration_number=456,
            registration_date=date(2023, 2, 2),
            trader_uk="Yes",
        )

        # Add third company - only the add block
        self.add_company_from_list_collector(company_name="Company3")
        cancel_link = self.get_link("[id='cancel-and-return']")
        self.get(cancel_link)  # Return to the list collector via cancel button

        # Add fourth company - complete

        self.add_company_and_repeating_blocks(
            company_name="Company4",
            registration_number=101,
            registration_date=date(2023, 4, 4),
            trader_uk="No",
        )

        # Assert completeness

        self.assert_company_incomplete(
            company_name="Company1", selector="[data-qa='list-item-1-label']"
        )
        self.assert_company_completed(
            company_name="Company2", selector="[data-qa='list-item-2-label']"
        )
        self.assert_company_incomplete(
            company_name="Company3", selector="[data-qa='list-item-3-label']"
        )
        self.assert_company_completed(
            company_name="Company4", selector="[data-qa='list-item-4-label']"
        )

        # Attempt to move along path after list collector - will route to first incomplete block of first incomplete item

        self.post({"any-other-companies-or-branches-answer": "No"})

        # Should be routed to incomplete block 2 of item 1
        self.post_repeating_block_2(trader_uk="Yes", trader_eu="Yes")
        self.assert_company_completed(
            company_name="Company1", selector="[data-qa='list-item-1-label']"
        )

        self.post({"any-other-companies-or-branches-answer": "No"})

        # Should be routed to incomplete block 1 of item 3
        self.post_repeating_block_1(
            registration_number=789, registration_date=date(2023, 3, 3)
        )
        self.post_repeating_block_2(trader_uk="Yes", trader_eu="No")
        self.assert_company_completed(
            company_name="Company3", selector="[data-qa='list-item-3-label']"
        )

        # Can now submit the survey as all items are complete
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post()
        self.post()
        self.assertInBody(
            "Thank you for completing the Test a List Collector with Repeating Blocks and Section Summary Items"
        )

    def test_adding_from_the_summary_page_adds_the_return_to_param_to_the_url(
            self,
    ):
        self.launchSurvey("test_list_collector_repeating_blocks_section_summary")

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

        self.assert_company_completed(
            company_name="Company1", selector="[data-qa='list-item-1-label']"
        )

        # Navigate to section summary
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.assertInUrl("/sections/section-companies/")

        # Add second company - from section summary

        add_link = self.get_link("[data-qa='add-item-link']")
        self.get(add_link)
        self.assertInUrl("?return_to=section-summary")
        self.add_company(company_name="Company2")
        self.post_repeating_block_1(
            registration_number=456, registration_date=date(2023, 2, 2)
        )
        self.post_repeating_block_2(trader_uk="Yes", trader_eu="No")

        self.assert_company_completed(
            company_name="Company2", selector="[data-qa='list-item-2-label']"
        )

        # Navigate to the submit page summary
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post()
        self.assertInUrl("/submit/")
        add_link = self.get_link("[data-qa='add-item-link']")
        self.get(add_link)
        self.assertInUrl("?return_to=section-summary")

        # Add third company - from submit summary

        self.add_company(company_name="Company3")
        self.post_repeating_block_1(
            registration_number=789, registration_date=date(2023, 3, 3)
        )
        self.post_repeating_block_2(trader_uk="No")

        self.assert_company_completed(
            company_name="Company3", selector="[data-qa='list-item-3-label']"
        )

        # Submit
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post()
        self.post()
        self.assertInBody(
            "Thank you for completing the Test a List Collector with Repeating Blocks and Section Summary Items"
        )

    def test_removing_from_the_summary_page_adds_the_return_to_param_to_the_url(
            self,
    ):
        self.launchSurvey("test_list_collector_repeating_blocks_section_summary")

        # Add some items to the list
        self.add_three_companies()

        # Navigate to section summary
        self.post({"any-other-companies-or-branches-answer": "No"})

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
        self.launchSurvey("test_list_collector_repeating_blocks_section_summary")

        # Add some items to the list
        self.add_three_companies()

        # Navigate to section summary
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.assertInUrl("/sections/section-companies/")

        # Edit  item 3

        edit_links = self.get_links("[data-qa='registration-number-edit']")
        self.get(edit_links[2])
        self.assertInUrl("?return_to=section-summary")
        self.post_repeating_block_1(
            registration_number=000, registration_date=date(2023, 9, 9)
        )
        self.assertInUrl("/sections/section-companies/")

        # Remove item 2

        edit_links = self.get_links("[data-qa='authorised-trader-uk-radio-edit']")
        self.get(edit_links[2])
        self.assertInUrl("?return_to=section-summary")
        self.post_repeating_block_2(trader_uk="No", trader_eu="No")
        self.assertInUrl("/sections/section-companies/")

        # Submit
        self.post()
        self.post()
        self.assertInBody(
            "Thank you for completing the Test a List Collector with Repeating Blocks and Section Summary Items"
        )

    def test_adding_incomplete_list_item_from_summary_returns_to_list_collector_not_summary(
            self,
    ):
        self.launchSurvey("test_list_collector_repeating_blocks_section_summary")

        # Add some items to the list
        self.add_three_companies()

        # Navigate to section summary
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.assertInUrl("/sections/section-companies/")

        # Add incomplete item from section summary add link
        add_link = self.get_link("[data-qa='add-item-link']")
        self.get(add_link)
        self.add_company(company_name="Company4")
        cancel_link = self.get_link("[id='cancel-and-return']")
        self.get(cancel_link)
        self.assertInUrl("/any-other-companies-or-branches/")
        self.assert_company_incomplete(
            company_name="Company4", selector="[data-qa='list-item-4-label']"
        )

        # Complete the incomplete item
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post_repeating_block_1(
            registration_number=101, registration_date=date(2023, 4, 4)
        )
        self.post_repeating_block_2(trader_uk="Yes", trader_eu="Yes")
        self.assert_company_completed(
            company_name="Company4", selector="[data-qa='list-item-4-label']"
        )

        # Navigate to submit summary
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post()

        # Add incomplete item from submit summary add link
        add_link = self.get_link("[data-qa='add-item-link']")
        self.get(add_link)
        self.add_company(company_name="Company5")
        cancel_link = self.get_link("[id='cancel-and-return']")
        self.get(cancel_link)
        self.assertInUrl("/any-other-companies-or-branches/")
        self.assert_company_incomplete(
            company_name="Company5", selector="[data-qa='list-item-5-label']"
        )

        # Complete the incomplete item
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post_repeating_block_1(
            registration_number=121, registration_date=date(2023, 5, 5)
        )
        self.post_repeating_block_2(trader_uk="No", trader_eu="No")
        self.assert_company_completed(
            company_name="Company5", selector="[data-qa='list-item-5-label']"
        )

        # Submit
        self.post({"any-other-companies-or-branches-answer": "No"})
        self.post()
        self.post()
        self.assertInBody(
            "Thank you for completing the Test a List Collector with Repeating Blocks and Section Summary Items"
        )
