import { test } from '../../../fixtures/test'
import IncorrectAnswerPage from '../../../generated_pages/routing_date_equals/incorrect-answer.page'
import CorrectAnswerPage from '../../../generated_pages/routing_date_equals/correct-answer.page'
import DateEqualsComparisonQuestionPage from '../../../generated_pages/routing_date_equals/comparison-date-block.page'
import DateEqualsQuestionPage from '../../../generated_pages/routing_date_equals/date-question.page'
import DateNotEqualsQuestionPage from '../../../generated_pages/routing_date_not_equals/date-question.page'
import DateGreaterThanQuestionPage from '../../../generated_pages/routing_date_greater_than/date-question.page'
import DateGreaterThanOrEqualsQuestionPage from '../../../generated_pages/routing_date_greater_than_or_equals/date-question.page'
import DateLessThanQuestionPage from '../../../generated_pages/routing_date_less_than/date-question.page'
import DateLessThanOrEqualsQuestionPage from '../../../generated_pages/routing_date_less_than_or_equals/date-question.page'
import { verifyUrlContains } from '../../../helpers'
const today = new Date()
const dayToday = today.getDate()
const monthToday = today.getMonth() + 1 // January is 0!
const yearToday = today.getFullYear()

const yesterday = new Date()
yesterday.setDate(today.getDate() - 1)
const dayYesterday = yesterday.getDate()
const monthYesterday = yesterday.getMonth() + 1
const yearYesterday = yesterday.getFullYear()

const tomorrow = new Date()
tomorrow.setDate(today.getDate() + 1)
const dayTomorrow = tomorrow.getDate()
const monthTomorrow = tomorrow.getMonth() + 1
const yearTomorrow = tomorrow.getFullYear()

