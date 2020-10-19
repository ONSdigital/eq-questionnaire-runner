import QuestionPage from "./question.page";

class FeedbackPage extends QuestionPage {
  constructor() {
    super("feedback/send");
  }

  title() {
    return '[data-qa="title"]';
  }

  feedbackType() {
    return "#feedback-type";
  }

  feedbackText() {
    return "#feedback-text";
  }

  submit() {
    return '[data-qa="btn-submit"]';
  }

  errorPanel() {
    return '[data-qa="error-body"]';
  }
}
export default new FeedbackPage();
