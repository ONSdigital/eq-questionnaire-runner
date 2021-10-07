import BasePage from "./base.page";

class CensusThankYouPage extends BasePage {
  title() {
    return '[data-qa="title"]';
  }

  exit() {
    return '[data-qa="btn-exit"]';
  }

  feedback() {
    return ".ons-feedback";
  }

  feedbackLink() {
    return ".ons-feedback__link";
  }
}

export default new CensusThankYouPage("thank-you");
