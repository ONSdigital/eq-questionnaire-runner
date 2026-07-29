import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../fixtures/test'
import { assertSummaryValues } from '../../../helpers'
import AddVehiclePage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/list-collector-add.page'
import AnyCostPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/any-cost.page'
import AnyVehiclePage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/any-vehicle.page'
import BaseCostPaymentBreakdownPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/base-cost-payment-breakdown.page'
import BaseCostsSectionPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/base-costs-section-summary.page'
import CalculatedSummaryBaseCostPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/calculated-summary-base-cost.page'
import CalculatedSummaryRunningCostPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/calculated-summary-running-cost.page'
import CostRepeatingBlock1RepeatingBlockPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/cost-repeating-block-1-repeating-block.page'
import DynamicCostBlockPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/dynamic-cost-block.page'
import FinanceCostPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/finance-cost.page'
import GcsBreakdownBlockPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/gcs-breakdown-block.page'
import GcsPipingPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/gcs-piping.page'
import GrandCalculatedSummaryVehiclePage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/grand-calculated-summary-vehicle.page'
import HubPage from '../../../base_pages/hub.page'
import ListCollectorCostAddPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/list-collector-cost-add.page'
import ListCollectorCostPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/list-collector-cost.page'
import ListCollectorCostRemovePage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/list-collector-cost-remove.page'
import ListCollectorPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/list-collector.page'
import VehicleDetailsSectionPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/vehicle-details-section-summary.page'
import VehicleFuelBlockPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/vehicle-fuel-block.page'
import VehicleMaintenanceBlockPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/vehicle-maintenance-block.page'
import VehiclesSectionPage from '../../../generated_pages/grand_calculated_summary_inside_repeating_section/vehicles-section-summary.page'

