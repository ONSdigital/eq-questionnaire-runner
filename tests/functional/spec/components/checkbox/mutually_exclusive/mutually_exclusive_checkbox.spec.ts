import { test, expect } from '../../../../fixtures/test'
import MandatoryCheckboxPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-checkbox.page'
import SummaryPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-checkbox-section-summary.page'

test.describe('Component: Mutually Exclusive Checkbox With Single Checkbox Override', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_mutually_exclusive.json')
  })

  test.describe('Given the user has clicked multiple non-exclusive options', () => {
    test('When then user clicks the mutually exclusive option, Then only the mutually exclusive option should be checked.', async ({ page }) => {
      const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
      const summaryPage = new SummaryPage(page)
      await mandatoryCheckboxPage.checkboxBritish().click()
      await mandatoryCheckboxPage.checkboxIrish().click()
      await mandatoryCheckboxPage.checkboxOther().click()
      await mandatoryCheckboxPage.checkboxOtherDetail().fill('The other option')

      await expect(mandatoryCheckboxPage.checkboxBritish()).toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxIrish()).toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxOther()).toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxOtherDetail()).toHaveValue('The other option')

      await mandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay().click()
      await expect(mandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).toBeChecked()

      await expect(mandatoryCheckboxPage.checkboxBritish()).not.toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxIrish()).not.toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxOther()).not.toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxOtherDetail()).toHaveValue('')

      await mandatoryCheckboxPage.submit().click()

      await expect(summaryPage.checkboxExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.checkboxExclusiveAnswer()).not.toContainText(/British|Irish/)
    })
  })

  test.describe('Given the user has clicked the mutually exclusive "other" option', () => {
    test('When the user returns to the question, Then the mutually exclusive other option should remain checked.', async ({ page }) => {
      const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
      const summaryPage = new SummaryPage(page)
      await mandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay().click()
      await mandatoryCheckboxPage.submit().click()

      await summaryPage.previous().click()

      await expect(mandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).toBeChecked()
    })
  })

  test.describe('Given the user has clicked the mutually exclusive option', () => {
    test('When the user clicks the non-exclusive options, Then only the non-exclusive options should be checked.', async ({ page }) => {
      const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
      const summaryPage = new SummaryPage(page)
      await mandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay().click()
      await expect(mandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).toBeChecked()

      await mandatoryCheckboxPage.checkboxBritish().click()
      await mandatoryCheckboxPage.checkboxIrish().click()

      await expect(mandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).not.toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxBritish()).toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxIrish()).toBeChecked()

      await mandatoryCheckboxPage.submit().click()

      await expect(summaryPage.checkboxAnswer().locator('li')).toHaveText(['British', 'Irish'])
      await expect(summaryPage.checkboxAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not clicked the mutually exclusive option', () => {
    test('When the user clicks multiple non-exclusive options, Then only the non-exclusive options should be checked.', async ({ page }) => {
      const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
      const summaryPage = new SummaryPage(page)
      await expect(mandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).not.toBeChecked()

      await mandatoryCheckboxPage.checkboxBritish().click()
      await mandatoryCheckboxPage.checkboxIrish().click()

      await expect(mandatoryCheckboxPage.checkboxBritish()).toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxIrish()).toBeChecked()

      await mandatoryCheckboxPage.submit().click()

      await expect(summaryPage.checkboxAnswer().locator('li')).toHaveText(['British', 'Irish'])
      await expect(summaryPage.checkboxAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not clicked any of the non-exclusive options', () => {
    test('When the user clicks the mutually exclusive option, Then only the exclusive option should be checked.', async ({ page }) => {
      const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
      const summaryPage = new SummaryPage(page)
      await expect(mandatoryCheckboxPage.checkboxBritish()).not.toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxIrish()).not.toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxOther()).not.toBeChecked()

      await mandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay().click()
      await expect(mandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).toBeChecked()
      await mandatoryCheckboxPage.submit().click()

      await expect(summaryPage.checkboxExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.checkboxExclusiveAnswer()).not.toContainText(/British|Irish/)
    })
  })

  test.describe('Given the user has not clicked any options and the question is mandatory', () => {
    test('When the user clicks the Continue button, Then a validation error message should be displayed.', async ({ page }) => {
      const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
      await expect(mandatoryCheckboxPage.checkboxBritish()).not.toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxIrish()).not.toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxOther()).not.toBeChecked()
      await expect(mandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).not.toBeChecked()

      await mandatoryCheckboxPage.submit().click()

      await expect(mandatoryCheckboxPage.errorHeader()).toHaveText('There is a problem with your answer')
      await expect(mandatoryCheckboxPage.errorNumber(1)).toContainText('Select at least one answer')
      await expect(mandatoryCheckboxPage.questionErrorPanel()).toBeVisible()
    })
  })
})
