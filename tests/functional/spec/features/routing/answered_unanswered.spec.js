import QuestionOne from "../../../generated_pages/new_routing_answered_unanswered/block-1.page";
import QuestionOneAnswered from "../../../generated_pages/new_routing_answered_unanswered/answered-question-1.page";
import QuestionOneUnanswered from "../../../generated_pages/new_routing_answered_unanswered/unanswered-question-1.page";

import QuestionTwo from "../../../generated_pages/new_routing_answered_unanswered/block-2.page";
import QuestionTwoAnswered from "../../../generated_pages/new_routing_answered_unanswered/answered-question-2.page";
import QuestionTwoUnanswered from "../../../generated_pages/new_routing_answered_unanswered/unanswered-question-2.page";

import QuestionThree from "../../../generated_pages/new_routing_answered_unanswered/block-3.page";
import QuestionThreeAnsweredOrNotOne from "../../../generated_pages/new_routing_answered_unanswered/answered-question-3.page";
import QuestionThreeUnansweredOrAnswerOne from "../../../generated_pages/new_routing_answered_unanswered/unanswered-or-not-say-question-3.page";

describe("Test routing question answered/unanswered", () => {
  describe("Given I am on the first question", () => {
    beforeEach("Load the questionnaire", () => {
      browser.openQuestionnaire("test_new_routing_answered_unanswered.json");
    });

    it("When I select any answer and and submit, Then I should see a page saying I have answered the first question", () => {
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
      browser.openQuestionnaire("test_new_routing_answered_unanswered.json");

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
      browser.openQuestionnaire("test_new_routing_answered_unanswered.json");

      $(QuestionOne.submit()).click();
      $(QuestionOneUnanswered.submit()).click();
      $(QuestionTwo.submit()).click();
      $(QuestionTwoUnanswered.submit()).click();
    });

    it("When I do not answer the question or answer `1` and submit, Then I should see a page saying I did not answer the question or that I chose `1`", () => {
      $(QuestionThree.submit()).click();
      expect($(QuestionThreeUnansweredOrAnswerOne.heading()).getText()).to.contain('You did not answer the question or chose "1 slice"');
      expect(browser.getUrl()).to.contain(QuestionThreeUnansweredOrAnswerOne.pageName);

      $(QuestionThreeUnansweredOrAnswerOne.previous()).click();
      $(QuestionThree.answer3()).setValue("1");
      $(QuestionThree.submit()).click();
      expect($(QuestionThreeUnansweredOrAnswerOne.heading()).getText()).to.contain('You did not answer the question or chose "1 slice"');
      expect(browser.getUrl()).to.contain(QuestionThreeUnansweredOrAnswerOne.pageName);
    });

    it("When I enter an answer great than 1 and submit, Then I should see a page saying I chose more than 1", () => {
      $(QuestionThree.answer3()).setValue("2");
      $(QuestionThree.submit()).click();
      expect($(QuestionTwoAnswered.heading()).getText()).to.contain("You chose more than 1 slice");
      expect(browser.getUrl()).to.contain(QuestionThreeAnsweredOrNotOne.pageName);
    });
  });
});
