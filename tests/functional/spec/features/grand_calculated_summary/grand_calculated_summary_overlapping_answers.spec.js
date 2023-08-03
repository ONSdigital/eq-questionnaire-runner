import HubPage from "../../../base_pages/hub.page";
import IntroductionBlockPage from "../../../generated_pages/grand_calculated_summary_overlapping_answers/introduction-block.page";
import Block1Page from "../../../generated_pages/grand_calculated_summary_overlapping_answers/block-1.page";
import Block2Page from "../../../generated_pages/grand_calculated_summary_overlapping_answers/block-2.page";
import CalculatedSummary1Page from "../../../generated_pages/grand_calculated_summary_overlapping_answers/calculated-summary-1.page";
import CalculatedSummary2Page from "../../../generated_pages/grand_calculated_summary_overlapping_answers/calculated-summary-2.page";
import Block3Page from "../../../generated_pages/grand_calculated_summary_overlapping_answers/block-3.page";
import CalculatedSummary4Page from "../../../generated_pages/grand_calculated_summary_overlapping_answers/calculated-summary-4.page";
import GrandCalculatedSummaryShoppingPage from "../../../generated_pages/grand_calculated_summary_overlapping_answers/grand-calculated-summary-shopping.page";
import Section1SummaryPage from "../../../generated_pages/grand_calculated_summary_overlapping_answers/section-1-summary.page";

describe("Feature: Grand Calculated Summary", () => {
  describe("Given I have a Grand Calculated Summary with overlapping answers", () => {
    before("completing the survey", async () => {
      await browser.openQuestionnaire("test_grand_calculated_summary_overlapping_answers.json");
      await $(IntroductionBlockPage.submit()).click();

      // grand calculated summary should not be enabled until section-1 complete
      await expect(await $(HubPage.summaryRowLink("section-3")).isExisting()).to.be.false;

      await $(HubPage.submit()).click();
      await $(Block1Page.q1A1()).setValue(100);
      await $(Block1Page.q1A2()).setValue(200);
      await $(Block1Page.submit()).click();
      await $(Block2Page.q2A1()).setValue(10);
      await $(Block2Page.q2A2()).setValue(20);
      await $(Block2Page.submit()).click();
      await $(CalculatedSummary1Page.submit()).click();
      await $(CalculatedSummary2Page.submit()).click();
      await $(Block3Page.yesExtraBreadAndCheese()).click();
      await $(Block3Page.submit()).click();
      await $(CalculatedSummary4Page.submit()).click();
      await $(Section1SummaryPage.submit()).click();
      await $(HubPage.submit()).click();
      await expect(await $(GrandCalculatedSummaryShoppingPage.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary of purchases this week comes to £360.00. Is this correct?",
      );
      await $(GrandCalculatedSummaryShoppingPage.submit()).click();
    });

    it("Given I edit an answer that is only used in a single calculated summary, I am routed back to the calculated summary and then the grand calculated summary", async () => {
      await $(HubPage.summaryRowLink("section-3")).click();
      await $(GrandCalculatedSummaryShoppingPage.calculatedSummary2Edit()).click();
      await $(CalculatedSummary2Page.q1A2Edit()).click();
      await $(Block1Page.q1A2()).setValue(300);
      await $(Block1Page.submit()).click();

      // taken back to calculated summary
      await expect(await browser.getUrl()).to.contain(CalculatedSummary2Page.pageName);
      await $(CalculatedSummary2Page.submit()).click();

      // then grand calculated summary
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummaryShoppingPage.pageName);
      await expect(await $(GrandCalculatedSummaryShoppingPage.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary of purchases this week comes to £460.00. Is this correct?",
      );
    });

    it("Given I edit an answer that is used in two calculated summaries, if I edit it from the first calculated summary change link, I taken through each block between the question and the second calculated summary before returning to the grand calculated summary", async () => {
      await $(GrandCalculatedSummaryShoppingPage.calculatedSummary2Edit()).click();
      await $(CalculatedSummary2Page.q2A2Edit()).click();
      await $(Block2Page.q2A2()).setValue(400);
      await $(Block2Page.submit()).click();

      // taken back to the FIRST calculated summary which uses it
      await expect(await browser.getUrl()).to.contain(CalculatedSummary2Page.pageName);
      await expect(await $(CalculatedSummary2Page.calculatedSummaryTitle()).getText()).to.contain(
        "Total of eggs and cheese is calculated to be £700.00. Is this correct?",
      );
      await $(CalculatedSummary2Page.submit()).click();

      // taken back to the SECOND calculated summary which uses it
      await expect(await browser.getUrl()).to.contain(CalculatedSummary4Page.pageName);
      await expect(await $(CalculatedSummary4Page.calculatedSummaryTitle()).getText()).to.contain(
        "Total extra items cost is calculated to be £410.00. Is this correct?",
      );
      await $(CalculatedSummary4Page.submit()).click();

      // then grand calculated summary
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummaryShoppingPage.pageName);
      await expect(await $(GrandCalculatedSummaryShoppingPage.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary of purchases this week comes to £1,220.00. Is this correct?",
      );
    });

    it("Given I edit an answer that is used in two calculated summaries, if I edit it from the second calculated summary change link, I taken through each block between the question and the second calculated summary before returning to the grand calculated summary", async () => {
      await $(GrandCalculatedSummaryShoppingPage.calculatedSummary4Edit()).click();
      await $(CalculatedSummary4Page.q2A2Edit()).click();
      await $(Block2Page.q2A2()).setValue(500);
      await $(Block2Page.submit()).click();

      // taken back to the FIRST calculated summary which uses it
      await expect(await browser.getUrl()).to.contain(CalculatedSummary2Page.pageName);
      await expect(await $(CalculatedSummary2Page.calculatedSummaryTitle()).getText()).to.contain(
        "Total of eggs and cheese is calculated to be £800.00. Is this correct?",
      );
      await $(CalculatedSummary2Page.submit()).click();

      // taken back to the SECOND calculated summary which uses it
      await expect(await browser.getUrl()).to.contain(CalculatedSummary4Page.pageName);
      await expect(await $(CalculatedSummary4Page.calculatedSummaryTitle()).getText()).to.contain(
        "Total extra items cost is calculated to be £510.00. Is this correct?",
      );
      await $(CalculatedSummary4Page.submit()).click();

      // then grand calculated summary
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummaryShoppingPage.pageName);
      await expect(await $(GrandCalculatedSummaryShoppingPage.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary of purchases this week comes to £1,420.00. Is this correct?",
      );
      await $(GrandCalculatedSummaryShoppingPage.submit()).click();
    });

    it("Given I change an answer and return to the Hub before all calculated summaries are confirmed, the grand calculated summary section becomes inaccessible", async () => {
      await $(HubPage.summaryRowLink("section-3")).click();
      await $(GrandCalculatedSummaryShoppingPage.calculatedSummary4Edit()).click();
      await $(CalculatedSummary4Page.q2A2Edit()).click();
      await $(Block2Page.q2A2()).setValue(100);
      await $(Block2Page.submit()).click();

      // confirm one of the calculated summaries but return to the hub instead of confirming the other
      await $(CalculatedSummary2Page.submit()).click();
      await browser.url(HubPage.url());

      // calculated summary 4 is not confirmed so GCS doesn't show
      await expect(await $(HubPage.summaryRowState("section-1")).getText()).to.equal("Partially completed");
      await expect(await $(HubPage.summaryRowLink("section-3")).isExisting()).to.be.false;
    });
  });
});
