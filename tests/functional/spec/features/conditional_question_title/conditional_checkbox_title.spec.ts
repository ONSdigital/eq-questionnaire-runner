import { test, expect } from '../../../fixtures/test'
import CheckBoxPage from '../../../generated_pages/titles_radio_and_checkbox/checkbox-block.page'
import NameEntryPage from '../../../generated_pages/titles_radio_and_checkbox/preamble-block.page'
import RadioButtonsPage from '../../../generated_pages/titles_radio_and_checkbox/radio-block.page'
import SubmitPage from '../../../generated_pages/titles_radio_and_checkbox/submit.page'

test.describe('Feature: Conditional checkbox and radio question titles', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_titles_radio_and_checkbox.json')
  })

  test.describe('Given I start the test_titles_radio_and_checkbox survey', () => {
    test('When I enter an expected name and submit', async ({ page }) => {
      const checkBoxPage = new CheckBoxPage(page)
      const nameEntryPage = new NameEntryPage(page)
      await nameEntryPage.name().fill('Peter')
      await nameEntryPage.submit().click()
      await expect(checkBoxPage.questionText()).toHaveText('Did Peter make changes to this business?')
    })

    test('When I enter an unknown name and go to the checkbox page', async ({ page }) => {
      const checkBoxPage = new CheckBoxPage(page)
      const nameEntryPage = new NameEntryPage(page)
      const radioButtonsPage = new RadioButtonsPage(page)
      await nameEntryPage.name().fill('Fred')
      await nameEntryPage.submit().click()
      await expect(checkBoxPage.questionText()).toHaveText('Did this business make major changes in the following areas?')
      await checkBoxPage.checkboxImplementationOfChangesToMarketingConceptsOrStrategies().click()
      await expect(radioButtonsPage.questionText()).toHaveText('Did this business make major changes in the following areas?')
    })

    test('When I enter another known name page title should include selected title', async ({ page }) => {
      const nameEntryPage = new NameEntryPage(page)
      await nameEntryPage.name().fill('Mary')
      await nameEntryPage.submit().click()

      await expect(page).toHaveTitle('Did Mary make changes to this business? - Test Titles Radio and Checkbox')
    })

    test('When I enter another known name and go to the summary', async ({ page }) => {
      const checkBoxPage = new CheckBoxPage(page)
      const nameEntryPage = new NameEntryPage(page)
      const radioButtonsPage = new RadioButtonsPage(page)
      const submitPage = new SubmitPage(page)
      await nameEntryPage.name().fill('Mary')
      await nameEntryPage.submit().click()
      await expect(checkBoxPage.questionText()).toHaveText('Did Mary make changes to this business?')
      await checkBoxPage.checkboxImplementationOfChangesToMarketingConceptsOrStrategiesLabel().click()
      await checkBoxPage.submit().click()
      await expect(radioButtonsPage.questionText()).toHaveText('Is Mary the boss?')
      await radioButtonsPage.radioMaybe().click()
      await radioButtonsPage.submit().click()
      await expect(submitPage.nameAnswer()).toHaveText('Mary')
      await expect(submitPage.checkboxQuestion()).toHaveText('Did Mary make changes to this business?')
    })
  })
})
