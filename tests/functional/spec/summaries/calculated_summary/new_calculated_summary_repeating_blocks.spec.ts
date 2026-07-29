import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../fixtures/test'
import SectionOnePage from '../../../generated_pages/new_calculated_summary_repeating_blocks/section-1-summary.page'
import SectionTwoPage from '../../../generated_pages/new_calculated_summary_repeating_blocks/section-2-summary.page'
import BlockCarPage from '../../../generated_pages/new_calculated_summary_repeating_blocks/block-car.page'
import AddTransportPage from '../../../generated_pages/new_calculated_summary_repeating_blocks/list-collector-add.page'
import RemoveTransportPage from '../../../generated_pages/new_calculated_summary_repeating_blocks/list-collector-remove.page'
import TransportRepeatingBlock1Page from '../../../generated_pages/new_calculated_summary_repeating_blocks/transport-repeating-block-1-repeating-block.page'
import TransportRepeatingBlock2Page from '../../../generated_pages/new_calculated_summary_repeating_blocks/transport-repeating-block-2-repeating-block.page'
import ListCollectorPage from '../../../generated_pages/new_calculated_summary_repeating_blocks/list-collector.page'
import CalculatedSummarySpendingPage from '../../../generated_pages/new_calculated_summary_repeating_blocks/calculated-summary-spending.page'
import CalculatedSummaryCountPage from '../../../generated_pages/new_calculated_summary_repeating_blocks/calculated-summary-count.page'
import HubPage from '../../../base_pages/hub.page'
import FamilyJourneysPage from '../../../generated_pages/new_calculated_summary_repeating_blocks/family-journeys.page'
import BlockSkipPage from '../../../generated_pages/new_calculated_summary_repeating_blocks/block-skip.page'
import { assertSummaryValues, repeatingAnswerChangeLink } from '../../../helpers'

