import { test, expect } from '../../../../fixtures/test'
import TotalAnswerPage from '../../../../generated_pages/validation_sum_against_total_multiple/total-block.page'
import BreakdownAnswerPage from '../../../../generated_pages/validation_sum_against_total_multiple/breakdown-block.page'
import SubmitPage from '../../../../generated_pages/validation_sum_against_total_multiple/submit.page'

test.describe('Feature: Sum validation (Multi Rule Equals)', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_validation_sum_against_total_multiple.json')
  })

  test.describe('Given I start a grouped answer with multi rule validation survey and enter 10 into the total', () => {
    test('When I continue and enter nothing, all zeros or 10 at breakdown level, Then I should be able to get to the summary', async ({ page }) => {
      const breakdownAnswerPage = new BreakdownAnswerPage(page)
      const submitPage = new SubmitPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('10')
      await totalAnswerPage.submit().click()
      await breakdownAnswerPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))

      await submitPage.previous().click()
      await breakdownAnswerPage.breakdown1().fill('0')
      await breakdownAnswerPage.breakdown2().fill('0')
      await breakdownAnswerPage.breakdown3().fill('0')
      await breakdownAnswerPage.breakdown4().fill('0')
      await breakdownAnswerPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))

      await submitPage.previous().click()
      await breakdownAnswerPage.breakdown1().fill('1')
      await breakdownAnswerPage.breakdown2().fill('2')
      await breakdownAnswerPage.breakdown3().fill('3')
      await breakdownAnswerPage.breakdown4().fill('4')
      await breakdownAnswerPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })
  })

  test.describe('Given I start a grouped answer with multi rule validation survey and enter 10 into the total', () => {
    test('When I continue and enter less between 1 - 9 or greater than 10, Then it should error', async ({ page }) => {
      const breakdownAnswerPage = new BreakdownAnswerPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('10')
      await totalAnswerPage.submit().click()
      await breakdownAnswerPage.breakdown1().fill('1')
      await breakdownAnswerPage.submit().click()

      await expect(breakdownAnswerPage.errorNumber(1)).toHaveText('Enter answers that add up to 10')

      await breakdownAnswerPage.breakdown2().fill('2')
      await breakdownAnswerPage.breakdown3().fill('3')
      await breakdownAnswerPage.breakdown4().fill('5')
      await breakdownAnswerPage.submit().click()
      await expect(breakdownAnswerPage.errorNumber(1)).toHaveText('Enter answers that add up to 10')
    })
  })
})