test.describe('Feature: Routing on a Date', () => {
  test.describe('Equals', () => {
    test.describe('Given I start date routing equals survey', () => {
      test.beforeEach(async ({ page, openQuestionnaire }) => {
        const dateEqualsComparisonQuestionPage = new DateEqualsComparisonQuestionPage(page)
        await openQuestionnaire('test_routing_date_equals.json')
        await dateEqualsComparisonQuestionPage.day().fill('31')
        await dateEqualsComparisonQuestionPage.month().fill('3')
        await dateEqualsComparisonQuestionPage.year().fill('2020')
        await dateEqualsComparisonQuestionPage.submit().click()
      })

      test('When I enter the same date, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateEqualsQuestionPage = new DateEqualsQuestionPage(page)
        await dateEqualsQuestionPage.day().fill('31')
        await dateEqualsQuestionPage.month().fill('3')
        await dateEqualsQuestionPage.year().fill('2020')
        await dateEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter the yesterday date, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateEqualsQuestionPage = new DateEqualsQuestionPage(page)
        await dateEqualsQuestionPage.day().fill('30')
        await dateEqualsQuestionPage.month().fill('3')
        await dateEqualsQuestionPage.year().fill('2020')
        await dateEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter the tomorrow date, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateEqualsQuestionPage = new DateEqualsQuestionPage(page)
        await dateEqualsQuestionPage.day().fill('1')
        await dateEqualsQuestionPage.month().fill('4')
        await dateEqualsQuestionPage.year().fill('2020')
        await dateEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter the last month date, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateEqualsQuestionPage = new DateEqualsQuestionPage(page)
        await dateEqualsQuestionPage.day().fill('29')
        await dateEqualsQuestionPage.month().fill('2')
        await dateEqualsQuestionPage.year().fill('2020')
        await dateEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter the next month date, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateEqualsQuestionPage = new DateEqualsQuestionPage(page)
        await dateEqualsQuestionPage.day().fill('30')
        await dateEqualsQuestionPage.month().fill('4')
        await dateEqualsQuestionPage.year().fill('2020')
        await dateEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter the last year date, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateEqualsQuestionPage = new DateEqualsQuestionPage(page)
        await dateEqualsQuestionPage.day().fill('31')
        await dateEqualsQuestionPage.month().fill('3')
        await dateEqualsQuestionPage.year().fill('2019')
        await dateEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter the next year date, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateEqualsQuestionPage = new DateEqualsQuestionPage(page)
        await dateEqualsQuestionPage.day().fill('31')
        await dateEqualsQuestionPage.month().fill('3')
        await dateEqualsQuestionPage.year().fill('2021')
        await dateEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter an incorrect date, Then I should be routed to the incorrect page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateEqualsComparisonQuestionPage = new DateEqualsComparisonQuestionPage(page)
        const dateEqualsQuestionPage = new DateEqualsQuestionPage(page)
        await dateEqualsQuestionPage.day().fill('1')
        await dateEqualsQuestionPage.month().fill('3')
        await dateEqualsQuestionPage.year().fill('2020')
        await dateEqualsComparisonQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })
    })
  })

  test.describe('Not Equals', () => {
    test.describe('Given I start date routing not equals survey', () => {
      test.beforeEach(async ({ openQuestionnaire }) => {
        await openQuestionnaire('test_routing_date_not_equals.json')
      })

      test('When I enter a different date to February 2018, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateNotEqualsQuestionPage = new DateNotEqualsQuestionPage(page)
        await dateNotEqualsQuestionPage.month().fill('3')
        await dateNotEqualsQuestionPage.year().fill('2018')
        await dateNotEqualsQuestionPage.submit().click()

        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter February 2018, Then I should be routed to the incorrect page', async ({ page }) => {
        const dateNotEqualsQuestionPage = new DateNotEqualsQuestionPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        await dateNotEqualsQuestionPage.month().fill('2')
        await dateNotEqualsQuestionPage.year().fill('2018')
        await dateNotEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, incorrectAnswerPage.pageName)
      })
    })
  })

  test.describe('Greater Than', () => {
    test.describe('Given I start date routing greater than survey', () => {
      test.beforeEach(async ({ openQuestionnaire }) => {
        await openQuestionnaire('test_routing_date_greater_than.json')
      })

      test('When I enter a date greater than the 1st March 2017, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateGreaterThanQuestionPage = new DateGreaterThanQuestionPage(page)
        await dateGreaterThanQuestionPage.day().fill('2')
        await dateGreaterThanQuestionPage.month().fill('3')
        await dateGreaterThanQuestionPage.year().fill('2017')
        await dateGreaterThanQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter the 1st March 2017, Then I should be routed to the incorrect page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateGreaterThanQuestionPage = new DateGreaterThanQuestionPage(page)
        await dateGreaterThanQuestionPage.day().fill('1')
        await dateGreaterThanQuestionPage.month().fill('3')
        await dateGreaterThanQuestionPage.year().fill('2017')
        await dateGreaterThanQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter a date less than the 1st March 2017, Then I should be routed to the incorrect page', async ({ page }) => {
        const dateGreaterThanQuestionPage = new DateGreaterThanQuestionPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        await dateGreaterThanQuestionPage.day().fill('28')
        await dateGreaterThanQuestionPage.month().fill('2')
        await dateGreaterThanQuestionPage.year().fill('2017')
        await dateGreaterThanQuestionPage.submit().click()
        await verifyUrlContains(page, incorrectAnswerPage.pageName)
      })
    })
  })

  test.describe('Greater Than Or Equals', () => {
    test.describe('Given I start date routing greater than or equals survey', () => {
      test.beforeEach(async ({ openQuestionnaire }) => {
        await openQuestionnaire('test_routing_date_greater_than_or_equals.json')
      })

      test('When I enter a date greater than 2017, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateGreaterThanOrEqualsQuestionPage = new DateGreaterThanOrEqualsQuestionPage(page)
        await dateGreaterThanOrEqualsQuestionPage.year().fill('2018')
        await dateGreaterThanOrEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter 2017, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateGreaterThanOrEqualsQuestionPage = new DateGreaterThanOrEqualsQuestionPage(page)
        await dateGreaterThanOrEqualsQuestionPage.year().fill('2017')
        await dateGreaterThanOrEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter a date less than March 2017, Then I should be routed to the incorrect page', async ({ page }) => {
        const dateGreaterThanOrEqualsQuestionPage = new DateGreaterThanOrEqualsQuestionPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        await dateGreaterThanOrEqualsQuestionPage.year().fill('2016')
        await dateGreaterThanOrEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, incorrectAnswerPage.pageName)
      })
    })
  })

  test.describe('Less Than', () => {
    test.describe('Given I start date routing less than survey', () => {
      test.beforeEach(async ({ openQuestionnaire }) => {
        await openQuestionnaire('test_routing_date_less_than.json')
      })

      test('When I enter a date less than today, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateLessThanQuestionPage = new DateLessThanQuestionPage(page)
        await dateLessThanQuestionPage.day().fill(String(dayYesterday))
        await dateLessThanQuestionPage.month().fill(String(monthYesterday))
        await dateLessThanQuestionPage.year().fill(String(yearYesterday))
        await dateLessThanQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter a date equal to today, Then I should be routed to the incorrect page', async ({ page }) => {
        const dateLessThanQuestionPage = new DateLessThanQuestionPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        await dateLessThanQuestionPage.day().fill(String(dayToday))
        await dateLessThanQuestionPage.month().fill(String(monthToday))
        await dateLessThanQuestionPage.year().fill(String(yearToday))
        await dateLessThanQuestionPage.submit().click()
        await verifyUrlContains(page, incorrectAnswerPage.pageName)
      })

      test('When I enter a date greater than today, Then I should be routed to the incorrect page', async ({ page }) => {
        const dateLessThanQuestionPage = new DateLessThanQuestionPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        await dateLessThanQuestionPage.day().fill(String(dayTomorrow))
        await dateLessThanQuestionPage.month().fill(String(monthTomorrow))
        await dateLessThanQuestionPage.year().fill(String(yearTomorrow))
        await dateLessThanQuestionPage.submit().click()
        await verifyUrlContains(page, incorrectAnswerPage.pageName)
      })
    })
  })

  test.describe('Less Than Or Equals', () => {
    test.describe('Given I start date routing less than or equals survey', () => {
      test.beforeEach(async ({ openQuestionnaire }) => {
        await openQuestionnaire('test_routing_date_less_than_or_equals.json')
      })

      test('When I enter a date less than today, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateLessThanOrEqualsQuestionPage = new DateLessThanOrEqualsQuestionPage(page)
        await dateLessThanOrEqualsQuestionPage.day().fill(String(dayYesterday))
        await dateLessThanOrEqualsQuestionPage.month().fill(String(monthYesterday))
        await dateLessThanOrEqualsQuestionPage.year().fill(String(yearYesterday))
        await dateLessThanOrEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter a date equal to today, Then I should be routed to the correct page', async ({ page }) => {
        const correctAnswerPage = new CorrectAnswerPage(page)
        const dateLessThanOrEqualsQuestionPage = new DateLessThanOrEqualsQuestionPage(page)
        await dateLessThanOrEqualsQuestionPage.day().fill(String(dayToday))
        await dateLessThanOrEqualsQuestionPage.month().fill(String(monthToday))
        await dateLessThanOrEqualsQuestionPage.year().fill(String(yearToday))
        await dateLessThanOrEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, correctAnswerPage.pageName)
      })

      test('When I enter a date greater than today, Then I should be routed to the incorrect page', async ({ page }) => {
        const dateLessThanOrEqualsQuestionPage = new DateLessThanOrEqualsQuestionPage(page)
        const incorrectAnswerPage = new IncorrectAnswerPage(page)
        await dateLessThanOrEqualsQuestionPage.day().fill(String(dayTomorrow))
        await dateLessThanOrEqualsQuestionPage.month().fill(String(monthTomorrow))
        await dateLessThanOrEqualsQuestionPage.year().fill(String(yearTomorrow))
        await dateLessThanOrEqualsQuestionPage.submit().click()
        await verifyUrlContains(page, incorrectAnswerPage.pageName)
      })
    })
  })
})
