import BasePage from "./base.page";

class ConfirmationPage extends BasePage {
  url() {
    return "/questionnaire/submit";
  }

  previous() {
    return 'a[id="top-previous"]';
  }

  heading() {
    return "h1";
  }

  warning() {
    return '[data-qa="warning"]';
  }

  guidance() {
    return '[data-qa="guidance"]';
  }

  submit() {
    return '[data-qa="btn-submit"]';
  }

  saveSignOut() {
    return '[data-qa="btn-save-sign-out"]';
  }

  switchLanguage(languageCode) {
    return `a[href="?language_code=${languageCode}"]`;
  }
}

export default new ConfirmationPage("confirmation");
