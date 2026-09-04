import { test, expect } from '../fixtures/test'
import NameBlockPage from '../generated_pages/question_description/name-block.page'
import DescriptionBlockPage from '../generated_pages/optional_guidance_and_description/description-block.page'
import RadioPage from '../generated_pages/optional_guidance_and_description/mandatory-radio.page'
import RadioPageTwo from '../generated_pages/optional_guidance_and_description/mandatory-radio-two.page'
import IntroductionPage from '../generated_pages/question_guidance/introduction.page'
import GuidancePage from '../generated_pages/question_guidance/block-test-guidance-title.page'

test.describe('Question description', () => {
  test('Given a question description has been set in the schema as an array, When it is rendered, Then it is displayed correctly as multiple paragraph attributes', async ({
    page,
    openQuestionnaire
  }) => {
    const nameBlockPage = new NameBlockPage(page)
    await openQuestionnaire('test_question_description.json')
    await expect(nameBlockPage.questionTitle().locator('p')).toHaveText(['Answer the question', 'Go on'])
  })
})

test.describe('Optional question description and guidance', () => {
  test('Given a question description has been set in the schema, When the value to be displayed is None, Then it is not rendered on the page', async ({
    page,
    openQuestionnaire
  }) => {
    const descriptionBlockPage = new DescriptionBlockPage(page)
    const radioPage = new RadioPage(page)
    const radioPageTwo = new RadioPageTwo(page)
    await openQuestionnaire('test_optional_guidance_and_description.json')
    await descriptionBlockPage.submit().click()
    await expect(radioPage.questionTitle()).not.toContainText("''")
    await expect(radioPage.guidance()).not.toBeVisible()
    await radioPage.no().click()
    await radioPage.submit().click()
    await expect(radioPageTwo.questionTitle().locator('li')).toHaveCount(1)
    await expect(radioPageTwo.questionTitle().locator('li')).toHaveText(['List item one'])
  })
})

test.describe('Question guidance', () => {
  test('Given a question guidance with multiple content items, When it is rendered, Then there should only be one guidance box', async ({
    page,
    openQuestionnaire
  }) => {
    const guidancePage = new GuidancePage(page)
    const introductionPage = new IntroductionPage(page)
    await openQuestionnaire('test_question_guidance.json')
    await introductionPage.submit().click()
    await expect(page).toHaveURL(new RegExp(guidancePage.pageName))
    await expect(page.locator('#question-guidance-question-test-guidance-title')).toHaveCount(1)
  })
})
