import { test, expect } from '../../../fixtures/test'
import CheckboxDropdownPage from '../../../generated_pages/checkbox_detail_answer_dropdown/optional-checkbox-with-dropdown-detail-answer-block.page'
import SubmitPage from '../../../generated_pages/checkbox_detail_answer_dropdown/submit.page'
import DropdownMandatoryPage from '../../../generated_pages/dropdown_mandatory/dropdown-mandatory.page'

test.describe('Optional Checkbox with a Dropdown detail answer', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_checkbox_detail_answer_dropdown.json')
  })

  test.describe('Given an optional checkbox with a dropdown detail answer', () => {
    test('When a placeholder is set for the detail answer, Then that value should be displayed as the first option', async ({ page }) => {
      const checkboxDropdownPage = new CheckboxDropdownPage(page)
      await checkboxDropdownPage.fruit().click()

      await expect(checkboxDropdownPage.fruitDetail()).toContainText('Select fruit')
    })

    test('When a placeholder is not set for the detail answer, Then the default placeholder should be displayed as the first option', async ({ page }) => {
      const checkboxDropdownPage = new CheckboxDropdownPage(page)
      await checkboxDropdownPage.jam().click()

      await expect(checkboxDropdownPage.jamDetail()).toContainText('Select an answer')
    })

    test("When the user does not provide an answer and submits, Then the summary should display 'No answer provided'", async ({ page }) => {
      const checkboxDropdownPage = new CheckboxDropdownPage(page)
      const submitPage = new SubmitPage(page)
      await checkboxDropdownPage.submit().click()

      await expect(submitPage.optionalCheckboxWithDropdownDetailAnswer()).toHaveText('No answer provided')
    })

    test('When the user selects an option with an optional detail answer but does not provide a detail answer, Then the summary should display the chosen option without the detail answer', async ({
      page
    }) => {
      const checkboxDropdownPage = new CheckboxDropdownPage(page)
      const submitPage = new SubmitPage(page)
      await checkboxDropdownPage.fruit().click()
      await checkboxDropdownPage.submit().click()

      await expect(submitPage.optionalCheckboxWithDropdownDetailAnswer()).toHaveText('Fruit')
    })

    test('When the user selects an option with an optional detail answer and provides a detail answer, Then the summary should display the chosen option and the detail answer', async ({
      page
    }) => {
      const checkboxDropdownPage = new CheckboxDropdownPage(page)
      const submitPage = new SubmitPage(page)
      await checkboxDropdownPage.fruit().click()
      await checkboxDropdownPage.fruitDetail().selectOption('Mango')
      await checkboxDropdownPage.submit().click()

      await expect(submitPage.optionalCheckboxWithDropdownDetailAnswer().locator('span')).toHaveText('Fruit')
      await expect(submitPage.optionalCheckboxWithDropdownDetailAnswer().locator('li')).toHaveText('Mango')
    })

    test('When the user selects the default dropdown option after submitting a detail answer, Then the summary should not display the detail answer', async ({
      page
    }) => {
      const checkboxDropdownPage = new CheckboxDropdownPage(page)
      const submitPage = new SubmitPage(page)
      await checkboxDropdownPage.fruit().click()
      await checkboxDropdownPage.fruitDetail().selectOption('Mango')
      await checkboxDropdownPage.submit().click()
      await submitPage.previous().click()
      await checkboxDropdownPage.fruitDetail().selectOption({ label: 'Select fruit' })
      await checkboxDropdownPage.submit().click()

      await expect(submitPage.optionalCheckboxWithDropdownDetailAnswer()).toHaveText('Fruit')
    })

    test('When the user selects an option with an mandatory detail answer but does not provide a detail answer, Then an error should be displayed when the user submits', async ({
      page
    }) => {
      const checkboxDropdownPage = new CheckboxDropdownPage(page)
      const dropdownMandatoryPage = new DropdownMandatoryPage(page)
      await checkboxDropdownPage.jam().click()
      await checkboxDropdownPage.submit().click()

      await expect(dropdownMandatoryPage.errorNumber(1)).toHaveText('Please select the type of Jam')
    })

    test('When the user selects an option with an mandatory detail answer and provides a detail answer, Then the summary should display the chosen option and its details', async ({
      page
    }) => {
      const checkboxDropdownPage = new CheckboxDropdownPage(page)
      const submitPage = new SubmitPage(page)
      await checkboxDropdownPage.jam().click()
      await checkboxDropdownPage.jamDetail().selectOption('Strawberry')
      await checkboxDropdownPage.submit().click()

      await expect(submitPage.optionalCheckboxWithDropdownDetailAnswer().locator('span')).toHaveText('Jam')
      await expect(submitPage.optionalCheckboxWithDropdownDetailAnswer().locator('li')).toHaveText('Strawberry')
    })

    test('When the user removes a previously submitted detail answer, Then the summary should not display the removed detail answer', async ({ page }) => {
      const checkboxDropdownPage = new CheckboxDropdownPage(page)
      const submitPage = new SubmitPage(page)
      await checkboxDropdownPage.fruit().click()
      await checkboxDropdownPage.fruitDetail().selectOption('Mango')
      await checkboxDropdownPage.submit().click()
      await submitPage.previous().click()
      await checkboxDropdownPage.fruit().click()
      await checkboxDropdownPage.submit().click()

      await expect(submitPage.optionalCheckboxWithDropdownDetailAnswer()).toHaveText('No answer provided')
    })

    test('When the user selects multiple options with detail answers and submits, Then the summary should display all the chosen options and their detail answer', async ({
      page
    }) => {
      const checkboxDropdownPage = new CheckboxDropdownPage(page)
      const submitPage = new SubmitPage(page)
      await checkboxDropdownPage.fruit().click()
      await checkboxDropdownPage.fruitDetail().selectOption('Mango')
      await checkboxDropdownPage.jam().click()
      await checkboxDropdownPage.jamDetail().selectOption('Strawberry')
      await checkboxDropdownPage.submit().click()

      const topLevelAnswers = submitPage.optionalCheckboxWithDropdownDetailAnswer().locator(':scope > ul > li')
      await expect(topLevelAnswers.nth(0).locator('span')).toHaveText('Fruit')
      await expect(topLevelAnswers.nth(0).locator('li')).toHaveText('Mango')
      await expect(topLevelAnswers.nth(1).locator('span')).toHaveText('Jam')
      await expect(topLevelAnswers.nth(1).locator('li')).toHaveText('Strawberry')
    })
  })
})
