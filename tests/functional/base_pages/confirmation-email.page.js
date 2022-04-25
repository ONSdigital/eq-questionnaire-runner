import BasePage from "./base.page";

class ConfirmationEmailSentPage extends BasePage {
  title() {
    return '[data-qa="title"]';
  }

  email() {
    return "#email";
  }

  errorPanel() {
    return `[data-qa=error-body] div.ons-panel__body > [data-qa=error-list]`;
  }

  feedback() {
    return ".ons-feedback";
  }
}
export default new ConfirmationEmailSentPage("email-confirmation");
