import FirstNumberQuestionPage from "../../../generated_pages/routing_and/number-question-1.page";
import SecondNumberQuestionPage from "../../../generated_pages/routing_and/number-question-2.page";
import CorrectAnswerPage from "../../../generated_pages/routing_and/correct-answer.page";
import IncorrectAnswerPage from "../../../generated_pages/routing_and/incorrect-answer.page";
import { click } from "../../../helpers";

describe("Feature: Routing - And Operator", () => {
  describe("Equals", () => {
    describe("Given I start the and operator routing survey", () => {
      beforeEach(async () => {
        await browser.openQuestionnaire("test_routing_and.json");
      });

      it("When I enter both answers correctly with 123 and 321, Then I should be routed to the correct page", async () => {
        await $(FirstNumberQuestionPage.answer1()).setValue(123);
        await click(FirstNumberQuestionPage.submit());
        await $(SecondNumberQuestionPage.answer2()).setValue(321);
        await click(SecondNumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I only enter the second answer correctly with 555 and 321, Then I should be routed to the incorrect page", async () => {
        await $(FirstNumberQuestionPage.answer1()).setValue(555);
        await click(FirstNumberQuestionPage.submit());
        await $(SecondNumberQuestionPage.answer2()).setValue(321);
        await click(SecondNumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });

      it("When I only enter the first answer correctly with 123 and 555, Then I should be routed to the incorrect page", async () => {
        await $(FirstNumberQuestionPage.answer1()).setValue(123);
        await click(FirstNumberQuestionPage.submit());
        await $(SecondNumberQuestionPage.answer2()).setValue(555);
        await click(SecondNumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });

      it("When I answer both questions incorrectly with 555 and 444, Then I should be routed to the incorrect page", async () => {
        await $(FirstNumberQuestionPage.answer1()).setValue(555);
        await click(FirstNumberQuestionPage.submit());
        await $(SecondNumberQuestionPage.answer2()).setValue(444);
        await click(SecondNumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });
});
