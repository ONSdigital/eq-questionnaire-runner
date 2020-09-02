import BasePage from "./base.page";

class IntroductionPage extends BasePage {
  myAccountLink() {
    return "#my-account";
  }

  exitButton() {
    return '[data-qa="btn-exit"]';
  }

  getStarted() {
    return ".qa-btn-get-started";
  }

  useOfInformation() {
    return "#use-of-information";
  }

  useOfData() {
    return "#how-we-use-your-data";
  }

  legalResponse() {
    return '[data-qa="legal-response"]';
  }

  legalBasis() {
    return '[data-qa="legal-basis"]';
  }

  introDescription() {
    return "#use-of-information p";
  }

  introTitleDescription() {
    return '[data-qa="details-changed-title"]';
  }
}

export default IntroductionPage;
