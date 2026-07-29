import { test, expect } from '../../../../fixtures/test'
import DurationPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-duration.page'
import SummaryPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-duration-section-summary.page'

test.describe('Component: Mutually Exclusive Duration With Single Checkbox Override', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_mutually_exclusive.json')
    await page.goto('/questionnaire/mutually-exclusive-duration')
  })

  test.describe('Given the user has entered a value for the non-exclusive duration answer', () => {
    test('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', async ({ page }) => {
      const durationPage = new DurationPage(page)
      const summaryPage = new SummaryPage(page)
      await durationPage.durationYears().fill('1')
      await durationPage.durationMonths().fill('7')

      await expect(durationPage.durationYears()).toHaveValue('1')
      await expect(durationPage.durationMonths()).toHaveValue('7')

      await durationPage.durationExclusiveIPreferNotToSay().click()

      await expect(durationPage.durationExclusiveIPreferNotToSay()).toBeChecked()
      await expect(durationPage.durationYears()).toHaveValue('')
      await expect(durationPage.durationMonths()).toHaveValue('')

      await durationPage.submit().click()

      await expect(summaryPage.durationExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.durationExclusiveAnswer()).not.toContainText('1 year 7 months')
    })
  })

  test.describe('Given the user has clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive duration answer and removes focus, Then only the non-exclusive duration answer should be answered.', async ({
      page
    }) => {
      const durationPage = new DurationPage(page)
      const summaryPage = new SummaryPage(page)
      await durationPage.durationExclusiveIPreferNotToSay().click()
      await expect(durationPage.durationExclusiveIPreferNotToSay()).toBeChecked()

      await durationPage.durationYears().fill('1')
      await durationPage.durationMonths().fill('7')

      await expect(durationPage.durationYears()).toHaveValue('1')
      await expect(durationPage.durationMonths()).toHaveValue('7')
      await expect(durationPage.durationExclusiveIPreferNotToSay()).not.toBeChecked()

      await durationPage.submit().click()

      await expect(summaryPage.durationAnswer()).toHaveText('1 year 7 months')
      await expect(summaryPage.durationAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive duration answer, Then only the non-exclusive duration answer should be answered.', async ({
      page
    }) => {
      const durationPage = new DurationPage(page)
      const summaryPage = new SummaryPage(page)
      await expect(durationPage.durationExclusiveIPreferNotToSay()).not.toBeChecked()

      await durationPage.durationYears().fill('1')
      await durationPage.durationMonths().fill('7')

      await expect(durationPage.durationYears()).toHaveValue('1')
      await expect(durationPage.durationMonths()).toHaveValue('7')
      await expect(durationPage.durationExclusiveIPreferNotToSay()).not.toBeChecked()

      await durationPage.submit().click()

      await expect(summaryPage.durationAnswer()).toHaveText('1 year 7 months')
      await expect(summaryPage.durationAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not answered the non-exclusive duration answer', () => {
    test('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', async ({ page }) => {
      const durationPage = new DurationPage(page)
      const summaryPage = new SummaryPage(page)
      await page.goto('/questionnaire/mutually-exclusive-duration')
      await expect(durationPage.durationYears()).toHaveValue('')
      await expect(durationPage.durationMonths()).toHaveValue('')

      await durationPage.durationExclusiveIPreferNotToSay().click()
      await expect(durationPage.durationExclusiveIPreferNotToSay()).toBeChecked()

      await durationPage.submit().click()

      await expect(summaryPage.durationExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.durationExclusiveAnswer()).not.toContainText('1 year 7 months')
    })
  })

  test.describe('Given the user has not answered the question and the question is optional', () => {
    test('When the user clicks the Continue button, Then it should display `No answer provided`', async ({ page }) => {
      const durationPage = new DurationPage(page)
      const summaryPage = new SummaryPage(page)
      await page.goto('/questionnaire/mutually-exclusive-duration')
      await expect(durationPage.durationYears()).toHaveValue('')
      await expect(durationPage.durationMonths()).toHaveValue('')
      await expect(durationPage.durationExclusiveIPreferNotToSay()).not.toBeChecked()

      await durationPage.submit().click()

      await expect(summaryPage.durationAnswer()).toHaveText('No answer provided')
    })
  })
})
