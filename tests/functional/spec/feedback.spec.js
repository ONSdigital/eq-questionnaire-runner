import SchemaFeedbackPage from "../generated_pages/feedback/feedback.page";
import SubmitPage from "../generated_pages/feedback/submit.page";

import FeedbackPage from "../base_pages/feedback.page";
import FeedbackSentPage from "../base_pages/feedback-sent.page";
import ThankYouPage from "../base_pages/thank-you.page";
import { click } from "../helpers";

describe("Feedback", () => {
  describe("Given I launch and complete the test feedback survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_feedback.json");
      await click(SchemaFeedbackPage.submit());
      await click(SubmitPage.submit());
    });

    it("When I view the thank you page, Then I can see the feedback call to action", async () => {
      await expect(browser).toHaveUrlContaining(ThankYouPage.pageName);
      await expect(await $(ThankYouPage.feedback()).getText()).toContain("What do you think about this service?");
      await expect(await $(ThankYouPage.feedbackLink()).getText()).toBe("Give feedback");
      await expect(await $(ThankYouPage.feedbackLink()).getAttribute("href")).toContain("/submitted/feedback/send");
    });

    it("When I try to submit without providing feedback, then I stay on the feedback page and get an error message", async () => {
      await browser.url(FeedbackPage.url());
      await expect(browser).toHaveUrlContaining(FeedbackPage.pageName);
      await expect(await $(FeedbackPage.feedbackTitle()).getText()).toBe("Give feedback about this service");
      await click(FeedbackPage.submit());
      await expect(browser).toHaveUrlContaining(FeedbackPage.pageName);
      await expect(await $(FeedbackPage.errorPanel()).isExisting()).toBe(true);
      await expect(await $(FeedbackPage.errorPanel()).getText()).toBe(
        "There are 2 problems with your feedback\nSelect what your feedback is about\nEnter your feedback",
      );
    });

    it("When I enter valid feedback, Then I can submit the feedback page and get confirmation that the feedback has been sent", async () => {
      await browser.url(FeedbackPage.url());
      await $(FeedbackPage.feedbackTypeGeneralFeedback()).click();
      await $(FeedbackPage.feedbackText()).setValue("Well done!");
      await click(FeedbackPage.submit());
      await expect(browser).toHaveUrlContaining(FeedbackSentPage.pageName);
      await expect(await $(FeedbackSentPage.feedbackThankYouText()).getText()).toBe("Thank you for your feedback");
    });

    it("When I click the done button on the feedback sent page, Then I am taken to the thank you page", async () => {
      await browser.url(FeedbackPage.url());
      await $(FeedbackPage.feedbackTypeGeneralFeedback()).click();
      await $(FeedbackPage.feedbackText()).setValue("Well done!");
      await click(FeedbackPage.submit());
      await $(FeedbackSentPage.doneButton()).click();
      await expect(browser).toHaveUrlContaining("thank-you");
      await expect(await $(ThankYouPage.title()).getText()).toBe("Thank you for completing the Feedback test schema");
    });
  });
});
