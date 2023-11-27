import TotalAnswerPage from "../../../../generated_pages/validation_sum_against_value_source/total-block.page";
import BreakdownAnswerPage from "../../../../generated_pages/validation_sum_against_value_source/breakdown-block.page";
import TotalPlaybackPage from "../../../../generated_pages/validation_sum_against_value_source/number-total-playback.page";
import SecondBreakdownAnswerPage from "../../../../generated_pages/validation_sum_against_value_source/second-breakdown-block.page";
import SubmitPage from "../../../../generated_pages/validation_sum_against_total_equal/submit.page";
import AnotherTotalPlaybackPage from "../../../../generated_pages/validation_sum_against_value_source/another-number-total-playback.page";
import { click } from "../../../../helpers";
const answerAndSubmitBreakdownQuestion = async (breakdown1, breakdown2, breakdown3, breakdown4) => {
  await $(BreakdownAnswerPage.breakdown1()).setValue(breakdown1);
  await $(BreakdownAnswerPage.breakdown2()).setValue(breakdown2);
  await $(BreakdownAnswerPage.breakdown3()).setValue(breakdown3);
  await $(BreakdownAnswerPage.breakdown4()).setValue(breakdown4);
  await click(BreakdownAnswerPage.submit());
};

const answerAndSubmitSecondBreakdownQuestion = async (breakdown1, breakdown2, breakdown3, breakdown4) => {
  await $(SecondBreakdownAnswerPage.secondBreakdown1()).setValue(breakdown1);
  await $(SecondBreakdownAnswerPage.secondBreakdown2()).setValue(breakdown2);
  await $(SecondBreakdownAnswerPage.secondBreakdown3()).setValue(breakdown3);
  await $(SecondBreakdownAnswerPage.secondBreakdown4()).setValue(breakdown4);
  await click(SecondBreakdownAnswerPage.submit());
};

const answerBothBreakdownQuestions = async (array1, array2) => {
  await answerAndSubmitBreakdownQuestion(array1[0], array1[1], array1[2], array1[3]);

  await click(TotalPlaybackPage.submit());

  await answerAndSubmitSecondBreakdownQuestion(array2[0], array2[1], array2[2], array2[3]);
};

