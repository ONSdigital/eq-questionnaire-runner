const BasePage = require('./base.page');

class ListCollectorSummary extends BasePage {

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

  listLabel(instance) { return `tbody:nth-child(${instance}) td:first-child`; }

  peopleListLabel(listItemInstance) { return 'div[data-qa="people-list-summary"] tbody:nth-child(' + listItemInstance + ') td:first-child'; }

}

module.exports = new ListCollectorSummary();
