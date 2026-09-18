import { test, expect } from '../../../../fixtures/test'
import TotalAnswerPage from '../../../../generated_pages/validation_sum_against_total_less_than/total-block.page'
import BreakdownAnswerPage from '../../../../generated_pages/validation_sum_against_total_less_than/breakdown-block.page'
import SubmitPage from '../../../../generated_pages/validation_sum_against_total_less_than/submit.page'

test.describe('Feature: Sum of grouped answers validation (less than) against total', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_validation_sum_against_total_less_than.json')
  })

  test.describe('Given I start a grouped answer validation survey and enter 12 into the total', () => {
    test('When I continue and enter 2 in each breakdown field, Then I should be able to get to the summary', async ({ page }) => {
      const breakdownAnswerPage = new BreakdownAnswerPage(page)
      const submitPage = new SubmitPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('12')
      await totalAnswerPage.submit().click()
      await breakdownAnswerPage.breakdown1().fill('2')
      await breakdownAnswerPage.breakdown2().fill('2')
      await breakdownAnswerPage.breakdown3().fill('2')
      await breakdownAnswerPage.breakdown4().fill('2')
      await breakdownAnswerPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })
  })

  test.describe('Given I start a grouped answer validation survey and enter 5 into the total', () => {
    test('When I continue and enter 4 into breakdown 1 and leave the others empty, Then I should be able to get to the summary', async ({ page }) => {
      const breakdownAnswerPage = new BreakdownAnswerPage(page)
      const submitPage = new SubmitPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('5')
      await totalAnswerPage.submit().click()
      await breakdownAnswerPage.breakdown1().fill('4')
      await breakdownAnswerPage.breakdown2().fill('')
      await breakdownAnswerPage.breakdown3().fill('')
      await breakdownAnswerPage.breakdown4().fill('')
      await breakdownAnswerPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })
  })

  test.describe('Given I start a grouped answer validation survey and enter 12 into the total', () => {
    test('When I continue and enter 3 in each breakdown field, Then I should see a validation error', async ({ page }) => {
      const breakdownAnswerPage = new BreakdownAnswerPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('12')
      await totalAnswerPage.submit().click()
      await breakdownAnswerPage.breakdown1().fill('3')
      await breakdownAnswerPage.breakdown2().fill('3')
      await breakdownAnswerPage.breakdown3().fill('3')
      await breakdownAnswerPage.breakdown4().fill('3')
      await breakdownAnswerPage.submit().click()
      await expect(breakdownAnswerPage.errorNumber(1)).toHaveText('Enter answers that add up to less than £12.00')
    })
  })

  test.describe('Given I start a grouped answer validation survey and enter 5 into the total', () => {
    test('When I continue and enter 3 in each breakdown field, Then I should see a validation error', async ({ page }) => {
      const breakdownAnswerPage = new BreakdownAnswerPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('5')
      await totalAnswerPage.submit().click()
      await breakdownAnswerPage.breakdown1().fill('3')
      await breakdownAnswerPage.breakdown2().fill('3')
      await breakdownAnswerPage.breakdown3().fill('3')
      await breakdownAnswerPage.breakdown4().fill('3')
      await breakdownAnswerPage.submit().click()
      await expect(breakdownAnswerPage.errorNumber(1)).toHaveText('Enter answers that add up to less than £5.00')
    })
  })
})
