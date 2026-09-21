import { test, expect } from '../../../fixtures/test'
import BreakfastPage from '../../../generated_pages/submit_with_custom_submission_text/breakfast.page'
import SubmitPage from '../../../base_pages/submit.page'
import IntroductionPage from '../../../base_pages/introduction.page'

test.describe('Given I launch a linear flow questionnaire without summary', () => {
  test.beforeEach('Load the questionnaire', async ({ page, openQuestionnaire }) => {
    const introductionPage = new IntroductionPage(page)
    await openQuestionnaire('test_submit_with_custom_submission_text.json')
    await introductionPage.getStarted().click()
  })

  test('When I complete the questionnaire, then I should be taken to the submit page without a summary', async ({ page }) => {
    const breakfastPage = new BreakfastPage(page)
    const submitPage = new SubmitPage(page)
    await breakfastPage.answer().fill('Bacon')
    await breakfastPage.submit().click()
    await expect(page).toHaveURL(new RegExp(submitPage.url()))
    await expect(submitPage.summary()).not.toBeVisible()
  })

  test('When I complete the questionnaire and submit the questionnaire, then the submission is successful', async ({ page }) => {
    const breakfastPage = new BreakfastPage(page)
    const submitPage = new SubmitPage(page)
    await breakfastPage.submit().click()
    await expect(page).toHaveURL(new RegExp(submitPage.url()))
    await submitPage.submit().click()
  })
})
