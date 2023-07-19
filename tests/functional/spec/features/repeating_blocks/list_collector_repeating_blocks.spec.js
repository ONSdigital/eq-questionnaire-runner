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
import { repeatingAnswerChangeLink, checkItemsInList, checkListItemComplete, checkListItemIncomplete } from "../../../helpers";
import HubPage from "../../../base_pages/hub.page";

const summaryValues = 'dd[class="ons-summary__values"]';
async function proceedToListCollector() {
  await $(ResponsiblePartyPage.yes()).click();
  await $(AnyCompaniesOrBranchesPage.submit()).click();
  await $(AnyCompaniesOrBranchesPage.yes()).click();
  await $(AnyCompaniesOrBranchesPage.submit()).click();
}

async function addCompany(
  companyOrBranchName,
  registrationNumber,
  registrationDateDay,
  registrationDateMonth,
  registrationDateYear,
  authorisedTraderUk,
  authorisedTraderEu
) {
  await $(AddCompanyPage.companyOrBranchName()).setValue(companyOrBranchName);
  await $(AddCompanyPage.submit()).click();
  await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(registrationNumber);
  await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(registrationDateDay);
  await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(registrationDateMonth);
  await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(registrationDateYear);
  await $(CompaniesRepeatingBlock1Page.submit()).click();
  if (authorisedTraderUk) {
    await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioYes()).click();
  } else {
    await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioNo()).click();
  }
  if (authorisedTraderEu) {
    await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioYes()).click();
  } else if (authorisedTraderEu !== undefined) {
    await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioNo()).click();
  }
  await $(CompaniesRepeatingBlock2Page.submit()).click();
}

describe("List Collector Repeating Blocks", () => {
  describe("Given a normal journey through the list collector with repeating blocks, the answers can be submitted.", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_repeating_blocks_section_summary.json");
    });
    it("The user is able to add companies, complete repeating blocks, and submit.", async () => {
      await proceedToListCollector();
      await addCompany("ONS", 123, 1, 1, 2023, true, true);
      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await addCompany("GOV", 456, 2, 2, 2023, false, false);

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
      await proceedToListCollector();
      await addCompany("ONS", 123, 1, 1, 2023, true, true);
      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await addCompany("GOV", 456, 2, 2, 2023, false, false);
      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await addCompany("MOD", 789, 3, 3, 2023, true);
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
      await addCompany("Council", 101, 4, 4, 2023, false, true);
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
      await proceedToListCollector();

      await addCompany("ONS", 123, 1, 1, 2023, true, true);
      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await $(AddCompanyPage.companyOrBranchName()).setValue("GOV");
      await $(AddCompanyPage.submit()).click();
      await $(CompaniesRepeatingBlock1Page.cancelAndReturn()).click();
      await $(EditCompanyPage.cancelAndReturn()).click();

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
      await $(CompaniesRepeatingBlock1Page.cancelAndReturn()).click();
      await $(EditCompanyPage.cancelAndReturn()).click();

      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await addCompany("NAV", 101, 4, 4, 2023, true, true);
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
      await proceedToListCollector();
      await addCompany("ONS", 123, 1, 1, 2023, true, true);
      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await addCompany("GOV", 456, 2, 2, 2023, false);
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
      await $(AnyOtherTradingDetailsPage.submit()).click();
      await $(SectionCompaniesPage.submit()).click();
    });

    it("Edit each type of answer on different items from the section summary.", async () => {
      await expect(await $$(summaryValues)[8].getText()).to.have.string(456);
      await repeatingAnswerChangeLink(8).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(789);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await expect(await $$(summaryValues)[8].getText()).to.have.string(789);

      await expect(await $$(summaryValues)[4].getText()).to.have.string("1 January 2023");
      await repeatingAnswerChangeLink(4).click();
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(4);
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(4);
      await $(CompaniesRepeatingBlock1Page.submit()).click();
      await expect(await $$(summaryValues)[4].getText()).to.have.string("4 April 2023");

      await expect(await $$(summaryValues)[5].getText()).to.have.string("Yes");
      await repeatingAnswerChangeLink(5).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioNo()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();
      await expect(await $$(summaryValues)[5].getText()).to.have.string("No");

      await expect(await $$(summaryValues)[11].getText()).to.have.string("No answer provided");
      await repeatingAnswerChangeLink(11).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioYes()).click();
      await $(CompaniesRepeatingBlock2Page.submit()).click();
      await expect(await $$(summaryValues)[11].getText()).to.have.string("Yes");
    });

    it("The list collector can then be submitted", async () => {
      await $(SubmitPage.submit()).click();
    });
  });
});

describe("Given a journey through the list collector with repeating blocks, in a mandatory section of  hub questionnaire, the incomplete repeating blocks mark the list collector incomplete and thus navigate back there.", () => {
  before("Load the survey", async () => {
    await browser.openQuestionnaire("test_list_collector_repeating_blocks_with_hub.json");
  });
  it("The user is able to add a compete company and an incomplete company.", async () => {
    await proceedToListCollector();

    await addCompany("ONS", 123, 1, 1, 2023, true, true);
    await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
    await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
    await $(AddCompanyPage.companyOrBranchName()).setValue("GOV");
    await $(AddCompanyPage.submit()).click();
    await $(CompaniesRepeatingBlock1Page.cancelAndReturn()).click();
  });

  it("Navigating to the root of the questionnaire will redirect to the incomplete list collector, which we can then complete.", async () => {
    await browser.url("questionnaire/");
    await expect(await browser.getUrl()).to.contain(AnyOtherCompaniesOrBranchesPage.url());

    await $(AnyOtherCompaniesOrBranchesPage.no()).click();
    await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
    await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(456);
    await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(2);
    await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(2);
    await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
    await $(CompaniesRepeatingBlock1Page.submit()).click();
    await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioNo()).click();
    await $(CompaniesRepeatingBlock2Page.submit()).click();
  });

  it("Another incomplete item can be added via the section summary.", async () => {
    await $(AnyOtherCompaniesOrBranchesPage.no()).click();
    await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
    await $(AnyOtherTradingDetailsPage.submit()).click();
    await $(SectionCompaniesPage.companiesListAddLink()).click();
    await $(AddCompanyPage.companyOrBranchName()).setValue("MOD");
    await $(AddCompanyPage.submit()).click();
    await $(CompaniesRepeatingBlock1Page.cancelAndReturn()).click();
  });

  it("Navigating to the submit page of the section will redirect to the incomplete list collector, which we can then complete.", async () => {
    await browser.url("questionnaire/sections/section-companies/");
    await expect(await browser.getUrl()).to.contain(AnyOtherCompaniesOrBranchesPage.url());

    await $(AnyOtherCompaniesOrBranchesPage.no()).click();
    await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
    await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(789);
    await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(3);
    await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(3);
    await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(2023);
    await $(CompaniesRepeatingBlock1Page.submit()).click();
    await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioYes()).click();
    await $(CompaniesRepeatingBlock2Page.submit()).click();
  });

  it("The section can now be submitted and and hub completed.", async () => {
    await $(AnyOtherCompaniesOrBranchesPage.no()).click();
    await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
    await $(SectionCompaniesPage.submit()).click();
    await $(HubPage.submit()).click();
  });
});
