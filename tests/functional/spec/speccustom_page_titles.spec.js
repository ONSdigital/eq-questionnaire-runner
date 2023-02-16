import DateOfBirthPage from "../generated_pages/custom_page_titles/date-of-birth.page.js";
import HubPage from "../base_pages/hub.page.js";
import IndividualInterstitialPage from "../generated_pages/custom_page_titles/individual-interstitial.page.js";
import ListCollectorAddPage from "../generated_pages/custom_page_titles/list-collector-add.page.js";
import ListCollectorEditPage from "../generated_pages/custom_page_titles/list-collector-edit.page.js";
import ListCollectorPage from "../generated_pages/custom_page_titles/list-collector.page.js";
import ProxyPage from "../generated_pages/custom_page_titles/proxy.page.js";
import RelationshipsPage from "../generated_pages/custom_page_titles/relationships.page.js";

describe("Feature: Custom Page Titles", () => {
  const schema = "test_custom_page_titles.json";

  describe("Given I am completing the test_custom_page_titles survey,", () => {
    before("load the survey", async ()=> {
      await browser.openQuestionnaire(schema);
    });

    it("When I navigate to the list collector page, Then I should see the custom page title", async ()=> {
      await $(await HubPage.submit()).click();
      const expectedPageTitle = browser.getTitle();
      await expect(expectedPageTitle).to.equal("Custom page title - Test Custom Page Titles");
    });

    it("When I navigate to the add person page, Then I should see the custom page title", async ()=> {
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      let expectedPageTitle = browser.getTitle();
      await expect(expectedPageTitle).to.equal("Add person 1 - Test Custom Page Titles");

      await $(await ListCollectorAddPage.firstName()).setValue("Marcus");
      await $(await ListCollectorAddPage.lastName()).setValue("Twin");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      expectedPageTitle = browser.getTitle();
      await expect(expectedPageTitle).to.equal("Add person 2 - Test Custom Page Titles");
    });

    it("When I navigate to relationship collector pages, Then I should see the custom page titles", async ()=> {
      await $(await ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Olivia");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.no()).click();
      await $(await ListCollectorPage.submit()).click();
      let expectedPageTitle = browser.getTitle();
      await expect(expectedPageTitle).to.equal("How Person 1 is related to Person 2 - Test Custom Page Titles");

      await $(await RelationshipsPage.husbandOrWife()).click();
      await $(await RelationshipsPage.submit()).click();
      expectedPageTitle = browser.getTitle();
      await expect(expectedPageTitle).to.equal("How Person 1 is related to Person 3 - Test Custom Page Titles");

      await $(await RelationshipsPage.sonOrDaughter()).click();
      await $(await RelationshipsPage.submit()).click();
      expectedPageTitle = browser.getTitle();
      await expect(expectedPageTitle).to.equal("How Person 2 is related to Person 3 - Test Custom Page Titles");

      await $(await RelationshipsPage.sonOrDaughter()).click();
      await $(await RelationshipsPage.submit()).click();
      expectedPageTitle = browser.getTitle();
      await expect(expectedPageTitle).to.equal("Custom section summary page title - Test Custom Page Titles");
    });

    it("When I navigate to list edit and remove pages Then I should see the custom page titles", async ()=> {
      await $(await ListCollectorPage.listEditLink(1)).click();
      let expectedPageTitle = browser.getTitle();
      await expect(expectedPageTitle).to.equal("Edit person 1 - Test Custom Page Titles");
      await $(await ListCollectorEditPage.previous()).click();
      await $(await ListCollectorPage.listRemoveLink(1)).click();
      expectedPageTitle = browser.getTitle();
      await expect(expectedPageTitle).to.equal("Remove person 1 - Test Custom Page Titles");
    });

    it("When I navigate to a repeating section which has custom page title, Then all page titles in the section should have the correct prefix", async ()=> {
      browser.url(HubPage.url());
      await $(await HubPage.submit()).click();
      await expect(browser.getTitle()).to.equal("Individual interstitial: Person 1 - Test Custom Page Titles");
      await $(await IndividualInterstitialPage.submit()).click();
      await expect(browser.getTitle()).to.equal("Proxy question: Person 1 - Test Custom Page Titles");
      await $(await ProxyPage.submit()).click();
      await expect(browser.getTitle()).to.equal("What is your date of birth?: Person 1 - Test Custom Page Titles");
      await $(await DateOfBirthPage.submit()).click();
      await expect(browser.getTitle()).to.equal("Summary: Person 1 - Test Custom Page Titles");
    });
  });
});
