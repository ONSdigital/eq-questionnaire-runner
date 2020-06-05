import NumberQuestionPage from "../../../generated_pages/routing_number_equals/number-question.page";
import CorrectAnswerPage from "../../../generated_pages/routing_number_equals/correct-answer.page";
import IncorrectAnswerPage from "../../../generated_pages/routing_number_equals/incorrect-answer.page";

describe("Feature: Routing on a Number", () => {
  describe("Equals", () => {
    describe("Given I start number routing equals survey", () => {
      before(() => {
        browser.openQuestionnaire("test_routing_number_equals.json");
      });

      it("When I enter the correct number, Then I should be routed to the correct page", () => {
        $(NumberQuestionPage.answer()).setValue(123);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter an incorrect number, Then I should be routed to the incorrect page", () => {
        $(CorrectAnswerPage.previous()).click();
        $(NumberQuestionPage.answer()).setValue(555);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Not Equals", () => {
    describe("Given I start number routing not equals survey", () => {
      before(() => {
        browser.openQuestionnaire("test_routing_number_not_equals.json");
      });

      it("When I enter a different number, Then I should be routed to the correct page", () => {
        $(NumberQuestionPage.answer()).setValue(987);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a matching number, Then I should be routed to the incorrect page", () => {
        $(CorrectAnswerPage.previous()).click();
        $(NumberQuestionPage.answer()).setValue(123);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Greater Than", () => {
    describe("Given I start number routing greater then survey", () => {
      before(() => {
        browser.openQuestionnaire("test_routing_number_greater_than.json");
      });

      it("When I enter a greater number, Then I should be routed to the correct page", () => {
        $(NumberQuestionPage.answer()).setValue(555);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a smaller number, Then I should be routed to the incorrect page", () => {
        $(CorrectAnswerPage.previous()).click();
        $(NumberQuestionPage.answer()).setValue(2);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Less Than", () => {
    describe("Given I start number routing less then survey", () => {
      before(() => {
        browser.openQuestionnaire("test_routing_number_less_than.json");
      });

      it("When I enter a smaller number, Then I should be routed to the correct page", () => {
        $(NumberQuestionPage.answer()).setValue(77);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a greater number, Then I should be routed to the incorrect page", () => {
        $(CorrectAnswerPage.previous()).click();
        $(NumberQuestionPage.answer()).setValue(765);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Greater Than or Equal", () => {
    describe("Given I start number routing greater then or equal survey", () => {
      before(() => {
        browser.openQuestionnaire("test_routing_number_greater_than_or_equal.json");
      });

      it("When I enter a greater number, Then I should be routed to the correct page", () => {
        $(NumberQuestionPage.answer()).setValue(555);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter an equal number, Then I should be routed to the correct page", () => {
        $(CorrectAnswerPage.previous()).click();
        $(NumberQuestionPage.answer()).setValue(123);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a smaller number, Then I should be routed to the incorrect page", () => {
        $(CorrectAnswerPage.previous()).click();
        $(NumberQuestionPage.answer()).setValue(2);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });

    describe("Given I have number routing with a greater than or equal to single condition", () => {
      before(() => {
        browser.openQuestionnaire("test_routing_number_greater_than_or_equal_single_condition.json");
      });

      it("When I enter a number larger than 123, Then I should be routed to the correct page", () => {
        $(NumberQuestionPage.answer()).setValue(555);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a number equal to 123, Then I should be routed to the correct page", () => {
        $(CorrectAnswerPage.previous()).click();
        $(NumberQuestionPage.answer()).setValue(123);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a number smaller than 123, Then I should be routed to the incorrect page", () => {
        $(CorrectAnswerPage.previous()).click();
        $(NumberQuestionPage.answer()).setValue(2);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Less Than or Equal", () => {
    describe("Given I start number routing less then or equal survey", () => {
      before(() => {
        browser.openQuestionnaire("test_routing_number_less_than_or_equal.json");
      });

      it("When I enter a less number, Then I should be routed to the correct page", () => {
        $(NumberQuestionPage.answer()).setValue(23);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter an equal number, Then I should be routed to the correct page", () => {
        $(CorrectAnswerPage.previous()).click();
        $(NumberQuestionPage.answer()).setValue(123);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a greater number, Then I should be routed to the incorrect page", () => {
        $(CorrectAnswerPage.previous()).click();
        $(NumberQuestionPage.answer()).setValue(546);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });

    describe("Given I have number routing with a less than or equal to single condition", () => {
      before(() => {
        browser.openQuestionnaire("test_routing_number_less_than_or_equal_single_condition.json");
      });

      it("When I enter a number less than 123, Then I should be routed to the correct page", () => {
        $(NumberQuestionPage.answer()).setValue(23);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a number equal to 123, Then I should be routed to the correct page", () => {
        $(CorrectAnswerPage.previous()).click();
        $(NumberQuestionPage.answer()).setValue(123);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a number larger than 123, Then I should be routed to the incorrect page", () => {
        $(CorrectAnswerPage.previous()).click();
        $(NumberQuestionPage.answer()).setValue(546);
        $(NumberQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });
});
