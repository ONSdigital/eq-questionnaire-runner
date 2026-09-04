import { test, expect } from '../../../../fixtures/test'
import DatePage from '../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-date.page'
import SummaryPage from '../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-date-section-summary.page'

test.describe('Component: Mutually Exclusive Day Month Year Date With Multiple Radio Override', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_mutually_exclusive_multiple.json')
    await page.goto('/questionnaire/mutually-exclusive-date')
  })

  test.describe('Given the user has entered a value for the non-exclusive month year date answer', () => {
    test.beforeEach(async ({ page }) => {
      const datePage = new DatePage(page)
      await datePage.dateDay().fill('17')
      await datePage.dateMonth().fill('3')
      await datePage.dateYear().fill('2018')
      await expect(datePage.dateDay()).toHaveValue('17')
      await expect(datePage.dateMonth()).toHaveValue('3')
      await expect(datePage.dateYear()).toHaveValue('2018')
    })

    test('When then user clicks the first mutually exclusive radio answer, Then only the first mutually exclusive radio should be answered.', async ({
      page
    }) => {
      const datePage = new DatePage(page)
      const summaryPage = new SummaryPage(page)
      await datePage.dateExclusiveIPreferNotToSay().click()

      await expect(datePage.dateExclusiveIPreferNotToSay()).toBeChecked()
      await expect(datePage.dateExclusiveIHaveNeverWorked()).not.toBeChecked()
      await expect(datePage.dateDay()).toHaveValue('')
      await expect(datePage.dateMonth()).toHaveValue('')
      await expect(datePage.dateYear()).toHaveValue('')

      await datePage.submit().click()

      await expect(summaryPage.dateExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.dateExclusiveAnswer()).not.toContainText('I have never worked')
      await expect(summaryPage.dateExclusiveAnswer()).not.toContainText('17 March 2018')
    })

    test('When then user clicks the second mutually exclusive radio answer, Then only the second mutually exclusive radio should be answered.', async ({
      page
    }) => {
      const datePage = new DatePage(page)
      const summaryPage = new SummaryPage(page)
      await datePage.dateExclusiveIHaveNeverWorked().click()

      await expect(datePage.dateExclusiveIHaveNeverWorked()).toBeChecked()
      await expect(datePage.dateExclusiveIPreferNotToSay()).not.toBeChecked()
      await expect(datePage.dateDay()).toHaveValue('')
      await expect(datePage.dateMonth()).toHaveValue('')
      await expect(datePage.dateYear()).toHaveValue('')

      await datePage.submit().click()

      await expect(summaryPage.dateExclusiveAnswer()).toHaveText('I have never worked')
      await expect(summaryPage.dateExclusiveAnswer()).not.toContainText('I prefer not to say')
      await expect(summaryPage.dateExclusiveAnswer()).not.toContainText('17 March 2018')
    })
  })

  test.describe('Given the user has clicked the first mutually exclusive radio answer', () => {
    test('When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.', async ({
      page
    }) => {
      const datePage = new DatePage(page)
      const summaryPage = new SummaryPage(page)
      await datePage.dateExclusiveIPreferNotToSay().click()
      await expect(datePage.dateExclusiveIPreferNotToSay()).toBeChecked()
      await expect(datePage.dateExclusiveIHaveNeverWorked()).not.toBeChecked()

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
      await expect(summaryPage.dateAnswer()).not.toContainText('I have never worked')
    })
  })

  test.describe('Given the user has clicked the second mutually exclusive radio answer', () => {
    test('When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.', async ({
      page
    }) => {
      const datePage = new DatePage(page)
      const summaryPage = new SummaryPage(page)
      await datePage.dateExclusiveIHaveNeverWorked().click()
      await expect(datePage.dateExclusiveIHaveNeverWorked()).toBeChecked()
      await expect(datePage.dateExclusiveIPreferNotToSay()).not.toBeChecked()

      await datePage.dateDay().fill('17')
      await datePage.dateMonth().fill('3')
      await datePage.dateYear().fill('2018')

      await expect(datePage.dateDay()).toHaveValue('17')
      await expect(datePage.dateMonth()).toHaveValue('3')
      await expect(datePage.dateYear()).toHaveValue('2018')

      await expect(datePage.dateExclusiveIHaveNeverWorked()).not.toBeChecked()

      await datePage.submit().click()

      await expect(summaryPage.dateAnswer()).toHaveText('17 March 2018')
      await expect(summaryPage.dateAnswer()).not.toContainText('I prefer not to say')
      await expect(summaryPage.dateAnswer()).not.toContainText('I have never worked')
    })
  })

  test.describe('Given the user has not clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive month year date answer, Then only the non-exclusive month year date answer should be answered.', async ({
      page
    }) => {
      const datePage = new DatePage(page)
      const summaryPage = new SummaryPage(page)
      await expect(datePage.dateExclusiveIPreferNotToSay()).not.toBeChecked()
      await expect(datePage.dateExclusiveIHaveNeverWorked()).not.toBeChecked()

      await datePage.dateDay().fill('17')
      await datePage.dateMonth().fill('3')
      await datePage.dateYear().fill('2018')

      await expect(datePage.dateDay()).toHaveValue('17')
      await expect(datePage.dateMonth()).toHaveValue('3')
      await expect(datePage.dateYear()).toHaveValue('2018')
      await expect(datePage.dateExclusiveIPreferNotToSay()).not.toBeChecked()
      await expect(datePage.dateExclusiveIHaveNeverWorked()).not.toBeChecked()

      await datePage.submit().click()
      await expect(summaryPage.dateAnswer()).toHaveText('17 March 2018')
      await expect(summaryPage.dateAnswer()).not.toContainText('I prefer not to say')
      await expect(summaryPage.dateAnswer()).not.toContainText('I have never worked')
    })
  })

  test.describe('Given the user has not answered the non-exclusive month year date answer', () => {
    test.beforeEach(async ({ page }) => {
      const datePage = new DatePage(page)
      await expect(datePage.dateDay()).toHaveValue('')
      await expect(datePage.dateMonth()).toHaveValue('')
      await expect(datePage.dateYear()).toHaveValue('')
    })

    test('When the user clicks the first mutually exclusive radio answer, Then only the first exclusive radio should be answered.', async ({ page }) => {
      const datePage = new DatePage(page)
      const summaryPage = new SummaryPage(page)
      await datePage.dateExclusiveIPreferNotToSay().click()
      await expect(datePage.dateExclusiveIPreferNotToSay()).toBeChecked()
      await expect(datePage.dateExclusiveIHaveNeverWorked()).not.toBeChecked()

      await datePage.submit().click()

      await expect(summaryPage.dateExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.dateExclusiveAnswer()).not.toContainText('I have never worked')
      await expect(summaryPage.dateExclusiveAnswer()).not.toContainText('17 March 2018')
    })

    test('When the user clicks the second mutually exclusive radio answer, Then only the second exclusive radio should be answered.', async ({ page }) => {
      const datePage = new DatePage(page)
      const summaryPage = new SummaryPage(page)
      await datePage.dateExclusiveIHaveNeverWorked().click()
      await expect(datePage.dateExclusiveIHaveNeverWorked()).toBeChecked()
      await expect(datePage.dateExclusiveIPreferNotToSay()).not.toBeChecked()

      await datePage.submit().click()

      await expect(summaryPage.dateExclusiveAnswer()).toHaveText('I have never worked')
      await expect(summaryPage.dateExclusiveAnswer()).not.toContainText('I prefer not to say')
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
      await expect(datePage.dateExclusiveIHaveNeverWorked()).not.toBeChecked()

      await datePage.submit().click()

      await expect(summaryPage.dateAnswer()).toHaveText('No answer provided')
    })
  })

  test.describe('Given the user has clicked a mutually exclusive option', () => {
    test('When the user clicks another mutually exclusive option, Then only the most recently clicked mutually exclusive option should be checked.', async ({
      page
    }) => {
      const datePage = new DatePage(page)
      const summaryPage = new SummaryPage(page)
      await datePage.dateExclusiveIPreferNotToSay().click()
      await expect(datePage.dateExclusiveIPreferNotToSay()).toBeChecked()
      await expect(datePage.dateExclusiveIHaveNeverWorked()).not.toBeChecked()

      await datePage.dateExclusiveIHaveNeverWorked().click()
      await expect(datePage.dateExclusiveIPreferNotToSay()).not.toBeChecked()
      await expect(datePage.dateExclusiveIHaveNeverWorked()).toBeChecked()
      await datePage.submit().click()

      await expect(summaryPage.dateExclusiveAnswer()).toHaveText('I have never worked')
      await expect(summaryPage.dateExclusiveAnswer()).not.toContainText('I prefer not to say')
    })
  })
})
