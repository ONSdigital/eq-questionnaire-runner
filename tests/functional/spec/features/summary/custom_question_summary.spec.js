const AddressBlockPage = require('../../../generated_pages/custom_question_summary/address.page.js');
const NameBlockPage = require('../../../generated_pages/custom_question_summary/name.page.js');
const SummaryPage = require('../../../generated_pages/custom_question_summary/summary.page.js');

const BaseSummaryPage = require('../../../base_pages/summary.page.js');

describe('Summary Screen', function() {
  beforeEach('Load the survey', function () {
    browser.openQuestionnaire('test_custom_question_summary.json');
  });

  it('Given a survey has question summary concatenations and has been completed when on the summary page then the correct response should be displayed formatted correctly', function() {
    completeAllQuestions();
    expect($(BaseSummaryPage.summaryRowState(1)).getText()).to.contain('John Smith');
    expect($(BaseSummaryPage.summaryRowState(2)).getText()).to.contain('Cardiff Road\nNewport\nNP10 8XG');
  });

  it('Given no values are entered in a question with multiple answers and concatenation set, when on the summary screen then the correct response should be displayed', function() {
    $(NameBlockPage.submit()).click();
    $(AddressBlockPage.submit()).click();
    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(BaseSummaryPage.summaryRowState(1)).getText()).to.contain('No answer provided');
  });

  function completeAllQuestions() {
    $(NameBlockPage.first()).setValue('John');
    $(NameBlockPage.last()).setValue('Smith');
    $(NameBlockPage.submit()).click();
    $(AddressBlockPage.line1()).setValue('Cardiff Road');
    $(AddressBlockPage.townCity()).setValue('Newport');
    $(AddressBlockPage.postcode()).setValue('NP10 8XG');
    $(AddressBlockPage.submit()).click();

    let expectedUrl = browser.getUrl();

    expect(expectedUrl).to.contain(SummaryPage.pageName);
  }
});
