import AnyCompaniesOrBranchesDrivingQuestionPage from "../generated_pages/list_collector_section_summary/any-companies-or-branches.page.js";
import AnyCompaniesOrBranchesPage from "../generated_pages/list_collector_section_summary/any-other-companies-or-branches.page.js";
import AnyCompaniesOrBranchesAddPage from "../generated_pages/list_collector_section_summary/any-other-companies-or-branches-add.page.js";
import AnyCompaniesOrBranchesRemovePage from "../generated_pages/list_collector_section_summary/any-other-companies-or-branches-remove.page.js";
import SectionSummaryPage from "../generated_pages/list_collector_section_summary/section-companies-summary.page";
import UkBasedPage from "../generated_pages/list_collector_section_summary/confirmation-checkbox.page";

describe("List Collector Section Summary Items", () => {
  describe("Given I launch the test list collector section summary items survey", () => {
    beforeEach(async () => {
      await browser.openQuestionnaire("test_list_collector_section_summary.json");
    });
    it("When I get to the section summary, Then the driving question should be visible.", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(SectionSummaryPage.anyCompaniesOrBranchesQuestion()).isExisting()).to.be.true;
      await expect(await $(SectionSummaryPage.anyCompaniesOrBranchesAnswer()).getText()).to.contain("Yes");
    });
    it("When I add my own item, Then the item should be visible on the section summary and have correct values", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      await expect(await $(SectionSummaryPage.companiesListLabel(1)).getText()).to.contain("Name of UK company or branch");
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      await expect(await $(companiesListRowItem(1, 2)).getText()).to.contain("123");
      await expect(await $(companiesListRowItem(1, 3)).getText()).to.contain("Yes");
      await expect(await $(companiesListRowItemAnchor(1)).getHTML()).to.contain("return_to=section-summary#company-or-branch-name");
      await expect(await $(companiesListRowItemAnchor(2)).getHTML()).to.contain("return_to_answer_id=registration-number#registration-number");
      await expect(await $(companiesListRowItemAnchor(3)).getHTML()).to.contain("return_to_answer_id=authorised-insurer-radio#authorised-insurer-radio");
    });
    it("When I add multiple items, Then all the items should be visible on the section summary and have correct values", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesYes();
      addCompany("Company B", "456", false);
      anyMoreCompaniesYes();
      addCompany("Company C", "789", true);
      anyMoreCompaniesNo();
      answerUkBasedQuestion();
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      await expect(await $(companiesListRowItem(1, 2)).getText()).to.contain("123");
      await expect(await $(companiesListRowItem(1, 3)).getText()).to.contain("Yes");
      await expect(await $(companiesListRowItem(2, 1)).getText()).to.contain("Company B");
      await expect(await $(companiesListRowItem(2, 2)).getText()).to.contain("456");
      await expect(await $(companiesListRowItem(2, 3)).getText()).to.contain("No");
      await expect(await $(companiesListRowItem(3, 1)).getText()).to.contain("Company C");
      await expect(await $(companiesListRowItem(3, 2)).getText()).to.contain("789");
      await expect(await $(companiesListRowItem(3, 3)).getText()).to.contain("Yes");
    });
    it("When I remove an item, Then the list of answers should no longer be visible on the section summary.", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      removeFirstCompany();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect($("body").getText()).to.not.have.string("Company A");
      await expect(await $(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.false;
      await expect(await $(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.false;
    });
    it("When I remove an item but the list collector is still on the path, Then the placeholder text should be visible on the section summary.", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      removeFirstCompany();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect($("body").getText()).to.contain("No UK company or branch added");
    });
    it("When I have multiple items in the list and I remove the first item, Then only the item that was not deleted should be visible on the section summary.", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesYes();
      addCompany("Company B", "234", true);
      anyMoreCompaniesNo();
      removeFirstCompany();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect($("body").getText()).to.not.have.string("Company A");
      await expect($("body").getText()).to.contain("Company B");
    });
    it("When I add an item and relevant data and answer No on the additional items page, Then I should get to the section summary page.", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(SectionSummaryPage.companiesListAddLink()).isExisting()).to.be.true;
    });
    it("When I add an item and relevant data and answer Yes on the additional items page, Then I should be able to and add a new item and relevant data.", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesYes();
      await expect(await $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).isExisting()).to.be.true;
      await expect(await $(AnyCompaniesOrBranchesAddPage.registrationNumber()).isExisting()).to.be.true;
      await expect(await $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).isExisting()).to.be.true;
      await expect(await $(AnyCompaniesOrBranchesAddPage.heading()).getText()).to.contain(
        "Give details about the company or branch that undertakes general insurance business"
      );
    });
    it("When I add an item and relevant data, Then I should be able to edit that item from the section summary page.", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      await $(SectionSummaryPage.companiesListEditLink(1)).click();
      await expect(browser.getUrl()).to.contain("edit-company/?return_to=section-summary");
      await expect(await $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).getValue()).to.equal("Company A");
    });
    it("When I edit an item after adding it, Then I should be redirected to the summary page", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      await $(SectionSummaryPage.companiesListEditLink(1)).click();
      await $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).setValue("Changed Company");
      await $(AnyCompaniesOrBranchesAddPage.submit()).click();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Changed Company");
    });
    it("When no item is added but I change my answer to the driving question to Yes, Then I should be able to add a new item.", async () => {
      drivingQuestionNo();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.false;
      await expect(await $(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.false;
      await expect(await $(SectionSummaryPage.companiesListAddLink()).isExisting()).to.be.false;
      await $(SectionSummaryPage.anyCompaniesOrBranchesAnswerEdit()).click();
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.true;
      await expect(await $(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.true;
      await expect(await $(SectionSummaryPage.companiesListAddLink()).isExisting()).to.be.true;
    });
    it("When I add an item and relevant data but change my answer to the driving question to No, Then I should see the original item on the summary if change the answer back to Yes.", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      await $(SectionSummaryPage.anyCompaniesOrBranchesAnswerEdit()).click();
      drivingQuestionNo();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.false;
      await expect(await $(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.false;
      await expect($("body").getText()).to.not.have.string("No UK company or branch added");
      await expect(await $(SectionSummaryPage.companiesListAddLink()).isExisting()).to.be.false;
      await $(SectionSummaryPage.anyCompaniesOrBranchesAnswerEdit()).click();
      drivingQuestionYes();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      await expect(await $(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.true;
      await expect(await $(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.true;
      await expect(await $(SectionSummaryPage.companiesListAddLink()).isExisting()).to.be.true;
    });
    it("When I add another company from the summary page, Then I am asked if I want to add any more company before accessing the section summary", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesNo();
      await $(SectionSummaryPage.companiesListAddLink()).click();
      await expect(browser.getUrl()).to.contain("/questionnaire/companies/add-company");
      await expect(browser.getUrl()).to.contain("?return_to=section-summary");
      addCompany("Company B", "456", true);
      await expect(browser.getUrl()).to.contain(AnyCompaniesOrBranchesPage.url());
      await expect($("body").getText()).to.have.string("Company A");
      await expect($("body").getText()).to.have.string("Company B");
      anyMoreCompaniesNo();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
    });
    it("When I add three companies, Then I am prompted with the confirmation question", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesYes();
      addCompany("Company B", "456", true);
      anyMoreCompaniesYes();
      addCompany("Company C", "789", true);
      anyMoreCompaniesNo();
      await expect(browser.getUrl()).to.contain(UkBasedPage.url());
    });
    it("When I add less than 3 companies, Then I am not prompted with the confirmation question", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesYes();
      addCompany("Company B", "456", true);
      anyMoreCompaniesNo();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
    });
    it("When I add more than 3 companies, Then I am not prompted with the confirmation question", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesYes();
      addCompany("Company B", "456", true);
      anyMoreCompaniesYes();
      addCompany("Company C", "789", true);
      anyMoreCompaniesYes();
      addCompany("Company D", "135", true);
      anyMoreCompaniesNo();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
    });
    it("When I add another company from the summary page, and the amount then totals to 3, and the confirmation question hasn't been previously answered, Then I am prompted with the confirmation question", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesYes();
      addCompany("Company B", "456", true);
      anyMoreCompaniesNo();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      await $(SectionSummaryPage.companiesListAddLink()).click();
      await expect(browser.getUrl()).to.contain("/questionnaire/companies/add-company");
      await expect(browser.getUrl()).to.contain("?return_to=section-summary");
      addCompany("Company C", "234", true);
      anyMoreCompaniesNo();
      await expect(browser.getUrl()).to.contain(UkBasedPage.url());
      answerUkBasedQuestion();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
    });
    it("When I remove a company from the summary page, and the amount then totals to 3, and the confirmation question hasn't been previously answered, Then I am prompted with the confirmation question", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesYes();
      addCompany("Company B", "456", true);
      anyMoreCompaniesYes();
      addCompany("Company C", "234", true);
      anyMoreCompaniesYes();
      addCompany("Company D", "345", true);
      anyMoreCompaniesNo();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      removeFirstCompany();
      await expect(browser.getUrl()).to.contain(UkBasedPage.url());
      answerUkBasedQuestion();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
    });
    it("When I remove a company from the summary page, and the amount then totals to 3, but the confirmation question has already been answered, Then I am not prompted with the confirmation question", async () => {
      drivingQuestionYes();
      addCompany("Company A", "123", true);
      anyMoreCompaniesYes();
      addCompany("Company B", "456", true);
      anyMoreCompaniesYes();
      addCompany("Company C", "234", true);
      anyMoreCompaniesNo();
      await expect(browser.getUrl()).to.contain(UkBasedPage.url());
      answerUkBasedQuestion();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      await $(SectionSummaryPage.companiesListAddLink()).click();
      await expect(browser.getUrl()).to.contain("/questionnaire/companies/add-company");
      await expect(browser.getUrl()).to.contain("?return_to=section-summary");
      addCompany("Company C", "234", true);
      anyMoreCompaniesNo();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
      removeFirstCompany();
      await expect(browser.getUrl()).to.contain(SectionSummaryPage.url());
    });
  });
});

