import BasePage from "./base.page";

class ConfirmEmailPage extends BasePage {
  questionTitle() {
    return '[data-qa="confirm-email-title"]';
  }

  yes() {
    return "#confirm-email-0";
  }

  no() {
    return "#confirm-email-1";
  }

  errorPanel() {
    return `[data-qa=error-body] div.panel__body > ol`;
  }
}
export default new ConfirmEmailPage("confirm-email");
