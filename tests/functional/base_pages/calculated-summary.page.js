import QuestionPage from "./question.page";

class CalculatedSummaryPage extends QuestionPage {
  calculatedSummaryTitle() {
    return '[data-qa="calculated-summary-title"]';
  }

  calculatedSummaryQuestion() {
    return "[data-qa=calculated-summary-question]";
  }

  calculatedSummaryAnswer() {
    return "[data-qa=calculated-summary-answer]";
  }
}

export default CalculatedSummaryPage;
