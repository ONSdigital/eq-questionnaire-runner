import { test, expect } from '../../../../fixtures/test'
import type { Page } from '../../../../fixtures/test'
import DatePage from '../../../../generated_pages/date_validation_single/date-block.page'
import DatePeriodPage from '../../../../generated_pages/date_validation_single/date-range-block.page'
import SubmitPage from '../../../../generated_pages/date_validation_single/submit.page'

test.describe('Feature: Validation for single date periods', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_date_validation_single.json')
    await completeFirstDatePage(page)
  })

  test.describe('Given I enter a date before the minimum offset meta date', () => {
    test('When I continue, Then I should see a period validation error', async ({ page }) => {
      const datePeriodPage = new DatePeriodPage(page)
      await datePeriodPage.dateRangeFromDay().fill('13')
      await datePeriodPage.dateRangeFromMonth().fill('2')
      await datePeriodPage.dateRangeFromYear().fill('2016')
      await datePeriodPage.submit().click()

      await datePeriodPage.dateRangeToDay().fill('3')
      await datePeriodPage.dateRangeToMonth().fill('3')
      await datePeriodPage.dateRangeToYear().fill('2018')
      await datePeriodPage.submit().click()
      await expect(datePeriodPage.errorNumber(1)).toHaveText('Enter a date after 12 December 2016')
    })
  })

  test.describe('Given I enter a date after the maximum offset value date', () => {
    test('When I continue, Then I should see a period validation error', async ({ page }) => {
      const datePeriodPage = new DatePeriodPage(page)
      await datePeriodPage.dateRangeFromDay().fill('13')
      await datePeriodPage.dateRangeFromMonth().fill('7')
      await datePeriodPage.dateRangeFromYear().fill('2017')
      await datePeriodPage.submit().click()

      await datePeriodPage.dateRangeToDay().fill('3')
      await datePeriodPage.dateRangeToMonth().fill('3')
      await datePeriodPage.dateRangeToYear().fill('2018')
      await datePeriodPage.submit().click()
      await expect(datePeriodPage.errorNumber(1)).toHaveText('Enter a date before 2 July 2017')
    })
  })

  test.describe('Given I enter a date before the minimum offset answer id date', () => {
    test('When I continue, Then I should see a period validation error', async ({ page }) => {
      const datePeriodPage = new DatePeriodPage(page)
      await datePeriodPage.dateRangeFromDay().fill('13')
      await datePeriodPage.dateRangeFromMonth().fill('11')
      await datePeriodPage.dateRangeFromYear().fill('2016')
      await datePeriodPage.submit().click()

      await datePeriodPage.dateRangeToDay().fill('13')
      await datePeriodPage.dateRangeToMonth().fill('1')
      await datePeriodPage.dateRangeToYear().fill('2018')
      await datePeriodPage.submit().click()
      await expect(datePeriodPage.errorNumber(2)).toHaveText('Enter a date after 10 February 2018')
    })
  })

  test.describe('Given I enter a date in between the minimum offset meta date and the maximum offset value date', () => {
    test('When I continue, Then I should be able to reach the summary', async ({ page }) => {
      const datePeriodPage = new DatePeriodPage(page)
      const submitPage = new SubmitPage(page)
      await datePeriodPage.dateRangeFromDay().fill('13')
      await datePeriodPage.dateRangeFromMonth().fill('12')
      await datePeriodPage.dateRangeFromYear().fill('2016')
      await datePeriodPage.submit().click()

      await datePeriodPage.dateRangeToDay().fill('11')
      await datePeriodPage.dateRangeToMonth().fill('2')
      await datePeriodPage.dateRangeToYear().fill('2018')
      await datePeriodPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })
  })

  async function completeFirstDatePage (page: Page): Promise<void> {
    const datePage = new DatePage(page)
    await datePage.day().fill('1')
    await datePage.month().fill('1')
    await datePage.year().fill('2018')
    await datePage.submit().click()
  }
})
