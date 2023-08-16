import HubPage from "../../../base_pages/hub.page";
import Block1Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/block-1.page";
import Block2Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/block-2.page";
import CalculatedSummary1Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-1.page";
import Block3Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/block-3.page";
import Block4Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/block-4.page";
import CalculatedSummary2Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-2.page";
import CalculatedSummary3Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-3.page";
import CalculatedSummary4Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-4.page";
import GrandCalculatedSummary1Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/grand-calculated-summary-1.page";
import GrandCalculatedSummary2Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/grand-calculated-summary-2.page";
import Section1SummaryPage from "../../../generated_pages/grand_calculated_summary_repeating_answers/section-1-summary.page";
import AddUtilityBillPage from "../../../generated_pages/grand_calculated_summary_repeating_answers/any-other-utility-bills-add.page.js";
import AnyOtherUtilityBillsPage from "../../../generated_pages/grand_calculated_summary_repeating_answers/any-other-utility-bills.page.js";
import DynamicAnswerPage from "../../../generated_pages/grand_calculated_summary_repeating_answers/dynamic-answer.page.js";
import CalculatedSummary5Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-5.page.js";
import AnyStreamingServicesPage from "../../../generated_pages/grand_calculated_summary_repeating_answers/any-streaming-services.page.js";
import AddStreamingServicePage from "../../../generated_pages/grand_calculated_summary_repeating_answers/any-other-streaming-services-add.page.js";
import RemoveStreamingServicePage from "../../../generated_pages/grand_calculated_summary_repeating_answers/any-other-streaming-services-remove.page.js";
import StreamingServiceRepeatingBlock1Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/streaming-service-repeating-block-1-repeating-block.page.js";
import StreamingServiceRepeatingBlock2Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/streaming-service-repeating-block-2-repeating-block.page.js";
import AnyOtherStreamingServicesPage from "../../../generated_pages/grand_calculated_summary_repeating_answers/any-other-streaming-services.page.js";
import CalculatedSummary6Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-6.page.js";
import CalculatedSummary7Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-7.page.js";
import OtherInternetUsagePage from "../../../generated_pages/grand_calculated_summary_repeating_answers/other-internet-usage.page.js";
import CalculatedSummary8Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/calculated-summary-8.page.js";
import GrandCalculatedSummary3Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/grand-calculated-summary-3.page.js";
import GrandCalculatedSummary4Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/grand-calculated-summary-4.page.js";
import GrandCalculatedSummary5Page from "../../../generated_pages/grand_calculated_summary_repeating_answers/grand-calculated-summary-5.page.js";
import AnyUtilityBillsPage from "../../../generated_pages/grand_calculated_summary_repeating_answers/any-utility-bills.page";
import Section4SummaryPage from "../../../generated_pages/grand_calculated_summary_repeating_answers/section-4-summary.page";
import Section5SummaryPage from "../../../generated_pages/grand_calculated_summary_repeating_answers/section-5-summary.page";
import { assertSummaryItems, assertSummaryValues, repeatingAnswerChangeLink } from "../../../helpers";

