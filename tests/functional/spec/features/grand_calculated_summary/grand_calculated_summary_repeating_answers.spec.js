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
import { assertSummaryItems, assertSummaryValues, repeatingAnswerChangeLink, click } from "../../../helpers";
import { expect } from "@wdio/globals";
import InternetBreakdownBlockPage from "../../../generated_pages/grand_calculated_summary_repeating_answers/internet-breakdown-block.page";
import Section6SummaryPage from "../../../generated_pages/grand_calculated_summary_repeating_answers/section-6-summary.page";
import PersonalExpenditureBlockPage from "../../../generated_pages/grand_calculated_summary_repeating_answers/personal-expenditure-block.page";
import GrandCalculatedSummaryPipingPage from "../../../generated_pages/grand_calculated_summary_repeating_answers/grand-calculated-summary-piping.page";

describe("Feature: Grand Calculated Summary", () => {
  const summaryRowTitles = ".ons-summary__row-title";

  describe("Given I have a Grand Calculated Summary across multiple sections", () => {
    before("Reaching the grand calculated summary section", async () => {
      await browser.openQuestionnaire("test_grand_calculated_summary_repeating_answers.json");
      await click(HubPage.submit());

      // complete 2 questions in section 1
      await $(Block1Page.q1A1()).setValue(10);
      await $(Block1Page.q1A2()).setValue(20);
      await click(Block1Page.submit());
      await $(Block2Page.q2A1()).setValue(30);
      await $(Block2Page.q2A2()).setValue(40);
      await click(Block2Page.submit());
      await click(CalculatedSummary1Page.submit());

      // and the one for section 2
      await $(Block3Page.q3A1()).setValue(100);
      await $(Block3Page.q3A2()).setValue(200);
      await click(Block3Page.submit());
      await click(CalculatedSummary2Page.submit());
      await click(CalculatedSummary3Page.submit());
      await click(GrandCalculatedSummary1Page.submit());
      await click(Section1SummaryPage.submit());
      await click(HubPage.submit());
      await $(Block4Page.q4A1()).setValue(5);
      await $(Block4Page.q4A2()).setValue(10);
      await click(Block4Page.submit());
      await click(CalculatedSummary4Page.submit());
      await click(HubPage.submit());
    });

    it("Given I click on the change link for a calculated summary, When I press continue, Then I am taken back to the grand calculated summary", async () => {
      await expect(await $(GrandCalculatedSummary2Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for shopping and entertainment is calculated to be £415.00. Is this correct?",
      );
      await $(GrandCalculatedSummary2Page.calculatedSummary1Edit()).click();
      await expect(browser).toHaveUrlContaining(CalculatedSummary1Page.pageName);

      await click(CalculatedSummary1Page.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary2Page.pageName);
    });

    it("Given I click on the change link for a calculated summary then one for an answer, When I press previous twice, I am return to the calculated summary then grand calculated summary", async () => {
      await $(GrandCalculatedSummary2Page.calculatedSummary1Edit()).click();
      await $(CalculatedSummary1Page.q1A1Edit()).click();
      await expect(browser).toHaveUrlContaining(Block1Page.pageName);

      await $(Block1Page.previous()).click();
      await expect(browser).toHaveUrlContaining(CalculatedSummary1Page.pageName);

      await $(CalculatedSummary1Page.previous()).click();
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary2Page.pageName);
    });

    it("Given I go back to the calculated summary and then to a question and edit the answer. I am first taken back to the each calculated summary that uses the answer, the grand calculated summary in section 1, and then the updated grand calculated summary in section 3.", async () => {
      await $(GrandCalculatedSummary2Page.calculatedSummary4Edit()).click();
      await expect(await $(CalculatedSummary4Page.calculatedSummaryTitle()).getText()).toContain(
        "Calculated Summary for games expenditure is calculated to be £15.00. Is this correct?",
      );
      await $(CalculatedSummary4Page.q4A1Edit()).click();
      await expect(browser).toHaveUrlContaining(Block4Page.pageName);

      await $(Block4Page.q4A1()).setValue(50);
      await click(Block4Page.submit());

      // first taken back to the calculated summary which has updated
      await expect(browser).toHaveUrlContaining(CalculatedSummary4Page.pageName);
      await expect(await $(CalculatedSummary4Page.calculatedSummaryTitle()).getText()).toContain(
        "Calculated Summary for games expenditure is calculated to be £60.00. Is this correct?",
      );
      await click(CalculatedSummary4Page.submit());

      // then taken back to the grand calculated summary which has also been updated correctly
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary2Page.pageName);
      await expect(await $(GrandCalculatedSummary2Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for shopping and entertainment is calculated to be £460.00. Is this correct?",
      );
    });

    it("Given I go back to another calculated summary and edit multiple answers, I am still correctly routed back to the grand calculated summary", async () => {
      await $(GrandCalculatedSummary2Page.calculatedSummary1Edit()).click();
      await expect(await $(CalculatedSummary1Page.calculatedSummaryTitle()).getText()).toContain(
        "Calculated Summary for food expenditure is calculated to be £100.00. Is this correct?",
      );

      // change first answer
      await $(CalculatedSummary1Page.q1A1Edit()).click();
      await expect(browser).toHaveUrlContaining(Block1Page.pageName);
      await $(Block1Page.q1A1()).setValue(100);
      await click(Block1Page.submit());

      // go to each calculated summary that uses the answer in turn, then each grand calculated summary up to the one we were editing
      await expect(browser).toHaveUrlContaining(CalculatedSummary1Page.pageName);
      await expect(await $(CalculatedSummary1Page.calculatedSummaryTitle()).getText()).toContain(
        "Calculated Summary for food expenditure is calculated to be £190.00. Is this correct?",
      );

      // change another answer
      await $(CalculatedSummary1Page.q2A2Edit()).click();
      await expect(browser).toHaveUrlContaining(Block2Page.pageName);
      await $(Block2Page.q2A2()).setValue(400);
      await click(Block2Page.submit());

      // back at updated calculated summary
      await expect(await $(CalculatedSummary1Page.calculatedSummaryTitle()).getText()).toContain(
        "Calculated Summary for food expenditure is calculated to be £550.00. Is this correct?",
      );

      // Go to each calculated/grand calculated summary including this answer and reconfirm before being taken back to grand calculated summary
      await click(CalculatedSummary1Page.submit());
      await expect(browser).toHaveUrlContaining(CalculatedSummary3Page.pageName);
      await click(CalculatedSummary3Page.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary1Page.pageName);
      await click(GrandCalculatedSummary1Page.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary2Page.pageName);
      await expect(await $(GrandCalculatedSummary2Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for shopping and entertainment is calculated to be £910.00. Is this correct?",
      );
    });

    it("Given I edit an answer included in a grand calculated summary, the calculated summary sections should return to partially completed, and the grand calculated summary becomes unavailable.", async () => {
      await click(GrandCalculatedSummary2Page.submit());
      await expect(await $(HubPage.summaryRowState("section-3")).getText()).toBe("Completed");

      // Now edit an answer from section 2 and go back to the hub
      await $(HubPage.summaryRowLink("section-3")).click();
      await $(GrandCalculatedSummary2Page.calculatedSummary4Edit()).click();
      await $(CalculatedSummary4Page.q4A1Edit()).click();
      await $(Block4Page.q4A1()).setValue(1);
      await click(Block4Page.submit());
      await $(CalculatedSummary4Page.previous()).click();
      await $(Block4Page.previous()).click();

      // calculated summary section should be in progress
      await expect(await $(HubPage.summaryRowState("section-2")).getText()).toBe("Partially completed");
      await expect(await $(HubPage.summaryRowLink("section-3")).isExisting()).toBe(false);
    });

    it("Given I confirm the calculated summary, When I return to the Hub, Then I see the grand calculated summary come back marked as partially completed", async () => {
      await $(HubPage.summaryRowLink("section-2")).click();
      await click(CalculatedSummary4Page.submit());
      await expect(await $(HubPage.summaryRowState("section-3")).getText()).toBe("Partially completed");
    });

    it("Given I set both answers to block 4 to zero which removes the Grand Calculated Summary from the path, I am routed back to the Hub after the calculated summary", async () => {
      await $(HubPage.summaryRowLink("section-3")).click();
      await $(GrandCalculatedSummary2Page.calculatedSummary4Edit()).click();
      await $(CalculatedSummary4Page.q4A1Edit()).click();
      await $(Block4Page.q4A1()).setValue(0);
      await $(Block4Page.q4A2()).setValue(0);
      await click(Block4Page.submit());
      await click(CalculatedSummary4Page.submit());
      // should be back at Hub, and grand calculated summary section not present
      await expect(browser).toHaveUrlContaining(HubPage.pageName);
      await expect(await $(HubPage.summaryRowLink("section-3")).isExisting()).toBe(false);
    });

    it("Given I have a grand calculated summary section requiring completion of all previous sections, When I complete each section in turn, Then I don't see the grand calculated summary until all sections are complete, at which point I see it on the Hub", async () => {
      // no grand calculated summary section on the hub
      await expect(await $(HubPage.summaryRowLink("section-6")).isExisting()).toBe(false);

      await click(HubPage.submit());
      await $(AnyUtilityBillsPage.yes()).click();
      await click(AnyUtilityBillsPage.submit());
      await $(AddUtilityBillPage.utilityBillName()).selectByAttribute("value", "Electricity");
      await click(AddUtilityBillPage.submit());
      await $(AnyOtherUtilityBillsPage.yes()).click();
      await click(AnyOtherUtilityBillsPage.submit());
      await $(AddUtilityBillPage.utilityBillName()).selectByAttribute("value", "Internet");
      await click(AddUtilityBillPage.submit());
      await $(AnyOtherUtilityBillsPage.yes()).click();
      await click(AnyOtherUtilityBillsPage.submit());
      await $(AddUtilityBillPage.utilityBillName()).selectByAttribute("value", "Gas");
      await click(AddUtilityBillPage.submit());
      await $(AnyOtherUtilityBillsPage.no()).click();
      await click(AnyOtherUtilityBillsPage.submit());
      await $$(DynamicAnswerPage.inputs())[0].setValue(150);
      await $$(DynamicAnswerPage.inputs())[1].setValue(35);
      await $$(DynamicAnswerPage.inputs())[2].setValue(65);
      await click(DynamicAnswerPage.submit());
      await click(CalculatedSummary5Page.submit());
      await click(Section4SummaryPage.submit());
      // still no grand calculated summary yet
      await expect(await $(HubPage.summaryRowLink("section-6")).isExisting()).toBe(false);

      await click(HubPage.submit());
      await $(AnyStreamingServicesPage.yes()).click();
      await click(AnyStreamingServicesPage.submit());
      await $(AddStreamingServicePage.streamingServiceName()).selectByAttribute("value", "Netflix");
      await click(AddStreamingServicePage.submit());
      await $(StreamingServiceRepeatingBlock1Page.streamingServiceMonthlyCost()).setValue(10);
      await $(StreamingServiceRepeatingBlock1Page.streamingServiceExtraCost()).setValue(0);
      await click(StreamingServiceRepeatingBlock1Page.submit());
      await $(StreamingServiceRepeatingBlock2Page.streamingServiceUsage()).setValue(20);
      await click(StreamingServiceRepeatingBlock2Page.submit());
      await $(AnyOtherStreamingServicesPage.yes()).click();
      await click(AnyOtherStreamingServicesPage.submit());
      await $(AddStreamingServicePage.streamingServiceName()).selectByAttribute("value", "Prime video");
      await click(AddStreamingServicePage.submit());
      await $(StreamingServiceRepeatingBlock1Page.streamingServiceMonthlyCost()).setValue(8);
      await $(StreamingServiceRepeatingBlock1Page.streamingServiceExtraCost()).setValue(12);
      await click(StreamingServiceRepeatingBlock1Page.submit());
      await $(StreamingServiceRepeatingBlock2Page.streamingServiceUsage()).setValue(25);
      await click(StreamingServiceRepeatingBlock2Page.submit());
      await $(AnyOtherStreamingServicesPage.no()).click();
      await click(AnyOtherStreamingServicesPage.submit());
      await click(CalculatedSummary6Page.submit());
      await click(CalculatedSummary7Page.submit());
      await $(OtherInternetUsagePage.mediaDownloads()).setValue(50);
      await $(OtherInternetUsagePage.miscInternet()).setValue(5);
      await click(OtherInternetUsagePage.submit());
      await click(CalculatedSummary8Page.submit());
      await click(Section5SummaryPage.submit());
      // grand calculated summary now present
      await expect(await $(HubPage.summaryRowLink("section-6")).isExisting()).toBe(true);
      await expect(await $(HubPage.summaryRowState("section-6")).getText()).toBe("Not started");
    });

    it("Given I have a calculated summary of repeating answers and a calculated summary of dynamic answers, When I reach the grand calculated summary of both, Then I see the correct total and items", async () => {
      await click(HubPage.submit());
      await expect(await $(GrandCalculatedSummary3Page.grandCalculatedSummaryTitle()).getText()).toContain(
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
      await click(GrandCalculatedSummary3Page.submit());
      await expect(await $(GrandCalculatedSummary4Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for internet usage is calculated to be 100 GB. Is this correct?",
      );
      assertSummaryValues(["45 GB", "55 GB", "100 GB"]);
      assertSummaryItems(["Total internet usage on streaming services", "Total internet usage on other services", "Total internet usage"]);
    });

    it("Given I have multiple calculated summaries of static, repeating and dynamic answers, When I reach the grand calculated summary of them all, Then I see the correct total and items", async () => {
      await click(GrandCalculatedSummary4Page.submit());
      await expect(await $(GrandCalculatedSummary5Page.grandCalculatedSummaryTitle()).getText()).toContain(
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
      await expect(browser).toHaveUrlContaining(DynamicAnswerPage.pageName);
      await $(DynamicAnswerPage.previous()).click();
      await $(CalculatedSummary5Page.previous()).click();
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary5Page.pageName);
    });

    it("Given I have a grand calculated summary featuring repeating answers, When I edit a dynamic answer, Then I return to the calculated summary to confirm, and then each affected grand calculated summary in turn", async () => {
      await $(GrandCalculatedSummary5Page.calculatedSummary5Edit()).click();
      await repeatingAnswerChangeLink(1).click();
      await $$(DynamicAnswerPage.inputs())[0].setValue("175");
      await click(DynamicAnswerPage.submit());
      await click(CalculatedSummary5Page.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary3Page.pageName);
      await expect(await $(GrandCalculatedSummary3Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for monthly spending on bills and services is calculated to be £305.00. Is this correct?",
      );
      await click(GrandCalculatedSummary3Page.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary5Page.pageName);
      await expect(await $(GrandCalculatedSummary5Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for total monthly household expenditure is calculated to be £1,155.00. Is this correct?",
      );
    });

    it("Given I have a grand calculated summary featuring repeating answers, When I click edit links to return to a list repeating block answer then previous twice, Then I return to the grand calculated summary anchored from where I started", async () => {
      await $(GrandCalculatedSummary5Page.calculatedSummary6Edit()).click();
      await repeatingAnswerChangeLink(2).click();
      await $(StreamingServiceRepeatingBlock1Page.previous()).click();
      await $(CalculatedSummary5Page.previous()).click();
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary5Page.pageName);
    });

    it("Given I have a grand calculated summary featuring repeating answers, When I edit a list repeating block answer, Then I return to the calculated summary to confirm, and then the grand calculated summary to confirm", async () => {
      await $(GrandCalculatedSummary5Page.calculatedSummary6Edit()).click();
      await repeatingAnswerChangeLink(2).click();
      await $(StreamingServiceRepeatingBlock1Page.streamingServiceMonthlyCost()).setValue(12);
      await click(StreamingServiceRepeatingBlock1Page.submit());
      await click(CalculatedSummary5Page.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary3Page.pageName);
      await expect(await $(GrandCalculatedSummary3Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for monthly spending on bills and services is calculated to be £309.00. Is this correct?",
      );
      await click(GrandCalculatedSummary3Page.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary5Page.pageName);
      await expect(await $(GrandCalculatedSummary5Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for total monthly household expenditure is calculated to be £1,159.00. Is this correct?",
      );
    });

    it("Given I pipe the grand calculated summary into the next question, When I press continue, Then I see the correct title", async () => {
      await click(GrandCalculatedSummary5Page.submit());
      await expect(await $(InternetBreakdownBlockPage.questionTitle()).getText()).toContain("How did you use the 100 GB across your devices?")
    });

    it("Given I use the grand calculated summary for validation, When I enter values with too large a sum, Then I see a validation error", async () => {
      await $(InternetBreakdownBlockPage.internetPc()).setValue(60);
      await $(InternetBreakdownBlockPage.internetPhone()).setValue(60);
      await click(InternetBreakdownBlockPage.submit());
      await expect(await $(InternetBreakdownBlockPage.errorNumber(1)).getText()).toContain("Enter answers that add up to 100");
    });

    it("Given I use the grand calculated summary for validation, When I enter values with the correct sum, Then I progress to the summary page", async () => {
      await $(InternetBreakdownBlockPage.internetPhone()).setValue(40);
      await click(InternetBreakdownBlockPage.submit());
      await expect(browser).toHaveUrlContaining(Section6SummaryPage.pageName);
      await click(Section6SummaryPage.submit());
    });

    it("Given I have a grand calculated summary featuring dynamic answers, When I add an item to the list collector and return to the hub, Then I see the section with dynamic answers is in progress, and the grand calculated summary section is not available", async () => {
      await $(HubPage.summaryRowLink("section-4")).click();
      await $(Section4SummaryPage.utilityBillsListAddLink()).click();
      await $(AddUtilityBillPage.utilityBillName()).selectByAttribute("value", "Water");
      await click(AddUtilityBillPage.submit());
      await $(AnyOtherUtilityBillsPage.no()).click();
      await click(AnyOtherUtilityBillsPage.submit());
      await $$(DynamicAnswerPage.inputs())[3].setValue("40");
      await click(DynamicAnswerPage.submit());
      await browser.url(HubPage.url());
      await expect(await $(HubPage.summaryRowState("section-4")).getText()).toContain("Partially completed");
      await expect(await $(HubPage.summaryRowLink("section-6")).isExisting()).toBe(false);
    });

    it("Given I complete the in progress section, When I return to the Hub, Then I see the grand calculated summary section re-enabled, and partially completed", async () => {
      await $(HubPage.summaryRowLink("section-4")).click();
      await expect(await $(CalculatedSummary5Page.calculatedSummaryTitle()).getText()).toContain(
        "Calculated Summary for monthly spending on utility bills is calculated to be £315.00. Is this correct?",
      );
      await click(CalculatedSummary5Page.submit());
      await click(Section4SummaryPage.submit());
      await expect(await $(HubPage.summaryRowState("section-6")).getText()).toContain("Partially completed");
    });

    it("Given I return to the grand calculated summary section, When I go to each grand calculated summary, Then I see the correct new values", async () => {
      await $(HubPage.summaryRowLink("section-6")).click();
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary3Page.pageName);
      await expect(await $(GrandCalculatedSummary3Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for monthly spending on bills and services is calculated to be £349.00. Is this correct?",
      );
      await click(GrandCalculatedSummary3Page.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary4Page.pageName);
      await expect(await $(GrandCalculatedSummary4Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for internet usage is calculated to be 100 GB. Is this correct?",
      );
      await click(GrandCalculatedSummary4Page.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary5Page.pageName);
      await expect(await $(GrandCalculatedSummary5Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for total monthly household expenditure is calculated to be £1,199.00. Is this correct?",
      );
      await click(GrandCalculatedSummary5Page.submit());
      await expect(browser).toHaveUrlContaining(Section6SummaryPage.pageName);
      await expect(await $$(summaryRowTitles)[0].getText()).toContain("How did you use the 100 GB across your devices?");
      await click(Section6SummaryPage.submit());
      await expect(await $(HubPage.summaryRowState("section-6")).getText()).toContain("Completed");
    });

    it("Given I add a list item for the section with list repeating blocks, When I return to the hub before and after completing the section, Then I see the grand calculated summary go from unavailable, to enabled and in progress", async () => {
      await $(HubPage.summaryRowLink("section-5")).click();
      await $(Section5SummaryPage.streamingServicesListAddLink()).click();
      await $(AddStreamingServicePage.streamingServiceName()).selectByAttribute("value", "Disney+");
      await click(AddStreamingServicePage.submit());
      await $(StreamingServiceRepeatingBlock1Page.streamingServiceMonthlyCost()).setValue(10);
      await click(StreamingServiceRepeatingBlock1Page.submit());
      await $(StreamingServiceRepeatingBlock2Page.streamingServiceUsage()).setValue(5);
      await click(StreamingServiceRepeatingBlock2Page.submit());
      await $(AnyOtherStreamingServicesPage.no()).click();
      await click(AnyOtherStreamingServicesPage.submit());
      await expect(await $(CalculatedSummary6Page.calculatedSummaryTitle()).getText()).toContain(
        "Calculated Summary for monthly expenditure on streaming services is calculated to be £44.00. Is this correct?",
      );
      await browser.url(HubPage.url());
      await expect(await $(HubPage.summaryRowState("section-5")).getText()).toContain("Partially completed");
      await expect(await $(HubPage.summaryRowLink("section-6")).isExisting()).toBe(false);
      await $(HubPage.summaryRowLink("section-5")).click();
      await click(CalculatedSummary6Page.submit());
      await expect(await $(CalculatedSummary7Page.calculatedSummaryTitle()).getText()).toContain(
        "Total monthly internet usage on streaming services is calculated to be 50 GB. Is this correct?",
      );
      await click(CalculatedSummary7Page.submit());
      await click(Section5SummaryPage.submit());
      await expect(await $(HubPage.summaryRowState("section-6")).getText()).toContain("Partially completed");
    });

    it("Given I the grand calculated summary section is now incomplete, When I return to the section, Then I am taken to each updated grand calculated summary to confirm the new total", async () => {
      await $(HubPage.summaryRowLink("section-6")).click();
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary3Page.pageName);
      await expect(await $(GrandCalculatedSummary3Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for monthly spending on bills and services is calculated to be £359.00. Is this correct?",
      );
      await click(GrandCalculatedSummary3Page.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary4Page.pageName);
      await expect(await $(GrandCalculatedSummary4Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for internet usage is calculated to be 105 GB. Is this correct?",
      );
      await click(GrandCalculatedSummary4Page.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary5Page.pageName);
      await expect(await $(GrandCalculatedSummary5Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for total monthly household expenditure is calculated to be £1,209.00. Is this correct?",
      );
      await click(GrandCalculatedSummary5Page.submit());
      await click(Section6SummaryPage.submit());
    });

    it("Given I remove a list item involved in the grand calculated summary, When I confirm, Then I am taken to each affected calculated summary to reconfirm, and when I return to the Hub the grand calculated summary is in progress", async () => {
      await expect(await $(HubPage.summaryRowState("section-6")).getText()).toContain("Completed");
      await $(HubPage.summaryRowLink("section-5")).click();
      await $(Section5SummaryPage.streamingServicesListRemoveLink(1)).click();
      await $(RemoveStreamingServicePage.yes()).click();
      await click(RemoveStreamingServicePage.submit());
      await expect(await $(CalculatedSummary6Page.calculatedSummaryTitle()).getText()).toContain(
        "Calculated Summary for monthly expenditure on streaming services is calculated to be £34.00. Is this correct?",
      );
      await click(CalculatedSummary6Page.submit());
      await expect(await $(CalculatedSummary7Page.calculatedSummaryTitle()).getText()).toContain(
        "Total monthly internet usage on streaming services is calculated to be 30 GB. Is this correct?",
      );
      await click(CalculatedSummary7Page.submit());
      await click(Section5SummaryPage.submit());
      await expect(await $(HubPage.summaryRowState("section-6")).getText()).toContain("Partially completed");
    });

    it("Given the section has reverted to partially complete, When I go back to the section, Then I am taken to each grand calculated summary to reconfirm with correct values", async () => {
      await $(HubPage.summaryRowLink("section-6")).click();
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary3Page.pageName);
      await expect(await $(GrandCalculatedSummary3Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for monthly spending on bills and services is calculated to be £349.00. Is this correct?",
      );
      await click(GrandCalculatedSummary3Page.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary4Page.pageName);
      await expect(await $(GrandCalculatedSummary4Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for internet usage is calculated to be 85 GB. Is this correct?",
      );
      await click(GrandCalculatedSummary4Page.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummary5Page.pageName);
      await expect(await $(GrandCalculatedSummary5Page.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary for total monthly household expenditure is calculated to be £1,199.00. Is this correct?",
      );
      await click(GrandCalculatedSummary5Page.submit());
    });

    it("Given I have a further section depending on the grand calculated summary section, When I return to the Hub, Then I see the new section is available", async () => {
      await click(Section6SummaryPage.submit());
      await expect(await $(HubPage.summaryRowState("section-7")).getText()).toContain("Not started");
      await click(HubPage.submit());
    });

    it("Given I use a grand calculated summary value as a maximum, When I enter a value that is too large, Then I see a validation error", async () => {
      await expect(await $(PersonalExpenditureBlockPage.questionTitle()).getText()).toContain("How much of the £1,199 household expenditure do you contribute personally?");
      await $(PersonalExpenditureBlockPage.personalExpenditure()).setValue(1200);
      await click(PersonalExpenditureBlockPage.submit());
      await expect(await $(PersonalExpenditureBlockPage.errorNumber(1)).getText()).toContain("Enter an answer less than or equal to £1,199.00");
    });

    it("Given I display multiple grand calculated summaries on an Interstitial page, When I reach the page, Then I see the correct values piped in", async () => {
      await $(PersonalExpenditureBlockPage.personalExpenditure()).setValue(1100);
      await click(PersonalExpenditureBlockPage.submit());
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryPipingPage.pageName);
      await expect(await $("body").getText()).toContain("Total household expenditure: £1,199");
      await expect(await $("body").getText()).toContain("Personal contribution: £1,100");
      await expect(await $("body").getText()).toContain("Total internet usage: 85 GB");
      await expect(await $("body").getText()).toContain("Usage by phone: 40 GB");
      await expect(await $("body").getText()).toContain("Usage by PC: 60 GB");
    });
  });
});
