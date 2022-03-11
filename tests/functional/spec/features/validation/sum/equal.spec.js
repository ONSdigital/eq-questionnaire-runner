import TotalAnswerPage from "../../../../generated_pages/validation_sum_against_total_equal/total-block.page";
import BreakdownAnswerPage from "../../../../generated_pages/validation_sum_against_total_equal/breakdown-block.page";
import SubmitPage from "../../../../generated_pages/validation_sum_against_total_equal/submit.page";

const answerAndSubmitBreakdownQuestion = (breakdown1, breakdown2, breakdown3, breakdown4) => {
  $(BreakdownAnswerPage.breakdown1()).setValue(breakdown1);
  $(BreakdownAnswerPage.breakdown2()).setValue(breakdown2);
  $(BreakdownAnswerPage.breakdown3()).setValue(breakdown3);
  $(BreakdownAnswerPage.breakdown4()).setValue(breakdown4);
  $(BreakdownAnswerPage.submit()).click();
};

describe("Feature: Sum of grouped answers equal to validation against total ", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_validation_sum_against_total_equal.json");
  });

  describe("Given I start a grouped answer validation survey and enter 12 into the total", () => {
    it("When I continue and enter 3 in each breakdown field, Then I should be able to get to the summary", () => {
      $(TotalAnswerPage.total()).setValue("12");
      $(TotalAnswerPage.submit()).click();

      answerAndSubmitBreakdownQuestion("3", "3", "3", "3");

      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });

  describe("Given I completed a grouped answer validation question and I am on the summary", () => {
    it("When I go back from the summary and change the total, Then I must reconfirm the breakdown question with valid answers before I can get to the summary", () => {
      $(TotalAnswerPage.total()).setValue("12");
      $(TotalAnswerPage.submit()).click();
      answerAndSubmitBreakdownQuestion("3", "3", "3", "3");

      $(SubmitPage.totalAnswerEdit()).click();
      $(TotalAnswerPage.total()).setValue("15");
      $(TotalAnswerPage.submit()).click();

      browser.url(SubmitPage.url());
      expect(browser.getUrl()).to.contain(BreakdownAnswerPage.pageName);

      $(BreakdownAnswerPage.submit()).click();
      expect($(BreakdownAnswerPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to 15");

      answerAndSubmitBreakdownQuestion("6", "3", "3", "3");

      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });

  describe("Given I start a grouped answer validation survey and enter 5 into the total", () => {
    it("When I continue and enter 5 into breakdown 1 and leave the others empty, Then I should be able to get to the summary", () => {
      $(TotalAnswerPage.total()).setValue("5");
      $(TotalAnswerPage.submit()).click();
      answerAndSubmitBreakdownQuestion("5", "", "", "");

      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });

  describe("Given I start a grouped answer validation survey and enter 5 into the total", () => {
    it("When I continue and enter 3 in each breakdown field, Then I should see a validation error", () => {
      $(TotalAnswerPage.total()).setValue("5");
      $(TotalAnswerPage.submit()).click();
      answerAndSubmitBreakdownQuestion("3", "3", "3", "3");

      expect($(BreakdownAnswerPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to 5");
    });
  });
});
