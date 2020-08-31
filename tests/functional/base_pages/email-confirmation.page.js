import QuestionPage from "./question.page";

class EmailConfirmationPage extends QuestionPage {
  constructor() {
    super("email-confirmation");
  }

  confirmationText() {
    return '[data-qa="confirmation-text"]';
  }

  sendAnotherEmail() {
    return 'a[id="send-another-email"]';
  }
}
export default new EmailConfirmationPage();
