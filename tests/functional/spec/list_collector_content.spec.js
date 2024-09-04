import AnyOtherCompaniesOrBranchesPage from "../generated_pages/list_collector_content_page/any-other-companies-or-branches.page.js";
import AnyCompaniesOrBranchesAddPage from "../generated_pages/list_collector_content_page/any-other-companies-or-branches-add.page.js";
import AnyCompaniesOrBranchesRemovePage from "../generated_pages/list_collector_content_page/any-other-companies-or-branches-remove.page.js";

import AnyCompaniesOrBranchesPage from "../generated_pages/list_collector_content_page/any-companies-or-branches.page";
import CompaniesSummaryPage from "../generated_pages/list_collector_content_page/section-companies-summary.page";
import HubPage from "../base_pages/hub.page";
import ResponsiblePartyQuestionPage from "../generated_pages/list_collector_content_page/responsible-party.page";
import ListCollectorFirstRepeatingBlockPage from "../generated_pages/list_collector_content_page/companies-repeating-block-1-repeating-block.page";
import ListCollectorSecondRepeatingBlockPage from "../generated_pages/list_collector_content_page/companies-repeating-block-2-repeating-block.page";
import ListCollectorContentPage from "../generated_pages/list_collector_content_page/list-collector-content.page";
import ListCollectorContentSectionSummaryPage from "../generated_pages/list_collector_content_page/section-list-collector-contents-summary.page";
import ConfirmationCheckboxPage from "../generated_pages/list_collector_content_page/confirmation-checkbox.page";
import { checkListItemComplete, checkListItemIncomplete, click } from "../helpers";

describe("List Collector Section Summary and Summary Items", () => {
  describe("Given I launch the test list collector section summary items survey", () => {
    beforeEach(async () => {
      await browser.openQuestionnaire("test_list_collector_content_page.json");
    });
    it("When I get to the Hub, Then from there the next block in list collector content section should be list collector content page.", async () => {
      await fillInListCollectorSection();
      await expect(browser).toHaveUrlContaining(HubPage.url());
      await expect(await $(HubPage.summaryRowState("section-list-collector-contents")).getText()).toBe("Not started");
      await click(HubPage.submit());
      await $(ResponsiblePartyQuestionPage.yes()).click();
      await click(ResponsiblePartyQuestionPage.submit());
      await expect(browser).toHaveUrlContaining(ListCollectorContentPage.url());
    });
    it("When I get to the list collector content page, Then the relevant content and button is displayed.", async () => {
      await fillInListCollectorSection();
      await click(HubPage.submit());
      await $(ResponsiblePartyQuestionPage.yes()).click();
      await click(ResponsiblePartyQuestionPage.submit());
      await expect(await $(ListCollectorContentPage.heading()).getHTML()).toContain("Companies");
      await expect(await $("#main-content > p").getText()).toBe(
        "You have previously reported the following companies. Press continue to updated registration and trading information.",
      );
      await expect(await $("#main-content > #guidance-1").getText()).toContain("Include all companies");
      await expect(await $("#main-content > #definition").getText()).toBe("Companies definition");
      await expect(await $(ListCollectorContentPage.submit()).getText()).toBe("Continue");
    });
    it("When I get to list collector content block section, Then I should be able to complete repeating blocks and get to the summary.", async () => {
      await fillInListCollectorSection();
      await click(HubPage.submit());
      await $(ResponsiblePartyQuestionPage.yes()).click();
      await click(ResponsiblePartyQuestionPage.submit());
      await click(ListCollectorContentPage.submit());
      await completeRepeatingBlocks(123, 1, 1, 1990, true, true);
      await click(ListCollectorContentPage.submit());
      await completeRepeatingBlocks(456, 1, 1, 1990, true, true);
      await click(ListCollectorContentPage.submit());
      await expect(browser).toHaveUrlContaining(ListCollectorContentSectionSummaryPage.url());
    });
    it("When I fill in first item repeating blocks, Then after going back to the hub the section should be in progress.", async () => {
      await fillInListCollectorSection();
      await click(HubPage.submit());
      await $(ResponsiblePartyQuestionPage.yes()).click();
      await click(ResponsiblePartyQuestionPage.submit());
      await click(ListCollectorContentPage.submit());
      await completeRepeatingBlocks(123, 1, 1, 1990, true, true);
      await $(ListCollectorContentPage.previous()).click();
      await $(ResponsiblePartyQuestionPage.previous()).click();
      await expect(await $(HubPage.summaryRowState("section-list-collector-contents")).getText()).toBe("Partially completed");
    });
    it("When I fill in both items repeating blocks, Then after going back to the hub the section should be completed.", async () => {
      await fillInListCollectorSection();
      await click(HubPage.submit());
      await $(ResponsiblePartyQuestionPage.yes()).click();
      await click(ResponsiblePartyQuestionPage.submit());
      await click(ListCollectorContentPage.submit());
      await completeRepeatingBlocks(123, 1, 1, 1990, true, true);
      await click(ListCollectorContentPage.submit());
      await completeRepeatingBlocks(456, 1, 1, 1990, true, true);
      await click(ListCollectorContentPage.submit());
      await $(ListCollectorContentSectionSummaryPage.previous()).click();
      await $(ListCollectorContentPage.previous()).click();
      await $(ResponsiblePartyQuestionPage.previous()).click();
      await expect(await $(HubPage.summaryRowState("section-list-collector-contents")).getText()).toBe("Completed");
    });
    it("When I complete both sections then add another item, The list collector content block reverts to in progress and the new repeating blocks need completing", async () => {
      await completeBothSections();
      await expect(await $(HubPage.summaryRowState("section-list-collector-contents")).getText()).toBe("Completed");
      await $(HubPage.summaryRowLink("section-companies")).click();
      await expect(browser).toHaveUrlContaining(CompaniesSummaryPage.pageName);
      await $(CompaniesSummaryPage.companiesListAddLink()).click();
      await addCompany("Company C", "789", false);
      await anyMoreCompaniesNo();
      await $(ConfirmationCheckboxPage.yes()).click();
      await click(ConfirmationCheckboxPage.submit());
      await click(CompaniesSummaryPage.submit());
      await expect(await $(HubPage.summaryRowState("section-list-collector-contents")).getText()).toBe("Partially completed");
      await click(HubPage.submit());
      await expect(browser).toHaveUrlContaining(ListCollectorContentPage.pageName);
      await checkListItemComplete(`li[data-qa="list-item-1-label"]`);
      await checkListItemComplete(`li[data-qa="list-item-2-label"]`);
      await checkListItemIncomplete(`li[data-qa="list-item-3-label"]`);
      await click(ListCollectorContentPage.submit());
      await expect(browser).toHaveUrlContaining(ListCollectorFirstRepeatingBlockPage.pageName);
      await completeRepeatingBlocks(666, 2, 5, 1995, true, true);
      await checkListItemComplete(`li[data-qa="list-item-3-label"]`);
      await click(ListCollectorContentPage.submit());
      await click(ListCollectorContentSectionSummaryPage.submit());
      await expect(await $(HubPage.summaryRowState("section-list-collector-contents")).getText()).toBe("Completed");
    });
    // :TODO: Currently, this is expected behaviour, if list collector content blocks no longer need revisiting after removing items, this test needs updating.
    it("When I complete both sections then remove a list item item, Then the list collector content block reverts to in progress the list summary is revisited", async () => {
      await completeBothSections();
      await expect(await $(HubPage.summaryRowState("section-list-collector-contents")).getText()).toBe("Completed");
      await $(HubPage.summaryRowLink("section-companies")).click();
      await $(CompaniesSummaryPage.companiesListRemoveLink(1)).click();
      await $(AnyCompaniesOrBranchesRemovePage.yes()).click();
      await click(AnyCompaniesOrBranchesRemovePage.submit());
      await click(CompaniesSummaryPage.submit());
      await expect(await $(HubPage.summaryRowState("section-list-collector-contents")).getText()).toBe("Partially completed");
      await click(HubPage.submit());
      await checkListItemComplete(`p[data-qa="list-item-1-label"]`);
      await click(ListCollectorContentPage.submit());
      await expect(browser).toHaveUrlContaining(ListCollectorContentSectionSummaryPage.pageName);
      await click(ListCollectorContentSectionSummaryPage.submit());
      await expect(await $(HubPage.summaryRowState("section-list-collector-contents")).getText()).toBe("Completed");
    });
  });
});
const fillInListCollectorSection = async () => {
  await $(AnyCompaniesOrBranchesPage.yes()).click();
  await click(AnyCompaniesOrBranchesPage.submit());
  await addCompany("Company A", "123", true);
  await anyMoreCompaniesYes();
  await addCompany("Company B", "456", true);
  await anyMoreCompaniesNo();
  await click(CompaniesSummaryPage.submit());
};