test.describe('Grand Calculated Summary inside a repeating section', () => {
  let firstCostListItemId = ''
  let firstVehicleListItemId = ''
  let targetVehicleListItemId = ''
  let targetCostListItemId = ''
  const summaryActions = 'dd[class="ons-summary__actions"]'
  const dynamicAnswerChangeLink = (page: Page, answerIndex: number): ReturnType<Page['locator']> => page.locator(summaryActions).nth(answerIndex).locator('a')
  const listItemIdFromPath = (url: string, listName: 'vehicles' | 'costs'): string => {
    const match = url.match(new RegExp(`/${listName}/([^/]+)/`))
    const listItemId = match?.[1]

    if (listItemId === undefined || listItemId.length === 0) {
      throw new Error(`Unable to extract ${listName} list item ID from URL: ${url}`)
    }

    return listItemId
  }

  test.describe.configure({ mode: 'serial' })

  let context: BrowserContext
  let page: Page
  let openQuestionnaire: OpenQuestionnaire

  test.beforeAll('Load the survey', async ({ browser }) => {
    context = await browser.newContext()
    page = await context.newPage()
    openQuestionnaire = createOpenQuestionnaire(page)
    await openQuestionnaire('test_grand_calculated_summary_inside_repeating_section.json')
  })

  test.afterAll(async () => {
    await context.close()
  })

  test('Given I have a Grand Calculated Summary inside a repeating section, When I reach it for the first list item, Then I see placeholder content rendered correctly', async () => {
    const addVehiclePage = new AddVehiclePage(page)
    const anyCostPage = new AnyCostPage(page)
    const anyVehiclePage = new AnyVehiclePage(page)
    const baseCostPaymentBreakdownPage = new BaseCostPaymentBreakdownPage(page)
    const baseCostsSectionPage = new BaseCostsSectionPage(page)
    const calculatedSummaryBaseCostPage = new CalculatedSummaryBaseCostPage(page)
    const calculatedSummaryRunningCostPage = new CalculatedSummaryRunningCostPage(page)
    const costRepeatingBlock1RepeatingBlockPage = new CostRepeatingBlock1RepeatingBlockPage(page)
    const dynamicCostBlockPage = new DynamicCostBlockPage(page)
    const financeCostPage = new FinanceCostPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    const hubPage = new HubPage(page)
    const listCollectorCostAddPage = new ListCollectorCostAddPage(page)
    const listCollectorCostPage = new ListCollectorCostPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const vehicleFuelBlockPage = new VehicleFuelBlockPage(page)
    const vehicleMaintenanceBlockPage = new VehicleMaintenanceBlockPage(page)
    const vehiclesSectionPage = new VehiclesSectionPage(page)
    await hubPage.submit().click()
    await anyCostPage.yes().click()
    await anyCostPage.submit().click()
    await listCollectorCostAddPage.costName().selectOption('Road Tax')
    await listCollectorCostAddPage.submit().click()
    firstCostListItemId = listItemIdFromPath(page.url(), 'costs')
    await costRepeatingBlock1RepeatingBlockPage.repeatingBlock1CostBase().fill('5')
    await costRepeatingBlock1RepeatingBlockPage.submit().click()
    await listCollectorCostPage.yes().click()
    await listCollectorCostPage.submit().click()
    await listCollectorCostAddPage.costName().selectOption('Parking Permit')
    await listCollectorCostAddPage.submit().click()
    targetCostListItemId = listItemIdFromPath(page.url(), 'costs')
    await costRepeatingBlock1RepeatingBlockPage.repeatingBlock1CostBase().fill('12')
    await costRepeatingBlock1RepeatingBlockPage.submit().click()
    await listCollectorCostPage.no().click()
    await listCollectorCostPage.submit().click()
    await dynamicCostBlockPage.inputs().nth(0).fill('5')
    await dynamicCostBlockPage.inputs().nth(1).fill('8')
    await dynamicCostBlockPage.submit().click()
    await financeCostPage.answer().fill('60')
    await financeCostPage.submit().click()
    await expect(calculatedSummaryBaseCostPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the total base cost for any owned vehicle to be £90.00. Is this correct?'
    )
    await calculatedSummaryBaseCostPage.submit().click()
    await baseCostPaymentBreakdownPage.baseCredit().fill('30')
    await baseCostPaymentBreakdownPage.baseDebit().fill('40')
    await baseCostPaymentBreakdownPage.submit().click()
    await baseCostsSectionPage.submit().click()
    await hubPage.submit().click()
    await anyVehiclePage.yes().click()
    await anyVehiclePage.submit().click()
    await addVehiclePage.vehicleName().selectOption('Car')
    await addVehiclePage.submit().click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await addVehiclePage.vehicleName().selectOption('Van')
    await addVehiclePage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await vehiclesSectionPage.submit().click()
    await hubPage.submit().click()
    await vehicleMaintenanceBlockPage.vehicleMaintenanceCost().fill('100')
    await vehicleMaintenanceBlockPage.submit().click()
    await vehicleFuelBlockPage.vehicleFuelCost().fill('125')
    await vehicleFuelBlockPage.submit().click()
    await expect(calculatedSummaryRunningCostPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the monthly running costs of your Car to be £225.00. Is this correct?'
    )
    await calculatedSummaryRunningCostPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    firstVehicleListItemId = listItemIdFromPath(page.url(), 'vehicles')
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).toHaveText(
      'The total cost of owning and running your Car is calculated to be £315.00. Is this correct?'
    )
    await expect(grandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostLabel()).toHaveText('Vehicle base cost')
    await expect(grandCalculatedSummaryVehiclePage.calculatedSummaryRunningCostLabel()).toHaveText('Monthly Car costs')
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryQuestion()).toHaveText('Grand total Car expenditure')
    await assertSummaryValues(page, ['£90.00', '£225.00', '£315.00'])
  })

  test('Given I immediately use that Grand Calculated Summary for validation, When I enter a sum of values too high, Then I see an error message', async () => {
    const gcsBreakdownBlockPage = new GcsBreakdownBlockPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    await grandCalculatedSummaryVehiclePage.submit().click()
    await gcsBreakdownBlockPage.payDebit().fill('100')
    await gcsBreakdownBlockPage.payCredit().fill('115')
    await gcsBreakdownBlockPage.payOther().fill('200')
    await gcsBreakdownBlockPage.submit().click()
    await expect(gcsBreakdownBlockPage.errorNumber()).toHaveText('Enter answers that add up to 315')
  })

  test('Given I enter a valid value for the Grand Calculated Summary breakdown, When I press continue, Then I see an Interstitial page with my values correctly piped in', async () => {
    const gcsBreakdownBlockPage = new GcsBreakdownBlockPage(page)
    const gcsPipingPage = new GcsPipingPage(page)
    await gcsBreakdownBlockPage.payOther().fill('100')
    await gcsBreakdownBlockPage.submit().click()
    await expect(page).toHaveURL(new RegExp(gcsPipingPage.pageName))
    await expect(page.locator('#main-content')).toContainText('Monthly maintenance cost: £100.00')
    await expect(page.locator('#main-content')).toContainText('Monthly fuel cost: £125.00')
    await expect(page.locator('#main-content')).toContainText('Total base cost: £90.00')
    await expect(page.locator('#main-content')).toContainText('Total running cost: £225.00')
    await expect(page.locator('#main-content')).toContainText('Total owning and running cost: £315.00')
    await expect(page.locator('#main-content')).toContainText('Paid by debit card: £100.00')
    await expect(page.locator('#main-content')).toContainText('Paid by credit card: £115.00')
    await expect(page.locator('#main-content')).toContainText('Paid by other means: £100.00')
  })

  test('Given I have a Grand Calculated Summary inside a repeating section, When I reach it for the second list item, Then I see placeholder content rendered correctly', async () => {
    const calculatedSummaryRunningCostPage = new CalculatedSummaryRunningCostPage(page)
    const gcsPipingPage = new GcsPipingPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    const hubPage = new HubPage(page)
    const vehicleDetailsSectionPage = new VehicleDetailsSectionPage(page)
    const vehicleFuelBlockPage = new VehicleFuelBlockPage(page)
    const vehicleMaintenanceBlockPage = new VehicleMaintenanceBlockPage(page)
    await gcsPipingPage.submit().click()
    await vehicleDetailsSectionPage.submit().click()
    await hubPage.submit().click()
    targetVehicleListItemId = listItemIdFromPath(page.url(), 'vehicles')
    await vehicleMaintenanceBlockPage.vehicleMaintenanceCost().fill('50')
    await vehicleMaintenanceBlockPage.submit().click()
    await vehicleFuelBlockPage.vehicleFuelCost().fill('45')
    await vehicleFuelBlockPage.submit().click()
    await expect(calculatedSummaryRunningCostPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the monthly running costs of your Van to be £95.00. Is this correct?'
    )
    await calculatedSummaryRunningCostPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).toHaveText(
      'The total cost of owning and running your Van is calculated to be £185.00. Is this correct?'
    )
    await expect(grandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostLabel()).toHaveText('Vehicle base cost')
    await expect(grandCalculatedSummaryVehiclePage.calculatedSummaryRunningCostLabel()).toHaveText('Monthly Van costs')
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryQuestion()).toHaveText('Grand total Van expenditure')
    await assertSummaryValues(page, ['£90.00', '£95.00', '£185.00'])
  })

  test('Given I am at a Grand Summary inside a repeating section, When I click the change link for a repeating calculated summary, Then I am taken to the correct page', async () => {
    const calculatedSummaryRunningCostPage = new CalculatedSummaryRunningCostPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    await expect(page).toHaveURL(new RegExp(`vehicles/${targetVehicleListItemId}/`))
    await grandCalculatedSummaryVehiclePage.calculatedSummaryRunningCostEdit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryRunningCostPage.pageName))
    await expect(page).toHaveURL(new RegExp(`vehicles/${targetVehicleListItemId}/`))
  })

  test('Given I have used a change link for a repeating calculated summary, When I click the continue button, Then I am taken to the Grand Calculated Summary', async () => {
    const calculatedSummaryRunningCostPage = new CalculatedSummaryRunningCostPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    await calculatedSummaryRunningCostPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(page).toHaveURL(new RegExp(`vehicles/${targetVehicleListItemId}/`))
  })

  test('Given I am at a Grand Summary inside a repeating section, When I click the change link for a non repeating calculated summary, Then I am taken to the correct page', async () => {
    const calculatedSummaryBaseCostPage = new CalculatedSummaryBaseCostPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    await grandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostEdit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryBaseCostPage.pageName))
  })

  test('Given I have used a change link for a non repeating calculated summary from a repeating section, When I click the continue button, Then I am taken to the Grand Calculated Summary for the correct list item', async () => {
    const calculatedSummaryBaseCostPage = new CalculatedSummaryBaseCostPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    await calculatedSummaryBaseCostPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(page).toHaveURL(new RegExp(`vehicles/${targetVehicleListItemId}/`))
  })

  test('Given I use a change link for a repeating calculated summary, When I use a change link there, Then pressing continue twice takes me back to the correct grand calculated summary', async () => {
    const calculatedSummaryRunningCostPage = new CalculatedSummaryRunningCostPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    const vehicleMaintenanceBlockPage = new VehicleMaintenanceBlockPage(page)
    await grandCalculatedSummaryVehiclePage.calculatedSummaryRunningCostEdit().click()
    await calculatedSummaryRunningCostPage.vehicleMaintenanceCostEdit().click()
    await expect(page).toHaveURL(new RegExp(vehicleMaintenanceBlockPage.pageName))
    await expect(page).toHaveURL(new RegExp(`vehicles/${targetVehicleListItemId}/`))
    await vehicleMaintenanceBlockPage.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryRunningCostPage.pageName))
    await expect(page).toHaveURL(new RegExp(`vehicles/${targetVehicleListItemId}/`))
    await calculatedSummaryRunningCostPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(page).toHaveURL(new RegExp(`vehicles/${targetVehicleListItemId}/`))
  })

  test('Given I use a change link for a non repeating calculated summary, When I use a change link there, Then pressing continue twice takes me back to the correct grand calculated summary', async () => {
    const calculatedSummaryBaseCostPage = new CalculatedSummaryBaseCostPage(page)
    const financeCostPage = new FinanceCostPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    await grandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostEdit().click()
    await calculatedSummaryBaseCostPage.financeCostAnswerEdit().click()
    await expect(page).toHaveURL(new RegExp(financeCostPage.pageName))
    await expect(page).toHaveURL(new RegExp(`return_to_list_item_id=${targetVehicleListItemId}`))
    await financeCostPage.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryBaseCostPage.pageName))
    await expect(page).toHaveURL(new RegExp(`return_to_list_item_id=${targetVehicleListItemId}`))
    await calculatedSummaryBaseCostPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(page).toHaveURL(new RegExp(`vehicles/${targetVehicleListItemId}/`))
  })

  test('Given I change a non repeating answer which results in the section being incomplete, When I press continue, Then I go to the next incomplete location with the list item id preserved', async () => {
    const baseCostPaymentBreakdownPage = new BaseCostPaymentBreakdownPage(page)
    const calculatedSummaryBaseCostPage = new CalculatedSummaryBaseCostPage(page)
    const financeCostPage = new FinanceCostPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    await grandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostEdit().click()
    await calculatedSummaryBaseCostPage.financeCostAnswerEdit().click()
    await financeCostPage.answer().fill('70')
    await financeCostPage.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryBaseCostPage.pageName))
    await expect(calculatedSummaryBaseCostPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the total base cost for any owned vehicle to be £100.00. Is this correct?'
    )
    await calculatedSummaryBaseCostPage.submit().click()
    await expect(page).toHaveURL(new RegExp(baseCostPaymentBreakdownPage.pageName))
    await expect(page).toHaveURL(new RegExp(`return_to_list_item_id=${targetVehicleListItemId}`))
  })

  test('Given I have changed a non repeating answer, When I return to the Grand Calculated Summary, Then I see the correctly updated values', async () => {
    const baseCostPaymentBreakdownPage = new BaseCostPaymentBreakdownPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    await baseCostPaymentBreakdownPage.submit().click()

    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).toHaveText(
      'The total cost of owning and running your Van is calculated to be £195.00. Is this correct?'
    )
  })

  test('Given I change a repeating answer, When I return to the Grand Calculated Summary, Then I see the correctly updated values', async () => {
    const calculatedSummaryRunningCostPage = new CalculatedSummaryRunningCostPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    const vehicleMaintenanceBlockPage = new VehicleMaintenanceBlockPage(page)
    await grandCalculatedSummaryVehiclePage.calculatedSummaryRunningCostEdit().click()
    await calculatedSummaryRunningCostPage.vehicleMaintenanceCostEdit().click()
    await vehicleMaintenanceBlockPage.vehicleMaintenanceCost().fill('75')
    await vehicleMaintenanceBlockPage.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryRunningCostPage.pageName))
    await expect(calculatedSummaryRunningCostPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the monthly running costs of your Van to be £120.00. Is this correct?'
    )
    await calculatedSummaryRunningCostPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).toHaveText(
      'The total cost of owning and running your Van is calculated to be £220.00. Is this correct?'
    )
  })

  test('Given I have edited a static answer whilst completing the repeating section, When I return to the Hub and enter the other repeat, Then I see the breakdown block needs to be revisited', async () => {
    const gcsBreakdownBlockPage = new GcsBreakdownBlockPage(page)
    const gcsPipingPage = new GcsPipingPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    const hubPage = new HubPage(page)
    const vehicleDetailsSectionPage = new VehicleDetailsSectionPage(page)
    await grandCalculatedSummaryVehiclePage.submit().click()
    await gcsBreakdownBlockPage.payDebit().fill('100')
    await gcsBreakdownBlockPage.payCredit().fill('110')
    await gcsBreakdownBlockPage.payOther().fill('10')
    await gcsBreakdownBlockPage.submit().click()
    await gcsPipingPage.submit().click()
    await vehicleDetailsSectionPage.submit().click()
    await hubPage.summaryRowLink('vehicle-details-section-1').click()
    await grandCalculatedSummaryVehiclePage.submit().click()
    await expect(page).toHaveURL(new RegExp(gcsBreakdownBlockPage.pageName))
    await expect(gcsBreakdownBlockPage.questionText()).toHaveText('How do you pay for the monthly fees of £325.00?')
    await gcsBreakdownBlockPage.payCredit().fill('125')
    await gcsBreakdownBlockPage.submit().click()
    await vehicleDetailsSectionPage.submit().click()
    await expect(hubPage.summaryRowState('vehicle-details-section-1')).toHaveText('Completed')
    await expect(hubPage.summaryRowState('vehicle-details-section-2')).toHaveText('Completed')
  })

  test('Given I edit the non-repeating calculated summary, When I return to the Hub, Then I see repeating sections are incomplete', async () => {
    const baseCostPaymentBreakdownPage = new BaseCostPaymentBreakdownPage(page)
    const baseCostsSectionPage = new BaseCostsSectionPage(page)
    const calculatedSummaryBaseCostPage = new CalculatedSummaryBaseCostPage(page)
    const financeCostPage = new FinanceCostPage(page)
    const hubPage = new HubPage(page)
    await hubPage.summaryRowLink('base-costs-section').click()
    await baseCostsSectionPage.financeCostAnswerEdit().click()
    await financeCostPage.answer().fill('80')
    await financeCostPage.submit().click()
    await calculatedSummaryBaseCostPage.submit().click()
    await baseCostPaymentBreakdownPage.submit().click()
    await baseCostsSectionPage.submit().click()
    await expect(hubPage.summaryRowState('vehicle-details-section-1')).toHaveText('Partially completed')
    await expect(hubPage.summaryRowState('vehicle-details-section-2')).toHaveText('Partially completed')
  })

  test('Given I have two partially complete repeating sections, When I press continue, Then I am taken straight to the grand calculated summary as it is the first incomplete block', async () => {
    const gcsBreakdownBlockPage = new GcsBreakdownBlockPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    const hubPage = new HubPage(page)
    const vehicleDetailsSectionPage = new VehicleDetailsSectionPage(page)
    await hubPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(page).toHaveURL(new RegExp(`vehicles/${firstVehicleListItemId}/`))
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).toHaveText(
      'The total cost of owning and running your Car is calculated to be £335.00. Is this correct?'
    )
    await grandCalculatedSummaryVehiclePage.submit().click()
    await expect(page).toHaveURL(new RegExp(gcsBreakdownBlockPage.pageName))
    await gcsBreakdownBlockPage.payCredit().fill('135')
    await gcsBreakdownBlockPage.submit().click()
    await vehicleDetailsSectionPage.submit().click()
  })

  test("Given I've completed the first repeating section, When I press continue, I am taken straight to the grand calculated summary of the second repeat", async () => {
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    const hubPage = new HubPage(page)
    await hubPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(page).toHaveURL(new RegExp(`vehicles/${targetVehicleListItemId}/`))
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).toHaveText(
      'The total cost of owning and running your Van is calculated to be £230.00. Is this correct?'
    )
  })

  test('Given I go to the non-repeating calculated summary, When I click a change link for a dynamic answer and press continue twice, Then I go back to the Grand Calculated Summary for the correct list item', async () => {
    const calculatedSummaryBaseCostPage = new CalculatedSummaryBaseCostPage(page)
    const dynamicCostBlockPage = new DynamicCostBlockPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    await grandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostEdit().click()
    await dynamicAnswerChangeLink(page, 2).click()
    await expect(page).toHaveURL(new RegExp(dynamicCostBlockPage.pageName))
    await dynamicCostBlockPage.submit().click()
    await calculatedSummaryBaseCostPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(page).toHaveURL(new RegExp(`vehicles/${targetVehicleListItemId}/`))
  })

  test('Given I go to the non-repeating calculated summary, When I click a change link for a repeating block answer and press continue twice, Then I go back to the Grand Calculated Summary for the correct list item', async () => {
    const calculatedSummaryBaseCostPage = new CalculatedSummaryBaseCostPage(page)
    const costRepeatingBlock1RepeatingBlockPage = new CostRepeatingBlock1RepeatingBlockPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    await grandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostEdit().click()
    await dynamicAnswerChangeLink(page, 0).click()
    await expect(page).toHaveURL(new RegExp(costRepeatingBlock1RepeatingBlockPage.pageName))
    await expect(page).toHaveURL(new RegExp(`costs/${firstCostListItemId}/`))
    await costRepeatingBlock1RepeatingBlockPage.submit().click()
    await calculatedSummaryBaseCostPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(page).toHaveURL(new RegExp(`vehicles/${targetVehicleListItemId}/`))
  })

  test('Given I edit a dynamic answer from the non-repeating calculated summary, When I return to the Grand Calculated Summary, Then I see the correct total', async () => {
    const baseCostPaymentBreakdownPage = new BaseCostPaymentBreakdownPage(page)
    const calculatedSummaryBaseCostPage = new CalculatedSummaryBaseCostPage(page)
    const dynamicCostBlockPage = new DynamicCostBlockPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    await grandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostEdit().click()
    await dynamicAnswerChangeLink(page, 3).click()
    await dynamicCostBlockPage.inputs().nth(1).fill('28')
    await dynamicCostBlockPage.submit().click()
    await calculatedSummaryBaseCostPage.submit().click()
    await baseCostPaymentBreakdownPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).toHaveText(
      'The total cost of owning and running your Van is calculated to be £250.00. Is this correct?'
    )
  })

  test('Given I edit a repeating block answer from the non-repeating calculated summary, When I return to the Grand Calculated Summary, Then I see the correct total', async () => {
    const baseCostPaymentBreakdownPage = new BaseCostPaymentBreakdownPage(page)
    const calculatedSummaryBaseCostPage = new CalculatedSummaryBaseCostPage(page)
    const costRepeatingBlock1RepeatingBlockPage = new CostRepeatingBlock1RepeatingBlockPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    await grandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostEdit().click()
    await dynamicAnswerChangeLink(page, 1).click()
    await expect(page).toHaveURL(new RegExp(costRepeatingBlock1RepeatingBlockPage.pageName))
    await expect(page).toHaveURL(new RegExp(`costs/${targetCostListItemId}/`))
    await costRepeatingBlock1RepeatingBlockPage.repeatingBlock1CostBase().fill('22')
    await costRepeatingBlock1RepeatingBlockPage.submit().click()
    await calculatedSummaryBaseCostPage.submit().click()
    await baseCostPaymentBreakdownPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).toHaveText(
      'The total cost of owning and running your Van is calculated to be £260.00. Is this correct?'
    )
  })

  test('Given I complete the Grand Calculated Summary, When I press continue, I am taken to the calculation question that depends on it and cant proceed till entering a valid breakdown', async () => {
    const gcsBreakdownBlockPage = new GcsBreakdownBlockPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    const vehicleDetailsSectionPage = new VehicleDetailsSectionPage(page)
    await grandCalculatedSummaryVehiclePage.submit().click()
    await expect(page).toHaveURL(new RegExp(gcsBreakdownBlockPage.pageName))
    await gcsBreakdownBlockPage.submit().click()
    await expect(gcsBreakdownBlockPage.errorNumber()).toHaveText('Enter answers that add up to 260')
    await gcsBreakdownBlockPage.payOther().fill('50')
    await gcsBreakdownBlockPage.submit().click()
    await expect(page).toHaveURL(new RegExp(vehicleDetailsSectionPage.pageName))
  })

  test('Given I have changed a static calculated summary during the section, When I return to the Hub, Then I see the other repeating section is incomplete as it also uses this calculated summary', async () => {
    const hubPage = new HubPage(page)
    const vehicleDetailsSectionPage = new VehicleDetailsSectionPage(page)
    await vehicleDetailsSectionPage.submit().click()
    await expect(hubPage.summaryRowState('vehicle-details-section-1')).toHaveText('Partially completed')
    await expect(hubPage.summaryRowState('vehicle-details-section-2')).toHaveText('Completed')
  })

  test('Given I go to the other repeating section, When I enter the section, Then I see the grand calculated summary with correctly updated totals', async () => {
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    const hubPage = new HubPage(page)
    await hubPage.submit().click()
    await expect(page).toHaveURL(new RegExp(grandCalculatedSummaryVehiclePage.pageName))
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).toHaveText(
      'The total cost of owning and running your Car is calculated to be £365.00. Is this correct?'
    )
  })

  test('Given I the grand calculated summary has changed, When I confirm it, Then I see the breakdown question and need to update the values', async () => {
    const gcsBreakdownBlockPage = new GcsBreakdownBlockPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    const vehicleDetailsSectionPage = new VehicleDetailsSectionPage(page)
    await grandCalculatedSummaryVehiclePage.submit().click()
    await expect(page).toHaveURL(new RegExp(gcsBreakdownBlockPage.pageName))
    await gcsBreakdownBlockPage.payOther().fill('130')
    await gcsBreakdownBlockPage.submit().click()
    await vehicleDetailsSectionPage.submit().click()
  })

  test('Given I remove an item from the costs lists, When I return to the Hub, Then I see both repeating sections revert to partially complete', async () => {
    const baseCostPaymentBreakdownPage = new BaseCostPaymentBreakdownPage(page)
    const baseCostsSectionPage = new BaseCostsSectionPage(page)
    const calculatedSummaryBaseCostPage = new CalculatedSummaryBaseCostPage(page)
    const dynamicCostBlockPage = new DynamicCostBlockPage(page)
    const hubPage = new HubPage(page)
    const listCollectorCostRemovePage = new ListCollectorCostRemovePage(page)
    await hubPage.summaryRowLink('base-costs-section').click()
    await baseCostsSectionPage.costsListRemoveLink(1).click()
    await listCollectorCostRemovePage.yes().click()
    await listCollectorCostRemovePage.submit().click()
    await dynamicCostBlockPage.submit().click()
    await expect(calculatedSummaryBaseCostPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the total base cost for any owned vehicle to be £130.00. Is this correct?'
    )
    await calculatedSummaryBaseCostPage.submit().click()
    await baseCostPaymentBreakdownPage.submit().click()
    await baseCostsSectionPage.submit().click()
    await expect(hubPage.summaryRowState('vehicle-details-section-1')).toHaveText('Partially completed')
    await expect(hubPage.summaryRowState('vehicle-details-section-2')).toHaveText('Partially completed')
  })

  test('Given I revisit both repeating sections, When I start each, Then I see the grand calculated summary page with correct values and must update the breakdown after', async () => {
    const gcsBreakdownBlockPage = new GcsBreakdownBlockPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    const hubPage = new HubPage(page)
    const vehicleDetailsSectionPage = new VehicleDetailsSectionPage(page)
    await hubPage.submit().click()
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).toHaveText(
      'The total cost of owning and running your Car is calculated to be £355.00. Is this correct?'
    )
    await grandCalculatedSummaryVehiclePage.submit().click()
    await expect(page).toHaveURL(new RegExp(gcsBreakdownBlockPage.pageName))
    await gcsBreakdownBlockPage.payOther().fill('120')
    await gcsBreakdownBlockPage.submit().click()
    await vehicleDetailsSectionPage.submit().click()
    await hubPage.submit().click()
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).toHaveText(
      'The total cost of owning and running your Van is calculated to be £250.00. Is this correct?'
    )
    await grandCalculatedSummaryVehiclePage.submit().click()
    await expect(page).toHaveURL(new RegExp(gcsBreakdownBlockPage.pageName))
    await gcsBreakdownBlockPage.payOther().fill('40')
    await gcsBreakdownBlockPage.submit().click()
    await vehicleDetailsSectionPage.submit().click()
  })

  test('Given I add an item to the costs lists, When I return to the Hub, Then I see both repeating sections revert to partially complete', async () => {
    const baseCostPaymentBreakdownPage = new BaseCostPaymentBreakdownPage(page)
    const baseCostsSectionPage = new BaseCostsSectionPage(page)
    const calculatedSummaryBaseCostPage = new CalculatedSummaryBaseCostPage(page)
    const costRepeatingBlock1RepeatingBlockPage = new CostRepeatingBlock1RepeatingBlockPage(page)
    const dynamicCostBlockPage = new DynamicCostBlockPage(page)
    const hubPage = new HubPage(page)
    const listCollectorCostAddPage = new ListCollectorCostAddPage(page)
    const listCollectorCostPage = new ListCollectorCostPage(page)
    await hubPage.summaryRowLink('base-costs-section').click()
    await baseCostsSectionPage.costsListAddLink().click()
    await listCollectorCostAddPage.costName().selectOption('Road Tax')
    await listCollectorCostAddPage.submit().click()
    await costRepeatingBlock1RepeatingBlockPage.repeatingBlock1CostBase().fill('30')
    await costRepeatingBlock1RepeatingBlockPage.submit().click()
    await listCollectorCostPage.no().click()
    await listCollectorCostPage.submit().click()
    await dynamicCostBlockPage.inputs().nth(1).fill('20')
    await dynamicCostBlockPage.submit().click()
    await expect(calculatedSummaryBaseCostPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the total base cost for any owned vehicle to be £180.00. Is this correct?'
    )
    await calculatedSummaryBaseCostPage.submit().click()
    await baseCostPaymentBreakdownPage.submit().click()
    await baseCostsSectionPage.submit().click()
    await expect(hubPage.summaryRowState('vehicle-details-section-1')).toHaveText('Partially completed')
    await expect(hubPage.summaryRowState('vehicle-details-section-2')).toHaveText('Partially completed')
  })

  test('Given I revisit both repeating sections with new items, When I start each, Then I see the grand calculated summary page with correct values and the breakdown after', async () => {
    const gcsBreakdownBlockPage = new GcsBreakdownBlockPage(page)
    const grandCalculatedSummaryVehiclePage = new GrandCalculatedSummaryVehiclePage(page)
    const hubPage = new HubPage(page)
    const vehicleDetailsSectionPage = new VehicleDetailsSectionPage(page)
    await hubPage.submit().click()
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).toHaveText(
      'The total cost of owning and running your Car is calculated to be £405.00. Is this correct?'
    )
    await grandCalculatedSummaryVehiclePage.submit().click()
    await gcsBreakdownBlockPage.payOther().fill('170')
    await gcsBreakdownBlockPage.submit().click()
    await vehicleDetailsSectionPage.submit().click()
    await hubPage.submit().click()
    await expect(grandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).toHaveText(
      'The total cost of owning and running your Van is calculated to be £300.00. Is this correct?'
    )
    await grandCalculatedSummaryVehiclePage.submit().click()
    await expect(page).toHaveURL(new RegExp(gcsBreakdownBlockPage.pageName))
  })
})
