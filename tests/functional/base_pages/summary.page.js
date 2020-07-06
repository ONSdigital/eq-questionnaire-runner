import QuestionPage from "./question.page";

class ThankYouPage extends QuestionPage {
  constructor() {
    super("summary");
  }

  summaryRowState(sectionId = "section-1") {
    return `[data-qa="hub-row-state-${sectionId}"]`;
  }
}

export default new ThankYouPage();
