const BasePage = require('./base.page');

class SectionSummaryPage extends BasePage {

  displayedName() { return 'h1'; }

  displayedDescription() { return 'p > strong'; }

  listCollectorPeopleRowAdd() {
    return '[data-qa=people-list-summary] [data-qa=add-item-link]';
  }

  listCollectorPeopleRowChange(number = 1) {
    return '[data-qa=people-list-summary] tbody:nth-child(' + number + ') [data-qa=change-item-link]';
  }

  listCollectorPeopleRowRemove(number = 1) {
    return '[data-qa=people-list-summary] tbody:nth-child(' + number + ') [data-qa=remove-item-link]';
  }

  listCollectorPeopleRowTitle(number = 1) {
    return '[data-qa=people-list-summary] tbody:nth-child(' + number + ') tr td.summary__item-title';
  }

  listCollectorVisitorRowAdd() {
    return '[data-qa=visitors-list-summary] [data-qa=add-item-link]';
  }

  listCollectorVisitorRowChange(number = 1) {
    return '[data-qa=visitors-list-summary] tbody:nth-child(' + number + ') [data-qa=change-item-link]';
  }

  listCollectorVisitorRowRemove(number = 1) {
    return '[data-qa=visitors-list-summary] tbody:nth-child(' + number + ') [data-qa=remove-item-link]';
  }

  listCollectorVisitorRowTitle(number = 1) {
    return '[data-qa=visitors-list-summary] tbody:nth-child(' + number + ') tr td.summary__item-title';
  }

  previous() { return 'a[id="top-previous"]'; }

  submit() { return '[data-qa="btn-submit"]'; }

  saveSignOut() { return '[data-qa="btn-save-sign-out"]'; }

  summaryItems() { return 'table.summary__items'; }

  summaryRowAction(number = 1) {
    return 'tbody:nth-child(' + number + ') tr td.summary__actions a';
  }

  summaryRowTitle(number = 1) {
    return 'tbody:nth-child(' + number + ') tr td.summary__item-title';
  }

  summaryRowValue(number = 1) {
    return 'tbody:nth-child(' + number + ') tr td.summary__values';
  }

}

module.exports = new SectionSummaryPage();
