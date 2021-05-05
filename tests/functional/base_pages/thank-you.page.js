import QuestionPage from "./question.page";

class ThankYouPage extends QuestionPage {
  constructor() {
    super("thank-you");
  }

  url() {
    return `/submitted/${this.pageName}`;
  }

  guidance() {
    return '[data-qa="guidance"]';
  }

  title() {
    return '[data-qa="title"]';
  }

  exitButton() {
    return '[data-qa="btn-exit"]';
  }

  email() {
    return "#email";
  }

  submit() {
    return '[data-qa="btn-submit"]';
  }

  errorPanel() {
    return '[data-qa="error-body"]';
  }

  feedback() {
    return ".feedback";
  }

  feedbackLink() {
    return ".feedback__link";
  }
}
export default new ThankYouPage();
