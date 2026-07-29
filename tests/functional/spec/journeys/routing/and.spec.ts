import { test, expect } from '../../../fixtures/test'
import FirstNumberQuestionPage from '../../../generated_pages/routing_and/number-question-1.page'
import SecondNumberQuestionPage from '../../../generated_pages/routing_and/number-question-2.page'
import CorrectAnswerPage from '../../../generated_pages/routing_and/correct-answer.page'
import IncorrectAnswerPage from '../../../generated_pages/routing_and/incorrect-answer.page'

test.describe('Feature: Routing - And Operator', () => {
  test.describe('Equals', () => {
    test.describe('Given I start the and operator routing survey', () => {
      test.beforeEach(async ({ openQuestionnaire }) => {
        await openQuestionnaire('test_routing_and.json')
      })

      test('When I enter both answers correctly with 123 and 321, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const firstNumberQuestionPage = new FirstNumberQuestionPage(page)
        const secondNumberQuestionPage = new SecondNumberQuestionPage(page)
        await firstNumberQuestionPage.answer1().fill('123')
        await firstNumberQuestionPage.submit().click()
        await secondNumberQuestionPage.answer2().fill('321')
        await secondNumberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(correctAnswerPage.pageName))
      })

      test('When I only enter the second answer correctly with 555 and 321, Then I should be routed to the incorrect page', async ({ page }) => {
        const firstNumberQuestionPage = new FirstNumberQuestionPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        const secondNumberQuestionPage = new SecondNumberQuestionPage(page)
        await firstNumberQuestionPage.answer1().fill('555')
        await firstNumberQuestionPage.submit().click()
        await secondNumberQuestionPage.answer2().fill('321')
        await secondNumberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(incorrectAnswerPage.pageName))
      })

      test('When I only enter the first answer correctly with 123 and 555, Then I should be routed to the incorrect page', async ({ page }) => {
        const firstNumberQuestionPage = new FirstNumberQuestionPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        const secondNumberQuestionPage = new SecondNumberQuestionPage(page)
        await firstNumberQuestionPage.answer1().fill('123')
        await firstNumberQuestionPage.submit().click()
        await secondNumberQuestionPage.answer2().fill('555')
        await secondNumberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(incorrectAnswerPage.pageName))
      })

      test('When I answer both questions incorrectly with 555 and 444, Then I should be routed to the incorrect page', async ({ page }) => {
        const firstNumberQuestionPage = new FirstNumberQuestionPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        const secondNumberQuestionPage = new SecondNumberQuestionPage(page)
        await firstNumberQuestionPage.answer1().fill('555')
        await firstNumberQuestionPage.submit().click()
        await secondNumberQuestionPage.answer2().fill('444')
        await secondNumberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(incorrectAnswerPage.pageName))
      })
    })
  })
})
