import BasePage from "./base.page";

class FeedbackBasePage extends BasePage {
  constructor(pageName) {
    super(pageName);
    this.questions = [];
  }

  url() {
    return `/submitted/feedback/${this.pageName}`;
  }
}

export default FeedbackBasePage;
