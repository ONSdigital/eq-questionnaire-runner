import BasePage from "./base.page";

class ViewSubmittedResponseBasePage extends BasePage {
  metadata() {
    return ".ons-metadata";
  }

  metadataTerm(number = 1) {
    return `.ons-metadata > dt:nth-of-type(${number})`;
  }

  metadataValue(number = 1) {
    return `.ons-metadata > dd:nth-of-type(${number})`;
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
