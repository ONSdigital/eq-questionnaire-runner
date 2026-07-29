import { test, expect } from '../../../../fixtures/test'
import DatePage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-date.page'
import SummaryPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-date-section-summary.page'

test.describe('Component: Mutually Exclusive Day Month Year Date With Single Checkbox Override', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_mutually_exclusive.json')
    await page.goto('/questionnaire/mutually-exclusive-date')
  })

  test.describe('Given the user has entered a value for the non-exclusive month year date answer', () => {
    test('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', async ({ page }) => {
      const datePage = new DatePage(page)
      const summaryPage = new SummaryPage(page)
      await datePage.dateDay().fill('17')
      await datePage.dateMonth().fill('3')
      await datePage.dateYear().fill('2018')
      await expect(datePage.dateDay()).toHaveValue('17')
      await expect(datePage.dateMonth()).toHaveValue('3')
      await expect(datePage.dateYear()).toHaveValue('2018')

      await datePage.dateExclusiveIPreferNotToSay().click()

      await expect(datePage.dateExclusiveIPreferNotToSay()).toBeChecked()
      await expect(datePage.dateDay()).toHaveValue('')
      await expect(datePage.dateMonth()).toHaveValue('')
      await expect(datePage.dateYear()).toHaveValue('')

      await datePage.submit().click()

      await expect(summaryPage.dateExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.dateExclusiveAnswer()).not.toContainText('17 March 2018')
    })
  })

  test.describe('Given the user has clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.', async ({
      page
    }) => {
      const datePage = new DatePage(page)
      const summaryPage = new SummaryPage(page)
      await datePage.dateExclusiveIPreferNotToSay().click()
      await expect(datePage.dateExclusiveIPreferNotToSay()).toBeChecked()

      await datePage.dateDay().fill('17')
      await datePage.dateMonth().fill('3')
      await datePage.dateYear().fill('2018')

      await expect(datePage.dateDay()).toHaveValue('17')
      await expect(datePage.dateMonth()).toHaveValue('3')
      await expect(datePage.dateYear()).toHaveValue('2018')

      await expect(datePage.dateExclusiveIPreferNotToSay()).not.toBeChecked()

      await datePage.submit().click()

      await expect(summaryPage.dateAnswer()).toHaveText('17 March 2018')
      await expect(summaryPage.dateAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive month year date answer, Then only the non-exclusive month year date answer should be answered.', async ({
      page
    }) => {
      const datePage = new DatePage(page)
      const summaryPage = new SummaryPage(page)
      await expect(datePage.dateExclusiveIPreferNotToSay()).not.toBeChecked()

      await datePage.dateDay().fill('17')
      await datePage.dateMonth().fill('3')
      await datePage.dateYear().fill('2018')

      await expect(datePage.dateDay()).toHaveValue('17')
      await expect(datePage.dateMonth()).toHaveValue('3')
      await expect(datePage.dateYear()).toHaveValue('2018')
      await expect(datePage.dateExclusiveIPreferNotToSay()).not.toBeChecked()

      await datePage.submit().click()
      await expect(summaryPage.dateAnswer()).toHaveText('17 March 2018')
      await expect(summaryPage.dateAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not answered the non-exclusive month year date answer', () => {
    test('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', async ({ page }) => {
      const datePage = new DatePage(page)
      const summaryPage = new SummaryPage(page)
      await expect(datePage.dateDay()).toHaveValue('')
      await expect(datePage.dateMonth()).toHaveValue('')
      await expect(datePage.dateYear()).toHaveValue('')

      await datePage.dateExclusiveIPreferNotToSay().click()
      await expect(datePage.dateExclusiveIPreferNotToSay()).toBeChecked()

      await datePage.submit().click()

      await expect(summaryPage.dateExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.dateExclusiveAnswer()).not.toContainText('17 March 2018')
    })
  })

  test.describe('Given the user has not answered the question and the question is optional', () => {
    test('When the user clicks the Continue button, Then it should display `No answer provided`', async ({ page }) => {
      const datePage = new DatePage(page)
      const summaryPage = new SummaryPage(page)
      await expect(datePage.dateDay()).toHaveValue('')
      await expect(datePage.dateMonth()).toHaveValue('')
      await expect(datePage.dateYear()).toHaveValue('')
      await expect(datePage.dateExclusiveIPreferNotToSay()).not.toBeChecked()

      await datePage.submit().click()

      await expect(summaryPage.dateAnswer()).toHaveText('No answer provided')
    })
  })
})
