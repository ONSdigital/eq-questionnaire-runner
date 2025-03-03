import BasePage from "./base.page";

class ViewSubmittedResponseBasePage extends BasePage {
  metadata() {
    return ".ons-description-list";
  }

  metadataTerm(number = 1) {
    return `.ons-description-list > .ons-description-list__item:nth-of-type(${number}) > dt`;
  }

  metadataValue(number = 1) {
    return `.ons-description-list > .ons-description-list__item:nth-of-type(${number}) > dd`;
  }

  informationPanel() {
    return '[id="view-submitted-guidance"]';
  }

  printButton() {
    return '[data-qa="btn-print"]';
  }

  downloadButton() {
    return '[data-qa="btn-pdf"]';
  }
}

export default ViewSubmittedResponseBasePage;
