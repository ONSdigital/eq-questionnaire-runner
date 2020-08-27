import QuestionPage from "./question.page";

class EmailConfirmationSentPage extends QuestionPage {
  constructor() {
    super("email-confirmation-sent");
  }

  title() {
    return '[data-qa="title"]';
  }

  sendAnotherEmail() {
    return 'a[id="send-another-email"]';
  }
}
export default new EmailConfirmationSentPage();
