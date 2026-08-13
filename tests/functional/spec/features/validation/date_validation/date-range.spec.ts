import { test, expect } from '../../../../fixtures/test'
import DateRangePage from '../../../../generated_pages/date_validation_range/date-range-block.page'
import SubmitPage from '../../../../generated_pages/date_validation_range/submit.page'

test.describe('Feature: Question level validation for date ranges', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_date_validation_range.json')
  })

  test.describe('Period Validation', () => {
    test.describe('Given I enter a date period greater than the max period limit', () => {
      test('When I continue, Then I should see a period validation error', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromDay().fill('1')
        await dateRangePage.dateRangeFromMonth().fill('1')
        await dateRangePage.dateRangeFromYear().fill('2018')

        await dateRangePage.dateRangeToDay().fill('3')
        await dateRangePage.dateRangeToMonth().fill('3')
        await dateRangePage.dateRangeToYear().fill('2018')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a reporting period less than or equal to 1 month, 20 days')
      })
    })

    test.describe('Given I enter a date period less than the min period limit', () => {
      test('When I continue, Then I should see a period validation error', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromDay().fill('1')
        await dateRangePage.dateRangeFromMonth().fill('1')
        await dateRangePage.dateRangeFromYear().fill('2018')

        await dateRangePage.dateRangeToDay().fill('3')
        await dateRangePage.dateRangeToMonth().fill('1')
        await dateRangePage.dateRangeToYear().fill('2018')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a reporting period greater than or equal to 23 days')
      })
    })

    test.describe('Given I enter a date period within the set period limits', () => {
      test('When I continue, Then I should be able to reach the summary', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        const submitPage = new SubmitPage(page)
        await dateRangePage.dateRangeFromDay().fill('1')
        await dateRangePage.dateRangeFromMonth().fill('1')
        await dateRangePage.dateRangeFromYear().fill('2018')

        await dateRangePage.dateRangeToDay().fill('3')
        await dateRangePage.dateRangeToMonth().fill('2')
        await dateRangePage.dateRangeToYear().fill('2018')
        await dateRangePage.submit().click()
        await expect(page).toHaveURL(new RegExp(submitPage.pageName))
      })
    })
  })

  test.describe('Date Range Validation', () => {
    test.describe('Given I enter a "to date" which is earlier than the "from date"', () => {
      test('When I continue, Then I should see a validation error', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromDay().fill('1')
        await dateRangePage.dateRangeFromMonth().fill('2')
        await dateRangePage.dateRangeFromYear().fill('2018')

        await dateRangePage.dateRangeToDay().fill('3')
        await dateRangePage.dateRangeToMonth().fill('1')
        await dateRangePage.dateRangeToYear().fill('2018')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText("Enter a 'period to' date later than the 'period from' date")
      })
    })

    test.describe('Given I enter matching dates for the "from" and "to" dates', () => {
      test('When I continue, Then I should see a validation error', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromDay().fill('1')
        await dateRangePage.dateRangeFromMonth().fill('1')
        await dateRangePage.dateRangeFromYear().fill('2018')

        await dateRangePage.dateRangeToDay().fill('1')
        await dateRangePage.dateRangeToMonth().fill('1')
        await dateRangePage.dateRangeToYear().fill('2018')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText("Enter a 'period to' date later than the 'period from' date")
      })
    })

    test.describe('Given I enter a valid date range', () => {
      test('When I continue, Then I should be able to reach the summary', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        const submitPage = new SubmitPage(page)
        await dateRangePage.dateRangeFromDay().fill('1')
        await dateRangePage.dateRangeFromMonth().fill('1')
        await dateRangePage.dateRangeFromYear().fill('2018')

        await dateRangePage.dateRangeToDay().fill('3')
        await dateRangePage.dateRangeToMonth().fill('2')
        await dateRangePage.dateRangeToYear().fill('2018')
        await dateRangePage.submit().click()
        await expect(page).toHaveURL(new RegExp(submitPage.pageName))
      })
    })
  })
})
