const BasePage = require('./base.page');

class SectionSummaryPage extends BasePage {
  displayedName() { return 'h1'; }

  displayedDescription() { return 'p > strong'; }

  previous() { return 'a[id="top-previous"]'; }

  submit() { return '[data-qa="btn-submit"]'; }

  saveSignOut() { return '[data-qa="btn-save-sign-out"]'; }

  summaryItems() { return 'table.summary__items'; }

  summaryRowAction(number = 1) { return 'tbody:nth-child(' + number + ') tr td.summary__actions a'; }

  summaryRowTitle(number = 1) { return 'tbody:nth-child(' + number + ') tr td.summary__item-title'; }

  summaryRowValue(number = 1) { return 'tbody:nth-child(' + number + ') tr td.summary__values'; }
}

module.exports = new SectionSummaryPage();
