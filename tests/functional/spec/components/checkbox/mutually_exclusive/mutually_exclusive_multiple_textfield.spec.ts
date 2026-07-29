import { test, expect } from '../../../../fixtures/test'
import TextFieldPage from '../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-textfield.page'
import SummaryPage from '../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-textfield-section-summary.page'

test.describe('Component: Mutually Exclusive Textfield With Multiple Radio Override', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_mutually_exclusive_multiple.json')
    await page.goto('/questionnaire/mutually-exclusive-textfield')
  })

  test.describe('Given the user has entered a value for the non-exclusive textfield answer', () => {
    test.beforeEach(async ({ page }) => {
      const textFieldPage = new TextFieldPage(page)
      await textFieldPage.textfield().fill('Blue')
      await expect(textFieldPage.textfield()).toHaveValue('Blue')
    })

    test('When then user clicks the second mutually exclusive radio answer, Then only the second mutually exclusive radio should be answered.', async ({
      page
    }) => {
      const summaryPage = new SummaryPage(page)
      const textFieldPage = new TextFieldPage(page)
      await textFieldPage.textfieldExclusiveIPreferNotToSay().click()

      await expect(textFieldPage.textfieldExclusiveIPreferNotToSay()).toBeChecked()
      await expect(textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).not.toBeChecked()
      await expect(textFieldPage.textfield()).toHaveValue('')

      await textFieldPage.submit().click()

      await expect(summaryPage.textfieldExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.textfieldExclusiveAnswer()).not.toContainText('I dont have a favorite colour')
      await expect(summaryPage.textfieldExclusiveAnswer()).not.toContainText('Blue')
    })

    test('When then user clicks the first mutually exclusive radio answer, Then only the first mutually exclusive radio should be answered.', async ({
      page
    }) => {
      const summaryPage = new SummaryPage(page)
      const textFieldPage = new TextFieldPage(page)
      await textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour().click()

      await expect(textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).toBeChecked()
      await expect(textFieldPage.textfieldExclusiveIPreferNotToSay()).not.toBeChecked()
      await expect(textFieldPage.textfield()).toHaveValue('')

      await textFieldPage.submit().click()

      await expect(summaryPage.textfieldExclusiveAnswer()).toHaveText('I dont have a favorite colour')
      await expect(summaryPage.textfieldExclusiveAnswer()).not.toContainText('I prefer not to say')
      await expect(summaryPage.textfieldExclusiveAnswer()).not.toContainText('Blue')
    })
  })

  test.describe('Given the user has clicked the first mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive textfield answer and removes focus, Then only the non-exclusive textfield answer should be answered.', async ({
      page
    }) => {
      const summaryPage = new SummaryPage(page)
      const textFieldPage = new TextFieldPage(page)
      await textFieldPage.textfieldExclusiveIPreferNotToSay().click()
      await expect(textFieldPage.textfieldExclusiveIPreferNotToSay()).toBeChecked()
      await expect(textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).not.toBeChecked()

      await textFieldPage.textfield().fill('Blue')

      await expect(textFieldPage.textfield()).toHaveValue('Blue')
      await expect(textFieldPage.textfieldExclusiveIPreferNotToSay()).not.toBeChecked()
      await expect(textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).not.toBeChecked()

      await textFieldPage.submit().click()

      await expect(summaryPage.textfieldAnswer()).toHaveText('Blue')
      await expect(summaryPage.textfieldAnswer()).not.toContainText('I prefer not to say')
      await expect(summaryPage.textfieldAnswer()).not.toContainText('I dont have a favorite colour')
    })
  })

  test.describe('Given the user has clicked the second mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive textfield answer and removes focus, Then only the non-exclusive textfield answer should be answered.', async ({
      page
    }) => {
      const summaryPage = new SummaryPage(page)
      const textFieldPage = new TextFieldPage(page)
      await textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour().click()
      await expect(textFieldPage.textfieldExclusiveIPreferNotToSay()).not.toBeChecked()
      await expect(textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).toBeChecked()

      await textFieldPage.textfield().fill('Blue')

      await expect(textFieldPage.textfield()).toHaveValue('Blue')
      await expect(textFieldPage.textfieldExclusiveIPreferNotToSay()).not.toBeChecked()
      await expect(textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).not.toBeChecked()

      await textFieldPage.submit().click()

      await expect(summaryPage.textfieldAnswer()).toHaveText('Blue')
      await expect(summaryPage.textfieldAnswer()).not.toContainText('I prefer not to say')
      await expect(summaryPage.textfieldAnswer()).not.toContainText('I dont have a favorite colour')
    })
  })

  test.describe('Given the user has not clicked the mutually exclusive checkbox answer', () => {
    test('When the user enters a value for the non-exclusive textfield answer, Then only the non-exclusive textfield answer should be answered.', async ({
      page
    }) => {
      const summaryPage = new SummaryPage(page)
      const textFieldPage = new TextFieldPage(page)
      await expect(textFieldPage.textfieldExclusiveIPreferNotToSay()).not.toBeChecked()
      await expect(textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).not.toBeChecked()

      await textFieldPage.textfield().fill('Blue')

      await expect(textFieldPage.textfield()).toHaveValue('Blue')
      await expect(textFieldPage.textfieldExclusiveIPreferNotToSay()).not.toBeChecked()
      await expect(textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).not.toBeChecked()

      await textFieldPage.submit().click()

      await expect(summaryPage.textfieldAnswer()).toHaveText('Blue')
      await expect(summaryPage.textfieldAnswer()).not.toContainText('I prefer not to say')
      await expect(summaryPage.textfieldAnswer()).not.toContainText('I dont have a favorite colour')
    })
  })

  test.describe('Given the user has not answered the non-exclusive textfield answer', () => {
    test.beforeEach(async ({ page }) => {
      const textFieldPage = new TextFieldPage(page)
      await expect(textFieldPage.textfield()).toHaveValue('')
    })

    test('When the user clicks the first mutually exclusive radio answer, Then only the first exclusive radio should be answered.', async ({ page }) => {
      const summaryPage = new SummaryPage(page)
      const textFieldPage = new TextFieldPage(page)
      await textFieldPage.textfieldExclusiveIPreferNotToSay().click()
      await expect(textFieldPage.textfieldExclusiveIPreferNotToSay()).toBeChecked()
      await expect(textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).not.toBeChecked()

      await textFieldPage.submit().click()

      await expect(summaryPage.textfieldExclusiveAnswer()).toHaveText('I prefer not to say')
      await expect(summaryPage.textfieldExclusiveAnswer()).not.toContainText('I dont have a favorite colour')
      await expect(summaryPage.textfieldExclusiveAnswer()).not.toContainText('Blue')
    })

    test('When the user clicks the second mutually exclusive radio answer, Then only the second exclusive radio should be answered.', async ({ page }) => {
      const summaryPage = new SummaryPage(page)
      const textFieldPage = new TextFieldPage(page)
      await textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour().click()
      await expect(textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).toBeChecked()
      await expect(textFieldPage.textfieldExclusiveIPreferNotToSay()).not.toBeChecked()

      await textFieldPage.submit().click()

      await expect(summaryPage.textfieldExclusiveAnswer()).toHaveText('I dont have a favorite colour')
      await expect(summaryPage.textfieldExclusiveAnswer()).not.toContainText('I prefer not to say')
      await expect(summaryPage.textfieldExclusiveAnswer()).not.toContainText('Blue')
    })
  })

  test.describe('Given the user has not answered the question and the question is optional', () => {
    test('When the user clicks the Continue button, Then it should display `No answer provided`', async ({ page }) => {
      const summaryPage = new SummaryPage(page)
      const textFieldPage = new TextFieldPage(page)
      await expect(textFieldPage.textfield()).toHaveValue('')
      await expect(textFieldPage.textfieldExclusiveIPreferNotToSay()).not.toBeChecked()
      await expect(textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).not.toBeChecked()

      await textFieldPage.submit().click()

      await expect(summaryPage.textfieldAnswer()).toHaveText('No answer provided')
    })
  })

  test.describe('Given the user has clicked a mutually exclusive option', () => {
    test('When the user clicks another mutually exclusive option, Then only the most recently clicked mutually exclusive option should be checked.', async ({
      page
    }) => {
      const summaryPage = new SummaryPage(page)
      const textFieldPage = new TextFieldPage(page)
      await textFieldPage.textfieldExclusiveIPreferNotToSay().click()
      await expect(textFieldPage.textfieldExclusiveIPreferNotToSay()).toBeChecked()
      await expect(textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).not.toBeChecked()

      await textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour().click()
      await expect(textFieldPage.textfieldExclusiveIPreferNotToSay()).not.toBeChecked()
      await expect(textFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).toBeChecked()
      await textFieldPage.submit().click()

      await expect(summaryPage.textfieldExclusiveAnswer()).toHaveText('I dont have a favorite colour')
      await expect(summaryPage.textfieldExclusiveAnswer()).not.toContainText('I prefer not to say')
    })
  })
})
