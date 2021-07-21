import BasePage from "./base.page";

class ConfirmationEmailSentPage extends BasePage {
  title() {
    return '[data-qa="title"]';
  }

  email() {
    return "#email";
  }

  errorPanel() {
    return `[data-qa=error-body] div.panel__body > ol`;
  }

  feedback() {
    return ".feedback";
  }
}
export default new ConfirmationEmailSentPage("email-confirmation");
