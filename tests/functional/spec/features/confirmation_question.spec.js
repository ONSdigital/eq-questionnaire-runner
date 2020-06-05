import NumberOfEmployeesTotalBlockPage from "../../generated_pages/confirmation_question/number-of-employees-total-block.page.js";
import ConfirmZeroEmployeesBlockPage from "../../generated_pages/confirmation_question/confirm-zero-employees-block.page.js";
import SummaryPage from "../../generated_pages/confirmation_question/summary.page.js";

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
      expect(browser.getUrl()).to.contain(SummaryPage.pageName);
      expect($(SummaryPage.numberOfEmployeesTotal()).getText()).to.contain("0");
      expect($$(SummaryPage.confirmZeroEmployeesAnswer())).to.be.empty;
    });
  });

  describe("Given a confirmation Question", () => {
    it("When I answer 'No' to the confirmation question, Then I should be routed back to the source question", () => {
      browser.openQuestionnaire("test_confirmation_question.json");
      $(NumberOfEmployeesTotalBlockPage.submit()).click();
      $(ConfirmZeroEmployeesBlockPage.noINeedToChangeThis()).click();
      $(ConfirmZeroEmployeesBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(NumberOfEmployeesTotalBlockPage.pageName);
    });
  });
});
