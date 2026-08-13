import { createOpenQuestionnaire, test, expect } from '../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../fixtures/test'
import SetMinMax from '../generated_pages/numbers/set-min-max-block.page'
import TestMinMax from '../generated_pages/numbers/test-min-max-block.page'
import DetailAnswer from '../generated_pages/numbers/detail-answer-block.page'
import SubmitPage from '../generated_pages/numbers/submit.page'
import CurrencyBlock from '../generated_pages/variants_question/currency-block.page'
import FirstNumberBlock from '../generated_pages/variants_question/first-number-block.page'
import SecondNumberBlock from '../generated_pages/variants_question/second-number-block.page'
import CurrencySectionSummary from '../generated_pages/variants_question/currency-section-summary.page'

test.describe('Number validation', () => {
  test.describe.configure({ mode: 'serial' })

  let context: BrowserContext
  let page: Page
  let openQuestionnaire: OpenQuestionnaire

  test.beforeAll(async ({ browser }) => {
    context = await browser.newContext()
    page = await context.newPage()
    openQuestionnaire = createOpenQuestionnaire(page)
    await openQuestionnaire('test_numbers.json')
  })

  test.afterAll(async () => {
    await context.close()
  })

  test.describe('Given I am completing the test numbers questionnaire,', () => {
    test('When a minimum value with decimals is used and I enter a value less than the minimum, Then the error message includes the minimum value with the decimals values', async () => {
      const setMinMax = new SetMinMax(page)
      await setMinMax.setMinimum().fill('-1000.99')
      await setMinMax.setMaximum().fill('1000')
      await setMinMax.submit().click()
      await expect(setMinMax.errorNumber(1)).toHaveText('Enter an answer more than or equal to -1,000.98')
    })

    test('When a maximum value with decimals is used and I enter a value greater than the maximum, Then the error message includes the minimum value with the decimal values', async () => {
      const setMinMax = new SetMinMax(page)
      await setMinMax.setMinimum().fill('100')
      await setMinMax.setMaximum().fill('10000.99')
      await setMinMax.submit().click()
      await expect(setMinMax.errorNumber(1)).toHaveText('Enter an answer less than or equal to 10,000.98')
    })

    test('When I am on the set minimum and maximum page, Then each field has a label', async () => {
      const setMinMax = new SetMinMax(page)
      await expect(setMinMax.setMinimumLabelDescription()).toHaveText('This is a description of the minimum value')
      await expect(setMinMax.setMaximumLabelDescription()).toHaveText('This is a description of the maximum value')
    })

    test('When I enter values outside of the set range, Then the correct error messages are displayed', async () => {
      const setMinMax = new SetMinMax(page)
      const testMinMax = new TestMinMax(page)
      await setMinMax.setMinimum().fill('10')
      await setMinMax.setMaximum().fill('1020')
      await setMinMax.submit().click()

      await testMinMax.testRange().fill('9')
      await testMinMax.testRangeExclusive().fill('10')
      await testMinMax.testMin().fill('-124')
      await testMinMax.testMax().fill('12345')
      await testMinMax.testMinExclusive().fill('123')
      await testMinMax.testMaxExclusive().fill('12345')
      await testMinMax.testPercent().fill('101')
      await testMinMax.testDecimal().fill('5.4')
      await testMinMax.submit().click()

      await expect(testMinMax.errorNumber(1)).toHaveText('Enter an answer more than or equal to 10')
      await expect(testMinMax.errorNumber(2)).toHaveText('Enter an answer more than 10')
      await expect(testMinMax.errorNumber(3)).toHaveText('Enter an answer more than or equal to -123')
      await expect(testMinMax.errorNumber(4)).toHaveText('Enter an answer less than or equal to 1,234')
      await expect(testMinMax.errorNumber(5)).toHaveText('Enter an answer more than 123')
      await expect(testMinMax.errorNumber(6)).toHaveText('Enter an answer less than 1,234')
      await expect(testMinMax.errorNumber(7)).toHaveText('Enter an answer less than or equal to 100')
      await expect(testMinMax.errorNumber(8)).toHaveText('Enter an answer more than or equal to £10.00')
    })

    test('When I enter values inside the set range but provide too many decimal places, Then the correct error messages are displayed', async () => {
      const testMinMax = new TestMinMax(page)
      await testMinMax.testRange().fill('12.344')
      await testMinMax.testRangeExclusive().fill('11')
      await testMinMax.testMin().fill('123')
      await testMinMax.testMax().fill('1019')
      await testMinMax.testMinExclusive().fill('124')
      await testMinMax.testMaxExclusive().fill('1233')
      await testMinMax.testPercent().fill('100')
      await testMinMax.testRange().fill('12.123456')
      await testMinMax.testDecimal().fill('11.123456')
      await testMinMax.submit().click()

      await expect(testMinMax.errorNumber(1)).toHaveText('Enter a number rounded to 2 decimal places')
      await expect(testMinMax.errorNumber(2)).toHaveText('Enter a number rounded to 5 decimal places')
    })

    test('When I enter values inside the set range, Then I should be able to submit the survey', async () => {
      const currencyBlock = new CurrencyBlock(page)
      const currencySectionSummary = new CurrencySectionSummary(page)
      const detailAnswer = new DetailAnswer(page)
      const firstNumberBlock = new FirstNumberBlock(page)
      const secondNumberBlock = new SecondNumberBlock(page)
      const submitPage = new SubmitPage(page)
      const testMinMax = new TestMinMax(page)
      await testMinMax.testRange().fill('1019')
      await testMinMax.testDecimal().fill('11.10000')
      await testMinMax.testPercent().fill('99')
      await testMinMax.submit().click()
      await detailAnswer.other().click()
      await detailAnswer.otherDetail().fill('1019')
      await testMinMax.submit().click()
      await currencyBlock.usDollars().click()
      await currencyBlock.submit().click()
      await firstNumberBlock.firstNumber().fill('50')
      await firstNumberBlock.submit().click()
      await secondNumberBlock.secondNumber().fill('321')
      await secondNumberBlock.submit().click()
      await currencySectionSummary.submit().click()

      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })

    test('When I edit and change the maximum value, Then I must re-validate and submit any dependent answers before I can return to the summary', async () => {
      const currencySectionSummary = new CurrencySectionSummary(page)
      const detailAnswer = new DetailAnswer(page)
      const secondNumberBlock = new SecondNumberBlock(page)
      const setMinMax = new SetMinMax(page)
      const submitPage = new SubmitPage(page)
      const testMinMax = new TestMinMax(page)
      await submitPage.setMaximumEdit().click()
      await setMinMax.setMaximum().fill('1018')
      await setMinMax.submit().click()
      await testMinMax.testRange().fill('1018')
      await testMinMax.submit().click()
      await detailAnswer.submit().click()

      await expect(detailAnswer.errorNumber(1)).toHaveText('Enter an answer less than or equal to 1,018')

      await detailAnswer.otherDetail().fill('1001')
      await detailAnswer.submit().click()
      await secondNumberBlock.submit().click()
      await currencySectionSummary.submit().click()

      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })

    test('When I edit and change the minimum value, Then I must re-validate and submit any dependent answers again before I can return to the summary', async () => {
      const setMinMax = new SetMinMax(page)
      const submitPage = new SubmitPage(page)
      const testMinMax = new TestMinMax(page)
      await submitPage.setMinimumEdit().click()
      await setMinMax.setMinimum().fill('11')
      await setMinMax.submit().click()
      await testMinMax.submit().click()

      await expect(testMinMax.errorNumber(1)).toHaveText('Enter an answer more than 11')

      await testMinMax.testRangeExclusive().fill('12')
      await testMinMax.submit().click()

      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })

    test('When a number with more than 3 decimal places has been entered, Then it should be displayed correctly on the summary', async () => {
      const submitPage = new SubmitPage(page)
      await expect(submitPage.testDecimal()).toHaveText('£11.10000')
    })
  })
})
