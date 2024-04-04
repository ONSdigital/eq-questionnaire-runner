import BasePage from "./base.page";

class IntroductionBasePage extends BasePage {
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

  previewQuestions() {
    return 'a[href="/questionnaire/preview"]';
  }

  introQuestion(number = 1) {
    return `#intro-questions-${number}`;
  }
}

export default IntroductionBasePage;
export const IntroductionPage = new IntroductionBasePage("introduction");
