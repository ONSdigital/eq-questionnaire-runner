import { test, expect } from '../../../fixtures/test'
import type { Page } from '../../../fixtures/test'
import DessertPage from '../../../generated_pages/submit_with_summary/dessert.page'
import DessertConfirmationPage from '../../../generated_pages/submit_with_summary/dessert-confirmation.page'
import NumbersPage from '../../../generated_pages/submit_with_summary/numbers.page'
import RadioPage from '../../../generated_pages/submit_with_summary/radio.page'
import SubmitPage from '../../../generated_pages/submit_with_summary/submit.page'

test.describe('Submit Page with Summary', () => {
  test.beforeEach('Load the questionnaire', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_submit_with_summary.json')
  })

  test('Given a questionnaire with a summary has been completed when the submit page is displayed, then it should contain a summary of all answers', async ({
    page
  }) => {
    const submitPage = new SubmitPage(page)
    await completeAllQuestions(page)

    await expect(submitPage.radioAnswer()).toHaveText('Bacon')
    await expect(submitPage.dessertGroupTitle()).toHaveText('Dessert')
    await expect(submitPage.dessertAnswer()).toHaveText('Crème Brûlée')
    await expect(submitPage.dessertConfirmationAnswer()).toHaveText('Yes')
    await expect(submitPage.numbersCurrencyAnswer()).toHaveText('£1,234.00')
    await expect(submitPage.numbersUnitAnswer()).toHaveText('123,456 km²')
    await expect(submitPage.numbersDecimalAnswer()).toHaveText('123,456.78')
  })

  test('Given a questionnaire with a summary has been completed when the submit page is displayed then I should be able to submit the answers', async ({
    page
  }) => {
    const submitPage = new SubmitPage(page)
    await completeAllQuestions(page)

    await submitPage.submit().click()
    await expect(page).toHaveURL(/thank-you/)
  })

  test('Given a questionnaire with a summary has been completed when a summary page edit link is clicked then it should return to that question', async ({
    page
  }) => {
    const radioPage = new RadioPage(page)
    const submitPage = new SubmitPage(page)
    await completeAllQuestions(page)

    await submitPage.radioAnswerEdit().click()

    await expect(radioPage.bacon()).toBeChecked()
  })

  test('Given a questionnaire with a summary has been completed and a summary page edit link is clicked, when I click previous, then it should return to the summary', async ({
    page
  }) => {
    const radioPage = new RadioPage(page)
    const submitPage = new SubmitPage(page)
    await completeAllQuestions(page)

    await submitPage.radioAnswerEdit().click()
    await radioPage.previous().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
  })

  test('Given a questionnaire with a summary has been completed when a summary page edit link is clicked then it should return to that question then back to summary', async ({
    page
  }) => {
    const radioPage = new RadioPage(page)
    const submitPage = new SubmitPage(page)
    await completeAllQuestions(page)

    await submitPage.radioAnswerEdit().click()
    await radioPage.sausage().click()
    await radioPage.submit().click()
    await expect(submitPage.radioAnswer()).toHaveText('Sausage')
  })

  test('Given the edit link is used when a question is updated then the submit page summary should show the new answer', async ({ page }) => {
    const numbersPage = new NumbersPage(page)
    const submitPage = new SubmitPage(page)
    await completeAllQuestions(page)

    await submitPage.numbersUnitAnswerEdit().click()
    await expect(numbersPage.unit()).toBeFocused()
    await numbersPage.unit().fill('654321')
    await numbersPage.submit().click()
    await expect(submitPage.numbersUnitAnswer()).toHaveText('654,321 km²')
  })

  test('Given a number value of zero is entered when on the submit page then formatted 0 should be displayed on the summary', async ({ page }) => {
    const dessertConfirmationPage = new DessertConfirmationPage(page)
    const dessertPage = new DessertPage(page)
    const numbersPage = new NumbersPage(page)
    const radioPage = new RadioPage(page)
    const submitPage = new SubmitPage(page)
    await radioPage.submit().click()
    await dessertPage.answer().fill('Cake')
    await dessertPage.submit().click()
    await dessertConfirmationPage.yes().click()
    await dessertConfirmationPage.submit().click()
    await numbersPage.currency().fill('0')
    await numbersPage.submit().click()
    await expect(submitPage.numbersCurrencyAnswer()).toHaveText('£0.00')
  })

  test('Given no value is entered when on the submit page summary then the correct response should be displayed', async ({ page }) => {
    const dessertConfirmationPage = new DessertConfirmationPage(page)
    const dessertPage = new DessertPage(page)
    const numbersPage = new NumbersPage(page)
    const radioPage = new RadioPage(page)
    const submitPage = new SubmitPage(page)
    await radioPage.submit().click()
    await dessertPage.answer().fill('Cake')
    await dessertPage.submit().click()
    await dessertConfirmationPage.yes().click()
    await dessertConfirmationPage.submit().click()
    await numbersPage.submit().click()
    await expect(submitPage.numbersCurrencyAnswer()).toHaveText('No answer provided')
  })

  test('Given a questionnaire with a summary has been completed, When submission content has not been set in the schema, Then the default content should be displayed', async ({
    page
  }) => {
    const submitPage = new SubmitPage(page)
    await completeAllQuestions(page)

    await expect(submitPage.heading()).toHaveText('Check your answers and submit')
    await expect(submitPage.submit()).toHaveText('Submit answers')
  })

  async function completeAllQuestions (page: Page): Promise<void> {
    const radioPage = new RadioPage(page)
    const dessertPage = new DessertPage(page)
    const dessertConfirmationPage = new DessertConfirmationPage(page)
    const numbersPage = new NumbersPage(page)
    const submitPage = new SubmitPage(page)

    await radioPage.bacon().click()
    await radioPage.submit().click()
    await dessertPage.answer().fill('Crème Brûlée')
    await dessertPage.submit().click()
    await dessertConfirmationPage.yes().click()
    await dessertConfirmationPage.submit().click()
    await numbersPage.currency().fill('1234')
    await numbersPage.unit().fill('123456')
    await numbersPage.decimal().fill('123456.78')
    await numbersPage.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
  }
})
