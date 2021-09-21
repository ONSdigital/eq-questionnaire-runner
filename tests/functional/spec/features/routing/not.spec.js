import FirstNumberQuestionPage from "../../../generated_pages/new_routing_not/number-question-1.page";
import SecondNumberQuestionPage from "../../../generated_pages/new_routing_not/number-question-2.page";
import CorrectAnswerPage from "../../../generated_pages/new_routing_not/correct-answer.page";
import IncorrectAnswerPage from "../../../generated_pages/new_routing_not/incorrect-answer.page";

describe("Feature: Routing - Not Operator", () => {
  describe("Equals", () => {
    describe("Given I start the not operator routing survey", () => {
      beforeEach(() => {
        browser.openQuestionnaire("test_new_routing_not.json");
      });

      it("When I enter both answers correctly, Then I should be routed to the correct page", () => {
        $(FirstNumberQuestionPage.answer1()).setValue(1);
        $(FirstNumberQuestionPage.submit()).click();
        $(SecondNumberQuestionPage.answer2()).setValue(2);
        $(SecondNumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter one of the answers incorrectly, Then I should be routed to the correct page", () => {
        $(FirstNumberQuestionPage.answer1()).setValue(555);
        $(FirstNumberQuestionPage.submit()).click();
        $(SecondNumberQuestionPage.answer2()).setValue(321);
        $(SecondNumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter both answers incorrectly, Then I should be routed to the incorrect page", () => {
          $(FirstNumberQuestionPage.answer1()).setValue(123);
          $(FirstNumberQuestionPage.submit()).click();
          $(SecondNumberQuestionPage.answer2()).setValue(321);
          $(SecondNumberQuestionPage.submit()).click();
          expect(browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
        });
    });
  });
});
