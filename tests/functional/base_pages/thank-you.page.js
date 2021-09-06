import BasePage from "./base.page";

class ThankYouPage extends BasePage {
  url() {
    return `/submitted/${this.pageName}`;
  }

  title() {
    return '[data-qa="title"]';
  }

  viewAnswersTitle() {
    return '[data-qa="view-submitted-response-title"]';
  }

  viewAnswersLink() {
    return 'a[id="view-submitted-response-link"]';
  }

  viewSubmittedWarning() {
    return '[id="view-submitted-response-warning"]';
  }

  metadata() {
    return ".metadata";
  }

  exitButton() {
    return '[data-qa="btn-exit"]';
  }

  email() {
    return "#email";
  }

  errorPanel() {
    return '[data-qa="error-body"]';
  }

  feedback() {
    return ".feedback";
  }
}
export default new ThankYouPage("thank-you");
