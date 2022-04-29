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
    return `[data-qa=error-body] div.ons-panel__body > [data-qa=error-list]`;
  }
}
export default new ConfirmEmailPage("confirm-email");
