import BasePage from "./base.page";

class QuestionPreviewBasePage extends BasePage {
  url() {
    return `/submitted/feedback/${this.pageName}`;
  }

  showButton() {
    return '[data-ga-category="Preview Survey"]';
  }
}

export default QuestionPreviewBasePage;
