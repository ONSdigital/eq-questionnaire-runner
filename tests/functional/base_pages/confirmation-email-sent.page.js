import BasePage from "./base.page";

class ConfirmationEmailSentPage extends BasePage {
  confirmationText() {
    return '[data-qa="confirmation-text"]';
  }

  sendAnotherEmail() {
    return 'a[id="send-another-email"]';
  }

  feedback() {
    return ".feedback";
  }

  feedbackLink() {
    return ".feedback__link";
  }
}
export default new ConfirmationEmailSentPage("email-confirmation");
