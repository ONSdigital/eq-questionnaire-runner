import SectionPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/section-summary.page.js";
import BlockCarPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/block-car.page.js";
import AddTransportPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/list-collector-add.page.js";
import RemoveTransportPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/list-collector-remove.page.js";
import TransportRepeatingBlock1Page from "../../../generated_pages/new_calculated_summary_repeating_blocks/transport-repeating-block-1-repeating-block.page.js";
import TransportRepeatingBlock2Page from "../../../generated_pages/new_calculated_summary_repeating_blocks/transport-repeating-block-2-repeating-block.page.js";
import ListCollectorPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/list-collector.page.js";
import CalculatedSummarySpendingPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/calculated-summary-spending.page.js";
import CalculatedSummaryCountPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/calculated-summary-count.page.js";
import { assertSummaryValues } from "../../../helpers";

describe("Feature: Calculated Summary using Repeating Blocks", () => {
  const summaryActions = 'dd[class="ons-summary__actions"]';
  const repeatingAnswerChangeLink = (answerIndex) => $$(summaryActions)[answerIndex].$("a");

  before("Reaching the first calculated summary", async () => {
    await browser.openQuestionnaire("test_new_calculated_summary_repeating_blocks.json");
    await $(BlockCarPage.car()).setValue(100);
    await $(BlockCarPage.submit()).click();
    await $(ListCollectorPage.yes()).click();
    await $(ListCollectorPage.submit()).click();
    await $(AddTransportPage.transportName()).selectByAttribute("value", "Bus");
    await $(AddTransportPage.submit()).click();
    await $(TransportRepeatingBlock1Page.transportCompany()).setValue("First");
    await $(TransportRepeatingBlock1Page.transportCost()).setValue(30);
    await $(TransportRepeatingBlock1Page.transportAdditionalCost()).setValue(5);
    await $(TransportRepeatingBlock1Page.submit()).click();
    await $(TransportRepeatingBlock2Page.transportCount()).setValue(10);
    await $(TransportRepeatingBlock2Page.submit()).click();
    await $(ListCollectorPage.yes()).click();
    await $(ListCollectorPage.submit()).click();
    await $(AddTransportPage.transportName()).selectByAttribute("value", "Plane");
    await $(AddTransportPage.submit()).click();
    await $(TransportRepeatingBlock1Page.transportCompany()).setValue("EasyJet");
    await $(TransportRepeatingBlock1Page.transportCost()).setValue(0);
    await $(TransportRepeatingBlock1Page.transportAdditionalCost()).setValue(265);
    await $(TransportRepeatingBlock1Page.submit()).click();
    await $(TransportRepeatingBlock2Page.transportCount()).setValue(2);
    await $(TransportRepeatingBlock2Page.submit()).click();
    await $(ListCollectorPage.no()).click();
    await $(ListCollectorPage.submit()).click();
  });

  it("Given I have a calculated summary using some answers from a repeating block and static answers, I see the correct items and total.", async () => {
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total monthly expenditure on transport to be £400.00. Is this correct?"
    );
    await assertSummaryValues(["£100.00", "£30.00", "£5.00", "£0.00", "£265.00"]);
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).to.contain("Monthly expenditure travelling by car");
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).to.contain("Monthly season ticket expenditure for travel by Bus");
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).to.contain("Additional monthly expenditure for travel by Bus");
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).to.contain("Monthly season ticket expenditure for travel by Plane");
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).to.contain("Additional monthly expenditure for travel by Plane");
    await $(CalculatedSummarySpendingPage.submit()).click();
  });

  it("Given I have a calculated summary using a single answer from a repeating block, I see the correct items and total", async () => {
    await expect(await $(CalculatedSummaryCountPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total journeys made per month to be 12. Is this correct?"
    );
    await assertSummaryValues(["10", "2"]);
    await expect(await $(CalculatedSummaryCountPage.summaryItems()).getText()).to.contain("Monthly journeys by Bus");
    await expect(await $(CalculatedSummaryCountPage.summaryItems()).getText()).to.contain("Monthly journeys by Plane");
    await $(CalculatedSummaryCountPage.submit()).click();
  });

  it("Given I add a new item to the list and complete the repeating blocks, I am taken to each calculated summary in turn to confirm the new total", async () => {
    await $(SectionPage.transportListAddLink()).click();
    await $(AddTransportPage.transportName()).selectByAttribute("value", "Train");
    await $(AddTransportPage.submit()).click();
    await $(TransportRepeatingBlock1Page.transportCompany()).setValue("Great Western Railway");
    await $(TransportRepeatingBlock1Page.transportCost()).setValue(100);
    await $(TransportRepeatingBlock1Page.transportAdditionalCost()).setValue(50);
    await $(TransportRepeatingBlock1Page.submit()).click();
    await $(TransportRepeatingBlock2Page.transportCount()).setValue(6);
    await $(TransportRepeatingBlock2Page.submit()).click();
    await $(ListCollectorPage.no()).click();
    await $(ListCollectorPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummarySpendingPage.pageName);
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total monthly expenditure on transport to be £550.00. Is this correct?"
    );
    await assertSummaryValues(["£100.00", "£30.00", "£5.00", "£0.00", "£265.00", "£100.00", "£50.00"]);
    await $(CalculatedSummarySpendingPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummaryCountPage.pageName);
    await expect(await $(CalculatedSummaryCountPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total journeys made per month to be 18. Is this correct?"
    );
    await assertSummaryValues(["10", "2", "6"]);
  });

  it("Given I use a change link on the first calculated summary, I am taken to the correct repeating block, and the continue button takes me back to the calculated summary", async () => {
    await $(CalculatedSummaryCountPage.previous()).click();
    await repeatingAnswerChangeLink(1).click();
    await expect(await browser.getUrl()).to.contain(TransportRepeatingBlock1Page.pageName);
    await $(TransportRepeatingBlock1Page.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummarySpendingPage.pageName);
  });

  it("Given I use a change link on the first calculated summary, the previous button takes me back to the calculated summary", async () => {
    await repeatingAnswerChangeLink(1).click();
    await $(TransportRepeatingBlock1Page.previous()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummarySpendingPage.pageName);
  });

  it("Given I edit one of my answers, I am taken back to the calculated summary and the new total is correct", async () => {
    await repeatingAnswerChangeLink(1).click();
    await $(TransportRepeatingBlock1Page.transportCost()).setValue(60);
    await $(TransportRepeatingBlock1Page.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummarySpendingPage.pageName);
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total monthly expenditure on transport to be £580.00. Is this correct?"
    );
    await assertSummaryValues(["£100.00", "£60.00", "£5.00", "£0.00", "£265.00", "£100.00", "£50.00"]);
    await $(CalculatedSummarySpendingPage.submit()).click();
  });

  it("Given I edit an answer for the second calculated summary, I am taken back to the second calculated summary and the new total is correct", async () => {
    await repeatingAnswerChangeLink(2).click();
    await $(TransportRepeatingBlock2Page.transportCount()).setValue(12);
    await $(TransportRepeatingBlock2Page.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummaryCountPage.pageName);
    await expect(await $(CalculatedSummaryCountPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total journeys made per month to be 24. Is this correct?"
    );
    await assertSummaryValues(["10", "2", "12"]);
    await $(CalculatedSummaryCountPage.submit()).click();
  });

  it("Given I remove one of the list items, I am taken back to each calculated summary in turn to confirm the new totals", async () => {
    await $(SectionPage.transportListRemoveLink(1)).click();
    await $(RemoveTransportPage.yes()).click();
    await $(RemoveTransportPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummarySpendingPage.pageName);
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total monthly expenditure on transport to be £515.00. Is this correct?"
    );
    await assertSummaryValues(["£100.00", "£0.00", "£265.00", "£100.00", "£50.00"]);
    await $(CalculatedSummarySpendingPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummaryCountPage.pageName);
    await expect(await $(CalculatedSummaryCountPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total journeys made per month to be 14. Is this correct?"
    );
    await assertSummaryValues(["2", "12"]);
  });
});
