import { test, expect } from '../../../fixtures/test'
import MandatoryCheckboxPage from '../../../generated_pages/checkbox_detail_answer_multiple/mandatory-checkbox.page'
import SubmitPage from '../../../generated_pages/checkbox_detail_answer_multiple/submit.page'

test.describe('Checkbox with multiple "detail_answer" options', () => {
  const checkboxSchema = 'test_checkbox_detail_answer_multiple.json'

  test('Given detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', async ({
    page,
    openQuestionnaire
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    await openQuestionnaire(checkboxSchema)
    await mandatoryCheckboxPage.yourChoice().click()
    await expect(mandatoryCheckboxPage.yourChoiceDetail()).toBeVisible()
    await mandatoryCheckboxPage.cheese().click()
    await expect(mandatoryCheckboxPage.cheeseDetail()).toBeVisible()
  })

  test('Given a mandatory detail answer, When I select the option but leave the input field empty and submit, Then an error should be displayed.', async ({
    page,
    openQuestionnaire
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    await openQuestionnaire(checkboxSchema)
    // Non-Mandatory detail answer given
    await mandatoryCheckboxPage.cheese().click()
    await mandatoryCheckboxPage.cheeseDetail().fill('Mozzarella')
    // Mandatory detail answer left blank
    await mandatoryCheckboxPage.yourChoice().click()
    await mandatoryCheckboxPage.submit().click()
    await expect(mandatoryCheckboxPage.error()).toBeVisible()
    await expect(mandatoryCheckboxPage.errorNumber(1)).toHaveText('Enter your topping choice to continue')
  })

  test('Given a selected checkbox answer with an error for a mandatory detail answer, When I enter valid value and submit the page, Then the error is cleared and I navigate to next page.', async ({
    page,
    openQuestionnaire
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire(checkboxSchema)
    await mandatoryCheckboxPage.yourChoice().click()
    await mandatoryCheckboxPage.submit().click()
    await expect(mandatoryCheckboxPage.error()).toBeVisible()

    await mandatoryCheckboxPage.yourChoiceDetail().fill('Bacon')
    await mandatoryCheckboxPage.submit().click()
    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
  })

  test('Given a non-mandatory detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', async ({
    page,
    openQuestionnaire
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire(checkboxSchema)
    await mandatoryCheckboxPage.cheese().click()
    await expect(mandatoryCheckboxPage.cheeseDetail()).toBeVisible()
    await mandatoryCheckboxPage.submit().click()
    await expect(submitPage.mandatoryCheckboxAnswer()).toHaveText('Cheese')
  })

  test('Given multiple detail answers, When the user provides text for all, Then that text should be displayed on the summary screen', async ({
    page,
    openQuestionnaire
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire(checkboxSchema)
    await mandatoryCheckboxPage.cheese().click()
    await mandatoryCheckboxPage.cheeseDetail().fill('Mozzarella')
    await mandatoryCheckboxPage.yourChoice().click()
    await mandatoryCheckboxPage.yourChoiceDetail().fill('Bacon')
    await mandatoryCheckboxPage.submit().click()

    const topLevelAnswers = submitPage.mandatoryCheckboxAnswer().locator(':scope > ul > li')
    await expect(topLevelAnswers.nth(0).locator('span')).toHaveText('Cheese')
    await expect(topLevelAnswers.nth(0).locator('li')).toHaveText('Mozzarella')
    await expect(topLevelAnswers.nth(1).locator('span')).toHaveText('Your choice')
    await expect(topLevelAnswers.nth(1).locator('li')).toHaveText('Bacon')
  })

  test('Given multiple detail answers, When the user provides text for just one, Then that text should be displayed on the summary screen', async ({
    page,
    openQuestionnaire
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire(checkboxSchema)
    await mandatoryCheckboxPage.yourChoice().click()
    await mandatoryCheckboxPage.yourChoiceDetail().fill('Bacon')
    await mandatoryCheckboxPage.submit().click()
    await expect(submitPage.mandatoryCheckboxAnswer().locator('span')).toHaveText('Your choice')
    await expect(submitPage.mandatoryCheckboxAnswer().locator('li')).toHaveText('Bacon')
  })

  test('Given I have previously added text in a detail answer and saved, When I uncheck the detail answer option and select a different checkbox, Then the text entered in the detail answer field should be empty.', async ({
    page,
    openQuestionnaire
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire(checkboxSchema)
    await mandatoryCheckboxPage.cheese().click()
    await mandatoryCheckboxPage.cheeseDetail().fill('Mozzarella')
    await mandatoryCheckboxPage.submit().click()
    await submitPage.previous().click()
    await mandatoryCheckboxPage.cheese().click()
    await mandatoryCheckboxPage.ham().click()
    await mandatoryCheckboxPage.submit().click()
    await submitPage.previous().click()
    await mandatoryCheckboxPage.cheese().click()
    await expect(mandatoryCheckboxPage.cheeseDetail()).toHaveValue('')
  })
})
