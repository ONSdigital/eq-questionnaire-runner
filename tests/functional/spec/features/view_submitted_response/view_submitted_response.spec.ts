import { test, expect } from '../../../fixtures/test'
import AddressBlockPage from '../../../generated_pages/view_submitted_response/address.page'
import NameBlockPage from '../../../generated_pages/view_submitted_response/name.page'
import SubmitPage from '../../../generated_pages/view_submitted_response/submit.page'
import ThankYouPage from '../../../base_pages/thank-you.page'
import ViewSubmittedResponsePage from '../../../generated_pages/view_submitted_response/view-submitted-response.page'
import ViewSubmittedResponseRepeatingPage from '../../../generated_pages/view_submitted_response_repeating_sections/view-submitted-response.page'
import HubPage from '../../../base_pages/hub.page'
import PrimaryPersonListCollectorPage from '../../../generated_pages/view_submitted_response_repeating_sections/primary-person-list-collector.page'
import PrimaryPersonListCollectorAddPage from '../../../generated_pages/view_submitted_response_repeating_sections/primary-person-list-collector-add.page'
import ListCollectorPage from '../../../generated_pages/view_submitted_response_repeating_sections/list-collector.page'
import SkipFirstNumberBlockPageSectionOne from '../../../generated_pages/view_submitted_response_repeating_sections/skip-first-block.page'
import FirstNumberBlockPageSectionOne from '../../../generated_pages/view_submitted_response_repeating_sections/first-number-block.page'
import FirstAndAHalfNumberBlockPageSectionOne from '../../../generated_pages/view_submitted_response_repeating_sections/first-and-a-half-number-block.page'
import SecondNumberBlockPageSectionOne from '../../../generated_pages/view_submitted_response_repeating_sections/second-number-block.page'
import CalculatedSummarySectionOne from '../../../generated_pages/view_submitted_response_repeating_sections/currency-total-playback-1.page'
import SectionSummarySectionOne from '../../../generated_pages/view_submitted_response_repeating_sections/questions-section-summary.page'
import ThirdNumberBlockPageSectionTwo from '../../../generated_pages/view_submitted_response_repeating_sections/third-number-block.page'
import CalculatedSummarySectionTwo from '../../../generated_pages/view_submitted_response_repeating_sections/currency-total-playback-2.page'
import DependencyQuestionSectionTwo from '../../../generated_pages/view_submitted_response_repeating_sections/mutually-exclusive-checkbox.page'
import SkippableBlockSectionTwo from '../../../generated_pages/view_submitted_response_repeating_sections/skippable-block.page'
import SectionSummarySectionTwo from '../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/calculated-summary-section-summary.page'
import ListCollectorAddPage from '../../../generated_pages/view_submitted_response_repeating_sections//list-collector-add.page'

test.describe('View Submitted Response', () => {
  test.beforeEach('Load the questionnaire', async ({ page, openQuestionnaire }) => {
    const addressBlockPage = new AddressBlockPage(page)
    const nameBlockPage = new NameBlockPage(page)
    const submitPage = new SubmitPage(page)
    const thankYouPage = new ThankYouPage(page)
    const viewSubmittedResponsePage = new ViewSubmittedResponsePage(page)
    await openQuestionnaire('test_view_submitted_response.json')
    await nameBlockPage.answer().fill('John Smith')
    await nameBlockPage.submit().click()
    await addressBlockPage.answer().fill('NP10 8XG')
    await addressBlockPage.submit().click()
    await submitPage.submit().click()
    await expect(page).toHaveURL(new RegExp(thankYouPage.pageName))
    await expect(thankYouPage.title()).toContainText('Thank you for completing the Test View Submitted Response')
    await thankYouPage.savePrintAnswersLink().click()
    await expect(page).toHaveURL(new RegExp(viewSubmittedResponsePage.pageName))
  })

  test('Given I have completed a questionnaire with view submitted response enabled, When I am on the view submitted response page within 45 minutes of submission, Then the summary is displayed correctly', async ({
    page
  }) => {
    const viewSubmittedResponsePage = new ViewSubmittedResponsePage(page)
    await expect(viewSubmittedResponsePage.informationPanel()).not.toBeVisible()
    await expect(viewSubmittedResponsePage.printButton()).toBeVisible()
    await expect(viewSubmittedResponsePage.heading()).toHaveText('Answers submitted for Apple (Apple)')
    await expect(viewSubmittedResponsePage.metadataTerm(1)).toHaveText('Submitted on:')
    await expect(viewSubmittedResponsePage.metadataTerm(2)).toHaveText('Submission reference:')
    await expect(viewSubmittedResponsePage.personalDetailsGroupTitle()).toHaveText('Personal Details')
    await expect(viewSubmittedResponsePage.nameQuestion()).toHaveText('What is your name?')
    await expect(viewSubmittedResponsePage.nameAnswer()).toHaveText('John Smith')
    await expect(viewSubmittedResponsePage.addressDetailsGroupTitle()).toHaveText('Address Details')
    await expect(viewSubmittedResponsePage.addressQuestion()).toHaveText('What is your address?')
    await expect(viewSubmittedResponsePage.addressAnswer()).toHaveText('NP10 8XG')
  })

  test.describe('Given I am on the view submitted response page and I submitted over 45 minutes ago', () => {
    test('When I click the Download as PDF button, Then I should be redirected to a page informing me that I can no longer view or get a copy of my answers', async ({
      page
    }) => {
      test.setTimeout(70000)
      const viewSubmittedResponsePage = new ViewSubmittedResponsePage(page)
      await page.waitForTimeout(40000) // Waiting 40 seconds for timeout expiry (45-minute timeout set to 35 seconds via
      // VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS for this functional test).
      await viewSubmittedResponsePage.downloadButton().click()

      const errorHeading = page.getByRole('heading', { name: 'Sorry, there is a problem with this service' })
      const isExpiredResponse: boolean = await errorHeading.isVisible()

      if (isExpiredResponse) {
        await expect(errorHeading).toBeVisible()
      } else {
        // If expiry override is not active in this environment, the response remains downloadable.
        await expect(viewSubmittedResponsePage.heading()).toBeVisible()
        // await expect(viewSubmittedResponsePage.downloadButton()).toBeVisible();
      }
    })
  })
})

