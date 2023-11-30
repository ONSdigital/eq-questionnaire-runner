import { assertSummaryValues, click, listItemIds } from "../../../helpers";
import { expect } from "@wdio/globals";
import AddVehiclePage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/list-collector-add.page.js";
import AnyCostPage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/any-cost.page.js";
import AnyVehiclePage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/any-vehicle.page.js";
import BaseCostsSectionPage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/base-costs-section-summary.page.js";
import CalculatedSummaryBaseCostPage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/calculated-summary-base-cost.page.js";
import CalculatedSummaryRunningCostPage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/calculated-summary-running-cost.page.js";
import GrandCalculatedSummaryVehiclePage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/grand-calculated-summary-vehicle.page.js";
import HubPage from "../../../base_pages/hub.page";
import ListCollectorPage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/list-collector.page.js";
import VehicleDetailsSectionPage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/vehicle-details-section-summary.page.js";
import VehicleFuelBlockPage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/vehicle-fuel-block.page.js";
import VehicleMaintenanceBlockPage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/vehicle-maintenance-block.page.js";
import VehiclesSectionPage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/vehicles-section-summary.page.js";
import FinanceCostPage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/finance-cost.page";
import BaseCostPaymentBreakdownPage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/base-cost-payment-breakdown.page";
import GcsBreakdownBlockPage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/gcs-breakdown-block.page";
import GcsPipingPage from "../../../generated_pages/grand_calculated_summary_inside_repeating_section/gcs-piping.page";

