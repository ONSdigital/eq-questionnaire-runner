import HubPage from "../../../base_pages/hub.page";
import ListCollectorPage from "../../../generated_pages/new_calculated_summary_repeating_section/list-collector.page";
import ListCollectorAddPage from "../../../generated_pages/new_calculated_summary_repeating_section/list-collector-add.page";
import QuestionBlockPage from "../../../generated_pages/progress_block_value_source_repeating_sections/question-block.page";
import DOBQuestionBlockPage from "../../../generated_pages/progress_block_value_source_repeating_sections/dob-block.page";
import RandomQuestionEnablerBlockPage from "../../../generated_pages/progress_block_value_source_repeating_sections/random-question-enabler-block.page";
import SectionTwoSummaryPage from "../../../generated_pages/progress_block_value_source_repeating_sections/section-2-summary.page";
import SectionThreeSummaryPage from "../../../generated_pages/progress_value_source_calculated_summary/section-3-summary.page";
import OtherQuestionBlockPage from "../../../generated_pages/progress_block_value_source_repeating_sections/other-question-block.page";
import FirstNumberBlockPage from "../../../generated_pages/progress_value_source_calculated_summary/first-number-block.page";
import SecondNumberBlockPage from "../../../generated_pages/progress_value_source_calculated_summary/second-number-block.page";
import SectionTwoQuestionBlockPage from "../../../generated_pages/progress_value_source_calculated_summary/s2-b1.page";
import CalculatedSummaryBlockPage from "../../../generated_pages/progress_value_source_calculated_summary/calculated-summary-block.page";
import { click } from "../../../helpers";
describe("Feature: Routing rules based on progress value sources in repeating sections", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_progress_block_value_source_repeating_sections.json");
  });

  describe("Given I have routing in a repeating section based on the completeness of a block", () => {
    it("When the block is incomplete, then I should not see the dependent question in the repeating section", async () => {
      await click(HubPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("John");
      await $(ListCollectorAddPage.lastName()).setValue("Doe");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await expect(await browser.getUrl()).to.contain(QuestionBlockPage.pageName);

      await browser.url(HubPage.url());
      await expect(await $(HubPage.summaryRowState("section-1")).getText()).to.equal("Partially completed");

      await $(HubPage.summaryRowLink("section-2-1")).click();
      await click(DOBQuestionBlockPage.submit());
      await expect(await browser.getUrl()).to.contain(SectionTwoSummaryPage.pageName);
    });
  });

  describe("Given I have routing in a repeating section based on the completeness of a block", () => {
    it("When the block is complete, then I should see the dependent question in the repeating section", async () => {
      await click(HubPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("John");
      await $(ListCollectorAddPage.lastName()).setValue("Doe");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await click(QuestionBlockPage.submit());
      await $(RandomQuestionEnablerBlockPage.randomQuestionEnabler()).setValue(1);
      await click(RandomQuestionEnablerBlockPage.submit());

      await browser.url(HubPage.url());
      await expect(await $(HubPage.summaryRowState("section-1")).getText()).to.equal("Completed");

      await $(HubPage.summaryRowLink("section-2-1")).click();
      await click(DOBQuestionBlockPage.submit());
      await expect(await browser.getUrl()).to.contain(OtherQuestionBlockPage.pageName);
    });
  });

  describe("Given I have routing in a repeating section based on the completeness of a block", () => {
    it("When the status of the block changes from incomplete to complete, then the dependent question should be on the path in the repeating sections", async () => {
      await click(HubPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("John");
      await $(ListCollectorAddPage.lastName()).setValue("Doe");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Joe");
      await $(ListCollectorAddPage.lastName()).setValue("Bloggs");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await browser.url(HubPage.url());
      await expect(await $(HubPage.summaryRowState("section-2-1")).getText()).to.equal("Not started");
      await expect(await $(HubPage.summaryRowState("section-2-2")).getText()).to.equal("Not started");

      await $(HubPage.summaryRowLink("section-2-1")).click();
      await click(DOBQuestionBlockPage.submit());
      await click(SectionTwoSummaryPage.submit());
      await expect(await $(HubPage.summaryRowState("section-2-1")).getText()).to.equal("Completed");
      await expect(await $(HubPage.summaryRowState("section-2-2")).getText()).to.equal("Not started");

      await click(HubPage.submit());
      await click(QuestionBlockPage.submit());
      await $(RandomQuestionEnablerBlockPage.randomQuestionEnabler()).setValue(1);
      await click(RandomQuestionEnablerBlockPage.submit());

      await expect(await $(HubPage.summaryRowState("section-2-1")).getText()).to.equal("Partially completed");
      await expect(await $(HubPage.summaryRowState("section-2-2")).getText()).to.equal("Not started");
    });
  });
});

describe("Feature: Routing rules based on progress value sources in repeating sections", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_progress_value_source_calculated_summary.json");
  });

  describe("Given I have routing in a repeating section based on the completeness of a calculated summary", () => {
    it("When the calculated summary block is incomplete, then I should not see the dependent question in the repeating section", async () => {
      await click(HubPage.submit());
      await $(FirstNumberBlockPage.firstNumber()).setValue(1);
      await click(FirstNumberBlockPage.submit());
      await browser.url(HubPage.url());

      await $(HubPage.summaryRowLink("section-2")).click();

      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("John");
      await $(ListCollectorAddPage.lastName()).setValue("Doe");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await expect(await browser.getUrl()).to.contain(HubPage.pageName);

      await $(HubPage.summaryRowLink("section-3-1")).click();
      await click(DOBQuestionBlockPage.submit());
      await click(SectionThreeSummaryPage.submit());

      await expect(await $(HubPage.summaryRowState("section-1")).getText()).to.equal("Partially completed");
      await expect(await $(HubPage.summaryRowState("section-2")).getText()).to.equal("Completed");
      await expect(await $(HubPage.summaryRowState("section-3-1")).getText()).to.equal("Completed");
    });
  });

  describe("Given I have routing in a repeating section based on the completeness of a calculated summary", () => {
    it("When the calculated summary block is incomplete but is updated so that it is completed, then I should see the dependency should be updated in the repeating section", async () => {
      await click(HubPage.submit());
      await $(FirstNumberBlockPage.firstNumber()).setValue(1);
      await click(FirstNumberBlockPage.submit());
      await browser.url(HubPage.url());

      await $(HubPage.summaryRowLink("section-2")).click();

      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("John");
      await $(ListCollectorAddPage.lastName()).setValue("Doe");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await expect(await browser.getUrl()).to.contain(HubPage.pageName);

      await $(HubPage.summaryRowLink("section-3-1")).click();
      await click(DOBQuestionBlockPage.submit());
      await click(SectionThreeSummaryPage.submit());

      await expect(await $(HubPage.summaryRowState("section-1")).getText()).to.equal("Partially completed");
      await expect(await $(HubPage.summaryRowState("section-2")).getText()).to.equal("Completed");
      await expect(await $(HubPage.summaryRowState("section-3-1")).getText()).to.equal("Completed");

      await $(HubPage.summaryRowLink("section-1")).click();
      await $(SecondNumberBlockPage.secondNumber()).setValue(2);
      await click(SecondNumberBlockPage.submit());
      await click(CalculatedSummaryBlockPage.submit());
      await browser.url(HubPage.url());

      await expect(await $(HubPage.summaryRowState("section-1")).getText()).to.equal("Completed");
      await expect(await $(HubPage.summaryRowState("section-2")).getText()).to.equal("Partially completed");
      await expect(await $(HubPage.summaryRowState("section-3-1")).getText()).to.equal("Partially completed");
    });
  });

  describe("Given I have routing in a repeating section based on the completeness of a calculated summary", () => {
    it("When the calculated summary block is complete, then I should see the dependent question in the repeating section", async () => {
      await click(HubPage.submit());
      await $(FirstNumberBlockPage.firstNumber()).setValue(1);
      await click(FirstNumberBlockPage.submit());
      await $(SecondNumberBlockPage.secondNumber()).setValue(2);
      await click(SecondNumberBlockPage.submit());
      await click(CalculatedSummaryBlockPage.submit());
      await browser.url(HubPage.url());

      await $(HubPage.summaryRowLink("section-2")).click();

      await $(SectionTwoQuestionBlockPage.q1A1()).setValue(1);
      await click(SectionTwoQuestionBlockPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("John");
      await $(ListCollectorAddPage.lastName()).setValue("Doe");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await expect(await browser.getUrl()).to.contain(HubPage.pageName);

      await $(HubPage.summaryRowLink("section-3-1")).click();
      await click(DOBQuestionBlockPage.submit());
      await expect(await browser.getUrl()).to.contain(OtherQuestionBlockPage.pageName);
    });
  });
});
