import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../fixtures/test'
import CurrencyTotalPlaybackPage from '../../../generated_pages/calculated_summary/currency-total-playback.page'
import UnitTotalPlaybackPage from '../../../generated_pages/calculated_summary/unit-total-playback.page'
import NumberTotalPlaybackPage from '../../../generated_pages/calculated_summary/number-total-playback.page'
import ThirdNumberBlockPage from '../../../generated_pages/calculated_summary/third-number-block.page'
import FourthNumberBlockPage from '../../../generated_pages/calculated_summary/fourth-number-block.page'
import FourthAndAHalfNumberBlockPage from '../../../generated_pages/calculated_summary/fourth-and-a-half-number-block.page'
import SixthNumberBlockPage from '../../../generated_pages/calculated_summary/sixth-number-block.page'
import FifthNumberBlockPage from '../../../generated_pages/calculated_summary/fifth-number-block.page'
import SkipFourthBlockPage from '../../../generated_pages/calculated_summary/skip-fourth-block.page'
import PercentageTotalPlaybackPage from '../../../generated_pages/calculated_summary/percentage-total-playback.page'
import CalculatedSummaryTotalConfirmation from '../../../generated_pages/calculated_summary/calculated-summary-total-confirmation.page'
import SetMinMaxBlockPage from '../../../generated_pages/calculated_summary/set-min-max-block.page'
import SubmitPage from '../../../generated_pages/calculated_summary/submit.page'
import ThirdAndAHalfNumberBlockPage from '../../../generated_pages/calculated_summary/third-and-a-half-number-block.page'
import ThankYouPage from '../../../base_pages/thank-you.page'
import FirstNumberBlockPage from '../../../generated_pages/calculated_summary/first-number-block.page'
import SecondNumberBlockPage from '../../../generated_pages/calculated_summary/second-number-block.page'
import HubPage from '../../../base_pages/hub.page'
import SkipFirstNumberBlockPageSectionOne from '../../../generated_pages/calculated_summary_cross_section_dependencies/skip-first-block.page'
import FirstNumberBlockPageSectionOne from '../../../generated_pages/calculated_summary_cross_section_dependencies/first-number-block.page'
import FirstAndAHalfNumberBlockPageSectionOne from '../../../generated_pages/calculated_summary_cross_section_dependencies/first-and-a-half-number-block.page'
import SecondNumberBlockPageSectionOne from '../../../generated_pages/calculated_summary_cross_section_dependencies/second-number-block.page'
import CalculatedSummarySectionOne from '../../../generated_pages/calculated_summary_cross_section_dependencies/currency-total-playback-1.page'
import CalculatedSummarySectionTwo from '../../../generated_pages/calculated_summary_cross_section_dependencies/currency-total-playback-2.page'
import ThirdNumberBlockPageSectionTwo from '../../../generated_pages/calculated_summary_cross_section_dependencies/third-number-block.page'
import SectionSummarySectionOne from '../../../generated_pages/calculated_summary_cross_section_dependencies/questions-section-summary.page'
import SectionSummarySectionTwo from '../../../generated_pages/calculated_summary_cross_section_dependencies/calculated-summary-section-summary.page'
import DependencyQuestionSectionTwo from '../../../generated_pages/calculated_summary_cross_section_dependencies/mutually-exclusive-checkbox.page'
import MinMaxSectionTwo from '../../../generated_pages/calculated_summary_cross_section_dependencies/set-min-max-block.page'
import { assertSummaryValues, verifyUrlContains } from '../../../helpers'

