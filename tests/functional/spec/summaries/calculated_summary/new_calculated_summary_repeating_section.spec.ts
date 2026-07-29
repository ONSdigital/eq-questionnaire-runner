import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../fixtures/test'
import FirstNumberBlockPage from '../../../generated_pages/new_calculated_summary_repeating_section/first-number-block.page'
import SecondNumberBlockPage from '../../../generated_pages/new_calculated_summary_repeating_section/second-number-block.page'
import ThirdNumberBlockPage from '../../../generated_pages/new_calculated_summary_repeating_section/third-number-block.page'
import ThirdAndAHalfNumberBlockPage from '../../../generated_pages/new_calculated_summary_repeating_section/third-and-a-half-number-block.page'
import SkipFourthBlockPage from '../../../generated_pages/new_calculated_summary_repeating_section/skip-fourth-block.page'
import FourthNumberBlockPage from '../../../generated_pages/new_calculated_summary_repeating_section/fourth-number-block.page'
import FourthAndAHalfNumberBlockPage from '../../../generated_pages/new_calculated_summary_repeating_section/fourth-and-a-half-number-block.page'
import FifthNumberBlockPage from '../../../generated_pages/new_calculated_summary_repeating_section/fifth-number-block.page'
import SixthNumberBlockPage from '../../../generated_pages/new_calculated_summary_repeating_section/sixth-number-block.page'
import CurrencyTotalPlaybackPage from '../../../generated_pages/new_calculated_summary_repeating_section/currency-total-playback.page'
import SetMinMaxBlockPage from '../../../generated_pages/new_calculated_summary_repeating_section/set-min-max-block.page'
import UnitTotalPlaybackPage from '../../../generated_pages/new_calculated_summary_repeating_section/unit-total-playback.page'
import PercentageTotalPlaybackPage from '../../../generated_pages/new_calculated_summary_repeating_section/percentage-total-playback.page'
import NumberTotalPlaybackPage from '../../../generated_pages/new_calculated_summary_repeating_section/number-total-playback.page'
import BreakdownPage from '../../../generated_pages/new_calculated_summary_repeating_section/breakdown.page'
import SecondCurrencyTotalPlaybackPage from '../../../generated_pages/new_calculated_summary_repeating_section/second-currency-total-playback.page'
import CalculatedSummaryTotalConfirmation from '../../../generated_pages/new_calculated_summary_repeating_section/calculated-summary-total-confirmation.page'
import SubmitPage from '../../../generated_pages/new_calculated_summary_repeating_section/personal-details-section-summary.page'
import ThankYouPage from '../../../base_pages/thank-you.page'
import HubPage from '../../../base_pages/hub.page'
import PrimaryPersonListCollectorPage from '../../../generated_pages/new_calculated_summary_repeating_section/primary-person-list-collector.page'
import PrimaryPersonListCollectorAddPage from '../../../generated_pages/new_calculated_summary_repeating_section/primary-person-list-collector-add.page'
import ListCollectorPage from '../../../generated_pages/new_calculated_summary_repeating_section/list-collector.page'
import ListCollectorAddPage from '../../../generated_pages/new_calculated_summary_repeating_section/list-collector-add.page'
import SkipFirstNumberBlockPageSectionOne from '../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/skip-first-block.page'
import FirstNumberBlockPageSectionOne from '../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/first-number-block.page'
import FirstAndAHalfNumberBlockPageSectionOne from '../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/first-and-a-half-number-block.page'
import SecondNumberBlockPageSectionOne from '../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/second-number-block.page'
import CalculatedSummarySectionOne from '../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/currency-total-playback-1.page'
import CalculatedSummarySectionTwo from '../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/currency-total-playback-2.page'
import ThirdNumberBlockPageSectionTwo from '../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/third-number-block.page'
import SectionSummarySectionOne from '../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/questions-section-summary.page'
import SectionSummarySectionTwo from '../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/calculated-summary-section-summary.page'
import DependencyQuestionSectionTwo from '../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/mutually-exclusive-checkbox.page'
import MinMaxSectionTwo from '../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/set-min-max-block.page'

