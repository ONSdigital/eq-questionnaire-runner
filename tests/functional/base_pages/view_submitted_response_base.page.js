import BasePage from "./base.page";

class ViewSubmittedResponseBasePage extends BasePage {
  metadata() {
    return ".ons-description-list";
  }

  metadataTerm(number = 1) {
    return `.ons-description-list > dt:nth-of-type(${number})`;
  }

  metadataValue(number = 1) {
    return `.ons-description-list > dd:nth-of-type(${number})`;
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
