import QuestionPage from "./question.page";

class FeedbackSentPage extends QuestionPage {
  constructor() {
    super("feedback/sent");
  }

  feedbackThankYouText() {
    return '[data-qa="feedback-thank-you-text"]';
  }
}
export default new FeedbackSentPage();
