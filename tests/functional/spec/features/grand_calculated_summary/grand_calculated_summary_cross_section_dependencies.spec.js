import SkipFirstBlockPage from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/skip-first-block.page";
import SecondNumberBlockPage from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/second-number-block.page";
import HubPage from "../../../base_pages/hub.page";
import CurrencySection1Page from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/currency-section-1.page";
import QuestionsSectionSummaryPage from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/questions-section-summary.page";
import ThirdNumberBlockPage from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/third-number-block.page";
import SkipCalculatedSummaryPage from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/skip-calculated-summary.page";
import CalculatedSummarySectionSummaryPage from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/calculated-summary-section-summary.page";
import CurrencyQuestion3Page from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/currency-question-3.page";
import CurrencyAllPage from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/currency-all.page";
import ResponseAny from "../../../generated_pages/conditional_combined_routing/response-any.page";
import FirstNumberBlockPartAPage from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/first-number-block-part-a.page";
import FirstNumberBlockPartBPage from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/first-number-block-part-b.page";
import FourthNumberBlockPage from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/fourth-number-block.page";

describe("Feature: Grand Calculated Summary", () => {
  describe("Given I have a Grand Calculated Summary", () => {
    before("Getting to the second calculated summary", async () => {
      await browser.openQuestionnaire("test_grand_calculated_summary_cross_section_dependencies.json");
      await $(HubPage.submit()).click();
      await $(SkipFirstBlockPage.no()).click();
      await $(SkipFirstBlockPage.submit()).click();
      await $(FirstNumberBlockPartAPage.firstNumberA()).setValue(100);
      await $(FirstNumberBlockPartAPage.submit()).click();
      await $(FirstNumberBlockPartBPage.firstNumberB()).setValue(200);
      await $(FirstNumberBlockPartBPage.submit()).click();
      await $(SecondNumberBlockPage.secondNumberA()).setValue(10);
      await $(SecondNumberBlockPage.secondNumberB()).setValue(20);
      await $(SecondNumberBlockPage.submit()).click();
      await $(CurrencySection1Page.submit()).click();
      await $(QuestionsSectionSummaryPage.submit()).click();
      // section 2
      await $(HubPage.submit()).click();
      await $(ThirdNumberBlockPage.thirdNumberPartA()).setValue(30);
      await $(ThirdNumberBlockPage.thirdNumberPartB()).setValue(40);
      await $(ThirdNumberBlockPage.submit()).click();
    });
    it("Given I don't skip the second calculated summary, it is included in the grand calculated summary", async () => {
      await $(SkipCalculatedSummaryPage.no()).click();
      await $(SkipCalculatedSummaryPage.submit()).click();
      await $(CurrencyQuestion3Page.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();
      await $(HubPage.submit()).click();
      await expect(await $(CurrencyAllPage.currencySection1()).getText()).to.contain("£330.00");
      await expect(await $(CurrencyAllPage.currencyQuestion3()).getText()).to.contain("£70.00");
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).to.contain(
        "The grand calculated summary is calculated to be £400.00. Is this correct?"
      );
      await $(CurrencyAllPage.submit()).click();
    });
    it("Given I go back and skip the second calculated summary, it is not included in the grand calculated summary, which is updated to be in-progress", async () => {
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(CalculatedSummarySectionSummaryPage.skipAnswer2Edit()).click();
      await $(SkipCalculatedSummaryPage.yes()).click();
      await $(SkipCalculatedSummaryPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();
      // TODO FIX TEST FAILURE
      // await expect(await $(HubPage.summaryRowState("grand-calculated-summary-section")).getText()).to.equal("Partially completed");
      await $(HubPage.summaryRowLink("grand-calculated-summary-section")).click();
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).to.contain(
        "The grand calculated summary is calculated to be £330.00. Is this correct?"
      );
      await expect(await $(CurrencyAllPage.currencyQuestion3()).isExisting()).to.be.false;
    });
    it("Given I confirm the grand calculated summary, then edit an answer for question 3, the grand calculated summary remains completed, because the calculated summary containing question 3 is not on the path", async () => {
      await $(CurrencyAllPage.submit()).click();
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(CalculatedSummarySectionSummaryPage.thirdNumberAnswerPartAEdit()).click();
      await $(ThirdNumberBlockPage.thirdNumberPartA()).setValue(130);
      await $(ThirdNumberBlockPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();
      // TODO FIX TEST FAILURE
      // await expect(await $(HubPage.summaryRowState("grand-calculated-summary-section")).getText()).to.equal("Completed");
      await $(HubPage.summaryRowLink("grand-calculated-summary-section")).click();
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).to.contain(
        "The grand calculated summary is calculated to be £330.00. Is this correct?"
      );
      await expect(await $(CurrencyAllPage.currencyQuestion3()).isExisting()).to.be.false;
      await $(CurrencyAllPage.submit()).click();
    });
    it("Given I change my response to include the calculated summary, the grand calculated summary returns to in progress", async () => {
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(CalculatedSummarySectionSummaryPage.skipAnswer2Edit()).click();
      await $(SkipCalculatedSummaryPage.no()).click();
      await $(SkipCalculatedSummaryPage.submit()).click();
      await $(CurrencyQuestion3Page.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();
      // TODO FIX TEST FAILURE
      // await expect(await $(HubPage.summaryRowState("grand-calculated-summary-section")).getText()).to.equal("Partially completed");
    });
    it("Given I change my answer to question 3 from the grand calculated summary, this opens up an additional question, and when I press continue I am taken to this question first, then the calculated summary, and then the grand calculated summary", async () => {
      await $(HubPage.summaryRowLink("grand-calculated-summary-section")).click();
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).to.contain(
        "The grand calculated summary is calculated to be £500.00. Is this correct?"
      );
      await $(CurrencyAllPage.currencyQuestion3Edit()).click();
      await $(CurrencyQuestion3Page.thirdNumberAnswerPartAEdit()).click();
      await $(ThirdNumberBlockPage.thirdNumberPartA()).setValue(100);
      await $(ThirdNumberBlockPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(FourthNumberBlockPage.pageName);
      await $(FourthNumberBlockPage.fourthNumber()).setValue(1);
      await $(FourthNumberBlockPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(CurrencyQuestion3Page.pageName);
      await $(CurrencyQuestion3Page.submit()).click();
      await expect(await browser.getUrl()).to.contain(CurrencyAllPage.pageName);
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).to.contain(
        "The grand calculated summary is calculated to be £471.00. Is this correct?"
      );
      await $(CurrencyAllPage.submit()).click();
    });
    it("Given I go back to section one and skip the first block, it is not included in the first calculated summary and consequently not included in the grand calculated summary", async () => {
      await $(HubPage.summaryRowLink("questions-section")).click();
      await $(QuestionsSectionSummaryPage.skipAnswer1Edit()).click();
      await $(SkipFirstBlockPage.yes()).click();
      await $(SkipFirstBlockPage.submit()).click();
      await $(QuestionsSectionSummaryPage.submit()).click();
      await $(HubPage.summaryRowLink("grand-calculated-summary-section")).click();
      await expect(await $(CurrencyAllPage.currencySection1()).getText()).to.contain("£30.00");
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).to.contain(
        "The grand calculated summary is calculated to be £171.00. Is this correct?"
      );
    });
  });
});
