import AnyOtherCompaniesOrBranchesPage from "../generated_pages/list_collector_content_page/any-other-companies-or-branches.page.js";
import AnyCompaniesOrBranchesAddPage from "../generated_pages/list_collector_content_page/any-other-companies-or-branches-add.page.js";
import AnyCompaniesOrBranchesPage from "../generated_pages/list_collector_content_page/any-companies-or-branches.page";
import CompaniesSummaryPage from "../generated_pages/list_collector_content_page/section-companies-summary.page";
import HubPage from "../base_pages/hub.page";
import ListCollectorFirstRepeatingBlockPage from "../generated_pages/list_collector_content_page/companies-repeating-block-1-repeating-block.page";
import ListCollectorSecondRepeatingBlockPage from "../generated_pages/list_collector_content_page/companies-repeating-block-2-repeating-block.page";
import ListCollectorContentPage from "../generated_pages/list_collector_content_page/list-collector-content.page";
import ListCollectorContentSectionSummaryPage from "../generated_pages/list_collector_content_page/section-list-collector-contents-summary.page";

describe("List Collector Section Summary and Summary Items", () => {
  describe("Given I launch the test list collector section summary items survey", () => {
    beforeEach(async () => {
      await browser.openQuestionnaire("test_list_collector_content_page.json");
    });
    it("When I get to the Hub, Then from there the next block in list collector content section should be list collector content page.", async () => {
      await fillInListCollectorSection();
      await expect(await browser.getUrl()).to.contain(HubPage.url());
      await expect(await $(HubPage.summaryRowState("section-list-collector-contents")).getText()).to.contain("Not started");
      await $(HubPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(ListCollectorContentPage.url());
    });
    it("When I get to the list collector content page, Then the relevant content is displayed.", async () => {
      await fillInListCollectorSection();
      await $(HubPage.submit()).click();
      await expect(await $("#main-content").getText()).to.contain(
        "You have previously reported the following companies. Press continue to updated registration and trading information."
      );
      await expect(await $(ListCollectorContentPage.questionText()).getHTML()).to.contain("Companies");
    });
    it("When I get to list collector content block section, Then I should be able to complete repeating blocks and get to the summary.", async () => {
      await fillInListCollectorSection();
      await $(HubPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(ListCollectorContentPage.url());
      await $(ListCollectorContentPage.submit()).click();
      await $(ListCollectorFirstRepeatingBlockPage.registrationNumberRepeatingBlock()).setValue(123);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockday()).setValue(1);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockmonth()).setValue(1);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockyear()).setValue(1990);
      await $(ListCollectorFirstRepeatingBlockPage.submit()).click();
      await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderUkRadioRepeatingBlockYes()).click();
      await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderEuRadioRepeatingBlockYes()).click();
      await $(ListCollectorSecondRepeatingBlockPage.submit()).click();
      await $(ListCollectorContentPage.submit()).click();
      await $(ListCollectorFirstRepeatingBlockPage.registrationNumberRepeatingBlock()).setValue(456);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockday()).setValue(1);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockmonth()).setValue(1);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockyear()).setValue(1990);
      await $(ListCollectorFirstRepeatingBlockPage.submit()).click();
      await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderUkRadioRepeatingBlockYes()).click();
      await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderEuRadioRepeatingBlockYes()).click();
      await $(ListCollectorSecondRepeatingBlockPage.submit()).click();
      await $(ListCollectorContentPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(ListCollectorContentSectionSummaryPage.url());
    });
    it("When I fill in first item repeating blocks, Then after going back to the hub the section should be in progress.", async () => {
      await fillInListCollectorSection();
      await $(HubPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(ListCollectorContentPage.url());
      await $(ListCollectorContentPage.submit()).click();
      await $(ListCollectorFirstRepeatingBlockPage.registrationNumberRepeatingBlock()).setValue(123);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockday()).setValue(1);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockmonth()).setValue(1);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockyear()).setValue(1990);
      await $(ListCollectorFirstRepeatingBlockPage.submit()).click();
      await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderUkRadioRepeatingBlockYes()).click();
      await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderEuRadioRepeatingBlockYes()).click();
      await $(ListCollectorSecondRepeatingBlockPage.submit()).click();
      await $(ListCollectorContentPage.previous()).click();
      await expect(await $(HubPage.summaryRowState("section-list-collector-contents")).getText()).to.contain("Partially completed");
    });
    it("When I fill in both items repeating blocks, Then after going back to the hub the section should be completed.", async () => {
      await fillInListCollectorSection();
      await $(HubPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(ListCollectorContentPage.url());
      await $(ListCollectorContentPage.submit()).click();
      await $(ListCollectorFirstRepeatingBlockPage.registrationNumberRepeatingBlock()).setValue(123);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockday()).setValue(1);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockmonth()).setValue(1);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockyear()).setValue(1990);
      await $(ListCollectorFirstRepeatingBlockPage.submit()).click();
      await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderUkRadioRepeatingBlockYes()).click();
      await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderEuRadioRepeatingBlockYes()).click();
      await $(ListCollectorSecondRepeatingBlockPage.submit()).click();
      await $(ListCollectorContentPage.submit()).click();
      await $(ListCollectorFirstRepeatingBlockPage.registrationNumberRepeatingBlock()).setValue(456);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockday()).setValue(1);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockmonth()).setValue(1);
      await $(ListCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockyear()).setValue(1990);
      await $(ListCollectorFirstRepeatingBlockPage.submit()).click();
      await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderUkRadioRepeatingBlockYes()).click();
      await $(ListCollectorSecondRepeatingBlockPage.authorisedTraderEuRadioRepeatingBlockYes()).click();
      await $(ListCollectorSecondRepeatingBlockPage.submit()).click();
      await $(ListCollectorContentPage.submit()).click();
      await $(ListCollectorContentSectionSummaryPage.previous()).click();
      await $(ListCollectorContentPage.previous()).click();
      await expect(await $(HubPage.summaryRowState("section-list-collector-contents")).getText()).to.contain("Completed");
    });
  });
});
const fillInListCollectorSection = async () => {
  await $(AnyCompaniesOrBranchesPage.yes()).click();
  await $(AnyCompaniesOrBranchesPage.submit()).click();
  await addCompany("Company A", "123", true);
  await anyMoreCompaniesYes();
  await addCompany("Company B", "456", true);
  await anyMoreCompaniesNo();
  await $(CompaniesSummaryPage.submit()).click();
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
  await $(AnyOtherCompaniesOrBranchesPage.yes()).click();
  await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
};

const anyMoreCompaniesNo = async () => {
  await $(AnyOtherCompaniesOrBranchesPage.no()).click();
  await $(AnyOtherCompaniesOrBranchesPage.submit()).click();
};
