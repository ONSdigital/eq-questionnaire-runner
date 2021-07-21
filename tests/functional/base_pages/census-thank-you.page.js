import BasePage from "./base.page";

class CensusThankYouPage extends BasePage {
  title() {
    return '[data-qa="title"]';
  }

  exit() {
    return '[data-qa="btn-exit"]';
  }

  feedback() {
    return ".feedback";
  }

  feedbackLink() {
    return ".feedback a";
  }
}

export default new CensusThankYouPage("thank-you");
