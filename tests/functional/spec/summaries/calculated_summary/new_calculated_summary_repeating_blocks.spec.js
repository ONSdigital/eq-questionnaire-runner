import SectionOnePage from "../../../generated_pages/new_calculated_summary_repeating_blocks/section-1-summary.page.js";
import SectionTwoPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/section-2-summary.page.js";
import BlockCarPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/block-car.page.js";
import AddTransportPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/list-collector-add.page.js";
import RemoveTransportPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/list-collector-remove.page.js";
import TransportRepeatingBlock1Page from "../../../generated_pages/new_calculated_summary_repeating_blocks/transport-repeating-block-1-repeating-block.page.js";
import TransportRepeatingBlock2Page from "../../../generated_pages/new_calculated_summary_repeating_blocks/transport-repeating-block-2-repeating-block.page.js";
import ListCollectorPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/list-collector.page.js";
import CalculatedSummarySpendingPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/calculated-summary-spending.page.js";
import CalculatedSummaryCountPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/calculated-summary-count.page.js";
import HubPage from "../../../base_pages/hub.page";
import FamilyJourneysPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/family-journeys.page";
import BlockSkipPage from "../../../generated_pages/new_calculated_summary_repeating_blocks/block-skip.page";
import { assertSummaryValues, repeatingAnswerChangeLink, click, verifyUrlContains } from "../../../helpers";
import { expect } from "@wdio/globals";

