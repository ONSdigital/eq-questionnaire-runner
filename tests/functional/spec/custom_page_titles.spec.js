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
    before("load the survey", () => {
      browser.openQuestionnaire(schema);
    });

    it("When I navigate to the list collector page, Then I should see the custom page title", () => {
      $(HubPage.submit()).click();
      const expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Custom page title - Test Custom Page Titles");
    });

    it("When I navigate to the add person page, Then I should see the custom page title", () => {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      let expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Add person 1 - Test Custom Page Titles");

      $(ListCollectorAddPage.firstName()).setValue("Marcus");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Add person 2 - Test Custom Page Titles");
    });

    it("When I navigate to relationship collector pages, Then I should see the custom page titles", () => {
      $(ListCollectorAddPage.firstName()).setValue("Samuel");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Olivia");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      let expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("How Person 1 is related to Person 2 - Test Custom Page Titles");

      $(RelationshipsPage.husbandOrWife()).click();
      $(RelationshipsPage.submit()).click();
      expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("How Person 1 is related to Person 3 - Test Custom Page Titles");

      $(RelationshipsPage.sonOrDaughter()).click();
      $(RelationshipsPage.submit()).click();
      expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("How Person 2 is related to Person 3 - Test Custom Page Titles");

      $(RelationshipsPage.sonOrDaughter()).click();
      $(RelationshipsPage.submit()).click();
      expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Custom section summary page title - Test Custom Page Titles");
    });

    it("When I navigate to list edit and remove pages Then I should see the custom page titles", () => {
      $(ListCollectorPage.listEditLink(1)).click();
      let expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Edit person 1 - Test Custom Page Titles");
      $(ListCollectorEditPage.previous()).click();
      $(ListCollectorPage.listRemoveLink(1)).click();
      expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Remove person 1 - Test Custom Page Titles");
    });

    it("When I navigate to a repeating section which has custom page title, Then all page titles in the section should have the correct prefix", () => {
      browser.url(HubPage.url());
      $(HubPage.submit()).click();
      expect(browser.getTitle()).to.equal("Individual interstitial: Person 1 - Test Custom Page Titles");
      $(IndividualInterstitialPage.submit()).click();
      expect(browser.getTitle()).to.equal("Proxy question: Person 1 - Test Custom Page Titles");
      $(ProxyPage.submit()).click();
      expect(browser.getTitle()).to.equal("What is your date of birth?: Person 1 - Test Custom Page Titles");
      $(DateOfBirthPage.submit()).click();
      expect(browser.getTitle()).to.equal("Summary: Person 1 - Test Custom Page Titles");
    });
  });
});
