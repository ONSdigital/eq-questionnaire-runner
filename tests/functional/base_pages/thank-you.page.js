import QuestionPage from "./question.page";

class ThankYouPage extends QuestionPage {
  constructor() {
    super("thank-you");
  }

  submissionSuccessfulTitle() {
    return '[data-qa="submission-successful-title"]';
  }

  viewSubmitted() {
    return '[data-qa="view-submission"]';
  }

  viewSubmissionExpired() {
    return '[data-qa="view-submission-expired"]';
  }

  signOut() {
    return '[data-qa="btn-sign-out"]';
  }
}
export default new ThankYouPage();
