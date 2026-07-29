import { test, expect } from '../../../../fixtures/test'
import CurrencyPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-currency.page'
import SummaryPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-currency-section-summary.page'

test.describe('Component: Mutually Exclusive Currency With Single Checkbox Override', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_mutually_exclusive.json')
    await page.goto('/questionnaire/mutually-exclusive-currency')
  })

  test.describe('Given the user has entered a value for the non-exclusive currency answer', () => {
    test('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', async ({ page }) => {
      const currencyPage = new CurrencyPage(page)
      const summaryPage = new SummaryPage(page)
      await currencyPage.currency().fill('123')
      await expect(currencyPage.currency()).toHaveValue('123')

      await currencyPage.currencyExclusiveIPreferNotToSay().click()

      await expect(currencyPage.currencyExclusiveIPreferNotToSay()).toBeChecked()
      await expect(currencyPage.currency()).toHaveValue('')

      await currencyPage.submit().click()

      await expect(summaryPage.currencyExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.currencyExclusiveAnswer()).not.toContainText('123')
    })
  })

  test.describe('Given the user has clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive currency answer and removes focus, Then only the non-exclusive currency answer should be answered.', async ({
      page
    }) => {
      const currencyPage = new CurrencyPage(page)
      const summaryPage = new SummaryPage(page)
      await currencyPage.currencyExclusiveIPreferNotToSay().click()
      await expect(currencyPage.currencyExclusiveIPreferNotToSay()).toBeChecked()

      await currencyPage.currency().fill('123')

      await currencyPage.currency().inputValue()
      await expect(currencyPage.currencyExclusiveIPreferNotToSay()).not.toBeChecked()

      await currencyPage.submit().click()

      await expect(summaryPage.currencyAnswer()).toHaveText('£123')
      await expect(summaryPage.currencyAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive currency answer, Then only the non-exclusive currency answer should be answered.', async ({
      page
    }) => {
      const currencyPage = new CurrencyPage(page)
      const summaryPage = new SummaryPage(page)
      await expect(currencyPage.currencyExclusiveIPreferNotToSay()).not.toBeChecked()

      await currencyPage.currency().fill('123')

      await expect(currencyPage.currency()).toHaveValue('123')
      await expect(currencyPage.currencyExclusiveIPreferNotToSay()).not.toBeChecked()

      await currencyPage.submit().click()

      await expect(summaryPage.currencyAnswer()).toHaveText('£123')
      await expect(summaryPage.currencyAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not answered the non-exclusive currency answer', () => {
    test('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', async ({ page }) => {
      const currencyPage = new CurrencyPage(page)
      const summaryPage = new SummaryPage(page)
      await expect(currencyPage.currency()).toHaveValue('')

      await currencyPage.currencyExclusiveIPreferNotToSay().click()
      await expect(currencyPage.currencyExclusiveIPreferNotToSay()).toBeChecked()

      await currencyPage.submit().click()

      await expect(summaryPage.currencyExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.currencyExclusiveAnswer()).not.toContainText('123')
    })
  })

  test.describe('Given the user has not answered the question and the question is optional', () => {
    test('When the user clicks the Continue button, Then it should display `No answer provided`', async ({ page }) => {
      const currencyPage = new CurrencyPage(page)
      const summaryPage = new SummaryPage(page)
      await expect(currencyPage.currency()).toHaveValue('')
      await expect(currencyPage.currencyExclusiveIPreferNotToSay()).not.toBeChecked()

      await currencyPage.submit().click()

      await expect(summaryPage.currencyAnswer()).toHaveText('No answer provided')
    })
  })
})
