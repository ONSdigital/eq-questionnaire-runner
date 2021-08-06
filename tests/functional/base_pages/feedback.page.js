import FeedbackBasePage from "./feedback-base.page.js";

class FeedbackPage extends FeedbackBasePage {
  feedbackTitle() {
    return '[data-qa="feedback-title"]';
  }

  feedbackType() {
    return "#feedback-type";
  }

  feedbackTypeCensusQuestions() {
    return "#feedback-type-0";
  }

  feedbackTypePageDesignAndStructure() {
    return "#feedback-type-1";
  }

  feedbackTypeGeneralFeedback() {
    return "#feedback-type-2";
  }

  feedbackText() {
    return "#feedback-text";
  }

  errorPanel() {
    return '[data-qa="error-body"]';
  }
}
export default new FeedbackPage("send");
