import QuestionPage from "./question.page";

class ConfirmEmailPage extends QuestionPage {
  constructor() {
    super("confirm-email");
  }

  questionTitle() {
    return '[data-qa="confirm-email-title"]';
  }

  yes() {
    return "#confirm-email-0";
  }

  no() {
    return "#confirm-email-1";
  }

  submit() {
    return '[data-qa="btn-submit"]';
  }

  errorPanel() {
    return `[data-qa=error-body] div.panel__body > ol`;
  }
}
export default new ConfirmEmailPage();
