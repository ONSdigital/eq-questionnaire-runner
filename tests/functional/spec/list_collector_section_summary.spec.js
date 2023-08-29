import AnyCompaniesOrBranchesDrivingQuestionPage from "../generated_pages/list_collector_section_summary/any-companies-or-branches.page.js";
import AnyCompaniesOrBranchesPage from "../generated_pages/list_collector_section_summary/any-other-companies-or-branches.page.js";
import AnyCompaniesOrBranchesAddPage from "../generated_pages/list_collector_section_summary/any-other-companies-or-branches-add.page.js";
import AnyCompaniesOrBranchesRemovePage from "../generated_pages/list_collector_section_summary/any-other-companies-or-branches-remove.page.js";
import SectionSummaryPage from "../generated_pages/list_collector_section_summary/section-companies-summary.page";
import SectionSummaryTwoPage from "../generated_pages/list_collector_section_summary/section-household-summary.page";
import UkBasedPage from "../generated_pages/list_collector_section_summary/confirmation-checkbox.page";
import ListCollectorPage from "../generated_pages/list_collector_section_summary/list-collector.page";
import HouseholderCheckboxPage from "../generated_pages/list_collector_section_summary/householder-checkbox.page";
import SubmitPage from "../generated_pages/list_collector_section_summary/submit.page";
import ThankYouPage from "../base_pages/thank-you.page";
import ViewSubmittedResponsePage from "../generated_pages/list_collector_section_summary/view-submitted-response.page";
import { click, listItemIds } from "../helpers";

