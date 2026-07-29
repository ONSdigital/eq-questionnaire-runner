import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../fixtures/test'
import HubPage from '../../../base_pages/hub.page'
import IntroductionBlockPage from '../../../generated_pages/grand_calculated_summary_overlapping_answers/introduction-block.page'
import Block1Page from '../../../generated_pages/grand_calculated_summary_overlapping_answers/block-1.page'
import Block2Page from '../../../generated_pages/grand_calculated_summary_overlapping_answers/block-2.page'
import CalculatedSummary1Page from '../../../generated_pages/grand_calculated_summary_overlapping_answers/calculated-summary-1.page'
import CalculatedSummary2Page from '../../../generated_pages/grand_calculated_summary_overlapping_answers/calculated-summary-2.page'
import Block3Page from '../../../generated_pages/grand_calculated_summary_overlapping_answers/block-3.page'
import CalculatedSummary4Page from '../../../generated_pages/grand_calculated_summary_overlapping_answers/calculated-summary-4.page'
import GrandCalculatedSummaryShoppingPage from '../../../generated_pages/grand_calculated_summary_overlapping_answers/grand-calculated-summary-shopping.page'
import Section1SummaryPage from '../../../generated_pages/grand_calculated_summary_overlapping_answers/section-1-summary.page'

test.describe('Feature: Grand Calculated Summary', () => {
  test.describe('Given I have a Grand Calculated Summary with overlapping answers', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('completing the survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)

      const block1Page = new Block1Page(page)
      const block2Page = new Block2Page(page)
      const block3Page = new Block3Page(page)
      const calculatedSummary1Page = new CalculatedSummary1Page(page)
      const calculatedSummary2Page = new CalculatedSummary2Page(page)
      const calculatedSummary4Page = new CalculatedSummary4Page(page)
      const grandCalculatedSummaryShoppingPage = new GrandCalculatedSummaryShoppingPage(page)
      const hubPage = new HubPage(page)
      const introductionBlockPage = new IntroductionBlockPage(page)
      const section1SummaryPage = new Section1SummaryPage(page)
      await openQuestionnaire('test_grand_calculated_summary_overlapping_answers.json')
      await introductionBlockPage.submit().click()

      // grand calculated summary should not be enabled until section-1 complete
      await expect(hubPage.summaryRowLink('section-3')).toBeHidden()

      await hubPage.submit().click()
      await block1Page.q1A1().fill('100')
      await block1Page.q1A2().fill('200')
      await block1Page.submit().click()
      await block2Page.q2A1().fill('10')
      await block2Page.q2A2().fill('20')
      await block2Page.submit().click()
      await calculatedSummary1Page.submit().click()
      await calculatedSummary2Page.submit().click()
      await block3Page.yesExtraBreadAndCheese().click()
      await block3Page.submit().click()
      await calculatedSummary4Page.submit().click()
      await section1SummaryPage.submit().click()
      await hubPage.submit().click()
      await expect(grandCalculatedSummaryShoppingPage.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary of purchases this week comes to £360.00. Is this correct?.'
      )
      await grandCalculatedSummaryShoppingPage.submit().click()
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('Given I edit an answer that is only used in a single calculated summary, I am routed back to the calculated summary and then the grand calculated summary and the correct fields are focused', async () => {
      const block1Page = new Block1Page(page)
      const calculatedSummary2Page = new CalculatedSummary2Page(page)
      const grandCalculatedSummaryShoppingPage = new GrandCalculatedSummaryShoppingPage(page)
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink('section-3').click()
      await grandCalculatedSummaryShoppingPage.calculatedSummary2Edit().click()
      await calculatedSummary2Page.q1A2Edit().click()
      await block1Page.q1A2().fill('300')
      await block1Page.submit().click()

      // taken back to calculated summary
      await expect(page).toHaveURL(new RegExp(calculatedSummary2Page.pageName))
      await expect(page).toHaveURL(
        new RegExp(
          '/questionnaire/calculated-summary-2/\\?return_to=grand-calculated-summary' +
            '&return_to_block_id=grand-calculated-summary-shopping&return_to_answer_id=calculated-summary-2#q1-a2'
        )
      )
      await calculatedSummary2Page.submit().click()

      // then grand calculated summary
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryShoppingPage.pageName))
      await expect(grandCalculatedSummaryShoppingPage.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary of purchases this week comes to £460.00. Is this correct?.'
      )
      await expect(page).toHaveURL(/\/questionnaire\/grand-calculated-summary-shopping\/#calculated-summary-2/)
    })

    test('Given I edit an answer that is used in two calculated summaries, if I edit it from the first calculated summary change link, I taken through each block between the question and the second calculated summary before returning to the grand calculated summary', async () => {
      const block2Page = new Block2Page(page)
      const calculatedSummary2Page = new CalculatedSummary2Page(page)
      const calculatedSummary4Page = new CalculatedSummary4Page(page)
      const grandCalculatedSummaryShoppingPage = new GrandCalculatedSummaryShoppingPage(page)
      await grandCalculatedSummaryShoppingPage.calculatedSummary2Edit().click()
      await calculatedSummary2Page.q2A2Edit().click()
      await block2Page.q2A2().fill('400')
      await block2Page.submit().click()

      // taken back to the FIRST calculated summary which uses it
      await expect(page).toHaveURL(new RegExp(calculatedSummary2Page.pageName))
      await expect(calculatedSummary2Page.calculatedSummaryTitle()).toHaveText('Total of eggs and cheese is calculated to be £700.00. Is this correct?')
      await calculatedSummary2Page.submit().click()

      // taken back to the SECOND calculated summary which uses it
      await expect(page).toHaveURL(new RegExp(calculatedSummary4Page.pageName))
      await expect(calculatedSummary4Page.calculatedSummaryTitle()).toContainText('Total extra items cost is calculated to be £410.00. Is this correct?')
      await calculatedSummary4Page.submit().click()

      // then grand calculated summary
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryShoppingPage.pageName))
      await expect(grandCalculatedSummaryShoppingPage.grandCalculatedSummaryTitle()).toContainText(
        'Grand Calculated Summary of purchases this week comes to £1,220.00. Is this correct?'
      )
    })

    test('Given I edit an answer that is used in two calculated summaries, if I edit it from the second calculated summary change link, I taken through each block between the question and the second calculated summary before returning to the grand calculated summary', async () => {
      const block2Page = new Block2Page(page)
      const calculatedSummary2Page = new CalculatedSummary2Page(page)
      const calculatedSummary4Page = new CalculatedSummary4Page(page)
      const grandCalculatedSummaryShoppingPage = new GrandCalculatedSummaryShoppingPage(page)
      await grandCalculatedSummaryShoppingPage.calculatedSummary4Edit().click()
      await calculatedSummary4Page.q2A2Edit().click()
      await block2Page.q2A2().fill('500')
      await block2Page.submit().click()

      // taken back to the FIRST calculated summary which uses it
      await expect(page).toHaveURL(new RegExp(calculatedSummary2Page.pageName))
      await expect(calculatedSummary2Page.calculatedSummaryTitle()).toHaveText('Total of eggs and cheese is calculated to be £800.00. Is this correct?')
      await calculatedSummary2Page.submit().click()

      // taken back to the SECOND calculated summary which uses it
      await expect(page).toHaveURL(new RegExp(calculatedSummary4Page.pageName))
      await expect(calculatedSummary4Page.calculatedSummaryTitle()).toContainText('Total extra items cost is calculated to be £510.00. Is this correct?')
      await calculatedSummary4Page.submit().click()

      // then grand calculated summary
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryShoppingPage.pageName))
      await expect(grandCalculatedSummaryShoppingPage.grandCalculatedSummaryTitle()).toContainText(
        'Grand Calculated Summary of purchases this week comes to £1,420.00. Is this correct?'
      )
      await grandCalculatedSummaryShoppingPage.submit().click()
    })

    test('Given I change an answer and return to the Hub before all calculated summaries are confirmed, the grand calculated summary section becomes inaccessible', async () => {
      const block2Page = new Block2Page(page)
      const calculatedSummary2Page = new CalculatedSummary2Page(page)
      const calculatedSummary4Page = new CalculatedSummary4Page(page)
      const grandCalculatedSummaryShoppingPage = new GrandCalculatedSummaryShoppingPage(page)
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink('section-3').click()
      await grandCalculatedSummaryShoppingPage.calculatedSummary4Edit().click()
      await calculatedSummary4Page.q2A2Edit().click()
      await block2Page.q2A2().fill('50')
      await block2Page.submit().click()

      // confirm one of the calculated summaries but return to the hub instead of confirming the other
      await calculatedSummary2Page.submit().click()
      await page.goto(hubPage.url())

      // calculated summary 4 is not confirmed so GCS doesn't show
      await expect(hubPage.summaryRowState('section-1')).toHaveText('Partially completed')
      await expect(hubPage.summaryRowLink('section-3')).toBeHidden()
    })

    test('Given I complete the calculated and grand calculated summaries, When I return to the Hub, Then I see a new conditional section has opened up', async () => {
      const calculatedSummary4Page = new CalculatedSummary4Page(page)
      const grandCalculatedSummaryShoppingPage = new GrandCalculatedSummaryShoppingPage(page)
      const hubPage = new HubPage(page)
      const section1SummaryPage = new Section1SummaryPage(page)
      await hubPage.submit().click()
      await expect(page).toHaveURL(new RegExp(calculatedSummary4Page.pageName))
      await calculatedSummary4Page.submit().click()
      await section1SummaryPage.submit().click()
      await hubPage.submit().click()
      await expect(grandCalculatedSummaryShoppingPage.grandCalculatedSummaryTitle()).toContainText(
        'Grand Calculated Summary of purchases this week comes to £520.00. Is this correct?'
      )
      await grandCalculatedSummaryShoppingPage.submit().click()
      await expect(hubPage.summaryRowState('section-1')).toHaveText('Completed')
      await expect(hubPage.summaryRowState('section-3')).toHaveText('Completed')
      await expect(hubPage.summaryRowLink('section-4')).toBeVisible()
    })

    test('Given I change my answer about purchasing additional items decreasing the gcs, When I return to the Hub, Then I see the conditional section is gone', async () => {
      const block3Page = new Block3Page(page)
      const hubPage = new HubPage(page)
      const section1SummaryPage = new Section1SummaryPage(page)
      await hubPage.summaryRowLink('section-1').click()
      await section1SummaryPage.radioExtraEdit().click()
      await block3Page.no().click()
      await block3Page.submit().click()
      await section1SummaryPage.submit().click()
      await expect(hubPage.summaryRowState('section-1')).toHaveText('Completed')
      await expect(hubPage.summaryRowState('section-3')).toHaveText('Completed')
      await expect(hubPage.summaryRowLink('section-4')).toBeHidden()
    })
  })
})
