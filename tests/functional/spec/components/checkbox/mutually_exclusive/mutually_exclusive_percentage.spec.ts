import { test, expect } from '../../../../fixtures/test'
import PercentagePage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-percentage.page'
import SummaryPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-percentage-section-summary.page'

test.describe('Component: Mutually Exclusive Percentage With Single Checkbox Override', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_mutually_exclusive.json')
    await page.goto('/questionnaire/mutually-exclusive-percentage')
  })

  test.describe('Given the user has entered a value for the non-exclusive percentage answer', () => {
    test('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', async ({ page }) => {
      const percentagePage = new PercentagePage(page)
      const summaryPage = new SummaryPage(page)
      await percentagePage.percentage().fill('99')
      await expect(percentagePage.percentage()).toHaveValue('99')

      await percentagePage.percentageExclusiveIPreferNotToSay().click()

      await expect(percentagePage.percentageExclusiveIPreferNotToSay()).toBeChecked()
      await expect(percentagePage.percentage()).toHaveValue('')

      await percentagePage.submit().click()

      await expect(summaryPage.percentageExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.percentageExclusiveAnswer()).not.toContainText('99')
    })
  })

  test.describe('Given the user has clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive percentage answer and removes focus, Then only the non-exclusive percentage answer should be answered.', async ({
      page
    }) => {
      const percentagePage = new PercentagePage(page)
      const summaryPage = new SummaryPage(page)
      await page.goto('/questionnaire/mutually-exclusive-percentage')
      await percentagePage.percentageExclusiveIPreferNotToSay().click()
      await expect(percentagePage.percentageExclusiveIPreferNotToSay()).toBeChecked()

      await percentagePage.percentage().fill('99')

      await expect(percentagePage.percentage()).toHaveValue('99')
      await expect(percentagePage.percentageExclusiveIPreferNotToSay()).not.toBeChecked()

      await percentagePage.submit().click()

      await expect(summaryPage.percentageAnswer()).toHaveText('99%')
      await expect(summaryPage.percentageAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive percentage answer, Then only the non-exclusive percentage answer should be answered.', async ({
      page
    }) => {
      const percentagePage = new PercentagePage(page)
      const summaryPage = new SummaryPage(page)
      await expect(percentagePage.percentageExclusiveIPreferNotToSay()).not.toBeChecked()

      await percentagePage.percentage().fill('99')

      await expect(percentagePage.percentage()).toHaveValue('99')
      await expect(percentagePage.percentageExclusiveIPreferNotToSay()).not.toBeChecked()

      await percentagePage.submit().click()

      await expect(summaryPage.percentageAnswer()).toHaveText('99%')
      await expect(summaryPage.percentageAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not answered the non-exclusive percentage answer', () => {
    test('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', async ({ page }) => {
      const percentagePage = new PercentagePage(page)
      const summaryPage = new SummaryPage(page)
      await expect(percentagePage.percentage()).toHaveValue('')

      await percentagePage.percentageExclusiveIPreferNotToSay().click()
      await expect(percentagePage.percentageExclusiveIPreferNotToSay()).toBeChecked()

      await percentagePage.submit().click()

      await expect(summaryPage.percentageExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.percentageExclusiveAnswer()).not.toContainText(/British|Irish/)
    })
  })

  test.describe('Given the user has not answered the question and the question is optional', () => {
    test('When the user clicks the Continue button, Then it should display `No answer provided`', async ({ page }) => {
      const percentagePage = new PercentagePage(page)
      const summaryPage = new SummaryPage(page)
      await expect(percentagePage.percentage()).toHaveValue('')
      await expect(percentagePage.percentageExclusiveIPreferNotToSay()).not.toBeChecked()

      await percentagePage.submit().click()

      await expect(summaryPage.percentageAnswer()).toHaveText('No answer provided')
    })
  })
})
