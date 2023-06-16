import ResponsiblePartyPage from "../../../generated_pages/list_collector_repeating_blocks_section_summary/responsible-party.page";
import AnyCompaniesOrBranchesPage from "../../../generated_pages/list_collector_repeating_blocks_section_summary/any-companies-or-branches.page";
import AddCompanyPage from "../../../generated_pages/list_collector_repeating_blocks_section_summary/any-other-companies-or-branches-add.page";
import EditCompanyPage from "../../../generated_pages/list_collector_repeating_blocks_section_summary/any-other-companies-or-branches-edit.page";
import RemoveCompanyPage from "../../../generated_pages/list_collector_repeating_blocks_section_summary/any-other-companies-or-branches-remove.page";
import CompaniesRepeatingBlock1Page from "../../../generated_pages/list_collector_repeating_blocks_section_summary/companies-repeating-block-1-repeating-block.page";
import CompaniesRepeatingBlock2Page from "../../../generated_pages/list_collector_repeating_blocks_section_summary/companies-repeating-block-2-repeating-block.page";
import AnyOtherCompaniesOrBranchesPage from "../../../generated_pages/list_collector_repeating_blocks_section_summary/any-other-companies-or-branches.page";
import SectionCompaniesPage from "../../../generated_pages/list_collector_repeating_blocks_section_summary/section-companies-summary.page";
import AnyOtherTradingDetailsPage from "../../../generated_pages/list_collector_repeating_blocks_section_summary/any-other-trading-details.page";
import SubmitPage from "../../../generated_pages/list_collector_repeating_blocks_section_summary/submit.page";
import { checkItemsInList, checkListItemComplete, checkListItemIncomplete } from "../../../helpers";

