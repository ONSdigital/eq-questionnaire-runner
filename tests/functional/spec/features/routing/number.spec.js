import NumberQuestionPage from "../../../generated_pages/routing_number_equals/number-question.page";
import CorrectAnswerPage from "../../../generated_pages/routing_number_equals/correct-answer.page";
import IncorrectAnswerPage from "../../../generated_pages/routing_number_equals/incorrect-answer.page";
import { click } from "../../../helpers";
describe("Feature: Routing on a Number", () => {
  describe("Equals", () => {
    describe("Given I start number routing equals survey", () => {
      before(async () => {
        await browser.openQuestionnaire("test_routing_number_equals.json");
      });

      it("When I enter 123, Then I should be routed to the correct page", async () => {
        await $(NumberQuestionPage.answer()).setValue(123);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a number that isn't 123, Then I should be routed to the incorrect page", async () => {
        await $(CorrectAnswerPage.previous()).click();
        await $(NumberQuestionPage.answer()).setValue(555);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Not Equals", () => {
    describe("Given I start number routing not equals survey", () => {
      before(async () => {
        await browser.openQuestionnaire("test_routing_number_not_equals.json");
      });

      it("When I enter a number that isn't 123, Then I should be routed to the correct page", async () => {
        await $(NumberQuestionPage.answer()).setValue(987);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter 123, Then I should be routed to the incorrect page", async () => {
        await $(CorrectAnswerPage.previous()).click();
        await $(NumberQuestionPage.answer()).setValue(123);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Greater Than", () => {
    describe("Given I start number routing greater than survey", () => {
      before(async () => {
        await browser.openQuestionnaire("test_routing_number_greater_than.json");
      });

      it("When I enter a number greater than 123, Then I should be routed to the correct page", async () => {
        await $(NumberQuestionPage.answer()).setValue(555);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter 123, Then I should be routed to the incorrect page", async () => {
        await $(CorrectAnswerPage.previous()).click();
        await $(NumberQuestionPage.answer()).setValue(123);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });

      it("When I enter a number less than 123, Then I should be routed to the incorrect page", async () => {
        await $(IncorrectAnswerPage.previous()).click();
        await $(NumberQuestionPage.answer()).setValue(2);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Less Than", () => {
    describe("Given I start number routing less than survey", () => {
      before(async () => {
        await browser.openQuestionnaire("test_routing_number_less_than.json");
      });

      it("When I enter a number less than 123, Then I should be routed to the correct page", async () => {
        await $(NumberQuestionPage.answer()).setValue(77);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter 123, Then I should be routed to the incorrect page", async () => {
        await $(CorrectAnswerPage.previous()).click();
        await $(NumberQuestionPage.answer()).setValue(123);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });

      it("When I enter a number greater than 123, Then I should be routed to the incorrect page", async () => {
        await $(IncorrectAnswerPage.previous()).click();
        await $(NumberQuestionPage.answer()).setValue(765);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Greater Than or Equal", () => {
    describe("Given I have number routing with a greater than or equal", () => {
      before(async () => {
        await browser.openQuestionnaire("test_routing_number_greater_than_or_equal.json");
      });

      it("When I enter a number greater than 123, Then I should be routed to the correct page", async () => {
        await $(NumberQuestionPage.answer()).setValue(555);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter 123, Then I should be routed to the correct page", async () => {
        await $(CorrectAnswerPage.previous()).click();
        await $(NumberQuestionPage.answer()).setValue(123);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a number less than 123, Then I should be routed to the incorrect page", async () => {
        await $(CorrectAnswerPage.previous()).click();
        await $(NumberQuestionPage.answer()).setValue(2);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Less Than or Equal", () => {
    describe("Given I have number routing with a less than or equal", () => {
      before(async () => {
        await browser.openQuestionnaire("test_routing_number_less_than_or_equal.json");
      });

      it("When I enter a number less than 123, Then I should be routed to the correct page", async () => {
        await $(NumberQuestionPage.answer()).setValue(23);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter 123, Then I should be routed to the correct page", async () => {
        await $(CorrectAnswerPage.previous()).click();
        await $(NumberQuestionPage.answer()).setValue(123);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a number larger than 123, Then I should be routed to the incorrect page", async () => {
        await $(CorrectAnswerPage.previous()).click();
        await $(NumberQuestionPage.answer()).setValue(546);
        await click(NumberQuestionPage.submit());
        await expect(await browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });
});
