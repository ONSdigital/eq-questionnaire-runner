import { test, expect } from '../../../fixtures/test'
import DessertBlockPage from '../../../generated_pages/submit_with_summary_custom_submission_text/dessert-block.page'
import SubmitPage from '../../../generated_pages/submit_with_summary_custom_submission_text/submit.page'

test.describe('Summary Screen', () => {
  test.beforeEach('Load the questionnaire', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_submit_with_summary_custom_submission_text.json')
  })

  test('Given a questionnaire with a summary and custom submission content has been completed, Then the correct submission content should be displayed', async ({
    page
  }) => {
    const dessertBlockPage = new DessertBlockPage(page)
    const submitPage = new SubmitPage(page)
    await dessertBlockPage.dessert().fill('Crème Brûlée')
    await dessertBlockPage.submit().click()
    await expect(submitPage.heading()).toHaveText('Submission title')
    await expect(submitPage.warning()).toHaveText('Submission warning')
    await expect(submitPage.guidance()).toHaveText('Submission guidance')
    await expect(submitPage.submit()).toHaveText('Submission button')
  })
})
