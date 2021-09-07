import BasePage from "./base.page";

class ViewSubmittedResponseBasePage extends BasePage {
  metadata() {
    return ".metadata";
  }

  metadataTerm(number = 1) {
    return `.metadata > dt:nth-of-type(${number})`;
  }

  metadataValue(number = 1) {
    return `.metadata > dd:nth-of-type(${number})`;
  }

  printButton() {
    return '[data-qa="btn-print"]';
  }
}

export default ViewSubmittedResponseBasePage;
