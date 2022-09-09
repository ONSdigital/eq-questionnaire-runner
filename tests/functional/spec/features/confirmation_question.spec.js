import NumberOfEmployeesTotalBlockPage from "../../generated_pages/confirmation_question/number-of-employees-total-block.page.js";
import ConfirmZeroEmployeesBlockPage from "../../generated_pages/confirmation_question/confirm-zero-employees-block.page.js";
import SubmitPage from "../../generated_pages/confirmation_question/submit.page.js";

describe("Feature: Confirmation Question", () => {
  describe("Given I have a completed the confirmation question", () => {
    before("Get to summary", () => {
      browser.openQuestionnaire("test_confirmation_question.json");
    });

    it("When I view the summary, Then the confirmation question should not be displayed", () => {
      $(NumberOfEmployeesTotalBlockPage.numberOfEmployeesTotal()).setValue(0);
      $(NumberOfEmployeesTotalBlockPage.submit()).click();
      $(ConfirmZeroEmployeesBlockPage.yesThisIsCorrect()).click();
      $(ConfirmZeroEmployeesBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      expect($(SubmitPage.numberOfEmployeesTotal()).getText()).to.contain("0");
      expect($$(SubmitPage.confirmZeroEmployeesAnswer())).to.be.empty;
    });
  });
  describe("Given a confirmation Question", () => {
    it("When I answer 'No' to the confirmation question, Then I should be routed back to the source question", () => {
      browser.openQuestionnaire("test_confirmation_question.json");
      $(NumberOfEmployeesTotalBlockPage.submit()).click();
      $(ConfirmZeroEmployeesBlockPage.noINeedToCorrectThis()).click();
      $(ConfirmZeroEmployeesBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(NumberOfEmployeesTotalBlockPage.pageName);
    });
  });
  describe("Given a number of employees Question", () => {
    it("When I don't answer the number of employees question and go to summary, Then default value should be displayed for the the number of employees question", () => {
      browser.openQuestionnaire("test_confirmation_question.json");
      $(NumberOfEmployeesTotalBlockPage.submit()).click();
      $(ConfirmZeroEmployeesBlockPage.yesThisIsCorrect()).click();
      $(ConfirmZeroEmployeesBlockPage.submit()).click();
      expect($(SubmitPage.numberOfEmployeesTotal()).getText()).to.contain("0");
    });
  });
});
