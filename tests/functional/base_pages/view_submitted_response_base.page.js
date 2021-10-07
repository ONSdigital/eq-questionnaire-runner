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

  printButton() {
    return '[data-qa="btn-print"]';
  }
}

export default ViewSubmittedResponseBasePage;
