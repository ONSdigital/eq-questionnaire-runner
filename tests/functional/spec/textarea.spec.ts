import { test, expect } from '../fixtures/test'
import type { Locator } from '../fixtures/test'
import TextareaBlock from '../generated_pages/textarea/textarea-block.page'
import TextareaSummary from '../generated_pages/textarea/submit.page'

test.describe('Textarea', () => {
  const textareaSchema = 'test_textarea.json'
  const textareaLimit = async (answerLocator: Locator): Promise<string> => {
    const answerId: string | null = await answerLocator.getAttribute('id')
    if (answerId === null || answerId.length === 0) {
      throw new Error('Expected textarea answer to have an id attribute')
    }

    return `#${answerId}-check[data-message-singular]`
  }

  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire(textareaSchema)
  })

  test('Given a textarea option, a user should be able to click the label of the textarea to focus', async ({ page }) => {
    const textareaBlock = new TextareaBlock(page)
    await textareaBlock.answerLabel().click()
    await expect(textareaBlock.answer()).toBeFocused()
  })

  test('Given a textarea option, When no text is entered, Then the summary should display "No answer provided"', async ({ page }) => {
    const textareaBlock = new TextareaBlock(page)
    const textareaSummary = new TextareaSummary(page)
    await textareaBlock.submit().click()
    await expect(textareaSummary.answer()).toHaveText('No answer provided')
  })

  test('Given a textarea option, When some text is entered, Then the summary should display the text', async ({ page }) => {
    const textareaBlock = new TextareaBlock(page)
    const textareaSummary = new TextareaSummary(page)
    await textareaBlock.answer().fill('Some text')
    await textareaBlock.submit().click()
    await expect(textareaSummary.answer()).toHaveText('Some text')
  })

  test('Given a text entered in textarea , When user submits and revisits the textarea, Then the textarea must contain the text entered previously', async ({
    page
  }) => {
    const textareaBlock = new TextareaBlock(page)
    const textareaSummary = new TextareaSummary(page)
    await textareaBlock.answer().fill("'Twenty><&Five'")
    await textareaBlock.submit().click()
    await expect(textareaSummary.answer()).toHaveText("'Twenty><&Five'")
    await textareaSummary.answerEdit().click()
    await textareaBlock.answer().inputValue()
  })

  test('Displays the number of characters remaining', async ({ page }) => {
    const textareaBlock = new TextareaBlock(page)
    const limitSelector = await textareaLimit(textareaBlock.answer())
    await expect(page.locator(limitSelector)).toContainText('20')
  })

  test('Updates the number of characters remaining when the user adds content', async ({ page }) => {
    const textareaBlock = new TextareaBlock(page)
    const limitSelector = await textareaLimit(textareaBlock.answer())
    await textareaBlock.answer().fill('Banjo')
    await expect(page.locator(limitSelector)).toContainText('15')
  })

  test('Displays the number of characters entered over the limit when the user exceeds the character limit', async ({ page }) => {
    const textareaBlock = new TextareaBlock(page)
    const limitSelector = await textareaLimit(textareaBlock.answer())
    await textareaBlock.answer().fill('This sentence is over twenty characters long')
    await expect(page.locator(limitSelector)).toContainText('24')
    await textareaBlock.answer().inputValue()
  })
})