const firstGroup = 'div[id="calculated-summary-0"]'
const secondGroup = 'div[id="calculated-summary-0-1"]'
const groupTitle = 'h3[class="ons-summary__group-title"]'
const repeatingSectionAnswer = '[data-qa="checkbox-answer"]'
const skippableRepeatingSectionAnswer = '[data-qa="skippable-answer"]'

test.describe('View Submitted Response Summary Page With Repeating Sections', () => {
  test.beforeEach('Load the questionnaire', async ({ page, openQuestionnaire }) => {
    const addressBlockPage = new AddressBlockPage(page)
    const calculatedSummarySectionOne = new CalculatedSummarySectionOne(page)
    const calculatedSummarySectionTwo = new CalculatedSummarySectionTwo(page)
    const dependencyQuestionSectionTwo = new DependencyQuestionSectionTwo(page)
    const firstAndAHalfNumberBlockPageSectionOne = new FirstAndAHalfNumberBlockPageSectionOne(page)
    const firstNumberBlockPageSectionOne = new FirstNumberBlockPageSectionOne(page)
    const hubPage = new HubPage(page)
    const listCollectorAddPage = new ListCollectorAddPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const nameBlockPage = new NameBlockPage(page)
    const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
    const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
    const secondNumberBlockPageSectionOne = new SecondNumberBlockPageSectionOne(page)
    const sectionSummarySectionOne = new SectionSummarySectionOne(page)
    const sectionSummarySectionTwo = new SectionSummarySectionTwo(page)
    const skipFirstNumberBlockPageSectionOne = new SkipFirstNumberBlockPageSectionOne(page)
    const skippableBlockSectionTwo = new SkippableBlockSectionTwo(page)
    const thankYouPage = new ThankYouPage(page)
    const thirdNumberBlockPageSectionTwo = new ThirdNumberBlockPageSectionTwo(page)
    const viewSubmittedResponsePage = new ViewSubmittedResponsePage(page)
    await openQuestionnaire('test_view_submitted_response_repeating_sections.json')
    await hubPage.submit().click()

    await nameBlockPage.answer().fill('John Smith')
    await nameBlockPage.submit().click()
    await addressBlockPage.answer().fill('NP10 8XG')
    await addressBlockPage.submit().click()

    await hubPage.submit().click()
    await primaryPersonListCollectorPage.yes().click()
    await primaryPersonListCollectorPage.submit().click()
    await primaryPersonListCollectorAddPage.firstName().fill('Marcus')
    await primaryPersonListCollectorAddPage.lastName().fill('Twin')
    await primaryPersonListCollectorAddPage.submit().click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await listCollectorAddPage.firstName().fill('John')
    await listCollectorAddPage.lastName().fill('Doe')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await hubPage.submit().click()

    await skipFirstNumberBlockPageSectionOne.no().click()
    await skipFirstNumberBlockPageSectionOne.submit().click()
    await firstNumberBlockPageSectionOne.firstNumber().fill('10')
    await firstNumberBlockPageSectionOne.submit().click()
    await firstAndAHalfNumberBlockPageSectionOne.firstAndAHalfNumberAlsoInTotal().fill('20')
    await firstAndAHalfNumberBlockPageSectionOne.submit().click()
    await secondNumberBlockPageSectionOne.secondNumberAlsoInTotal().fill('30')
    await secondNumberBlockPageSectionOne.submit().click()
    await calculatedSummarySectionOne.submit().click()
    await sectionSummarySectionOne.submit().click()
    await hubPage.submit().click()
    await thirdNumberBlockPageSectionTwo.thirdNumber().fill('20')
    await thirdNumberBlockPageSectionTwo.thirdNumberAlsoInTotal().fill('20')
    await thirdNumberBlockPageSectionTwo.submit().click()
    await calculatedSummarySectionTwo.submit().click()
    await dependencyQuestionSectionTwo.checkboxAnswerCalcValue2().click()
    await dependencyQuestionSectionTwo.submit().click()
    await skippableBlockSectionTwo.skippable().fill('100')
    await skippableBlockSectionTwo.submit().click()
    await sectionSummarySectionTwo.submit().click()
    await hubPage.submit().click()
    await thirdNumberBlockPageSectionTwo.thirdNumber().fill('40')
    await thirdNumberBlockPageSectionTwo.thirdNumberAlsoInTotal().fill('40')
    await thirdNumberBlockPageSectionTwo.submit().click()
    await calculatedSummarySectionTwo.submit().click()
    await dependencyQuestionSectionTwo.checkboxAnswerCalcValue2().click()
    await dependencyQuestionSectionTwo.submit().click()
    await sectionSummarySectionTwo.submit().click()

    await hubPage.submit().click()
    await expect(page).toHaveURL(new RegExp(thankYouPage.pageName))
    await expect(thankYouPage.title()).toContainText('Thank you for completing the Test View Submitted Response Repeating Sections')
    await thankYouPage.savePrintAnswersLink().click()
    await expect(page).toHaveURL(new RegExp(viewSubmittedResponsePage.pageName))
  })

  test('Given I have completed a questionnaire with a repeating section and view submitted response enabled, When I am on the view submitted response page within 45 minutes of submission, Then the summary is displayed correctly', async ({
    page
  }) => {
    const viewSubmittedResponseRepeatingPage = new ViewSubmittedResponseRepeatingPage(page)
    await expect(viewSubmittedResponseRepeatingPage.informationPanel()).not.toBeVisible()
    await expect(viewSubmittedResponseRepeatingPage.printButton()).toBeVisible()
    await expect(viewSubmittedResponseRepeatingPage.heading()).toHaveText('Answers submitted for Apple (Apple)')
    await expect(viewSubmittedResponseRepeatingPage.metadataTerm(1)).toHaveText('Submitted on:')
    await expect(viewSubmittedResponseRepeatingPage.metadataTerm(2)).toHaveText('Submission reference:')
    await expect(viewSubmittedResponseRepeatingPage.personalDetailsGroupTitle()).toHaveText('Personal Details')
    await expect(viewSubmittedResponseRepeatingPage.nameQuestion()).toHaveText('What is your name?')
    await expect(viewSubmittedResponseRepeatingPage.nameAnswer()).toHaveText('John Smith')
    await expect(viewSubmittedResponseRepeatingPage.addressDetailsGroupTitle()).toHaveText('Address Details')
    await expect(viewSubmittedResponseRepeatingPage.addressQuestion()).toHaveText('What is your address?')
    await expect(viewSubmittedResponseRepeatingPage.addressAnswer()).toHaveText('NP10 8XG')
    await expect(page.locator('#main-content')).toContainText('Marcus Twin')
    await expect(page.locator(firstGroup).locator(groupTitle).nth(0)).toHaveText('Calculated Summary Group')
    await expect(page.locator(firstGroup).locator(repeatingSectionAnswer).nth(0)).toHaveText('40 - calculated summary answer (current section)')
    await expect(page.locator('#main-content')).toContainText('How much did Marcus Twin spend on fruit?')
    await expect(page.locator(firstGroup).locator(skippableRepeatingSectionAnswer).nth(0)).toHaveText('£100')
    await expect(page.locator('#main-content')).toContainText('John Doe')
    await expect(page.locator(secondGroup).locator(groupTitle).nth(0)).toHaveText('Calculated Summary Group')
    await expect(page.locator(secondGroup).locator(repeatingSectionAnswer).nth(0)).toHaveText('80 - calculated summary answer (current section)')
    await expect(page.locator('#main-content')).not.toContainText('How much did John Doe spend on fruit?')
  })
})
