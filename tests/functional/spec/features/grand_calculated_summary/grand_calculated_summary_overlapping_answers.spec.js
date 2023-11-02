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
import { click } from "../../../helpers";
import { expect } from "@wdio/globals";

describe("Feature: Grand Calculated Summary", () => {
  describe("Given I have a Grand Calculated Summary with overlapping answers", () => {
    before("completing the survey", async () => {
      await browser.openQuestionnaire("test_grand_calculated_summary_overlapping_answers.json");
      await click(IntroductionBlockPage.submit());

      // grand calculated summary should not be enabled until section-1 complete
      await expect(await $(HubPage.summaryRowLink("section-3")).isExisting()).toBe(false);

      await click(HubPage.submit());
      await $(Block1Page.q1A1()).setValue(100);
      await $(Block1Page.q1A2()).setValue(200);
      await click(Block1Page.submit());
      await $(Block2Page.q2A1()).setValue(10);
      await $(Block2Page.q2A2()).setValue(20);
      await click(Block2Page.submit());
      await click(CalculatedSummary1Page.submit());
      await click(CalculatedSummary2Page.submit());
      await $(Block3Page.yesExtraBreadAndCheese()).click();
      await click(Block3Page.submit());
      await click(CalculatedSummary4Page.submit());
      await click(Section1SummaryPage.submit());
      await click(HubPage.submit());
      await expect(await $(GrandCalculatedSummaryShoppingPage.grandCalculatedSummaryTitle()).getText()).toBe(
        "Grand Calculated Summary of purchases this week comes to £360.00. Is this correct?.",
      );
      await click(GrandCalculatedSummaryShoppingPage.submit());
    });

    it("Given I edit an answer that is only used in a single calculated summary, I am routed back to the calculated summary and then the grand calculated summary", async () => {
      await $(HubPage.summaryRowLink("section-3")).click();
      await $(GrandCalculatedSummaryShoppingPage.calculatedSummary2Edit()).click();
      await $(CalculatedSummary2Page.q1A2Edit()).click();
      await $(Block1Page.q1A2()).setValue(300);
      await click(Block1Page.submit());

      // taken back to calculated summary
      await expect(browser).toHaveUrlContaining(CalculatedSummary2Page.pageName);
      await click(CalculatedSummary2Page.submit());

      // then grand calculated summary
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryShoppingPage.pageName);
      await expect(await $(GrandCalculatedSummaryShoppingPage.grandCalculatedSummaryTitle()).getText()).toBe(
        "Grand Calculated Summary of purchases this week comes to £460.00. Is this correct?.",
      );
    });

    it("Given I edit an answer that is used in two calculated summaries, if I edit it from the first calculated summary change link, I taken through each block between the question and the second calculated summary before returning to the grand calculated summary", async () => {
      await $(GrandCalculatedSummaryShoppingPage.calculatedSummary2Edit()).click();
      await $(CalculatedSummary2Page.q2A2Edit()).click();
      await $(Block2Page.q2A2()).setValue(400);
      await click(Block2Page.submit());

      // taken back to the FIRST calculated summary which uses it
      await expect(browser).toHaveUrlContaining(CalculatedSummary2Page.pageName);
      await expect(await $(CalculatedSummary2Page.calculatedSummaryTitle()).getText()).toBe(
        "Total of eggs and cheese is calculated to be £700.00. Is this correct?",
      );
      await click(CalculatedSummary2Page.submit());

      // taken back to the SECOND calculated summary which uses it
      await expect(browser).toHaveUrlContaining(CalculatedSummary4Page.pageName);
      await expect(await $(CalculatedSummary4Page.calculatedSummaryTitle()).getText()).toContain(
        "Total extra items cost is calculated to be £410.00. Is this correct?",
      );
      await click(CalculatedSummary4Page.submit());

      // then grand calculated summary
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryShoppingPage.pageName);
      await expect(await $(GrandCalculatedSummaryShoppingPage.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary of purchases this week comes to £1,220.00. Is this correct?",
      );
    });

    it("Given I edit an answer that is used in two calculated summaries, if I edit it from the second calculated summary change link, I taken through each block between the question and the second calculated summary before returning to the grand calculated summary", async () => {
      await $(GrandCalculatedSummaryShoppingPage.calculatedSummary4Edit()).click();
      await $(CalculatedSummary4Page.q2A2Edit()).click();
      await $(Block2Page.q2A2()).setValue(500);
      await click(Block2Page.submit());

      // taken back to the FIRST calculated summary which uses it
      await expect(browser).toHaveUrlContaining(CalculatedSummary2Page.pageName);
      await expect(await $(CalculatedSummary2Page.calculatedSummaryTitle()).getText()).toBe(
        "Total of eggs and cheese is calculated to be £800.00. Is this correct?",
      );
      await click(CalculatedSummary2Page.submit());

      // taken back to the SECOND calculated summary which uses it
      await expect(browser).toHaveUrlContaining(CalculatedSummary4Page.pageName);
      await expect(await $(CalculatedSummary4Page.calculatedSummaryTitle()).getText()).toContain(
        "Total extra items cost is calculated to be £510.00. Is this correct?",
      );
      await click(CalculatedSummary4Page.submit());

      // then grand calculated summary
      await expect(browser).toHaveUrlContaining(GrandCalculatedSummaryShoppingPage.pageName);
      await expect(await $(GrandCalculatedSummaryShoppingPage.grandCalculatedSummaryTitle()).getText()).toContain(
        "Grand Calculated Summary of purchases this week comes to £1,420.00. Is this correct?",
      );
      await click(GrandCalculatedSummaryShoppingPage.submit());
    });

    it("Given I change an answer and return to the Hub before all calculated summaries are confirmed, the grand calculated summary section becomes inaccessible", async () => {
      await $(HubPage.summaryRowLink("section-3")).click();
      await $(GrandCalculatedSummaryShoppingPage.calculatedSummary4Edit()).click();
      await $(CalculatedSummary4Page.q2A2Edit()).click();
      await $(Block2Page.q2A2()).setValue(100);
      await click(Block2Page.submit());

      // confirm one of the calculated summaries but return to the hub instead of confirming the other
      await click(CalculatedSummary2Page.submit());
      await browser.url(HubPage.url());

      // calculated summary 4 is not confirmed so GCS doesn't show
      await expect(await $(HubPage.summaryRowState("section-1")).getText()).toBe("Partially completed");
      await expect(await $(HubPage.summaryRowLink("section-3")).isExisting()).toBe(false);
    });
  });
});
