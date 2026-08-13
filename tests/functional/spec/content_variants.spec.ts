import { test, expect } from '../fixtures/test'
import AgeQuestionBlock from '../generated_pages/variants_content/age-question-block.page'

test.describe('QuestionVariants', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_variants_content.json')
  })

  test('Given I am completing the survey, then the correct content is shown based on my previous answers when i am under 16', async ({ page }) => {
    const ageQuestionBlock = new AgeQuestionBlock(page)
    await ageQuestionBlock.age().fill('12')
    await ageQuestionBlock.submit().click()
    await expect(page.locator('main.ons-page__main h1')).toHaveText('You are 16 or younger')
  })

  test('Given I am completing the survey, then the correct content is shown based on my previous answers when i am over 16', async ({ page }) => {
    const ageQuestionBlock = new AgeQuestionBlock(page)
    await ageQuestionBlock.age().fill('22')
    await ageQuestionBlock.submit().click()
    await expect(page.locator('main.ons-page__main h1')).toHaveText('You are 16 or older')
  })
})