const completeBothSections = async () => {
  await fillInListCollectorSection();
  await click(HubPage.submit());
  await $(ResponsiblePartyQuestionPage.yes()).click();
  await click(ResponsiblePartyQuestionPage.submit());
  await click(ListCollectorContentPage.submit());
  await completeRepeatingBlocks(654, 2, 6, 1999, true, true);
  await click(ListCollectorContentPage.submit());
  await completeRepeatingBlocks(655, 12, 1, 1989, true, false);
  await click(ListCollectorContentPage.submit());
  await click(ListCollectorContentSectionSummaryPage.submit());
};

const completeRepeatingBlocks = async (registrationNumber, day, month, year, authorisedUk, authorisedEu) => {
  await $(ListCollectorFirstRepeatingBlockPage.registrationNumberRepeatingBlock()).setValue(registrationNumber);
  await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockday()).setValue(day);
  await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockmonth()).setValue(month);
  await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockyear()).setValue(year);
  await click(ListCollectorFirstRepeatingBlockPage.submit());
  if (authorisedUk) {
    await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderUkRadioRepeatingBlockYes()).click();
  } else {
    await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderUkRadioRepeatingBlockNo()).click();
  }
  if (authorisedEu) {
    await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderEuRadioRepeatingBlockYes()).click();
  } else {
    await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderEuRadioRepeatingBlockNo()).click();
  }
  await click(ListCollectorSecondRepeatingBlockPage.submit());
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
  await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
  await click(AnyOtherCompaniesOrBranchesPage.submit());
};

const anyMoreCompaniesNo = async () => {
  await $(AnyOtherCompaniesOrBranchesPage.no()).click();
  await click(AnyOtherCompaniesOrBranchesPage.submit());
};
