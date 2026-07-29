import { test, expect } from '../../../../fixtures/test'
import NumberPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-number.page'
import SummaryPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-number-section-summary.page'

test.describe('Component: Mutually Exclusive Number With Single Checkbox Override', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_mutually_exclusive.json')
    await page.goto('/questionnaire/mutually-exclusive-number')
  })

  test.describe('Given the user has entered a value for the non-exclusive number answer', () => {
    test('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', async ({ page }) => {
      const numberPage = new NumberPage(page)
      const summaryPage = new SummaryPage(page)
      await numberPage.number().fill('123')
      await expect(numberPage.number()).toHaveValue('123')

      await numberPage.numberExclusiveIPreferNotToSay().click()

      await expect(numberPage.numberExclusiveIPreferNotToSay()).toBeChecked()
      await expect(numberPage.number()).toHaveValue('')

      await numberPage.submit().click()

      await expect(summaryPage.numberExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.numberExclusiveAnswer()).not.toContainText('123')
    })
  })

  test.describe('Given the user has clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive number answer and removes focus, Then only the non-exclusive number answer should be answered.', async ({
      page
    }) => {
      const numberPage = new NumberPage(page)
      const summaryPage = new SummaryPage(page)
      await numberPage.numberExclusiveIPreferNotToSay().click()
      await expect(numberPage.numberExclusiveIPreferNotToSay()).toBeChecked()

      await numberPage.number().fill('123')

      await expect(numberPage.number()).toHaveValue('123')
      await expect(numberPage.numberExclusiveIPreferNotToSay()).not.toBeChecked()

      await numberPage.submit().click()

      await expect(summaryPage.numberAnswer()).toHaveText('123')
      await expect(summaryPage.numberAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive number answer, Then only the non-exclusive number answer should be answered.', async ({
      page
    }) => {
      const numberPage = new NumberPage(page)
      const summaryPage = new SummaryPage(page)
      await expect(numberPage.numberExclusiveIPreferNotToSay()).not.toBeChecked()

      await numberPage.number().fill('123')

      await expect(numberPage.number()).toHaveValue('123')
      await expect(numberPage.numberExclusiveIPreferNotToSay()).not.toBeChecked()

      await numberPage.submit().click()

      await expect(summaryPage.numberAnswer()).toHaveText('123')
      await expect(summaryPage.numberAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not answered the non-exclusive number answer', () => {
    test('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', async ({ page }) => {
      const numberPage = new NumberPage(page)
      const summaryPage = new SummaryPage(page)
      await expect(numberPage.number()).toHaveValue('')

      await numberPage.numberExclusiveIPreferNotToSay().click()
      await expect(numberPage.numberExclusiveIPreferNotToSay()).toBeChecked()

      await numberPage.submit().click()

      await expect(summaryPage.numberExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.numberExclusiveAnswer()).not.toContainText('123')
    })
  })

  test.describe('Given the user has not answered the question and the question is optional', () => {
    test('When the user clicks the Continue button, Then it should display `No answer provided`', async ({ page }) => {
      const numberPage = new NumberPage(page)
      const summaryPage = new SummaryPage(page)
      await expect(numberPage.number()).toHaveValue('')
      await expect(numberPage.numberExclusiveIPreferNotToSay()).not.toBeChecked()

      await numberPage.submit().click()

      await expect(summaryPage.numberAnswer()).toHaveText('No answer provided')
    })
  })
})
