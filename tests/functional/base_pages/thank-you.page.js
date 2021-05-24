import BasePage from "./base.page";

class ThankYouPage extends BasePage {
  url() {
    return `/submitted/${this.pageName}`;
  }

  title() {
    return '[data-qa="title"]';
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
