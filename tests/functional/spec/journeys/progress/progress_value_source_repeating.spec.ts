import { test, expect } from '../../../fixtures/test'
import HubPage from '../../../base_pages/hub.page'
import ListCollectorPage from '../../../generated_pages/new_calculated_summary_repeating_section/list-collector.page'
import ListCollectorAddPage from '../../../generated_pages/new_calculated_summary_repeating_section/list-collector-add.page'
import QuestionBlockPage from '../../../generated_pages/progress_block_value_source_repeating_sections/question-block.page'
import DOBQuestionBlockPage from '../../../generated_pages/progress_block_value_source_repeating_sections/dob-block.page'
import RandomQuestionEnablerBlockPage from '../../../generated_pages/progress_block_value_source_repeating_sections/random-question-enabler-block.page'
import SectionTwoSummaryPage from '../../../generated_pages/progress_block_value_source_repeating_sections/section-2-summary.page'
import SectionThreeSummaryPage from '../../../generated_pages/progress_value_source_calculated_summary/section-3-summary.page'
import OtherQuestionBlockPage from '../../../generated_pages/progress_block_value_source_repeating_sections/other-question-block.page'
import FirstNumberBlockPage from '../../../generated_pages/progress_value_source_calculated_summary/first-number-block.page'
import SecondNumberBlockPage from '../../../generated_pages/progress_value_source_calculated_summary/second-number-block.page'
import SectionTwoQuestionBlockPage from '../../../generated_pages/progress_value_source_calculated_summary/s2-b1.page'
import CalculatedSummaryBlockPage from '../../../generated_pages/progress_value_source_calculated_summary/calculated-summary-block.page'

test.describe('Feature: Routing rules based on progress value sources in repeating sections', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_progress_block_value_source_repeating_sections.json')
  })

  test('When the block is incomplete, then the dependent question should not be visible in the repeating section', async ({ page }) => {
    const hubPage = new HubPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const listCollectorAddPage = new ListCollectorAddPage(page)
    const questionBlockPage = new QuestionBlockPage(page)
    const dobQuestionBlockPage = new DOBQuestionBlockPage(page)
    const sectionTwoSummaryPage = new SectionTwoSummaryPage(page)

    await hubPage.submit().click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await listCollectorAddPage.firstName().fill('John')
    await listCollectorAddPage.lastName().fill('Doe')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await expect(page).toHaveURL(new RegExp(questionBlockPage.pageName))

    await page.goto(hubPage.url())
    await expect(hubPage.summaryRowState('section-1')).toHaveText('Partially completed')

    await hubPage.summaryRowLink('section-2-1').click()
    await dobQuestionBlockPage.submit().click()
    await expect(page).toHaveURL(new RegExp(sectionTwoSummaryPage.pageName))
  })

  test('When the block is complete, then the dependent question should be visible in the repeating section', async ({ page }) => {
    const hubPage = new HubPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const listCollectorAddPage = new ListCollectorAddPage(page)
    const questionBlockPage = new QuestionBlockPage(page)
    const dobQuestionBlockPage = new DOBQuestionBlockPage(page)
    const randomQuestionEnablerBlockPage = new RandomQuestionEnablerBlockPage(page)
    const otherQuestionBlockPage = new OtherQuestionBlockPage(page)

    await hubPage.submit().click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await listCollectorAddPage.firstName().fill('John')
    await listCollectorAddPage.lastName().fill('Doe')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await questionBlockPage.submit().click()
    await randomQuestionEnablerBlockPage.randomQuestionEnabler().fill('1')
    await randomQuestionEnablerBlockPage.submit().click()

    await page.goto(hubPage.url())
    await expect(hubPage.summaryRowState('section-1')).toHaveText('Completed')

    await hubPage.summaryRowLink('section-2-1').click()
    await dobQuestionBlockPage.submit().click()
    await expect(page).toHaveURL(new RegExp(otherQuestionBlockPage.pageName))
  })

  test('When block status changes from incomplete to complete, Then dependent repeating-section routing should update', async ({ page }) => {
    const hubPage = new HubPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const listCollectorAddPage = new ListCollectorAddPage(page)
    const questionBlockPage = new QuestionBlockPage(page)
    const dobQuestionBlockPage = new DOBQuestionBlockPage(page)
    const randomQuestionEnablerBlockPage = new RandomQuestionEnablerBlockPage(page)
    const sectionTwoSummaryPage = new SectionTwoSummaryPage(page)

    await hubPage.submit().click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await listCollectorAddPage.firstName().fill('John')
    await listCollectorAddPage.lastName().fill('Doe')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await listCollectorAddPage.firstName().fill('Joe')
    await listCollectorAddPage.lastName().fill('Bloggs')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()

    await page.goto(hubPage.url())
    await expect(hubPage.summaryRowState('section-2-1')).toHaveText('Not started')
    await expect(hubPage.summaryRowState('section-2-2')).toHaveText('Not started')

    await hubPage.summaryRowLink('section-2-1').click()
    await dobQuestionBlockPage.submit().click()
    await sectionTwoSummaryPage.submit().click()
    await expect(hubPage.summaryRowState('section-2-1')).toHaveText('Completed')
    await expect(hubPage.summaryRowState('section-2-2')).toHaveText('Not started')

    await hubPage.submit().click()
    await questionBlockPage.submit().click()
    await randomQuestionEnablerBlockPage.randomQuestionEnabler().fill('1')
    await randomQuestionEnablerBlockPage.submit().click()

    await expect(hubPage.summaryRowState('section-2-1')).toHaveText('Partially completed')
    await expect(hubPage.summaryRowState('section-2-2')).toHaveText('Not started')
  })
})

