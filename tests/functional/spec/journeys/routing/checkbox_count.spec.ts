import { test, expect } from '../../../fixtures/test'
import ToppingCheckboxPage from '../../../generated_pages/routing_checkbox_count/topping-checkbox.page'
import CorrectAnswerPage from '../../../generated_pages/routing_checkbox_count/correct-answer.page'
import IncorrectAnswerPage from '../../../generated_pages/routing_checkbox_count/incorrect-answer.page'

test.describe('Test routing using count of checkboxes checked', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_routing_checkbox_count.json')
  })

  test('Given a user selects 2 checkboxes, When they submit, Then they should be routed to the correct page', async ({ page }) => {
    const correctAnswerPage = new CorrectAnswerPage(page)
    const toppingCheckboxPage = new ToppingCheckboxPage(page)
    await toppingCheckboxPage.cheese().click()
    await toppingCheckboxPage.ham().click()
    await toppingCheckboxPage.submit().click()

    await expect(page).toHaveURL(new RegExp(correctAnswerPage.pageName))
    await expect(correctAnswerPage.questionText()).toHaveText('You selected 2 or more toppings')
  })

  test('Given a user selects no checkboxes, When they submit, Then they should be routed to the incorrect page', async ({ page }) => {
    const incorrectAnswerPage = new IncorrectAnswerPage(page)
    const toppingCheckboxPage = new ToppingCheckboxPage(page)
    await toppingCheckboxPage.submit().click()

    await expect(page).toHaveURL(new RegExp(incorrectAnswerPage.pageName))
    await expect(incorrectAnswerPage.questionText()).toHaveText('You did not select 2 or more toppings')
  })

  test('Given a user selects 1 checkbox, When they submit, Then they should be routed to the incorrect page', async ({ page }) => {
    const incorrectAnswerPage = new IncorrectAnswerPage(page)
    const toppingCheckboxPage = new ToppingCheckboxPage(page)
    await toppingCheckboxPage.cheese().click()
    await toppingCheckboxPage.submit().click()

    await expect(page).toHaveURL(new RegExp(incorrectAnswerPage.pageName))
    await expect(incorrectAnswerPage.questionText()).toHaveText('You did not select 2 or more toppings')
  })

  test('Given a user selects 3 checkbox, When they submit, Then they should be routed to the correct page', async ({ page }) => {
    const correctAnswerPage = new CorrectAnswerPage(page)
    const toppingCheckboxPage = new ToppingCheckboxPage(page)
    await toppingCheckboxPage.cheese().click()
    await toppingCheckboxPage.ham().click()
    await toppingCheckboxPage.pineapple().click()
    await toppingCheckboxPage.submit().click()

    await expect(page).toHaveURL(new RegExp(correctAnswerPage.pageName))
    await expect(correctAnswerPage.questionText()).toHaveText('You selected 2 or more toppings')
  })
})
