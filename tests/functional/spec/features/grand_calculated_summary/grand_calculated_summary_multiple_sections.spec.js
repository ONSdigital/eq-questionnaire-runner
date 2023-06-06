import HubPage from "../../../base_pages/hub.page";
import Block1Page from "../../../generated_pages/grand_calculated_summary_multiple_sections/block-1.page";
import Block2Page from "../../../generated_pages/grand_calculated_summary_multiple_sections/block-2.page";
import CalculatedSummary1Page from "../../../generated_pages/grand_calculated_summary_multiple_sections/calculated-summary-1.page";
import Block3Page from "../../../generated_pages/grand_calculated_summary_multiple_sections/block-3.page";
import Block4Page from "../../../generated_pages/grand_calculated_summary_multiple_sections/block-4.page";
import CalculatedSummary2Page from "../../../generated_pages/grand_calculated_summary_multiple_sections/calculated-summary-2.page";
import CalculatedSummary3Page from "../../../generated_pages/grand_calculated_summary_multiple_sections/calculated-summary-3.page";
import CalculatedSummary4Page from "../../../generated_pages/grand_calculated_summary_multiple_sections/calculated-summary-4.page";
import GrandCalculatedSummary1Page from "../../../generated_pages/grand_calculated_summary_multiple_sections/grand-calculated-summary-1.page";
import GrandCalculatedSummary2Page from "../../../generated_pages/grand_calculated_summary_multiple_sections/grand-calculated-summary-2.page";
import Section1SummaryPage from "../../../generated_pages/grand_calculated_summary_multiple_sections/section-1-summary.page";

describe("Feature: Grand Calculated Summary", () => {
  describe("Given I have a Grand Calculated Summary across multiple sections", () => {
    before("Reaching the grand calculated summary section", async () => {
      await browser.openQuestionnaire("test_grand_calculated_summary_multiple_sections.json");
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
        "Grand Calculated Summary for section 1 and 2 is calculated to be £415.00. Is this correct?"
      );
      await $(GrandCalculatedSummary2Page.calculatedSummary1Edit()).click();
      await expect(await browser.getUrl()).to.contain(CalculatedSummary1Page.pageName);

      await $(CalculatedSummary1Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary2Page.pageName);
    });

    it("Given I go back to the calculated summary and then to a question and edit the answer. I am first taken back to the each calculated summary that uses the answer, the grand calculated summary in section 1, and then the updated grand calculated summary in section 3.", async () => {
      await $(GrandCalculatedSummary2Page.calculatedSummary4Edit()).click();
      await expect(await $(CalculatedSummary4Page.calculatedSummaryTitle()).getText()).to.contain(
        "Calculated Summary for Question 4 is calculated to be £15.00. Is this correct?"
      );
      await $(CalculatedSummary4Page.q4A1Edit()).click();
      await expect(await browser.getUrl()).to.contain(Block4Page.pageName);

      await $(Block4Page.q4A1()).setValue(50);
      await $(Block4Page.submit()).click();

      // first taken back to the calculated summary which has updated
      await expect(await browser.getUrl()).to.contain(CalculatedSummary4Page.pageName);
      await expect(await $(CalculatedSummary4Page.calculatedSummaryTitle()).getText()).to.contain(
        "Calculated Summary for Question 4 is calculated to be £60.00. Is this correct?"
      );
      await $(CalculatedSummary4Page.submit()).click();

      // then taken back to the grand calculated summary which has also been updated correctly
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary2Page.pageName);
      await expect(await $(GrandCalculatedSummary2Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for section 1 and 2 is calculated to be £460.00. Is this correct?"
      );
    });

    it("Given I go back to another calculated summary and edit multiple answers, I am still correctly routed back to the grand calculated summary", async () => {
      await $(GrandCalculatedSummary2Page.calculatedSummary1Edit()).click();
      await expect(await $(CalculatedSummary1Page.calculatedSummaryTitle()).getText()).to.contain(
        "Calculated Summary for Question 1 is calculated to be £100.00. Is this correct?"
      );

      // change first answer
      await $(CalculatedSummary1Page.q1A1Edit()).click();
      await expect(await browser.getUrl()).to.contain(Block1Page.pageName);
      await $(Block1Page.q1A1()).setValue(100);
      await $(Block1Page.submit()).click();

      // go to each calculated summary that uses the answer in turn, then each grand calculated summary up to the one we were editing
      await expect(await browser.getUrl()).to.contain(CalculatedSummary1Page.pageName);
      await expect(await $(CalculatedSummary1Page.calculatedSummaryTitle()).getText()).to.contain(
        "Calculated Summary for Question 1 is calculated to be £190.00. Is this correct?"
      );

      // change another answer
      await $(CalculatedSummary1Page.q2A2Edit()).click();
      await expect(await browser.getUrl()).to.contain(Block2Page.pageName);
      await $(Block2Page.q2A2()).setValue(400);
      await $(Block2Page.submit()).click();

      // back at updated calculated summary
      await expect(await $(CalculatedSummary1Page.calculatedSummaryTitle()).getText()).to.contain(
        "Calculated Summary for Question 1 is calculated to be £550.00. Is this correct?"
      );

      // Go to each calculated/grand calculated summary including this answer and reconfirm before being taken back to grand calculated summary
      await $(CalculatedSummary1Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(CalculatedSummary3Page.pageName);
      await $(CalculatedSummary3Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary1Page.pageName);
      await $(GrandCalculatedSummary1Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(GrandCalculatedSummary2Page.pageName);
      await expect(await $(GrandCalculatedSummary2Page.grandCalculatedSummaryTitle()).getText()).to.contain(
        "Grand Calculated Summary for section 1 and 2 is calculated to be £910.00. Is this correct?"
      );
    });

    it("Given I edit an answer included in a grand calculated summary, both the calculated and grand calculated summary sections should return to partially completed.", async () => {
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
      // TODO: grand calculated summary should not show, but this requires progress source, until this is implemented, it should at least show as in progress
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
  });
});
