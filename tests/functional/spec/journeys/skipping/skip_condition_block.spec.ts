import { test, expect } from '../../../fixtures/test'
import QuestionPage from '../../../generated_pages/skip_condition_block/do-you-want-to-skip.page'
import SkipPage from '../../../generated_pages/skip_condition_block/should-skip.page'
import SubmitPage from '../../../generated_pages/skip_condition_block/submit.page'

test.describe('Skip Conditions - Block', () => {
  const schema = 'test_skip_condition_block.json'

  test.describe('Given I am completing the test skip condition block survey,', () => {
    test.beforeEach('load the survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire(schema)
    })

    test('When I choose to skip on the first page, Then I should see the summary page', async ({ page }) => {
      const questionPage = new QuestionPage(page)
      const submitPage = new SubmitPage(page)
      await questionPage.yes().click()
      await questionPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })

    test('When I choose not to skip on the first page, Then I should see the should-skip page', async ({ page }) => {
      const questionPage = new QuestionPage(page)
      const skipPage = new SkipPage(page)
      await questionPage.no().click()
      await questionPage.submit().click()
      await expect(page).toHaveURL(new RegExp(skipPage.pageName))
    })
  })
})
