import QuestionOne from "../../../generated_pages/routing_answered_unanswered/block-1.page";
import QuestionOneAnswered from "../../../generated_pages/routing_answered_unanswered/answered-question-1.page";
import QuestionOneUnanswered from "../../../generated_pages/routing_answered_unanswered/unanswered-question-1.page";

import QuestionTwo from "../../../generated_pages/routing_answered_unanswered/block-2.page";
import QuestionTwoAnswered from "../../../generated_pages/routing_answered_unanswered/answered-question-2.page";
import QuestionTwoUnanswered from "../../../generated_pages/routing_answered_unanswered/unanswered-question-2.page";

import QuestionThree from "../../../generated_pages/routing_answered_unanswered/block-3.page";
import QuestionThreeAnsweredOrNotZero from "../../../generated_pages/routing_answered_unanswered/answered-question-3.page";
import QuestionThreeUnansweredOrAnswerZero from "../../../generated_pages/routing_answered_unanswered/unanswered-or-zero-question-3.page";

describe("Test routing question answered/unanswered", () => {
  describe("Given I am on the first question", () => {
    beforeEach("Load the questionnaire", () => {
      browser.openQuestionnaire("test_routing_answered_unanswered.json");
    });

    it("When I select any answer and submit, Then I should see a page saying I have answered the first question", () => {
      $(QuestionOne.ham()).click();
      $(QuestionOne.submit()).click();
      expect($(QuestionOneAnswered.heading()).getText()).to.contain("You answered the first question!");
      expect(browser.getUrl()).to.contain(QuestionOneAnswered.pageName);

      $(QuestionOneAnswered.previous()).click();
      $(QuestionOne.cheese()).click();
      $(QuestionOne.submit()).click();
      expect($(QuestionOneAnswered.heading()).getText()).to.contain("You answered the first question!");
      expect(browser.getUrl()).to.contain(QuestionOneAnswered.pageName);
    });

    it("When I don't select an answer and submit, Then I should see a page saying I have not answered the first question", () => {
      $(QuestionOne.submit()).click();
      expect($(QuestionOneAnswered.heading()).getText()).to.contain("You did not answer the first question!");
      expect(browser.getUrl()).to.contain(QuestionOneAnswered.pageName);
    });
  });

  describe("Given I am on the second question", () => {
    beforeEach("Load the questionnaire and get to the second question", () => {
      browser.openQuestionnaire("test_routing_answered_unanswered.json");

      $(QuestionOne.submit()).click();
      $(QuestionOneUnanswered.submit()).click();
    });

    it("When I select any answer and submit, Then I should see a page saying I have answered the second question", () => {
      $(QuestionTwo.pizzaHut()).click();
      $(QuestionTwo.submit()).click();
      expect($(QuestionTwoAnswered.heading()).getText()).to.contain("You answered the second question!");
      expect(browser.getUrl()).to.contain(QuestionTwoAnswered.pageName);

      $(QuestionOneAnswered.previous()).click();
      $(QuestionTwo.dominoS()).click();
      $(QuestionTwo.submit()).click();
      expect($(QuestionTwoAnswered.heading()).getText()).to.contain("You answered the second question!");
      expect(browser.getUrl()).to.contain(QuestionTwoAnswered.pageName);
    });

    it("When I don't select an answer and submit, Then I should see a page saying I have not answered the second question", () => {
      $(QuestionTwo.submit()).click();
      expect($(QuestionTwoUnanswered.heading()).getText()).to.contain("You did not answer the second question!");
      expect(browser.getUrl()).to.contain(QuestionTwoAnswered.pageName);
    });
  });

  describe("Given I am on the third question", () => {
    beforeEach("Load the questionnaire and get to the third question", () => {
      browser.openQuestionnaire("test_routing_answered_unanswered.json");

      $(QuestionOne.submit()).click();
      $(QuestionOneUnanswered.submit()).click();
      $(QuestionTwo.submit()).click();
      $(QuestionTwoUnanswered.submit()).click();
    });

    it("When I do not answer the question or answer `0` and submit, Then I should see a page saying I did not answer the question or that I chose `0`", () => {
      $(QuestionThree.submit()).click();
      expect($(QuestionThreeUnansweredOrAnswerZero.heading()).getText()).to.contain("You did not answer the question or chose 0 slices");
      expect(browser.getUrl()).to.contain(QuestionThreeUnansweredOrAnswerZero.pageName);

      $(QuestionThreeUnansweredOrAnswerZero.previous()).click();
      $(QuestionThree.answer3()).setValue("0");
      $(QuestionThree.submit()).click();
      expect($(QuestionThreeUnansweredOrAnswerZero.heading()).getText()).to.contain("You did not answer the question or chose 0 slices");
      expect(browser.getUrl()).to.contain(QuestionThreeUnansweredOrAnswerZero.pageName);
    });

    it("When I enter an answer greater than 0 and submit, Then I should see a page saying I chose at least one", () => {
      $(QuestionThree.answer3()).setValue("2");
      $(QuestionThree.submit()).click();
      expect($(QuestionTwoAnswered.heading()).getText()).to.contain("You chose at least 1 slice");
      expect(browser.getUrl()).to.contain(QuestionThreeAnsweredOrNotZero.pageName);
    });
  });
});
