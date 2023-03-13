import FirstNumberQuestionPage from "../../../generated_pages/routing_or/number-question-1.page";
import SecondNumberQuestionPage from "../../../generated_pages/routing_or/number-question-2.page";
import CorrectAnswerPage from "../../../generated_pages/routing_or/correct-answer.page";
import IncorrectAnswerPage from "../../../generated_pages/routing_or/incorrect-answer.page";

describe("Feature: Routing - OR Operator", () => {
  describe("Equals", () => {
    describe("Given I start the or operator routing survey", () => {
      beforeEach(() => {
        browser.openQuestionnaire("test_routing_or.json");
      });

      it("When I enter both answers correctly with 123 and 321, Then I should be routed to the correct page", () => {
        $(FirstNumberQuestionPage.answer1()).setValue(123);
        $(FirstNumberQuestionPage.submit()).click();
        $(SecondNumberQuestionPage.answer2()).setValue(321);
        $(SecondNumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I only enter the second answer correctly with 555 and 321, Then I should be routed to the correct page", () => {
        $(FirstNumberQuestionPage.answer1()).setValue(555);
        $(FirstNumberQuestionPage.submit()).click();
        $(SecondNumberQuestionPage.answer2()).setValue(321);
        $(SecondNumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I only enter the first answer correctly with 123 and 555, Then I should be routed to the correct page", () => {
        $(FirstNumberQuestionPage.answer1()).setValue(123);
        $(FirstNumberQuestionPage.submit()).click();
        $(SecondNumberQuestionPage.answer2()).setValue(555);
        $(SecondNumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I answer both questions incorrectly with 555 and 444, Then I should be routed to the incorrect page", () => {
        $(FirstNumberQuestionPage.answer1()).setValue(555);
        $(FirstNumberQuestionPage.submit()).click();
        $(SecondNumberQuestionPage.answer2()).setValue(444);
        $(SecondNumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });
});
