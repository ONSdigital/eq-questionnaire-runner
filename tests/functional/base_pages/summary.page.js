const QuestionPage = require('./question.page');

class ThankYouPage extends QuestionPage {
  constructor() {
    super('summary');
  }

  viewSubmissionText() {
    return '[data-qa="view-submission-text"]';
  }

  summaryRowState(number = 1) {
    return 'tbody:nth-child(' + number + ') tr td.summary__values';
  }
}

module.exports = new ThankYouPage();
