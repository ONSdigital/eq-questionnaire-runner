import NumberOfEmployeesTotalBlockPage from "../../../generated_pages/confirmation_question/number-of-employees-total-block.page.js";
import ConfirmZeroEmployeesBlockPage from "../../../generated_pages/confirmation_question/confirm-zero-employees-block.page.js";
import SubmitPage from "../../../generated_pages/confirmation_question/submit.page.js";

describe("Feature: Routing incompletes block if routing backwards", () => {
  describe("Given I have a confirmation Question", () => {
    before("Get to summary", () => {
      browser.openQuestionnaire("test_confirmation_question.json");
      $(NumberOfEmployeesTotalBlockPage.numberOfEmployeesTotal()).setValue(0);
      $(NumberOfEmployeesTotalBlockPage.submit()).click();
      $(ConfirmZeroEmployeesBlockPage.yes()).click();
      $(ConfirmZeroEmployeesBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });
});
