import NumberOfEmployeesTotalBlockPage from "../../../generated_pages/confirmation_question/number-of-employees-total-block.page.js";
import ConfirmZeroEmployeesBlockPage from "../../../generated_pages/confirmation_question/confirm-zero-employees-block.page.js";
import SubmitPage from "../../../generated_pages/confirmation_question/submit.page.js";
import { click, verifyUrlContains } from "../../../helpers";
describe("Feature: Routing incompletes block if routing backwards", () => {
  describe("Given I have a confirmation Question", () => {
    beforeAll("Load the survey", async () => {
      await browser.openQuestionnaire("test_confirmation_question.json");
    });
    it("When I route to submit, I get to the summary", async () => {
      await $(NumberOfEmployeesTotalBlockPage.numberOfEmployeesTotal()).setValue(0);
      await click(NumberOfEmployeesTotalBlockPage.submit());
      await $(ConfirmZeroEmployeesBlockPage.yesThisIsCorrect()).click();
      await click(ConfirmZeroEmployeesBlockPage.submit());
      await verifyUrlContains(SubmitPage.pageName);
    });
  });
});
