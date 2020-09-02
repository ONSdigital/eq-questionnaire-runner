import QuestionPage from "./question.page";

class ConfirmationEmailSentPage extends QuestionPage {
  constructor() {
    super("email-confirmation");
  }

  title() {
    return '[data-qa="title"]';
  }

  email() {
    return "#email";
  }

  submit() {
    return '[data-qa="btn-submit"]';
  }

  errorPanel() {
    return `[data-qa=error-body] div.panel__body > ul`;
  }
}
export default new ConfirmationEmailSentPage();
