import { test, expect } from '../../../../fixtures/test'
import DateRangePage from '../../../../generated_pages/date_validation_yyyy_combined/date-range-block.page'
import SubmitPage from '../../../../generated_pages/date_validation_yyyy_combined/submit.page'

test.describe('Feature: Combined question level and single validation for MM-YYYY dates', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_date_validation_yyyy_combined.json')
  })

  test.describe('Period Validation', () => {
    test.describe('Given I enter dates', () => {
      test('When I enter dates that are too early and too late, Then I should see two validation errors', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromYear().fill('2015')
        await dateRangePage.dateRangeToYear().fill('2021')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a date after 2015')
        await expect(dateRangePage.errorNumber(2)).toHaveText('Enter a date before 2021')
      })

      test('When I enter a range too large, Then I should see a range validation error', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromYear().fill('2016')
        await dateRangePage.dateRangeToYear().fill('2020')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a reporting period less than or equal to 3 years')
      })

      test('When I enter a range too small, Then I should see a range validation error', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        await dateRangePage.dateRangeFromYear().fill('2016')
        await dateRangePage.dateRangeToYear().fill('2017')
        await dateRangePage.submit().click()
        await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a reporting period greater than or equal to 2 years')
      })

      test('When I enter valid dates, Then I should see the summary page', async ({ page }) => {
        const dateRangePage = new DateRangePage(page)
        const submitPage = new SubmitPage(page)
        await dateRangePage.dateRangeFromYear().fill('2016')
        // Min range
        await dateRangePage.dateRangeToYear().fill('2018')
        await dateRangePage.submit().click()
        await expect(submitPage.dateRangeFrom()).toHaveText('2016 to 2018')

        // Max range
        await submitPage.dateRangeFromEdit().click()
        await dateRangePage.dateRangeToYear().fill('2019')
        await dateRangePage.submit().click()
        await expect(submitPage.dateRangeFrom()).toHaveText('2016 to 2019')
      })
    })
  })
})
