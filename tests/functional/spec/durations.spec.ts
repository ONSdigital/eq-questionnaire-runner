import { test, expect } from '../fixtures/test'
import DurationPage from '../generated_pages/durations/duration-block.page'
import SubmitPage from '../generated_pages/durations/submit.page'

test.describe('Durations', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_durations.json')
  })

  test('Given the test_durations survey is selected durations suffixes are visible', async ({ page }) => {
    const durationPage = new DurationPage(page)
    await expect(durationPage.yearMonthYearsSuffix()).toHaveText('Years')
    await expect(durationPage.mandatoryYearMonthMonthsSuffix()).toHaveText('Months')
    await expect(durationPage.yearYearsSuffix()).toHaveText('Years')
    await expect(durationPage.mandatoryMonthMonthsSuffix()).toHaveText('Months')
  })

  test('Given the test_durations survey is selected when durations are entered then the summary screen shows the durations entered formatted', async ({
    page
  }) => {
    const durationPage = new DurationPage(page)
    const submitPage = new SubmitPage(page)
    await durationPage.yearMonthYears().fill('1')
    await durationPage.yearMonthMonths().fill('2')
    await durationPage.mandatoryYearMonthYears().fill('1')
    await durationPage.mandatoryYearMonthMonths().fill('2')
    await durationPage.mandatoryYearYears().fill('1')
    await durationPage.mandatoryMonthMonths().fill('1')
    await durationPage.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    await expect(submitPage.yearMonthAnswer()).toHaveText('1 year 2 months')
    await submitPage.submit().click()
  })

  test('Given the test_durations survey is selected when one of the units is 0 it is excluded from the summary', async ({ page }) => {
    const durationPage = new DurationPage(page)
    const submitPage = new SubmitPage(page)
    await durationPage.yearMonthYears().fill('0')
    await durationPage.yearMonthMonths().fill('2')
    await durationPage.mandatoryYearMonthYears().fill('1')
    await durationPage.mandatoryYearMonthMonths().fill('2')
    await durationPage.mandatoryYearYears().fill('1')
    await durationPage.mandatoryMonthMonths().fill('1')
    await durationPage.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    await expect(submitPage.yearMonthAnswer()).toHaveText('2 months')
    await submitPage.submit().click()
  })

  test('Given the test_durations survey is selected when no duration is entered the summary shows no answer provided', async ({ page }) => {
    const durationPage = new DurationPage(page)
    const submitPage = new SubmitPage(page)
    await durationPage.mandatoryYearMonthYears().fill('1')
    await durationPage.mandatoryYearMonthMonths().fill('2')
    await durationPage.mandatoryYearYears().fill('1')
    await durationPage.mandatoryMonthMonths().fill('1')
    await durationPage.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    await expect(submitPage.yearMonthAnswer()).toHaveText('No answer provided')
    await submitPage.submit().click()
  })

  test('Given the test_durations survey is selected when one of the units is missing an error is shown', async ({ page }) => {
    const durationPage = new DurationPage(page)
    await durationPage.yearMonthMonths().fill('2')
    await durationPage.mandatoryYearMonthMonths().fill('2')
    await durationPage.mandatoryYearYears().fill('1')
    await durationPage.mandatoryMonthMonths().fill('1')
    await durationPage.submit().click()

    await expect(durationPage.errorNumber(1)).toHaveText('Enter a valid duration')
    await expect(durationPage.errorNumber(2)).toHaveText('Enter a valid duration')
  })

  test('Given the test_durations survey is selected when one of the units not a number an error is shown', async ({ page }) => {
    const durationPage = new DurationPage(page)
    await durationPage.yearMonthYears().fill('word')
    await durationPage.yearMonthMonths().fill('2')
    await durationPage.mandatoryYearMonthYears().fill('word')
    await durationPage.mandatoryYearMonthMonths().fill('2')
    await durationPage.mandatoryYearYears().fill('1')
    await durationPage.mandatoryMonthMonths().fill('1')
    await durationPage.submit().click()

    await expect(durationPage.errorNumber(1)).toHaveText('Enter a valid duration')
    await expect(durationPage.errorNumber(2)).toHaveText('Enter a valid duration')
  })

  test('Given the test_durations survey is selected when the number of months is more than 11 an error is shown', async ({ page }) => {
    const durationPage = new DurationPage(page)
    await durationPage.yearMonthYears().fill('1')
    await durationPage.yearMonthMonths().fill('12')
    await durationPage.mandatoryYearMonthYears().fill('1')
    await durationPage.mandatoryYearMonthMonths().fill('12')
    await durationPage.mandatoryYearYears().fill('1')
    await durationPage.mandatoryMonthMonths().fill('1')
    await durationPage.submit().click()

    await expect(durationPage.errorNumber(1)).toHaveText('Enter a valid duration')
    await expect(durationPage.errorNumber(2)).toHaveText('Enter a valid duration')
  })

  test('Given the test_durations survey is selected when the mandatory duration is missing an error is shown', async ({ page }) => {
    const durationPage = new DurationPage(page)
    await durationPage.mandatoryYearYears().fill('1')
    await durationPage.mandatoryMonthMonths().fill('1')
    await durationPage.submit().click()

    await expect(durationPage.errorNumber(1)).toHaveText('Enter a duration')
  })
})
