import TotalAnswerPage from "../../../../generated_pages/validation_sum_against_total_less_than/total-block.page";
import BreakdownAnswerPage from "../../../../generated_pages/validation_sum_against_total_less_than/breakdown-block.page";
import SubmitPage from "../../../../generated_pages/validation_sum_against_total_less_than/submit.page";

describe("Feature: Sum of grouped answers validation (less than) against total", () => {
  beforeEach(async ()=> {
    await browser.openQuestionnaire("test_validation_sum_against_total_less_than.json");
  });

  describe("Given I start a grouped answer validation survey and enter 12 into the total", () => {
    it("When I continue and enter 2 in each breakdown field, Then I should be able to get to the summary", async ()=> {
      await $(await TotalAnswerPage.total()).setValue("12");
      await $(await TotalAnswerPage.submit()).click();
      await $(await BreakdownAnswerPage.breakdown1()).setValue("2");
      await $(await BreakdownAnswerPage.breakdown2()).setValue("2");
      await $(await BreakdownAnswerPage.breakdown3()).setValue("2");
      await $(await BreakdownAnswerPage.breakdown4()).setValue("2");
      await $(await BreakdownAnswerPage.submit()).click();
      await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });

  describe("Given I start a grouped answer validation survey and enter 5 into the total", () => {
    it("When I continue and enter 4 into breakdown 1 and leave the others empty, Then I should be able to get to the summary", async ()=> {
      await $(await TotalAnswerPage.total()).setValue("5");
      await $(await TotalAnswerPage.submit()).click();
      await $(await BreakdownAnswerPage.breakdown1()).setValue("4");
      await $(await BreakdownAnswerPage.breakdown2()).setValue("");
      await $(await BreakdownAnswerPage.breakdown3()).setValue("");
      await $(await BreakdownAnswerPage.breakdown4()).setValue("");
      await $(await BreakdownAnswerPage.submit()).click();
      await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });

  describe("Given I start a grouped answer validation survey and enter 12 into the total", () => {
    it("When I continue and enter 3 in each breakdown field, Then I should see a validation error", async ()=> {
      await $(await TotalAnswerPage.total()).setValue("12");
      await $(await TotalAnswerPage.submit()).click();
      await $(await BreakdownAnswerPage.breakdown1()).setValue("3");
      await $(await BreakdownAnswerPage.breakdown2()).setValue("3");
      await $(await BreakdownAnswerPage.breakdown3()).setValue("3");
      await $(await BreakdownAnswerPage.breakdown4()).setValue("3");
      await $(await BreakdownAnswerPage.submit()).click();
      await expect(await $(await BreakdownAnswerPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to less than £12.00");
    });
  });

  describe("Given I start a grouped answer validation survey and enter 5 into the total", () => {
    it("When I continue and enter 3 in each breakdown field, Then I should see a validation error", async ()=> {
      await $(await TotalAnswerPage.total()).setValue("5");
      await $(await TotalAnswerPage.submit()).click();
      await $(await BreakdownAnswerPage.breakdown1()).setValue("3");
      await $(await BreakdownAnswerPage.breakdown2()).setValue("3");
      await $(await BreakdownAnswerPage.breakdown3()).setValue("3");
      await $(await BreakdownAnswerPage.breakdown4()).setValue("3");
      await $(await BreakdownAnswerPage.submit()).click();
      await expect(await $(await BreakdownAnswerPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to less than £5.00");
    });
  });
});
