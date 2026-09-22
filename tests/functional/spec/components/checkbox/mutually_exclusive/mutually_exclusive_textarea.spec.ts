import { test, expect } from '../../../../fixtures/test'
import TextFieldPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-textarea.page'
import SummaryPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-textarea-section-summary.page'

test.describe('Component: Mutually Exclusive TextArea With Single Checkbox Override', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_mutually_exclusive.json')
    await page.goto('/questionnaire/mutually-exclusive-textarea')
  })

  test.describe('Given the user has not clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive textarea answer, Then only the non-exclusive textarea answer should be answered.', async ({
      page
    }) => {
      const summaryPage = new SummaryPage(page)
      const textFieldPage = new TextFieldPage(page)
      await expect(textFieldPage.textareaExclusiveIPreferNotToSay()).not.toBeChecked()

      await textFieldPage.textarea().fill('Blue')

      await expect(textFieldPage.textarea()).toHaveValue('Blue')
      await expect(textFieldPage.textareaExclusiveIPreferNotToSay()).not.toBeChecked()

      await textFieldPage.submit().click()

      await expect(summaryPage.textareaAnswer()).toHaveText('Blue')
      await expect(summaryPage.textareaAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not answered the non-exclusive textarea answer', () => {
    test('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', async ({ page }) => {
      const summaryPage = new SummaryPage(page)
      const textFieldPage = new TextFieldPage(page)
      await expect(textFieldPage.textarea()).toHaveValue('')

      await textFieldPage.textareaExclusiveIPreferNotToSay().click()
      await expect(textFieldPage.textareaExclusiveIPreferNotToSay()).toBeChecked()

      await textFieldPage.submit().click()

      await expect(summaryPage.textareaExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.textareaExclusiveAnswer()).not.toContainText('Blue')
    })
  })

  test.describe('Given the user has not answered the question and the question is optional', () => {
    test('When the user clicks the Continue button, Then it should display `No answer provided`', async ({ page }) => {
      const summaryPage = new SummaryPage(page)
      const textFieldPage = new TextFieldPage(page)
      await expect(textFieldPage.textarea()).toHaveValue('')
      await expect(textFieldPage.textareaExclusiveIPreferNotToSay()).not.toBeChecked()

      await textFieldPage.submit().click()

      await expect(summaryPage.textareaAnswer()).toHaveText('No answer provided')
    })
  })
})
