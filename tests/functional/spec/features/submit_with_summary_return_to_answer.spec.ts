import { test, expect } from '../../fixtures/test'
import InsuranceAddressPage from '../../generated_pages/submit_with_summary_return_to_answer/insurance-address.page'
import InsuranceTypePage from '../../generated_pages/submit_with_summary_return_to_answer/insurance-type.page'
import PropertyDetailsSummaryPage from '../../generated_pages/submit_with_summary_return_to_answer/property-details-section-summary.page'
import HouseType from '../../generated_pages/submit_with_summary_return_to_answer/house-type.page'
import HouseholdDetailsSummaryPage from '../../generated_pages/submit_with_summary_return_to_answer/house-details-section-summary.page'
import SubmitPage from '../../generated_pages/submit_with_summary_return_to_answer/submit.page'
import AddressDurationPage from '../../generated_pages/submit_with_summary_return_to_answer/address-duration.page'
import NamePage from '../../generated_pages/submit_with_summary_return_to_answer/name.page'

test.describe('Summary Anchor Scrolling', () => {
  test.describe('Given I start a Test Section Summary survey', () => {
    test.beforeEach(async ({ page, openQuestionnaire }) => {
      const insuranceTypePage = new InsuranceTypePage(page)
      const namePage = new NamePage(page)
      await openQuestionnaire('test_submit_with_summary_return_to_answer.json')
      await namePage.submit().click()
      await insuranceTypePage.both().click()
      await insuranceTypePage.submit().click()
    })

    test(
      'When I have provided an answer and click through to the next question, ' +
        "Then the Previous link url shouldn't contain any anchors or reference to return_to or return_to_answer_id",
      async ({ page }) => {
        const insuranceAddressPage = new InsuranceAddressPage(page)
        await expect(insuranceAddressPage.previous()).not.toHaveAttribute('href', /#/)
        await expect(insuranceAddressPage.previous()).not.toHaveAttribute('href', /return_to/)
        await expect(insuranceAddressPage.previous()).not.toHaveAttribute('href', /return_to_answer_id/)
      }
    )

    test('When I reach the section summary page, Then the Change link url should contain return_to, return_to_answer_id query params', async ({ page }) => {
      const addressDurationPage = new AddressDurationPage(page)
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await insuranceAddressPage.submit().click()
      await addressDurationPage.submit().click()
      const insuranceAddressEditHref = await propertyDetailsSummaryPage.insuranceAddressAnswer2Edit().getAttribute('href')
      expect(insuranceAddressEditHref).toContain(
        'insurance-address/?return_to=section-summary&return_to_answer_id=insurance-address-answer2#insurance-address-answer2'
      )
    })

    test('When I reach the section summary page, Then the Change link url for a concatenated answer should contain return_to, return_to_answer_id query params', async ({
      page
    }) => {
      const addressDurationPage = new AddressDurationPage(page)
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await insuranceAddressPage.submit().click()
      await addressDurationPage.submit().click()
      const concatenatedNameEditHref = await propertyDetailsSummaryPage.summaryRowState('name-question-concatenated-answer-edit').getAttribute('href')
      expect(concatenatedNameEditHref).toContain('name/?return_to=section-summary&return_to_answer_id=name-question-concatenated-answer#first-name')
    })

    test('When I edit an answer from the section summary page, Then the Previous link url should contain an anchor referencing the answer id of the answer I am changing', async ({
      page
    }) => {
      const addressDurationPage = new AddressDurationPage(page)
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await insuranceAddressPage.submit().click()
      await addressDurationPage.submit().click()
      await propertyDetailsSummaryPage.insuranceAddressAnswer2Edit().click()
      await expect(insuranceAddressPage.previous()).toHaveAttribute('href', /property-details-section\/#insurance-address-answer2/)
    })

    test('When I edit an answer from the section summary page and click the Previous link, Then the browser url should contain an anchor referencing the answer id of the answer I am changing', async ({
      page
    }) => {
      const addressDurationPage = new AddressDurationPage(page)
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await insuranceAddressPage.submit().click()
      await addressDurationPage.submit().click()
      await propertyDetailsSummaryPage.insuranceAddressAnswer2Edit().click()
      await insuranceAddressPage.previous().click()
      await expect(page).toHaveURL(/property-details-section\/#insurance-address-answer2/)
    })

    test('When I edit an answer from the section summary page and click the Submit button, Then I am taken to the summary page and the browser url should contain an anchor referencing the answer id of the answer I am changing', async ({
      page
    }) => {
      const addressDurationPage = new AddressDurationPage(page)
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      await insuranceAddressPage.submit().click()
      await addressDurationPage.submit().click()
      await propertyDetailsSummaryPage.insuranceAddressAnswer2Edit().click()
      await insuranceAddressPage.submit().click()
      await expect(page).toHaveURL(/property-details-section\/#insurance-address-answer2/)
    })

    test('When I am on the final summary page, Then the Change link url should contain return_to, return_to_answer_id query params', async ({ page }) => {
      const addressDurationPage = new AddressDurationPage(page)
      const householdDetailsSummaryPage = new HouseholdDetailsSummaryPage(page)
      const houseType = new HouseType(page)
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      const submitPage = new SubmitPage(page)
      await insuranceAddressPage.submit().click()
      await addressDurationPage.submit().click()
      await propertyDetailsSummaryPage.submit().click()
      await houseType.submit().click()
      await householdDetailsSummaryPage.submit().click()
      await submitPage.summaryShowAllButton().click()
      const finalSummaryInsuranceEditHref = await submitPage.insuranceAddressAnswer2Edit().getAttribute('href')
      expect(finalSummaryInsuranceEditHref).toContain('?return_to=final-summary&return_to_answer_id=insurance-address-answer2#insurance-address-answer2')
    })

    test('When I edit an answer from the final summary page, Then the browser url contains return_to, return_to_answer_id query params', async ({ page }) => {
      const addressDurationPage = new AddressDurationPage(page)
      const householdDetailsSummaryPage = new HouseholdDetailsSummaryPage(page)
      const houseType = new HouseType(page)
      const insuranceAddressPage = new InsuranceAddressPage(page)
      const propertyDetailsSummaryPage = new PropertyDetailsSummaryPage(page)
      const submitPage = new SubmitPage(page)
      await insuranceAddressPage.submit().click()
      await addressDurationPage.submit().click()
      await propertyDetailsSummaryPage.submit().click()
      await houseType.submit().click()
      await householdDetailsSummaryPage.submit().click()
      await submitPage.summaryShowAllButton().click()
      await submitPage.insuranceAddressAnswer2Edit().click()
      await expect(page).toHaveURL(/\\?return_to=final-summary&return_to_answer_id=insurance-address-answer2#insurance-address-answer2/)
    })
  })
})
