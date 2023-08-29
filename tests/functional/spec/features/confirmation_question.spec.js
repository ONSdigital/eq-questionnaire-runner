import NumberOfEmployeesTotalBlockPage from "../../generated_pages/confirmation_question/number-of-employees-total-block.page.js";
import ConfirmZeroEmployeesBlockPage from "../../generated_pages/confirmation_question/confirm-zero-employees-block.page.js";
import SubmitPage from "../../generated_pages/confirmation_question/submit.page.js";
import { click } from "../../helpers";

describe("Feature: Confirmation Question", () => {
  describe("Given I have a completed the confirmation question", () => {
    before("Get to summary", async () => {
      await browser.openQuestionnaire("test_confirmation_question.json");
    });

    it("When I view the summary, Then the confirmation question should not be displayed", async () => {
      await $(NumberOfEmployeesTotalBlockPage.numberOfEmployeesTotal()).setValue(0);
      await click(NumberOfEmployeesTotalBlockPage.submit());
      await $(ConfirmZeroEmployeesBlockPage.yesThisIsCorrect()).click();
      await click(ConfirmZeroEmployeesBlockPage.submit());
      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
      await expect(await $(SubmitPage.numberOfEmployeesTotal()).getText()).to.contain("0");
      await expect(await $$(SubmitPage.confirmZeroEmployeesAnswer())).to.be.empty;
    });
  });
  describe("Given a confirmation Question", () => {
    it("When I answer 'No' to the confirmation question, Then I should be routed back to the source question", async () => {
      await browser.openQuestionnaire("test_confirmation_question.json");
      await click(NumberOfEmployeesTotalBlockPage.submit());
      await $(ConfirmZeroEmployeesBlockPage.noINeedToCorrectThis()).click();
      await click(ConfirmZeroEmployeesBlockPage.submit());
      await expect(await browser.getUrl()).to.contain(NumberOfEmployeesTotalBlockPage.pageName);
    });
  });
  describe("Given a number of employees Question", () => {
    it("When I don't answer the number of employees question and go to summary, Then default value should be displayed for the the number of employees question", async () => {
      await browser.openQuestionnaire("test_confirmation_question.json");
      await click(NumberOfEmployeesTotalBlockPage.submit());
      await $(ConfirmZeroEmployeesBlockPage.yesThisIsCorrect()).click();
      await click(ConfirmZeroEmployeesBlockPage.submit());
      await expect(await $(SubmitPage.numberOfEmployeesTotal()).getText()).to.contain("0");
    });
  });
});
