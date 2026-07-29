import { test, expect } from '../../../../fixtures/test'
import DateRangePage from '../../../../generated_pages/date_validation_combined/date-range-block.page'
import SubmitPage from '../../../../generated_pages/date_validation_combined/submit.page'

test.describe('Feature: Combined question level and single validation for dates', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_date_validation_combined.json')
  })

  test.describe('Period Validation', () => {
    test.describe('Given I enter dates', () => {
      test('When I enter a single dates that are too early/late, Then I should see a single validation errors', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromDay().fill('12')
        await dateRangePage.dateRangeFromMonth().fill('12')
        await dateRangePage.dateRangeFromYear().fill('2016')

        await dateRangePage.dateRangeToDay().fill('22')
        await dateRangePage.dateRangeToMonth().fill('2')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a date after 12 December 2016')
        await expect(dateRangePage.errorNumber(2)).toHaveText('Enter a date before 22 February 2017')
      })

      test('When I enter a range too large, Then I should see a range validation error', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromDay().fill('13')
        await dateRangePage.dateRangeFromMonth().fill('12')
        await dateRangePage.dateRangeFromYear().fill('2016')

        await dateRangePage.dateRangeToDay().fill('21')
        await dateRangePage.dateRangeToMonth().fill('2')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a reporting period less than or equal to 50 days')
      })

      test('When I enter a range too small, Then I should see a range validation error', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromDay().fill('1')
        await dateRangePage.dateRangeFromMonth().fill('1')
        await dateRangePage.dateRangeFromYear().fill('2017')

        await dateRangePage.dateRangeToDay().fill('10')
        await dateRangePage.dateRangeToMonth().fill('1')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a reporting period greater than or equal to 10 days')
      })

      test('When I enter valid dates, Then I should see the summary page', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        const submitPage = new SubmitPage(page)
        await dateRangePage.dateRangeFromDay().fill('1')
        await dateRangePage.dateRangeFromMonth().fill('1')
        await dateRangePage.dateRangeFromYear().fill('2017')

        // Min range
        await dateRangePage.dateRangeToDay().fill('11')
        await dateRangePage.dateRangeToMonth().fill('1')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(submitPage.dateRangeFrom()).toHaveText('1 January 2017 to 11 January 2017')

        // Max range
        await submitPage.dateRangeFromEdit().click()
        await dateRangePage.dateRangeToDay().fill('20')
        await dateRangePage.dateRangeToMonth().fill('2')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(submitPage.dateRangeFrom()).toHaveText('1 January 2017 to 20 February 2017')
      })
    })
  })
})
