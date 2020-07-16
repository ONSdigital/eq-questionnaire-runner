import QuestionPage from "./question.page";

class ThankYouPage extends QuestionPage {
  constructor() {
    super("thank-you");
  }

  guidance() {
   return '[data-qa="guidance"]';
  }

  title() {
    return '[data-qa="title"]';
  }

  signOut() {
    return '[data-qa="btn-sign-out"]';
  }

}
export default new ThankYouPage();
