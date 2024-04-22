import FeedbackBasePage from "./feedback-base.page.js";

class FeedbackSentBasePage extends FeedbackBasePage {
  feedbackThankYouText() {
    return '[data-qa="feedback-thank-you-text"]';
  }

  doneButton() {
    return '[data-qa="btn-done"]';
  }
}
export default new FeedbackSentBasePage("sent");
