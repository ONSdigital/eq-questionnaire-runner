import TotalAnswerPage from "../../../../generated_pages/validation_sum_against_total_equal/total-block.page";
import BreakdownAnswerPage from "../../../../generated_pages/validation_sum_against_total_equal/breakdown-block.page";
import SubmitPage from "../../../../generated_pages/validation_sum_against_total_equal/submit.page";

const answerAndSubmitBreakdownQuestion = async (breakdown1, breakdown2, breakdown3, breakdown4) => {
  await $(BreakdownAnswerPage.breakdown1()).setValue(breakdown1);
  await $(BreakdownAnswerPage.breakdown2()).setValue(breakdown2);
  await $(BreakdownAnswerPage.breakdown3()).setValue(breakdown3);
  await $(BreakdownAnswerPage.breakdown4()).setValue(breakdown4);
  await $(BreakdownAnswerPage.submit()).click();
};

describe("Feature: Sum of grouped answers equal to validation against total ", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_validation_sum_against_total_equal.json");
  });

  describe("Given I start a grouped answer validation survey and enter 12 into the total", () => {
    it("When I continue and enter 3 in each breakdown field, Then I should be able to get to the summary", async () => {
      await $(TotalAnswerPage.total()).setValue("12");
      await $(TotalAnswerPage.submit()).click();

      await answerAndSubmitBreakdownQuestion("3", "3", "3", "3");

      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });

  describe("Given I completed a grouped answer validation question and I am on the summary", () => {
    it("When I go back from the summary and change the total, Then I must reconfirm the breakdown question with valid answers before I can get to the summary", async () => {
      await $(TotalAnswerPage.total()).setValue("12");
      await $(TotalAnswerPage.submit()).click();
      await answerAndSubmitBreakdownQuestion("3", "3", "3", "3");

      await $(SubmitPage.totalAnswerEdit()).click();
      await $(TotalAnswerPage.total()).setValue("15");
      await $(TotalAnswerPage.submit()).click();

      await browser.url(SubmitPage.url());
      await expect(await browser.getUrl()).to.contain(BreakdownAnswerPage.pageName);

      await $(BreakdownAnswerPage.submit()).click();
      await expect(await $(BreakdownAnswerPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to 15");

      await answerAndSubmitBreakdownQuestion("6", "3", "3", "3");

      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });

  describe("Given I start a grouped answer validation survey and enter 5 into the total", () => {
    it("When I continue and enter 5 into breakdown 1 and leave the others empty, Then I should be able to get to the summary", async () => {
      await $(TotalAnswerPage.total()).setValue("5");
      await $(TotalAnswerPage.submit()).click();
      await answerAndSubmitBreakdownQuestion("5", "", "", "");

      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });

  describe("Given I start a grouped answer validation survey and enter 5 into the total", () => {
    it("When I continue and enter 3 in each breakdown field, Then I should see a validation error", async () => {
      await $(TotalAnswerPage.total()).setValue("5");
      await $(TotalAnswerPage.submit()).click();
      await answerAndSubmitBreakdownQuestion("3", "3", "3", "3");

      await expect(await $(BreakdownAnswerPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to 5");
    });
  });
});
