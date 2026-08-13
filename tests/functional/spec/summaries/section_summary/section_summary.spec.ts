import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../fixtures/test'
import AddressDurationPage from '../../../generated_pages/section_summary/address-duration.page'
import HouseholdCountSectionSummaryPage from '../../../generated_pages/section_summary/household-count-section-summary.page'
import HouseholdDetailsSummaryPage from '../../../generated_pages/section_summary/house-details-section-summary.page'
import HouseType from '../../../generated_pages/section_summary/house-type.page'
import InsuranceAddressPage from '../../../generated_pages/section_summary/insurance-address.page'
import InsuranceTypePage from '../../../generated_pages/section_summary/insurance-type.page'
import ListedPage from '../../../generated_pages/section_summary/listed.page'
import NumberOfPeoplePage from '../../../generated_pages/section_summary/number-of-people.page'
import PropertyDetailsSummaryPage from '../../../generated_pages/section_summary/property-details-section-summary.page'
import SubmitPage from '../../../generated_pages/section_summary/submit.page'

test.describe('Section Summary', () => {
  test.describe.configure({ mode: 'serial' })

  let page: Page
  let openQuestionnaire: OpenQuestionnaire

  test.beforeEach(async ({ page: fixturePage, openQuestionnaire: fixtureOpenQuestionnaire }) => {
    page = fixturePage
    openQuestionnaire = fixtureOpenQuestionnaire
  })

  test.describe('Given I start a Test Section Summary survey and complete to Section Summary', () => {
    test.beforeEach(async () => {
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const insuranceTypePage = new InsuranceTypePage(page)
      const listedPage = new ListedPage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await openQuestionnaire('test_section_summary.json')
      await insuranceTypePage.both().click()
      await insuranceTypePage.submit().click()
      await insuranceAddressPage.submit().click()
      await listedPage.submit().click()
      await expect(propertyDetailsSummaryPage.insuranceTypeAnswer()).toHaveText('Both')
    })

    test("When I get to the section summary page, Then the submit button should read 'Continue'", async () => {
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await expect(propertyDetailsSummaryPage.submit()).toHaveText('Continue')
    })

    test('When I have selected an answer to edit and edit it, Then I should return to the section summary with new value displayed', async () => {
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await propertyDetailsSummaryPage.insuranceAddressAnswerEdit().click()
      await insuranceAddressPage.answer().fill('Test Address')
      await insuranceAddressPage.submit().click()
      await expect(propertyDetailsSummaryPage.insuranceAddressAnswer()).toHaveText('Test Address')
    })

    test('When I select edit from the section summary and click previous on the question page, Then I should be taken back to the section summary', async () => {
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await propertyDetailsSummaryPage.insuranceAddressAnswerEdit().click()
      await insuranceAddressPage.previous().click()
      await expect(page).toHaveURL(new RegExp(propertyDetailsSummaryPage.url()))
    })

    test('When I continue on the section summary page, Then I should be taken to the next section', async () => {
      const houseType = new HouseType(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await propertyDetailsSummaryPage.submit().click()
      await expect(page).toHaveURL(new RegExp(houseType.pageName))
    })

    test('When I select edit from Section Summary but change routing, Then I should step through the section and be returned to the Section Summary once all new questions have been answered', async () => {
      const addressDurationPage = new AddressDurationPage(page)
      const insuranceTypePage = new InsuranceTypePage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await propertyDetailsSummaryPage.insuranceTypeAnswerEdit().click()
      await insuranceTypePage.contents().click()
      await insuranceTypePage.submit().click()
      await expect(page).toHaveURL(new RegExp(addressDurationPage.pageName))
      await addressDurationPage.submit().click()
      await expect(page).toHaveURL(new RegExp(propertyDetailsSummaryPage.pageName))
    })

    test('When I select edit from Section Summary but change routing, Then using previous should not prevent me returning to the section summary once all new questions have been answered', async () => {
      const addressDurationPage = new AddressDurationPage(page)
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const insuranceTypePage = new InsuranceTypePage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await propertyDetailsSummaryPage.insuranceTypeAnswerEdit().click()
      await insuranceTypePage.contents().click()
      await insuranceTypePage.submit().click()
      await expect(page).toHaveURL(new RegExp(addressDurationPage.pageName))
      await addressDurationPage.previous().click()
      await expect(page).toHaveURL(new RegExp(insuranceAddressPage.pageName))
      await insuranceAddressPage.submit().click()
      await addressDurationPage.submit().click()
      await expect(page).toHaveURL(new RegExp(propertyDetailsSummaryPage.pageName))
    })
  })

  test.describe('Given I start a Test Section Summary survey and complete to Final Summary', () => {
    test.beforeEach(async () => {
      const householdCountSectionSummaryPage = new HouseholdCountSectionSummaryPage(page)
      const householdDetailsSummaryPage = new HouseholdDetailsSummaryPage(page)
      const houseType = new HouseType(page)
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const insuranceTypePage = new InsuranceTypePage(page)
      const listedPage = new ListedPage(page)
      const numberOfPeoplePage = new NumberOfPeoplePage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      const submitPage = new SubmitPage(page)
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
      await expect(page).toHaveURL(new RegExp(submitPage.url()))
    })

    test("When I select edit from Final Summary and don't change an answer, Then I should be taken to the Final Summary", async () => {
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const submitPage = new SubmitPage(page)
      await submitPage.summaryShowAllButton().click()
      await submitPage.insuranceAddressAnswerEdit().click()
      await insuranceAddressPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.url()))
    })

    test("When I select edit from Final Summary and change an answer that doesn't affect completeness, Then I should be taken to the Final Summary", async () => {
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const submitPage = new SubmitPage(page)
      await submitPage.summaryShowAllButton().click()
      await submitPage.insuranceAddressAnswerEdit().click()
      await insuranceAddressPage.answer().fill('Test Address')
      await insuranceAddressPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.url()))
    })

    test('When I select edit from Final Summary but change routing, Then I should step through the section and be returned to the Final Summary once all new questions have been answered', async () => {
      const addressDurationPage = new AddressDurationPage(page)
      const insuranceTypePage = new InsuranceTypePage(page)
      const submitPage = new SubmitPage(page)
      await submitPage.summaryShowAllButton().click()
      await submitPage.insuranceTypeAnswerEdit().click()
      await insuranceTypePage.contents().click()
      await insuranceTypePage.submit().click()
      await expect(page).toHaveURL(new RegExp(addressDurationPage.pageName))
      await addressDurationPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })

    test('When I select edit from Final Summary but change routing, Then using previous should not prevent me returning to the section summary once all new questions have been answered', async () => {
      const addressDurationPage = new AddressDurationPage(page)
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const insuranceTypePage = new InsuranceTypePage(page)
      const submitPage = new SubmitPage(page)
      await submitPage.summaryShowAllButton().click()
      await submitPage.insuranceTypeAnswerEdit().click()
      await insuranceTypePage.contents().click()
      await insuranceTypePage.submit().click()
      await expect(page).toHaveURL(new RegExp(addressDurationPage.pageName))
      await addressDurationPage.previous().click()
      await expect(page).toHaveURL(new RegExp(insuranceAddressPage.pageName))
      await insuranceAddressPage.submit().click()
      await addressDurationPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })

    test('When I select edit from Final Summary and change an answer and then go to the next question and click previous, Since I cannot return to the section summary yet I return to the previous block in the section', async () => {
      const addressDurationPage = new AddressDurationPage(page)
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const insuranceTypePage = new InsuranceTypePage(page)
      const submitPage = new SubmitPage(page)
      await submitPage.summaryShowAllButton().click()
      await submitPage.insuranceTypeAnswerEdit().click()
      await insuranceTypePage.contents().click()
      await insuranceTypePage.submit().click()
      await addressDurationPage.previous().click()
      await expect(page).toHaveURL(new RegExp(insuranceAddressPage.pageName))
    })

    test('When I change an answer, Then the final summary should display the updated value', async () => {
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const submitPage = new SubmitPage(page)
      await submitPage.summaryShowAllButton().click()
      await expect(submitPage.insuranceAddressAnswer()).toHaveText('No answer provided')
      await submitPage.insuranceAddressAnswerEdit().click()
      await expect(page).toHaveURL(new RegExp(insuranceAddressPage.pageName))
      await insuranceAddressPage.answer().fill('Test Address')
      await insuranceAddressPage.submit().click()
      await submitPage.summaryShowAllButton().click()
      await expect(submitPage.insuranceAddressAnswer()).toHaveText('Test Address')
    })
  })

  test.describe('Given I start the Test Section Summary questionnaire', () => {
    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll(async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_section_summary.json')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When there is no title set in the sections summary, the section title is used for the section summary title', async () => {
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const insuranceTypePage = new InsuranceTypePage(page)
      const listedPage = new ListedPage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await insuranceTypePage.both().click()
      await insuranceTypePage.submit().click()
      await insuranceAddressPage.submit().click()
      await listedPage.submit().click()
      await expect(propertyDetailsSummaryPage.heading()).toHaveText('Property Details Section')
    })

    test('When there is a title set in the sections summary, it is used for the section summary title', async () => {
      const householdDetailsSummaryPage = new HouseholdDetailsSummaryPage(page)
      const houseType = new HouseType(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await propertyDetailsSummaryPage.submit().click()
      await houseType.semiDetached().click()
      await houseType.submit().click()
      await expect(householdDetailsSummaryPage.heading()).toHaveText('Household Summary - Semi-detached')
    })
  })
})
