import BasePage from "./base.page";

class GrandCalculatedSummaryBasePage extends BasePage {
  grandCalculatedSummaryTitle() {
    return '[data-qa="grand-calculated-summary-title"]';
  }

  grandCalculatedSummaryQuestion() {
    return "[data-qa=grand-calculated-summary-question]";
  }

  grandCalculatedSummaryAnswer() {
    return "[data-qa=grand-calculated-summary-answer]";
  }
}

export default GrandCalculatedSummaryBasePage;
