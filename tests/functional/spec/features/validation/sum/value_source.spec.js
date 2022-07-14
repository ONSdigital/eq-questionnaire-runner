import TotalAnswerPage from "../../../../generated_pages/validation_sum_against_value_source/total-block.page";
import BreakdownAnswerPage from "../../../../generated_pages/validation_sum_against_value_source/breakdown-block.page";
import TotalPlaybackPage from "../../../../generated_pages/validation_sum_against_value_source/number-total-playback.page";
import SecondBreakdownAnswerPage from "../../../../generated_pages/validation_sum_against_value_source/second-breakdown-block.page";
import SubmitPage from "../../../../generated_pages/validation_sum_against_total_equal/submit.page";

const answerAndSubmitBreakdownQuestion = (breakdown1, breakdown2, breakdown3, breakdown4) => {
  $(BreakdownAnswerPage.breakdown1()).setValue(breakdown1);
  $(BreakdownAnswerPage.breakdown2()).setValue(breakdown2);
  $(BreakdownAnswerPage.breakdown3()).setValue(breakdown3);
  $(BreakdownAnswerPage.breakdown4()).setValue(breakdown4);
  $(BreakdownAnswerPage.submit()).click();
};

const answerAndSubmitSecondBreakdownQuestion = (breakdown1, breakdown2, breakdown3, breakdown4) => {
  $(SecondBreakdownAnswerPage.secondBreakdown1()).setValue(breakdown1);
  $(SecondBreakdownAnswerPage.secondBreakdown2()).setValue(breakdown2);
  $(SecondBreakdownAnswerPage.secondBreakdown3()).setValue(breakdown3);
  $(SecondBreakdownAnswerPage.secondBreakdown4()).setValue(breakdown4);
  $(SecondBreakdownAnswerPage.submit()).click();
};

const answerBothBreakdownQuestions = (array1, array2) => {
  answerAndSubmitBreakdownQuestion(array1[0], array1[1], array1[2], array1[3]);

  $(TotalPlaybackPage.submit()).click();

  answerAndSubmitSecondBreakdownQuestion(array2[0], array2[1], array2[2], array2[3]);
};

describe("Feature: Sum of grouped answers equal to validation against value source ", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_validation_sum_against_value_source.json");
  });

  describe("Given I start a grouped answer validation survey and enter 12 into the total", () => {
    it("When I continue and enter 3 in each breakdown field, Then I should be able to get to the total playback page", () => {
      $(TotalAnswerPage.total()).setValue("12");
      $(TotalAnswerPage.submit()).click();

      answerAndSubmitBreakdownQuestion("3", "3", "3", "3");

      expect(browser.getUrl()).to.contain(TotalPlaybackPage.pageName);
    });
  });

  describe("Given I have a calculated summary value of 12", () => {
    it("When I continue to second breakdown and enter values equal to calculated summary total, Then I should be able to get to the summary page", () => {
      $(TotalAnswerPage.total()).setValue("12");
      $(TotalAnswerPage.submit()).click();

      answerBothBreakdownQuestions(["3", "3", "3", "3"], ["2", "2", "1", "1"]);

      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });

  describe("Given I completed both grouped answer validation questions and I am on the summary", () => {
    it("When I go back from the summary and change the total, Then I must reconfirm both breakdown questions with valid answers before I can get to the summary", () => {
      $(TotalAnswerPage.total()).setValue("12");
      $(TotalAnswerPage.submit()).click();

      answerBothBreakdownQuestions(["3", "3", "3", "3"], ["2", "2", "1", "1"]);

      $(SubmitPage.totalAnswerEdit()).click();
      $(TotalAnswerPage.total()).setValue("15");
      $(TotalAnswerPage.submit()).click();

      $(BreakdownAnswerPage.submit()).click();

      expect($(BreakdownAnswerPage.singleErrorLink()).isDisplayed()).to.be.true;

      expect($(BreakdownAnswerPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to 15");

      answerBothBreakdownQuestions(["6", "3", "3", "3"], ["3", "3", "2", "1"]);

      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });

  describe("Given I completed both grouped answer validation questions and I am on the summary", () => {
    it("When I go back from the summary and change the total, Then I must reconfirm the breakdown question based on answer value source with valid answers before I can continue", () => {
      $(TotalAnswerPage.total()).setValue("12");
      $(TotalAnswerPage.submit()).click();

      answerBothBreakdownQuestions(["3", "3", "3", "3"], ["2", "2", "1", "1"]);

      $(SubmitPage.totalAnswerEdit()).click();
      $(TotalAnswerPage.total()).setValue("15");
      $(TotalAnswerPage.submit()).click();

      answerAndSubmitBreakdownQuestion("0", "3", "3", "3");

      expect($(BreakdownAnswerPage.singleErrorLink()).isDisplayed()).to.be.true;

      expect($(BreakdownAnswerPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to 15");

      answerBothBreakdownQuestions(["5", "4", "4", "2"], ["3", "3", "2", "1"]);

      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });

  describe("Given I completed both grouped answer validation questions and I am on the summary", () => {
    it("When I go back from the summary and change the first breakdown question answers so its total changes, Then I must reconfirm the second breakdown question based on calculated summary value source with valid answers before I can continue", () => {
      $(TotalAnswerPage.total()).setValue("12");
      $(TotalAnswerPage.submit()).click();

      answerBothBreakdownQuestions(["3", "3", "3", "3"], ["2", "2", "1", "1"]);

      $(SubmitPage.breakdown1Edit()).click();

      answerAndSubmitBreakdownQuestion("6", "3", "2", "1");

      $(TotalPlaybackPage.submit()).click();

      $(SecondBreakdownAnswerPage.submit()).click();

      expect($(SecondBreakdownAnswerPage.singleErrorLink()).isDisplayed()).to.be.true;

      expect($(SecondBreakdownAnswerPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to 9");

      answerAndSubmitSecondBreakdownQuestion("5", "4", "0", "0");

      expect($(SecondBreakdownAnswerPage.singleErrorLink()).isDisplayed()).to.be.false;

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

  describe("Given I start a grouped answer validation survey and enter 5 into the total", () => {
    it("When I enter 3 in each breakdown field and continue to second breakdown and enter 3 in each field, Then I should see a validation error", () => {
      $(TotalAnswerPage.total()).setValue("5");
      $(TotalAnswerPage.submit()).click();

      answerBothBreakdownQuestions(["2", "1", "1", "1"], ["3", "3", "3", "3"]);

      expect($(SecondBreakdownAnswerPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to 3");
    });
  });
});