describe("Feature: Sum of grouped answers equal to validation against value source ", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_validation_sum_against_value_source.json");
  });

  describe("Given I start a grouped answer validation survey and enter 12 into the total", () => {
    it("When I continue and enter 3 in each breakdown field, Then I should be able to get to the total playback page", async () => {
      await $(TotalAnswerPage.total()).setValue("12");
      await click(TotalAnswerPage.submit());

      await answerAndSubmitBreakdownQuestion("3", "3", "3", "3");

      await expect(browser).toHaveUrlContaining(TotalPlaybackPage.pageName);
    });
  });

  describe("Given I have a calculated summary value of 12", () => {
    it("When I continue to second breakdown and enter values equal to calculated summary total, Then I should be able to get to the summary page", async () => {
      await $(TotalAnswerPage.total()).setValue("12");
      await click(TotalAnswerPage.submit());

      await answerBothBreakdownQuestions(["3", "3", "3", "3"], ["2", "2", "1", "1"]);

      await expect(browser).toHaveUrlContaining(AnotherTotalPlaybackPage.pageName);
    });
  });

  describe("Given I completed both grouped answer validation questions and I am on the summary", () => {
    it("When I go back from the summary and change the total, Then I must reconfirm both breakdown questions with valid answers before I can get to the summary", async () => {
      await $(TotalAnswerPage.total()).setValue("12");
      await click(TotalAnswerPage.submit());

      await answerBothBreakdownQuestions(["3", "3", "3", "3"], ["2", "2", "1", "1"]);

      await click(AnotherTotalPlaybackPage.submit());

      await $(SubmitPage.totalAnswerEdit()).click();
      await $(TotalAnswerPage.total()).setValue("15");
      await click(TotalAnswerPage.submit());

      await click(BreakdownAnswerPage.submit());

      await expect(await $(BreakdownAnswerPage.singleErrorLink()).isDisplayed()).toBe(true);

      await expect(await $(BreakdownAnswerPage.errorNumber(1)).getText()).toBe("Enter answers that add up to 15");

      await answerBothBreakdownQuestions(["6", "3", "3", "3"], ["3", "3", "2", "1"]);

      await expect(browser).toHaveUrlContaining(AnotherTotalPlaybackPage.pageName);
    });
  });

  describe("Given I completed both grouped answer validation questions and I am on the summary", () => {
    it("When I go back from the summary and change the total, Then I must reconfirm the breakdown question based on answer value source with valid answers before I can continue", async () => {
      await $(TotalAnswerPage.total()).setValue("12");
      await click(TotalAnswerPage.submit());

      await answerBothBreakdownQuestions(["3", "3", "3", "3"], ["2", "2", "1", "1"]);

      await click(AnotherTotalPlaybackPage.submit());

      await $(SubmitPage.totalAnswerEdit()).click();
      await $(TotalAnswerPage.total()).setValue("15");
      await click(TotalAnswerPage.submit());

      await answerAndSubmitBreakdownQuestion("0", "3", "3", "3");

      await expect(await $(BreakdownAnswerPage.singleErrorLink()).isDisplayed()).toBe(true);

      await expect(await $(BreakdownAnswerPage.errorNumber(1)).getText()).toBe("Enter answers that add up to 15");

      await answerBothBreakdownQuestions(["5", "4", "4", "2"], ["3", "3", "2", "1"]);

      await expect(browser).toHaveUrlContaining(AnotherTotalPlaybackPage.pageName);
    });
  });

  describe("Given I completed both grouped answer validation questions and I am on the summary", () => {
    it("When I go back from the summary and change the first breakdown question answers so its total changes, Then I must reconfirm the second breakdown question based on calculated summary value source with valid answers before I can continue", async () => {
      await $(TotalAnswerPage.total()).setValue("12");
      await click(TotalAnswerPage.submit());

      await answerBothBreakdownQuestions(["3", "3", "3", "3"], ["2", "2", "1", "1"]);

      await click(AnotherTotalPlaybackPage.submit());

      await $(SubmitPage.breakdown1Edit()).click();

      await answerAndSubmitBreakdownQuestion("6", "3", "2", "1");

      await click(TotalPlaybackPage.submit());

      await click(SecondBreakdownAnswerPage.submit());

      await expect(await $(SecondBreakdownAnswerPage.singleErrorLink()).isDisplayed()).toBe(true);

      await expect(await $(SecondBreakdownAnswerPage.errorNumber(1)).getText()).toBe("Enter answers that add up to 9");

      await answerAndSubmitSecondBreakdownQuestion("5", "4", "0", "0");

      await expect(await $(SecondBreakdownAnswerPage.singleErrorLink()).isDisplayed()).toBe(false);

      await expect(browser).toHaveUrlContaining(AnotherTotalPlaybackPage.pageName);
    });
  });

  describe("Given I start a grouped answer validation survey and enter 5 into the total", () => {
    it("When I continue and enter 3 in each breakdown field, Then I should see a validation error", async () => {
      await $(TotalAnswerPage.total()).setValue("5");
      await click(TotalAnswerPage.submit());

      await answerAndSubmitBreakdownQuestion("3", "3", "3", "3");

      await expect(await $(BreakdownAnswerPage.errorNumber(1)).getText()).toBe("Enter answers that add up to 5");
    });
  });

  describe("Given I start a grouped answer validation survey and enter 5 into the total", () => {
    it("When I enter 3 in each breakdown field and continue to second breakdown and enter 3 in each field, Then I should see a validation error", async () => {
      await $(TotalAnswerPage.total()).setValue("5");
      await click(TotalAnswerPage.submit());

      await answerBothBreakdownQuestions(["2", "1", "1", "1"], ["3", "3", "3", "3"]);

      await expect(await $(SecondBreakdownAnswerPage.errorNumber(1)).getText()).toBe("Enter answers that add up to 3");
    });
  });
  describe("Given I complete a grouped answer validation survey and get to the final summary page", () => {
    it("When I journey back and I end up with no answer_id anchor for the url, Then I should not see any errors", async () => {
      await $(TotalAnswerPage.total()).setValue("5");
      await click(TotalAnswerPage.submit());

      await answerBothBreakdownQuestions(["2", "1", "1", "1"], ["1", "2", "0", "0"]);

      await click(AnotherTotalPlaybackPage.submit());

      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);

      await $(SubmitPage.previous()).click();

      await $(AnotherTotalPlaybackPage.breakdown1Edit()).click();

      await $(BreakdownAnswerPage.breakdown1()).setValue("1");
      await $(BreakdownAnswerPage.breakdown2()).setValue("2");

      await click(BreakdownAnswerPage.submit());

      await click(TotalPlaybackPage.previous());

      await click(BreakdownAnswerPage.submit());

      await click(TotalPlaybackPage.submit());

      await click(SecondBreakdownAnswerPage.submit());

      await click(AnotherTotalPlaybackPage.submit());

      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
    });
  });
});
