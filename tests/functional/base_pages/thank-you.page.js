import QuestionPage from "./question.page";

class ThankYouPage extends QuestionPage {
  constructor() {
    super("thank-you");
  }

  guidance() {
    return '[data-qa="guidance"]';
  }

  title() {
    return '[data-qa="title"]';
  }

  signOut() {
    return '[data-qa="btn-sign-out"]';
  }

  emailAddress() {
    return "#email";
  }

  submit() {
    return '[data-qa="btn-submit"]';
  }

  errorPanel() {
    return '[data-qa="error-body"]';
  }
}
export default new ThankYouPage();
