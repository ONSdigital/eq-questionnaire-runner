import BasePage from "./base.page";

class SummaryResponsePage extends BasePage {
  url() {
    return `/submitted/${this.pageName}`;
  }

  summary() {
    return `.summary`;
  }

  summaryRowState(sectionId) {
    return `[data-qa="${sectionId}"]`;
  }
}
export default new SummaryResponsePage("view-response");
