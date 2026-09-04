import { test, expect } from '../../../fixtures/test'
import RadioDropdownPage from '../../../generated_pages/radio_detail_answer_dropdown/optional-radio-with-dropdown-detail-answer-block.page'
import SubmitPage from '../../../generated_pages/radio_detail_answer_dropdown/submit.page'
import DropdownMandatoryPage from '../../../generated_pages/dropdown_mandatory/dropdown-mandatory.page'

test.describe('Optional Radio with a Dropdown detail answer', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_radio_detail_answer_dropdown.json')
  })

  test.describe('Given an optional radio with a dropdown detail answer', () => {
    test('When a placeholder is set for the detail answer, Then that value should be displayed as the first option', async ({ page }) => {
      const radioDropdownPage = new RadioDropdownPage(page)
      await radioDropdownPage.fruit().click()

      await expect(radioDropdownPage.fruitDetail()).toContainText('Select fruit')
    })

    test('When a placeholder is not set for the detail answer, Then the default placeholder should be displayed as the first option', async ({ page }) => {
      const radioDropdownPage = new RadioDropdownPage(page)
      await radioDropdownPage.jam().click()

      await expect(radioDropdownPage.jamDetail()).toContainText('Select an answer')
    })

    test("When the user does not provide an answer and submits, Then the summary should display 'No answer provided'", async ({ page }) => {
      const radioDropdownPage = new RadioDropdownPage(page)
      const submitPage = new SubmitPage(page)
      await radioDropdownPage.submit().click()

      await expect(submitPage.optionalRadioWithDropdownDetailAnswer()).toHaveText('No answer provided')
    })

    test('When the user selects an option with an optional detail answer but does not provide a detail answer, Then the summary should display the chosen option without the detail answer', async ({
      page
    }) => {
      const radioDropdownPage = new RadioDropdownPage(page)
      const submitPage = new SubmitPage(page)
      await radioDropdownPage.fruit().click()
      await radioDropdownPage.submit().click()

      await expect(submitPage.optionalRadioWithDropdownDetailAnswer()).toHaveText('Fruit')
    })

    test('When the user selects an option with an optional detail answer and provides a detail answer, Then the summary should display the chosen option and the detail answer', async ({
      page
    }) => {
      const radioDropdownPage = new RadioDropdownPage(page)
      const submitPage = new SubmitPage(page)
      await radioDropdownPage.fruit().click()
      await radioDropdownPage.fruitDetail().selectOption('Mango')
      await radioDropdownPage.submit().click()

      await expect(submitPage.optionalRadioWithDropdownDetailAnswer().locator('span')).toHaveText('Fruit')
      await expect(submitPage.optionalRadioWithDropdownDetailAnswer().locator('li')).toHaveText('Mango')
    })

    test('When the user selects the default dropdown option after submitting a detail answer, Then the summary should not display the detail answer', async ({
      page
    }) => {
      const radioDropdownPage = new RadioDropdownPage(page)
      const submitPage = new SubmitPage(page)
      await radioDropdownPage.fruit().click()
      await radioDropdownPage.fruitDetail().selectOption('Mango')
      await radioDropdownPage.submit().click()
      await submitPage.previous().click()
      await radioDropdownPage.fruitDetail().selectOption({ label: 'Select fruit' })
      await radioDropdownPage.submit().click()

      await expect(submitPage.optionalRadioWithDropdownDetailAnswer()).toHaveText('Fruit')
    })

    test('When the user selects an option with an mandatory detail answer but does not provide a detail answer, Then an error should be displayed when the user submits', async ({
      page
    }) => {
      const dropdownMandatoryPage = new DropdownMandatoryPage(page)
      const radioDropdownPage = new RadioDropdownPage(page)
      await radioDropdownPage.jam().click()
      await radioDropdownPage.submit().click()

      await expect(dropdownMandatoryPage.errorNumber(1)).toHaveText('Please select the type of Jam')
    })

    test('When the user selects an option with an mandatory detail answer and provides a detail answer, Then the summary should display the chosen option and its detail answer', async ({
      page
    }) => {
      const radioDropdownPage = new RadioDropdownPage(page)
      const submitPage = new SubmitPage(page)
      await radioDropdownPage.jam().click()
      await radioDropdownPage.jamDetail().selectOption('Strawberry')
      await radioDropdownPage.submit().click()

      await expect(submitPage.optionalRadioWithDropdownDetailAnswer().locator('span')).toHaveText('Jam')
      await expect(submitPage.optionalRadioWithDropdownDetailAnswer().locator('li')).toHaveText('Strawberry')
    })

    test('When the user removes a previously submitted detail answer by selecting another radio option, Then the summary should only display the new radio option', async ({
      page
    }) => {
      const radioDropdownPage = new RadioDropdownPage(page)
      const submitPage = new SubmitPage(page)
      await radioDropdownPage.jam().click()
      await radioDropdownPage.jamDetail().selectOption('Raspberry')
      await radioDropdownPage.submit().click()
      await submitPage.previous().click()
      await radioDropdownPage.fruit().click()
      await radioDropdownPage.submit().click()

      await expect(submitPage.optionalRadioWithDropdownDetailAnswer()).toHaveText('Fruit')
    })
  })
})
