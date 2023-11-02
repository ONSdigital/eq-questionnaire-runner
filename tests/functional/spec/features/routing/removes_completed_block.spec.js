import NumberOfEmployeesTotalBlockPage from "../../../generated_pages/confirmation_question/number-of-employees-total-block.page.js";
import ConfirmZeroEmployeesBlockPage from "../../../generated_pages/confirmation_question/confirm-zero-employees-block.page.js";
import SubmitPage from "../../../generated_pages/confirmation_question/submit.page.js";
import { click } from "../../../helpers";
describe("Feature: Routing incompletes block if routing backwards", () => {
  describe("Given I have a confirmation Question", () => {
    before("Get to summary", async () => {
      await browser.openQuestionnaire("test_confirmation_question.json");
      await $(NumberOfEmployeesTotalBlockPage.numberOfEmployeesTotal()).setValue(0);
      await click(NumberOfEmployeesTotalBlockPage.submit());
      await $(ConfirmZeroEmployeesBlockPage.yes()).click();
      await click(ConfirmZeroEmployeesBlockPage.submit());
      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
    });
  });
});
