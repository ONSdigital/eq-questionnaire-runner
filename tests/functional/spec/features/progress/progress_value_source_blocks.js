import FirstQuestionPage from "../../../generated_pages/progress_value_source_blocks/s1-b1.page";
import SecondQuestionPage from "../../../generated_pages/progress_value_source_blocks/s1-b2.page";
import ThirdQuestionPage from "../../../generated_pages/progress_value_source_blocks/s1-b3.page";
import ThirdQuestionSectionTwoPage from "../../../generated_pages/progress_value_source_section_enabled_no_hub/s2-b1.page";
import FourthQuestionPage from "../../../generated_pages/progress_value_source_blocks/s1-b4.page";
import FifthQuestionPage from "../../../generated_pages/progress_value_source_blocks/s1-b5.page";
import SixthQuestionPage from "../../../generated_pages/progress_value_source_blocks/s1-b6.page";
import SeventhQuestionPage from "../../../generated_pages/progress_value_source_blocks/s1-b7.page";
import SubmitPage from "../../../generated_pages/progress_value_source_blocks/submit.page";
import HubPage from "../../../base_pages/hub.page";
import { click } from "../../../helpers";
describe("Feature: Routing  based on progress value sources using block identifiers", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_progress_value_source_blocks.json");
  });

  describe("Given I have routing based on the completeness of a block", () => {
    it("When the block being evaluated is incomplete (Q2), Then the dependent question (Q4) should not be on the path or displayed on the summary", async () => {
      await $(FirstQuestionPage.q1A1()).setValue("0");
      await click(FirstQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(ThirdQuestionPage.pageName);
      await $(ThirdQuestionPage.q1A1()).setValue("1");
      await click(ThirdQuestionPage.submit());

      await $(FifthQuestionPage.q1A1()).setValue("2");
      await click(FifthQuestionPage.submit());

      await $(SeventhQuestionPage.q1A1()).setValue("3");
      await click(SeventhQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
      await expect(await $("body").getText()).to.not.have.string("Section 1 Question 2");
      await expect(await $("body").getText()).to.not.have.string("Section 1 Question 4");
    });
  });

  describe("Given I have routing based on the completeness of a block", () => {
    it("When the blocks being evaluated are complete (Q2 + Q5), Then the dependent questions (Q4 + Q6) should be on the path and displayed on the summary", async () => {
      await $(FirstQuestionPage.q1A1()).setValue("1");
      await click(FirstQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(SecondQuestionPage.pageName);
      await $(SecondQuestionPage.q1A1()).setValue("1");
      await click(SecondQuestionPage.submit());

      await $(ThirdQuestionPage.q1A1()).setValue("2");
      await click(ThirdQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(FourthQuestionPage.pageName);
      await $(FourthQuestionPage.q1A1()).setValue("3");
      await click(FourthQuestionPage.submit());

      await $(FifthQuestionPage.q1A1()).setValue("4");
      await click(FifthQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(SixthQuestionPage.pageName);
      await $(SixthQuestionPage.q1A1()).setValue("5");
      await click(SixthQuestionPage.submit());

      await $(SeventhQuestionPage.q1A1()).setValue("6");
      await click(SeventhQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
      await expect(await $("body").getText()).to.have.string("Section 1 Question 4");
      await expect(await $("body").getText()).to.have.string("Section 1 Question 6");
    });
  });

  describe("Given I have routing based on the completeness of a block", () => {
    it("When an answer is changed so that the block being evaluated is completed, Then the dependent questions (Q4 + Q6) should be on the path and displayed on the summary", async () => {
      await $(FirstQuestionPage.q1A1()).setValue("0");
      await click(FirstQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(ThirdQuestionPage.pageName);
      await $(ThirdQuestionPage.q1A1()).setValue("1");
      await click(ThirdQuestionPage.submit());

      await $(FifthQuestionPage.q1A1()).setValue("2");
      await click(FifthQuestionPage.submit());

      await $(SeventhQuestionPage.q1A1()).setValue("3");
      await click(SeventhQuestionPage.submit());

      await $(SubmitPage.s1B1Q1A1Edit()).click();
      await expect(await browser.getUrl()).to.contain(FirstQuestionPage.pageName);
      await $(FirstQuestionPage.q1A1()).setValue("1");
      await click(FirstQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(SecondQuestionPage.pageName);
      await $(SecondQuestionPage.q1A1()).setValue("1");
      await click(SecondQuestionPage.submit());

      await click(ThirdQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(FourthQuestionPage.pageName);
      await $(FourthQuestionPage.q1A1()).setValue("3");
      await click(FourthQuestionPage.submit());

      await click(FifthQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(SixthQuestionPage.pageName);
      await $(SixthQuestionPage.q1A1()).setValue("3");
      await click(SixthQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
      await expect(await $("body").getText()).to.have.string("Section 1 Question 4");
      await expect(await $("body").getText()).to.have.string("Section 1 Question 6");
    });
  });

  describe("Given I have routing based on the completeness of a block", () => {
    it("When an answer is removed form the path block being evaluated is no longer completed, Then the dependent questions (Q4 + Q6) should not be on the path and not be displayed on the summary", async () => {
      await $(FirstQuestionPage.q1A1()).setValue("1");
      await click(FirstQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(SecondQuestionPage.pageName);
      await $(SecondQuestionPage.q1A1()).setValue("1");
      await click(SecondQuestionPage.submit());

      await $(ThirdQuestionPage.q1A1()).setValue("2");
      await click(ThirdQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(FourthQuestionPage.pageName);
      await $(FourthQuestionPage.q1A1()).setValue("3");
      await click(FourthQuestionPage.submit());

      await $(FifthQuestionPage.q1A1()).setValue("4");
      await click(FifthQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(SixthQuestionPage.pageName);
      await $(SixthQuestionPage.q1A1()).setValue("5");
      await click(SixthQuestionPage.submit());

      await $(SeventhQuestionPage.q1A1()).setValue("6");
      await click(SeventhQuestionPage.submit());

      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
      await $(SubmitPage.s1B1Q1A1Edit()).click();
      await expect(await browser.getUrl()).to.contain(FirstQuestionPage.pageName);
      await $(FirstQuestionPage.q1A1()).setValue("0");
      await click(FirstQuestionPage.submit());

      await expect(await $("body").getText()).to.not.have.string("Section 1 Question 4");
      await expect(await $("body").getText()).to.not.have.string("Section 1 Question 6");
    });
  });
});

describe("Feature: Section enabled based on progress value sources using block identifiers (no hub)", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_progress_value_source_section_enabled_no_hub.json");
  });

  describe("Given I have a section enabled based on the completeness of a block", () => {
    it("When the block being evaluated is complete, Then the dependent section should be enabled", async () => {
      await $(FirstQuestionPage.q1A1()).setValue("0");
      await click(FirstQuestionPage.submit());
      await $(SecondQuestionPage.q1A1()).setValue("1");
      await click(SecondQuestionPage.submit());
      await expect(await browser.getUrl()).to.contain(ThirdQuestionSectionTwoPage.pageName);
    });
  });
});

describe("Feature: Section enabled based on progress value sources using section identifiers", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_progress_value_source_section_enabled_hub.json");
  });

  describe("Given I have a section enabled based on the completeness of another section", () => {
    it("When the section being evaluated is complete, Then the dependent section should be enabled", async () => {
      await click(HubPage.submit());
      await $(FirstQuestionPage.q1A1()).setValue("0");
      await click(FirstQuestionPage.submit());
      await $(SecondQuestionPage.q1A1()).setValue("1");
      await click(SecondQuestionPage.submit());
      await expect(await $(HubPage.summaryRowState("section-2")).getText()).to.equal("Not started");
    });
  });

  describe("Given I have a section enabled based on the completeness of another section", () => {
    it("When the section being evaluated is incomplete, Then the dependent section should not be enabled", async () => {
      await click(HubPage.submit());
      await $(FirstQuestionPage.q1A1()).setValue("0");
      await click(FirstQuestionPage.submit());
      await browser.url(HubPage.url());

      await expect(await $(HubPage.summaryRowState("section-1")).getText()).to.equal("Partially completed");
      await expect(await $("body").getText()).to.not.have.string("Section 2");
    });
  });
});
