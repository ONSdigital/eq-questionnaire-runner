import { test, expect } from '../../../../fixtures/test'
import MonthYearDatePage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-month-year-date.page'
import SummaryPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-month-year-date-section-summary.page'

test.describe('Component: Mutually Exclusive Month Year Date With Single Checkbox Override', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_mutually_exclusive.json')
    await page.goto('/questionnaire/mutually-exclusive-month-year-date')
  })

  test.describe('Given the user has entered a value for the non-exclusive month year date answer', () => {
    test('When the user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', async ({ page }) => {
      const monthYearDatePage = new MonthYearDatePage(page)
      const summaryPage = new SummaryPage(page)
      await monthYearDatePage.monthYearDateMonth().fill('3')
      await monthYearDatePage.monthYearDateYear().fill('2018')
      await expect(monthYearDatePage.monthYearDateMonth()).toHaveValue('3')
      await expect(monthYearDatePage.monthYearDateYear()).toHaveValue('2018')

      await monthYearDatePage.monthYearDateExclusiveIPreferNotToSay().click()

      await expect(monthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).toBeChecked()
      await expect(monthYearDatePage.monthYearDateMonth()).toHaveValue('')
      await expect(monthYearDatePage.monthYearDateYear()).toHaveValue('')

      await monthYearDatePage.submit().click()

      await expect(summaryPage.monthYearDateExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.monthYearDateExclusiveAnswer()).not.toContainText('March 2018')
    })
  })

  test.describe('Given the user has clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.', async ({
      page
    }) => {
      const monthYearDatePage = new MonthYearDatePage(page)
      const summaryPage = new SummaryPage(page)
      await monthYearDatePage.monthYearDateExclusiveIPreferNotToSay().click()
      await expect(monthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).toBeChecked()

      await monthYearDatePage.monthYearDateMonth().fill('3')
      await monthYearDatePage.monthYearDateYear().fill('2018')

      await expect(monthYearDatePage.monthYearDateMonth()).toHaveValue('3')
      await expect(monthYearDatePage.monthYearDateYear()).toHaveValue('2018')

      await expect(monthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).not.toBeChecked()

      await monthYearDatePage.submit().click()

      await expect(summaryPage.monthYearDateAnswer()).toHaveText('March 2018')
      await expect(summaryPage.monthYearDateAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive month year date answer, Then only the non-exclusive month year date answer should be answered.', async ({
      page
    }) => {
      const monthYearDatePage = new MonthYearDatePage(page)
      const summaryPage = new SummaryPage(page)
      await expect(monthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).not.toBeChecked()

      await monthYearDatePage.monthYearDateMonth().fill('3')
      await monthYearDatePage.monthYearDateYear().fill('2018')

      await expect(monthYearDatePage.monthYearDateMonth()).toHaveValue('3')
      await expect(monthYearDatePage.monthYearDateYear()).toHaveValue('2018')
      await expect(monthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).not.toBeChecked()

      await monthYearDatePage.submit().click()

      await expect(summaryPage.monthYearDateAnswer()).toHaveText('March 2018')
      await expect(summaryPage.monthYearDateAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not answered the non-exclusive month year date answer', () => {
    test('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', async ({ page }) => {
      const monthYearDatePage = new MonthYearDatePage(page)
      const summaryPage = new SummaryPage(page)
      await expect(monthYearDatePage.monthYearDateMonth()).toHaveValue('')
      await expect(monthYearDatePage.monthYearDateYear()).toHaveValue('')

      await monthYearDatePage.monthYearDateExclusiveIPreferNotToSay().click()
      await expect(monthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).toBeChecked()

      await monthYearDatePage.submit().click()

      await expect(summaryPage.monthYearDateExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.monthYearDateExclusiveAnswer()).not.toContainText('March 2018')
    })
  })

  test.describe('Given the user has not answered the question and the question is optional', () => {
    test('When the user clicks the Continue button, Then it should display `No answer provided`', async ({ page }) => {
      const monthYearDatePage = new MonthYearDatePage(page)
      const summaryPage = new SummaryPage(page)
      await expect(monthYearDatePage.monthYearDateMonth()).toHaveValue('')
      await expect(monthYearDatePage.monthYearDateYear()).toHaveValue('')
      await expect(monthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).not.toBeChecked()

      await monthYearDatePage.submit().click()

      await expect(summaryPage.monthYearDateAnswer()).toHaveText('No answer provided')
    })
  })
})
