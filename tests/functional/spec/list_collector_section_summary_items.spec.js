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
    it("When I answer yes to the driving question, Then I should be able to add my own item and the relevant data about it and get to the list collector question page.", () => {
      $(AnyCompaniesOrBranchesDrivingQuestionPage.yes()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
      $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).setValue("Company A");
      $(AnyCompaniesOrBranchesAddPage.registrationNumber()).setValue("0123456789");
      $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).click();
      $(AnyCompaniesOrBranchesAddPage.submit()).click();
      expect(browser.getUrl()).to.contain(AnyCompaniesOrBranchesPage.url());
    });
    it("When I add my own item and relevant data, Then after submitting I should be asked if I have more items to add.", () => {
      $(AnyCompaniesOrBranchesDrivingQuestionPage.yes()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
      $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).setValue("Company A");
      $(AnyCompaniesOrBranchesAddPage.registrationNumber()).setValue("0123456789");
      $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).click();
      $(AnyCompaniesOrBranchesAddPage.submit()).click();
      expect($(AnyCompaniesOrBranchesPage.yes()).isExisting()).to.be.true;
      expect($(AnyCompaniesOrBranchesPage.no()).isExisting()).to.be.true;
      expect($(AnyCompaniesOrBranchesPage.heading()).getText()).to.contain(
        "Do you need to add any other UK companies or branches that undertake general insurance business?"
      );
    });
    it("When I add my own item and relevant data, Then after I answer no on additional items page I should get to the section summary page.", () => {
      $(AnyCompaniesOrBranchesDrivingQuestionPage.yes()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
      $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).setValue("Company A");
      $(AnyCompaniesOrBranchesAddPage.registrationNumber()).setValue("0123456789");
      $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).click();
      $(AnyCompaniesOrBranchesAddPage.submit()).click();
      $(AnyCompaniesOrBranchesPage.no()).click();
      $(AnyCompaniesOrBranchesPage.submit()).click();
      $(EstimatePage.submit()).click();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
    });
    it("When I add my own item and relevant data, Then after I answer yes on additional items page I should be able to choose an item from the items list and add relevant data about it.", () => {
      $(AnyCompaniesOrBranchesDrivingQuestionPage.yes()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
      $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).setValue("Company A");
      $(AnyCompaniesOrBranchesAddPage.registrationNumber()).setValue("0123456789");
      $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).click();
      $(AnyCompaniesOrBranchesAddPage.submit()).click();
      $(AnyCompaniesOrBranchesPage.yes()).click();
      $(AnyCompaniesOrBranchesPage.submit()).click();
      expect($(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).isExisting()).to.be.true;
      expect($(AnyCompaniesOrBranchesAddPage.registrationNumber()).isExisting()).to.be.true;
      expect($(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).isExisting()).to.be.true;
      expect($(AnyCompaniesOrBranchesAddPage.heading()).getText()).to.contain(
        "Give details about the company or branch that undertakes general insurance business"
      );
    });
    it("When I add my own item and relevant data, Then I should be able to edit that item from the section summary page.", () => {
      $(AnyCompaniesOrBranchesDrivingQuestionPage.yes()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
      $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).setValue("Company A");
      $(AnyCompaniesOrBranchesAddPage.registrationNumber()).setValue("0123456789");
      $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).click();
      $(AnyCompaniesOrBranchesAddPage.submit()).click();
      $(AnyCompaniesOrBranchesPage.no()).click();
      $(AnyCompaniesOrBranchesPage.submit()).click();
      $(EstimatePage.submit()).click();
      $(SectionSummaryPage.companiesListEditLink(1)).click();
      expect(browser.getUrl()).to.contain("edit-company/?return_to=section-summary");
    });
    it("When I add my own item and relevant data, Then I should be able to remove that item from the section summary page.", () => {
      $(AnyCompaniesOrBranchesDrivingQuestionPage.yes()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
      $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).setValue("Company A");
      $(AnyCompaniesOrBranchesAddPage.registrationNumber()).setValue("0123456789");
      $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).click();
      $(AnyCompaniesOrBranchesAddPage.submit()).click();
      $(AnyCompaniesOrBranchesPage.no()).click();
      $(AnyCompaniesOrBranchesPage.submit()).click();
      $(EstimatePage.submit()).click();
      $(SectionSummaryPage.companiesListRemoveLink(1)).click();
      expect(browser.getUrl()).to.contain("remove-company/?return_to=section-summary");
      $(AnyCompaniesOrBranchesRemovePage.yes()).click();
      $(AnyCompaniesOrBranchesRemovePage.submit()).click();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      expect($(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.false;
      expect($(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.false;
    });
    it("When I decide not to add an item and relevant data and I change my answer to yes, Then I should be able to add the item.", () => {
      $(AnyCompaniesOrBranchesDrivingQuestionPage.no()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
      $(EstimatePage.submit()).click();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      expect($(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.false;
      expect($(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.false;
      expect($(SectionSummaryPage.companiesListAddLink()).isExisting()).to.be.true;
      $(SectionSummaryPage.anyCompaniesOrBranchesAnswerEdit()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.yes()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
      $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).setValue("Company A");
      $(AnyCompaniesOrBranchesAddPage.registrationNumber()).setValue("0123456789");
      $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).click();
      $(AnyCompaniesOrBranchesAddPage.submit()).click();
      $(AnyCompaniesOrBranchesPage.no()).click();
      $(AnyCompaniesOrBranchesPage.submit()).click();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      expect($(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.true;
      expect($(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.true;
    });
    it("When I decide to add an item and relevant data and I decide to remove it, Then I should be able to see the item again after I decide to add more items.", () => {
      $(AnyCompaniesOrBranchesDrivingQuestionPage.yes()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
      $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).setValue("Company A");
      $(AnyCompaniesOrBranchesAddPage.registrationNumber()).setValue("0123456789");
      $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).click();
      $(AnyCompaniesOrBranchesAddPage.submit()).click();
      $(AnyCompaniesOrBranchesPage.no()).click();
      $(AnyCompaniesOrBranchesPage.submit()).click();
      $(EstimatePage.submit()).click();
      $(SectionSummaryPage.anyCompaniesOrBranchesAnswerEdit()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.no()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      expect($(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.false;
      expect($(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.false;
      $(SectionSummaryPage.anyCompaniesOrBranchesAnswerEdit()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.yes()).click();
      $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
      expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      expect($(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.true;
      expect($(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.true;
    });
  });
});
