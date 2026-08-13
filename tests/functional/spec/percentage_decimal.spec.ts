import { test, expect } from '../fixtures/test'
import PercentagePage from '../generated_pages/percentage/block.page'
import PercentageDecimalPage from '../generated_pages/percentage/block-decimal.page'
import SubmitPage from '../generated_pages/percentage/submit.page'

test.describe('Decimal places', () => {
  test('Given an answer allows 3 decimal places, When I enter a value to 3 decimal places and return to edit the value, Then the answer should be displayed with 3 decimal places', async ({
    page,
    openQuestionnaire
  }) => {
    const percentageDecimalPage = new PercentageDecimalPage(page)
    const percentagePage = new PercentagePage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire('test_percentage.json')
    await percentagePage.submit().click()
    await percentageDecimalPage.decimal().fill('3.333')
    await percentageDecimalPage.submit().click()
    await submitPage.previous().click()
    await expect(page).toHaveURL(new RegExp(percentageDecimalPage.pageName))
    await expect(percentageDecimalPage.decimal()).toHaveValue('3.333')
  })

  test('Given an answer allows 3 decimal places, When I enter a value to 1 decimal place and return to edit the value, Then the answer should be displayed with 3 decimal places', async ({
    page,
    openQuestionnaire
  }) => {
    const percentageDecimalPage = new PercentageDecimalPage(page)
    const percentagePage = new PercentagePage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire('test_percentage.json')
    await percentagePage.submit().click()
    await percentageDecimalPage.decimal().fill('3.3')
    await percentageDecimalPage.submit().click()
    await submitPage.previous().click()
    await expect(page).toHaveURL(new RegExp(percentageDecimalPage.pageName))
    await expect(percentageDecimalPage.decimal()).toHaveValue('3.300')
  })
})
