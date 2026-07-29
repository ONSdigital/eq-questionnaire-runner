import { test, expect } from '../../../fixtures/test'
import AgeBlockYearPage from '../../../generated_pages/placeholder_difference_in_years/age-block.page'
import AgeTestYearPage from '../../../generated_pages/placeholder_difference_in_years/age-test.page'
import AgeBlockMonthYearPage from '../../../generated_pages/placeholder_difference_in_years_month_year/age-block.page'
import AgeTestMonthYearPage from '../../../generated_pages/placeholder_difference_in_years_month_year/age-test.page'
import AgeBlockDayMonthYearRangePage from '../../../generated_pages/placeholder_difference_in_years_range/date-block.page'
import AgeTestDayMonthYearRangePage from '../../../generated_pages/placeholder_difference_in_years_range/age-test.page'
import AgeBlockMonthYearRangePage from '../../../generated_pages/placeholder_difference_in_years_month_year_range/date-block.page'
import AgeTestMonthYearRangePage from '../../../generated_pages/placeholder_difference_in_years_month_year_range/age-test.page'

test.describe('Difference check (years)', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_placeholder_difference_in_years.json')
  })

  test('Given a day, month and year answer is provided for a date question then the age in years should be calculated and displayed on the page ', async ({
    page
  }) => {
    const ageBlockYearPage = new AgeBlockYearPage(page)
    const ageTestYearPage = new AgeTestYearPage(page)
    await ageBlockYearPage.day().fill('1')
    await ageBlockYearPage.month().fill('1')
    await ageBlockYearPage.year().fill('1990')
    await ageBlockYearPage.submit().click()
    await expect(ageTestYearPage.heading()).toHaveText(`You are ${getYears('1990/01/01')} years old. Is this correct?`)
  })
})

test.describe('Difference check (months and years)', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_placeholder_difference_in_years_month_year.json')
  })

  test('Given a month and year answer is provided for a date question then the difference in years should be calculated and displayed on the page ', async ({
    page
  }) => {
    const ageBlockMonthYearPage = new AgeBlockMonthYearPage(page)
    const ageTestMonthYearPage = new AgeTestMonthYearPage(page)
    await ageBlockMonthYearPage.month().fill('1')
    await ageBlockMonthYearPage.year().fill('1990')

    await ageBlockMonthYearPage.submit().click()

    await expect(ageTestMonthYearPage.heading()).toHaveText(`It has been ${getYears('1990/01/01')} years since you last went on holiday. Is this correct?`)
  })
})

test.describe('Difference check (months and years range)', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_placeholder_difference_in_years_month_year_range.json')
  })

  test(
    "Given a month and year answers 'from' and 'to' are provided for a date question " +
      'then the difference in years should be calculated and displayed on the page ',
    async ({ page }) => {
      const ageBlockMonthYearRangePage = new AgeBlockMonthYearRangePage(page)
      const ageTestMonthYearRangePage = new AgeTestMonthYearRangePage(page)
      await ageBlockMonthYearRangePage.periodFromMonth().fill('1')
      await ageBlockMonthYearRangePage.periodFromYear().fill('1990')
      await ageBlockMonthYearRangePage.periodToMonth().fill('1')
      await ageBlockMonthYearRangePage.periodToYear().fill('1991')

      await ageBlockMonthYearRangePage.submit().click()

      await expect(ageTestMonthYearRangePage.heading()).toHaveText('You were out of the UK for 1 year. Is this correct?')
    }
  )
})

test.describe('Difference check (years range)', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_placeholder_difference_in_years_range.json')
  })

  test(
    "Given a day, month and year answers 'from' and 'to' are provided for a date question " +
      'then the difference in years should be calculated and displayed on the page ',
    async ({ page }) => {
      const ageBlockDayMonthYearRangePage = new AgeBlockDayMonthYearRangePage(page)
      const ageTestDayMonthYearRangePage = new AgeTestDayMonthYearRangePage(page)
      await ageBlockDayMonthYearRangePage.periodFromDay().fill('1')
      await ageBlockDayMonthYearRangePage.periodFromMonth().fill('1')
      await ageBlockDayMonthYearRangePage.periodFromYear().fill('1990')

      await ageBlockDayMonthYearRangePage.periodToDay().fill('1')
      await ageBlockDayMonthYearRangePage.periodToMonth().fill('1')
      await ageBlockDayMonthYearRangePage.periodToYear().fill('1991')

      await ageBlockDayMonthYearRangePage.submit().click()

      await expect(ageTestDayMonthYearRangePage.heading()).toHaveText('You were out of the UK for 1 year. Is this correct?')
    }
  )
})

function getYears (date: string): number {
  return new Date(new Date().getTime() - new Date(date).getTime()).getFullYear() - 1970
}