describe("List Collector Section Summary and Summary Items", () => {
  describe("Given I launch the test list collector section summary items survey", () => {
    beforeEach(async () => {
      await browser.openQuestionnaire("test_list_collector_section_summary.json");
    });
    it("When I get to the section summary, Then the driving question should be visible.", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesNo();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(SectionSummaryPage.anyCompaniesOrBranchesQuestion()).isExisting()).to.be.true;
      await expect(await $(SectionSummaryPage.anyCompaniesOrBranchesAnswer()).getText()).to.contain("Yes");
    });
    it("When I add my own item, Then the item should be visible on the section summary and have correct values", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesNo();
      await expect(await $(SectionSummaryPage.companiesListLabel(1)).getText()).to.contain("Name of UK company or branch");
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      await expect(await $(companiesListRowItem(1, 2)).getText()).to.contain("123");
      await expect(await $(companiesListRowItem(1, 3)).getText()).to.contain("Yes");
      const listItemId = (await listItemIds())[0];
      await expect(await $(companiesListRowItemAnchor(1)).getHTML()).to.contain(
        `return_to=section-summary&amp;return_to_answer_id=${listItemId}#company-or-branch-name`,
      );
      await expect(await $(companiesListRowItemAnchor(2)).getHTML()).to.contain(`return_to_answer_id=registration-number-${listItemId}#registration-number`);
      await expect(await $(companiesListRowItemAnchor(3)).getHTML()).to.contain(
        `return_to_answer_id=authorised-insurer-radio-${listItemId}#authorised-insurer-radio`,
      );
    });
    it("When I add multiple items, Then all the items should be visible on the section summary and have correct values", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesYes();
      await addCompany("Company B", "456", false);
      await anyMoreCompaniesYes();
      await addCompany("Company C", "789", true);
      await anyMoreCompaniesNo();
      await answerUkBasedQuestion();
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
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesNo();
      await removeFirstCompany();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $("body").getText()).to.not.have.string("Company A");
      await expect(await $(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.false;
      await expect(await $(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.false;
    });
    it("When I remove an item but the list collector is still on the path, Then the placeholder text should be visible on the section summary.", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesNo();
      await removeFirstCompany();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $("body").getText()).to.contain("No UK company or branch added");
    });
    it("When I have multiple items in the list and I remove the first item, Then only the item that was not deleted should be visible on the section summary.", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesYes();
      await addCompany("Company B", "234", true);
      await anyMoreCompaniesNo();
      await removeFirstCompany();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $("body").getText()).to.not.have.string("Company A");
      await expect(await $("body").getText()).to.contain("Company B");
    });
    it("When I add an item and relevant data and answer No on the additional items page, Then I should get to the section summary page.", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesNo();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(SectionSummaryPage.companiesListAddLink()).isExisting()).to.be.true;
    });
    it("When I add an item and relevant data and answer Yes on the additional items page, Then I should be able to and add a new item and relevant data.", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesYes();
      await expect(await $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).isExisting()).to.be.true;
      await expect(await $(AnyCompaniesOrBranchesAddPage.registrationNumber()).isExisting()).to.be.true;
      await expect(await $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).isExisting()).to.be.true;
      await expect(await $(AnyCompaniesOrBranchesAddPage.heading()).getText()).to.contain(
        "Give details about the company or branch that undertakes general insurance business",
      );
    });
    it("When I add an item and relevant data, Then I should be able to edit that item from the section summary page.", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesNo();
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      await $(SectionSummaryPage.companiesListEditLink(1)).click();
      await expect(await browser.getUrl()).to.contain("edit-company/?return_to=section-summary");
      await expect(await $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).getValue()).to.equal("Company A");
    });
    it("When I edit an item after adding it, Then I should be redirected to the summary page", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesNo();
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      await $(SectionSummaryPage.companiesListEditLink(1)).click();
      await $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).setValue("Changed Company");
      await click(AnyCompaniesOrBranchesAddPage.submit());
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Changed Company");
    });
    it("When no item is added but I change my answer to the driving question to Yes, Then I should be able to add a new item.", async () => {
      await drivingQuestionNo();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.false;
      await expect(await $(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.false;
      await expect(await $(SectionSummaryPage.companiesListAddLink()).isExisting()).to.be.false;
      await $(SectionSummaryPage.anyCompaniesOrBranchesAnswerEdit()).click();
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesNo();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.true;
      await expect(await $(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.true;
      await expect(await $(SectionSummaryPage.companiesListAddLink()).isExisting()).to.be.true;
    });
    it("When I add an item and relevant data but change my answer to the driving question to No, Then I should see the original item on the summary if change the answer back to Yes.", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesNo();
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      await $(SectionSummaryPage.anyCompaniesOrBranchesAnswerEdit()).click();
      await drivingQuestionNo();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.false;
      await expect(await $(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.false;
      await expect(await $("body").getText()).to.not.have.string("No UK company or branch added");
      await expect(await $(SectionSummaryPage.companiesListAddLink()).isExisting()).to.be.false;
      await $(SectionSummaryPage.anyCompaniesOrBranchesAnswerEdit()).click();
      await drivingQuestionYes();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      await expect(await $(SectionSummaryPage.companiesListEditLink(1)).isExisting()).to.be.true;
      await expect(await $(SectionSummaryPage.companiesListRemoveLink(1)).isExisting()).to.be.true;
      await expect(await $(SectionSummaryPage.companiesListAddLink()).isExisting()).to.be.true;
    });
    it("When I add another company from the summary page, Then I am asked if I want to add any more company before accessing the section summary", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesNo();
      await $(SectionSummaryPage.companiesListAddLink()).click();
      await expect(await browser.getUrl()).to.contain("/questionnaire/companies/add-company");
      await expect(await browser.getUrl()).to.contain("?return_to=section-summary");
      await addCompany("Company B", "456", true);
      await expect(await browser.getUrl()).to.contain(AnyCompaniesOrBranchesPage.url());
      await expect(await $("body").getText()).to.have.string("Company A");
      await expect(await $("body").getText()).to.have.string("Company B");
      await anyMoreCompaniesNo();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
    });
    it("When I add three companies, Then I am prompted with the confirmation question", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesYes();
      await addCompany("Company B", "456", true);
      await anyMoreCompaniesYes();
      await addCompany("Company C", "789", true);
      await anyMoreCompaniesNo();
      await expect(await browser.getUrl()).to.contain(UkBasedPage.url());
    });
    it("When I add less than 3 companies, Then I am not prompted with the confirmation question", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesYes();
      await addCompany("Company B", "456", true);
      await anyMoreCompaniesNo();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
    });
    it("When I add more than 3 companies, Then I am not prompted with the confirmation question", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesYes();
      await addCompany("Company B", "456", true);
      await anyMoreCompaniesYes();
      await addCompany("Company C", "789", true);
      await anyMoreCompaniesYes();
      await addCompany("Company D", "135", true);
      await anyMoreCompaniesNo();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
    });
    it("When I add another company from the summary page, and the amount then totals to 3, and the confirmation question hasn't been previously answered, Then I am prompted with the confirmation question", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesYes();
      await addCompany("Company B", "456", true);
      await anyMoreCompaniesNo();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await $(SectionSummaryPage.companiesListAddLink()).click();
      await expect(await browser.getUrl()).to.contain("/questionnaire/companies/add-company");
      await expect(await browser.getUrl()).to.contain("?return_to=section-summary");
      await addCompany("Company C", "234", true);
      await anyMoreCompaniesNo();
      await expect(await browser.getUrl()).to.contain(UkBasedPage.url());
      await answerUkBasedQuestion();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
    });
    it("When I remove a company from the summary page, and the amount then totals to 3, and the confirmation question hasn't been previously answered, Then I am prompted with the confirmation question", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesYes();
      await addCompany("Company B", "456", true);
      await anyMoreCompaniesYes();
      await addCompany("Company C", "234", true);
      await anyMoreCompaniesYes();
      await addCompany("Company D", "345", true);
      await anyMoreCompaniesNo();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await removeFirstCompany();
      await expect(await browser.getUrl()).to.contain(UkBasedPage.url());
      await answerUkBasedQuestion();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
    });

    it("When I get to the summary page, Then the summary should be displayed as expected with change links", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesYes();
      await addCompany("Company B", "456", true);
      await anyMoreCompaniesYes();
      await addCompany("Company C", "234", true);
      await anyMoreCompaniesNo();
      await expect(await browser.getUrl()).to.contain(UkBasedPage.url());
      await answerUkBasedQuestion();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await click(SectionSummaryPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await $(HouseholderCheckboxPage.no()).click();
      await click(HouseholderCheckboxPage.submit());
      await click(SectionSummaryTwoPage.submit());

      await expect(await browser.getUrl()).to.contain(SubmitPage.url());
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      await expect(await $(companiesListRowItem(1, 2)).getText()).to.contain("123");
      await expect(await $(companiesListRowItem(1, 3)).getText()).to.contain("Change");
      await expect(await $(companiesListRowItem(2, 1)).getText()).to.contain("Company B");
      await expect(await $(companiesListRowItem(2, 2)).getText()).to.contain("456");
      await expect(await $(companiesListRowItem(2, 3)).getText()).to.contain("Change");
      await expect(await $(companiesListRowItem(3, 1)).getText()).to.contain("Company C");
      await expect(await $(companiesListRowItem(3, 2)).getText()).to.contain("234");
      await expect(await $(companiesListRowItem(3, 3)).getText()).to.contain("Change");
      await expect(await $(SubmitPage.householderCheckboxAnswer()).getText()).to.contain("No");
      await expect(await $("body").getHTML()).to.contain("Add another UK company or branch");
      await expect(await $("body").getHTML()).to.contain("Remove");
    });

    it("When I get to the view submitted response page, Then the summary should be displayed as expected without any change or remove links", async () => {
      await drivingQuestionYes();
      await addCompany("Company A", "123", true);
      await anyMoreCompaniesYes();
      await addCompany("Company B", "456", true);
      await anyMoreCompaniesYes();
      await addCompany("Company C", "234", true);
      await anyMoreCompaniesNo();
      await expect(await browser.getUrl()).to.contain(UkBasedPage.url());
      await answerUkBasedQuestion();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.url());
      await click(SectionSummaryPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await $(HouseholderCheckboxPage.no()).click();
      await click(HouseholderCheckboxPage.submit());
      await click(SectionSummaryTwoPage.submit());
      await click(SubmitPage.submit());
      await expect(await $(ThankYouPage.title()).getHTML()).to.contain("Thank you for completing the Test");
      await $(ThankYouPage.savePrintAnswersLink()).click();

      await expect(await browser.getUrl()).to.contain(ViewSubmittedResponsePage.pageName);
      await expect(await $(companiesListRowItem(1, 1)).getText()).to.contain("Company A");
      await expect(await $(companiesListRowItem(1, 2)).getText()).to.contain("123");
      await expect(await $(companiesListRowItem(2, 1)).getText()).to.contain("Company B");
      await expect(await $(companiesListRowItem(2, 2)).getText()).to.contain("456");
      await expect(await $(companiesListRowItem(3, 1)).getText()).to.contain("Company C");
      await expect(await $(companiesListRowItem(3, 2)).getText()).to.contain("234");
      await expect(await $("body").getHTML()).to.not.contain("Change");
      await expect(await $("body").getHTML()).to.not.contain("Remove");
      await expect(await $("body").getHTML()).to.not.contain("Add another UK company or branch");
    });
  });
});