test.describe('Feature: Routing rules based on progress value sources from calculated summaries in repeating sections', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_progress_value_source_calculated_summary.json')
  })

  test('When calculated summary is incomplete, then dependent repeating-section question should not appear', async ({ page }) => {
    const hubPage = new HubPage(page)
    const firstNumberBlockPage = new FirstNumberBlockPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const listCollectorAddPage = new ListCollectorAddPage(page)
    const dobQuestionBlockPage = new DOBQuestionBlockPage(page)
    const sectionThreeSummaryPage = new SectionThreeSummaryPage(page)

    await hubPage.submit().click()
    await firstNumberBlockPage.firstNumber().fill('1')
    await firstNumberBlockPage.submit().click()
    await page.goto(hubPage.url())

    await hubPage.summaryRowLink('section-2').click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await listCollectorAddPage.firstName().fill('John')
    await listCollectorAddPage.lastName().fill('Doe')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await expect(page).toHaveURL(new RegExp(hubPage.pageName))

    await hubPage.summaryRowLink('section-3-1').click()
    await dobQuestionBlockPage.submit().click()
    await sectionThreeSummaryPage.submit().click()

    await expect(hubPage.summaryRowState('section-1')).toHaveText('Partially completed')
    await expect(hubPage.summaryRowState('section-2')).toHaveText('Completed')
    await expect(hubPage.summaryRowState('section-3-1')).toHaveText('Completed')
  })

  test('When calculated summary is updated from incomplete to complete, then repeating-section dependency should update', async ({ page }) => {
    const hubPage = new HubPage(page)
    const firstNumberBlockPage = new FirstNumberBlockPage(page)
    const secondNumberBlockPage = new SecondNumberBlockPage(page)
    const calculatedSummaryBlockPage = new CalculatedSummaryBlockPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const listCollectorAddPage = new ListCollectorAddPage(page)
    const dobQuestionBlockPage = new DOBQuestionBlockPage(page)
    const sectionThreeSummaryPage = new SectionThreeSummaryPage(page)

    await hubPage.submit().click()
    await firstNumberBlockPage.firstNumber().fill('1')
    await firstNumberBlockPage.submit().click()
    await page.goto(hubPage.url())

    await hubPage.summaryRowLink('section-2').click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await listCollectorAddPage.firstName().fill('John')
    await listCollectorAddPage.lastName().fill('Doe')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await expect(page).toHaveURL(new RegExp(hubPage.pageName))

    await hubPage.summaryRowLink('section-3-1').click()
    await dobQuestionBlockPage.submit().click()
    await sectionThreeSummaryPage.submit().click()

    await expect(hubPage.summaryRowState('section-1')).toHaveText('Partially completed')
    await expect(hubPage.summaryRowState('section-2')).toHaveText('Completed')
    await expect(hubPage.summaryRowState('section-3-1')).toHaveText('Completed')

    await hubPage.summaryRowLink('section-1').click()
    await secondNumberBlockPage.secondNumber().fill('2')
    await secondNumberBlockPage.submit().click()
    await calculatedSummaryBlockPage.submit().click()
    await page.goto(hubPage.url())

    await expect(hubPage.summaryRowState('section-1')).toHaveText('Completed')
    await expect(hubPage.summaryRowState('section-2')).toHaveText('Partially completed')
    await expect(hubPage.summaryRowState('section-3-1')).toHaveText('Partially completed')
  })

  test('When calculated summary is complete, then dependent repeating-section question should appear', async ({ page }) => {
    const hubPage = new HubPage(page)
    const firstNumberBlockPage = new FirstNumberBlockPage(page)
    const secondNumberBlockPage = new SecondNumberBlockPage(page)
    const calculatedSummaryBlockPage = new CalculatedSummaryBlockPage(page)
    const sectionTwoQuestionBlockPage = new SectionTwoQuestionBlockPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const listCollectorAddPage = new ListCollectorAddPage(page)
    const dobQuestionBlockPage = new DOBQuestionBlockPage(page)
    const otherQuestionBlockPage = new OtherQuestionBlockPage(page)

    await hubPage.submit().click()
    await firstNumberBlockPage.firstNumber().fill('1')
    await firstNumberBlockPage.submit().click()
    await secondNumberBlockPage.secondNumber().fill('2')
    await secondNumberBlockPage.submit().click()
    await calculatedSummaryBlockPage.submit().click()
    await page.goto(hubPage.url())

    await hubPage.summaryRowLink('section-2').click()
    await sectionTwoQuestionBlockPage.q1A1().fill('1')
    await sectionTwoQuestionBlockPage.submit().click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await listCollectorAddPage.firstName().fill('John')
    await listCollectorAddPage.lastName().fill('Doe')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await expect(page).toHaveURL(new RegExp(hubPage.pageName))

    await hubPage.summaryRowLink('section-3-1').click()
    await dobQuestionBlockPage.submit().click()
    await expect(page).toHaveURL(new RegExp(otherQuestionBlockPage.pageName))
  })
})
