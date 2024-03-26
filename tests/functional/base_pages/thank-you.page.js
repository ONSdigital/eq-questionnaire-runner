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

  viewSubmittedGuidance() {
    return '[id="view-submitted-response-guidance"]';
  }

  viewSubmittedCountdown() {
    return '[id="view-submitted-response-countdown"]';
  }

  metadata() {
    return ".ons-description-list";
  }

  exitButton() {
    return '[data-qa="btn-exit"]';
  }

  savePrintAnswersLink() {
    return '[id="view-submitted-response-link"]';
  }

  email() {
    return "#email";
  }

  errorPanel() {
    return '[data-qa="error-body"]';
  }

  feedback() {
    return ".ons-feedback";
  }

  feedbackLink() {
    return ".ons-feedback__link";
  }
}
export default new ThankYouPage("thank-you");
