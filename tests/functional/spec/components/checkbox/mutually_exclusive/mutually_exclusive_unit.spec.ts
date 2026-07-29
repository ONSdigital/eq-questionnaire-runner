import { test, expect } from '../../../../fixtures/test'
import UnitPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-unit.page'
import SummaryPage from '../../../../generated_pages/mutually_exclusive/mutually-exclusive-unit-section-summary.page'

test.describe('Component: Mutually Exclusive Unit With Single Checkbox Override', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_mutually_exclusive.json')
    await page.goto('/questionnaire/mutually-exclusive-unit')
  })

  test.describe('Given the user has entered a value for the non-exclusive unit answer', () => {
    test('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', async ({ page }) => {
      const summaryPage = new SummaryPage(page)
      const unitPage = new UnitPage(page)
      await unitPage.unit().fill('10')
      await expect(unitPage.unit()).toHaveValue('10')

      await unitPage.unitExclusiveIPreferNotToSay().click()

      await expect(unitPage.unitExclusiveIPreferNotToSay()).toBeChecked()
      await expect(unitPage.unit()).toHaveValue('')

      await unitPage.submit().click()

      await expect(summaryPage.unitExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.unitExclusiveAnswer()).not.toContainText('10')
    })
  })

  test.describe('Given the user has clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive unit answer and removes focus, Then only the non-exclusive unit answer should be answered.', async ({
      page
    }) => {
      const summaryPage = new SummaryPage(page)
      const unitPage = new UnitPage(page)
      await unitPage.unitExclusiveIPreferNotToSay().click()
      await expect(unitPage.unitExclusiveIPreferNotToSay()).toBeChecked()

      await unitPage.unit().fill('10')

      await expect(unitPage.unit()).toHaveValue(/10/)
      await expect(unitPage.unitExclusiveIPreferNotToSay()).not.toBeChecked()

      await unitPage.submit().click()

      await expect(summaryPage.unitAnswer()).toContainText('10')
      await expect(summaryPage.unitAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive unit answer, Then only the non-exclusive unit answer should be answered.', async ({ page }) => {
      const summaryPage = new SummaryPage(page)
      const unitPage = new UnitPage(page)
      await expect(unitPage.unitExclusiveIPreferNotToSay()).not.toBeChecked()

      await unitPage.unit().fill('10')

      await expect(unitPage.unit()).toHaveValue('10')
      await expect(unitPage.unitExclusiveIPreferNotToSay()).not.toBeChecked()

      await unitPage.submit().click()

      await expect(summaryPage.unitAnswer()).toContainText('10')
      await expect(summaryPage.unitAnswer()).not.toContainText('I prefer not to say')
    })
  })

  test.describe('Given the user has not answered the non-exclusive unit answer', () => {
    test('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', async ({ page }) => {
      const summaryPage = new SummaryPage(page)
      const unitPage = new UnitPage(page)
      await expect(unitPage.unit()).toHaveValue('')

      await unitPage.unitExclusiveIPreferNotToSay().click()
      await expect(unitPage.unitExclusiveIPreferNotToSay()).toBeChecked()

      await unitPage.submit().click()

      await expect(summaryPage.unitExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.unitExclusiveAnswer()).not.toContainText('10')
    })
  })

  test.describe('Given the user has not answered the question and the question is optional', () => {
    test('When the user clicks the Continue button, Then it should display `No answer provided`', async ({ page }) => {
      const summaryPage = new SummaryPage(page)
      const unitPage = new UnitPage(page)
      await expect(unitPage.unit()).toHaveValue('')
      await expect(unitPage.unitExclusiveIPreferNotToSay()).not.toBeChecked()

      await unitPage.submit().click()

      await expect(summaryPage.unitAnswer()).toHaveText('No answer provided')
    })
  })
})
