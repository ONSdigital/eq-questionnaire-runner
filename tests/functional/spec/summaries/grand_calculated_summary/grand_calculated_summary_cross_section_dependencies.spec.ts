import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../fixtures/test'
import SkipFirstBlockPage from '../../../generated_pages/grand_calculated_summary_cross_section_dependencies/skip-first-block.page'
import SecondNumberBlockPage from '../../../generated_pages/grand_calculated_summary_cross_section_dependencies/second-number-block.page'
import HubPage from '../../../base_pages/hub.page'
import CurrencySection1Page from '../../../generated_pages/grand_calculated_summary_cross_section_dependencies/currency-section-1.page'
import QuestionsSectionSummaryPage from '../../../generated_pages/grand_calculated_summary_cross_section_dependencies/questions-section-summary.page'
import ThirdNumberBlockPage from '../../../generated_pages/grand_calculated_summary_cross_section_dependencies/third-number-block.page'
import SkipCalculatedSummaryPage from '../../../generated_pages/grand_calculated_summary_cross_section_dependencies/skip-calculated-summary.page'
import CalculatedSummarySectionSummaryPage from '../../../generated_pages/grand_calculated_summary_cross_section_dependencies/calculated-summary-section-summary.page'
import CurrencyQuestion3Page from '../../../generated_pages/grand_calculated_summary_cross_section_dependencies/currency-question-3.page'
import CurrencyAllPage from '../../../generated_pages/grand_calculated_summary_cross_section_dependencies/currency-all.page'
import FirstNumberBlockPartAPage from '../../../generated_pages/grand_calculated_summary_cross_section_dependencies/first-number-block-part-a.page'
import FourthNumberBlockPage from '../../../generated_pages/grand_calculated_summary_cross_section_dependencies/fourth-number-block.page'
import TvChoiceBlockPage from '../../../generated_pages/grand_calculated_summary_cross_section_dependencies/tv-choice-block.page'