describe("List Collector Repeating Blocks", () => {
  describe("Given a normal journey through the list collector with repeating blocks, the answers can be submitted.", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_repeating_blocks_section_summary.json");
    });
    it("The user is able to add companies, complete repeating blocks, and submit.", async () => {
      await $(ResponsiblePartyPage.yes()).click();
      await $(AnyCompaniesOrBranchesPage.submit()).click();
      await $(AnyCompaniesOrBranchesPage.yes()).click();
      await $(AnyCompaniesOrBranchesPage.submit()).click();

      await $(AddCompanyPage.companyOrBranchName()).setValue("ONS");
      await $(AddCompanyPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(123);
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(1);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(1);
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();

      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await $(AddCompanyPage.companyOrBranchName()).setValue("GOV");
      await $(AddCompanyPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(456);
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(2);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(2);
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioNo()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioNo()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();

      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();

      await $(AnyOtherTradingDetailsPage.submit()).click();
      await $(SectionCompaniesPage.submit()).click();
      await $(SubmitPage.submit()).click();
    });
  });

  describe("Given a journey through the list collector with repeating blocks, the companies can be added, removed and edited.", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_repeating_blocks_section_summary.json");
    });
    it("The user is able to add companies and complete repeating blocks.", async () => {
      await $(ResponsiblePartyPage.yes()).click();
      await $(AnyCompaniesOrBranchesPage.submit()).click();
      await $(AnyCompaniesOrBranchesPage.yes()).click();
      await $(AnyCompaniesOrBranchesPage.submit()).click();

      await $(AddCompanyPage.companyOrBranchName()).setValue("ONS");
      await $(AddCompanyPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(123);
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(1);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(1);
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();

      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await $(AddCompanyPage.companyOrBranchName()).setValue("GOV");
      await $(AddCompanyPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(456);
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(2);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(2);
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioNo()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioNo()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();

      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await $(AddCompanyPage.companyOrBranchName()).setValue("MOD");
      await $(AddCompanyPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(789);
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(3);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(3);
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();
    });

    it("The list collector shows all of the companies.", async () => {
      const companiesExpected = ["ONS", "GOV", "MOD"];
      checkItemsInList(companiesExpected, AnyOtherCompaniesOrBranchesPage.listLabel);
    });

    it("The list collector allows the name of 'GOV' to be changed", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.listEditLink(2)).click();
      await $(EditCompanyPage.companyOrBranchName()).setValue("Government");
      await $(EditCompanyPage.submit()).click();
      await expect(await $(AnyOtherCompaniesOrBranchesPage.listLabel(2)).getText()).to.equal("Government");
    });

    it("The list collector allows removal of 'Government'", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.listRemoveLink(2)).click();
      await $(RemoveCompanyPage.yes()).click();
      await $(RemoveCompanyPage.submit()).click();
    });

    it("The list collector does not show 'GOV' anymore.", async () => {
      await expect(await $(AnyOtherCompaniesOrBranchesPage.listLabel(2)).getText()).to.not.have.string("Government");
      await expect(await $(AnyOtherCompaniesOrBranchesPage.listLabel(2)).getText()).to.equal("MOD");
    });

    it("The list collector can add more companies.", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await $(AddCompanyPage.companyOrBranchName()).setValue("Council");
      await $(AddCompanyPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(101);
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(4);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(4);
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioNo()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();
    });

    it("The list collector shows all of the companies.", async () => {
      const companiesExpected = ["ONS", "MOD", "Council", "another one"];
      checkItemsInList(companiesExpected, AnyOtherCompaniesOrBranchesPage.listLabel);
    });

    it("The list collector can then be submitted", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();

      await $(AnyOtherTradingDetailsPage.submit()).click();
      await $(SectionCompaniesPage.submit()).click();
      await $(SubmitPage.submit()).click();
    });
  });

  describe("Given a journey through the list collector with repeating blocks, any incomplete repeating_block will be revisited before navigating to the next block after the list collector.", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_repeating_blocks_section_summary.json");
    });
    it("The user is able to add companies complete some repeating blocks and leave others incomplete.", async () => {
      await $(ResponsiblePartyPage.yes()).click();
      await $(AnyCompaniesOrBranchesPage.submit()).click();
      await $(AnyCompaniesOrBranchesPage.yes()).click();
      await $(AnyCompaniesOrBranchesPage.submit()).click();

      await $(AddCompanyPage.companyOrBranchName()).setValue("ONS");
      await $(AddCompanyPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(123);
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(1);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(1);
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();

      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await $(AddCompanyPage.companyOrBranchName()).setValue("GOV");
      await $(AddCompanyPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.cancelAndReturn()).click();

      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await $(AddCompanyPage.companyOrBranchName()).setValue("MOD");
      await $(AddCompanyPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(789);
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(3);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(3);
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await $(CompaniesRepeatingBlock2Page.cancelAndReturn()).click();

      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await $(AddCompanyPage.companyOrBranchName()).setValue("NAV");
      await $(AddCompanyPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(101);
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(4);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(4);
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();
    });

    it("The list collector shows all of the companies as well as checkmarks on the complete items 1 and 4, but not on the incomplete items 3 and 4.", async () => {
      const companiesExpected = ["ONS", "GOV", "MOD", "NAV"];
      checkItemsInList(companiesExpected, AnyOtherCompaniesOrBranchesPage.listLabel);
      checkListItemComplete(`dt[data-qa="list-item-1-label"]`);
      checkListItemIncomplete(`dt[data-qa="list-item-2-label"]`);
      checkListItemIncomplete(`dt[data-qa="list-item-3-label"]`);
      checkListItemComplete(`dt[data-qa="list-item-1-label"]`);
    });

    it("Attempting to complete the list collector will navigate the user to the first incomplete block of the second list item.", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(456);
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(2);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(2);
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioNo()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioNo()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();
    });

    it("Attempting to complete the list collector will navigate the user to the first incomplete block of the third list item.", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioNo()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();
    });

    it("All items are now marked as completed with the checkmark icon.", async () => {
      checkListItemComplete(`dt[data-qa="list-item-1-label"]`);
      checkListItemComplete(`dt[data-qa="list-item-2-label"]`);
      checkListItemComplete(`dt[data-qa="list-item-3-label"]`);
      checkListItemComplete(`dt[data-qa="list-item-4-label"]`);
    });

    it("The list collector can now be submitted.", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();

      await $(AnyOtherTradingDetailsPage.submit()).click();
      await $(SectionCompaniesPage.submit()).click();
      await $(SubmitPage.submit()).click();
    });
  });

  describe("Given a journey through the list collector with repeating blocks, the answers from repeating blocks can be edited.", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_repeating_blocks_section_summary.json");
    });
    it("The user is able to add companies, complete repeating blocks and navigate to the section summary.", async () => {
      await $(ResponsiblePartyPage.yes()).click();
      await $(AnyCompaniesOrBranchesPage.submit()).click();
      await $(AnyCompaniesOrBranchesPage.yes()).click();
      await $(AnyCompaniesOrBranchesPage.submit()).click();

      await $(AddCompanyPage.companyOrBranchName()).setValue("ONS");
      await $(AddCompanyPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(123);
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(1);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(1);
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();

      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await $(AddCompanyPage.companyOrBranchName()).setValue("GOV");
      await $(AddCompanyPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(456);
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(2);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(2);
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioNo()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();

      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();

      await $(AnyOtherTradingDetailsPage.submit()).click();
      await $(SectionCompaniesPage.submit()).click();
    });

    it("Edit each type of answer on different items from the section summary.", async () => {
      await expect(await $$(`dd[data-qa="registration-number"]`)[1].getText()).to.have.string(456);
      await $$(`a[data-qa="registration-number-edit"]`)[1].click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(789);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await expect(await $$(`dd[data-qa="registration-number"]`)[1].getText()).to.have.string(789);

      await expect(await $$(`dd[data-qa="registration-date"]`)[0].getText()).to.have.string("1 January 2023");
      await $$(`a[data-qa="registration-date-edit"]`)[0].click();
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(4);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(4);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await expect(await $$(`dd[data-qa="registration-date"]`)[0].getText()).to.have.string("4 April 2023");

      await expect(await $$(`dd[data-qa="authorised-trader-uk-radio"]`)[0].getText()).to.have.string("Yes");
      await $$(`a[data-qa="authorised-trader-uk-radio-edit"]`)[0].click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioNo()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();
      await expect(await $$(`dd[data-qa="authorised-trader-uk-radio"]`)[0].getText()).to.have.string("No");

      await expect(await $$(`dd[data-qa="authorised-trader-eu-radio"]`)[1].getText()).to.have.string("No answer provided");
      await $$(`a[data-qa="authorised-trader-eu-radio-edit"]`)[1].click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();
      await expect(await $$(`dd[data-qa="authorised-trader-eu-radio"]`)[1].getText()).to.have.string("Yes");
    });

    it("The list collector can then be submitted", async () => {
      await $(SubmitPage.submit()).click();
    });
  });
});