test.describe('Feature: Calculated Summary Repeating Section', () => {
  test.describe('Given I have a Calculated Summary in a Repeating Section', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Get to Calculated Summary', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const hubPage = new HubPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      await openQuestionnaire('test_new_calculated_summary_repeating_section.json')
      await hubPage.submit().click()
      await primaryPersonListCollectorPage.yes().click()
      await primaryPersonListCollectorPage.submit().click()
      await primaryPersonListCollectorAddPage.firstName().fill('Marcus')
      await primaryPersonListCollectorAddPage.lastName().fill('Twin')
      await primaryPersonListCollectorAddPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await hubPage.submit().click()

      await getToFirstCalculatedSummary(page)

      await expect(page).toHaveURL(new RegExp(currencyTotalPlaybackPage.pageName))
    })

    test.afterAll(async () => {
      await context.close()
    })

    test(
      'Given I have completed all questions, ' +
        "When I am on the calculated summary and there is no custom page title, Then the page title should use the calculation's title",
      async () => {
        await expect(page).toHaveTitle('Grand total of previous values - Test New Calculated Summary Repeating Section')
      }
    )

    test('Given I complete every question, When I get to the currency summary, Then I should see the correct total', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const numberTotalPlaybackPage = new NumberTotalPlaybackPage(page)
      const unitTotalPlaybackPage = new UnitTotalPlaybackPage(page)
      // Totals and titles should be shown
      await expect(currencyTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of currency values entered to be £20.71. Is this correct?'
      )
      await expect(currencyTotalPlaybackPage.calculatedSummaryQuestion()).toHaveText('Grand total of previous values')
      await expect(currencyTotalPlaybackPage.calculatedSummaryAnswer()).toHaveText('£20.71')

      // Answers included in calculation should be shown
      await expect(currencyTotalPlaybackPage.firstNumberAnswerLabel()).toHaveText('First answer label')
      await expect(currencyTotalPlaybackPage.firstNumberAnswer()).toHaveText('£1.23')
      await expect(currencyTotalPlaybackPage.secondNumberAnswerLabel()).toHaveText('Second answer in currency label')
      await expect(currencyTotalPlaybackPage.secondNumberAnswer()).toHaveText('£4.56')
      await expect(currencyTotalPlaybackPage.secondNumberAnswerAlsoInTotalLabel()).toHaveText('Second answer label also in currency total (optional)')
      await expect(currencyTotalPlaybackPage.secondNumberAnswerAlsoInTotal()).toHaveText('£0.12')
      await expect(currencyTotalPlaybackPage.thirdNumberAnswerLabel()).toHaveText('Third answer label')
      await expect(currencyTotalPlaybackPage.thirdNumberAnswer()).toHaveText('£3.45')
      await expect(currencyTotalPlaybackPage.fourthNumberAnswerLabel()).toHaveText('Fourth answer label (optional)')
      await expect(currencyTotalPlaybackPage.fourthNumberAnswer()).toHaveText('£9.01')
      await expect(currencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotalLabel()).toHaveText('Fourth answer label also in total (optional)')
      await expect(currencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotal()).toHaveText('£2.34')

      // Answers not included in calculation should not be shown
      await expect(unitTotalPlaybackPage.secondNumberAnswerUnitTotal()).toHaveCount(0)
      await expect(unitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal()).toHaveCount(0)
      await expect(numberTotalPlaybackPage.fifthNumberAnswer()).toHaveCount(0)
      await expect(numberTotalPlaybackPage.sixthNumberAnswer()).toHaveCount(0)
    })

    test('Given I reach the calculated summary page, Then the Change link url should contain return_to, return_to_answer_id and return_to_block_id query params', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const firstNumberEditHref = await currencyTotalPlaybackPage.firstNumberAnswerEdit().getAttribute('href')
      expect(firstNumberEditHref).toContain(
        'first-number-block/?return_to=calculated-summary' +
          '&return_to_answer_id=first-number-answer&return_to_block_id=currency-total-playback#first-number-answer'
      )
    })

    test('Given I edit an answer from the calculated summary page and click the Previous button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await currencyTotalPlaybackPage.thirdNumberAnswerEdit().click()
      await thirdNumberBlockPage.previous().click()
      await expect(page).toHaveURL(/currency-total-playback\/#third-number-answer/)
    })

    test('Given I edit an answer from the calculated summary page and click the Submit button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await currencyTotalPlaybackPage.thirdNumberAnswerEdit().click()
      await thirdNumberBlockPage.submit().click()
      await expect(page).toHaveURL(/currency-total-playback\/#third-number-answer/)
    })

    test('Given I change an answer, When I get to the currency summary, Then I should see the new total', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const fourthNumberBlockPage = new FourthNumberBlockPage(page)
      await currencyTotalPlaybackPage.fourthNumberAnswerEdit().click()
      await fourthNumberBlockPage.fourthNumber().fill('19.01')
      await fourthNumberBlockPage.submit().click()

      await expect(page).toHaveURL(new RegExp(currencyTotalPlaybackPage.pageName))
      await expect(currencyTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of currency values entered to be £30.71. Is this correct?'
      )
      await expect(currencyTotalPlaybackPage.calculatedSummaryAnswer()).toHaveText('£30.71')
    })

    test('Given I leave an answer empty, When I get to the currency summary, Then I should see no answer provided and new total', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const fourthAndAHalfNumberBlockPage = new FourthAndAHalfNumberBlockPage(page)
      await currencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotalEdit().click()
      await fourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal().fill('')
      await fourthAndAHalfNumberBlockPage.submit().click()

      await expect(page).toHaveURL(new RegExp(currencyTotalPlaybackPage.pageName))
      await expect(currencyTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of currency values entered to be £28.37. Is this correct?'
      )
      await expect(currencyTotalPlaybackPage.calculatedSummaryAnswer()).toHaveText('£28.37')
      await expect(currencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotal()).toHaveText('No answer provided')
    })

    test('Given I skip the fourth page, When I get to the playback, Then I can should not see it in the total', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const fifthNumberBlockPage = new FifthNumberBlockPage(page)
      const fourthAndAHalfNumberBlockPage = new FourthAndAHalfNumberBlockPage(page)
      const fourthNumberBlockPage = new FourthNumberBlockPage(page)
      const sixthNumberBlockPage = new SixthNumberBlockPage(page)
      const skipFourthBlockPage = new SkipFourthBlockPage(page)
      await currencyTotalPlaybackPage.previous().click()
      await sixthNumberBlockPage.previous().click()
      await fifthNumberBlockPage.previous().click()
      await fourthAndAHalfNumberBlockPage.previous().click()
      await fourthNumberBlockPage.previous().click()

      await skipFourthBlockPage.yes().click()
      await skipFourthBlockPage.submit().click()

      await fifthNumberBlockPage.submit().click()
      await sixthNumberBlockPage.submit().click()

      await expect(page).toHaveURL(new RegExp(currencyTotalPlaybackPage.pageName))
      await expect(currencyTotalPlaybackPage.fourthNumberAnswer()).toHaveCount(0)
      await expect(currencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotal()).toHaveCount(0)
      await expect(currencyTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of currency values entered to be £9.36. Is this correct?'
      )
      await expect(currencyTotalPlaybackPage.calculatedSummaryAnswer()).toHaveText('£9.36')
    })

    test('Given I complete every question, When I get to the unit summary, Then I should see the correct total', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const unitTotalPlaybackPage = new UnitTotalPlaybackPage(page)
      // Totals and titles should be shown
      await currencyTotalPlaybackPage.submit().click()
      await expect(unitTotalPlaybackPage.calculatedSummaryTitle()).toHaveText('We calculate the total of unit values entered to be 1,467 cm. Is this correct?')
      await expect(unitTotalPlaybackPage.calculatedSummaryQuestion()).toHaveText('Grand total of previous values')
      await expect(unitTotalPlaybackPage.calculatedSummaryAnswer()).toHaveText('1,467 cm')

      // Answers included in calculation should be shown
      await expect(unitTotalPlaybackPage.secondNumberAnswerUnitTotalLabel()).toHaveText('Second answer label in unit total')
      await expect(unitTotalPlaybackPage.secondNumberAnswerUnitTotal()).toHaveText('789 cm')
      await expect(unitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotalLabel()).toHaveText('Third answer label in unit total')
      await expect(unitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal()).toHaveText('678 cm')
    })

    test('Given the calculated summary has a custom title, When I am on the unit calculated summary, Then the page title should use the custom title', async () => {
      await expect(page).toHaveTitle('Total Unit Values - Test New Calculated Summary Repeating Section')
    })

    test('Given I complete every question, When I get to the percentage summary, Then I should see the correct total', async () => {
      const percentageTotalPlaybackPage = new PercentageTotalPlaybackPage(page)
      const unitTotalPlaybackPage = new UnitTotalPlaybackPage(page)
      // Totals and titles should be shown
      await unitTotalPlaybackPage.submit().click()
      await expect(unitTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of percentage values entered to be 79%. Is this correct?'
      )
      await expect(unitTotalPlaybackPage.calculatedSummaryQuestion()).toHaveText('Grand total of previous values')
      await expect(unitTotalPlaybackPage.calculatedSummaryAnswer()).toHaveText('79%')

      // Answers included in calculation should be shown
      await expect(percentageTotalPlaybackPage.fifthPercentAnswerLabel()).toHaveText('Fifth answer label percentage total')
      await expect(percentageTotalPlaybackPage.fifthPercentAnswer()).toHaveText('56%')
      await expect(percentageTotalPlaybackPage.sixthPercentAnswerLabel()).toHaveText('Sixth answer label percentage total')
      await expect(percentageTotalPlaybackPage.sixthPercentAnswer()).toHaveText('23%')
    })

    test('Given the calculated summary has a custom title with the list item position, When I am on the percentage calculated summary, Then the page title should use the custom title with the list item position', async () => {
      await expect(page).toHaveTitle('Percentage Calculated Summary: Person 1 - Test New Calculated Summary Repeating Section')
    })

    test('Given I complete every question, When I get to the number summary, Then I should see the correct total', async () => {
      const numberTotalPlaybackPage = new NumberTotalPlaybackPage(page)
      const unitTotalPlaybackPage = new UnitTotalPlaybackPage(page)
      // Totals and titles should be shown
      await unitTotalPlaybackPage.submit().click()
      await expect(unitTotalPlaybackPage.calculatedSummaryTitle()).toHaveText('We calculate the total of number values entered to be 124.58. Is this correct?')
      await expect(unitTotalPlaybackPage.calculatedSummaryQuestion()).toHaveText('Grand total of previous values')
      await expect(unitTotalPlaybackPage.calculatedSummaryAnswer()).toHaveText('124.58')

      // Answers included in calculation should be shown
      await expect(numberTotalPlaybackPage.fifthNumberAnswerLabel()).toHaveText('Fifth answer label number total')
      await expect(numberTotalPlaybackPage.fifthNumberAnswer()).toHaveText('78.91')
      await expect(numberTotalPlaybackPage.sixthNumberAnswerLabel()).toHaveText('Sixth answer label number total')
      await expect(numberTotalPlaybackPage.sixthNumberAnswer()).toHaveText('45.67')
    })

    test('Given I have a calculated summary total that is used as a placeholder in another calculated summary, When I get to the calculated summary page displaying the placeholder, Then I should see the correct total', async () => {
      const breakdownPage = new BreakdownPage(page)
      const numberTotalPlaybackPage = new NumberTotalPlaybackPage(page)
      const secondCurrencyTotalPlaybackPage = new SecondCurrencyTotalPlaybackPage(page)
      await numberTotalPlaybackPage.submit().click()
      await expect(page).toHaveURL(new RegExp(breakdownPage.pageName))
      await breakdownPage.answer1().fill('100.0')
      await breakdownPage.answer2().fill('24.58')
      await breakdownPage.submit().click()
      await expect(page).toHaveURL(new RegExp(secondCurrencyTotalPlaybackPage.pageName))
      await expect(secondCurrencyTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of number values entered to be £124.58. Is this correct?'
      )
      await expect(page.locator('#main-content')).toContainText('Enter two values that add up to the previous calculated summary total of £124.58')
      await expect(secondCurrencyTotalPlaybackPage.calculatedSummaryAnswer()).toHaveText('£124.58')
    })

    test('Given I complete every calculated summary, When I go to a page with calculated summary piping, Then I should the see the piped calculated summary total for each summary', async () => {
      const secondCurrencyTotalPlaybackPage = new SecondCurrencyTotalPlaybackPage(page)
      await secondCurrencyTotalPlaybackPage.submit().click()

      const summaryList = page.locator('h1 + ul')
      const textsToAssert = ['Total currency values: £9.36', 'Total unit values: 1,467', 'Total percentage values: 79', 'Total number values: 124.58']

      for (const text of textsToAssert) {
        await expect(summaryList).toContainText(text)
      }
    })

    test('Given I have an answer minimum based on a calculated summary total, When I enter an invalid answer, Then I should see an error message on the page', async () => {
      const calculatedSummaryTotalConfirmation = new CalculatedSummaryTotalConfirmation(page)
      const setMinMaxBlockPage = new SetMinMaxBlockPage(page)
      await calculatedSummaryTotalConfirmation.submit().click()
      await expect(page).toHaveURL(new RegExp(setMinMaxBlockPage.pageName))
      await setMinMaxBlockPage.setMinimum().fill('8.0')
      await setMinMaxBlockPage.submit().click()
      await expect(setMinMaxBlockPage.errorNumber(1)).toHaveText('Enter an answer more than or equal to £9.36')
      await setMinMaxBlockPage.setMinimum().fill('10.0')
    })

    test('Given I have an answer maximum based on a calculated summary total, When I enter an invalid answer, Then I should see an error message on the page', async () => {
      const setMinMaxBlockPage = new SetMinMaxBlockPage(page)
      await setMinMaxBlockPage.setMaximum().fill('10.0')
      await setMinMaxBlockPage.submit().click()
      await expect(setMinMaxBlockPage.errorNumber(1)).toHaveText('Enter an answer less than or equal to £9.36')
      await setMinMaxBlockPage.setMaximum().fill('7.0')
      await setMinMaxBlockPage.submit().click()
    })

    test('Given I confirm the totals and am on the summary, When I edit and change an answer, Then I go to each incomplete page in turn before I return to the summary', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const setMinMaxBlockPage = new SetMinMaxBlockPage(page)
      const submitPage = new SubmitPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
      await submitPage.thirdNumberAnswerEdit().click()
      await thirdNumberBlockPage.thirdNumber().fill('3.5')
      await thirdNumberBlockPage.submit().click()

      // first incomplete block
      await expect(page).toHaveURL(new RegExp(currencyTotalPlaybackPage.pageName))
      await expect(currencyTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of currency values entered to be £9.41. Is this correct?'
      )
      await currencyTotalPlaybackPage.submit().click()

      // second incomplete block
      await expect(page).toHaveURL(new RegExp(setMinMaxBlockPage.pageName))
      await setMinMaxBlockPage.setMinimum().fill('10.0')
      await setMinMaxBlockPage.setMaximum().fill('9.0')
      await setMinMaxBlockPage.submit().click()

      // back to summary
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })

    test('Given I confirm the totals and am on the summary, When I edit and change an answer that has a dependent minimum value from a calculated summary total, And the minimum value has been changed, Then I must re-validate before I get to the summary', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const setMinMaxBlockPage = new SetMinMaxBlockPage(page)
      const submitPage = new SubmitPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
      await submitPage.thirdNumberAnswerEdit().click()
      await thirdNumberBlockPage.thirdNumber().fill('10.0')
      await thirdNumberBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(currencyTotalPlaybackPage.pageName))
      await expect(currencyTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of currency values entered to be £15.91. Is this correct?'
      )
      await currencyTotalPlaybackPage.submit().click()
      await expect(page).toHaveURL(new RegExp(setMinMaxBlockPage.pageName))
      await setMinMaxBlockPage.submit().click()
      await expect(setMinMaxBlockPage.errorNumber(1)).toHaveText('Enter an answer more than or equal to £15.91')
      await setMinMaxBlockPage.setMinimum().fill('16.0')
      await setMinMaxBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })

    test('Given I confirm the totals and am on the summary, When I edit and change an answer that has a dependent maximum value from a calculated summary total, And the maximum value has been changed, Then I must re-validate before I get to the summary', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const setMinMaxBlockPage = new SetMinMaxBlockPage(page)
      const submitPage = new SubmitPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
      await submitPage.thirdNumberAnswerEdit().click()
      await thirdNumberBlockPage.thirdNumber().fill('1.0')
      await thirdNumberBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(currencyTotalPlaybackPage.pageName))
      await expect(currencyTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of currency values entered to be £6.91. Is this correct?'
      )
      await currencyTotalPlaybackPage.submit().click()
      await expect(page).toHaveURL(new RegExp(setMinMaxBlockPage.pageName))
      await setMinMaxBlockPage.submit().click()
      await expect(setMinMaxBlockPage.errorNumber(1)).toHaveText('Enter an answer less than or equal to £6.91')
      await setMinMaxBlockPage.setMaximum().fill('6.0')
      await setMinMaxBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })

    test('Given I am on the summary, When I submit the questionnaire, Then I should see the thank you page', async () => {
      const hubPage = new HubPage(page)
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      await submitPage.submit().click()
      await hubPage.submit().click()
      await expect(page).toHaveURL(new RegExp(thankYouPage.pageName))
    })
  })

  test.describe('Given I have a Calculated Summary in a Repeating Section', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Get to Final Summary', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      const hubPage = new HubPage(page)
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      const submitPage = new SubmitPage(page)
      await openQuestionnaire('test_new_calculated_summary_repeating_section.json')
      await hubPage.submit().click()
      await primaryPersonListCollectorPage.no().click()
      await primaryPersonListCollectorPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Jean')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Jane')
      await listCollectorAddPage.lastName().fill('Doe')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await hubPage.submit().click()
      await getToFirstCalculatedSummary(page)
      await getToSubmitPage(page)
      await submitPage.submit().click()
      await hubPage.submit().click()
      await getToFirstCalculatedSummary(page)
      await getToSubmitPage(page)
      await submitPage.submit().click()
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('Given I am on the submit page, When I have completed two repeating sections containing a calculated summary, Then the section status for both repeating sections should be complete', async () => {
      const hubPage = new HubPage(page)
      await expect(page).toHaveURL(new RegExp(hubPage.pageName))
      await expect(hubPage.summaryRowState('personal-details-section-1')).toHaveText('Completed')
      await expect(hubPage.summaryRowState('personal-details-section-2')).toHaveText('Completed')
    })

    test('Given I change an answer with a dependent calculated summary question, When I return to the hub, Then only the section status for the repeating section I updated should be incomplete', async () => {
      const hubPage = new HubPage(page)
      const skipFourthBlockPage = new SkipFourthBlockPage(page)
      const submitPage = new SubmitPage(page)
      await expect(page).toHaveURL(new RegExp(hubPage.pageName))
      await hubPage.summaryRowLink('personal-details-section-1').click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
      await submitPage.skipFourthBlockAnswerEdit().click()
      await skipFourthBlockPage.yes().click()
      await skipFourthBlockPage.submit().click()
      await page.goto(hubPage.url())
      await expect(hubPage.summaryRowState('personal-details-section-1')).toHaveText('Partially completed')
      await expect(hubPage.summaryRowState('personal-details-section-2')).toHaveText('Completed')
    })

    test('Given I return to a partially completed section with a calculated summary, When I answer the dependent questions and return to the hub, Then the section status for the repeating section I updated should be complete', async () => {
      const hubPage = new HubPage(page)
      const setMinMaxBlockPage = new SetMinMaxBlockPage(page)
      const submitPage = new SubmitPage(page)
      await expect(page).toHaveURL(new RegExp(hubPage.pageName))
      await expect(hubPage.summaryRowState('personal-details-section-1')).toHaveText('Partially completed')
      await hubPage.summaryRowLink('personal-details-section-1').click()
      await expect(page).toHaveURL(new RegExp(setMinMaxBlockPage.pageName))
      await setMinMaxBlockPage.setMinimum().fill('10.0')
      await setMinMaxBlockPage.setMaximum().fill('6.0')
      await setMinMaxBlockPage.submit().click()
      await submitPage.submit().click()
      await expect(page).toHaveURL(new RegExp(hubPage.pageName))
      await expect(hubPage.summaryRowState('personal-details-section-1')).toHaveText('Completed')
      await expect(hubPage.summaryRowState('personal-details-section-2')).toHaveText('Completed')
    })
  })

  test.describe('Given I have a Calculated Summary in a Repeating Section with a Dependency based on a calculated summary in another section', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Get to the Dependent question page', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      const calculatedSummarySectionOne = new CalculatedSummarySectionOne(page)
      const calculatedSummarySectionTwo = new CalculatedSummarySectionTwo(page)
      const firstAndAHalfNumberBlockPageSectionOne = new FirstAndAHalfNumberBlockPageSectionOne(page)
      const firstNumberBlockPageSectionOne = new FirstNumberBlockPageSectionOne(page)
      const hubPage = new HubPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      const secondNumberBlockPageSectionOne = new SecondNumberBlockPageSectionOne(page)
      const sectionSummarySectionOne = new SectionSummarySectionOne(page)
      const skipFirstNumberBlockPageSectionOne = new SkipFirstNumberBlockPageSectionOne(page)
      const thirdNumberBlockPageSectionTwo = new ThirdNumberBlockPageSectionTwo(page)
      await openQuestionnaire('test_new_calculated_summary_cross_section_dependencies_repeating.json')
      await hubPage.submit().click()
      await primaryPersonListCollectorPage.yes().click()
      await primaryPersonListCollectorPage.submit().click()
      await primaryPersonListCollectorAddPage.firstName().fill('Marcus')
      await primaryPersonListCollectorAddPage.lastName().fill('Twin')
      await primaryPersonListCollectorAddPage.submit().click()
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
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('Given I have a placeholder displaying a calculated summary value source, When the calculated summary value is from a previous section, Then the value displayed should be correct', async () => {
      const dependencyQuestionSectionTwo = new DependencyQuestionSectionTwo(page)
      await expect(page).toHaveURL(new RegExp(dependencyQuestionSectionTwo.pageName))
      await expect(dependencyQuestionSectionTwo.checkboxAnswerCalcValue1Label()).toHaveText('60 - calculated summary answer (previous section)')
      await expect(dependencyQuestionSectionTwo.checkboxAnswerCalcValue2Label()).toHaveText('40 - calculated summary answer (current section)')
    })

    test('Given I have validation using a calculated summary value source, When the calculated summary value is from a previous section, Then the value used to validate should be correct', async () => {
      const dependencyQuestionSectionTwo = new DependencyQuestionSectionTwo(page)
      const minMaxSectionTwo = new MinMaxSectionTwo(page)
      await dependencyQuestionSectionTwo.checkboxAnswerCalcValue1().click()
      await dependencyQuestionSectionTwo.submit().click()
      await expect(page).toHaveURL(new RegExp(minMaxSectionTwo.pageName))
      await minMaxSectionTwo.setMinimum().fill('59.0')
      await minMaxSectionTwo.setMaximum().fill('1.0')
      await minMaxSectionTwo.submit().click()
      await expect(minMaxSectionTwo.errorNumber(1)).toHaveText('Enter an answer more than or equal to £60.00')
      await minMaxSectionTwo.setMinimum().fill('61.0')
      await minMaxSectionTwo.setMaximum().fill('40.0')
      await minMaxSectionTwo.submit().click()
    })

    test('Given I remove answers from the path for a calculated summary in a previous section by changing an answer, When I return to the question with the calculated summary value source, Then the value displayed should be correct', async () => {
      const dependencyQuestionSectionTwo = new DependencyQuestionSectionTwo(page)
      const hubPage = new HubPage(page)
      const sectionSummarySectionOne = new SectionSummarySectionOne(page)
      const sectionSummarySectionTwo = new SectionSummarySectionTwo(page)
      const skipFirstNumberBlockPageSectionOne = new SkipFirstNumberBlockPageSectionOne(page)
      await sectionSummarySectionTwo.submit().click()
      await hubPage.summaryRowLink('questions-section').click()
      await sectionSummarySectionOne.skipFirstBlockAnswerEdit().click()
      await skipFirstNumberBlockPageSectionOne.yes().click()
      await skipFirstNumberBlockPageSectionOne.submit().click()
      await sectionSummarySectionOne.submit().click()
      await hubPage.summaryRowLink('calculated-summary-section-1').click()
      await expect(page.locator('#main-content')).toContainText('30 - calculated summary answer (previous section)')
      await sectionSummarySectionTwo.checkboxAnswerEdit().click()
      await expect(dependencyQuestionSectionTwo.checkboxAnswerCalcValue1Label()).toHaveText('30 - calculated summary answer (previous section)')
      await expect(dependencyQuestionSectionTwo.checkboxAnswerCalcValue2Label()).toHaveText('40 - calculated summary answer (current section)')
    })
  })
})

