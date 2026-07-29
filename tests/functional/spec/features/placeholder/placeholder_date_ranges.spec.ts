import { test, expect } from '../../../fixtures/test'
import DateQuestionPage from '../../../generated_pages/placeholder_transform_date_range_bounds/date-question.page'
import DaysQuestionBlockPage from '../../../generated_pages/placeholder_transform_date_range_bounds/days-question-block.page'
import Block0Page from '../../../generated_pages/placeholder_transform_date_range_bounds/block0.page'
import RangeQuestionBlockPage from '../../../generated_pages/placeholder_transform_date_range_bounds/range-question-block.page'

test.describe('Date checks', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_placeholder_transform_date_range_bounds.json')
  })

  test('Given a reference date is provided, When I get to the next page, Then the placeholder contains a formatted date range based on the reference date', async ({
    page
  }) => {
    const dateQuestionPage = new DateQuestionPage(page)
    const daysQuestionBlockPage = new DaysQuestionBlockPage(page)
    await dateQuestionPage.day().fill('8')
    await dateQuestionPage.month().fill('9')
    await dateQuestionPage.year().fill('2021')

    await dateQuestionPage.submit().click()

    await expect(daysQuestionBlockPage.questionText()).toContainText('Monday 30 August to Monday 13 September 2021')
    await daysQuestionBlockPage.submit().click()
  })

  test('Given a reference date is provided, When I get to the next page, Then the placeholder contains a formatted date range', async ({ page }) => {
    const block0Page = new Block0Page(page)
    const dateQuestionPage = new DateQuestionPage(page)
    const daysQuestionBlockPage = new DaysQuestionBlockPage(page)
    const rangeQuestionBlockPage = new RangeQuestionBlockPage(page)
    await dateQuestionPage.day().fill('15')
    await dateQuestionPage.month().fill('9')
    await dateQuestionPage.year().fill('2021')

    await dateQuestionPage.submit().click()
    await daysQuestionBlockPage.submit().click()

    await block0Page.ref0Day().fill('1')
    await block0Page.ref0Month().fill('5')
    await block0Page.ref0Year().fill('2019')

    await block0Page.ref1Day().fill('19')
    await block0Page.ref1Month().fill('5')
    await block0Page.ref1Year().fill('2019')

    await block0Page.submit().click()

    await expect(rangeQuestionBlockPage.questionText()).toContainText('Wednesday 1 to Sunday 19 May 2019')
  })
})
