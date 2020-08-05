import BasePage from "./base.page";

class HubPage extends BasePage {
  url() {
    return "/questionnaire/";
  }

  myAccountLink() {
    return "#my-account";
  }

  alert() {
    return '[data-qa="error-body"]';
  }

  error() {
    return ".js-inpagelink";
  }

  errorHeader() {
    return '[data-qa="error-header"]';
  }

  errorNumber(number = 1) {
    return `[data-qa="error-link-${number}"]`;
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

  summaryItems() {
    return "table.summary__items";
  }

  summaryRowState(sectionId) {
    return `[data-qa="hub-row-${sectionId}-state"]`;
  }

  summaryRowLink(sectionId) {
    return `[data-qa="hub-row-${sectionId}-link"]`;
  }

  summaryRowTitle(sectionId) {
    return `[data-qa="hub-row-${sectionId}-title"]`;
  }
}

export default new HubPage();
