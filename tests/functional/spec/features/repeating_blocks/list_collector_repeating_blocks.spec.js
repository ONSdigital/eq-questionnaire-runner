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
import { repeatingAnswerChangeLink, checkItemsInList, checkListItemComplete, checkListItemIncomplete, click } from "../../../helpers";
import HubPage from "../../../base_pages/hub.page";
import ResponsiblePartyHubPage from "../../../generated_pages/list_collector_repeating_blocks_with_hub/responsible-party-business.page";
import { expect } from "@wdio/globals";
import ThankYouPage from "../../../base_pages/thank-you.page";

const summaryValues = 'dd[class="ons-summary__values"]';
async function proceedToListCollector() {
  await $(ResponsiblePartyPage.yes()).click();
  await click(AnyCompaniesOrBranchesPage.submit());
  await $(AnyCompaniesOrBranchesPage.yes()).click();
  await click(AnyCompaniesOrBranchesPage.submit());
}

async function addCompany(
  companyOrBranchName,
  registrationNumber,
  registrationDateDay,
  registrationDateMonth,
  registrationDateYear,
  authorisedTraderUk,
  authorisedTraderEu,
) {
  await $(AddCompanyPage.companyOrBranchName()).setValue(companyOrBranchName);
  await click(AddCompanyPage.submit());
  await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue(registrationNumber);
  await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue(registrationDateDay);
  await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue(registrationDateMonth);
  await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue(registrationDateYear);
  await click(CompaniesRepeatingBlock1Page.submit());
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
  await click(CompaniesRepeatingBlock2Page.submit());
}

