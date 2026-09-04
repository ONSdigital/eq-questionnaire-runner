import { test, expect } from '../../../fixtures/test'
import HouseholdCountSectionSummaryPage from '../../../generated_pages/section_summary/household-count-section-summary.page'
import HouseholdDetailsSummaryPage from '../../../generated_pages/section_summary/house-details-section-summary.page'
import HouseType from '../../../generated_pages/section_summary/house-type.page'
import InsuranceAddressPage from '../../../generated_pages/section_summary/insurance-address.page'
import InsuranceTypePage from '../../../generated_pages/section_summary/insurance-type.page'
import ListedPage from '../../../generated_pages/section_summary/listed.page'
import NumberOfPeoplePage from '../../../generated_pages/section_summary/number-of-people.page'
import PropertyDetailsSummaryPage from '../../../generated_pages/section_summary/property-details-section-summary.page'
import SubmitPage from '../../../generated_pages/section_summary/submit.page'

test.describe('Collapsible Summary', () => {
  test.describe('Given I complete a questionnaire with collapsible summary enabled', () => {
    test.beforeEach(async ({ page, openQuestionnaire }) => {
      const householdCountSectionSummaryPage = new HouseholdCountSectionSummaryPage(page)
      const householdDetailsSummaryPage = new HouseholdDetailsSummaryPage(page)
      const houseType = new HouseType(page)
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const insuranceTypePage = new InsuranceTypePage(page)
      const listedPage = new ListedPage(page)
      const numberOfPeoplePage = new NumberOfPeoplePage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await openQuestionnaire('test_section_summary.json')
      await insuranceTypePage.both().click()
      await insuranceTypePage.submit().click()
      await insuranceAddressPage.submit().click()
      await listedPage.submit().click()
      await propertyDetailsSummaryPage.submit().click()
      await houseType.submit().click()
      await householdDetailsSummaryPage.submit().click()
      await numberOfPeoplePage.answer().fill('3')
      await numberOfPeoplePage.submit().click()
      await householdCountSectionSummaryPage.submit().click()
    })

    test('When I am on the submit page, Then a collapsed summary should be displayed with the group title and questions should not be displayed', async ({
      page
    }) => {
      const submitPage = new SubmitPage(page)
      await expect(submitPage.collapsibleSummary()).toBeVisible()

      await expect(submitPage.collapsibleSummary()).toContainText('Property Details')
      await expect(submitPage.collapsibleSummary()).toContainText('House Details')

      await expect(submitPage.insuranceAddressQuestion()).not.toBeVisible()
      await expect(submitPage.numberOfPeopleQuestion()).not.toBeVisible()
    })

    test('When I click the Show all button, Then the summary should be expanded and questions should be displayed', async ({ page }) => {
      const submitPage = new SubmitPage(page)
      await submitPage.summaryShowAllButton().click()

      await expect(submitPage.insuranceAddressQuestion()).toHaveText('What is the address you would like to insure?')
      await expect(submitPage.insuranceAddressQuestion()).toBeVisible()
      await expect(submitPage.numberOfPeopleQuestion()).toHaveText('Title')
      await expect(submitPage.numberOfPeopleQuestion()).toBeVisible()
    })
  })
})
