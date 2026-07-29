import { test, expect } from '../../../../fixtures/test'
import DateRangePage from '../../../../generated_pages/date_validation_mm_yyyy_combined/date-range-block.page'
import SubmitPage from '../../../../generated_pages/date_validation_mm_yyyy_combined/submit.page'

test.describe('Feature: Combined question level and single validation for MM-YYYY dates', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_date_validation_mm_yyyy_combined.json')
  })

  test.describe('Period Validation', () => {
    test.describe('Given I enter dates', () => {
      test('When I enter a month but no year, Then I should see only a single invalid date error', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromYear().fill('2018')

        await dateRangePage.dateRangeToMonth().fill('4')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a valid date')
        await expect(dateRangePage.errorNumber(2)).not.toBeVisible()
      })

      test('When I enter a year but no month, Then I should see only a single invalid date error', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromMonth().fill('10')
        await dateRangePage.dateRangeFromYear().fill('')

        await dateRangePage.dateRangeToMonth().fill('4')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a valid date')
        await expect(dateRangePage.errorNumber(2)).not.toBeVisible()
      })

      test('When I enter a year of 0, Then I should see only a single invalid date error', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromMonth().fill('10')
        await dateRangePage.dateRangeFromYear().fill('0')

        await dateRangePage.dateRangeToMonth().fill('4')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter the year in a valid format. For example, 2023.')
        await expect(dateRangePage.errorNumber(2)).not.toBeVisible()
      })

      test('When I enter a single dates that are too early/late, Then I should see a single validation errors', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromMonth().fill('10')
        await dateRangePage.dateRangeFromYear().fill('2016')

        await dateRangePage.dateRangeToMonth().fill('6')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a date after November 2016')
        await expect(dateRangePage.errorNumber(2)).toHaveText('Enter a date before June 2017')
      })

      test('When I enter a range too large, Then I should see a range validation error', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromMonth().fill('12')
        await dateRangePage.dateRangeFromYear().fill('2016')

        await dateRangePage.dateRangeToMonth().fill('5')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a reporting period less than or equal to 3 months')
      })

      test('When I enter a range too small, Then I should see a range validation error', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromMonth().fill('12')
        await dateRangePage.dateRangeFromYear().fill('2016')

        await dateRangePage.dateRangeToMonth().fill('1')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a reporting period greater than or equal to 2 months')
      })

      test('When I enter valid dates, Then I should see the summary page', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        const submitPage = new SubmitPage(page)
        await dateRangePage.dateRangeFromMonth().fill('1')
        await dateRangePage.dateRangeFromYear().fill('2017')

        // Min range
        await dateRangePage.dateRangeToMonth().fill('3')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(submitPage.dateRangeFrom()).toHaveText('January 2017 to March 2017')

        // Max range
        await submitPage.dateRangeFromEdit().click()
        await dateRangePage.dateRangeToMonth().fill('4')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(submitPage.dateRangeFrom()).toHaveText('January 2017 to April 2017')
      })
    })
  })
})
