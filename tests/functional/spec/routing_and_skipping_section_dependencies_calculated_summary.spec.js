import CalculatedSummarySectionSummaryPage from "../generated_pages/new_routing_section_dependencies_calculated_summary/calculated-summary-section-summary.page";
import CurrencyTotalPlaybackPage from "../generated_pages/new_routing_section_dependencies_calculated_summary/currency-total-playback.page";
import DependentQuestionSectionSummaryPage from "../generated_pages/new_routing_section_dependencies_calculated_summary/dependent-question-section-summary.page";
import FirstQuestionBlockPage from "../generated_pages/new_routing_section_dependencies_calculated_summary/first-question-block.page";
import FruitPage from "../generated_pages/new_routing_section_dependencies_calculated_summary/fruit.page";
import SecondQuestionBlockPage from "../generated_pages/new_routing_section_dependencies_calculated_summary/second-question-block.page";
import VegetablesPage from "../generated_pages/new_routing_section_dependencies_calculated_summary/vegetables.page";

import HubPage from "../base_pages/hub.page";

describe("Routing and skipping section dependencies based on calculated summaries", () => {
  describe("Given the section dependencies based on a calculated summary questionnaire", () => {
    beforeEach("Load the survey", () => {
      browser.openQuestionnaire("test_new_routing_section_dependencies_calculated_summary.json");
    });

    it("When the calculated summary total has not been set, Then the dependent section should not be enabled", () => {
      expect($(HubPage.summaryRowLink("calculated-summary-section")).isExisting()).to.be.true;
      expect($(HubPage.summaryRowLink("dependent-question-section")).isExisting()).to.be.true;
      expect($(HubPage.summaryRowLink("dependent-enabled-section")).isExisting()).to.be.false;
    });

    it("When the calculated summary total is equal to £100, Then the dependent section should be enabled", () => {
      $(HubPage.summaryRowLink("calculated-summary-section")).click();
      $(FirstQuestionBlockPage.milk()).setValue(25);
      $(FirstQuestionBlockPage.eggs()).setValue(25);
      $(FirstQuestionBlockPage.bread()).setValue(25);
      $(FirstQuestionBlockPage.cheese()).setValue(25);
      $(FirstQuestionBlockPage.submit()).click();
      $(CurrencyTotalPlaybackPage.submit()).click();
      $(CalculatedSummarySectionSummaryPage.submit()).click();

      expect($(HubPage.summaryRowLink("calculated-summary-section")).isExisting()).to.be.true;
      expect($(HubPage.summaryRowLink("dependent-question-section")).isExisting()).to.be.true;
      expect($(HubPage.summaryRowLink("dependent-enabled-section")).isExisting()).to.be.true;
    });

    it("When a question in another section has a skip condition dependency on a calculated summary total, and the skip condition is not met (total less than £10), then the dependent question should be displayed", () => {
      $(HubPage.summaryRowLink("calculated-summary-section")).click();
      $(FirstQuestionBlockPage.milk()).setValue(1);
      $(FirstQuestionBlockPage.eggs()).setValue(1);
      $(FirstQuestionBlockPage.bread()).setValue(1);
      $(FirstQuestionBlockPage.cheese()).setValue(1);
      $(FirstQuestionBlockPage.submit()).click();
      $(CurrencyTotalPlaybackPage.submit()).click();
      $(CalculatedSummarySectionSummaryPage.submit()).click();

      $(HubPage.summaryRowLink("dependent-question-section")).click();
      expect(browser.getUrl()).to.contain(FruitPage.pageName);
    });

    it("When a question in another section has a skip condition dependency on a calculated summary total, and the skip condition is met (total greater than £10), then the dependent question should not be displayed", () => {
      $(HubPage.summaryRowLink("calculated-summary-section")).click();
      $(FirstQuestionBlockPage.milk()).setValue(5);
      $(FirstQuestionBlockPage.eggs()).setValue(5);
      $(FirstQuestionBlockPage.bread()).setValue(5);
      $(FirstQuestionBlockPage.cheese()).setValue(5);
      $(FirstQuestionBlockPage.submit()).click();
      $(CurrencyTotalPlaybackPage.submit()).click();
      $(CalculatedSummarySectionSummaryPage.submit()).click();

      $(HubPage.summaryRowLink("dependent-question-section")).click();
      expect(browser.getUrl()).to.contain(VegetablesPage.pageName);
    });

    it("When a question in another section has a routing rule dependency on a calculated summary total, and the calculated summary total is greater than £100, then we should be routed to the second question block", () => {
      $(HubPage.summaryRowLink("calculated-summary-section")).click();
      $(FirstQuestionBlockPage.milk()).setValue(30);
      $(FirstQuestionBlockPage.eggs()).setValue(30);
      $(FirstQuestionBlockPage.bread()).setValue(30);
      $(FirstQuestionBlockPage.cheese()).setValue(30);
      $(FirstQuestionBlockPage.submit()).click();
      $(CurrencyTotalPlaybackPage.submit()).click();
      $(CalculatedSummarySectionSummaryPage.submit()).click();

      $(HubPage.summaryRowLink("dependent-question-section")).click();
      $(VegetablesPage.yes()).click();
      $(VegetablesPage.submit()).click();
      expect(browser.getUrl()).to.contain(SecondQuestionBlockPage.pageName);
    });

    it("When a question in another section has a routing rule dependency on a calculated summary total, and the calculated summary total is less than £100, then we should be routed to the section summary", () => {
      $(HubPage.summaryRowLink("calculated-summary-section")).click();
      $(FirstQuestionBlockPage.milk()).setValue(20);
      $(FirstQuestionBlockPage.eggs()).setValue(20);
      $(FirstQuestionBlockPage.bread()).setValue(20);
      $(FirstQuestionBlockPage.cheese()).setValue(20);
      $(FirstQuestionBlockPage.submit()).click();
      $(CurrencyTotalPlaybackPage.submit()).click();
      $(CalculatedSummarySectionSummaryPage.submit()).click();

      $(HubPage.summaryRowLink("dependent-question-section")).click();
      $(VegetablesPage.yes()).click();
      $(VegetablesPage.submit()).click();
      expect(browser.getUrl()).to.contain(DependentQuestionSectionSummaryPage.pageName);
    });

    it("When a question in another section has a dependency on a calculated summary total, and both sections are complete, and I go back and edit the calculated summary total, then the dependent section status should be in progress", () => {
      $(HubPage.summaryRowLink("calculated-summary-section")).click();
      $(FirstQuestionBlockPage.milk()).setValue(20);
      $(FirstQuestionBlockPage.eggs()).setValue(20);
      $(FirstQuestionBlockPage.bread()).setValue(20);
      $(FirstQuestionBlockPage.cheese()).setValue(20);
      $(FirstQuestionBlockPage.submit()).click();
      $(CurrencyTotalPlaybackPage.submit()).click();
      $(CalculatedSummarySectionSummaryPage.submit()).click();

      $(HubPage.summaryRowLink("dependent-question-section")).click();
      $(VegetablesPage.yes()).click();
      $(VegetablesPage.submit()).click();
      $(DependentQuestionSectionSummaryPage.submit()).click();
      expect($(HubPage.summaryRowState("dependent-question-section")).getText()).to.equal("Completed");

      $(HubPage.summaryRowLink("calculated-summary-section")).click();
      $(CurrencyTotalPlaybackPage.milkAnswerEdit()).click();
      $(FirstQuestionBlockPage.milk()).setValue(100);
      $(FirstQuestionBlockPage.submit()).click();
      $(CurrencyTotalPlaybackPage.submit()).click();
      $(CalculatedSummarySectionSummaryPage.submit()).click();
      expect($(HubPage.summaryRowState("dependent-question-section")).getText()).to.equal("Partially completed");
    });
  });
});
