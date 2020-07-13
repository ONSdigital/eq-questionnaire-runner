import QuestionPage from "./question.page";

class ThankYouPage extends QuestionPage {
  constructor() {
    super("summary");
  }

  summaryRowState(sectionId) {
    return `[data-qa="${sectionId}"]`;
  }
}

export default new ThankYouPage();
