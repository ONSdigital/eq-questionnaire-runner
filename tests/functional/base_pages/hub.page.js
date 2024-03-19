import BasePage from "./base.page";

class HubPage extends BasePage {
  url() {
    return `/${this.pageName}/`;
  }

  summaryItems() {
    return "dl.ons-summary__items";
  }

  summaryRowState(sectionId) {
    return `[data-qa="hub-row-${sectionId}-state"]`;
  }

  summaryRowLink(sectionId) {
    return `[data-qa="hub-row-${sectionId}-link"]`;
  }

  summaryRowTitle(sectionId) {
    return `[data-qa="hub-row-${sectionId}-title"]`;
  }
}

export default new HubPage("questionnaire");
