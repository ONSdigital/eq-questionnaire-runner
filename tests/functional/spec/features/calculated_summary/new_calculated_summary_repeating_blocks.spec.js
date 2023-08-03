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
import { assertSummaryValues, repeatingAnswerChangeLink } from "../../../helpers";

describe("Feature: Calculated Summary using Repeating Blocks", () => {
  before("Reaching the first calculated summary", async () => {
    await browser.openQuestionnaire("test_new_calculated_summary_repeating_blocks.json");
    await $(BlockCarPage.car()).setValue(100);
    await $(BlockCarPage.submit()).click();
    await $(BlockSkipPage.no()).click();
    await $(BlockSkipPage.submit()).click();
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

  it("Given I have a calculated summary using both list repeating block and static answers, When I reach the calculated summary page, Then I see the correct items and total.", async () => {
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total monthly expenditure on transport to be £400.00. Is this correct?",
    );
    await assertSummaryValues(["£100.00", "£30.00", "£5.00", "£0.00", "£265.00"]);
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).to.contain("Monthly expenditure travelling by car");
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).to.contain("Monthly season ticket expenditure for travel by Bus");
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).to.contain("Additional monthly expenditure for travel by Bus");
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).to.contain("Monthly season ticket expenditure for travel by Plane");
    await expect(await $(CalculatedSummarySpendingPage.summaryItems()).getText()).to.contain("Additional monthly expenditure for travel by Plane");
    await $(CalculatedSummarySpendingPage.submit()).click();
  });

  it("Given I have a calculated summary using a single answer from a repeating block, When I reach the calculated summary page, Then I see the correct items and total", async () => {
    await expect(await $(CalculatedSummaryCountPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total journeys made per month to be 12. Is this correct?",
    );
    await assertSummaryValues(["10", "2"]);
    await expect(await $(CalculatedSummaryCountPage.summaryItems()).getText()).to.contain("Monthly journeys by Bus");
    await expect(await $(CalculatedSummaryCountPage.summaryItems()).getText()).to.contain("Monthly journeys by Plane");
    await $(CalculatedSummaryCountPage.submit()).click();
  });

  it("Given I add a new item to the list, When I complete the repeating blocks and press continue, Then I see the first calculated summary page which the updated total", async () => {
    await $(SectionOnePage.transportListAddLink()).click();
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
      "We calculate the total monthly expenditure on transport to be £550.00. Is this correct?",
    );
    await assertSummaryValues(["£100.00", "£30.00", "£5.00", "£0.00", "£265.00", "£100.00", "£50.00"]);
  });

  it("Given I am on the first calculated summary, When I confirm the total, Then I see the second calculated summary with an updated total", async () => {
    await $(CalculatedSummarySpendingPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummaryCountPage.pageName);
    await expect(await $(CalculatedSummaryCountPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total journeys made per month to be 18. Is this correct?",
    );
    await assertSummaryValues(["10", "2", "6"]);
    await $(CalculatedSummaryCountPage.previous()).click();
  });

  it("Given I am on the first calculated summary, When I use one of the change links, Then I see the correct repeating block", async () => {
    await repeatingAnswerChangeLink(1).click();
    await expect(await browser.getUrl()).to.contain(TransportRepeatingBlock1Page.pageName);
  });

  it("Given I have used a change link on a calculated summary to go back to the first repeating block, When I press continue, Then I see the calculated summary I came from", async () => {
    await $(TransportRepeatingBlock1Page.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummarySpendingPage.pageName);
  });

  it("Given I am on a calculated summary with change links for repeating blocks, When I use a change link and click previous, Then I see the calculated summary I came from", async () => {
    await repeatingAnswerChangeLink(1).click();
    await $(TransportRepeatingBlock1Page.previous()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummarySpendingPage.pageName);
  });

  it("Given I use a repeating block change link on the first calculated summary, When I edit my answer and press continue, Then I see the first calculated summary with a new correct total", async () => {
    await repeatingAnswerChangeLink(1).click();
    await $(TransportRepeatingBlock1Page.transportCost()).setValue(60);
    await $(TransportRepeatingBlock1Page.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummarySpendingPage.pageName);
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total monthly expenditure on transport to be £580.00. Is this correct?",
    );
    await assertSummaryValues(["£100.00", "£60.00", "£5.00", "£0.00", "£265.00", "£100.00", "£50.00"]);
    await $(CalculatedSummarySpendingPage.submit()).click();
  });

  it("Given I use a repeating block change link on the second calculated summary, When I edit my answer and press continue, Then I see the second calculated summary with a new correct total", async () => {
    await repeatingAnswerChangeLink(2).click();
    await $(TransportRepeatingBlock2Page.transportCount()).setValue(12);
    await $(TransportRepeatingBlock2Page.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummaryCountPage.pageName);
    await expect(await $(CalculatedSummaryCountPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total journeys made per month to be 24. Is this correct?",
    );
    await assertSummaryValues(["10", "2", "12"]);
    await $(CalculatedSummaryCountPage.submit()).click();
  });

  it("Given I use a remove link for on the summary page, When I press yes to confirm deleting the item, Then I see see the first calculated summary where I'm asked to reconfirm the total", async () => {
    await $(SectionOnePage.transportListRemoveLink(1)).click();
    await $(RemoveTransportPage.yes()).click();
    await $(RemoveTransportPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummarySpendingPage.pageName);
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total monthly expenditure on transport to be £515.00. Is this correct?",
    );
    await assertSummaryValues(["£100.00", "£0.00", "£265.00", "£100.00", "£50.00"]);
  });

  it("Given I have confirmed the first updated total, When I press continue, Then I see the next calculated summary to confirm that total too", async () => {
    await $(CalculatedSummarySpendingPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummaryCountPage.pageName);
    await expect(await $(CalculatedSummaryCountPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total journeys made per month to be 14. Is this correct?",
    );
    await assertSummaryValues(["2", "12"]);
  });

  it("Given I have a second section, When I begin and answer the first question with a total higher than the calculated summary, Then I see an error message preventing me from continuing", async () => {
    await $(CalculatedSummaryCountPage.submit()).click();
    await $(SectionOnePage.submit()).click();
    await $(HubPage.submit()).click();
    await expect(await $(FamilyJourneysPage.questionTitle()).getText()).to.contain("How many of your 14 journeys are to visit family?");
    await $(FamilyJourneysPage.answer()).setValue(15);
    await $(FamilyJourneysPage.submit()).click();
    await expect(await $(FamilyJourneysPage.singleErrorLink()).getText()).to.contain("Enter an answer less than or equal to 14");
  });

  it("Given I enter a value below the calculated summary from section 1, When I press Continue, Then I see my answer displayed on the next page", async () => {
    await $(FamilyJourneysPage.answer()).setValue(10);
    await $(FamilyJourneysPage.submit()).click();
    await expect(await $(SectionTwoPage.familyJourneysQuestion()).getText()).to.contain("How many of your 14 journeys are to visit family?");
    await expect(await $(SectionTwoPage.familyJourneysAnswer()).getText()).to.contain("10");
    await $(SectionTwoPage.submit()).click();
  });

  it("Given I use the add list item link, When I add a new item and return to the Hub, Then I see the progress of section 2 has reverted to Partially Complete", async () => {
    await expect(await $(HubPage.summaryRowState("section-1")).getText()).to.equal("Completed");
    await expect(await $(HubPage.summaryRowState("section-2")).getText()).to.equal("Completed");
    await $(HubPage.summaryRowLink("section-1")).click();
    await $(SectionOnePage.transportListAddLink()).click();
    await $(AddTransportPage.transportName()).selectByAttribute("value", "Tube");
    await $(AddTransportPage.submit()).click();
    await $(TransportRepeatingBlock1Page.submit()).click();
    await $(TransportRepeatingBlock2Page.transportCount()).setValue(2);
    await $(TransportRepeatingBlock2Page.submit()).click();
    await $(ListCollectorPage.no()).click();
    await $(ListCollectorPage.submit()).click();
    await $(CalculatedSummarySpendingPage.submit()).click();
    await $(CalculatedSummaryCountPage.submit()).click();
    await browser.url(HubPage.url());
    await expect(await $(HubPage.summaryRowState("section-1")).getText()).to.equal("Completed");
    await expect(await $(HubPage.summaryRowState("section-2")).getText()).to.equal("Partially completed");
  });

  it("Given I complete section-2 again, When I remove a list item and return to the Hub, Then I see the progress of section 2 has reverted to Partially Complete", async () => {
    await $(HubPage.submit()).click();
    await $(FamilyJourneysPage.answer()).setValue(16);
    await $(FamilyJourneysPage.submit()).click();
    await $(SectionTwoPage.submit()).click();
    await expect(await $(HubPage.summaryRowState("section-1")).getText()).to.equal("Completed");
    await expect(await $(HubPage.summaryRowState("section-2")).getText()).to.equal("Completed");
    await $(HubPage.summaryRowLink("section-1")).click();
    await $(SectionOnePage.transportListRemoveLink(3)).click();
    await $(RemoveTransportPage.yes()).click();
    await $(RemoveTransportPage.submit()).click();
    await $(CalculatedSummarySpendingPage.submit()).click();
    await $(CalculatedSummaryCountPage.submit()).click();
    await $(SectionOnePage.submit()).click();
    await expect(await $(HubPage.summaryRowState("section-1")).getText()).to.equal("Completed");
    await expect(await $(HubPage.summaryRowState("section-2")).getText()).to.equal("Partially completed");
  });

  it("Given I have a question which removes the list collector from the path, When I change my answer to the question removing the list collector and route backwards from the summary, Then I see the first calculated summary with an updated total", async () => {
    await $(HubPage.summaryRowLink("section-1")).click();
    await $(SectionOnePage.answerSkipEdit()).click();
    await $(BlockSkipPage.yes()).click();
    await $(BlockSkipPage.submit()).click();
    // calculated summary progress is not altered by removing the list collector from the path so next location is summary page
    await expect(await browser.getUrl()).to.contain(SectionOnePage.pageName);
    await $(SectionOnePage.previous()).click();
    // other calculated summary should not be on the path, so go straight back to the spending one which now has none of the list items
    await expect(await browser.getUrl()).to.contain(CalculatedSummarySpendingPage.pageName);
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total monthly expenditure on transport to be £100.00. Is this correct?",
    );
    await assertSummaryValues(["£100.00"]);
  });

  it("Given I confirm the calculated summary and finish the section, When I return to the Hub, Then I see that section 2 is no longer available", async () => {
    await $(CalculatedSummarySpendingPage.submit()).click();
    await $(SectionOnePage.submit()).click();
    // section 2 is now gone
    await expect(await $$(HubPage.summaryItems()).length).to.equal(1);
  });
});
