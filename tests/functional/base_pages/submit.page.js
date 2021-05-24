import BasePage from "./base.page";

class SubmitPage extends BasePage {
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
    return ".js-collapsible-all";
  }
}

export default new SubmitPage("submit");
