const BasePage = require('./base.page');

class SectionSummaryPage extends BasePage {

  constructor(pageName) {
    super(pageName);
  }

  url() { return "/questionnaire/"; }

  myAccountLink() { return '#my-account'; }

  alert() { return '[data-qa="error-body"]';  }

  error() { return '.js-inpagelink'; }

  errorHeader() { return '#main-content > div.panel.panel--error.u-mb-s > div.panel__header > div'; }

  errorNumber(number = 1) { return '[data-qa="error-body"] ul > li:nth-child(' + number + ') > a'; }

  previous() { return 'a[id="top-previous"]'; }

  displayedName() { return 'h1'; }

  displayedDescription() { return 'p > strong'; }

  submit() { return '[data-qa="btn-submit"]'; }

  saveSignOut() { return '[data-qa="btn-save-sign-out"]'; }

  switchLanguage(language_code) { return 'a[href="?language_code=' + language_code + '"]'; }

  summaryItems() { return 'table.summary__items'; }

  summaryRowValues(number = 1) {
    return 'tbody:nth-child(' + number + ') tr td.summary__values';
  }

  summaryRowAction(number = 1) {
    return 'tbody:nth-child(' + number + ') tr td.summary__actions a';
  }

  summaryRowTitle(number = 1) {
    return 'tbody:nth-child(' + number + ') tr td.summary__item-title';
  }


 listCollectorHouseholdRowTitle(number = 1) {
    return '[data-qa=people-list-summary] tbody:nth-child(' + number + ') tr td.summary__item-title';
  }

  listCollectorHouseholdRowChange(number = 1) {
    return '[data-qa=people-list-summary] tbody:nth-child(' + number + ') [data-qa=change-item-link]';
  }

   listCollectorPeopleRowAdd() {
    return '[data-qa=people-list-summary] [data-qa=add-item-link]';
  }

 listCollectorHouseholdRowRemove(number = 1) {
    return '[data-qa=people-list-summary] tbody:nth-child(' + number + ') [data-qa=remove-item-link]';
  }

  listCollectorVisitorRowTitle(number = 1) {
    return '[data-qa=visitors-list-summary] tbody:nth-child(' + number + ') tr td.summary__item-title';
  }

  listCollectorVisitorRowChange(number = 1) {
    return '[data-qa=visitors-list-summary] tbody:nth-child(' + number + ') [data-qa=change-item-link]';
  }

  listCollectorVisitorRowRemove(number = 1) {
    return '[data-qa=visitors-list-summary] tbody:nth-child(' + number + ') [data-qa=remove-item-link]';
  }

  listCollectorVisitorRowAdd() {
    return '[data-qa=visitors-list-summary] [data-qa=add-item-link]';
  }

}

module.exports = new SectionSummaryPage();
