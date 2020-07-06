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

  displayedName() {
    return "h1";
  }

  displayedGuidance() {
    return '[data-qa="displayed-guidance"]';
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

  summaryRowState(sectionId = "section-1") {
    return `[data-qa="hub-row-state-${sectionId}"]`;
  }

  summaryRowLink(sectionId = "section-1") {
    return `[data-qa="hub-row-link-${sectionId}"]`;
  }

  summaryRowTitle(sectionId = "section-1") {
    return `[data-qa="hub-row-title-${sectionId}"]`;
  }
}

export default new HubPage();
