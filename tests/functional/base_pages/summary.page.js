import QuestionPage from "./question.page";

class SummmaryPage extends QuestionPage {
  constructor() {
    super("submit");
  }

  summary() {
    return `.summary`;
  }

  summaryRowState(sectionId) {
    return `[data-qa="${sectionId}"]`;
  }
}

export default new SummmaryPage();
