import QuestionPage from "./question.page";

class CensusThankYouPage extends QuestionPage {
  constructor() {
    super("thank-you");
  }

  guidance() {
    return '[data-qa="guidance"]';
  }

  title() {
    return '[data-qa="title"]';
  }

  exit() {
    return '[data-qa="btn-exit"]';
  }
}

export default new CensusThankYouPage();
