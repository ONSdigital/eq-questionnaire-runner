import BasePage from "./base.page";

class ConfirmationEmailSentPage extends BasePage {
  confirmationText() {
    return '[data-qa="confirmation-text"]';
  }

  sendAnotherEmail() {
    return 'a[id="send-another-email"]';
  }

  feedback() {
    return ".ons-feedback";
  }

  feedbackLink() {
    return ".ons-feedback__link";
  }
}
export default new ConfirmationEmailSentPage("email-confirmation");