test.describe('Feature: Calculated Summary using Repeating Blocks', () => {
  test.describe.configure({ mode: 'serial' })

  let context: BrowserContext
  let page: Page
  let openQuestionnaire: OpenQuestionnaire

  test.beforeAll('Reaching the first calculated summary', async ({ browser }) => {
    context = await browser.newContext()
    page = await context.newPage()
    openQuestionnaire = createOpenQuestionnaire(page)
    const addTransportPage = new AddTransportPage(page)
    const blockCarPage = new BlockCarPage(page)
    const blockSkipPage = new BlockSkipPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const transportRepeatingBlock1Page = new TransportRepeatingBlock1Page(page)
    const transportRepeatingBlock2Page = new TransportRepeatingBlock2Page(page)
    await openQuestionnaire('test_new_calculated_summary_repeating_blocks.json')
    await blockCarPage.car().fill('100')
    await blockCarPage.submit().click()
    await blockSkipPage.no().click()
    await blockSkipPage.submit().click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await addTransportPage.transportName().selectOption('Bus')
    await addTransportPage.submit().click()
    await transportRepeatingBlock1Page.transportCompany().fill('First')
    await transportRepeatingBlock1Page.transportCost().fill('30')
    await transportRepeatingBlock1Page.transportAdditionalCost().fill('5')
    await transportRepeatingBlock1Page.submit().click()
    await transportRepeatingBlock2Page.transportCount().fill('10')
    await transportRepeatingBlock2Page.submit().click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await addTransportPage.transportName().selectOption('Plane')
    await addTransportPage.submit().click()
    await transportRepeatingBlock1Page.transportCompany().fill('EasyJet')
    await transportRepeatingBlock1Page.transportCost().fill('0')
    await transportRepeatingBlock1Page.transportAdditionalCost().fill('265')
    await transportRepeatingBlock1Page.submit().click()
    await transportRepeatingBlock2Page.transportCount().fill('2')
    await transportRepeatingBlock2Page.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
  })

  test.afterAll(async () => {
    await context.close()
  })

  test('Given I have a calculated summary using both list repeating block and static answers, When I reach the calculated summary page, Then I see the correct items and total.', async () => {
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    await expect(calculatedSummarySpendingPage.calculatedSummaryTitle()).toContainText(
      'We calculate the total monthly expenditure on transport to be £400.00. Is this correct?'
    )
    await assertSummaryValues(page, ['£100.00', '£30.00', '£5.00', '£0.00', '£265.00', '£400.00'])
    await expect(calculatedSummarySpendingPage.summaryItems()).toContainText('Monthly expenditure travelling by car')
    await expect(calculatedSummarySpendingPage.summaryItems()).toContainText('Monthly season ticket expenditure for travel by Bus')
    await expect(calculatedSummarySpendingPage.summaryItems()).toContainText('Additional monthly expenditure for travel by Bus')
    await expect(calculatedSummarySpendingPage.summaryItems()).toContainText('Monthly season ticket expenditure for travel by Plane')
    await expect(calculatedSummarySpendingPage.summaryItems()).toContainText('Additional monthly expenditure for travel by Plane')
    await calculatedSummarySpendingPage.submit().click()
  })

  test('Given I have a calculated summary using a single answer from a repeating block, When I reach the calculated summary page, Then I see the correct items and total', async () => {
    const calculatedSummaryCountPage = new CalculatedSummaryCountPage(page)
    await expect(calculatedSummaryCountPage.calculatedSummaryTitle()).toContainText(
      'We calculate the total journeys made per month to be 12. Is this correct?'
    )
    await assertSummaryValues(page, ['10', '2', '12'])
    await expect(calculatedSummaryCountPage.summaryItems()).toContainText('Monthly journeys by Bus')
    await expect(calculatedSummaryCountPage.summaryItems()).toContainText('Monthly journeys by Plane')
    await calculatedSummaryCountPage.submit().click()
  })

  test('Given I add a new item to the list, When I complete the repeating blocks and press continue, Then I see the first calculated summary page which the updated total', async () => {
    const addTransportPage = new AddTransportPage(page)
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const sectionOnePage = new SectionOnePage(page)
    const transportRepeatingBlock1Page = new TransportRepeatingBlock1Page(page)
    const transportRepeatingBlock2Page = new TransportRepeatingBlock2Page(page)
    await sectionOnePage.transportListAddLink().click()
    await addTransportPage.transportName().selectOption('Train')
    await addTransportPage.submit().click()
    await transportRepeatingBlock1Page.transportCompany().fill('Great Western Railway')
    await transportRepeatingBlock1Page.transportCost().fill('100')
    await transportRepeatingBlock1Page.transportAdditionalCost().fill('50')
    await transportRepeatingBlock1Page.submit().click()
    await transportRepeatingBlock2Page.transportCount().fill('6')
    await transportRepeatingBlock2Page.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummarySpendingPage.pageName))
    await expect(calculatedSummarySpendingPage.calculatedSummaryTitle()).toContainText(
      'We calculate the total monthly expenditure on transport to be £550.00. Is this correct?'
    )
    await assertSummaryValues(page, ['£100.00', '£30.00', '£5.00', '£0.00', '£265.00', '£100.00', '£50.00', '£550.00'])
  })

  test('Given I am on the first calculated summary, When I confirm the total, Then I see the second calculated summary with an updated total', async () => {
    const calculatedSummaryCountPage = new CalculatedSummaryCountPage(page)
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    await calculatedSummarySpendingPage.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryCountPage.pageName))
    await expect(calculatedSummaryCountPage.calculatedSummaryTitle()).toContainText(
      'We calculate the total journeys made per month to be 18. Is this correct?'
    )
    await assertSummaryValues(page, ['10', '2', '6', '18'])
    await calculatedSummaryCountPage.previous().click()
  })

  test('Given I am on the first calculated summary, When I use one of the change links, Then I see the correct repeating block', async () => {
    const transportRepeatingBlock1Page = new TransportRepeatingBlock1Page(page)
    await repeatingAnswerChangeLink(page, 1).click()
    await expect(page).toHaveURL(new RegExp(transportRepeatingBlock1Page.pageName))
  })

  test('Given I have used a change link on a calculated summary to go back to the first repeating block, When I press continue, Then I see the calculated summary I came from', async () => {
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    const transportRepeatingBlock1Page = new TransportRepeatingBlock1Page(page)
    await transportRepeatingBlock1Page.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummarySpendingPage.pageName))
  })

  test('Given I am on a calculated summary with change links for repeating blocks, When I use a change link and click previous, Then I see the calculated summary I came from', async () => {
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    const transportRepeatingBlock1Page = new TransportRepeatingBlock1Page(page)
    await repeatingAnswerChangeLink(page, 1).click()
    await transportRepeatingBlock1Page.previous().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummarySpendingPage.pageName))
  })

  test('Given I use a repeating block change link on the first calculated summary, When I edit my answer and press continue, Then I see the first calculated summary with a new correct total', async () => {
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    const transportRepeatingBlock1Page = new TransportRepeatingBlock1Page(page)
    await repeatingAnswerChangeLink(page, 1).click()
    await transportRepeatingBlock1Page.transportCost().fill('60')
    await transportRepeatingBlock1Page.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummarySpendingPage.pageName))
    await expect(calculatedSummarySpendingPage.calculatedSummaryTitle()).toContainText(
      'We calculate the total monthly expenditure on transport to be £580.00. Is this correct?'
    )
    await assertSummaryValues(page, ['£100.00', '£60.00', '£5.00', '£0.00', '£265.00', '£100.00', '£50.00', '£580.00'])
    await calculatedSummarySpendingPage.submit().click()
  })

  test('Given I use a repeating block change link on the second calculated summary, When I edit my answer and press continue, Then I see the second calculated summary with a new correct total', async () => {
    const calculatedSummaryCountPage = new CalculatedSummaryCountPage(page)
    const transportRepeatingBlock2Page = new TransportRepeatingBlock2Page(page)
    await repeatingAnswerChangeLink(page, 2).click()
    await transportRepeatingBlock2Page.transportCount().fill('12')
    await transportRepeatingBlock2Page.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryCountPage.pageName))
    await expect(calculatedSummaryCountPage.calculatedSummaryTitle()).toContainText(
      'We calculate the total journeys made per month to be 24. Is this correct?'
    )
    await assertSummaryValues(page, ['10', '2', '12', '24'])
    await calculatedSummaryCountPage.submit().click()
  })

  test(
    'Given I use a remove link for on the summary page, ' +
      "When I press yes to confirm deleting the item, Then I see see the first calculated summary where I'm asked to reconfirm the total",
    async () => {
      const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
      const removeTransportPage = new RemoveTransportPage(page)
      const sectionOnePage = new SectionOnePage(page)
      await sectionOnePage.transportListRemoveLink(1).click()
      await removeTransportPage.yes().click()
      await removeTransportPage.submit().click()
      await expect(page).toHaveURL(new RegExp(calculatedSummarySpendingPage.pageName))
      await expect(calculatedSummarySpendingPage.calculatedSummaryTitle()).toContainText(
        'We calculate the total monthly expenditure on transport to be £515.00. Is this correct?'
      )
      await assertSummaryValues(page, ['£100.00', '£0.00', '£265.00', '£100.00', '£50.00', '£515.00'])
    }
  )

  test('Given I have confirmed the first updated total, When I press continue, Then I see the next calculated summary to confirm that total too', async () => {
    const calculatedSummaryCountPage = new CalculatedSummaryCountPage(page)
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    await calculatedSummarySpendingPage.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryCountPage.pageName))
    await expect(calculatedSummaryCountPage.calculatedSummaryTitle()).toContainText(
      'We calculate the total journeys made per month to be 14. Is this correct?'
    )
    await assertSummaryValues(page, ['2', '12', '14'])
  })

  test('Given I have a second section, When I begin and answer the first question with a total higher than the calculated summary, Then I see an error message preventing me from continuing', async () => {
    const calculatedSummaryCountPage = new CalculatedSummaryCountPage(page)
    const familyJourneysPage = new FamilyJourneysPage(page)
    const hubPage = new HubPage(page)
    const sectionOnePage = new SectionOnePage(page)
    await calculatedSummaryCountPage.submit().click()
    await sectionOnePage.submit().click()
    await hubPage.submit().click()
    await expect(familyJourneysPage.questionTitle()).toContainText('How many of your 14 journeys are to visit family?')
    await familyJourneysPage.answer().fill('15')
    await familyJourneysPage.submit().click()
    await expect(familyJourneysPage.singleErrorLink()).toContainText('Enter an answer less than or equal to 14')
  })

  test('Given I enter a value below the calculated summary from section 1, When I press Continue, Then I see my answer displayed on the next page', async () => {
    const familyJourneysPage = new FamilyJourneysPage(page)
    const sectionTwoPage = new SectionTwoPage(page)
    await familyJourneysPage.answer().fill('10')
    await familyJourneysPage.submit().click()
    await expect(sectionTwoPage.familyJourneysQuestion()).toContainText('How many of your 14 journeys are to visit family?')
    await expect(sectionTwoPage.familyJourneysAnswer()).toContainText('10')
    await sectionTwoPage.submit().click()
  })

  test('Given I use the add list item link, When I add a new item and return to the Hub, Then I see the progress of section 2 has reverted to Partially Complete', async () => {
    const addTransportPage = new AddTransportPage(page)
    const calculatedSummaryCountPage = new CalculatedSummaryCountPage(page)
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    const hubPage = new HubPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const sectionOnePage = new SectionOnePage(page)
    const transportRepeatingBlock1Page = new TransportRepeatingBlock1Page(page)
    const transportRepeatingBlock2Page = new TransportRepeatingBlock2Page(page)
    await expect(hubPage.summaryRowState('section-1')).toHaveText('Completed')
    await expect(hubPage.summaryRowState('section-2')).toHaveText('Completed')
    await hubPage.summaryRowLink('section-1').click()
    await sectionOnePage.transportListAddLink().click()
    await addTransportPage.transportName().selectOption('Tube')
    await addTransportPage.submit().click()
    await transportRepeatingBlock1Page.submit().click()
    await transportRepeatingBlock2Page.transportCount().fill('2')
    await transportRepeatingBlock2Page.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await calculatedSummarySpendingPage.submit().click()
    await calculatedSummaryCountPage.submit().click()
    await page.goto(hubPage.url())
    await expect(hubPage.summaryRowState('section-1')).toHaveText('Completed')
    await expect(hubPage.summaryRowState('section-2')).toHaveText('Partially completed')
  })

  test('Given I complete section-2 again, When I remove a list item and return to the Hub, Then I see the progress of section 2 has reverted to Partially Complete', async () => {
    const calculatedSummaryCountPage = new CalculatedSummaryCountPage(page)
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    const familyJourneysPage = new FamilyJourneysPage(page)
    const hubPage = new HubPage(page)
    const removeTransportPage = new RemoveTransportPage(page)
    const sectionOnePage = new SectionOnePage(page)
    const sectionTwoPage = new SectionTwoPage(page)
    await hubPage.submit().click()
    await familyJourneysPage.answer().fill('16')
    await familyJourneysPage.submit().click()
    await sectionTwoPage.submit().click()
    await expect(hubPage.summaryRowState('section-1')).toHaveText('Completed')
    await expect(hubPage.summaryRowState('section-2')).toHaveText('Completed')
    await hubPage.summaryRowLink('section-1').click()
    await sectionOnePage.transportListRemoveLink(3).click()
    await removeTransportPage.yes().click()
    await removeTransportPage.submit().click()
    await calculatedSummarySpendingPage.submit().click()
    await calculatedSummaryCountPage.submit().click()
    await sectionOnePage.submit().click()
    await expect(hubPage.summaryRowState('section-1')).toHaveText('Completed')
    await expect(hubPage.summaryRowState('section-2')).toHaveText('Partially completed')
  })

  test('Given I have a question which removes the list collector from the path, When I change my answer to the question removing the list collector and route backwards from the summary, Then I see the first calculated summary with an updated total', async () => {
    const blockSkipPage = new BlockSkipPage(page)
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    const hubPage = new HubPage(page)
    const sectionOnePage = new SectionOnePage(page)
    await hubPage.summaryRowLink('section-1').click()
    await sectionOnePage.answerSkipEdit().click()
    await blockSkipPage.yes().click()
    await blockSkipPage.submit().click()
    // calculated summary progress is not altered by removing the list collector from the path so next location is summary page
    await expect(page).toHaveURL(new RegExp(sectionOnePage.pageName))
    await sectionOnePage.previous().click()
    // other calculated summary should not be on the path, so go straight back to the spending one which now has none of the list items
    await expect(page).toHaveURL(new RegExp(calculatedSummarySpendingPage.pageName))
    await expect(calculatedSummarySpendingPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the total monthly expenditure on transport to be £100.00. Is this correct?'
    )
    await assertSummaryValues(page, ['£100.00', '£100.00'])
  })

  test('Given I confirm the calculated summary and finish the section, When I return to the Hub, Then I see that section 2 is no longer available', async () => {
    const calculatedSummarySpendingPage = new CalculatedSummarySpendingPage(page)
    const hubPage = new HubPage(page)
    const sectionOnePage = new SectionOnePage(page)
    await calculatedSummarySpendingPage.submit().click()
    await sectionOnePage.submit().click()
    // section 2 is now gone
    await expect(hubPage.summaryItems()).toHaveCount(1)
  })
})
