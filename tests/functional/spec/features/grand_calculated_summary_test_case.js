import SkipFirstBlockPage from "../../generated_pages/grand_calculated_summary_cross_section_dependencies/skip-first-block.page";
import SecondNumberBlockPage from "../../generated_pages/grand_calculated_summary_cross_section_dependencies/second-number-block.page";
import HubPage from "../../base_pages/hub.page";
import CurrencySection1Page from "../../generated_pages/grand_calculated_summary_cross_section_dependencies/currency-section-1.page";
import QuestionsSectionSummaryPage from "../../generated_pages/grand_calculated_summary_cross_section_dependencies/questions-section-summary.page";
import ThirdNumberBlockPage from "../../generated_pages/grand_calculated_summary_cross_section_dependencies/third-number-block.page";
import SkipCalculatedSummaryPage from "../../generated_pages/grand_calculated_summary_cross_section_dependencies/skip-calculated-summary.page";
import CalculatedSummarySectionSummaryPage
  from "../../generated_pages/grand_calculated_summary_cross_section_dependencies/calculated-summary-section-summary.page";
import CurrencyQuestion3Page from "../../generated_pages/grand_calculated_summary_cross_section_dependencies/currency-question-3.page";
import CurrencyAllPage from "../../generated_pages/grand_calculated_summary_cross_section_dependencies/currency-all.page";
import ResponseAny from "../../generated_pages/conditional_combined_routing/response-any.page";
import FirstNumberBlockPartAPage from "../../generated_pages/grand_calculated_summary_cross_section_dependencies/first-number-block-part-a.page";
import FirstNumberBlockPartBPage from "../../generated_pages/grand_calculated_summary_cross_section_dependencies/first-number-block-part-b.page";

class TestCase {
  testCrossSectionDependencies(schema) {
    before("Get to the second calculated summary", async () => {
      await browser.openQuestionnaire(schema);
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
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).to.contain("The grand calculated summary is calculated to be £400.00. Is this correct?");
    });
    it("Given I go back and skip the second calculated summary, it is not included in the grand calculated summary", async () => {
      await $(ResponseAny.previous()).click();
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(CalculatedSummarySectionSummaryPage.skipAnswer2Edit()).click();
      await $(SkipCalculatedSummaryPage.yes()).click();
      await $(SkipCalculatedSummaryPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();
      await $(HubPage.submit()).click();
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).to.contain("The grand calculated summary is calculated to be £330.00. Is this correct?");
      await expect(await $(CurrencyAllPage.currencyQuestion3()).isExisting()).to.be.false;
    });
    it("Given I go back to section one and skip the first block, it is not included in the first calculated summary and consequently not included in the grand calculated summary", async () => {
      await $(ResponseAny.previous()).click();
      await $(HubPage.summaryRowLink("questions-section")).click();
      await $(QuestionsSectionSummaryPage.skipAnswer1Edit()).click();
      await $(SkipFirstBlockPage.yes()).click();
      await $(SkipFirstBlockPage.submit()).click();
      await $(QuestionsSectionSummaryPage.submit()).click();
      await $(HubPage.summaryRowLink("grand-calculated-summary-section")).click();
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).to.contain("The grand calculated summary is calculated to be £30.00. Is this correct?");
      await expect(await $(CurrencyAllPage.currencyQuestion3()).isExisting()).to.be.false;
    });
  }
}

export const GrandCalculatedSummaryTestCase = new TestCase();
