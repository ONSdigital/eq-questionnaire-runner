import BasePage from "./base.page";

class SubmitBasePage extends BasePage {
  url() {
    return `/questionnaire/${this.pageName}`;
  }

  summary() {
    return `.summary`;
  }

  summaryRowState(sectionId) {
    return `[data-qa="${sectionId}"]`;
  }

  summaryShowAllButton() {
    return ".ons-accordion__toggle-all";
  }
}

export default SubmitBasePage;
export const SubmitPage = new SubmitBasePage("submit");