const drivingQuestionYes = async () => {
  await $(AnyCompaniesOrBranchesDrivingQuestionPage.yes()).click();
  await $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
};

const drivingQuestionNo = async () => {
  await $(AnyCompaniesOrBranchesDrivingQuestionPage.no()).click();
  await $(AnyCompaniesOrBranchesDrivingQuestionPage.submit()).click();
};

const addCompany = async (name, number, authorised) => {
  await $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).setValue(name);
  await $(AnyCompaniesOrBranchesAddPage.registrationNumber()).setValue(number);
  if (authorised) {
    await $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).click();
  } else {
    await $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioNo()).click();
  }
  await $(AnyCompaniesOrBranchesAddPage.submit()).click();
};

const anyMoreCompaniesYes = async () => {
  await $(AnyCompaniesOrBranchesPage.yes()).click();
  await $(AnyCompaniesOrBranchesPage.submit()).click();
};

const anyMoreCompaniesNo = async () => {
  await $(AnyCompaniesOrBranchesPage.no()).click();
  await $(AnyCompaniesOrBranchesPage.submit()).click();
};

const removeFirstCompany = async () => {
  await $(SectionSummaryPage.companiesListRemoveLink(1)).click();
  await $(AnyCompaniesOrBranchesRemovePage.yes()).click();
  await $(AnyCompaniesOrBranchesRemovePage.submit()).click();
};

const answerUkBasedQuestion = async () => {
  await $(UkBasedPage.yes()).click();
  await $(UkBasedPage.submit()).click();
};

const companiesListRowItem = async (row, index) => {
  return `#group-companies-1 .ons-summary__items .ons-summary__item:nth-of-type(${row}) .ons-summary__row:nth-of-type(${index})`;
};

const companiesListRowItemAnchor = async (index) => {
  return `#group-companies-1 .ons-summary__items .ons-summary__item .ons-summary__row:nth-of-type(${index}) a`;
};
