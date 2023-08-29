import CalculatedSummarySectionSummaryPage from "../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/calculated-summary-section-summary.page";
import CurrencyTotalPlaybackPage from "../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/currency-total-playback.page";
import DependentQuestionSectionSummaryPage from "../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/dependent-question-section-summary.page";
import FirstQuestionBlockPage from "../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/first-question-block.page";
import FruitPage from "../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/fruit.page";
import SecondQuestionBlockPage from "../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/second-question-block.page";
import VegetablesPage from "../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/vegetables.page";
import SkipQuestionPage from "../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/skip-butter-block.page";
import ButterPage from "../generated_pages/routing_and_skipping_section_dependencies_calculated_summary/butter-block.page";

import HubPage from "../base_pages/hub.page";

describe("Routing and skipping section dependencies based on calculated summaries", () => {
  describe("Given the section dependencies based on a calculated summary questionnaire", () => {
    beforeEach("Load the survey", async () => {
      await browser.openQuestionnaire("test_routing_and_skipping_section_dependencies_calculated_summary.json");
    });

    it("When the calculated summary total has not been set, Then the dependent section should not be enabled", async () => {
      await expect(await $(HubPage.summaryRowLink("calculated-summary-section")).isExisting()).to.be.true;
      await expect(await $(HubPage.summaryRowLink("dependent-question-section")).isExisting()).to.be.true;
      await expect(await $(HubPage.summaryRowLink("dependent-enabled-section")).isExisting()).to.be.false;
    });

    it("When the calculated summary total is equal to £100, Then the dependent section should be enabled", async () => {
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(FirstQuestionBlockPage.milk()).setValue(25);
      await $(FirstQuestionBlockPage.eggs()).setValue(25);
      await $(FirstQuestionBlockPage.bread()).setValue(25);
      await $(FirstQuestionBlockPage.cheese()).setValue(25);
      await $(FirstQuestionBlockPage.submit()).click();
      await $(SkipQuestionPage.yes()).click();
      await $(SkipQuestionPage.submit()).click();
      await $(CurrencyTotalPlaybackPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();

      await expect(await $(HubPage.summaryRowLink("calculated-summary-section")).isExisting()).to.be.true;
      await expect(await $(HubPage.summaryRowLink("dependent-question-section")).isExisting()).to.be.true;
      await expect(await $(HubPage.summaryRowLink("dependent-enabled-section")).isExisting()).to.be.true;
    });

    it("When a question in another section has a skip condition dependency on a calculated summary total, and the skip condition is not met (total less than £10), then the dependent question should be displayed", async () => {
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(FirstQuestionBlockPage.milk()).setValue(1);
      await $(FirstQuestionBlockPage.eggs()).setValue(1);
      await $(FirstQuestionBlockPage.bread()).setValue(1);
      await $(FirstQuestionBlockPage.cheese()).setValue(1);
      await $(FirstQuestionBlockPage.submit()).click();
      await $(SkipQuestionPage.yes()).click();
      await $(SkipQuestionPage.submit()).click();
      await $(CurrencyTotalPlaybackPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();

      await $(HubPage.summaryRowLink("dependent-question-section")).click();
      await expect(await browser.getUrl()).to.contain(FruitPage.pageName);
    });

    it("When a question in another section has a skip condition dependency on a calculated summary total, and the skip condition is met (total greater than £10), then the dependent question should not be displayed", async () => {
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(FirstQuestionBlockPage.milk()).setValue(5);
      await $(FirstQuestionBlockPage.eggs()).setValue(5);
      await $(FirstQuestionBlockPage.bread()).setValue(5);
      await $(FirstQuestionBlockPage.cheese()).setValue(5);
      await $(FirstQuestionBlockPage.submit()).click();
      await $(SkipQuestionPage.yes()).click();
      await $(SkipQuestionPage.submit()).click();
      await $(CurrencyTotalPlaybackPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();

      await $(HubPage.summaryRowLink("dependent-question-section")).click();
      await expect(await browser.getUrl()).to.contain(VegetablesPage.pageName);
    });

    it("When a question in another section has a routing rule dependency on a calculated summary total, and the calculated summary total is greater than £100, then we should be routed to the second question block", async () => {
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(FirstQuestionBlockPage.milk()).setValue(30);
      await $(FirstQuestionBlockPage.eggs()).setValue(30);
      await $(FirstQuestionBlockPage.bread()).setValue(30);
      await $(FirstQuestionBlockPage.cheese()).setValue(30);
      await $(FirstQuestionBlockPage.submit()).click();
      await $(SkipQuestionPage.yes()).click();
      await $(SkipQuestionPage.submit()).click();
      await $(CurrencyTotalPlaybackPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();

      await $(HubPage.summaryRowLink("dependent-question-section")).click();
      await $(VegetablesPage.yes()).click();
      await $(VegetablesPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(SecondQuestionBlockPage.pageName);
    });

    it("When a question in another section has a routing rule dependency on a calculated summary total, and the calculated summary total is less than £100, then we should be routed to the section summary", async () => {
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(FirstQuestionBlockPage.milk()).setValue(20);
      await $(FirstQuestionBlockPage.eggs()).setValue(20);
      await $(FirstQuestionBlockPage.bread()).setValue(20);
      await $(FirstQuestionBlockPage.cheese()).setValue(20);
      await $(FirstQuestionBlockPage.submit()).click();
      await $(SkipQuestionPage.yes()).click();
      await $(SkipQuestionPage.submit()).click();
      await $(CurrencyTotalPlaybackPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();

      await $(HubPage.summaryRowLink("dependent-question-section")).click();
      await $(VegetablesPage.yes()).click();
      await $(VegetablesPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(DependentQuestionSectionSummaryPage.pageName);
    });

    it("When a question in another section has a dependency on a calculated summary total, and both sections are complete, and I go back and edit the calculated summary total, then the dependent section status should be in progress", async () => {
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(FirstQuestionBlockPage.milk()).setValue(20);
      await $(FirstQuestionBlockPage.eggs()).setValue(20);
      await $(FirstQuestionBlockPage.bread()).setValue(20);
      await $(FirstQuestionBlockPage.cheese()).setValue(20);
      await $(FirstQuestionBlockPage.submit()).click();
      await $(SkipQuestionPage.yes()).click();
      await $(SkipQuestionPage.submit()).click();
      await $(CurrencyTotalPlaybackPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();

      await $(HubPage.summaryRowLink("dependent-question-section")).click();
      await $(VegetablesPage.yes()).click();
      await $(VegetablesPage.submit()).click();
      await $(DependentQuestionSectionSummaryPage.submit()).click();
      await expect(await $(HubPage.summaryRowState("dependent-question-section")).getText()).to.equal("Completed");

      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(CurrencyTotalPlaybackPage.milkAnswerEdit()).click();
      await $(FirstQuestionBlockPage.milk()).setValue(100);
      await $(FirstQuestionBlockPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(CurrencyTotalPlaybackPage.pageName);
      await $(CurrencyTotalPlaybackPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();
      await expect(await $(HubPage.summaryRowState("dependent-question-section")).getText()).to.equal("Partially completed");
    });

    it("When the calculated summary total is less than £100 but additional answers on the path are opened up as a result of editing an answer, Then the dependent section should be enabled", async () => {
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(FirstQuestionBlockPage.milk()).setValue(10);
      await $(FirstQuestionBlockPage.eggs()).setValue(10);
      await $(FirstQuestionBlockPage.bread()).setValue(10);
      await $(FirstQuestionBlockPage.cheese()).setValue(10);
      await $(FirstQuestionBlockPage.submit()).click();
      await $(SkipQuestionPage.yes()).click();
      await $(SkipQuestionPage.submit()).click();
      await $(CurrencyTotalPlaybackPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();

      await expect(await $(HubPage.summaryRowLink("calculated-summary-section")).isExisting()).to.be.true;
      await expect(await $(HubPage.summaryRowLink("dependent-question-section")).isExisting()).to.be.true;
      await expect(await $(HubPage.summaryRowLink("dependent-enabled-section")).isExisting()).to.be.false;

      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(CalculatedSummarySectionSummaryPage.skipButterBlockAnswerEdit()).click();
      await $(SkipQuestionPage.no()).click();
      await $(SkipQuestionPage.submit()).click();
      await $(ButterPage.butter()).setValue(60);
      await $(ButterPage.submit()).click();
      await $(CurrencyTotalPlaybackPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();

      await expect(await $(HubPage.summaryRowLink("calculated-summary-section")).isExisting()).to.be.true;
      await expect(await $(HubPage.summaryRowLink("dependent-question-section")).isExisting()).to.be.true;
      await expect(await $(HubPage.summaryRowLink("dependent-enabled-section")).isExisting()).to.be.true;
    });

    it("When the calculated summary total is equal to £100 but answers on the path are remove as a result of an answer edit, Then the dependent section should be enabled", async () => {
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(FirstQuestionBlockPage.milk()).setValue(10);
      await $(FirstQuestionBlockPage.eggs()).setValue(10);
      await $(FirstQuestionBlockPage.bread()).setValue(10);
      await $(FirstQuestionBlockPage.cheese()).setValue(10);
      await $(FirstQuestionBlockPage.submit()).click();
      await $(SkipQuestionPage.no()).click();
      await $(SkipQuestionPage.submit()).click();
      await $(ButterPage.butter()).setValue(60);
      await $(ButterPage.submit()).click();
      await $(CurrencyTotalPlaybackPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();

      await expect(await $(HubPage.summaryRowLink("calculated-summary-section")).isExisting()).to.be.true;
      await expect(await $(HubPage.summaryRowLink("dependent-question-section")).isExisting()).to.be.true;
      await expect(await $(HubPage.summaryRowLink("dependent-enabled-section")).isExisting()).to.be.true;

      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await $(CalculatedSummarySectionSummaryPage.skipButterBlockAnswerEdit()).click();
      await $(SkipQuestionPage.yes()).click();
      await $(SkipQuestionPage.submit()).click();
      await $(CalculatedSummarySectionSummaryPage.submit()).click();

      await expect(await $(HubPage.summaryRowLink("calculated-summary-section")).isExisting()).to.be.true;
      await expect(await $(HubPage.summaryRowLink("dependent-question-section")).isExisting()).to.be.true;
      await expect(await $(HubPage.summaryRowLink("dependent-enabled-section")).isExisting()).to.be.false;
    });
  });
});