class TestCase {
  testCase (schema: string): void {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Get to Calculated Summary', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const fifthNumberBlockPage = new FifthNumberBlockPage(page)
      const firstNumberBlockPage = new FirstNumberBlockPage(page)
      const fourthAndAHalfNumberBlockPage = new FourthAndAHalfNumberBlockPage(page)
      const fourthNumberBlockPage = new FourthNumberBlockPage(page)
      const secondNumberBlockPage = new SecondNumberBlockPage(page)
      const sixthNumberBlockPage = new SixthNumberBlockPage(page)
      const skipFourthBlockPage = new SkipFourthBlockPage(page)
      const thirdAndAHalfNumberBlockPage = new ThirdAndAHalfNumberBlockPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await openQuestionnaire(schema)

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

      await verifyUrlContains(page, currencyTotalPlaybackPage.pageName)
    })

    test.afterAll(async () => {
      await context.close()
    })

    test("Given I have completed all questions, When I am on the calculated summary, Then the page title should use the calculation's title", async () => {
      await expect(page).toHaveTitle(/Grand total of previous values - /)
    })

    test('Given I complete every question, When I get to the currency summary, Then I should see the correct total', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const numberTotalPlaybackPage = new NumberTotalPlaybackPage(page)
      const unitTotalPlaybackPage = new UnitTotalPlaybackPage(page)

      await expect(currencyTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of currency values entered to be £20.71. Is this correct?'
      )
      await expect(currencyTotalPlaybackPage.calculatedSummaryQuestion()).toHaveText('Grand total of previous values')
      await expect(currencyTotalPlaybackPage.calculatedSummaryAnswer()).toHaveText('£20.71')

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

      await expect(unitTotalPlaybackPage.secondNumberAnswerUnitTotal()).toHaveCount(0)
      await expect(unitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal()).toHaveCount(0)
      await expect(numberTotalPlaybackPage.fifthNumberAnswer()).toHaveCount(0)
      await expect(numberTotalPlaybackPage.sixthNumberAnswer()).toHaveCount(0)
    })

    test('Given I reach the calculated summary page, Then the Change link url should contain return_to, return_to_answer_id and return_to_block_id query params', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const firstNumberEditHref = await currencyTotalPlaybackPage.firstNumberAnswerEdit().getAttribute('href')
      expect(firstNumberEditHref).toContain(
        '/questionnaire/first-number-block/?return_to=calculated-summary' +
          '&return_to_answer_id=first-number-answer&return_to_block_id=currency-total-playback#first-number-answer'
      )
    })

    test('Given I edit an answer from the calculated summary page and click the Previous button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await currencyTotalPlaybackPage.thirdNumberAnswerEdit().click()
      await thirdNumberBlockPage.previous().click()
      await verifyUrlContains(page, 'currency-total-playback/#third-number-answer')
    })

    test('Given I edit an answer from the calculated summary page and click the Submit button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await currencyTotalPlaybackPage.thirdNumberAnswerEdit().click()
      await thirdNumberBlockPage.submit().click()
      await verifyUrlContains(page, 'currency-total-playback/#third-number-answer')
    })

    test('Given I change an answer, When I get to the currency summary, Then I should see the new total', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const fourthNumberBlockPage = new FourthNumberBlockPage(page)
      await currencyTotalPlaybackPage.fourthNumberAnswerEdit().click()
      await fourthNumberBlockPage.fourthNumber().fill('19.01')
      await fourthNumberBlockPage.submit().click()

      await verifyUrlContains(page, currencyTotalPlaybackPage.pageName)
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

      await verifyUrlContains(page, currencyTotalPlaybackPage.pageName)
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

      await verifyUrlContains(page, currencyTotalPlaybackPage.pageName)
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
      await currencyTotalPlaybackPage.submit().click()
      await expect(unitTotalPlaybackPage.calculatedSummaryTitle()).toHaveText('We calculate the total of unit values entered to be 1,467 cm. Is this correct?')
      await expect(unitTotalPlaybackPage.calculatedSummaryQuestion()).toHaveText('Grand total of previous values')
      await expect(unitTotalPlaybackPage.calculatedSummaryAnswer()).toHaveText('1,467 cm')

      await expect(unitTotalPlaybackPage.secondNumberAnswerUnitTotalLabel()).toHaveText('Second answer label in unit total')
      await expect(unitTotalPlaybackPage.secondNumberAnswerUnitTotal()).toHaveText('789 cm')
      await expect(unitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotalLabel()).toHaveText('Third answer label in unit total')
      await expect(unitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal()).toHaveText('678 cm')
    })

    test('Given the calculated summary has a custom title, When I am on the unit calculated summary, Then the page title should use the custom title', async () => {
      await expect(page).toHaveTitle(/Total Unit Values - /)
    })

    test('Given I complete every question, When I get to the percentage summary, Then I should see the correct total', async () => {
      const percentageTotalPlaybackPage = new PercentageTotalPlaybackPage(page)
      const unitTotalPlaybackPage = new UnitTotalPlaybackPage(page)
      await unitTotalPlaybackPage.submit().click()
      await expect(unitTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of percentage values entered to be 79%. Is this correct?'
      )
      await expect(unitTotalPlaybackPage.calculatedSummaryQuestion()).toHaveText('Grand total of previous values')
      await expect(unitTotalPlaybackPage.calculatedSummaryAnswer()).toHaveText('79%')

      await expect(percentageTotalPlaybackPage.fifthPercentAnswerLabel()).toHaveText('Fifth answer label percentage total')
      await expect(percentageTotalPlaybackPage.fifthPercentAnswer()).toHaveText('56%')
      await expect(percentageTotalPlaybackPage.sixthPercentAnswerLabel()).toHaveText('Sixth answer label percentage total')
      await expect(percentageTotalPlaybackPage.sixthPercentAnswer()).toHaveText('23%')
    })

    test('Given I complete every question, When I get to the number summary, Then I should see the correct total', async () => {
      const numberTotalPlaybackPage = new NumberTotalPlaybackPage(page)
      const unitTotalPlaybackPage = new UnitTotalPlaybackPage(page)
      await unitTotalPlaybackPage.submit().click()
      await expect(unitTotalPlaybackPage.calculatedSummaryTitle()).toHaveText('We calculate the total of number values entered to be 124.58. Is this correct?')
      await expect(unitTotalPlaybackPage.calculatedSummaryQuestion()).toHaveText('Grand total of previous values')
      await expect(unitTotalPlaybackPage.calculatedSummaryAnswer()).toHaveText('124.58')

      await expect(numberTotalPlaybackPage.fifthNumberAnswerLabel()).toHaveText('Fifth answer label number total')
      await expect(numberTotalPlaybackPage.fifthNumberAnswer()).toHaveText('78.91')
      await expect(numberTotalPlaybackPage.sixthNumberAnswerLabel()).toHaveText('Sixth answer label number total')
      await expect(numberTotalPlaybackPage.sixthNumberAnswer()).toHaveText('45.67')
    })

    test('Given I complete every calculated summary, When I go to a page with calculated summary piping, Then I should the see the piped calculated summary total for each summary', async () => {
      const numberTotalPlaybackPage = new NumberTotalPlaybackPage(page)
      await numberTotalPlaybackPage.submit().click()

      const summaryList = page.locator('h1 + ul')
      const textsToAssert = [
        'Total currency values: £9.36',
        'Total unformatted unit values: 1,467',
        'Total formatted unit values: 1,467 cm',
        'Total unformatted percentage values: 79',
        'Total formatted percentage values: 79%',
        'Total number values: 124.58'
      ]

      for (const text of textsToAssert) {
        await expect(summaryList).toContainText(text)
      }
    })

    test(
      'Given I have an answer minimum based on a calculated summary total, ' + 'When I enter an invalid answer, Then I should see an error message on the page',
      async () => {
        const calculatedSummaryTotalConfirmation = new CalculatedSummaryTotalConfirmation(page)
        const setMinMaxBlockPage = new SetMinMaxBlockPage(page)
        await calculatedSummaryTotalConfirmation.submit().click()
        await verifyUrlContains(page, setMinMaxBlockPage.pageName)
        await setMinMaxBlockPage.setMinimum().fill('8.0')
        await setMinMaxBlockPage.submit().click()
        await expect(setMinMaxBlockPage.errorNumber(1)).toHaveText('Enter an answer more than or equal to £9.36')
        await setMinMaxBlockPage.setMinimum().fill('10.0')
        await setMinMaxBlockPage.submit().click()
      }
    )

    test(
      'Given I have an answer maximum based on a calculated summary total, ' + 'When I enter an invalid answer, Then I should see an error message on the page',
      async () => {
        const setMinMaxBlockPage = new SetMinMaxBlockPage(page)
        const submitPage = new SubmitPage(page)
        await submitPage.submit().click()
        await verifyUrlContains(page, setMinMaxBlockPage.pageName)
        await setMinMaxBlockPage.setMaximum().fill('10.0')
        await setMinMaxBlockPage.submit().click()
        await expect(setMinMaxBlockPage.errorNumber(1)).toHaveText('Enter an answer less than or equal to £9.36')
        await setMinMaxBlockPage.setMaximum().fill('7.0')
        await setMinMaxBlockPage.submit().click()
      }
    )

    test('Given I confirm the totals and am on the summary, When I edit and change an answer, Then I must re-confirm the dependant calculated summary page and min max question page before I can return to the summary', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const setMinMaxBlockPage = new SetMinMaxBlockPage(page)
      const submitPage = new SubmitPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await verifyUrlContains(page, submitPage.pageName)
      await submitPage.thirdNumberAnswerEdit().click()
      await thirdNumberBlockPage.thirdNumber().fill('3.5')
      await thirdNumberBlockPage.submit().click()

      await verifyUrlContains(page, currencyTotalPlaybackPage.pageName)
      await expect(currencyTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of currency values entered to be £9.41. Is this correct?'
      )
      await currencyTotalPlaybackPage.submit().click()

      await verifyUrlContains(page, setMinMaxBlockPage.pageName)
      await setMinMaxBlockPage.setMinimum().fill('10.0')
      await setMinMaxBlockPage.setMaximum().fill('9.0')
      await setMinMaxBlockPage.submit().click()

      await verifyUrlContains(page, submitPage.pageName)
    })

    test('Given I confirm the totals and am on the summary, When I edit and change an answer that has a dependent minimum value from a calculated summary total, And the minimum value has been changed, Then I must re-validate before I get to the summary', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const setMinMaxBlockPage = new SetMinMaxBlockPage(page)
      const submitPage = new SubmitPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await verifyUrlContains(page, submitPage.pageName)
      await submitPage.thirdNumberAnswerEdit().click()
      await thirdNumberBlockPage.thirdNumber().fill('10.0')
      await thirdNumberBlockPage.submit().click()
      await verifyUrlContains(page, currencyTotalPlaybackPage.pageName)
      await expect(currencyTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of currency values entered to be £15.91. Is this correct?'
      )
      await currencyTotalPlaybackPage.submit().click()
      await verifyUrlContains(page, setMinMaxBlockPage.pageName)
      await setMinMaxBlockPage.submit().click()
      await expect(setMinMaxBlockPage.errorNumber(1)).toHaveText('Enter an answer more than or equal to £15.91')
      await setMinMaxBlockPage.setMinimum().fill('16.0')
      await setMinMaxBlockPage.submit().click()
      await verifyUrlContains(page, submitPage.pageName)
    })

    test('Given I confirm the totals and am on the summary, When I edit and change an answer that has a dependent maximum value from a calculated summary total, And the maximum value has been changed, Then I must re-validate before I get to the summary', async () => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const setMinMaxBlockPage = new SetMinMaxBlockPage(page)
      const submitPage = new SubmitPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await verifyUrlContains(page, submitPage.pageName)
      await submitPage.thirdNumberAnswerEdit().click()
      await thirdNumberBlockPage.thirdNumber().fill('1.0')
      await thirdNumberBlockPage.submit().click()
      await verifyUrlContains(page, currencyTotalPlaybackPage.pageName)
      await expect(currencyTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total of currency values entered to be £6.91. Is this correct?'
      )
      await currencyTotalPlaybackPage.submit().click()
      await verifyUrlContains(page, setMinMaxBlockPage.pageName)
      await setMinMaxBlockPage.submit().click()
      await expect(setMinMaxBlockPage.errorNumber(1)).toHaveText('Enter an answer less than or equal to £6.91')
      await setMinMaxBlockPage.setMaximum().fill('6.0')
      await setMinMaxBlockPage.submit().click()
      await verifyUrlContains(page, submitPage.pageName)
    })

    test('Given I am on a page with a placeholder containing a calculated summary value, When I have updated the calculated summary so that additional answers are on the path, Then the placeholder should display the updated value', async () => {
      const calculatedSummaryTotalConfirmation = new CalculatedSummaryTotalConfirmation(page)
      const skipFourthBlockPage = new SkipFourthBlockPage(page)
      const submitPage = new SubmitPage(page)
      await submitPage.skipFourthBlockAnswerEdit().click()
      await skipFourthBlockPage.no().click()
      await skipFourthBlockPage.submit().click()
      await submitPage.skipFourthBlockAnswerEdit().click()
      await page.goto(calculatedSummaryTotalConfirmation.url())
      await verifyUrlContains(page, calculatedSummaryTotalConfirmation.pageName)
      const summaryList = page.locator('h1 + ul')
      const textsToAssert = [
        'Total currency values: £25.92',
        'Total unformatted unit values: 1,467',
        'Total formatted unit values: 1,467 cm',
        'Total unformatted percentage values: 79',
        'Total formatted percentage values: 79%',
        'Total number values: 124.58'
      ]

      for (const text of textsToAssert) {
        await expect(summaryList).toContainText(text)
      }
      await page.goto(submitPage.url())
    })

    test('Given I am on a page with a dependent question based on a calculated summary value, When I have updated the calculated summary so that additional answers are on the path, Then the question should display the updated value', async () => {
      const setMinMaxBlockPage = new SetMinMaxBlockPage(page)
      const submitPage = new SubmitPage(page)
      await submitPage.setMinimumAnswerEdit().click()
      await verifyUrlContains(page, setMinMaxBlockPage.pageName)
      await expect(setMinMaxBlockPage.questionTitle()).toContainText('Set minimum and maximum values based on your calculated summary total of £25.92')
      await setMinMaxBlockPage.submit().click()
      await expect(setMinMaxBlockPage.errorNumber(1)).toHaveText('Enter an answer more than or equal to £25.92')
      await setMinMaxBlockPage.setMinimum().fill('30.0')
      await setMinMaxBlockPage.setMaximum().fill('6.0')
      await setMinMaxBlockPage.submit().click()
    })

    test('Given I am on the summary, When I submit the questionnaire, Then I should see the thank you page', async () => {
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      await submitPage.submit().click()
      await verifyUrlContains(page, thankYouPage.pageName)
    })
  }

  testCrossSectionDependencies (schema: string): void {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Get to the question containing calculated summary values with cross section dependencies', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      const calculatedSummarySectionOne = new CalculatedSummarySectionOne(page)
      const calculatedSummarySectionTwo = new CalculatedSummarySectionTwo(page)
      const firstAndAHalfNumberBlockPageSectionOne = new FirstAndAHalfNumberBlockPageSectionOne(page)
      const firstNumberBlockPageSectionOne = new FirstNumberBlockPageSectionOne(page)
      const hubPage = new HubPage(page)
      const secondNumberBlockPageSectionOne = new SecondNumberBlockPageSectionOne(page)
      const sectionSummarySectionOne = new SectionSummarySectionOne(page)
      const skipFirstNumberBlockPageSectionOne = new SkipFirstNumberBlockPageSectionOne(page)
      const thirdNumberBlockPageSectionTwo = new ThirdNumberBlockPageSectionTwo(page)
      await openQuestionnaire(schema)
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
      await verifyUrlContains(page, dependencyQuestionSectionTwo.pageName)
      await expect(dependencyQuestionSectionTwo.checkboxAnswerCalcValue1Label()).toHaveText('60 - calculated summary answer (previous section)')
      await expect(dependencyQuestionSectionTwo.checkboxAnswerCalcValue2Label()).toHaveText('40 - calculated summary answer (current section)')
    })

    test('Given I have validation using a calculated summary value source, When the calculated summary value is from a previous section, Then the value used to validate should be correct', async () => {
      const dependencyQuestionSectionTwo = new DependencyQuestionSectionTwo(page)
      const minMaxSectionTwo = new MinMaxSectionTwo(page)
      await dependencyQuestionSectionTwo.checkboxAnswerCalcValue1().click()
      await dependencyQuestionSectionTwo.submit().click()
      await verifyUrlContains(page, minMaxSectionTwo.pageName)
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
      await hubPage.summaryRowLink('calculated-summary-section').click()
      await expect(page.locator('main')).toContainText('30 - calculated summary answer (previous section)')
      await sectionSummarySectionTwo.checkboxAnswerEdit().click()
      await expect(dependencyQuestionSectionTwo.checkboxAnswerCalcValue1Label()).toHaveText('30 - calculated summary answer (previous section)')
      await expect(dependencyQuestionSectionTwo.checkboxAnswerCalcValue2Label()).toHaveText('40 - calculated summary answer (current section)')
    })
  }

  testNegative (
    schema: string,
    firstAnswerValue: number,
    secondAnswerValue: number,
    thirdAnswerValue: number,
    fourthAnswerValue: number,
    expectedTotalValue: string,
    expectedAnswerValues: string[]
  ): void {
    test.beforeEach('Get to Calculated Summary', async ({ page, openQuestionnaire }) => {
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const fifthNumberBlockPage = new FifthNumberBlockPage(page)
      const firstNumberBlockPage = new FirstNumberBlockPage(page)
      const fourthAndAHalfNumberBlockPage = new FourthAndAHalfNumberBlockPage(page)
      const fourthNumberBlockPage = new FourthNumberBlockPage(page)
      const secondNumberBlockPage = new SecondNumberBlockPage(page)
      const sixthNumberBlockPage = new SixthNumberBlockPage(page)
      const skipFourthBlockPage = new SkipFourthBlockPage(page)
      const thirdAndAHalfNumberBlockPage = new ThirdAndAHalfNumberBlockPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await openQuestionnaire(schema)

      await firstNumberBlockPage.firstNumber().fill(`${firstAnswerValue}`)
      await firstNumberBlockPage.submit().click()

      await secondNumberBlockPage.secondNumber().fill(`${secondAnswerValue}`)
      await secondNumberBlockPage.secondNumberUnitTotal().fill('789')
      await secondNumberBlockPage.secondNumberAlsoInTotal().fill('0')
      await secondNumberBlockPage.submit().click()

      await thirdNumberBlockPage.thirdNumber().fill(`${thirdAnswerValue}`)
      await thirdNumberBlockPage.submit().click()
      await thirdAndAHalfNumberBlockPage.thirdAndAHalfNumberUnitTotal().fill('678')
      await thirdAndAHalfNumberBlockPage.submit().click()

      await skipFourthBlockPage.no().click()
      await skipFourthBlockPage.submit().click()

      await fourthNumberBlockPage.fourthNumber().fill(`${fourthAnswerValue}`)
      await fourthNumberBlockPage.submit().click()
      await fourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal().fill('0')
      await fourthAndAHalfNumberBlockPage.submit().click()

      await fifthNumberBlockPage.fifthPercent().fill('56')
      await fifthNumberBlockPage.fifthNumber().fill('78.91')
      await fifthNumberBlockPage.submit().click()

      await sixthNumberBlockPage.sixthPercent().fill('23')
      await sixthNumberBlockPage.sixthNumber().fill('45')
      await sixthNumberBlockPage.submit().click()

      await verifyUrlContains(page, currencyTotalPlaybackPage.pageName)
    })

    test(
      'Given I have entered a range of positive and negative values, ' + 'When I reach the calculated summary, Then the total is correct',
      async ({ page }) => {
        const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
        await assertSummaryValues(page, expectedAnswerValues)
        await expect(currencyTotalPlaybackPage.calculatedSummaryTitle()).toHaveText(
          `We calculate the total of currency values entered to be ${expectedTotalValue}. Is this correct?`
        )
      }
    )
  }
}

export const CalculatedSummaryTestCase = new TestCase()
