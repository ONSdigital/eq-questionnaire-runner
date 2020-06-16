import QuestionPage from "./question.page";

class ThankYouPage extends QuestionPage {
  constructor() {
    super("summary");
  }

  summaryRowState(number = 1) {
    return `tbody:nth-child(${number}) tr td.summary__values`;
  }
}

export default new ThankYouPage();
