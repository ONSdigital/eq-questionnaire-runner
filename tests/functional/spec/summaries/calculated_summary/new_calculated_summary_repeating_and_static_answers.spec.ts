import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../fixtures/test'
import HubPage from '../../../base_pages/hub.page'
import AnySupermarketPage from '../../../generated_pages/new_calculated_summary_repeating_and_static_answers/any-supermarket.page'
import ListCollectorPage from '../../../generated_pages/new_calculated_summary_repeating_and_static_answers/list-collector.page'
import ExtraSpendingBlockPage from '../../../generated_pages/new_calculated_summary_repeating_and_static_answers/extra-spending-block.page'
import CalculatedSummarySpendingPage from '../../../generated_pages/new_calculated_summary_repeating_and_static_answers/calculated-summary-spending.page'
import CalculatedSummaryVisitsPage from '../../../generated_pages/new_calculated_summary_repeating_and_static_answers/calculated-summary-visits.page'
import ListCollectorAddPage from '../../../generated_pages/new_calculated_summary_repeating_and_static_answers/list-collector-add.page'
import DynamicAnswerPage from '../../../generated_pages/new_calculated_summary_repeating_and_static_answers/dynamic-answer.page'
import SummaryPage from '../../../generated_pages/new_calculated_summary_repeating_and_static_answers/section-1-summary.page'
import ExtraSpendingMethodBlockPage from '../../../generated_pages/new_calculated_summary_repeating_and_static_answers/extra-spending-method-block.page'
import ListCollectorRemovePage from '../../../generated_pages/new_calculated_summary_repeating_and_static_answers/list-collector-remove.page'
import SupermarketTransportPage from '../../../generated_pages/new_calculated_summary_repeating_and_static_answers/supermarket-transport.page'
import SupermarketTransportCostPage from '../../../generated_pages/new_calculated_summary_repeating_and_static_answers/supermarket-transport-cost.page'
import CalculatedSummaryPipingPage from '../../../generated_pages/new_calculated_summary_repeating_and_static_answers/calculated-summary-piping.page'
import { assertSummaryValues } from '../../../helpers'

