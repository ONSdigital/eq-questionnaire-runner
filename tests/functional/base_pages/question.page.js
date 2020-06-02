import BasePage from "./base.page";

class QuestionPage extends BasePage {
  constructor(pageName) {
    super(pageName);
    this.questions = [];
  }

  url() {
    return `/questionnaire/${this.pageName}`;
  }

  myAccountLink() {
    return "#my-account";
  }

  summaryQuestionText() {
    return ".summary__item-title";
  }

  questionText() {
    return "h1";
  }

  alert() {
    return '[data-qa="error-body"]';
  }

  error() {
    return ".js-inpagelink";
  }

  errorHeader() {
    return "#main-content > div.panel.panel--error.u-mb-s > div.panel__header > div";
  }

  errorNumber(number = 1) {
    return `[data-qa="error-body"] ul > li:nth-child(${number}) > a`;
  }

  previous() {
    return 'a[id="top-previous"]';
  }

  cancelAndReturn() {
    return 'a[id="cancel-and-return"]';
  }

  displayedName() {
    return '[data-qa="block-title"]';
  }

  displayedDescription() {
    return '[data-qa="block-description"]';
  }

  lastViewedQuestionGuidance() {
    return "#last-viewed-question-guidance";
  }

  lastViewedQuestionGuidanceLink() {
    return "#last-viewed-question-guidance > div.panel__body > a";
  }

  submit() {
    return '[data-qa="btn-submit"]';
  }

  summaryShowAllButton() {
    return ".js-collapsible-all";
  }

  saveSignOut() {
    return '[data-qa="btn-save-sign-out"]';
  }

  switchLanguage(languageCode) {
    return `a[href="?language_code=${languageCode}"]`;
  }

  returnToHubLink() {
    return 'a[href="/questionnaire/"]';
  }
}

export default QuestionPage;
