import { test, expect } from '../../../fixtures/test'
import CalculatedSummarySectionSummaryPage from '../../../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/calculated-summary-section-summary.page'
import CurrencyTotalPlaybackPage from '../../../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/currency-total-playback.page'
import DependentQuestionSectionSummaryPage from '../../../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/dependent-question-section-summary.page'
import FirstQuestionBlockPage from '../../../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/first-question-block.page'
import FruitPage from '../../../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/fruit.page'
import SecondQuestionBlockPage from '../../../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/second-question-block.page'
import VegetablesPage from '../../../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/vegetables.page'
import SkipQuestionPage from '../../../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/skip-butter-block.page'
import ButterPage from '../../../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/butter-block.page'
import HubPage from '../../../base_pages/hub.page'
import { verifyUrlContains } from '../../../helpers'

test.describe('Routing and skipping section dependencies based on calculated summaries', () => {
  test.describe('Given the section dependencies based on a calculated summary questionnaire', () => {
    test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_routing_and_skipping_section_dependencies_calculated_summary.json')
    })

    test('When the calculated summary total has not been set, Then the dependent section should not be enabled', async ({ page }) => {
      const hubPage = new HubPage(page)
      await expect(hubPage.summaryRowLink('calculated-summary-section')).toBeVisible()
      await expect(hubPage.summaryRowLink('dependent-question-section')).toBeVisible()
      await expect(hubPage.summaryRowLink('dependent-enabled-section')).not.toBeVisible()
    })

    test('When the calculated summary total is equal to £100, Then the dependent section should be enabled', async ({ page }) => {
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const firstQuestionBlockPage = new FirstQuestionBlockPage(page)
      const hubPage = new HubPage(page)
      const skipQuestionPage = new SkipQuestionPage(page)
      await hubPage.summaryRowLink('calculated-summary-section').click()
      await firstQuestionBlockPage.milk().fill('25')
      await firstQuestionBlockPage.eggs().fill('25')
      await firstQuestionBlockPage.bread().fill('25')
      await firstQuestionBlockPage.cheese().fill('25')
      await firstQuestionBlockPage.submit().click()
      await skipQuestionPage.yes().click()
      await skipQuestionPage.submit().click()
      await currencyTotalPlaybackPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()

      await expect(hubPage.summaryRowLink('calculated-summary-section')).toBeVisible()
      await expect(hubPage.summaryRowLink('dependent-question-section')).toBeVisible()
      await expect(hubPage.summaryRowLink('dependent-enabled-section')).toBeVisible()
    })

    test('When a question in another section has a skip condition dependency on a calculated summary total, and the skip condition is not met (total less than £10), then the dependent question should be displayed', async ({
      page
    }) => {
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const firstQuestionBlockPage = new FirstQuestionBlockPage(page)
      const fruitPage = new FruitPage(page)
      const hubPage = new HubPage(page)
      const skipQuestionPage = new SkipQuestionPage(page)
      await hubPage.summaryRowLink('calculated-summary-section').click()
      await firstQuestionBlockPage.milk().fill('1')
      await firstQuestionBlockPage.eggs().fill('1')
      await firstQuestionBlockPage.bread().fill('1')
      await firstQuestionBlockPage.cheese().fill('1')
      await firstQuestionBlockPage.submit().click()
      await skipQuestionPage.yes().click()
      await skipQuestionPage.submit().click()
      await currencyTotalPlaybackPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()

      await hubPage.summaryRowLink('dependent-question-section').click()
      await verifyUrlContains(page, fruitPage.pageName)
    })

    test('When a question in another section has a skip condition dependency on a calculated summary total, and the skip condition is met (total greater than £10), then the dependent question should not be displayed', async ({
      page
    }) => {
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const firstQuestionBlockPage = new FirstQuestionBlockPage(page)
      const hubPage = new HubPage(page)
      const skipQuestionPage = new SkipQuestionPage(page)
      const vegetablesPage = new VegetablesPage(page)
      await hubPage.summaryRowLink('calculated-summary-section').click()
      await firstQuestionBlockPage.milk().fill('5')
      await firstQuestionBlockPage.eggs().fill('5')
      await firstQuestionBlockPage.bread().fill('5')
      await firstQuestionBlockPage.cheese().fill('5')
      await firstQuestionBlockPage.submit().click()
      await skipQuestionPage.yes().click()
      await skipQuestionPage.submit().click()
      await currencyTotalPlaybackPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()

      await hubPage.summaryRowLink('dependent-question-section').click()
      await verifyUrlContains(page, vegetablesPage.pageName)
    })

    test('When a question in another section has a routing rule dependency on a calculated summary total, and the calculated summary total is greater than £100, then we should be routed to the second question block', async ({
      page
    }) => {
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const firstQuestionBlockPage = new FirstQuestionBlockPage(page)
      const hubPage = new HubPage(page)
      const secondQuestionBlockPage = new SecondQuestionBlockPage(page)
      const skipQuestionPage = new SkipQuestionPage(page)
      const vegetablesPage = new VegetablesPage(page)
      await hubPage.summaryRowLink('calculated-summary-section').click()
      await firstQuestionBlockPage.milk().fill('30')
      await firstQuestionBlockPage.eggs().fill('30')
      await firstQuestionBlockPage.bread().fill('30')
      await firstQuestionBlockPage.cheese().fill('30')
      await firstQuestionBlockPage.submit().click()
      await skipQuestionPage.yes().click()
      await skipQuestionPage.submit().click()
      await currencyTotalPlaybackPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()

      await hubPage.summaryRowLink('dependent-question-section').click()
      await vegetablesPage.yes().click()
      await vegetablesPage.submit().click()
      await verifyUrlContains(page, secondQuestionBlockPage.pageName)
    })

    test('When a question in another section has a routing rule dependency on a calculated summary total, and the calculated summary total is less than £100, then we should be routed to the section summary', async ({
      page
    }) => {
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const dependentQuestionSectionSummaryPage = new DependentQuestionSectionSummaryPage(page)
      const firstQuestionBlockPage = new FirstQuestionBlockPage(page)
      const hubPage = new HubPage(page)
      const skipQuestionPage = new SkipQuestionPage(page)
      const vegetablesPage = new VegetablesPage(page)
      await hubPage.summaryRowLink('calculated-summary-section').click()
      await firstQuestionBlockPage.milk().fill('20')
      await firstQuestionBlockPage.eggs().fill('20')
      await firstQuestionBlockPage.bread().fill('20')
      await firstQuestionBlockPage.cheese().fill('20')
      await firstQuestionBlockPage.submit().click()
      await skipQuestionPage.yes().click()
      await skipQuestionPage.submit().click()
      await currencyTotalPlaybackPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()

      await hubPage.summaryRowLink('dependent-question-section').click()
      await vegetablesPage.yes().click()
      await vegetablesPage.submit().click()
      await verifyUrlContains(page, dependentQuestionSectionSummaryPage.pageName)
    })

    test('When a question in another section has a dependency on a calculated summary total, and both sections are complete, and I go back and edit the calculated summary total, then the dependent section status should be in progress', async ({
      page
    }) => {
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const dependentQuestionSectionSummaryPage = new DependentQuestionSectionSummaryPage(page)
      const firstQuestionBlockPage = new FirstQuestionBlockPage(page)
      const hubPage = new HubPage(page)
      const skipQuestionPage = new SkipQuestionPage(page)
      const vegetablesPage = new VegetablesPage(page)
      await hubPage.summaryRowLink('calculated-summary-section').click()
      await firstQuestionBlockPage.milk().fill('20')
      await firstQuestionBlockPage.eggs().fill('20')
      await firstQuestionBlockPage.bread().fill('20')
      await firstQuestionBlockPage.cheese().fill('20')
      await firstQuestionBlockPage.submit().click()
      await skipQuestionPage.yes().click()
      await skipQuestionPage.submit().click()
      await currencyTotalPlaybackPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()

      await hubPage.summaryRowLink('dependent-question-section').click()
      await vegetablesPage.yes().click()
      await vegetablesPage.submit().click()
      await dependentQuestionSectionSummaryPage.submit().click()
      await expect(hubPage.summaryRowState('dependent-question-section')).toHaveText('Completed')

      await hubPage.summaryRowLink('calculated-summary-section').click()
      await currencyTotalPlaybackPage.milkAnswerEdit().click()
      await firstQuestionBlockPage.milk().fill('100')
      await firstQuestionBlockPage.submit().click()
      await verifyUrlContains(page, currencyTotalPlaybackPage.pageName)
      await currencyTotalPlaybackPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()
      await expect(hubPage.summaryRowState('dependent-question-section')).toHaveText('Partially completed')
    })

    test('When the calculated summary total is less than £100 but additional answers on the path are opened up as a result of editing an answer, Then the dependent section should be enabled', async ({
      page
    }) => {
      const butterPage = new ButterPage(page)
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const firstQuestionBlockPage = new FirstQuestionBlockPage(page)
      const hubPage = new HubPage(page)
      const skipQuestionPage = new SkipQuestionPage(page)
      await hubPage.summaryRowLink('calculated-summary-section').click()
      await firstQuestionBlockPage.milk().fill('10')
      await firstQuestionBlockPage.eggs().fill('10')
      await firstQuestionBlockPage.bread().fill('10')
      await firstQuestionBlockPage.cheese().fill('10')
      await firstQuestionBlockPage.submit().click()
      await skipQuestionPage.yes().click()
      await skipQuestionPage.submit().click()
      await currencyTotalPlaybackPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()

      await expect(hubPage.summaryRowLink('calculated-summary-section')).toBeVisible()
      await expect(hubPage.summaryRowLink('dependent-question-section')).toBeVisible()
      await expect(hubPage.summaryRowLink('dependent-enabled-section')).not.toBeVisible()

      await hubPage.summaryRowLink('calculated-summary-section').click()
      await calculatedSummarySectionSummaryPage.skipButterBlockAnswerEdit().click()
      await skipQuestionPage.no().click()
      await skipQuestionPage.submit().click()
      await butterPage.butter().fill('60')
      await butterPage.submit().click()
      await currencyTotalPlaybackPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()

      await expect(hubPage.summaryRowLink('calculated-summary-section')).toBeVisible()
      await expect(hubPage.summaryRowLink('dependent-question-section')).toBeVisible()
      await expect(hubPage.summaryRowLink('dependent-enabled-section')).toBeVisible()
    })

    test('When the calculated summary total is equal to £100 but answers on the path are remove as a result of an answer edit, Then the dependent section should be enabled', async ({
      page
    }) => {
      const butterPage = new ButterPage(page)
      const calculatedSummarySectionSummaryPage = new CalculatedSummarySectionSummaryPage(page)
      const currencyTotalPlaybackPage = new CurrencyTotalPlaybackPage(page)
      const firstQuestionBlockPage = new FirstQuestionBlockPage(page)
      const hubPage = new HubPage(page)
      const skipQuestionPage = new SkipQuestionPage(page)
      await hubPage.summaryRowLink('calculated-summary-section').click()
      await firstQuestionBlockPage.milk().fill('10')
      await firstQuestionBlockPage.eggs().fill('10')
      await firstQuestionBlockPage.bread().fill('10')
      await firstQuestionBlockPage.cheese().fill('10')
      await firstQuestionBlockPage.submit().click()
      await skipQuestionPage.no().click()
      await skipQuestionPage.submit().click()
      await butterPage.butter().fill('60')
      await butterPage.submit().click()
      await currencyTotalPlaybackPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()

      await expect(hubPage.summaryRowLink('calculated-summary-section')).toBeVisible()
      await expect(hubPage.summaryRowLink('dependent-question-section')).toBeVisible()
      await expect(hubPage.summaryRowLink('dependent-enabled-section')).toBeVisible()

      await hubPage.summaryRowLink('calculated-summary-section').click()
      await calculatedSummarySectionSummaryPage.skipButterBlockAnswerEdit().click()
      await skipQuestionPage.yes().click()
      await skipQuestionPage.submit().click()
      await calculatedSummarySectionSummaryPage.submit().click()

      await expect(hubPage.summaryRowLink('calculated-summary-section')).toBeVisible()
      await expect(hubPage.summaryRowLink('dependent-question-section')).toBeVisible()
      await expect(hubPage.summaryRowLink('dependent-enabled-section')).not.toBeVisible()
    })
  })
})
