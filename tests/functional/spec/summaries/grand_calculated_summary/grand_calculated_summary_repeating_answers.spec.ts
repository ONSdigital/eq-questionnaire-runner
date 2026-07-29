import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../fixtures/test'
import HubPage from '../../../base_pages/hub.page'
import Block1Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/block-1.page'
import Block2Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/block-2.page'
import CalculatedSummary1Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-1.page'
import Block3Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/block-3.page'
import Block4Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/block-4.page'
import CalculatedSummary2Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-2.page'
import CalculatedSummary3Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-3.page'
import CalculatedSummary4Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-4.page'
import GrandCalculatedSummary1Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/grand-calculated-summary-1.page'
import GrandCalculatedSummary2Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/grand-calculated-summary-2.page'
import Section1SummaryPage from '../../../generated_pages/grand_calculated_summary_repeating_answers/section-1-summary.page'
import AddUtilityBillPage from '../../../generated_pages/grand_calculated_summary_repeating_answers/any-other-utility-bills-add.page'
import AnyOtherUtilityBillsPage from '../../../generated_pages/grand_calculated_summary_repeating_answers/any-other-utility-bills.page'
import DynamicAnswerPage from '../../../generated_pages/grand_calculated_summary_repeating_answers/dynamic-answer.page'
import CalculatedSummary5Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-5.page'
import AnyStreamingServicesPage from '../../../generated_pages/grand_calculated_summary_repeating_answers/any-streaming-services.page'
import AddStreamingServicePage from '../../../generated_pages/grand_calculated_summary_repeating_answers/any-other-streaming-services-add.page'
import RemoveStreamingServicePage from '../../../generated_pages/grand_calculated_summary_repeating_answers/any-other-streaming-services-remove.page'
import StreamingServiceRepeatingBlock1Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/streaming-service-repeating-block-1-repeating-block.page'
import StreamingServiceRepeatingBlock2Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/streaming-service-repeating-block-2-repeating-block.page'
import AnyOtherStreamingServicesPage from '../../../generated_pages/grand_calculated_summary_repeating_answers/any-other-streaming-services.page'
import CalculatedSummary6Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-6.page'
import CalculatedSummary7Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-7.page'
import OtherInternetUsagePage from '../../../generated_pages/grand_calculated_summary_repeating_answers/other-internet-usage.page'
import CalculatedSummary8Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-8.page'
import GrandCalculatedSummary3Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/grand-calculated-summary-3.page'
import GrandCalculatedSummary4Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/grand-calculated-summary-4.page'
import GrandCalculatedSummary5Page from '../../../generated_pages/grand_calculated_summary_repeating_answers/grand-calculated-summary-5.page'
import AnyUtilityBillsPage from '../../../generated_pages/grand_calculated_summary_repeating_answers/any-utility-bills.page'
import Section4SummaryPage from '../../../generated_pages/grand_calculated_summary_repeating_answers/section-4-summary.page'
import Section5SummaryPage from '../../../generated_pages/grand_calculated_summary_repeating_answers/section-5-summary.page'
import { assertSummaryItems, assertSummaryValues, repeatingAnswerChangeLink } from '../../../helpers'
import InternetBreakdownBlockPage from '../../../generated_pages/grand_calculated_summary_repeating_answers/internet-breakdown-block.page'
import Section6SummaryPage from '../../../generated_pages/grand_calculated_summary_repeating_answers/section-6-summary.page'
import PersonalExpenditureBlockPage from '../../../generated_pages/grand_calculated_summary_repeating_answers/personal-expenditure-block.page'
import GrandCalculatedSummaryPipingPage from '../../../generated_pages/grand_calculated_summary_repeating_answers/grand-calculated-summary-piping.page'

