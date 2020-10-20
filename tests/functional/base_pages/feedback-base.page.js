import BasePage from "./base.page";

class FeedbackBasePage extends BasePage {
  constructor(pageName) {
    super(pageName);
    this.questions = [];
  }

  url() {
    return `/submitted/feedback/${this.pageName}`;
  }

  previous() {
    return 'a[id="top-previous"]';
  }

  submit() {
    return '[data-qa="btn-submit"]';
  }
}

export default FeedbackBasePage;