const drivingQuestionYes = async () => {
  await $(AnyCompaniesOrBranchesDrivingQuestionPage.yes()).click();
  await click(AnyCompaniesOrBranchesDrivingQuestionPage.submit());
};

const drivingQuestionNo = async () => {
  await $(AnyCompaniesOrBranchesDrivingQuestionPage.no()).click();
  await click(AnyCompaniesOrBranchesDrivingQuestionPage.submit());
};

const addCompany = async (name, number, authorised) => {
  await $(AnyCompaniesOrBranchesAddPage.companyOrBranchName()).setValue(name);
  await $(AnyCompaniesOrBranchesAddPage.registrationNumber()).setValue(number);
  if (authorised) {
    await $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).click();
  } else {
    await $(AnyCompaniesOrBranchesAddPage.authorisedInsurerRadioNo()).click();
  }
  await click(AnyCompaniesOrBranchesAddPage.submit());
};

const anyMoreCompaniesYes = async () => {
  await $(AnyCompaniesOrBranchesPage.yes()).click();
  await click(AnyCompaniesOrBranchesPage.submit());
};

const anyMoreCompaniesNo = async () => {
  await $(AnyCompaniesOrBranchesPage.no()).click();
  await click(AnyCompaniesOrBranchesPage.submit());
};

const removeFirstCompany = async () => {
  await $(SectionSummaryPage.companiesListRemoveLink(1)).click();
  await $(AnyCompaniesOrBranchesRemovePage.yes()).click();
  await click(AnyCompaniesOrBranchesRemovePage.submit());
};

const answerUkBasedQuestion = async () => {
  await $(UkBasedPage.yes()).click();
  await click(UkBasedPage.submit());
};

const companiesListRowItem = (row, index) => {
  return `#group-companies-1 .ons-summary__items .ons-summary__item:nth-of-type(${row}) .ons-summary__row:nth-of-type(${index})`;
};

const companiesListRowItemAnchor = (index) => {
  return `#group-companies-1 .ons-summary__items .ons-summary__item .ons-summary__row:nth-of-type(${index}) a`;
};