test.describe('Feature: Grand Calculated Summary', () => {
  const summaryRowTitles = '.ons-summary__row-title'

  test.describe('Given I have a Grand Calculated Summary across multiple sections', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Reaching the grand calculated summary section', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      const block1Page = new Block1Page(page)
      const block2Page = new Block2Page(page)
      const block3Page = new Block3Page(page)
      const block4Page = new Block4Page(page)
      const calculatedSummary1Page = new CalculatedSummary1Page(page)
      const calculatedSummary2Page = new CalculatedSummary2Page(page)
      const calculatedSummary3Page = new CalculatedSummary3Page(page)
      const calculatedSummary4Page = new CalculatedSummary4Page(page)
      const grandCalculatedSummary1Page = new GrandCalculatedSummary1Page(page)
      const hubPage = new HubPage(page)
      const section1SummaryPage = new Section1SummaryPage(page)
      await openQuestionnaire('test_grand_calculated_summary_repeating_answers.json')
      await hubPage.submit().click()

      // complete 2 questions in section 1
      await block1Page.q1A1().fill('10')
      await block1Page.q1A2().fill('20')
      await block1Page.submit().click()
      await block2Page.q2A1().fill('30')
      await block2Page.q2A2().fill('40')
      await block2Page.submit().click()
      await calculatedSummary1Page.submit().click()

      // and the one for section 2
      await block3Page.q3A1().fill('100')
      await block3Page.q3A2().fill('200')
      await block3Page.submit().click()
      await calculatedSummary2Page.submit().click()
      await calculatedSummary3Page.submit().click()
      await grandCalculatedSummary1Page.submit().click()
      await section1SummaryPage.submit().click()
      await hubPage.submit().click()
      await block4Page.q4A1().fill('5')
      await block4Page.q4A2().fill('10')
      await block4Page.submit().click()
      await calculatedSummary4Page.submit().click()
      await hubPage.submit().click()
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('Given I click on the change link for a calculated summary, When I press continue, Then I am taken back to the grand calculated summary', async () => {
      const calculatedSummary1Page = new CalculatedSummary1Page(page)
      const grandCalculatedSummary2Page = new GrandCalculatedSummary2Page(page)
      await expect(grandCalculatedSummary2Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for shopping and entertainment is calculated to be £415.00. Is this correct?'
      )
      await grandCalculatedSummary2Page.calculatedSummary1Edit().click()
      await expect(page).toHaveURL(new RegExp(calculatedSummary1Page.pageName))

      await calculatedSummary1Page.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary2Page.pageName))
    })

    test('Given I click on the change link for a calculated summary then one for an answer, When I press previous twice, I am return to the calculated summary then grand calculated summary', async () => {
      const block1Page = new Block1Page(page)
      const calculatedSummary1Page = new CalculatedSummary1Page(page)
      const grandCalculatedSummary2Page = new GrandCalculatedSummary2Page(page)
      await grandCalculatedSummary2Page.calculatedSummary1Edit().click()
      await calculatedSummary1Page.q1A1Edit().click()
      await expect(page).toHaveURL(new RegExp(block1Page.pageName))

      await block1Page.previous().click()
      await expect(page).toHaveURL(new RegExp(calculatedSummary1Page.pageName))

      await calculatedSummary1Page.previous().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary2Page.pageName))
    })

    test('Given I go back to the calculated summary and then to a question and edit the answer. I am first taken back to the each calculated summary that uses the answer, the grand calculated summary in section 1, and then the updated grand calculated summary in section 3.', async () => {
      const block4Page = new Block4Page(page)
      const calculatedSummary4Page = new CalculatedSummary4Page(page)
      const grandCalculatedSummary2Page = new GrandCalculatedSummary2Page(page)
      await grandCalculatedSummary2Page.calculatedSummary4Edit().click()
      await expect(calculatedSummary4Page.calculatedSummaryTitle()).toHaveText(
        'Calculated Summary for games expenditure is calculated to be £15.00. Is this correct?'
      )
      await calculatedSummary4Page.q4A1Edit().click()
      await expect(page).toHaveURL(new RegExp(block4Page.pageName))

      await block4Page.q4A1().fill('50')
      await block4Page.submit().click()

      // first taken back to the calculated summary which has updated
      await expect(page).toHaveURL(new RegExp(calculatedSummary4Page.pageName))
      await expect(calculatedSummary4Page.calculatedSummaryTitle()).toHaveText(
        'Calculated Summary for games expenditure is calculated to be £60.00. Is this correct?'
      )
      await calculatedSummary4Page.submit().click()

      // then taken back to the grand calculated summary which has also been updated correctly
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary2Page.pageName))
      await expect(grandCalculatedSummary2Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for shopping and entertainment is calculated to be £460.00. Is this correct?'
      )
    })

    test('Given I go back to another calculated summary and edit multiple answers,I am still correctly routed back to the grand calculated summary', async () => {
      const block1Page = new Block1Page(page)
      const block2Page = new Block2Page(page)
      const calculatedSummary1Page = new CalculatedSummary1Page(page)
      const calculatedSummary3Page = new CalculatedSummary3Page(page)
      const grandCalculatedSummary1Page = new GrandCalculatedSummary1Page(page)
      const grandCalculatedSummary2Page = new GrandCalculatedSummary2Page(page)
      await grandCalculatedSummary2Page.calculatedSummary1Edit().click()
      await expect(calculatedSummary1Page.calculatedSummaryTitle()).toHaveText(
        'Calculated Summary for food expenditure is calculated to be £100.00. Is this correct?'
      )

      // change first answer
      await calculatedSummary1Page.q1A1Edit().click()
      await expect(page).toHaveURL(new RegExp(block1Page.pageName))
      await block1Page.q1A1().fill('100')
      await block1Page.submit().click()

      // go to each calculated summary that uses the answer in turn, then each grand calculated summary up to the one we were editing
      await expect(page).toHaveURL(new RegExp(calculatedSummary1Page.pageName))
      await expect(calculatedSummary1Page.calculatedSummaryTitle()).toHaveText(
        'Calculated Summary for food expenditure is calculated to be £190.00. Is this correct?'
      )

      // change another answer
      await calculatedSummary1Page.q2A2Edit().click()
      await expect(page).toHaveURL(new RegExp(block2Page.pageName))
      await block2Page.q2A2().fill('400')
      await block2Page.submit().click()

      // back at updated calculated summary
      await expect(calculatedSummary1Page.calculatedSummaryTitle()).toHaveText(
        'Calculated Summary for food expenditure is calculated to be £550.00. Is this correct?'
      )

      // Go to each calculated/grand calculated summary including this answer and reconfirm before being taken back to grand calculated summary
      await calculatedSummary1Page.submit().click()
      await expect(page).toHaveURL(new RegExp(calculatedSummary3Page.pageName))
      await calculatedSummary3Page.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary1Page.pageName))
      await grandCalculatedSummary1Page.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary2Page.pageName))
      await expect(grandCalculatedSummary2Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for shopping and entertainment is calculated to be £910.00. Is this correct?'
      )
    })

    test('Given I edit an answer included in a grand calculated summary, the calculated summary sections should return to partially completed, and the grand calculated summary becomes unavailable.', async () => {
      const block4Page = new Block4Page(page)
      const calculatedSummary4Page = new CalculatedSummary4Page(page)
      const grandCalculatedSummary2Page = new GrandCalculatedSummary2Page(page)
      const hubPage = new HubPage(page)
      await grandCalculatedSummary2Page.submit().click()
      await expect(hubPage.summaryRowState('section-3')).toHaveText('Completed')

      // Now edit an answer from section 2 and go back to the hub
      await hubPage.summaryRowLink('section-3').click()
      await grandCalculatedSummary2Page.calculatedSummary4Edit().click()
      await calculatedSummary4Page.q4A1Edit().click()
      await block4Page.q4A1().fill('1')
      await block4Page.submit().click()
      await calculatedSummary4Page.previous().click()
      await block4Page.previous().click()

      // calculated summary section should be in progress
      await expect(hubPage.summaryRowState('section-2')).toHaveText('Partially completed')
      await expect(hubPage.summaryRowLink('section-3')).toBeHidden()
    })

    test('Given I confirm the calculated summary, When I return to the Hub, Then I see the grand calculated summary come back marked as partially completed', async () => {
      const calculatedSummary4Page = new CalculatedSummary4Page(page)
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink('section-2').click()
      await calculatedSummary4Page.submit().click()
      await expect(hubPage.summaryRowState('section-3')).toHaveText('Partially completed')
    })

    test('Given I set both answers to block 4 to zero which removes the Grand Calculated Summary from the path, I am routed back to the Hub after the calculated summary', async () => {
      const block4Page = new Block4Page(page)
      const calculatedSummary4Page = new CalculatedSummary4Page(page)
      const grandCalculatedSummary2Page = new GrandCalculatedSummary2Page(page)
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink('section-3').click()
      await grandCalculatedSummary2Page.calculatedSummary4Edit().click()
      await calculatedSummary4Page.q4A1Edit().click()
      await block4Page.q4A1().fill('0')
      await block4Page.q4A2().fill('0')
      await block4Page.submit().click()
      await calculatedSummary4Page.submit().click()
      // should be back at Hub, and grand calculated summary section not present
      await expect(page).toHaveURL(new RegExp(hubPage.pageName))
      await expect(hubPage.summaryRowLink('section-3')).toBeHidden()
    })

    test(
      'Given I have a grand calculated summary section requiring completion of all previous sections, ' +
        "When I complete each section in turn, Then I don't see the grand calculated summary " +
        'until all sections are complete, at which point I see it on the Hub',
      async () => {
        const addStreamingServicePage = new AddStreamingServicePage(page)
        const addUtilityBillPage = new AddUtilityBillPage(page)
        const anyOtherStreamingServicesPage = new AnyOtherStreamingServicesPage(page)
        const anyOtherUtilityBillsPage = new AnyOtherUtilityBillsPage(page)
        const anyStreamingServicesPage = new AnyStreamingServicesPage(page)
        const anyUtilityBillsPage = new AnyUtilityBillsPage(page)
        const calculatedSummary5Page = new CalculatedSummary5Page(page)
        const calculatedSummary6Page = new CalculatedSummary6Page(page)
        const calculatedSummary7Page = new CalculatedSummary7Page(page)
        const calculatedSummary8Page = new CalculatedSummary8Page(page)
        const dynamicAnswerPage = new DynamicAnswerPage(page)
        const hubPage = new HubPage(page)
        const otherInternetUsagePage = new OtherInternetUsagePage(page)
        const section4SummaryPage = new Section4SummaryPage(page)
        const section5SummaryPage = new Section5SummaryPage(page)
        const streamingServiceRepeatingBlock1Page = new StreamingServiceRepeatingBlock1Page(page)
        const streamingServiceRepeatingBlock2Page = new StreamingServiceRepeatingBlock2Page(page)
        // no grand calculated summary section on the hub
        await expect(hubPage.summaryRowLink('section-6')).toBeHidden()

        await hubPage.submit().click()
        await anyUtilityBillsPage.yes().click()
        await anyUtilityBillsPage.submit().click()
        await addUtilityBillPage.utilityBillName().selectOption('Electricity')
        await addUtilityBillPage.submit().click()
        await anyOtherUtilityBillsPage.yes().click()
        await anyOtherUtilityBillsPage.submit().click()
        await addUtilityBillPage.utilityBillName().selectOption('Internet')
        await addUtilityBillPage.submit().click()
        await anyOtherUtilityBillsPage.yes().click()
        await anyOtherUtilityBillsPage.submit().click()
        await addUtilityBillPage.utilityBillName().selectOption('Gas')
        await addUtilityBillPage.submit().click()
        await anyOtherUtilityBillsPage.no().click()
        await anyOtherUtilityBillsPage.submit().click()
        await dynamicAnswerPage.inputs().nth(0).fill('150')
        await dynamicAnswerPage.inputs().nth(1).fill('35')
        await dynamicAnswerPage.inputs().nth(2).fill('65')
        await dynamicAnswerPage.submit().click()
        await calculatedSummary5Page.submit().click()
        await section4SummaryPage.submit().click()
        // still no grand calculated summary yet
        await expect(hubPage.summaryRowLink('section-6')).toBeHidden()

        await hubPage.submit().click()
        await anyStreamingServicesPage.yes().click()
        await anyStreamingServicesPage.submit().click()
        await addStreamingServicePage.streamingServiceName().selectOption('Netflix')
        await addStreamingServicePage.submit().click()
        await streamingServiceRepeatingBlock1Page.streamingServiceMonthlyCost().fill('10')
        await streamingServiceRepeatingBlock1Page.streamingServiceExtraCost().fill('0')
        await streamingServiceRepeatingBlock1Page.submit().click()
        await streamingServiceRepeatingBlock2Page.streamingServiceUsage().fill('20')
        await streamingServiceRepeatingBlock2Page.submit().click()
        await anyOtherStreamingServicesPage.yes().click()
        await anyOtherStreamingServicesPage.submit().click()
        await addStreamingServicePage.streamingServiceName().selectOption('Prime video')
        await addStreamingServicePage.submit().click()
        await streamingServiceRepeatingBlock1Page.streamingServiceMonthlyCost().fill('8')
        await streamingServiceRepeatingBlock1Page.streamingServiceExtraCost().fill('12')
        await streamingServiceRepeatingBlock1Page.submit().click()
        await streamingServiceRepeatingBlock2Page.streamingServiceUsage().fill('25')
        await streamingServiceRepeatingBlock2Page.submit().click()
        await anyOtherStreamingServicesPage.no().click()
        await anyOtherStreamingServicesPage.submit().click()
        await calculatedSummary6Page.submit().click()
        await calculatedSummary7Page.submit().click()
        await otherInternetUsagePage.mediaDownloads().fill('50')
        await otherInternetUsagePage.miscInternet().fill('5')
        await otherInternetUsagePage.submit().click()
        await calculatedSummary8Page.submit().click()
        await section5SummaryPage.submit().click()
        // grand calculated summary now present
        await expect(hubPage.summaryRowLink('section-6')).toBeVisible()
        await expect(hubPage.summaryRowState('section-6')).toHaveText('Not started')
      }
    )

    test('Given I have a calculated summary of repeating answers and a calculated summary of dynamic answers, When I reach the grand calculated summary of both, Then I see the correct total and items', async () => {
      const grandCalculatedSummary3Page = new GrandCalculatedSummary3Page(page)
      const hubPage = new HubPage(page)
      await hubPage.submit().click()
      await expect(grandCalculatedSummary3Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for monthly spending on bills and services is calculated to be £280.00. Is this correct?'
      )
      await assertSummaryValues(page, ['£250.00', '£30.00', '£280.00'])
      await assertSummaryItems(page, [
        'Total monthly expenditure on utility bills',
        'Total monthly expenditure on streaming services',
        'Total monthly expenditure on bills and streaming services'
      ])
    })

    test('Given I have 2 calculated summaries of list repeating block answers, When I reach the grand calculated summary of both, Then I see the correct total and items', async () => {
      const grandCalculatedSummary3Page = new GrandCalculatedSummary3Page(page)
      const grandCalculatedSummary4Page = new GrandCalculatedSummary4Page(page)
      await grandCalculatedSummary3Page.submit().click()
      await expect(grandCalculatedSummary4Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for internet usage is calculated to be 100 GB. Is this correct?'
      )
      await assertSummaryValues(page, ['45 GB', '55 GB', '100 GB'])
      await assertSummaryItems(page, ['Total internet usage on streaming services', 'Total internet usage on other services', 'Total internet usage'])
    })

    test('Given I have multiple calculated summaries of static, repeating and dynamic answers, When I reach the grand calculated summary of them all, Then I see the correct total and items', async () => {
      const grandCalculatedSummary4Page = new GrandCalculatedSummary4Page(page)
      const grandCalculatedSummary5Page = new GrandCalculatedSummary5Page(page)
      await grandCalculatedSummary4Page.submit().click()
      await expect(grandCalculatedSummary5Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for total monthly household expenditure is calculated to be £1,130.00. Is this correct?'
      )
      await assertSummaryValues(page, ['£550.00', '£300.00', '£0.00', '£250.00', '£30.00', '£1,130.00'])
      await assertSummaryItems(page, [
        'Total monthly food expenditure',
        'Total monthly clothes expenditure',
        'Total games expenditure',
        'Total monthly expenditure on utility bills',
        'Total monthly expenditure on streaming services',
        'Total monthly expenditure'
      ])
    })

    test('Given I a grand calculated summary featuring repeating answers, When I click edit links to return to a dynamic answer then previous twice, Then I return to the grand calculated summary where I started', async () => {
      const calculatedSummary5Page = new CalculatedSummary5Page(page)
      const dynamicAnswerPage = new DynamicAnswerPage(page)
      const grandCalculatedSummary5Page = new GrandCalculatedSummary5Page(page)
      await grandCalculatedSummary5Page.calculatedSummary5Edit().click()
      await repeatingAnswerChangeLink(page, 0).click()
      await expect(page).toHaveURL(new RegExp(dynamicAnswerPage.pageName))
      await dynamicAnswerPage.previous().click()
      await calculatedSummary5Page.previous().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary5Page.pageName))
    })

    test('Given I have a grand calculated summary featuring repeating answers, When I edit a dynamic answer, Then I return to the calculated summary to confirm, and then each affected grand calculated summary in turn', async () => {
      const calculatedSummary5Page = new CalculatedSummary5Page(page)
      const dynamicAnswerPage = new DynamicAnswerPage(page)
      const grandCalculatedSummary3Page = new GrandCalculatedSummary3Page(page)
      const grandCalculatedSummary5Page = new GrandCalculatedSummary5Page(page)
      await grandCalculatedSummary5Page.calculatedSummary5Edit().click()
      await repeatingAnswerChangeLink(page, 1).click()
      await dynamicAnswerPage.inputs().nth(0).fill('175')
      await dynamicAnswerPage.submit().click()
      await calculatedSummary5Page.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary3Page.pageName))
      await expect(grandCalculatedSummary3Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for monthly spending on bills and services is calculated to be £305.00. Is this correct?'
      )
      await grandCalculatedSummary3Page.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary5Page.pageName))
      await expect(grandCalculatedSummary5Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for total monthly household expenditure is calculated to be £1,155.00. Is this correct?'
      )
    })

    test('Given I have a grand calculated summary featuring repeating answers, When I click edit links to return to a list repeating block answer then previous twice, Then I return to the grand calculated summary anchored from where I started', async () => {
      const calculatedSummary5Page = new CalculatedSummary5Page(page)
      const grandCalculatedSummary5Page = new GrandCalculatedSummary5Page(page)
      const streamingServiceRepeatingBlock1Page = new StreamingServiceRepeatingBlock1Page(page)
      await grandCalculatedSummary5Page.calculatedSummary6Edit().click()
      await repeatingAnswerChangeLink(page, 2).click()
      await streamingServiceRepeatingBlock1Page.previous().click()
      await calculatedSummary5Page.previous().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary5Page.pageName))
    })

    test('Given I have a grand calculated summary featuring repeating answers, When I edit a list repeating block answer, Then I return to the calculated summary to confirm, and then the grand calculated summary to confirm', async () => {
      const calculatedSummary5Page = new CalculatedSummary5Page(page)
      const grandCalculatedSummary3Page = new GrandCalculatedSummary3Page(page)
      const grandCalculatedSummary5Page = new GrandCalculatedSummary5Page(page)
      const streamingServiceRepeatingBlock1Page = new StreamingServiceRepeatingBlock1Page(page)
      await grandCalculatedSummary5Page.calculatedSummary6Edit().click()
      await repeatingAnswerChangeLink(page, 2).click()
      await streamingServiceRepeatingBlock1Page.streamingServiceMonthlyCost().fill('12')
      await streamingServiceRepeatingBlock1Page.submit().click()
      await calculatedSummary5Page.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary3Page.pageName))
      await expect(grandCalculatedSummary3Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for monthly spending on bills and services is calculated to be £309.00. Is this correct?'
      )
      await grandCalculatedSummary3Page.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary5Page.pageName))
      await expect(grandCalculatedSummary5Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for total monthly household expenditure is calculated to be £1,159.00. Is this correct?'
      )
    })

    test('Given I pipe the grand calculated summary into the next question, When I press continue, Then I see the correct title', async () => {
      const grandCalculatedSummary5Page = new GrandCalculatedSummary5Page(page)
      const internetBreakdownBlockPage = new InternetBreakdownBlockPage(page)
      await grandCalculatedSummary5Page.submit().click()
      await expect(internetBreakdownBlockPage.questionTitle()).toContainText('How did you use the 100 GB across your devices?')
    })

    test('Given I use the grand calculated summary for validation, When I enter values with too large a sum, Then I see a validation error', async () => {
      const internetBreakdownBlockPage = new InternetBreakdownBlockPage(page)
      await internetBreakdownBlockPage.internetPc().fill('60')
      await internetBreakdownBlockPage.internetPhone().fill('60')
      await internetBreakdownBlockPage.submit().click()
      await expect(internetBreakdownBlockPage.errorNumber(1)).toHaveText('Enter answers that add up to 100')
    })

    test('Given I use the grand calculated summary for validation, When I enter values with the correct sum, Then I progress to the summary page', async () => {
      const internetBreakdownBlockPage = new InternetBreakdownBlockPage(page)
      const section6SummaryPage = new Section6SummaryPage(page)
      await internetBreakdownBlockPage.internetPhone().fill('40')
      await internetBreakdownBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(section6SummaryPage.pageName))
      await section6SummaryPage.submit().click()
    })

    test('Given I have a grand calculated summary featuring dynamic answers, When I add an item to the list collector and return to the hub, Then I see the section with dynamic answers is in progress, and the grand calculated summary section is not available', async () => {
      const addUtilityBillPage = new AddUtilityBillPage(page)
      const anyOtherUtilityBillsPage = new AnyOtherUtilityBillsPage(page)
      const dynamicAnswerPage = new DynamicAnswerPage(page)
      const hubPage = new HubPage(page)
      const section4SummaryPage = new Section4SummaryPage(page)
      await hubPage.summaryRowLink('section-4').click()
      await section4SummaryPage.utilityBillsListAddLink().click()
      await addUtilityBillPage.utilityBillName().selectOption('Water')
      await addUtilityBillPage.submit().click()
      await anyOtherUtilityBillsPage.no().click()
      await anyOtherUtilityBillsPage.submit().click()
      await dynamicAnswerPage.inputs().nth(3).fill('40')
      await dynamicAnswerPage.submit().click()
      await page.goto(hubPage.url())
      await expect(hubPage.summaryRowState('section-4')).toHaveText('Partially completed')
      await expect(hubPage.summaryRowLink('section-6')).toBeHidden()
    })

    test('Given I complete the in progress section, When I return to the Hub, Then I see the grand calculated summary section re-enabled, and partially completed', async () => {
      const calculatedSummary5Page = new CalculatedSummary5Page(page)
      const hubPage = new HubPage(page)
      const section4SummaryPage = new Section4SummaryPage(page)
      await hubPage.summaryRowLink('section-4').click()
      await expect(calculatedSummary5Page.calculatedSummaryTitle()).toHaveText(
        'Calculated Summary for monthly spending on utility bills is calculated to be £315.00. Is this correct?'
      )
      await calculatedSummary5Page.submit().click()
      await section4SummaryPage.submit().click()
      await expect(hubPage.summaryRowState('section-6')).toHaveText('Partially completed')
    })

    test('Given I return to the grand calculated summary section, When I go to each grand calculated summary, Then I see the correct new values', async () => {
      const grandCalculatedSummary3Page = new GrandCalculatedSummary3Page(page)
      const grandCalculatedSummary4Page = new GrandCalculatedSummary4Page(page)
      const grandCalculatedSummary5Page = new GrandCalculatedSummary5Page(page)
      const hubPage = new HubPage(page)
      const section6SummaryPage = new Section6SummaryPage(page)
      await hubPage.summaryRowLink('section-6').click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary3Page.pageName))
      await expect(grandCalculatedSummary3Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for monthly spending on bills and services is calculated to be £349.00. Is this correct?'
      )
      await grandCalculatedSummary3Page.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary4Page.pageName))
      await expect(grandCalculatedSummary4Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for internet usage is calculated to be 100 GB. Is this correct?'
      )
      await grandCalculatedSummary4Page.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary5Page.pageName))
      await expect(grandCalculatedSummary5Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for total monthly household expenditure is calculated to be £1,199.00. Is this correct?'
      )
      await grandCalculatedSummary5Page.submit().click()
      await expect(page).toHaveURL(new RegExp(section6SummaryPage.pageName))
      await expect(page.locator(summaryRowTitles).nth(0)).toHaveText('How did you use the 100 GB across your devices?')
      await section6SummaryPage.submit().click()
      await expect(hubPage.summaryRowState('section-6')).toHaveText('Completed')
    })

    test('Given I add a list item for the section with list repeating blocks, When I return to the hub before and after completing the section, Then I see the grand calculated summary go from unavailable, to enabled and in progress', async () => {
      const addStreamingServicePage = new AddStreamingServicePage(page)
      const anyOtherStreamingServicesPage = new AnyOtherStreamingServicesPage(page)
      const calculatedSummary6Page = new CalculatedSummary6Page(page)
      const calculatedSummary7Page = new CalculatedSummary7Page(page)
      const hubPage = new HubPage(page)
      const section5SummaryPage = new Section5SummaryPage(page)
      const streamingServiceRepeatingBlock1Page = new StreamingServiceRepeatingBlock1Page(page)
      const streamingServiceRepeatingBlock2Page = new StreamingServiceRepeatingBlock2Page(page)
      await hubPage.summaryRowLink('section-5').click()
      await section5SummaryPage.streamingServicesListAddLink().click()
      await addStreamingServicePage.streamingServiceName().selectOption('Disney+')
      await addStreamingServicePage.submit().click()
      await streamingServiceRepeatingBlock1Page.streamingServiceMonthlyCost().fill('10')
      await streamingServiceRepeatingBlock1Page.submit().click()
      await streamingServiceRepeatingBlock2Page.streamingServiceUsage().fill('5')
      await streamingServiceRepeatingBlock2Page.submit().click()
      await anyOtherStreamingServicesPage.no().click()
      await anyOtherStreamingServicesPage.submit().click()
      await expect(calculatedSummary6Page.calculatedSummaryTitle()).toHaveText(
        'Calculated Summary for monthly expenditure on streaming services is calculated to be £44.00. Is this correct?'
      )
      await page.goto(hubPage.url())
      await expect(hubPage.summaryRowState('section-5')).toHaveText('Partially completed')
      await expect(hubPage.summaryRowLink('section-6')).toBeHidden()
      await hubPage.summaryRowLink('section-5').click()
      await calculatedSummary6Page.submit().click()
      await expect(calculatedSummary7Page.calculatedSummaryTitle()).toHaveText(
        'Total monthly internet usage on streaming services is calculated to be 50 GB. Is this correct?'
      )
      await calculatedSummary7Page.submit().click()
      await section5SummaryPage.submit().click()
      await expect(hubPage.summaryRowState('section-6')).toHaveText('Partially completed')
    })

    test('Given I the grand calculated summary section is now incomplete, When I return to the section, Then I am taken to each updated grand calculated summary to confirm the new total', async () => {
      const grandCalculatedSummary3Page = new GrandCalculatedSummary3Page(page)
      const grandCalculatedSummary4Page = new GrandCalculatedSummary4Page(page)
      const grandCalculatedSummary5Page = new GrandCalculatedSummary5Page(page)
      const hubPage = new HubPage(page)
      const internetBreakdownBlockPage = new InternetBreakdownBlockPage(page)
      const section6SummaryPage = new Section6SummaryPage(page)
      await hubPage.summaryRowLink('section-6').click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary3Page.pageName))
      await expect(grandCalculatedSummary3Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for monthly spending on bills and services is calculated to be £359.00. Is this correct?'
      )
      await grandCalculatedSummary3Page.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary4Page.pageName))
      await expect(grandCalculatedSummary4Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for internet usage is calculated to be 105 GB. Is this correct?'
      )
      await grandCalculatedSummary4Page.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary5Page.pageName))
      await expect(grandCalculatedSummary5Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for total monthly household expenditure is calculated to be £1,209.00. Is this correct?'
      )
      await grandCalculatedSummary5Page.submit().click()
      await internetBreakdownBlockPage.internetPhone().fill('45')
      await internetBreakdownBlockPage.submit().click()
      await section6SummaryPage.submit().click()
    })

    test('Given I remove a list item involved in the grand calculated summary, When I confirm, Then I am taken to each affected calculated summary to reconfirm, and when I return to the Hub the grand calculated summary is in progress', async () => {
      const calculatedSummary6Page = new CalculatedSummary6Page(page)
      const calculatedSummary7Page = new CalculatedSummary7Page(page)
      const hubPage = new HubPage(page)
      const removeStreamingServicePage = new RemoveStreamingServicePage(page)
      const section5SummaryPage = new Section5SummaryPage(page)
      await expect(hubPage.summaryRowState('section-6')).toHaveText('Completed')
      await hubPage.summaryRowLink('section-5').click()
      await section5SummaryPage.streamingServicesListRemoveLink(1).click()
      await removeStreamingServicePage.yes().click()
      await removeStreamingServicePage.submit().click()
      await expect(calculatedSummary6Page.calculatedSummaryTitle()).toHaveText(
        'Calculated Summary for monthly expenditure on streaming services is calculated to be £34.00. Is this correct?'
      )
      await calculatedSummary6Page.submit().click()
      await expect(calculatedSummary7Page.calculatedSummaryTitle()).toHaveText(
        'Total monthly internet usage on streaming services is calculated to be 30 GB. Is this correct?'
      )
      await calculatedSummary7Page.submit().click()
      await section5SummaryPage.submit().click()
      await expect(hubPage.summaryRowState('section-6')).toHaveText('Partially completed')
    })

    test('Given the section has reverted to partially complete, When I go back to the section, Then I am taken to each grand calculated summary to reconfirm with correct values', async () => {
      const grandCalculatedSummary3Page = new GrandCalculatedSummary3Page(page)
      const grandCalculatedSummary4Page = new GrandCalculatedSummary4Page(page)
      const grandCalculatedSummary5Page = new GrandCalculatedSummary5Page(page)
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink('section-6').click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary3Page.pageName))
      await expect(grandCalculatedSummary3Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for monthly spending on bills and services is calculated to be £349.00. Is this correct?'
      )
      await grandCalculatedSummary3Page.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary4Page.pageName))
      await expect(grandCalculatedSummary4Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for internet usage is calculated to be 85 GB. Is this correct?'
      )
      await grandCalculatedSummary4Page.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummary5Page.pageName))
      await expect(grandCalculatedSummary5Page.grandCalculatedSummaryTitle()).toHaveText(
        'Grand Calculated Summary for total monthly household expenditure is calculated to be £1,199.00. Is this correct?'
      )
    })

    test('Given I have a further section depending on the grand calculated summary section, When I return to the Hub, Then I see the new section is available', async () => {
      const grandCalculatedSummary5Page = new GrandCalculatedSummary5Page(page)
      const hubPage = new HubPage(page)
      const internetBreakdownBlockPage = new InternetBreakdownBlockPage(page)
      const section6SummaryPage = new Section6SummaryPage(page)
      await grandCalculatedSummary5Page.submit().click()
      await internetBreakdownBlockPage.internetPhone().fill('25')
      await internetBreakdownBlockPage.submit().click()
      await section6SummaryPage.submit().click()
      await expect(hubPage.summaryRowState('section-7')).toHaveText('Not started')
      await hubPage.submit().click()
    })

    test('Given I use a grand calculated summary value as a maximum, When I enter a value that is too large, Then I see a validation error', async () => {
      const personalExpenditureBlockPage = new PersonalExpenditureBlockPage(page)
      await expect(personalExpenditureBlockPage.questionTitle()).toContainText('How much of the £1,199.00 household expenditure do you contribute personally?')
      await personalExpenditureBlockPage.personalExpenditure().fill('1200')
      await personalExpenditureBlockPage.submit().click()
      await expect(personalExpenditureBlockPage.errorNumber(1)).toHaveText('Enter an answer less than or equal to £1,199.00')
    })

    test('Given I display multiple grand calculated summaries on an Interstitial page, When I reach the page, Then I see the correct values piped in', async () => {
      const grandCalculatedSummaryPipingPage = new GrandCalculatedSummaryPipingPage(page)
      const personalExpenditureBlockPage = new PersonalExpenditureBlockPage(page)
      await personalExpenditureBlockPage.personalExpenditure().fill('1100')
      await personalExpenditureBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryPipingPage.pageName))
      await expect(page.locator('#main-content')).toContainText('Total household expenditure: £1,199.00')
      await expect(page.locator('#main-content')).toContainText('Personal contribution: £1,100.00')
      await expect(page.locator('#main-content')).toContainText('Total internet usage: 85 GB')
      await expect(page.locator('#main-content')).toContainText('Usage by phone: 25 GB')
      await expect(page.locator('#main-content')).toContainText('Usage by PC: 60 GB')
    })
  })
})
