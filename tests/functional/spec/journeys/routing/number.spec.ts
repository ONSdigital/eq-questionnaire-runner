import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../fixtures/test'
import NumberQuestionPage from '../../../generated_pages/routing_number_equals/number-question.page'
import CorrectAnswerPage from '../../../generated_pages/routing_number_equals/correct-answer.page'
import IncorrectAnswerPage from '../../../generated_pages/routing_number_equals/incorrect-answer.page'

test.describe('Feature: Routing on a Number', () => {
  test.describe.configure({ mode: 'serial' })

  test.describe('Equals', () => {
    test.describe('Given I start number routing equals survey', () => {
      let context: BrowserContext
      let page: Page
      let openQuestionnaire: OpenQuestionnaire

      test.beforeAll(async ({ browser }) => {
        context = await browser.newContext()
        page = await context.newPage()
        openQuestionnaire = createOpenQuestionnaire(page)
        await openQuestionnaire('test_routing_number_equals.json')
      })

      test.afterAll(async () => {
        await context.close()
      })

      test('When I enter 123, Then I should be routed to the correct page', async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await numberQuestionPage.answer().fill('123')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(correctAnswerPage.pageName))
      })

      test("When I enter a number that isn't 123, Then I should be routed to the incorrect page", async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await correctAnswerPage.previous().click()
        await numberQuestionPage.answer().fill('555')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(incorrectAnswerPage.pageName))
      })
    })
  })

  test.describe('Not Equals', () => {
    test.describe('Given I start number routing not equals survey', () => {
      let context: BrowserContext
      let page: Page
      let openQuestionnaire: OpenQuestionnaire

      test.beforeAll(async ({ browser }) => {
        context = await browser.newContext()
        page = await context.newPage()
        openQuestionnaire = createOpenQuestionnaire(page)
        await openQuestionnaire('test_routing_number_not_equals.json')
      })

      test.afterAll(async () => {
        await context.close()
      })

      test("When I enter a number that isn't 123, Then I should be routed to the correct page", async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await numberQuestionPage.answer().fill('987')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(correctAnswerPage.pageName))
      })

      test('When I enter 123, Then I should be routed to the incorrect page', async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await correctAnswerPage.previous().click()
        await numberQuestionPage.answer().fill('123')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(incorrectAnswerPage.pageName))
      })
    })
  })

  test.describe('Greater Than', () => {
    test.describe('Given I start number routing greater than survey', () => {
      let context: BrowserContext
      let page: Page
      let openQuestionnaire: OpenQuestionnaire

      test.beforeAll(async ({ browser }) => {
        context = await browser.newContext()
        page = await context.newPage()
        openQuestionnaire = createOpenQuestionnaire(page)
        await openQuestionnaire('test_routing_number_greater_than.json')
      })

      test.afterAll(async () => {
        await context.close()
      })

      test('When I enter a number greater than 123, Then I should be routed to the correct page', async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await numberQuestionPage.answer().fill('555')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(correctAnswerPage.pageName))
      })

      test('When I enter 123, Then I should be routed to the incorrect page', async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await correctAnswerPage.previous().click()
        await numberQuestionPage.answer().fill('123')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(incorrectAnswerPage.pageName))
      })

      test('When I enter a number less than 123, Then I should be routed to the incorrect page', async () => {
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await incorrectAnswerPage.previous().click()
        await numberQuestionPage.answer().fill('2')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(incorrectAnswerPage.pageName))
      })
    })
  })

  test.describe('Less Than', () => {
    test.describe('Given I start number routing less than survey', () => {
      let context: BrowserContext
      let page: Page
      let openQuestionnaire: OpenQuestionnaire

      test.beforeAll(async ({ browser }) => {
        context = await browser.newContext()
        page = await context.newPage()
        openQuestionnaire = createOpenQuestionnaire(page)
        await openQuestionnaire('test_routing_number_less_than.json')
      })

      test.afterAll(async () => {
        await context.close()
      })

      test('When I enter a number less than 123, Then I should be routed to the correct page', async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await numberQuestionPage.answer().fill('77')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(correctAnswerPage.pageName))
      })

      test('When I enter 123, Then I should be routed to the incorrect page', async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await correctAnswerPage.previous().click()
        await numberQuestionPage.answer().fill('123')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(incorrectAnswerPage.pageName))
      })

      test('When I enter a number greater than 123, Then I should be routed to the incorrect page', async () => {
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await incorrectAnswerPage.previous().click()
        await numberQuestionPage.answer().fill('765')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(incorrectAnswerPage.pageName))
      })
    })
  })

  test.describe('Greater Than or Equal', () => {
    test.describe('Given I have number routing with a greater than or equal', () => {
      let context: BrowserContext
      let page: Page
      let openQuestionnaire: OpenQuestionnaire

      test.beforeAll(async ({ browser }) => {
        context = await browser.newContext()
        page = await context.newPage()
        openQuestionnaire = createOpenQuestionnaire(page)
        await openQuestionnaire('test_routing_number_greater_than_or_equal.json')
      })

      test.afterAll(async () => {
        await context.close()
      })

      test('When I enter a number greater than 123, Then I should be routed to the correct page', async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await numberQuestionPage.answer().fill('555')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(correctAnswerPage.pageName))
      })

      test('When I enter 123, Then I should be routed to the correct page', async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await correctAnswerPage.previous().click()
        await numberQuestionPage.answer().fill('123')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(correctAnswerPage.pageName))
      })

      test('When I enter a number less than 123, Then I should be routed to the incorrect page', async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await correctAnswerPage.previous().click()
        await numberQuestionPage.answer().fill('2')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(incorrectAnswerPage.pageName))
      })
    })
  })

  test.describe('Less Than or Equal', () => {
    test.describe('Given I have number routing with a less than or equal', () => {
      let context: BrowserContext
      let page: Page
      let openQuestionnaire: OpenQuestionnaire

      test.beforeAll(async ({ browser }) => {
        context = await browser.newContext()
        page = await context.newPage()
        openQuestionnaire = createOpenQuestionnaire(page)
        await openQuestionnaire('test_routing_number_less_than_or_equal.json')
      })

      test.afterAll(async () => {
        await context.close()
      })

      test('When I enter a number less than 123, Then I should be routed to the correct page', async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await numberQuestionPage.answer().fill('23')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(correctAnswerPage.pageName))
      })

      test('When I enter 123, Then I should be routed to the correct page', async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await correctAnswerPage.previous().click()
        await numberQuestionPage.answer().fill('123')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(correctAnswerPage.pageName))
      })

      test('When I enter a number larger than 123, Then I should be routed to the incorrect page', async () => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        const numberQuestionPage = new NumberQuestionPage(page)
        await correctAnswerPage.previous().click()
        await numberQuestionPage.answer().fill('546')
        await numberQuestionPage.submit().click()
        await expect(page).toHaveURL(new RegExp(incorrectAnswerPage.pageName))
      })
    })
  })
})
