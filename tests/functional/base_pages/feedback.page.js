import FeedbackBasePage from "./feedback-base.page.js";

class FeedbackPage extends FeedbackBasePage {
  constructor() {
    super("send");
  }

  feedbackTitle() {
    return '[data-qa="feedback-title"]';
  }

  feedbackType() {
    return "#feedback-type";
  }

  feedbackText() {
    return "#feedback-text";
  }

  errorPanel() {
    return '[data-qa="error-body"]';
  }
}
export default new FeedbackPage();
