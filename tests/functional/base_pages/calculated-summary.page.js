import BasePage from "./base.page";

class CalculatedSummaryPage extends BasePage {
  calculatedSummaryTitle() {
    return '[data-qa="calculated-summary-title"]';
  }

  calculatedSummaryQuestion() {
    return "[data-qa=calculated-summary-question]";
  }

  calculatedSummaryAnswer() {
    return "[data-qa=calculated-summary-answer]";
  }

  summaryItems() {
    return "dl.ons-summary__items";
  }
}

export default CalculatedSummaryPage;
