import TotalAnswerPage from "../../../../generated_pages/validation_sum_against_total_multiple/total-block.page";
import BreakdownAnswerPage from "../../../../generated_pages/validation_sum_against_total_multiple/breakdown-block.page";
import SubmitPage from "../../../../generated_pages/validation_sum_against_total_multiple/submit.page";
import { click } from "../../../../helpers";
describe("Feature: Sum validation (Multi Rule Equals)", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_validation_sum_against_total_multiple.json");
  });

  describe("Given I start a grouped answer with multi rule validation survey and enter 10 into the total", () => {
    it("When I continue and enter nothing, all zeros or 10 at breakdown level, Then I should be able to get to the summary", async () => {
      await $(TotalAnswerPage.total()).setValue("10");
      await click(TotalAnswerPage.submit());
      await click(BreakdownAnswerPage.submit());
      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);

      await $(SubmitPage.previous()).click();
      await $(BreakdownAnswerPage.breakdown1()).setValue("0");
      await $(BreakdownAnswerPage.breakdown2()).setValue("0");
      await $(BreakdownAnswerPage.breakdown3()).setValue("0");
      await $(BreakdownAnswerPage.breakdown4()).setValue("0");
      await click(BreakdownAnswerPage.submit());
      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);

      await $(SubmitPage.previous()).click();
      await $(BreakdownAnswerPage.breakdown1()).setValue("1");
      await $(BreakdownAnswerPage.breakdown2()).setValue("2");
      await $(BreakdownAnswerPage.breakdown3()).setValue("3");
      await $(BreakdownAnswerPage.breakdown4()).setValue("4");
      await click(BreakdownAnswerPage.submit());
      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
    });
  });

  describe("Given I start a grouped answer with multi rule validation survey and enter 10 into the total", () => {
    it("When I continue and enter less between 1 - 9 or greater than 10, Then it should error", async () => {
      await $(TotalAnswerPage.total()).setValue("10");
      await click(TotalAnswerPage.submit());
      await $(BreakdownAnswerPage.breakdown1()).setValue("1");
      await click(BreakdownAnswerPage.submit());

      await expect(await $(BreakdownAnswerPage.errorNumber(1)).getText()).toBe("Enter answers that add up to 10");

      await $(BreakdownAnswerPage.breakdown2()).setValue("2");
      await $(BreakdownAnswerPage.breakdown3()).setValue("3");
      await $(BreakdownAnswerPage.breakdown4()).setValue("5");
      await click(BreakdownAnswerPage.submit());
      await expect(await $(BreakdownAnswerPage.errorNumber(1)).getText()).toBe("Enter answers that add up to 10");
    });
  });
});
