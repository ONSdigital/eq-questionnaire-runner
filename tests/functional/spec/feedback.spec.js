import SchemaFeedbackPage from "../generated_pages/feedback/feedback.page";
import SummaryPage from "../generated_pages/feedback/summary.page";

import FeedbackPage from "../base_pages/feedback.page";
import FeedbackSentPage from "../base_pages/feedback-sent.page";

describe("Feedback", () => {
  describe("Given I launch and complete the test feedback survey", () => {
    before(() => {
      browser.openQuestionnaire("test_feedback.json");
      $(SchemaFeedbackPage.submit()).click();
      $(SummaryPage.submit()).click();
    });

    it("When I try to submit without providing feedback, then I stay on the feedback page and get an error message", () => {
      browser.url("/submitted/feedback/send");
      expect(browser.getUrl()).to.contain(FeedbackPage.pageName);
      $(FeedbackPage.submit()).click();
      expect(browser.getUrl()).to.contain(FeedbackPage.pageName);
      expect($(FeedbackPage.errorPanel()).isExisting()).to.be.true;
      expect($(FeedbackPage.errorPanel()).getText()).to.contain("There are 2 problems with your answer");
      expect($(FeedbackPage.errorPanel()).getText()).to.contain("1. Select what your feedback is about");
      expect($(FeedbackPage.errorPanel()).getText()).to.contain("2. Enter your feedback");
    });

    it("When I enter valid feedback, Then I can submit the feedback page and get confirmation that the feedback has been sent", () => {
      browser.url("/submitted/feedback/send");
      expect(browser.getUrl()).to.contain(FeedbackPage.pageName);
      $(FeedbackPage.feedbackType()).click();
      $(FeedbackPage.feedbackText()).setValue("The census questions");
      $(FeedbackPage.submit()).click();
      expect(browser.getUrl()).to.contain(FeedbackSentPage.pageName);
      expect($(FeedbackSentPage.feedbackThankYouText()).getText()).to.contain("Thank you for your feedback");
    });
  });
});