test.describe('Feature: Grand Calculated Summary', () => {
  test.describe('Given I have a Grand Calculated Summary', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Getting to the second calculated summary', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      const currencySection1Page = new CurrencySection1Page(page)
      const firstNumberBlockPartAPage = new FirstNumberBlockPartAPage(page)
      const hubPage = new HubPage(page)
      const questionsSectionSummaryPage = new QuestionsSectionSummaryPage(page)
      const secondNumberBlockPage = new SecondNumberBlockPage(page)
      const skipFirstBlockPage = new SkipFirstBlockPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await openQuestionnaire('test_grand_calculated_summary_cross_section_dependencies.json')
      await hubPage.submit().click()
      await skipFirstBlockPage.no().click()
      await skipFirstBlockPage.submit().click()
      await firstNumberBlockPartAPage.firstNumberA().fill('300')
      await firstNumberBlockPartAPage.submit().click()
      await secondNumberBlockPage.secondNumberA().fill('10')
      await secondNumberBlockPage.secondNumberB().fill('5')
      await secondNumberBlockPage.secondNumberC().fill('15')
      await secondNumberBlockPage.submit().click()
      await currencySection1Page.submit().click()
      await questionsSectionSummaryPage.submit().click()
      // section 2
      await hubPage.submit().click()
      await thirdNumberBlockPage.thirdNumberPartA().fill('70')
      await thirdNumberBlockPage.submit().click()
    })

    test.afterAll(async () => {
      await context.close()
    })

    test("Given I don't skip the second calculated summary, it is included in the grand calculated summary", async () => {
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyAllPage = new CurrencyAllPage(page)
      const currencyQuestion3Page = new CurrencyQuestion3Page(page)
      const hubPage = new HubPage(page)
      const skipCalculatedSummaryPage = new SkipCalculatedSummaryPage(page)
      const tvChoiceBlockPage = new TvChoiceBlockPage(page)
      await skipCalculatedSummaryPage.no().click()
      await skipCalculatedSummaryPage.submit().click()
      await currencyQuestion3Page.submit().click()
      await tvChoiceBlockPage.television().click()
      await tvChoiceBlockPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()
      await hubPage.submit().click()
      await expect(currencyAllPage.currencySection1()).toHaveText('£330.00')
      await expect(currencyAllPage.currencyQuestion3()).toHaveText('£70.00')
      await expect(currencyAllPage.grandCalculatedSummaryTitle()).toHaveText('The grand calculated summary is calculated to be £400.00. Is this correct?')
      await currencyAllPage.submit().click()
    })

    test('Given I go back and skip the second calculated summary, it is not included in the grand calculated summary', async () => {
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyAllPage = new CurrencyAllPage(page)
      const hubPage = new HubPage(page)
      const skipCalculatedSummaryPage = new SkipCalculatedSummaryPage(page)
      await hubPage.summaryRowLink('calculated-summary-section').click()
      await calculatedSummarySectionSummaryPage.skipAnswer2Edit().click()
      await skipCalculatedSummaryPage.yes().click()
      await skipCalculatedSummaryPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()
      // Currently the grand calculated summary remains 'Completed' because none of the answers have changed
      await expect(hubPage.summaryRowState('grand-calculated-summary-section')).toHaveText('Completed')
      await hubPage.summaryRowLink('grand-calculated-summary-section').click()
      await expect(currencyAllPage.grandCalculatedSummaryTitle()).toHaveText('The grand calculated summary is calculated to be £330.00. Is this correct?')
      await expect(currencyAllPage.currencyQuestion3()).not.toBeVisible()
    })

    test('Given I confirm the grand calculated summary, then edit an answer for question 3, the grand calculated summary updates to be incomplete, because this is a dependency', async () => {
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyAllPage = new CurrencyAllPage(page)
      const hubPage = new HubPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await currencyAllPage.submit().click()
      await hubPage.summaryRowLink('calculated-summary-section').click()
      await calculatedSummarySectionSummaryPage.thirdNumberAnswerPartAEdit().click()
      await thirdNumberBlockPage.thirdNumberPartA().fill('130')
      await thirdNumberBlockPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()
      // Although the calculated summary is not on the path, the answer is still a grand calculated summary dependency, so it updates progress
      await expect(hubPage.summaryRowState('grand-calculated-summary-section')).toHaveText('Partially completed')
      await hubPage.summaryRowLink('grand-calculated-summary-section').click()
      await expect(currencyAllPage.grandCalculatedSummaryTitle()).toHaveText('The grand calculated summary is calculated to be £330.00. Is this correct?')
      await expect(currencyAllPage.currencyQuestion3()).not.toBeVisible()
      await currencyAllPage.submit().click()
    })

    test('Given I change my response to include the calculated summary, When I press continue, Then I am routed to the new block that opens up', async () => {
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyQuestion3Page = new CurrencyQuestion3Page(page)
      const hubPage = new HubPage(page)
      const skipCalculatedSummaryPage = new SkipCalculatedSummaryPage(page)
      await hubPage.summaryRowLink('calculated-summary-section').click()
      await calculatedSummarySectionSummaryPage.skipAnswer2Edit().click()
      await skipCalculatedSummaryPage.no().click()
      await skipCalculatedSummaryPage.submit().click()
      await expect(page).toHaveURL(new RegExp(currencyQuestion3Page.pageName))
    })

    test('Given I confirm the calculated summary and the blocks following it are already complete, When I press submit, Then I am returned to the section summary anchored to the answer I edited initially', async () => {
      const currencyQuestion3Page = new CurrencyQuestion3Page(page)
      await currencyQuestion3Page.submit().click()
      await expect(page).toHaveURL(/calculated-summary-section\/#skip-answer-2/)
    })

    test('Given I change an answer, When I press previous from the now incomplete calculated summary, Then I am routed to the block before the calculated summary', async () => {
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyQuestion3Page = new CurrencyQuestion3Page(page)
      const skipCalculatedSummaryPage = new SkipCalculatedSummaryPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await calculatedSummarySectionSummaryPage.thirdNumberAnswerPartAEdit().click()
      await thirdNumberBlockPage.thirdNumberPartA().fill('120')
      await thirdNumberBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(currencyQuestion3Page.pageName))
      await currencyQuestion3Page.previous().click()
      await expect(page).toHaveURL(new RegExp(skipCalculatedSummaryPage.pageName))
    })

    test('Given I complete the section, When I go back to the grand calculated summary, Then I see the new calculated summary included', async () => {
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyAllPage = new CurrencyAllPage(page)
      const currencyQuestion3Page = new CurrencyQuestion3Page(page)
      const hubPage = new HubPage(page)
      const skipCalculatedSummaryPage = new SkipCalculatedSummaryPage(page)
      await skipCalculatedSummaryPage.submit().click()
      await currencyQuestion3Page.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()
      await expect(hubPage.summaryRowState('grand-calculated-summary-section')).toHaveText('Partially completed')
      await hubPage.summaryRowLink('grand-calculated-summary-section').click()
      await expect(currencyAllPage.grandCalculatedSummaryTitle()).toHaveText('The grand calculated summary is calculated to be £450.00. Is this correct?')
    })

    test('Given I provide an answer to question 3b from the grand calculated summary, this opens up an additional question, and when I press continue I am taken to this question first, then the calculated summary, and then the grand calculated summary', async () => {
      const currencyAllPage = new CurrencyAllPage(page)
      const currencyQuestion3Page = new CurrencyQuestion3Page(page)
      const fourthNumberBlockPage = new FourthNumberBlockPage(page)
      const thirdNumberBlockPage = new ThirdNumberBlockPage(page)
      await currencyAllPage.currencyQuestion3Edit().click()
      await currencyQuestion3Page.thirdNumberAnswerPartBEdit().click()
      await thirdNumberBlockPage.thirdNumberPartB().fill('10')
      await thirdNumberBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(fourthNumberBlockPage.pageName))
      await fourthNumberBlockPage.fourthNumber().fill('1')
      await fourthNumberBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(currencyQuestion3Page.pageName))
      await currencyQuestion3Page.submit().click()
      await expect(page).toHaveURL(new RegExp(currencyAllPage.pageName))
      await expect(currencyAllPage.grandCalculatedSummaryTitle()).toHaveText('The grand calculated summary is calculated to be £461.00. Is this correct?')
      await currencyAllPage.submit().click()
    })

    test('Given I go back to section one and skip the first block, it is not included in the first calculated summary and consequently not included in the grand calculated summary', async () => {
      const currencyAllPage = new CurrencyAllPage(page)
      const hubPage = new HubPage(page)
      const questionsSectionSummaryPage = new QuestionsSectionSummaryPage(page)
      const skipFirstBlockPage = new SkipFirstBlockPage(page)
      await hubPage.summaryRowLink('questions-section').click()
      await questionsSectionSummaryPage.skipAnswer1Edit().click()
      await skipFirstBlockPage.yes().click()
      await skipFirstBlockPage.submit().click()
      await questionsSectionSummaryPage.submit().click()
      await hubPage.summaryRowLink('grand-calculated-summary-section').click()
      await expect(currencyAllPage.currencySection1()).toHaveText('£30.00')
      await expect(currencyAllPage.grandCalculatedSummaryTitle()).toHaveText('The grand calculated summary is calculated to be £161.00. Is this correct?')
    })
  })
})