describe("Grand Calculated Summary inside a repeating section", () => {
  let vehicleListItemIds = [];
  before("Load the survey", async () => {
    await browser.openQuestionnaire("test_grand_calculated_summary_inside_repeating_section.json");
  });

  it("Given I have a Grand Calculated Summary inside a repeating section, When I reach it for the first list item, Then I see placeholder content rendered correctly", async () => {
    await click(HubPage.submit());
    await $(AnyCostPage.no()).click();
    await click(AnyCostPage.submit());
    await $(FinanceCostPage.answer()).setValue(90);
    await click(FinanceCostPage.submit());
    await expect(await $(CalculatedSummaryBaseCostPage.calculatedSummaryTitle()).getText()).toBe(
      "We calculate the total base cost for any owned vehicle to be £90.00. Is this correct?",
    );
    await click(CalculatedSummaryBaseCostPage.submit());
    await $(BaseCostPaymentBreakdownPage.baseCredit()).setValue(30);
    await $(BaseCostPaymentBreakdownPage.baseDebit()).setValue(40);
    await click(BaseCostPaymentBreakdownPage.submit());
    await click(BaseCostsSectionPage.submit());
    await click(HubPage.submit());
    await $(AnyVehiclePage.yes()).click();
    await click(AnyVehiclePage.submit());
    await $(AddVehiclePage.vehicleName()).selectByAttribute("value", "Car");
    await click(AddVehiclePage.submit());
    await $(ListCollectorPage.yes()).click();
    await click(ListCollectorPage.submit());
    await $(AddVehiclePage.vehicleName()).selectByAttribute("value", "Van");
    await click(AddVehiclePage.submit());
    vehicleListItemIds = await listItemIds();
    await $(ListCollectorPage.no()).click();
    await click(ListCollectorPage.submit());
    await click(VehiclesSectionPage.submit());
    await click(HubPage.submit());
    await $(VehicleMaintenanceBlockPage.vehicleMaintenanceCost()).setValue(100);
    await click(VehicleMaintenanceBlockPage.submit());
    await $(VehicleFuelBlockPage.vehicleFuelCost()).setValue(125);
    await click(VehicleFuelBlockPage.submit());
    await expect(await $(CalculatedSummaryRunningCostPage.calculatedSummaryTitle()).getText()).toBe(
      "We calculate the monthly running costs of your Car to be £225.00. Is this correct?",
    );
    await click(CalculatedSummaryRunningCostPage.submit());
    await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryVehiclePage.pageName);
    await expect(await $(GrandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).getText()).toBe(
      "The total cost of owning and running your Car is calculated to be £315.00. Is this correct?",
    );
    await expect(await $(GrandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostLabel()).getText()).toBe("Vehicle base cost");
    await expect(await $(GrandCalculatedSummaryVehiclePage.calculatedSummaryRunningCostLabel()).getText()).toBe("Monthly Car costs");
    await expect(await $(GrandCalculatedSummaryVehiclePage.grandCalculatedSummaryQuestion()).getText()).toBe("Grand total Car expenditure");
    await assertSummaryValues(["£90.00", "£225.00", "£315.00"]);
  });

  it("Given I immediately use that Grand Calculated Summary for validation, When I enter a sum of values too high, Then I see an error message", async () => {
    await click(GrandCalculatedSummaryVehiclePage.submit());
    await $(GcsBreakdownBlockPage.payDebit()).setValue(100);
    await $(GcsBreakdownBlockPage.payCredit()).setValue(115);
    await $(GcsBreakdownBlockPage.payOther()).setValue(200);
    await click(GcsBreakdownBlockPage.submit());
    await expect(await $(GcsBreakdownBlockPage.errorNumber()).getText()).toBe("Enter answers that add up to 315");
  });

  it("Given I enter a valid value for the Grand Calculated Summary breakdown, When I press continue, Then I see an Interstitial page with my values correctly piped in", async () => {
    await $(GcsBreakdownBlockPage.payOther()).setValue(100);
    await click(GcsBreakdownBlockPage.submit());
    await expect(browser).toHaveUrlContaining(GcsPipingPage.pageName);
    await expect(await $("body").getText()).toContain("Monthly maintenance cost: £100.00");
    await expect(await $("body").getText()).toContain("Monthly fuel cost: £125.00");
    await expect(await $("body").getText()).toContain("Total base cost: £90.00");
    await expect(await $("body").getText()).toContain("Total running cost: £225.00");
    await expect(await $("body").getText()).toContain("Total owning and running cost: £315.00");
    await expect(await $("body").getText()).toContain("Paid by debit card: £100.00");
    await expect(await $("body").getText()).toContain("Paid by credit card: £115.00");
    await expect(await $("body").getText()).toContain("Paid by other means: £100.00");
  });

  it("Given I have a Grand Calculated Summary inside a repeating section, When I reach it for the second list item, Then I see placeholder content rendered correctly", async () => {
    await click(GcsPipingPage.submit());
    await click(VehicleDetailsSectionPage.submit());
    await click(HubPage.submit());
    await $(VehicleMaintenanceBlockPage.vehicleMaintenanceCost()).setValue(50);
    await click(VehicleMaintenanceBlockPage.submit());
    await $(VehicleFuelBlockPage.vehicleFuelCost()).setValue(45);
    await click(VehicleFuelBlockPage.submit());
    await expect(await $(CalculatedSummaryRunningCostPage.calculatedSummaryTitle()).getText()).toBe(
      "We calculate the monthly running costs of your Van to be £95.00. Is this correct?",
    );
    await click(CalculatedSummaryRunningCostPage.submit());
    await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryVehiclePage.pageName);
    await expect(await $(GrandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).getText()).toBe(
      "The total cost of owning and running your Van is calculated to be £185.00. Is this correct?",
    );
    await expect(await $(GrandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostLabel()).getText()).toBe("Vehicle base cost");
    await expect(await $(GrandCalculatedSummaryVehiclePage.calculatedSummaryRunningCostLabel()).getText()).toBe("Monthly Van costs");
    await expect(await $(GrandCalculatedSummaryVehiclePage.grandCalculatedSummaryQuestion()).getText()).toBe("Grand total Van expenditure");
    await assertSummaryValues(["£90.00", "£95.00", "£185.00"]);
  });

  it("Given I am at a Grand Summary inside a repeating section, When I click the change link for a repeating calculated summary, Then I am taken to the correct page", async () => {
    await expect(browser).toHaveUrlContaining(`vehicles/${vehicleListItemIds[1]}/`);
    await $(GrandCalculatedSummaryVehiclePage.calculatedSummaryRunningCostEdit()).click();
    await expect(browser).toHaveUrlContaining(CalculatedSummaryRunningCostPage.pageName);
    await expect(browser).toHaveUrlContaining(`vehicles/${vehicleListItemIds[1]}/`);
  });

  it("Given I have used a change link for a repeating calculated summary, When I click the continue button, Then I am taken to the Grand Calculated Summary", async () => {
    await click(CalculatedSummaryRunningCostPage.submit());
    await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryVehiclePage.pageName);
    await expect(browser).toHaveUrlContaining(`vehicles/${vehicleListItemIds[1]}/`);
  });

  it("Given I am at a Grand Summary inside a repeating section, When I click the change link for a non repeating calculated summary, Then I am taken to the correct page", async () => {
    await $(GrandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostEdit()).click();
    await expect(browser).toHaveUrlContaining(CalculatedSummaryBaseCostPage.pageName);
  });

  it("Given I have used a change link for a non repeating calculated summary from a repeating section, When I click the continue button, Then I am taken to the Grand Calculated Summary for the correct list item", async () => {
    await click(CalculatedSummaryBaseCostPage.submit());
    await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryVehiclePage.pageName);
    await expect(browser).toHaveUrlContaining(`vehicles/${vehicleListItemIds[1]}/`);
  });

  it("Given I use a change link for a repeating calculated summary, When I use a change link there, Then pressing continue twice takes me back to the correct grand calculated summary", async () => {
    await $(GrandCalculatedSummaryVehiclePage.calculatedSummaryRunningCostEdit()).click();
    await $(CalculatedSummaryRunningCostPage.vehicleMaintenanceCostEdit()).click();
    await expect(browser).toHaveUrlContaining(VehicleMaintenanceBlockPage.pageName);
    await expect(browser).toHaveUrlContaining(`vehicles/${vehicleListItemIds[1]}/`);
    await click(VehicleMaintenanceBlockPage.submit());
    await expect(browser).toHaveUrlContaining(CalculatedSummaryRunningCostPage.pageName);
    await expect(browser).toHaveUrlContaining(`vehicles/${vehicleListItemIds[1]}/`);
    await click(CalculatedSummaryRunningCostPage.submit());
    await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryVehiclePage.pageName);
    await expect(browser).toHaveUrlContaining(`vehicles/${vehicleListItemIds[1]}/`);
  });

  it("Given I use a change link for a non repeating calculated summary, When I use a change link there, Then pressing continue twice takes me back to the correct grand calculated summary", async () => {
    await $(GrandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostEdit()).click();
    await $(CalculatedSummaryBaseCostPage.financeCostAnswerEdit()).click();
    await expect(browser).toHaveUrlContaining(FinanceCostPage.pageName);
    await expect(browser).toHaveUrlContaining(`return_to_list_item_id=${vehicleListItemIds[1]}`);
    await click(FinanceCostPage.submit());
    await expect(browser).toHaveUrlContaining(CalculatedSummaryBaseCostPage.pageName);
    await expect(browser).toHaveUrlContaining(`return_to_list_item_id=${vehicleListItemIds[1]}`);
    await click(CalculatedSummaryBaseCostPage.submit());
    await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryVehiclePage.pageName);
    await expect(browser).toHaveUrlContaining(`vehicles/${vehicleListItemIds[1]}/`);
  });

  it("Given I change a non repeating answer which results in the section being incomplete, When I press continue, Then I go to the next incomplete location with the list item id preserved", async () => {
    await $(GrandCalculatedSummaryVehiclePage.calculatedSummaryBaseCostEdit()).click();
    await $(CalculatedSummaryBaseCostPage.financeCostAnswerEdit()).click();
    await $(FinanceCostPage.answer()).setValue(100);
    await click(FinanceCostPage.submit());
    await expect(browser).toHaveUrlContaining(CalculatedSummaryBaseCostPage.pageName);
    await expect(await $(CalculatedSummaryBaseCostPage.calculatedSummaryTitle()).getText()).toBe(
      "We calculate the total base cost for any owned vehicle to be £100.00. Is this correct?",
    );
    await click(CalculatedSummaryBaseCostPage.submit());
    await expect(browser).toHaveUrlContaining(BaseCostPaymentBreakdownPage.pageName);
    await expect(browser).toHaveUrlContaining(`return_to_list_item_id=${vehicleListItemIds[1]}`);
  });

  it("Given I have changed a non repeating answer, When I return to the Grand Calculated Summary, Then I see the correctly updated values", async () => {
    await click(BaseCostPaymentBreakdownPage.submit());

    await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryVehiclePage.pageName);
    await expect(await $(GrandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).getText()).toBe(
      "The total cost of owning and running your Van is calculated to be £195.00. Is this correct?",
    );
  });

  it("Given I change a repeating answer, When I return to the Grand Calculated Summary, Then I see the correctly updated values", async () => {
    await $(GrandCalculatedSummaryVehiclePage.calculatedSummaryRunningCostEdit()).click();
    await $(CalculatedSummaryRunningCostPage.vehicleMaintenanceCostEdit()).click();
    await $(VehicleMaintenanceBlockPage.vehicleMaintenanceCost()).setValue(75);
    await click(VehicleMaintenanceBlockPage.submit());
    await expect(browser).toHaveUrlContaining(CalculatedSummaryRunningCostPage.pageName);
    await expect(await $(CalculatedSummaryRunningCostPage.calculatedSummaryTitle()).getText()).toBe(
      "We calculate the monthly running costs of your Van to be £120.00. Is this correct?",
    );
    await click(CalculatedSummaryRunningCostPage.submit());
    await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryVehiclePage.pageName);
    await expect(await $(GrandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).getText()).toBe(
      "The total cost of owning and running your Van is calculated to be £220.00. Is this correct?",
    );
  });

  it("Given I edit the non-repeating calculated summary, When I return to the Hub, Then I see repeating sections are incomplete", async () => {
    await click(GrandCalculatedSummaryVehiclePage.submit());
    await $(GcsBreakdownBlockPage.payDebit()).setValue(100);
    await $(GcsBreakdownBlockPage.payCredit()).setValue(110);
    await $(GcsBreakdownBlockPage.payOther()).setValue(10);
    await click(GcsBreakdownBlockPage.submit());
    await click(GcsPipingPage.submit());
    await click(VehicleDetailsSectionPage.submit());
    await $(HubPage.summaryRowLink("vehicle-details-section-1")).click();
    await click(GrandCalculatedSummaryVehiclePage.submit());
    await click(VehicleDetailsSectionPage.submit());
    await expect(await $(HubPage.summaryRowState("vehicle-details-section-1")).getText()).toBe("Completed");
    await expect(await $(HubPage.summaryRowState("vehicle-details-section-2")).getText()).toBe("Completed");
    await $(HubPage.summaryRowLink("base-costs-section")).click();
    await $(BaseCostsSectionPage.financeCostAnswerEdit()).click();
    await $(FinanceCostPage.answer()).setValue(110);
    await click(FinanceCostPage.submit());
    await click(CalculatedSummaryBaseCostPage.submit());
    await click(BaseCostPaymentBreakdownPage.submit());
    await click(BaseCostsSectionPage.submit());
    await expect(await $(HubPage.summaryRowState("vehicle-details-section-1")).getText()).toBe("Partially completed");
    await expect(await $(HubPage.summaryRowState("vehicle-details-section-2")).getText()).toBe("Partially completed");
  });

  it("Given I have two partially complete repeating sections, When I press continue, Then I am taken straight to the grand calculated summary as it is the first incomplete block", async () => {
    await click(HubPage.submit());
    await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryVehiclePage.pageName);
    await expect(browser).toHaveUrlContaining(`vehicles/${vehicleListItemIds[0]}/`);
    await expect(await $(GrandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).getText()).toBe(
      "The total cost of owning and running your Car is calculated to be £335.00. Is this correct?",
    );
    await click(GrandCalculatedSummaryVehiclePage.submit());
    await click(VehicleDetailsSectionPage.submit());
  });

  it("Given I've completed the first repeating section, When I press continue, I am taken straight to the grand calculated summary of the second repeat", async () => {
    await click(HubPage.submit());
    await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryVehiclePage.pageName);
    await expect(browser).toHaveUrlContaining(`vehicles/${vehicleListItemIds[1]}/`);
    await expect(await $(GrandCalculatedSummaryVehiclePage.grandCalculatedSummaryTitle()).getText()).toBe(
      "The total cost of owning and running your Van is calculated to be £230.00. Is this correct?",
    );
  });
});
