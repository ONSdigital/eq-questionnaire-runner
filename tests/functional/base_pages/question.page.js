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
    return '[data-qa="error-header"]';
  }

  errorList() {
    return '[data-qa="error-list"]';
  }

  errorNumber(number = 1) {
    return `[data-qa="error-link-${number}"]`;
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

  individualResponseGuidance() {
    return '[data-qa="individual-response-url"]';
  }

  lastViewedQuestionGuidance() {
    return "#last-viewed-question-guidance";
  }

  lastViewedQuestionGuidanceLink() {
    return "#section-start-link";
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

  warning() {
    return '[data-qa="warning"]';
  }

  guidance() {
    return '[data-qa="guidance"]';
  }
}

export default QuestionPage;
