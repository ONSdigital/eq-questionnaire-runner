import BasePage from "./base.page";

class QuestionBasePage extends BasePage {
  constructor(pageName) {
    super(pageName);
    this.questions = [];
  }

  url() {
    return `/questionnaire/${this.pageName}`;
  }

  questionText() {
    return this.heading();
  }

  alert() {
    return '[data-qa="error-body"]';
  }

  error() {
    return ".ons-js-inpagelink";
  }

  legend() {
    return "legend";
  }

  errorHeader() {
    return '[data-qa="error-header"]';
  }

  errorNumber(number = 1) {
    return `[data-qa="error-link-${number}"]`;
  }

  cancelAndReturn() {
    return 'a[id="cancel-and-return"]';
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
}

export default QuestionBasePage;
