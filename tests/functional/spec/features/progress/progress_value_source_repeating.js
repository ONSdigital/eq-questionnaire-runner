import HubPage from "../../../base_pages/hub.page";
import ListCollectorPage from "../../../generated_pages/new_calculated_summary_repeating_section/list-collector.page";
import ListCollectorAddPage from "../../../generated_pages/new_calculated_summary_repeating_section/list-collector-add.page";
import QuestionBlockPage from "../../../generated_pages/progress_value_source_repeating_sections/question-block.page";
import DOBQuestionBlockPage from "../../../generated_pages/progress_value_source_repeating_sections/dob-block.page";
import RandomQuestionEnablerBlockPage from "../../../generated_pages/progress_value_source_repeating_sections/random-question-enabler-block.page";
import SectionTwoSummaryPage from "../../../generated_pages/progress_value_source_repeating_sections/section-2-summary.page";
import OtherQuestionBlockPage from "../../../generated_pages/progress_value_source_repeating_sections/other-question-block.page";

describe("Feature: Routing rules based on progress value sources in repeating sections", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_progress_value_source_repeating_sections.json");
  });

  describe("Given I have routing in a repeating section based on the completeness of a block", () => {
    it("When the block is incomplete, then I should not see the dependent question in the repeating section", async () => {
      await $(HubPage.submit()).click();
      await $(ListCollectorPage.yes()).click();
      await $(ListCollectorPage.submit()).click();
      await $(ListCollectorAddPage.firstName()).setValue("John");
      await $(ListCollectorAddPage.lastName()).setValue("Doe");
      await $(ListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(QuestionBlockPage.pageName);

      await browser.url(HubPage.url());
      await expect(await $(HubPage.summaryRowState("section-1")).getText()).to.equal("Partially completed");

      await $(HubPage.summaryRowLink("section-2-1")).click();
      await $(DOBQuestionBlockPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(SectionTwoSummaryPage.pageName);
    });
  });

  describe("Given I have routing in a repeating section based on the completeness of a block", () => {
    it("When the block is complete, then I should see the dependent question in the repeating section", async () => {
      await $(HubPage.submit()).click();
      await $(ListCollectorPage.yes()).click();
      await $(ListCollectorPage.submit()).click();
      await $(ListCollectorAddPage.firstName()).setValue("John");
      await $(ListCollectorAddPage.lastName()).setValue("Doe");
      await $(ListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();
      await $(QuestionBlockPage.submit()).click();
      await $(RandomQuestionEnablerBlockPage.randomQuestionEnabler()).setValue(1);
      await $(RandomQuestionEnablerBlockPage.submit()).click();

      await browser.url(HubPage.url());
      await expect(await $(HubPage.summaryRowState("section-1")).getText()).to.equal("Completed");

      await $(HubPage.summaryRowLink("section-2-1")).click();
      await $(DOBQuestionBlockPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(OtherQuestionBlockPage.pageName);
    });
  });
});
