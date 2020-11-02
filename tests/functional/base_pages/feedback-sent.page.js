import FeedbackBasePage from "./feedback-base.page.js";

class FeedbackSentPage extends FeedbackBasePage {
  constructor() {
    super("sent");
  }

  feedbackThankYouText() {
    return '[data-qa="feedback-thank-you-text"]';
  }

  doneButton() {
    return '[data-qa="btn-done"]';
  }
}
export default new FeedbackSentPage();