const getToFirstCalculatedSummary = async (page: Page): Promise<void> => {
  const firstNumberBlockPage = new FirstNumberBlockPage(page)
  const secondNumberBlockPage = new SecondNumberBlockPage(page)
  const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
  const thirdAndAHalfNumberBlockPage = new ThirdAndAHalfNumberBlockPage(page)
  const skipFourthBlockPage = new SkipFourthBlockPage(page)
  const fourthNumberBlockPage = new FourthNumberBlockPage(page)
  const fourthAndAHalfNumberBlockPage = new FourthAndAHalfNumberBlockPage(page)
  const fifthNumberBlockPage = new FifthNumberBlockPage(page)
  const sixthNumberBlockPage = new SixthNumberBlockPage(page)
  await firstNumberBlockPage.firstNumber().fill('1.23')
  await firstNumberBlockPage.submit().click()

  await secondNumberBlockPage.secondNumber().fill('4.56')
  await secondNumberBlockPage.secondNumberUnitTotal().fill('789')
  await secondNumberBlockPage.secondNumberAlsoInTotal().fill('0.12')
  await secondNumberBlockPage.submit().click()

  await thirdNumberBlockPage.thirdNumber().fill('3.45')
  await thirdNumberBlockPage.submit().click()
  await thirdAndAHalfNumberBlockPage.thirdAndAHalfNumberUnitTotal().fill('678')
  await thirdAndAHalfNumberBlockPage.submit().click()

  await skipFourthBlockPage.no().click()
  await skipFourthBlockPage.submit().click()

  await fourthNumberBlockPage.fourthNumber().fill('9.01')
  await fourthNumberBlockPage.submit().click()
  await fourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal().fill('2.34')
  await fourthAndAHalfNumberBlockPage.submit().click()

  await fifthNumberBlockPage.fifthPercent().fill('56')
  await fifthNumberBlockPage.fifthNumber().fill('78.91')
  await fifthNumberBlockPage.submit().click()

  await sixthNumberBlockPage.sixthPercent().fill('23')
  await sixthNumberBlockPage.sixthNumber().fill('45.67')
  await sixthNumberBlockPage.submit().click()
}

const getToSubmitPage = async (page: Page): Promise<void> => {
  const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
  const unitTotalPlaybackPage = new UnitTotalPlaybackPage(page)
  const percentageTotalPlaybackPage = new PercentageTotalPlaybackPage(page)
  const numberTotalPlaybackPage = new NumberTotalPlaybackPage(page)
  const breakdownPage = new BreakdownPage(page)
  const secondCurrencyTotalPlaybackPage = new SecondCurrencyTotalPlaybackPage(page)
  const calculatedSummaryTotalConfirmation = new CalculatedSummaryTotalConfirmation(page)
  await currencyTotalPlaybackPage.submit().click()
  await unitTotalPlaybackPage.submit().click()
  await percentageTotalPlaybackPage.submit().click()
  await numberTotalPlaybackPage.submit().click()
  await breakdownPage.answer1().fill('100.0')
  await breakdownPage.answer2().fill('24.58')
  await breakdownPage.submit().click()
  await secondCurrencyTotalPlaybackPage.submit().click()
  await calculatedSummaryTotalConfirmation.submit().click()
}
