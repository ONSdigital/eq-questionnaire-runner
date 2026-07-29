import { test, expect } from '../fixtures/test'
import DateRangePage from '../generated_pages/dates/date-range-block.page'
import DateMonthYearPage from '../generated_pages/dates/date-month-year-block.page'
import DateSinglePage from '../generated_pages/dates/date-single-block.page'
import DateNonMandatoryPage from '../generated_pages/dates/date-non-mandatory-block.page'
import DateYearDatePage from '../generated_pages/dates/date-year-date-block.page'
import SubmitPage from '../generated_pages/dates/submit.page'

test.describe('Date checks', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_dates.json')
  })

  test('Given an answer label is provided for a date question then the label should be displayed ', async ({ page }) => {
    const dateRangePage = new DateRangePage(page)
    await expect(dateRangePage.legend().first()).toHaveText('Period from')
  })

  test('Given an answer label is not provided for a date question then the question title should be used within the legend ', async ({ page }) => {
    const dateMonthYearPage = new DateMonthYearPage(page)
    const dateRangePage = new DateRangePage(page)
    await dateRangePage.dateRangeFromDay().fill('1')
    await dateRangePage.dateRangeFromMonth().fill('1')
    await dateRangePage.dateRangeFromYear().fill('1901')

    await dateRangePage.dateRangeToDay().fill('3')
    await dateRangePage.dateRangeToMonth().fill('5')
    await dateRangePage.dateRangeToYear().fill('2017')

    await dateRangePage.submit().click()

    await expect(dateMonthYearPage.legend()).toHaveText('Date with month and year')
  })

  test('Given the test_dates survey is selected when dates are entered then the summary screen shows the dates entered formatted', async ({ page }) => {
    const dateMonthYearPage = new DateMonthYearPage(page)
    const dateNonMandatoryPage = new DateNonMandatoryPage(page)
    const dateRangePage = new DateRangePage(page)
    const dateSinglePage = new DateSinglePage(page)
    const dateYearDatePage = new DateYearDatePage(page)
    const submitPage = new SubmitPage(page)
    await dateRangePage.dateRangeFromDay().fill('1')
    await dateRangePage.dateRangeFromMonth().fill('1')
    await dateRangePage.dateRangeFromYear().fill('1901')

    await dateRangePage.dateRangeToDay().fill('3')
    await dateRangePage.dateRangeToMonth().fill('5')
    await dateRangePage.dateRangeToYear().fill('2017')

    await dateRangePage.submit().click()

    await dateMonthYearPage.month().fill('4')
    await dateMonthYearPage.year().fill('2018')

    await dateMonthYearPage.submit().click()

    await dateSinglePage.day().fill('4')
    await dateSinglePage.month().fill('1')
    await dateSinglePage.year().fill('1999')

    await dateSinglePage.submit().click()

    await dateNonMandatoryPage.submit().click()

    await dateYearDatePage.year().fill('2005')

    await dateYearDatePage.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))

    await expect(submitPage.dateRangeFromAnswer()).toHaveText('1 January 1901 to 3 May 2017')
    await expect(submitPage.monthYearAnswer()).toHaveText('April 2018')
    await expect(submitPage.singleDateAnswer()).toHaveText('4 January 1999')
    await expect(submitPage.nonMandatoryDateAnswer()).toHaveText('No answer provided')
    await expect(submitPage.yearDateAnswer()).toHaveText('2005')
  })

  test('Given the test_dates survey is selected when the from date is greater than the to date then an error message is shown', async ({ page }) => {
    const dateRangePage = new DateRangePage(page)
    await dateRangePage.dateRangeFromDay().fill('1')
    await dateRangePage.dateRangeFromMonth().fill('1')
    await dateRangePage.dateRangeFromYear().fill('2016')

    await dateRangePage.dateRangeToDay().fill('1')
    await dateRangePage.dateRangeToMonth().fill('1')
    await dateRangePage.dateRangeToYear().fill('2015')

    await dateRangePage.submit().click()

    await expect(dateRangePage.errorNumber(1)).toHaveText("Enter a 'period to' date later than the 'period from' date")
    await expect(dateRangePage.dateRangeQuestionErrorPanel()).toBeVisible()

    await dateRangePage.errorNumber(1).click()
    await expect(dateRangePage.dateRangeFromDay()).toBeFocused()
  })

  test('Given the test_dates survey is selected when the from date and the to date are the same then an error message is shown', async ({ page }) => {
    const dateRangePage = new DateRangePage(page)
    await dateRangePage.dateRangeFromDay().fill('1')
    await dateRangePage.dateRangeFromMonth().fill('1')
    await dateRangePage.dateRangeFromYear().fill('2016')

    await dateRangePage.dateRangeToDay().fill('1')
    await dateRangePage.dateRangeToMonth().fill('1')
    await dateRangePage.dateRangeToYear().fill('2016')

    await dateRangePage.submit().click()

    await expect(dateRangePage.errorNumber(1)).toHaveText("Enter a 'period to' date later than the 'period from' date")
    await expect(dateRangePage.dateRangeQuestionErrorPanel()).toBeVisible()
  })

  test('Given the test_dates survey is selected when an invalid date is entered in a date range then an error message is shown', async ({ page }) => {
    const dateRangePage = new DateRangePage(page)
    await dateRangePage.dateRangeFromDay().fill('1')
    await dateRangePage.dateRangeFromMonth().fill('1')
    await dateRangePage.dateRangeFromYear().fill('2016')

    await dateRangePage.dateRangeToDay().fill('1')
    await dateRangePage.dateRangeToMonth().fill('1')
    await dateRangePage.dateRangeToYear().fill('')

    await dateRangePage.submit().click()

    await expect(dateRangePage.errorNumber(1)).toHaveText('Enter a valid date')
  })

  test('Given the test_dates survey is selected when the year (month year type) is left empty then an error message is shown', async ({ page }) => {
    const dateMonthYearPage = new DateMonthYearPage(page)
    const dateRangePage = new DateRangePage(page)
    await dateRangePage.dateRangeFromDay().fill('1')
    await dateRangePage.dateRangeFromMonth().fill('1')
    await dateRangePage.dateRangeFromYear().fill('2016')
    await dateRangePage.dateRangeToDay().fill('1')
    await dateRangePage.dateRangeToMonth().fill('1')
    await dateRangePage.dateRangeToYear().fill('2017')
    await dateRangePage.submit().click()

    await dateMonthYearPage.month().fill('4')
    await dateMonthYearPage.year().fill('')

    await dateMonthYearPage.submit().click()

    await expect(dateMonthYearPage.errorNumber(1)).toHaveText('Enter a valid date')
  })

  test('Given the test_dates survey is selected, When an error message is shown and it is corrected, Then the next question is displayed', async ({ page }) => {
    const dateMonthYearPage = new DateMonthYearPage(page)
    const dateRangePage = new DateRangePage(page)
    const dateSinglePage = new DateSinglePage(page)
    await dateRangePage.dateRangeFromDay().fill('1')
    await dateRangePage.dateRangeFromMonth().fill('1')
    await dateRangePage.dateRangeFromYear().fill('2016')
    await dateRangePage.dateRangeToDay().fill('1')
    await dateRangePage.dateRangeToMonth().fill('1')
    await dateRangePage.dateRangeToYear().fill('2017')
    await dateRangePage.submit().click()

    await dateMonthYearPage.month().fill('4')
    await dateMonthYearPage.year().fill('')
    await dateMonthYearPage.submit().click()

    await expect(dateMonthYearPage.error()).toHaveText('Enter a valid date')

    await dateMonthYearPage.year().fill('2018')
    await dateMonthYearPage.submit().click()

    await expect(page).toHaveURL(new RegExp(dateSinglePage.url()))
  })

  test('Given the test_dates survey is selected when an error message is shown then when it is corrected, it goes to the summary page and the information is correct', async ({
    page
  }) => {
    const dateMonthYearPage = new DateMonthYearPage(page)
    const dateNonMandatoryPage = new DateNonMandatoryPage(page)
    const dateRangePage = new DateRangePage(page)
    const dateSinglePage = new DateSinglePage(page)
    await dateRangePage.dateRangeFromDay().fill('1')
    await dateRangePage.dateRangeFromMonth().fill('1')
    await dateRangePage.dateRangeFromYear().fill('2016')
    await dateRangePage.dateRangeToDay().fill('1')
    await dateRangePage.dateRangeToMonth().fill('1')
    await dateRangePage.dateRangeToYear().fill('2017')
    await dateRangePage.submit().click()

    await dateMonthYearPage.month().fill('1')
    await dateMonthYearPage.year().fill('2016')
    await dateMonthYearPage.submit().click()

    await dateSinglePage.day().fill('1')
    await dateSinglePage.month().fill('1')
    await dateSinglePage.year().fill('2016')
    await dateMonthYearPage.submit().click()

    await dateNonMandatoryPage.day().fill('4')
    await dateNonMandatoryPage.month().fill('1')
    await dateNonMandatoryPage.submit().click()

    await expect(dateNonMandatoryPage.errorNumber(1)).toHaveText('Enter a valid date')
  })

  test('Given the test_dates survey is selected, When a user clicks the day label then the day subfield should gain the focus', async ({ page }) => {
    const dateMonthYearPage = new DateMonthYearPage(page)
    const dateRangePage = new DateRangePage(page)
    const dateSinglePage = new DateSinglePage(page)
    await dateRangePage.dateRangeFromDay().fill('1')
    await dateRangePage.dateRangeFromMonth().fill('1')
    await dateRangePage.dateRangeFromYear().fill('2016')
    await dateRangePage.dateRangeToDay().fill('1')
    await dateRangePage.dateRangeToMonth().fill('1')
    await dateRangePage.dateRangeToYear().fill('2017')
    await dateRangePage.submit().click()

    await dateMonthYearPage.month().fill('1')
    await dateMonthYearPage.year().fill('2016')
    await dateMonthYearPage.submit().click()

    await dateSinglePage.dayLabel().click()

    await expect(dateSinglePage.day()).toBeFocused()
  })
})
