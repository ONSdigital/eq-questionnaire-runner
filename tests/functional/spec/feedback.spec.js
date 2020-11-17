import SchemaFeedbackPage from "../generated_pages/feedback/feedback.page";
import SummaryPage from "../generated_pages/feedback/summary.page";

import FeedbackPage from "../base_pages/feedback.page";
import FeedbackSentPage from "../base_pages/feedback-sent.page";
import CensusThankYouPage from "../base_pages/census-thank-you.page";

describe("Feedback", () => {
  describe("Given I launch and complete the test feedback survey", () => {
    before(() => {
      browser.openQuestionnaire("test_feedback.json");
      $(SchemaFeedbackPage.submit()).click();
      $(SummaryPage.submit()).click();
    });

    it("When I view the thank you page, Then I can see the feedback call to action", () => {
      expect(browser.getUrl()).to.contain(CensusThankYouPage.pageName);
      expect($(CensusThankYouPage.feedback()).getText()).to.contain("What do you think about this service?");
      expect($(CensusThankYouPage.feedbackLink()).getAttribute("href")).to.contain("/submitted/feedback/send");
    });

    it("When I try to submit without providing feedback, then I stay on the feedback page and get an error message", () => {
      browser.url(FeedbackPage.url());
      expect(browser.getUrl()).to.contain(FeedbackPage.pageName);
      expect($(FeedbackPage.feedbackTitle()).getText()).to.contain("Give feedback about this service");
      $(FeedbackPage.submit()).click();
      expect(browser.getUrl()).to.contain(FeedbackPage.pageName);
      expect($(FeedbackPage.errorPanel()).isExisting()).to.be.true;
      expect($(FeedbackPage.errorPanel()).getText()).to.contain("There are 2 problems with your feedback");
      expect($(FeedbackPage.errorPanel()).getText()).to.contain("1. Select what your feedback is about");
      expect($(FeedbackPage.errorPanel()).getText()).to.contain("2. Enter your feedback");
    });

    it("When I enter valid feedback, Then I can submit the feedback page and get confirmation that the feedback has been sent", () => {
      browser.url(FeedbackPage.url());
      $(FeedbackPage.feedbackType()).click();
      $(FeedbackPage.feedbackText()).setValue("The census questions");
      $(FeedbackPage.submit()).click();
      expect(browser.getUrl()).to.contain(FeedbackSentPage.pageName);
      expect($(FeedbackSentPage.feedbackThankYouText()).getText()).to.contain("Thank you for your feedback");
    });

    it("When I click the done button on the feedback sent page, Then I am taken to the thank you page", () => {
      browser.url(FeedbackPage.url());
      $(FeedbackPage.feedbackType()).click();
      $(FeedbackPage.feedbackText()).setValue("The census questions");
      $(FeedbackPage.submit()).click();
      $(FeedbackSentPage.doneButton()).click();
      expect(browser.getUrl()).to.contain("thank-you");
      expect($(CensusThankYouPage.title()).getText()).to.contain("Thank you for completing the census");
    });
  });
});