test.describe('Calculated summary with repeating answers', () => {
  test.describe.configure({ mode: 'serial' })

  const summaryActions = 'dd[class="ons-summary__actions"]'
  const dynamicAnswerChangeLink = (page: Page, answerIndex: number): ReturnType<Page['locator']> => page.locator(summaryActions).nth(answerIndex).locator('a')

  let context: BrowserContext
  let page: Page
  let openQuestionnaire: OpenQuestionnaire

  test.beforeAll('Completing the list collector and dynamic answer', async ({ browser }) => {
    context = await browser.newContext()
    page = await context.newPage()
    openQuestionnaire = createOpenQuestionnaire(page)
    const anySupermarketPage = new AnySupermarketPage(page)
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    const extraSpendingBlockPage = new ExtraSpendingBlockPage(page)
    const hubPage = new HubPage(page)
    const listCollectorAddPage = new ListCollectorAddPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    await openQuestionnaire('test_new_calculated_summary_repeating_and_static_answers.json')
    await hubPage.acceptCookies().click()
    await anySupermarketPage.yes().click()
    await anySupermarketPage.submit().click()
    await listCollectorAddPage.supermarketName().fill('Tesco')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await listCollectorAddPage.supermarketName().fill('Lidl')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await dynamicAnswerPage.inputs().nth(0).fill('300')
    await dynamicAnswerPage.inputs().nth(1).fill('200')
    await dynamicAnswerPage.inputs().nth(2).fill('30')
    await dynamicAnswerPage.inputs().nth(3).fill('15')
    await dynamicAnswerPage.inputs().nth(4).fill('4')
    await dynamicAnswerPage.inputs().nth(5).fill('2')
    await dynamicAnswerPage.extraStatic().fill('5')
    await dynamicAnswerPage.submit().click()
    await extraSpendingBlockPage.extraSpending().fill('0')
  })

  test.afterAll(async () => {
    await context.close()
  })

  test(
    'Given I complete all list collector dynamic answers for two calculated summaries one of which also has static answers, ' +
      "I'm taken to each one in turn, showing the correct answers",
    async () => {
      const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
      const calculatedSummaryVisitsPage = new CalculatedSummaryVisitsPage(page)
      const extraSpendingBlockPage = new ExtraSpendingBlockPage(page)
      await extraSpendingBlockPage.submit().click()
      await expect(calculatedSummarySpendingPage.calculatedSummaryTitle()).toHaveText(
        'We calculate the total cost of your weekly shopping to be £550.00. Is this correct?'
      )
      await expect(calculatedSummarySpendingPage.calculatedSummaryAnswer()).toHaveText('£550.00')
      await assertSummaryValues(page, ['£300.00', '£200.00', '£30.00', '£15.00', '£5.00', '£0.00', '£550.00'])
      await calculatedSummarySpendingPage.submit().click()
      await expect(calculatedSummaryVisitsPage.calculatedSummaryTitle()).toHaveText('We calculate the total visits to the shop to be 6. Is this correct?')
      await assertSummaryValues(page, ['4', '2', '6'])
    }
  )

  test('Given I click on a change link, When I use the previous button, I return to the calculated summary', async () => {
    const calculatedSummaryVisitsPage = new CalculatedSummaryVisitsPage(page)
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    await dynamicAnswerChangeLink(page, 1).click()
    await expect(page).toHaveURL(new RegExp(dynamicAnswerPage.pageName))
    await dynamicAnswerPage.previous().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryVisitsPage.pageName))
  })

  test('Given I click on a change link, edit an answer and continue, I return to the calculated summary to reconfirm it', async () => {
    const calculatedSummaryVisitsPage = new CalculatedSummaryVisitsPage(page)
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    await dynamicAnswerChangeLink(page, 0).click()
    await dynamicAnswerPage.inputs().nth(5).fill('3')
    await dynamicAnswerPage.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryVisitsPage.pageName))
    await expect(calculatedSummaryVisitsPage.calculatedSummaryTitle()).toHaveText('We calculate the total visits to the shop to be 7. Is this correct?')
    await assertSummaryValues(page, ['4', '3', '7'])
    await calculatedSummaryVisitsPage.submit().click()
  })

  test('Given I go back and change an answer that opens up a new question before the calculated summary, I am taken to the new question, and then the calculated summary', async () => {
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    const extraSpendingBlockPage = new ExtraSpendingBlockPage(page)
    const extraSpendingMethodBlockPage = new ExtraSpendingMethodBlockPage(page)
    const summaryPage = new SummaryPage(page)
    await summaryPage.extraSpendingAnswerEdit().click()
    await extraSpendingBlockPage.extraSpending().fill('50')
    await extraSpendingBlockPage.submit().click()

    // new question
    await expect(page).toHaveURL(new RegExp(extraSpendingMethodBlockPage.pageName))
    await extraSpendingMethodBlockPage.yes().click()
    await extraSpendingMethodBlockPage.submit().click()

    // then calculated summary
    await expect(page).toHaveURL(new RegExp(calculatedSummarySpendingPage.pageName))
    await expect(calculatedSummarySpendingPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the total cost of your weekly shopping to be £600.00. Is this correct?'
    )

    // then jump straight back to section summary (as other calculated summary is unchanged
    await calculatedSummarySpendingPage.submit().click()
    await expect(page).toHaveURL(new RegExp(summaryPage.pageName))
  })

  test('Given I add a new item to the list, I return to the list collector block, then the dynamic answers, then both calculated summaries to confirm newly added answers', async () => {
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    const calculatedSummaryVisitsPage = new CalculatedSummaryVisitsPage(page)
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    const listCollectorAddPage = new ListCollectorAddPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const summaryPage = new SummaryPage(page)
    await summaryPage.supermarketsListAddLink().click()
    await listCollectorAddPage.supermarketName().fill('Sainsburys')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()

    // return to dynamic answer
    await expect(page).toHaveURL(new RegExp(dynamicAnswerPage.pageName))
    await dynamicAnswerPage.inputs().nth(2).fill('100')
    await dynamicAnswerPage.inputs().nth(5).fill('10')
    await dynamicAnswerPage.inputs().nth(8).fill('7')
    await dynamicAnswerPage.submit().click()

    // first calc summary
    await expect(page).toHaveURL(new RegExp(calculatedSummarySpendingPage.pageName))
    await expect(calculatedSummarySpendingPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the total cost of your weekly shopping to be £710.00. Is this correct?'
    )
    await assertSummaryValues(page, ['£300.00', '£200.00', '£100.00', '£30.00', '£15.00', '£10.00', '£5.00', '£50.00', '£710.00'])

    // second calculated summary
    await calculatedSummarySpendingPage.submit().click()
    await expect(calculatedSummaryVisitsPage.calculatedSummaryTitle()).toHaveText('We calculate the total visits to the shop to be 14. Is this correct?')
    await assertSummaryValues(page, ['4', '3', '7', '14'])
    await calculatedSummaryVisitsPage.submit().click()
    await expect(page).toHaveURL(new RegExp(summaryPage.pageName))
  })

  test('Given I remove an item from the list which changes the calculated summaries, I return to each incomplete block only to confirm new dynamic answers and totals with answers removed', async () => {
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    const calculatedSummaryVisitsPage = new CalculatedSummaryVisitsPage(page)
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    const listCollectorRemovePage = new ListCollectorRemovePage(page)
    const summaryPage = new SummaryPage(page)
    await expect(summaryPage.supermarketsListLabel(1)).toHaveText('Tesco')
    await expect(summaryPage.supermarketsListLabel(2)).toHaveText('Lidl')
    await expect(summaryPage.supermarketsListLabel(3)).toHaveText('Sainsburys')
    await expect(summaryPage.supermarketsListLabel(4)).not.toBeVisible()
    await summaryPage.supermarketsListRemoveLink(1).click()

    await expect(page).toHaveURL(new RegExp(listCollectorRemovePage.pageName))
    await listCollectorRemovePage.yes().click()
    await listCollectorRemovePage.submit().click()

    // section is now incomplete as dynamic answers and calculated summary depend on the removed item - step through each incomplete block only
    await expect(page).toHaveURL(new RegExp(dynamicAnswerPage.pageName))
    await dynamicAnswerPage.submit().click()

    // Tesco is now gone
    await expect(calculatedSummarySpendingPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the total cost of your weekly shopping to be £380.00. Is this correct?'
    )
    await assertSummaryValues(page, ['£200.00', '£100.00', '£15.00', '£10.00', '£5.00', '£50.00', '£380.00'])
    await calculatedSummarySpendingPage.submit().click()
    await expect(calculatedSummaryVisitsPage.calculatedSummaryTitle()).toHaveText('We calculate the total visits to the shop to be 10. Is this correct?')
    await assertSummaryValues(page, ['3', '7', '10'])
    await calculatedSummaryVisitsPage.submit().click()

    await expect(summaryPage.supermarketsListLabel(1)).toHaveText('Lidl')
    await expect(summaryPage.supermarketsListLabel(2)).toHaveText('Sainsburys')
    await expect(summaryPage.supermarketsListLabel(3)).not.toBeVisible()
  })

  test('Given I proceed to the second section and enter a value greater than the calculated summary from the previous section, the correct error message is displayed', async () => {
    const hubPage = new HubPage(page)
    const summaryPage = new SummaryPage(page)
    const supermarketTransportPage = new SupermarketTransportPage(page)
    await summaryPage.submit().click()
    await hubPage.submit().click()
    await supermarketTransportPage.weeklyCarTrips().fill('11')
    await supermarketTransportPage.submit().click()
    await expect(supermarketTransportPage.singleErrorLink()).toHaveText('Enter an answer less than or equal to 10')
  })

  test('Given I change my answer to a value less than the calculated summary from the previous section, I am able to proceed', async () => {
    const supermarketTransportCostPage = new SupermarketTransportCostPage(page)
    const supermarketTransportPage = new SupermarketTransportPage(page)
    await supermarketTransportPage.weeklyCarTrips().fill('9')
    await supermarketTransportPage.submit().click()
    await expect(page).toHaveURL(new RegExp(supermarketTransportCostPage.pageName))
  })

  test('Given I reach the final block, the calculated summary of dynamic answers is piped in correctly', async () => {
    const calculatedSummaryPipingPage = new CalculatedSummaryPipingPage(page)
    const supermarketTransportCostPage = new SupermarketTransportCostPage(page)
    await supermarketTransportCostPage.weeklyTripsCost().fill('30')
    await supermarketTransportCostPage.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryPipingPage.pageName))
    await expect(page.locator('#main-content')).toContainText('Total weekly supermarket spending: £380.00')
    await expect(page.locator('#main-content')).toContainText('Total weekly supermarket visits: 10')
    await expect(page.locator('#main-content')).toContainText('Total of supermarket visits by car: 9')
    await expect(page.locator('#main-content')).toContainText('Total spending on parking: £30.00')
    await calculatedSummaryPipingPage.submit().click()
  })

  test('Given I return to section 1 and update the calculated summary used in section 2 validation, the progress of section 2 is updated', async () => {
    const calculatedSummaryVisitsPage = new CalculatedSummaryVisitsPage(page)
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    const hubPage = new HubPage(page)
    const summaryPage = new SummaryPage(page)
    await expect(hubPage.summaryRowState('section-1')).toHaveText('Completed')
    await expect(hubPage.summaryRowState('section-2')).toHaveText('Completed')
    await hubPage.summaryRowLink('section-1').click()
    await dynamicAnswerChangeLink(page, 8).click()
    await dynamicAnswerPage.inputs().nth(5).fill('1')
    await dynamicAnswerPage.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryVisitsPage.pageName))
    await calculatedSummaryVisitsPage.submit().click()
    await summaryPage.submit().click()
    await expect(hubPage.summaryRowState('section-1')).toHaveText('Completed')
    await expect(hubPage.summaryRowState('section-2')).toHaveText('Partially completed')
  })
})