describe("Feature: Grand Calculated Summary", () => {
  describe("Given I have a Grand Calculated Summary across multiple sections", () => {
    before("Reaching the grand calculated summary section", async () => {
      await browser.openQuestionnaire("test_grand_calculated_summary_repeating_answers.json");
      await $(HubPage.submit()).click();

      // complete 2 questions in section 1
      await $(Block1Page.q1A1()).setValue(10);
      await $(Block1Page.q1A2()).setValue(20);
      await $(Block1Page.submit()).click();
      await $(Block2Page.q2A1()).setValue(30);
      await $(Block2Page.q2A2()).setValue(40);
      await $(Block2Page.submit()).click();
      await $(CalculatedSummary1Page.submit()).click();

      // and the one for section 2
      await $(Block3Page.q3A1()).setValue(100);
      await $(Block3Page.q3A2()).setValue(200);
      await $(Block3Page.submit()).click();
      await $(CalculatedSummary2Page.submit()).click();
      await $(CalculatedSummary3Page.submit()).click();
      await $(GrandCalculatedSummary1Page.submit()).click();
      await $(Section1SummaryPage.submit()).click();
      await $(HubPage.submit()).click();
      await $(Block4Page.q4A1()).setValue(5);
      await $(Block4Page.q4A2()).setValue(10);
      await $(Block4Page.submit()).click();
      await $(CalculatedSummary4Page.submit()).click();
      await $(HubPage.submit()).click();
    });

    it("Given I click on the change link for a calculated summary then press continue, I am taken back to the grand calculated summary", async () => {
      await expect(await $(GrandCalculatedSummary2Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for shopping and entertainment is calculated to be £415.00. Is this correct?",
      );
      await $(GrandCalculatedSummary2Page.calculatedSummary1Edit()).click();
      await expect(await browser.getUrl()).to.contain(CalculatedSummary1Page.pageName);

      await $(CalculatedSummary1Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary2Page.pageName);
    });

    it("Given I go back to the calculated summary and then to a question and edit the answer. I am first taken back to the each calculated summary that uses the answer, the grand calculated summary in section 1, and then the updated grand calculated summary in section 3.", async () => {
      await $(GrandCalculatedSummary2Page.calculatedSummary4Edit()).click();
      await expect(await $(CalculatedSummary4Page.calculatedSummaryTitle()).getText()).to.contain(
        "Calculated Summary for games expenditure is calculated to be £15.00. Is this correct?",
      );
      await $(CalculatedSummary4Page.q4A1Edit()).click();
      await expect(await browser.getUrl()).to.contain(Block4Page.pageName);

      await $(Block4Page.q4A1()).setValue(50);
      await $(Block4Page.submit()).click();

      // first taken back to the calculated summary which has updated
      await expect(await browser.getUrl()).to.contain(CalculatedSummary4Page.pageName);
      await expect(await $(CalculatedSummary4Page.calculatedSummaryTitle()).getText()).to.contain(
        "Calculated Summary for games expenditure is calculated to be £60.00. Is this correct?",
      );
      await $(CalculatedSummary4Page.submit()).click();

      // then taken back to the grand calculated summary which has also been updated correctly
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary2Page.pageName);
      await expect(await $(GrandCalculatedSummary2Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for shopping and entertainment is calculated to be £460.00. Is this correct?",
      );
    });

    it("Given I go back to another calculated summary and edit multiple answers, I am still correctly routed back to the grand calculated summary", async () => {
      await $(GrandCalculatedSummary2Page.calculatedSummary1Edit()).click();
      await expect(await $(CalculatedSummary1Page.calculatedSummaryTitle()).getText()).to.contain(
        "Calculated Summary for food expenditure is calculated to be £100.00. Is this correct?",
      );

      // change first answer
      await $(CalculatedSummary1Page.q1A1Edit()).click();
      await expect(await browser.getUrl()).to.contain(Block1Page.pageName);
      await $(Block1Page.q1A1()).setValue(100);
      await $(Block1Page.submit()).click();

      // go to each calculated summary that uses the answer in turn, then each grand calculated summary up to the one we were editing
      await expect(await browser.getUrl()).to.contain(CalculatedSummary1Page.pageName);
      await expect(await $(CalculatedSummary1Page.calculatedSummaryTitle()).getText()).to.contain(
        "Calculated Summary for food expenditure is calculated to be £190.00. Is this correct?",
      );

      // change another answer
      await $(CalculatedSummary1Page.q2A2Edit()).click();
      await expect(await browser.getUrl()).to.contain(Block2Page.pageName);
      await $(Block2Page.q2A2()).setValue(400);
      await $(Block2Page.submit()).click();

      // back at updated calculated summary
      await expect(await $(CalculatedSummary1Page.calculatedSummaryTitle()).getText()).to.contain(
        "Calculated Summary for food expenditure is calculated to be £550.00. Is this correct?",
      );

      // Go to each calculated/grand calculated summary including this answer and reconfirm before being taken back to grand calculated summary
      await $(CalculatedSummary1Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(CalculatedSummary3Page.pageName);
      await $(CalculatedSummary3Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary1Page.pageName);
      await $(GrandCalculatedSummary1Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary2Page.pageName);
      await expect(await $(GrandCalculatedSummary2Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for shopping and entertainment is calculated to be £910.00. Is this correct?",
      );
    });

    it("Given I edit an answer included in a grand calculated summary, the calculated summary sections should return to partially completed, and the grand calculated summary becomes unavailable.", async () => {
      await $(GrandCalculatedSummary2Page.submit()).click();
      await expect(await $(HubPage.summaryRowState("section-3")).getText()).to.equal("Completed");

      // Now edit an answer from section 2 and go back to the hub
      await $(HubPage.summaryRowLink("section-3")).click();
      await $(GrandCalculatedSummary2Page.calculatedSummary4Edit()).click();
      await $(CalculatedSummary4Page.q4A1Edit()).click();
      await $(Block4Page.q4A1()).setValue(1);
      await $(Block4Page.submit()).click();
      await $(CalculatedSummary4Page.previous()).click();
      await $(Block4Page.previous()).click();

      // calculated summary section should be in progress
      await expect(await $(HubPage.summaryRowState("section-2")).getText()).to.equal("Partially completed");
      await expect(await $(HubPage.summaryRowLink("section-3")).isExisting()).to.be.false;
    });

    it("Given I confirm the calculated summary, When I return to the Hub, Then I see the grand calculated summary come back marked as partially completed", async () => {
      await $(HubPage.summaryRowLink("section-2")).click();
      await $(CalculatedSummary4Page.submit()).click();
      await expect(await $(HubPage.summaryRowState("section-3")).getText()).to.equal("Partially completed");
    });

    it("Given I set both answers to block 4 to zero which removes the Grand Calculated Summary from the path, I am routed back to the Hub after the calculated summary", async () => {
      await $(HubPage.summaryRowLink("section-3")).click();
      await $(GrandCalculatedSummary2Page.calculatedSummary4Edit()).click();
      await $(CalculatedSummary4Page.q4A1Edit()).click();
      await $(Block4Page.q4A1()).setValue(0);
      await $(Block4Page.q4A2()).setValue(0);
      await $(Block4Page.submit()).click();
      await $(CalculatedSummary4Page.submit()).click();
      // should be back at Hub, and grand calculated summary section not present
      await expect(await browser.getUrl()).to.contain(HubPage.pageName);
      await expect(await $(HubPage.summaryRowLink("section-3")).isExisting()).to.be.false;
    });

    it("Given I have a grand calculated summary section requiring completion of all previous sections, When I complete each section in turn, Then I don't see the grand calculated summary until all sections are complete, at which point I see it on the Hub", async () => {
      // no grand calculated summary section on the hub
      await expect(await $(HubPage.summaryRowLink("section-6")).isExisting()).to.be.false;

      await $(HubPage.submit()).click();
      await $(AnyUtilityBillsPage.yes()).click();
      await $(AnyUtilityBillsPage.submit()).click();
      await $(AddUtilityBillPage.utilityBillName()).selectByAttribute("value", "Electricity");
      await $(AddUtilityBillPage.submit()).click();
      await $(AnyOtherUtilityBillsPage.yes()).click();
      await $(AnyOtherUtilityBillsPage.submit()).click();
      await $(AddUtilityBillPage.utilityBillName()).selectByAttribute("value", "Internet");
      await $(AddUtilityBillPage.submit()).click();
      await $(AnyOtherUtilityBillsPage.yes()).click();
      await $(AnyOtherUtilityBillsPage.submit()).click();
      await $(AddUtilityBillPage.utilityBillName()).selectByAttribute("value", "Gas");
      await $(AddUtilityBillPage.submit()).click();
      await $(AnyOtherUtilityBillsPage.no()).click();
      await $(AnyOtherUtilityBillsPage.submit()).click();
      await $$(DynamicAnswerPage.inputs())[0].setValue(150);
      await $$(DynamicAnswerPage.inputs())[1].setValue(35);
      await $$(DynamicAnswerPage.inputs())[2].setValue(65);
      await $(DynamicAnswerPage.submit()).click();
      await $(CalculatedSummary5Page.submit()).click();
      await $(Section4SummaryPage.submit()).click();
      // still no grand calculated summary yet
      await expect(await $(HubPage.summaryRowLink("section-6")).isExisting()).to.be.false;

      await $(HubPage.submit()).click();
      await $(AnyStreamingServicesPage.yes()).click();
      await $(AnyStreamingServicesPage.submit()).click();
      await $(AddStreamingServicePage.streamingServiceName()).selectByAttribute("value", "Netflix");
      await $(AddStreamingServicePage.submit()).click();
      await $(StreamingServiceRepeatingBlock1Page.streamingServiceMonthlyCost()).setValue(10);
      await $(StreamingServiceRepeatingBlock1Page.streamingServiceExtraCost()).setValue(0);
      await $(StreamingServiceRepeatingBlock1Page.submit()).click();
      await $(StreamingServiceRepeatingBlock2Page.streamingServiceUsage()).setValue(20);
      await $(StreamingServiceRepeatingBlock2Page.submit()).click();
      await $(AnyOtherStreamingServicesPage.yes()).click();
      await $(AnyOtherStreamingServicesPage.submit()).click();
      await $(AddStreamingServicePage.streamingServiceName()).selectByAttribute("value", "Prime video");
      await $(AddStreamingServicePage.submit()).click();
      await $(StreamingServiceRepeatingBlock1Page.streamingServiceMonthlyCost()).setValue(8);
      await $(StreamingServiceRepeatingBlock1Page.streamingServiceExtraCost()).setValue(12);
      await $(StreamingServiceRepeatingBlock1Page.submit()).click();
      await $(StreamingServiceRepeatingBlock2Page.streamingServiceUsage()).setValue(25);
      await $(StreamingServiceRepeatingBlock2Page.submit()).click();
      await $(AnyOtherStreamingServicesPage.no()).click();
      await $(AnyOtherStreamingServicesPage.submit()).click();
      await $(CalculatedSummary6Page.submit()).click();
      await $(CalculatedSummary7Page.submit()).click();
      await $(OtherInternetUsagePage.mediaDownloads()).setValue(50);
      await $(OtherInternetUsagePage.miscInternet()).setValue(5);
      await $(OtherInternetUsagePage.submit()).click();
      await $(CalculatedSummary8Page.submit()).click();
      await $(Section5SummaryPage.submit()).click();
      // grand calculated summary now present
      await expect(await $(HubPage.summaryRowLink("section-6")).isExisting()).to.be.true;
      await expect(await $(HubPage.summaryRowState("section-6")).getText()).to.equal("Not started");
    });

    it("Given I have a calculated summary of repeating answers and a calculated summary of dynamic answers, When I reach the grand calculated summary of both, Then I see the correct total and items", async () => {
      await $(HubPage.submit()).click();
      await expect(await $(GrandCalculatedSummary3Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for monthly spending on bills and services is calculated to be £280.00. Is this correct?",
      );
      assertSummaryValues(["£250.00", "£30.00", "£280.00"]);
      assertSummaryItems([
        "Total monthly expenditure on utility bills",
        "Total monthly expenditure on streaming services",
        "Total monthly expenditure on bills and streaming services",
      ]);
    });

    it("Given I have 2 calculated summaries of list repeating block answers, When I reach the grand calculated summary of both, Then I see the correct total and items", async () => {
      await $(GrandCalculatedSummary3Page.submit()).click();
      await expect(await $(GrandCalculatedSummary4Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for internet usage is calculated to be 100 GB. Is this correct?",
      );
      assertSummaryValues(["45 GB", "55 GB", "100 GB"]);
      assertSummaryItems(["Total internet usage on streaming services", "Total internet usage on other services", "Total internet usage"]);
    });

    it("Given I have multiple calculated summaries of static, repeating and dynamic answers, When I reach the grand calculated summary of them all, Then I see the correct total and items", async () => {
      await $(GrandCalculatedSummary4Page.submit()).click();
      await expect(await $(GrandCalculatedSummary5Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for total monthly household expenditure is calculated to be £1,130.00. Is this correct?",
      );
      assertSummaryValues(["£550.00", "£300.00", "£0.00", "£250.00", "£30.00", "£1,130.00"]);
      assertSummaryValues([
        "Total monthly food expenditure",
        "Total monthly clothes expenditure",
        "Total games expenditure",
        "Total monthly expenditure on utility bills",
        "Total monthly expenditure on streaming services",
      ]);
    });

    it("Given I a grand calculated summary featuring repeating answers, When I click edit links to return to a dynamic answer then previous twice, Then I return to the grand calculated summary where I started", async () => {
      await $(GrandCalculatedSummary5Page.calculatedSummary5Edit()).click();
      await repeatingAnswerChangeLink(0).click();
      await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
      await $(DynamicAnswerPage.previous()).click();
      await $(CalculatedSummary5Page.previous()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary5Page.pageName);
    });

    it("Given I have a grand calculated summary featuring repeating answers, When I edit a dynamic answer, Then I return to the calculated summary to confirm, and then each affected grand calculated summary in turn", async () => {
      await $(GrandCalculatedSummary5Page.calculatedSummary5Edit()).click();
      await repeatingAnswerChangeLink(1).click();
      await $$(DynamicAnswerPage.inputs())[0].setValue("175");
      await $(DynamicAnswerPage.submit()).click();
      await $(CalculatedSummary5Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary3Page.pageName);
      await expect(await $(GrandCalculatedSummary3Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for monthly spending on bills and services is calculated to be £305.00. Is this correct?",
      );
      await $(GrandCalculatedSummary3Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary5Page.pageName);
      await expect(await $(GrandCalculatedSummary5Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for total monthly household expenditure is calculated to be £1,155.00. Is this correct?",
      );
    });

    it("Given I have a grand calculated summary featuring repeating answers, When I click edit links to return to a list repeating block answer then previous twice, Then I return to the grand calculated summary anchored from where I started", async () => {
      await $(GrandCalculatedSummary5Page.calculatedSummary6Edit()).click();
      await repeatingAnswerChangeLink(2).click();
      await $(StreamingServiceRepeatingBlock1Page.previous()).click();
      await $(CalculatedSummary5Page.previous()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary5Page.pageName);
    });

    it("Given I have a grand calculated summary featuring repeating answers, When I edit a list repeating block answer, Then I return to the calculated summary to confirm, and then the grand calculated summary to confirm", async () => {
      await $(GrandCalculatedSummary5Page.calculatedSummary6Edit()).click();
      await repeatingAnswerChangeLink(2).click();
      await $(StreamingServiceRepeatingBlock1Page.streamingServiceMonthlyCost()).setValue(12);
      await $(StreamingServiceRepeatingBlock1Page.submit()).click();
      await $(CalculatedSummary5Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary3Page.pageName);
      await expect(await $(GrandCalculatedSummary3Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for monthly spending on bills and services is calculated to be £309.00. Is this correct?",
      );
      await $(GrandCalculatedSummary3Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary5Page.pageName);
      await expect(await $(GrandCalculatedSummary5Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for total monthly household expenditure is calculated to be £1,159.00. Is this correct?",
      );
      await $(GrandCalculatedSummary5Page.submit()).click();
    });

    it("Given I have a grand calculated summary featuring dynamic answers, When I add an item to the list collector and return to the hub, Then I see the section with dynamic answers is in progress, and the grand calculated summary section is not available", async () => {
      await $(HubPage.summaryRowLink("section-4")).click();
      await $(Section4SummaryPage.utilityBillsListAddLink()).click();
      await $(AddUtilityBillPage.utilityBillName()).selectByAttribute("value", "Water");
      await $(AddUtilityBillPage.submit()).click();
      await $(AnyOtherUtilityBillsPage.no()).click();
      await $(AnyOtherUtilityBillsPage.submit()).click();
      await $$(DynamicAnswerPage.inputs())[3].setValue("40");
      await $(DynamicAnswerPage.submit()).click();
      await browser.url(HubPage.url());
      await expect(await $(HubPage.summaryRowState("section-4")).getText()).to.contain("Partially completed");
      await expect(await $(HubPage.summaryRowLink("section-6")).isExisting()).to.be.false;
    });

    it("Given I complete the in progress section, When I return to the Hub, Then I see the grand calculated summary section re-enabled, and partially completed", async () => {
      await $(HubPage.summaryRowLink("section-4")).click();
      await expect(await $(CalculatedSummary5Page.calculatedSummaryTitle()).getText()).to.contain(
        "Calculated Summary for monthly spending on utility bills is calculated to be £315.00. Is this correct?",
      );
      await $(CalculatedSummary5Page.submit()).click();
      await $(Section4SummaryPage.submit()).click();
      await expect(await $(HubPage.summaryRowState("section-6")).getText()).to.contain("Partially completed");
    });

    it("Given I return to the grand calculated summary section, When I go to each grand calculated summary, Then I see the correct new values", async () => {
      await $(HubPage.summaryRowLink("section-6")).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary3Page.pageName);
      await expect(await $(GrandCalculatedSummary3Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for monthly spending on bills and services is calculated to be £349.00. Is this correct?",
      );
      await $(GrandCalculatedSummary3Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary4Page.pageName);
      await expect(await $(GrandCalculatedSummary4Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for internet usage is calculated to be 100 GB. Is this correct?",
      );
      await $(GrandCalculatedSummary4Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary5Page.pageName);
      await expect(await $(GrandCalculatedSummary5Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for total monthly household expenditure is calculated to be £1,199.00. Is this correct?",
      );
      await $(GrandCalculatedSummary5Page.submit()).click();
      await expect(await $(HubPage.summaryRowState("section-6")).getText()).to.contain("Completed");
    });

    it("Given I add a list item for the section with list repeating blocks, When I return to the hub before and after completing the section, Then I see the grand calculated summary go from unavailable, to enabled and in progress", async () => {
      await $(HubPage.summaryRowLink("section-5")).click();
      await $(Section5SummaryPage.streamingServicesListAddLink()).click();
      await $(AddStreamingServicePage.streamingServiceName()).selectByAttribute("value", "Disney+");
      await $(AddStreamingServicePage.submit()).click();
      await $(StreamingServiceRepeatingBlock1Page.streamingServiceMonthlyCost()).setValue(10);
      await $(StreamingServiceRepeatingBlock1Page.submit()).click();
      await $(StreamingServiceRepeatingBlock2Page.streamingServiceUsage()).setValue(5);
      await $(StreamingServiceRepeatingBlock2Page.submit()).click();
      await $(AnyOtherStreamingServicesPage.no()).click();
      await $(AnyOtherStreamingServicesPage.submit()).click();
      await expect(await $(CalculatedSummary6Page.calculatedSummaryTitle()).getText()).to.contain(
        "Calculated Summary for monthly expenditure on streaming services is calculated to be £44.00. Is this correct?",
      );
      await browser.url(HubPage.url());
      await expect(await $(HubPage.summaryRowState("section-5")).getText()).to.contain("Partially completed");
      await expect(await $(HubPage.summaryRowLink("section-6")).isExisting()).to.be.false;
      await $(HubPage.summaryRowLink("section-5")).click();
      await $(CalculatedSummary6Page.submit()).click();
      await expect(await $(CalculatedSummary7Page.calculatedSummaryTitle()).getText()).to.contain(
        "Total monthly internet usage on streaming services is calculated to be 50 GB. Is this correct?",
      );
      await $(CalculatedSummary7Page.submit()).click();
      await $(Section5SummaryPage.submit()).click();
      await expect(await $(HubPage.summaryRowState("section-6")).getText()).to.contain("Partially completed");
    });

    it("Given I the grand calculated summary section is now incomplete, When I return to the section, Then I am taken to each updated grand calculated summary to confirm the new total", async () => {
      await $(HubPage.summaryRowLink("section-6")).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary3Page.pageName);
      await expect(await $(GrandCalculatedSummary3Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for monthly spending on bills and services is calculated to be £359.00. Is this correct?",
      );
      await $(GrandCalculatedSummary3Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary4Page.pageName);
      await expect(await $(GrandCalculatedSummary4Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for internet usage is calculated to be 105 GB. Is this correct?",
      );
      await $(GrandCalculatedSummary4Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary5Page.pageName);
      await expect(await $(GrandCalculatedSummary5Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for total monthly household expenditure is calculated to be £1,209.00. Is this correct?",
      );
      await $(GrandCalculatedSummary5Page.submit()).click();
    });

    it("Given I remove a list item involved in the grand calculated summary, When I confirm, Then I am taken to each affected calculated summary to reconfirm, and when I return to the Hub the grand calculated summary is in progress", async () => {
      await expect(await $(HubPage.summaryRowState("section-6")).getText()).to.contain("Completed");
      await $(HubPage.summaryRowLink("section-5")).click();
      await $(Section5SummaryPage.streamingServicesListRemoveLink(1)).click();
      await $(RemoveStreamingServicePage.yes()).click();
      await $(RemoveStreamingServicePage.submit()).click();
      await expect(await $(CalculatedSummary6Page.calculatedSummaryTitle()).getText()).to.contain(
        "Calculated Summary for monthly expenditure on streaming services is calculated to be £34.00. Is this correct?",
      );
      await $(CalculatedSummary6Page.submit()).click();
      await expect(await $(CalculatedSummary7Page.calculatedSummaryTitle()).getText()).to.contain(
        "Total monthly internet usage on streaming services is calculated to be 30 GB. Is this correct?",
      );
      await $(CalculatedSummary7Page.submit()).click();
      await $(Section5SummaryPage.submit()).click();
      await expect(await $(HubPage.summaryRowState("section-6")).getText()).to.contain("Partially completed");
    });

    it("Given the section has reverted to partially complete, When I go back to the section, Then I am taken to each grand calculated summary to reconfirm with correct values", async () => {
      await $(HubPage.summaryRowLink("section-6")).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary3Page.pageName);
      await expect(await $(GrandCalculatedSummary3Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for monthly spending on bills and services is calculated to be £349.00. Is this correct?",
      );
      await $(GrandCalculatedSummary3Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary4Page.pageName);
      await expect(await $(GrandCalculatedSummary4Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for internet usage is calculated to be 85 GB. Is this correct?",
      );
      await $(GrandCalculatedSummary4Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary5Page.pageName);
      await expect(await $(GrandCalculatedSummary5Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for total monthly household expenditure is calculated to be £1,199.00. Is this correct?",
      );
      await $(GrandCalculatedSummary5Page.submit()).click();
    });
  });
});
