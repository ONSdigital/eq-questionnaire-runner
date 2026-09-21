import { test, expect } from '../../../../fixtures/test'
import type { Page } from '../../../../fixtures/test'
import TotalAnswerPage from '../../../../generated_pages/validation_sum_against_total_equal/total-block.page'
import BreakdownAnswerPage from '../../../../generated_pages/validation_sum_against_total_equal/breakdown-block.page'
import SubmitPage from '../../../../generated_pages/validation_sum_against_total_equal/submit.page'

const answerAndSubmitBreakdownQuestion = async (page: Page, breakdown1: string, breakdown2: string, breakdown3: string, breakdown4: string): Promise<void> => {
  const breakdownAnswerPage = new BreakdownAnswerPage(page)
  await breakdownAnswerPage.breakdown1().fill(breakdown1)
  await breakdownAnswerPage.breakdown2().fill(breakdown2)
  await breakdownAnswerPage.breakdown3().fill(breakdown3)
  await breakdownAnswerPage.breakdown4().fill(breakdown4)
  await breakdownAnswerPage.submit().click()
}

test.describe('Feature: Sum of grouped answers equal to validation against total ', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_validation_sum_against_total_equal.json')
  })

  test.describe('Given I start a grouped answer validation survey and enter 12 into the total', () => {
    test('When I continue and enter 3 in each breakdown field, Then I should be able to get to the summary', async ({ page }) => {
      const submitPage = new SubmitPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('12')
      await totalAnswerPage.submit().click()

      await answerAndSubmitBreakdownQuestion(page, '3', '3', '3', '3')

      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })
  })

  test.describe('Given I completed a grouped answer validation question and I am on the summary', () => {
    test('When I go back from the summary and change the total, Then I must reconfirm the breakdown question with valid answers before I can get to the summary', async ({
      page
    }) => {
      const breakdownAnswerPage = new BreakdownAnswerPage(page)
      const submitPage = new SubmitPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('12')
      await totalAnswerPage.submit().click()
      await answerAndSubmitBreakdownQuestion(page, '3', '3', '3', '3')

      await submitPage.totalAnswerEdit().click()
      await totalAnswerPage.total().fill('15')
      await totalAnswerPage.submit().click()

      await page.goto(submitPage.url())
      await expect(page).toHaveURL(new RegExp(breakdownAnswerPage.pageName))

      await breakdownAnswerPage.submit().click()
      await expect(breakdownAnswerPage.errorNumber(1)).toHaveText('Enter answers that add up to 15')

      await answerAndSubmitBreakdownQuestion(page, '6', '3', '3', '3')

      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })
  })

  test.describe('Given I start a grouped answer validation survey and enter 5 into the total', () => {
    test('When I continue and enter 5 into breakdown 1 and leave the others empty, Then I should be able to get to the summary', async ({ page }) => {
      const submitPage = new SubmitPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('5')
      await totalAnswerPage.submit().click()
      await answerAndSubmitBreakdownQuestion(page, '5', '', '', '')

      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })
  })

  test.describe('Given I start a grouped answer validation survey and enter 5 into the total', () => {
    test('When I continue and enter 3 in each breakdown field, Then I should see a validation error', async ({ page }) => {
      const breakdownAnswerPage = new BreakdownAnswerPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('5')
      await totalAnswerPage.submit().click()
      await answerAndSubmitBreakdownQuestion(page, '3', '3', '3', '3')

      await expect(breakdownAnswerPage.errorNumber(1)).toHaveText('Enter answers that add up to 5')
    })
  })
})