describe("List Collector Repeating Blocks", () => {
  describe("Given a normal journey through the list collector with repeating blocks", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_repeating_blocks_section_summary.json");
      // These tests sometimes fail when a button is on the screen, but right on the very edge, accept cookies to increase screen space
      await $(ResponsiblePartyPage.acceptCookies()).click();
    });
    it("When the user adds items and completes all of the repeating blocks, Then they are able to successfully submit the questionnaire.", async () => {
      await proceedToListCollector();
      await addCompany("ONS", "123", "1", "1", "2023", true, true);
      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await addCompany("GOV", "456", "2", "2", "2023", false, false);

      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());

      await click(AnyOtherTradingDetailsPage.submit());
      await click(SectionCompaniesPage.submit());
      await click(SubmitPage.submit());
      await expect(await browser.getUrl()).toContain(ThankYouPage.pageName);
    });
  });

  describe("Given a journey through the list collector with repeating blocks where items need to be updated", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_repeating_blocks_section_summary.json");
    });
    it("When the user adds items to the list and completes the repeating blocks, Then the completed items are displayed on the list collector page.", async () => {
      await proceedToListCollector();
      await addCompany("ONS", "123", "1", "1", "2023", true, true);
      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await addCompany("GOV", "456", "2", "2", "2023", false, false);
      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await addCompany("MOD", "789", "3", "3", "2023", true);
      checkItemsInList(["ONS", "GOV", "MOD"], AnyOtherCompaniesOrBranchesPage.listLabel);
    });

    it("When the user edits an item, Then the name of the item is able to be changed", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.listEditLink(2)).click();
      await $(EditCompanyPage.companyOrBranchName()).setValue("Government");
      await click(EditCompanyPage.submit());
      await expect(await $(AnyOtherCompaniesOrBranchesPage.listLabel(2)).getText()).toBe("Government");
    });

    it("When the user clicks the remove link, Then the item selected is removed", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.listRemoveLink(2)).click();
      await $(RemoveCompanyPage.yes()).click();
      await click(RemoveCompanyPage.submit());
      checkItemsInList(["ONS", "MOD"], AnyOtherCompaniesOrBranchesPage.listLabel);
      await expect(await $(AnyOtherCompaniesOrBranchesPage.listLabel(2)).getText()).not.toContain("Government");
      await expect(await $(AnyOtherCompaniesOrBranchesPage.listLabel(2)).getText()).toBe("MOD");
    });

    it("When a user has finished editing or removing from the list, Then they are still able to add additional companies", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await addCompany("Council", "101", "4", "4", "2023", false, true);
      checkItemsInList(["ONS", "MOD", "Council"], AnyOtherCompaniesOrBranchesPage.listLabel);
    });

    it("When a user has finished making changes to the list, Then section can be completed and the questionnaire submitted", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());

      await click(AnyOtherTradingDetailsPage.submit());
      await click(SectionCompaniesPage.submit());
      await click(SubmitPage.submit());
      await expect(await browser.getUrl()).toContain(ThankYouPage.pageName);
    });
  });

  describe("Given a journey that test routes through the list collector with repeating blocks.", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_repeating_blocks_section_summary.json");
    });
    it("When the user only completes some of the repeating blocks and leaves others incomplete, Then on the list collector page only completed items should display the completed checkmark icon.", async () => {
      await proceedToListCollector();

      await addCompany("ONS", "123", "1", "1", "2023", true, true);
      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await $(AddCompanyPage.companyOrBranchName()).setValue("GOV");
      await click(AddCompanyPage.submit());
      await $(CompaniesRepeatingBlock1Page.cancelAndReturn()).click();
      await $(EditCompanyPage.cancelAndReturn()).click();

      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await $(AddCompanyPage.companyOrBranchName()).setValue("MOD");
      await click(AddCompanyPage.submit());
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue("789");
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue("3");
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue("3");
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue("2023");
      await click(CompaniesRepeatingBlock1Page.submit());
      await $(CompaniesRepeatingBlock2Page.cancelAndReturn()).click();
      await $(CompaniesRepeatingBlock1Page.cancelAndReturn()).click();
      await $(EditCompanyPage.cancelAndReturn()).click();

      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await addCompany("NAV", "101", "4", "4", "2023", true, true);

      // Only the ONS and NAV items should be complete
      checkItemsInList(["ONS", "GOV", "MOD", "NAV"], AnyOtherCompaniesOrBranchesPage.listLabel);
      checkListItemComplete(`dt[data-qa="list-item-1-label"]`);
      checkListItemIncomplete(`dt[data-qa="list-item-2-label"]`);
      checkListItemIncomplete(`dt[data-qa="list-item-3-label"]`);
      checkListItemComplete(`dt[data-qa="list-item-1-label"]`);
    });

    it("When an item has incomplete repeating blocks, Then using submit on the list collector page will navigate the user to the first incomplete repeating block.", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await expect(await browser.getUrl()).toContain(CompaniesRepeatingBlock1Page.pageName);
    });

    it("When there are multiple incomplete items and only the first incomplete item is completed, Then attempting using Submit on the list collector page will navigate the user to the next incomplete item.", async () => {
      // Complete the first incomplete list item
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue("456");
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue("2");
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue("2");
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue("2023");
      await click(CompaniesRepeatingBlock1Page.submit());
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioNo()).click();
      await $(CompaniesRepeatingBlock2Page.authorisedTraderEuRadioNo()).click();
      await click(CompaniesRepeatingBlock2Page.submit());

      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());

      // The user is taken to the next incomplete repeating block
      await expect(await browser.getUrl()).toContain(CompaniesRepeatingBlock2Page.pageName);
    });

    it("When the last remaining incomplete repeating block is completed, Then all items are marked as completed with the checkmark icon.", async () => {
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioNo()).click();
      await click(CompaniesRepeatingBlock2Page.submit());
      checkListItemComplete(`dt[data-qa="list-item-1-label"]`);
      checkListItemComplete(`dt[data-qa="list-item-2-label"]`);
      checkListItemComplete(`dt[data-qa="list-item-3-label"]`);
      checkListItemComplete(`dt[data-qa="list-item-4-label"]`);
    });

    it("When the user clicks a change link from the section summary and submits without changing an answer, Then the user is returned to the section summary anchored to the answer they clicked on", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await click(AnyOtherTradingDetailsPage.submit());

      await $(SectionCompaniesPage.anyOtherTradingDetailsAnswerEdit()).click();
      await click(AnyOtherTradingDetailsPage.submit());
      await expect(await browser.getUrl()).toContain("section-companies/#any-other-trading-details-answer");

      await $(SectionCompaniesPage.anyOtherTradingDetailsAnswerEdit()).click();
      await $(AnyOtherTradingDetailsPage.previous()).click();
      await expect(await browser.getUrl()).toContain("section-companies/#any-other-trading-details-answer");
    });

    it("When an answer is edited from the section summary which does not affect progress, Then pressing continue returns the user to the section summary anchored to the answer they edited", async () => {
      await $(SectionCompaniesPage.anyOtherTradingDetailsAnswerEdit()).click();
      await $(AnyOtherTradingDetailsPage.answer()).setValue("No");
      await click(AnyOtherTradingDetailsPage.submit());
      await expect(await browser.getUrl()).toContain("section-companies/#any-other-trading-details-answer");
    });

    it("When a user clicks a change link from the final summary and submits without changing an answer, Then the user is returned to the final summary anchored to the answer they clicked on", async () => {
      await click(SectionCompaniesPage.submit());

      await $(SubmitPage.anyOtherTradingDetailsAnswerEdit()).click();
      await click(AnyOtherTradingDetailsPage.submit());
      await expect(await browser.getUrl()).toContain("submit/#any-other-trading-details-answer");

      await $(SubmitPage.anyOtherTradingDetailsAnswerEdit()).click();
      await $(AnyOtherTradingDetailsPage.previous()).click();
      await expect(await browser.getUrl()).toContain("submit/#any-other-trading-details-answer");
    });

    it("When an an answer is edited from the final summary which does not affect progress, Then pressing continue returns the user to the final summary anchored to the answer they edited", async () => {
      await $(SectionCompaniesPage.anyOtherTradingDetailsAnswerEdit()).click();
      await $(AnyOtherTradingDetailsPage.answer()).setValue("Yes");
      await click(AnyOtherTradingDetailsPage.submit());
      await expect(await browser.getUrl()).toContain("submit/#any-other-trading-details-answer");
    });

    it("When all items are completed by the user, Then the questionnaire is able to be submitted.", async () => {
      await click(SubmitPage.submit());
      await expect(await browser.getUrl()).toContain(ThankYouPage.pageName);
    });
  });

  describe("Given a journey through the list collector with repeating blocks", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_repeating_blocks_section_summary.json");
    });
    it("When the user adds and completes items, Then they are able to see the items on the section summary page.", async () => {
      await proceedToListCollector();
      await addCompany("ONS", "123", "1", "1", "2023", true, true);
      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await addCompany("GOV", "456", "2", "2", "2023", false);
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await click(AnyOtherTradingDetailsPage.submit());
      await click(SectionCompaniesPage.submit());
      await expect(await $$(summaryValues)[2].getText()).toContain("ONS");
      await expect(await $$(summaryValues)[4].getText()).toContain("1 January 2023");
      await expect(await $$(summaryValues)[5].getText()).toContain("Yes");
      await expect(await $$(summaryValues)[7].getText()).toContain("GOV");
      await expect(await $$(summaryValues)[8].getText()).toContain("456");
      await expect(await $$(summaryValues)[11].getText()).toContain("No answer provided");
    });

    it("When an item is edited from the section summary page, Then the correct value is displayed when the user returns to the summary.", async () => {
      await expect(await $$(summaryValues)[8].getText()).toContain("456");
      await repeatingAnswerChangeLink(8).click();
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue("789");
      await click(CompaniesRepeatingBlock1Page.submit());
      await expect(await $$(summaryValues)[8].getText()).toContain("789");
    });
  });

  describe("Given the user is completing a list collector with repeating blocks in a mandatory section of a hub based questionnaire.", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_repeating_blocks_with_hub.json");
    });
    it("When the user adds complete and incomplete items and returns to the hub, Then the user should be taken to first incomplete repeating block when pressing Continue.", async () => {
      await proceedToListCollector();

      await addCompany("ONS", "123", "1", "1", "2023", true, true);
      await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await $(AddCompanyPage.companyOrBranchName()).setValue("GOV");
      await click(AddCompanyPage.submit());
      await $(CompaniesRepeatingBlock1Page.cancelAndReturn()).click();
      await browser.url("questionnaire/");
      await click(HubPage.submit());
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await expect(await browser.getUrl()).toContain(CompaniesRepeatingBlock1Page.pageName);
    });

    it("When the user completes the incomplete blocks and returns to the list collector Page, Then the completed items should display the checkmark icon", async () => {
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue("456");
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue("2");
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue("2");
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue("2023");
      await click(CompaniesRepeatingBlock1Page.submit());
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioNo()).click();
      await click(CompaniesRepeatingBlock2Page.submit());
      await expect(await browser.getUrl()).toContain(AnyOtherCompaniesOrBranchesPage.pageName);
      checkListItemComplete(`dt[data-qa="list-item-1-label"]`);
      checkListItemComplete(`dt[data-qa="list-item-2-label"]`);
    });

    it("When another incomplete item is added via the section summary, Then navigating to the submit page of the section will redirect to the list collector page.", async () => {
      // Add another item and partially complete
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await click(AnyOtherTradingDetailsPage.submit());
      await $(SectionCompaniesPage.companiesListAddLink()).click();
      await $(AddCompanyPage.companyOrBranchName()).setValue("MOD");
      await click(AddCompanyPage.submit());
      await $(CompaniesRepeatingBlock1Page.cancelAndReturn()).click();

      // Navigating to the section summary will redirect to the list collector page
      await browser.url("questionnaire/sections/section-companies/");
      await expect(await browser.getUrl()).toContain(AnyOtherCompaniesOrBranchesPage.url());
    });

    it("When the incomplete repeating blocks are completed, Then the user is able to complete the section and is taken to the hub page.", async () => {
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue("789");
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue("3");
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue("3");
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue("2023");
      await click(CompaniesRepeatingBlock1Page.submit());
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioYes()).click();
      await click(CompaniesRepeatingBlock2Page.submit());
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await click(SectionCompaniesPage.submit());
      await expect(await browser.getUrl()).toContain(HubPage.pageName);
    });

    it("When the user is on the Hub page and has completed the section, Then they are able to add additional companies using the Add link", async () => {
      await $(HubPage.summaryRowLink("section-companies")).click();
      await $(SectionCompaniesPage.companiesListAddLink()).click();
      await $(AddCompanyPage.companyOrBranchName()).setValue("MOJ");
      await click(AddCompanyPage.submit());
      await $(CompaniesRepeatingBlock1Page.registrationNumber()).setValue("789");
      await $(CompaniesRepeatingBlock1Page.registrationDateday()).setValue("3");
      await $(CompaniesRepeatingBlock1Page.registrationDatemonth()).setValue("3");
      await $(CompaniesRepeatingBlock1Page.registrationDateyear()).setValue("2023");
      await click(CompaniesRepeatingBlock1Page.submit());
      await $(CompaniesRepeatingBlock2Page.authorisedTraderUkRadioYes()).click();
      await click(CompaniesRepeatingBlock2Page.submit());
      await $(AnyOtherCompaniesOrBranchesPage.no()).click();
      await click(AnyOtherCompaniesOrBranchesPage.submit());
      await click(SectionCompaniesPage.submit());
      await expect(await browser.getUrl()).toContain(HubPage.pageName);
    });

    it("When the user has completed the list collector section and uses Submit on the hub page, Then the user will be redirected to the next section.", async () => {
      await click(HubPage.submit());
      await expect(browser).toHaveUrlContaining(ResponsiblePartyHubPage.pageName);
    });
  });
});
