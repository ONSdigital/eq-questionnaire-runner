import SchemaFeedbackPage from "../generated_pages/feedback/feedback.page";
import SubmitPage from "../generated_pages/feedback/submit.page";

import FeedbackPage from "../base_pages/feedback.page";
import FeedbackSentPage from "../base_pages/feedback-sent.page";
import ThankYouPage from "../base_pages/thank-you.page";

describe("Feedback", () => {
  describe("Given I launch and complete the test feedback survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_feedback.json");
      await $(SchemaFeedbackPage.submit()).click();
      await $(SubmitPage.submit()).click();
    });

    it("When I view the thank you page, Then I can see the feedback call to action", async () => {
      await expect(await browser.getUrl()).to.contain(ThankYouPage.pageName);
      await expect(await $(ThankYouPage.feedback()).getText()).to.contain("What do you think about this service?");
      await expect(await $(ThankYouPage.feedbackLink()).getText()).to.equal("Give feedback");
      await expect(await $(ThankYouPage.feedbackLink()).getAttribute("href")).to.contain("/submitted/feedback/send");
    });

    it("When I try to submit without providing feedback, then I stay on the feedback page and get an error message", async () => {
      await browser.url(FeedbackPage.url());
      await expect(await browser.getUrl()).to.contain(FeedbackPage.pageName);
      await expect(await $(FeedbackPage.feedbackTitle()).getText()).to.contain("Give feedback about this service");
      await $(FeedbackPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(FeedbackPage.pageName);
      await expect(await $(FeedbackPage.errorPanel()).isExisting()).to.be.true;
      await expect(await $(FeedbackPage.errorPanel()).getText()).to.contain(
        "There are 2 problems with your feedback\nSelect what your feedback is about\nEnter your feedback",
      );
    });

    it("When I enter valid feedback, Then I can submit the feedback page and get confirmation that the feedback has been sent", async () => {
      await browser.url(FeedbackPage.url());
      await $(FeedbackPage.feedbackTypeGeneralFeedback()).click();
      await $(FeedbackPage.feedbackText()).setValue("Well done!");
      await $(FeedbackPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(FeedbackSentPage.pageName);
      await expect(await $(FeedbackSentPage.feedbackThankYouText()).getText()).to.contain("Thank you for your feedback");
    });

    it("When I click the done button on the feedback sent page, Then I am taken to the thank you page", async () => {
      await browser.url(FeedbackPage.url());
      await $(FeedbackPage.feedbackTypeGeneralFeedback()).click();
      await $(FeedbackPage.feedbackText()).setValue("Well done!");
      await $(FeedbackPage.submit()).click();
      await $(FeedbackSentPage.doneButton()).click();
      await expect(await browser.getUrl()).to.contain("thank-you");
      await expect(await $(ThankYouPage.title()).getText()).to.contain("Thank you for completing the Feedback test schema");
    });
  });
});
