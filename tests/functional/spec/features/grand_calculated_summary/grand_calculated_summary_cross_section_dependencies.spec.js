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
import FirstNumberBlockPartAPage from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/first-number-block-part-a.page";
import FourthNumberBlockPage from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/fourth-number-block.page";
import tvChoiceBlockPage from "../../../generated_pages/grand_calculated_summary_cross_section_dependencies/tv-choice-block.page";
import { click } from "../../../helpers";
import { expect } from "@wdio/globals";

describe("Feature: Grand Calculated Summary", () => {
  describe("Given I have a Grand Calculated Summary", () => {
    before("Getting to the second calculated summary", async () => {
      await browser.openQuestionnaire("test_grand_calculated_summary_cross_section_dependencies.json");
      await click(HubPage.submit());
      await $(SkipFirstBlockPage.no()).click();
      await click(SkipFirstBlockPage.submit());
      await $(FirstNumberBlockPartAPage.firstNumberA()).setValue(300);
      await click(FirstNumberBlockPartAPage.submit());
      await $(SecondNumberBlockPage.secondNumberA()).setValue(10);
      await $(SecondNumberBlockPage.secondNumberB()).setValue(5);
      await $(SecondNumberBlockPage.secondNumberC()).setValue(15);
      await click(SecondNumberBlockPage.submit());
      await click(CurrencySection1Page.submit());
      await click(QuestionsSectionSummaryPage.submit());
      // section 2
      await click(HubPage.submit());
      await $(ThirdNumberBlockPage.thirdNumberPartA()).setValue(70);
      await click(ThirdNumberBlockPage.submit());
    });
    it("Given I don't skip the second calculated summary, it is included in the grand calculated summary", async () => {
      await $(SkipCalculatedSummaryPage.no()).click();
      await click(SkipCalculatedSummaryPage.submit());
      await click(CurrencyQuestion3Page.submit());
      await $(tvChoiceBlockPage.television()).click();
      await click(tvChoiceBlockPage.submit());
      await click(CalculatedSummarySectionSummaryPage.submit());
      await click(HubPage.submit());
      await expect(await $(CurrencyAllPage.currencySection1()).getText()).toBe("£330.00");
      await expect(await $(CurrencyAllPage.currencyQuestion3()).getText()).toBe("£70.00");
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).toBe(
        "The grand calculated summary is calculated to be £400.00. Is this correct?",
      );
      await click(CurrencyAllPage.submit());
    });
    it("Given I go back and skip the second calculated summary, it is not included in the grand calculated summary", async () => {
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(CalculatedSummarySectionSummaryPage.skipAnswer2Edit()).click();
      await $(SkipCalculatedSummaryPage.yes()).click();
      await click(SkipCalculatedSummaryPage.submit());
      await click(CalculatedSummarySectionSummaryPage.submit());
      // Currently the grand calculated summary remains 'Completed' because none of the answers have changed
      await expect(await $(HubPage.summaryRowState("grand-calculated-summary-section")).getText()).toBe("Completed");
      await $(HubPage.summaryRowLink("grand-calculated-summary-section")).click();
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).toBe(
        "The grand calculated summary is calculated to be £330.00. Is this correct?",
      );
      await expect(await $(CurrencyAllPage.currencyQuestion3()).isExisting()).toBe(false);
    });
    it("Given I confirm the grand calculated summary, then edit an answer for question 3, the grand calculated summary updates to be incomplete, because this is a dependency", async () => {
      await click(CurrencyAllPage.submit());
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(CalculatedSummarySectionSummaryPage.thirdNumberAnswerPartAEdit()).click();
      await $(ThirdNumberBlockPage.thirdNumberPartA()).setValue(130);
      await click(ThirdNumberBlockPage.submit());
      await click(CalculatedSummarySectionSummaryPage.submit());
      // Although the calculated summary is not on the path, the answer is still a grand calculated summary dependency, so it updates progress
      await expect(await $(HubPage.summaryRowState("grand-calculated-summary-section")).getText()).toBe("Partially completed");
      await $(HubPage.summaryRowLink("grand-calculated-summary-section")).click();
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).toBe(
        "The grand calculated summary is calculated to be £330.00. Is this correct?",
      );
      await expect(await $(CurrencyAllPage.currencyQuestion3()).isExisting()).toBe(false);
      await click(CurrencyAllPage.submit());
    });
    it("Given I change my response to include the calculated summary, When I press continue, Then I am routed to the new block that opens up", async () => {
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(CalculatedSummarySectionSummaryPage.skipAnswer2Edit()).click();
      await $(SkipCalculatedSummaryPage.no()).click();
      await click(SkipCalculatedSummaryPage.submit());
      await expect(browser).toHaveUrlContaining(CurrencyQuestion3Page.pageName);
    });
    it("Given I confirm the calculated summary and the blocks following it are already complete, When I press submit, Then I am returned to the section summary anchored to the answer I edited initially", async () => {
      await click(CurrencyQuestion3Page.submit());
      await expect(browser).toHaveUrlContaining("calculated-summary-section/#skip-answer-2");
    });
    it("Given I change an answer, When I press previous from the now incomplete calculated summary, Then I am routed to the block before the calculated summary", async () => {
      await $(CalculatedSummarySectionSummaryPage.thirdNumberAnswerPartAEdit()).click();
      await $(ThirdNumberBlockPage.thirdNumberPartA()).setValue(120);
      await click(ThirdNumberBlockPage.submit());
      await expect(browser).toHaveUrlContaining(CurrencyQuestion3Page.pageName);
      await $(CurrencyQuestion3Page.previous()).click();
      await expect(browser).toHaveUrlContaining(SkipCalculatedSummaryPage.pageName);
    });
    it("Given I complete the section, When I go back to the grand calculated summary, Then I see the new calculated summary included", async () => {
      await click(SkipCalculatedSummaryPage.submit());
      await click(CurrencyQuestion3Page.submit());
      await click(CalculatedSummarySectionSummaryPage.submit());
      await expect(await $(HubPage.summaryRowState("grand-calculated-summary-section")).getText()).toBe("Partially completed");
      await $(HubPage.summaryRowLink("grand-calculated-summary-section")).click();
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).toBe(
        "The grand calculated summary is calculated to be £450.00. Is this correct?",
      );
    });
    it("Given I provide an answer to question 3b from the grand calculated summary, this opens up an additional question, and when I press continue I am taken to this question first, then the calculated summary, and then the grand calculated summary", async () => {
      await $(CurrencyAllPage.currencyQuestion3Edit()).click();
      await $(CurrencyQuestion3Page.thirdNumberAnswerPartBEdit()).click();
      await $(ThirdNumberBlockPage.thirdNumberPartB()).setValue(10);
      await click(ThirdNumberBlockPage.submit());
      await expect(browser).toHaveUrlContaining(FourthNumberBlockPage.pageName);
      await $(FourthNumberBlockPage.fourthNumber()).setValue(1);
      await click(FourthNumberBlockPage.submit());
      await expect(browser).toHaveUrlContaining(CurrencyQuestion3Page.pageName);
      await click(CurrencyQuestion3Page.submit());
      await expect(browser).toHaveUrlContaining(CurrencyAllPage.pageName);
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).toBe(
        "The grand calculated summary is calculated to be £461.00. Is this correct?",
      );
      await click(CurrencyAllPage.submit());
    });
    it("Given I go back to section one and skip the first block, it is not included in the first calculated summary and consequently not included in the grand calculated summary", async () => {
      await $(HubPage.summaryRowLink("questions-section")).click();
      await $(QuestionsSectionSummaryPage.skipAnswer1Edit()).click();
      await $(SkipFirstBlockPage.yes()).click();
      await click(SkipFirstBlockPage.submit());
      await click(QuestionsSectionSummaryPage.submit());
      await $(HubPage.summaryRowLink("grand-calculated-summary-section")).click();
      await expect(await $(CurrencyAllPage.currencySection1()).getText()).toBe("£30.00");
      await expect(await $(CurrencyAllPage.grandCalculatedSummaryTitle()).getText()).toBe(
        "The grand calculated summary is calculated to be £161.00. Is this correct?",
      );
    });
  });
});
