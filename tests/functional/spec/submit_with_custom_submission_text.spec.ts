import { test, expect } from '../fixtures/test'
import BreakfastPage from '../generated_pages/submit_with_custom_submission_text/breakfast.page'
import IntroductionPage from '../generated_pages/submit_with_custom_submission_text/introduction.page'
import SubmitPage from '../base_pages/submit.page'

test.describe('Submit with custom submission text', () => {
  test.beforeEach('Load the questionnaire', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_submit_with_custom_submission_text.json')
  })

  test('Given a questionnaire with custom submission content has been started, when it is completed to the submit page, then the correct submission content should be displayed', async ({
    page
  }) => {
    const breakfastPage = new BreakfastPage(page)
    const introductionPage = new IntroductionPage(page)
    const submitPage = new SubmitPage(page)
    await introductionPage.getStarted().click()
    await breakfastPage.answer().fill('Eggs')
    await breakfastPage.submit().click()
    await expect(submitPage.heading()).toHaveText('Submit your questionnaire')
    await expect(submitPage.warning()).toHaveText('You cannot view your answers after submission')
    await expect(submitPage.guidance()).toHaveText('Thank you for your answers, submit this to complete it')
  })
})