describe("Feature: Calculated Summary using Repeating Blocks", () => {
  before("Reaching the first calculated summary", async () => {
    await browser.openQuestionnaire("test_new_calculated_summary_repeating_blocks.json");
    await $(BlockCarPage.car()).setValue(100);
    await click(BlockCarPage.submit());
    await $(BlockSkipPage.no()).click();
    await click(BlockSkipPage.submit());
    await $(ListCollectorPage.yes()).click();
    await click(ListCollectorPage.submit());
    await $(AddTransportPage.transportName()).selectByAttribute("value", "Bus");
    await click(AddTransportPage.submit());
    await $(TransportRepeatingBlock1Page.transportCompany()).setValue("First");
    await $(TransportRepeatingBlock1Page.transportCost()).setValue(30);
    await $(TransportRepeatingBlock1Page.transportAdditionalCost()).setValue(5);
    await click(TransportRepeatingBlock1Page.submit());
    await $(TransportRepeatingBlock2Page.transportCount()).setValue(10);
    await click(TransportRepeatingBlock2Page.submit());
    await $(ListCollectorPage.yes()).click();
    await click(ListCollectorPage.submit());
    await $(AddTransportPage.transportName()).selectByAttribute("value", "Plane");
    await click(AddTransportPage.submit());
    await $(TransportRepeatingBlock1Page.transportCompany()).setValue("EasyJet");
    await $(TransportRepeatingBlock1Page.transportCost()).setValue(0);
    await $(TransportRepeatingBlock1Page.transportAdditionalCost()).setValue(265);
    await click(TransportRepeatingBlock1Page.submit());
    await $(TransportRepeatingBlock2Page.transportCount()).setValue(2);
    await click(TransportRepeatingBlock2Page.submit());
    await $(ListCollectorPage.no()).click();
    await click(ListCollectorPage.submit());
  });

  it("Given I have a calculated summary using both list repeating block and static answers, When I reach the calculated summary page, Then I see the correct items and total.", async () => {
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).toContain(
      "We calculate the total monthly expenditure on transport to be £400.00. Is this correct?",
    );
    await assertSummaryValues(["£100.00", "£30.00", "£5.00", "£0.00", "£265.00", "£400.00"]);
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).toContain("Monthly expenditure travelling by car");
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).toContain("Monthly season ticket expenditure for travel by Bus");
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).toContain("Additional monthly expenditure for travel by Bus");
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).toContain("Monthly season ticket expenditure for travel by Plane");
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).toContain("Additional monthly expenditure for travel by Plane");
    await click(CalculatedSummarySpendingPage.submit());
  });

  it("Given I have a calculated summary using a single answer from a repeating block, When I reach the calculated summary page, Then I see the correct items and total", async () => {
    await expect(await $(CalculatedSummaryCountPage.calculatedSummaryTitle()).getText()).toContain(
      "We calculate the total journeys made per month to be 12. Is this correct?",
    );
    await assertSummaryValues(["10", "2", "12"]);
    await expect(await $(CalculatedSummaryCountPage.summaryItems()).getText()).toContain("Monthly journeys by Bus");
    await expect(await $(CalculatedSummaryCountPage.summaryItems()).getText()).toContain("Monthly journeys by Plane");
    await click(CalculatedSummaryCountPage.submit());
  });

  it("Given I add a new item to the list, When I complete the repeating blocks and press continue, Then I see the first calculated summary page which the updated total", async () => {
    await $(SectionOnePage.transportListAddLink()).click();
    await $(AddTransportPage.transportName()).selectByAttribute("value", "Train");
    await click(AddTransportPage.submit());
    await $(TransportRepeatingBlock1Page.transportCompany()).setValue("Great Western Railway");
    await $(TransportRepeatingBlock1Page.transportCost()).setValue(100);
    await $(TransportRepeatingBlock1Page.transportAdditionalCost()).setValue(50);
    await click(TransportRepeatingBlock1Page.submit());
    await $(TransportRepeatingBlock2Page.transportCount()).setValue(6);
    await click(TransportRepeatingBlock2Page.submit());
    await $(ListCollectorPage.no()).click();
    await click(ListCollectorPage.submit());
    await verifyUrlContains(CalculatedSummarySpendingPage.pageName);
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).toContain(
      "We calculate the total monthly expenditure on transport to be £550.00. Is this correct?",
    );
    await assertSummaryValues(["£100.00", "£30.00", "£5.00", "£0.00", "£265.00", "£100.00", "£50.00", "£550.00"]);
  });

  it("Given I am on the first calculated summary, When I confirm the total, Then I see the second calculated summary with an updated total", async () => {
    await click(CalculatedSummarySpendingPage.submit());
    await verifyUrlContains(CalculatedSummaryCountPage.pageName);
    await expect(await $(CalculatedSummaryCountPage.calculatedSummaryTitle()).getText()).toContain(
      "We calculate the total journeys made per month to be 18. Is this correct?",
    );
    await assertSummaryValues(["10", "2", "6", "18"]);
    await $(CalculatedSummaryCountPage.previous()).click();
  });

  it("Given I am on the first calculated summary, When I use one of the change links, Then I see the correct repeating block", async () => {
    await repeatingAnswerChangeLink(1).click();
    await verifyUrlContains(TransportRepeatingBlock1Page.pageName);
  });

  it("Given I have used a change link on a calculated summary to go back to the first repeating block, When I press continue, Then I see the calculated summary I came from", async () => {
    await click(TransportRepeatingBlock1Page.submit());
    await verifyUrlContains(CalculatedSummarySpendingPage.pageName);
  });

  it("Given I am on a calculated summary with change links for repeating blocks, When I use a change link and click previous, Then I see the calculated summary I came from", async () => {
    await repeatingAnswerChangeLink(1).click();
    await $(TransportRepeatingBlock1Page.previous()).click();
    await verifyUrlContains(CalculatedSummarySpendingPage.pageName);
  });

  it("Given I use a repeating block change link on the first calculated summary, When I edit my answer and press continue, Then I see the first calculated summary with a new correct total", async () => {
    await repeatingAnswerChangeLink(1).click();
    await $(TransportRepeatingBlock1Page.transportCost()).setValue(60);
    await click(TransportRepeatingBlock1Page.submit());
    await verifyUrlContains(CalculatedSummarySpendingPage.pageName);
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).toContain(
      "We calculate the total monthly expenditure on transport to be £580.00. Is this correct?",
    );
    await assertSummaryValues(["£100.00", "£60.00", "£5.00", "£0.00", "£265.00", "£100.00", "£50.00", "£580.00"]);
    await click(CalculatedSummarySpendingPage.submit());
  });

  it("Given I use a repeating block change link on the second calculated summary, When I edit my answer and press continue, Then I see the second calculated summary with a new correct total", async () => {
    await repeatingAnswerChangeLink(2).click();
    await $(TransportRepeatingBlock2Page.transportCount()).setValue(12);
    await click(TransportRepeatingBlock2Page.submit());
    await verifyUrlContains(CalculatedSummaryCountPage.pageName);
    await expect(await $(CalculatedSummaryCountPage.calculatedSummaryTitle()).getText()).toContain(
      "We calculate the total journeys made per month to be 24. Is this correct?",
    );
    await assertSummaryValues(["10", "2", "12", "24"]);
    await click(CalculatedSummaryCountPage.submit());
  });

  it("Given I use a remove link for on the summary page, When I press yes to confirm deleting the item, Then I see see the first calculated summary where I'm asked to reconfirm the total", async () => {
    await $(SectionOnePage.transportListRemoveLink(1)).click();
    await $(RemoveTransportPage.yes()).click();
    await click(RemoveTransportPage.submit());
    await verifyUrlContains(CalculatedSummarySpendingPage.pageName);
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).toContain(
      "We calculate the total monthly expenditure on transport to be £515.00. Is this correct?",
    );
    await assertSummaryValues(["£100.00", "£0.00", "£265.00", "£100.00", "£50.00", "£515.00"]);
  });

  it("Given I have confirmed the first updated total, When I press continue, Then I see the next calculated summary to confirm that total too", async () => {
    await click(CalculatedSummarySpendingPage.submit());
    await verifyUrlContains(CalculatedSummaryCountPage.pageName);
    await expect(await $(CalculatedSummaryCountPage.calculatedSummaryTitle()).getText()).toContain(
      "We calculate the total journeys made per month to be 14. Is this correct?",
    );
    await assertSummaryValues(["2", "12", "14"]);
  });

  it("Given I have a second section, When I begin and answer the first question with a total higher than the calculated summary, Then I see an error message preventing me from continuing", async () => {
    await click(CalculatedSummaryCountPage.submit());
    await click(SectionOnePage.submit());
    await click(HubPage.submit());
    await expect(await $(FamilyJourneysPage.questionTitle()).getText()).toContain("How many of your 14 journeys are to visit family?");
    await $(FamilyJourneysPage.answer()).setValue(15);
    await click(FamilyJourneysPage.submit());
    await expect(await $(FamilyJourneysPage.singleErrorLink()).getText()).toContain("Enter an answer less than or equal to 14");
  });

  it("Given I enter a value below the calculated summary from section 1, When I press Continue, Then I see my answer displayed on the next page", async () => {
    await $(FamilyJourneysPage.answer()).setValue(10);
    await click(FamilyJourneysPage.submit());
    await expect(await $(SectionTwoPage.familyJourneysQuestion()).getText()).toContain("How many of your 14 journeys are to visit family?");
    await expect(await $(SectionTwoPage.familyJourneysAnswer()).getText()).toContain("10");
    await click(SectionTwoPage.submit());
  });

  it("Given I use the add list item link, When I add a new item and return to the Hub, Then I see the progress of section 2 has reverted to Partially Complete", async () => {
    await expect(await $(HubPage.summaryRowState("section-1")).getText()).toBe("Completed");
    await expect(await $(HubPage.summaryRowState("section-2")).getText()).toBe("Completed");
    await $(HubPage.summaryRowLink("section-1")).click();
    await $(SectionOnePage.transportListAddLink()).click();
    await $(AddTransportPage.transportName()).selectByAttribute("value", "Tube");
    await click(AddTransportPage.submit());
    await click(TransportRepeatingBlock1Page.submit());
    await $(TransportRepeatingBlock2Page.transportCount()).setValue(2);
    await click(TransportRepeatingBlock2Page.submit());
    await $(ListCollectorPage.no()).click();
    await click(ListCollectorPage.submit());
    await click(CalculatedSummarySpendingPage.submit());
    await click(CalculatedSummaryCountPage.submit());
    await browser.url(HubPage.url());
    await expect(await $(HubPage.summaryRowState("section-1")).getText()).toBe("Completed");
    await expect(await $(HubPage.summaryRowState("section-2")).getText()).toBe("Partially completed");
  });

  it("Given I complete section-2 again, When I remove a list item and return to the Hub, Then I see the progress of section 2 has reverted to Partially Complete", async () => {
    await click(HubPage.submit());
    await $(FamilyJourneysPage.answer()).setValue(16);
    await click(FamilyJourneysPage.submit());
    await click(SectionTwoPage.submit());
    await expect(await $(HubPage.summaryRowState("section-1")).getText()).toBe("Completed");
    await expect(await $(HubPage.summaryRowState("section-2")).getText()).toBe("Completed");
    await $(HubPage.summaryRowLink("section-1")).click();
    await $(SectionOnePage.transportListRemoveLink(3)).click();
    await $(RemoveTransportPage.yes()).click();
    await click(RemoveTransportPage.submit());
    await click(CalculatedSummarySpendingPage.submit());
    await click(CalculatedSummaryCountPage.submit());
    await click(SectionOnePage.submit());
    await expect(await $(HubPage.summaryRowState("section-1")).getText()).toBe("Completed");
    await expect(await $(HubPage.summaryRowState("section-2")).getText()).toBe("Partially completed");
  });

  it("Given I have a question which removes the list collector from the path, When I change my answer to the question removing the list collector and route backwards from the summary, Then I see the first calculated summary with an updated total", async () => {
    await $(HubPage.summaryRowLink("section-1")).click();
    await $(SectionOnePage.answerSkipEdit()).click();
    await $(BlockSkipPage.yes()).click();
    await click(BlockSkipPage.submit());
    // calculated summary progress is not altered by removing the list collector from the path so next location is summary page
    await verifyUrlContains(SectionOnePage.pageName);
    await $(SectionOnePage.previous()).click();
    // other calculated summary should not be on the path, so go straight back to the spending one which now has none of the list items
    await verifyUrlContains(CalculatedSummarySpendingPage.pageName);
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).toBe(
      "We calculate the total monthly expenditure on transport to be £100.00. Is this correct?",
    );
    await assertSummaryValues(["£100.00", "£100.00"]);
  });

  it("Given I confirm the calculated summary and finish the section, When I return to the Hub, Then I see that section 2 is no longer available", async () => {
    await click(CalculatedSummarySpendingPage.submit());
    await click(SectionOnePage.submit());
    await expect(await $$(HubPage.summaryItems()).length).toBe(1);
  });
});
