import { test, expect } from '../../../../fixtures/test'
import YearDatePage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-year-date.page'
import SubmitPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-year-date-section-summary.page'

test.describe('Component: Mutually Exclusive Year Date With Single Checkbox Override', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_mutually_exclusive.json')
    await page.goto('/questionnaire/mutually-exclusive-year-date')
  })

  test.describe('Given the user has entered a value for the non-exclusive year date answer', () => {
    test('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', async ({ page }) => {
      const submitPage = new SubmitPage(page)
      const yearDatePage = new YearDatePage(page)
      await yearDatePage.yearDateYear().fill('2018')
      await expect(yearDatePage.yearDateYear()).toHaveValue('2018')

      await yearDatePage.yearDateExclusiveIPreferNotToSay().click()

      await expect(yearDatePage.yearDateExclusiveIPreferNotToSay()).toBeChecked()
      await expect(yearDatePage.yearDateYear()).toHaveValue('')

      await yearDatePage.submit().click()

      await expect(submitPage.yearDateExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(submitPage.yearDateExclusiveAnswer()).not.toContainText('2018')
    })
  })

  test.describe('Given the user has clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive year date answer and removes focus, Then only the non-exclusive year date answer should be answered.', async ({
      page
    }) => {
      const submitPage = new SubmitPage(page)
      const yearDatePage = new YearDatePage(page)
      await yearDatePage.yearDateExclusiveIPreferNotToSay().click()
      await expect(yearDatePage.yearDateExclusiveIPreferNotToSay()).toBeChecked()

      await yearDatePage.yearDateYear().fill('2018')

      await expect(yearDatePage.yearDateYear()).toHaveValue('2018')
      await expect(yearDatePage.yearDateExclusiveIPreferNotToSay()).not.toBeChecked()

      await yearDatePage.submit().click()

      await expect(submitPage.yearDateAnswer()).toHaveText('2018')
      await expect(submitPage.yearDateAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive year date answer, Then only the non-exclusive year date answer should be answered.', async ({
      page
    }) => {
      const submitPage = new SubmitPage(page)
      const yearDatePage = new YearDatePage(page)
      await expect(yearDatePage.yearDateExclusiveIPreferNotToSay()).not.toBeChecked()

      await yearDatePage.yearDateYear().fill('2018')

      await expect(yearDatePage.yearDateYear()).toHaveValue('2018')
      await expect(yearDatePage.yearDateExclusiveIPreferNotToSay()).not.toBeChecked()

      await yearDatePage.submit().click()

      await expect(submitPage.yearDateAnswer()).toHaveText('2018')
      await expect(submitPage.yearDateAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not answered the non-exclusive year date answer', () => {
    test('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', async ({ page }) => {
      const submitPage = new SubmitPage(page)
      const yearDatePage = new YearDatePage(page)
      await expect(yearDatePage.yearDateYear()).toHaveValue('')

      await yearDatePage.yearDateExclusiveIPreferNotToSay().click()
      await expect(yearDatePage.yearDateExclusiveIPreferNotToSay()).toBeChecked()

      await yearDatePage.submit().click()

      await expect(submitPage.yearDateExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(submitPage.yearDateExclusiveAnswer()).not.toContainText('2018')
    })
  })

  test.describe('Given the user has not answered the question and the question is optional', () => {
    test('When the user clicks the Continue button, Then it should display `No answer provided`', async ({ page }) => {
      const submitPage = new SubmitPage(page)
      const yearDatePage = new YearDatePage(page)
      await expect(yearDatePage.yearDateYear()).toHaveValue('')
      await expect(yearDatePage.yearDateExclusiveIPreferNotToSay()).not.toBeChecked()

      await yearDatePage.submit().click()

      await expect(submitPage.yearDateAnswer()).toHaveText('No answer provided')
    })
  })
})
