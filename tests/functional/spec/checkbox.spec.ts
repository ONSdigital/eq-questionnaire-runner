import MandatoryCheckboxPage from '../generated_pages/checkbox/mandatory-checkbox.page'
import NonMandatoryCheckboxPage from '../generated_pages/checkbox/non-mandatory-checkbox.page'
import SingleCheckboxPage from '../generated_pages/checkbox/single-checkbox.page'
import SubmitPage from '../generated_pages/checkbox/submit.page'
import { test, expect } from '../fixtures/test'

test.describe('Checkbox with "other" option', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_checkbox.json')
  })

  test('Given a label has not been provided in the schema for a checkbox answer, When the checkbox answer is displayed, Then the default label should be visible', async ({
    page
  }) => {
    await expect(page.locator('#main-content')).toContainText('Select all that apply')
  })

  test('Given a label has been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then the label should be visible', async ({
    page
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)

    await mandatoryCheckboxPage.none().check()
    await mandatoryCheckboxPage.submit().click()

    await expect(page.locator('#main-content')).toContainText('Select any answers that apply')
  })

  test('Given that there is only one checkbox, When the checkbox answer is displayed, Then no label should be present', async ({ page }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const nonMandatoryCheckboxPage = new NonMandatoryCheckboxPage(page)

    await mandatoryCheckboxPage.none().check()
    await mandatoryCheckboxPage.submit().click()
    await nonMandatoryCheckboxPage.submit().click()

    await expect(page.locator('#main-content')).not.toContainText('Select all that apply')
  })

  test('Given an "other" option is available, When the user clicks the "other" option the other input should be visible.', async ({ page }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)

    await expect(mandatoryCheckboxPage.otherLabelDescription()).toHaveText('Choose any other topping')
    await mandatoryCheckboxPage.other().check()
    await expect(mandatoryCheckboxPage.otherDetail()).toBeVisible()
  })

  test('Given a mandatory checkbox answer, When I select the other option, leave the input field empty and submit, Then an error should be displayed.', async ({
    page
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)

    await mandatoryCheckboxPage.other().check()
    await mandatoryCheckboxPage.submit().click()

    await expect(mandatoryCheckboxPage.error()).toBeVisible()
  })

  test('Given a mandatory checkbox answer, When I leave the input field empty and submit, Then the question text should be hidden in the error message using a span element.', async ({
    page
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)

    await mandatoryCheckboxPage.submit().click()

    const hiddenQuestionText = mandatoryCheckboxPage.error().locator('span.ons-u-vh')
    await expect(hiddenQuestionText).toHaveCount(1)
    await expect(hiddenQuestionText).toContainText(/Which pizza toppings would you like\?/)
  })

  test('Given a mandatory checkbox answer, When there is an error on the page for other field and I enter valid value and submit page, Then the error is cleared and I navigate to next page.', async ({
    page
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const nonMandatoryCheckboxPage = new NonMandatoryCheckboxPage(page)

    await mandatoryCheckboxPage.other().check()
    await mandatoryCheckboxPage.submit().click()
    await expect(mandatoryCheckboxPage.error()).toBeVisible()

    await mandatoryCheckboxPage.otherDetail().fill('Other Text')
    await mandatoryCheckboxPage.submit().click()

    await expect(page).toHaveURL(new RegExp(nonMandatoryCheckboxPage.pageName))
  })

  test("Given a non-mandatory checkbox answer, When the user does not select an option, Then 'No answer provided' should be displayed on the summary screen", async ({
    page
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const nonMandatoryCheckboxPage = new NonMandatoryCheckboxPage(page)
    const singleCheckboxPage = new SingleCheckboxPage(page)
    const submitPage = new SubmitPage(page)

    await mandatoryCheckboxPage.other().check()
    await mandatoryCheckboxPage.otherDetail().fill('Other value')
    await mandatoryCheckboxPage.submit().click()
    await nonMandatoryCheckboxPage.submit().click()
    await singleCheckboxPage.submit().click()

    await expect(submitPage.nonMandatoryCheckboxAnswer()).toHaveText('No answer provided')
  })

  test("Given a non-mandatory checkbox answer, When the user selects Other but does not supply a value, Then 'Other' should be displayed on the summary screen", async ({
    page
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const nonMandatoryCheckboxPage = new NonMandatoryCheckboxPage(page)
    const singleCheckboxPage = new SingleCheckboxPage(page)
    const submitPage = new SubmitPage(page)

    await mandatoryCheckboxPage.other().check()
    await mandatoryCheckboxPage.otherDetail().fill('Other value')
    await mandatoryCheckboxPage.submit().click()
    await nonMandatoryCheckboxPage.other().check()
    await nonMandatoryCheckboxPage.submit().click()
    await singleCheckboxPage.submit().click()

    await expect(submitPage.nonMandatoryCheckboxAnswer()).toHaveText('Other')
  })

  test('Given a non-mandatory checkbox answer, When the user selects Other and supplies a value, Then the supplied value should be displayed on the summary screen', async ({
    page
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const nonMandatoryCheckboxPage = new NonMandatoryCheckboxPage(page)
    const singleCheckboxPage = new SingleCheckboxPage(page)
    const submitPage = new SubmitPage(page)

    await mandatoryCheckboxPage.other().check()
    await mandatoryCheckboxPage.otherDetail().fill('Other value')
    await mandatoryCheckboxPage.submit().click()
    await nonMandatoryCheckboxPage.other().check()
    await nonMandatoryCheckboxPage.otherDetail().fill('The other value')
    await nonMandatoryCheckboxPage.submit().click()
    await singleCheckboxPage.submit().click()

    await expect(submitPage.nonMandatoryCheckboxAnswer()).toContainText('The other value')
  })

  test('Given that there is an escaped character in an answer label, When the user selects the answer, Then the label should be displayed on the summary screen', async ({
    page
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const nonMandatoryCheckboxPage = new NonMandatoryCheckboxPage(page)
    const singleCheckboxPage = new SingleCheckboxPage(page)
    const submitPage = new SubmitPage(page)

    await mandatoryCheckboxPage.hamCheese().check()
    await mandatoryCheckboxPage.submit().click()
    await nonMandatoryCheckboxPage.other().check()
    await nonMandatoryCheckboxPage.otherDetail().fill('The other value')
    await nonMandatoryCheckboxPage.submit().click()
    await singleCheckboxPage.submit().click()

    await expect(submitPage.mandatoryCheckboxAnswer()).toHaveText('Ham & Cheese')
  })

  test('Given I have previously added text in other textfield and saved, when I uncheck other options and select a different checkbox as answer, then the text entered in other field must be wiped.', async ({
    page
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const nonMandatoryCheckboxPage = new NonMandatoryCheckboxPage(page)

    await mandatoryCheckboxPage.other().check()
    await mandatoryCheckboxPage.otherDetail().fill('Other value')
    await mandatoryCheckboxPage.submit().click()

    await nonMandatoryCheckboxPage.previous().click()
    await mandatoryCheckboxPage.other().uncheck()
    await mandatoryCheckboxPage.hamCheese().check()
    await mandatoryCheckboxPage.submit().click()

    await nonMandatoryCheckboxPage.previous().click()
    await mandatoryCheckboxPage.other().check()
    await expect(mandatoryCheckboxPage.otherDetail()).toHaveValue('')
  })

  test('Given a mandatory checkbox answer, When the user selects only one option, Then the answer should not be displayed as a list on the summary screen', async ({
    page
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const nonMandatoryCheckboxPage = new NonMandatoryCheckboxPage(page)
    const submitPage = new SubmitPage(page)

    await mandatoryCheckboxPage.ham().check()
    await mandatoryCheckboxPage.submit().click()
    await nonMandatoryCheckboxPage.submit().click()

    await expect(submitPage.mandatoryCheckboxAnswer().locator('li')).toHaveCount(0)
  })

  test('Given a mandatory checkbox answer, When the user selects more than one option, Then the answer should be displayed as a list on the summary screen', async ({
    page
  }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    const nonMandatoryCheckboxPage = new NonMandatoryCheckboxPage(page)
    const singleCheckboxPage = new SingleCheckboxPage(page)
    const submitPage = new SubmitPage(page)

    await mandatoryCheckboxPage.ham().check()
    await mandatoryCheckboxPage.hamCheese().check()
    await mandatoryCheckboxPage.submit().click()
    await nonMandatoryCheckboxPage.submit().click()
    await singleCheckboxPage.submit().click()

    await expect(submitPage.mandatoryCheckboxAnswer().locator('li')).toHaveCount(2)
  })
})
