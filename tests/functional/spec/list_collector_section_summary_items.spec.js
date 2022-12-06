import AnyCompaniesOrBranchesDrivingQuestionPage from "../generated_pages/list_collector_section_summary_items/any-companies-or-branches.page.js";
import AnyCompaniesOrBranchesPage from "../generated_pages/list_collector_section_summary_items/any-other-companies-or-branches.page.js";
import AnyCompaniesOrBranchesAddPage from "../generated_pages/list_collector_section_summary_items/any-other-companies-or-branches-add.page.js";
import AnyCompaniesOrBranchesRemovePage from "../generated_pages/list_collector_section_summary_items/any-other-companies-or-branches-remove.page.js";
import SectionSummaryPage from "../generated_pages/list_collector_section_summary_items/section-companies-summary.page";
import EstimatePage from "../generated_pages/list_collector_section_summary_items/estimate-checkbox.page";

describe("List Collector Section Summary Items", () => {
  describe("Given I launch the test list collector section summary items survey", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_list_collector_section_summary_items.json");
    });
    it("When I get to the section summary, Then the driving question should be visible.", () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      $(EstimatePage.submit()).click();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      expect($(SectionSummaryPage.anyCompaniesOrBranchesQuestion()).isExisting()).to.be.true;
      expect($(SectionSummaryPage.anyCompaniesOrBranchesAnswer()).getText()).to.contain("Yes");
    });
    it("When I add my own item, Then the item should be visible on the section summary and have correct values", () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      $(EstimatePage.submit()).click();
      expect($(SectionSummaryPage.companiesListLabel(1)).getText()).to.contain("Name of UK company or branch");
      expect($(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      expect($(companiesListRowItem(1, 2)).getText()).to.contain("123");
      expect($(companiesListRowItem(1, 3)).getText()).to.contain("Yes");
      expect($(companiesListRowItemAnchor(1)).getHTML()).to.contain("return_to=section-summary#company-or-branch-name");
      expect($(companiesListRowItemAnchor(2)).getHTML()).to.contain("return_to_answer_id=registration-number#registration-number");
      expect($(companiesListRowItemAnchor(3)).getHTML()).to.contain("return_to_answer_id=authorised-insurer-radio#authorised-insurer-radio");
    });
    it("When I add multiple items, Then all the items should be visible on the section summary and have correct values", () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesYes();
      addCompany("Company B", "456", false);
      anyMoreCompaniesYes();
      addCompany("Company C", "789", true);
      anyMoreCompaniesNo();
      $(EstimatePage.submit()).click();
      expect($(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      expect($(companiesListRowItem(1, 2)).getText()).to.contain("123");
      expect($(companiesListRowItem(1, 3)).getText()).to.contain("Yes");
      expect($(companiesListRowItem(2, 1)).getText()).to.contain("Company B");
      expect($(companiesListRowItem(2, 2)).getText()).to.contain("456");
      expect($(companiesListRowItem(2, 3)).getText()).to.contain("No");
      expect($(companiesListRowItem(3, 1)).getText()).to.contain("Company C");
      expect($(companiesListRowItem(3, 2)).getText()).to.contain("789");
      expect($(companiesListRowItem(3, 3)).getText()).to.contain("Yes");
    });
    it("When I add my own item, Then I should be able to remove that item from the section summary page.", () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      $(EstimatePage.submit()).click();
      $(SectionSummaryPage.companiesListRemoveLink(1)).click();
      expect(browser.getUrl()).to.contain("remove-company/?return_to=section-summary");
    });
    it("When I add my own item and make it not on the path, Then the list of answers should not be visible on the section summary.", () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      $(EstimatePage.submit()).click();
      removeFirstCompany();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      expect($(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.false;
      expect($(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.false;
    });
    it("When I remove my own item but list collector is still on the path, Then the placeholder text should be visible on the section summary.", () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      $(EstimatePage.submit()).click();
      removeFirstCompany();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      expect($("body").getText()).to.contain("No UK company or branch added");
    });
    it("When I add my own item and relevant data, Then after I answer no on additional items page I should get to the section summary page.", () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      $(EstimatePage.submit()).click();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
    });
    it("When I add my own item and relevant data, Then after I answer yes on additional items page I should be able to choose an item from the items list and add relevant data about it.", () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesYes();
      expect($(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).isExisting()).to.be.true;
      expect($(AnyCompaniesOrBranchesAddPage.registrationNumber()).isExisting()).to.be.true;
      expect($(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).isExisting()).to.be.true;
      expect($(AnyCompaniesOrBranchesAddPage.heading()).getText()).to.contain(
        "Give details about the company or branch that undertakes general insurance business"
      );
    });
    it("When I add my own item and relevant data, Then I should be able to edit that item from the section summary page.", () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      $(EstimatePage.submit()).click();
      $(SectionSummaryPage.companiesListEditLink(1)).click();
      expect(browser.getUrl()).to.contain("edit-company/?return_to=section-summary");
    });
    it("When I decide not to add an item and relevant data and I change my answer to yes, Then I should be able to add the item.", () => {
      drivingQuestionNo();
      $(EstimatePage.submit()).click();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      expect($(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.false;
      expect($(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.false;
      expect($(SectionSummaryPage.companiesListAddLink()).isExisting()).to.be.false;
      $(SectionSummaryPage.anyCompaniesOrBranchesAnswerEdit()).click();
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      expect($(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.true;
      expect($(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.true;
      expect($(SectionSummaryPage.companiesListAddLink()).isExisting()).to.be.true;
    });
    it("When I decide to add an item and relevant data and I decide to remove it, Then I should be able to see the item again after I decide to add more items.", () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      $(EstimatePage.submit()).click();
      $(SectionSummaryPage.anyCompaniesOrBranchesAnswerEdit()).click();
      drivingQuestionNo();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      expect($(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.false;
      expect($(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.false;
      $(SectionSummaryPage.anyCompaniesOrBranchesAnswerEdit()).click();
      drivingQuestionYes();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      expect($(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.true;
      expect($(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.true;
    });
  });
});

function drivingQuestionYes() {
  $(AnyCompaniesOrBranchesDrivingQuestionPage.yes()).click();
  $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
}

function drivingQuestionNo() {
  $(AnyCompaniesOrBranchesDrivingQuestionPage.no()).click();
  $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
}

function addCompany(name, number, authorised) {
  $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).setValue(name);
  $(AnyCompaniesOrBranchesAddPage.registrationNumber()).setValue(number);
  if (authorised) {
    $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).click();
  } else {
    $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioNo()).click();
  }
  $(AnyCompaniesOrBranchesAddPage.submit()).click();
}

function anyMoreCompaniesYes() {
  $(AnyCompaniesOrBranchesPage.yes()).click();
  $(AnyCompaniesOrBranchesPage.submit()).click();
}

function anyMoreCompaniesNo() {
  $(AnyCompaniesOrBranchesPage.no()).click();
  $(AnyCompaniesOrBranchesPage.submit()).click();
}

function removeFirstCompany() {
  $(SectionSummaryPage.companiesListRemoveLink(1)).click();
  $(AnyCompaniesOrBranchesRemovePage.yes()).click();
  $(AnyCompaniesOrBranchesRemovePage.submit()).click();
}

function companiesListRowItem(row, index) {
  return `#group-companies-1 .ons-summary__items .ons-summary__item:nth-of-type(${row}) .ons-summary__row:nth-of-type(${index})`;
}

function companiesListRowItemAnchor(index) {
  return `#group-companies-1 .ons-summary__items .ons-summary__item .ons-summary__row:nth-of-type(${index}) a`;
}
