import HubPage from "../base_pages/hub.page.js";
import IndividualInterstitialPage from "../generated_pages/custom_page_titles/individual-interstitial.page.js";
import ListCollectorAddPage from "../generated_pages/custom_page_titles/list-collector-add.page.js";
import ListCollectorEditPage from "../generated_pages/custom_page_titles/list-collector-edit.page.js";
import ListCollectorPage from "../generated_pages/custom_page_titles/list-collector.page.js";
import RelationshipsPage from "../generated_pages/custom_page_titles/relationships.page.js";
import SectionSummaryPage from "../generated_pages/custom_page_titles/section-summary.page.js";

describe("Feature: Custom Page Titles", () => {
  const schema = "test_custom_page_titles.json";

  describe("Given I am completing the test_custom_page_titles survey,", () => {
    beforeEach("load the survey", () => {
      browser.openQuestionnaire(schema);
    });

    it("When I navigate to the list collector page, Then I should see the custom page title", () => {
      $(HubPage.submit()).click();
      const expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Custom page title");
    });

    it("When I navigate to the add person pages, Then I should see the custom page titles", () => {
      $(HubPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      let expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Add person 1");

      $(ListCollectorAddPage.firstName()).setValue("Marcus");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Add person 2");
    });

    it("When I navigate to relationship collector pages, Then I should see the custom page titles", () => {
      $(HubPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Marcus");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
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
      expect(expectedPageTitle).to.equal("How Person 1 is related to Person 2");

      $(RelationshipsPage.husbandOrWife()).click();
      $(RelationshipsPage.submit()).click();
      expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("How Person 1 is related to Person 3");

      $(RelationshipsPage.sonOrDaughter()).click();
      $(RelationshipsPage.submit()).click();
      expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("How Person 2 is related to Person 3");

      $(RelationshipsPage.submit()).click();
      $(RelationshipsPage.sonOrDaughter()).click();
      $(RelationshipsPage.submit()).click();
      expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Custom section summary page title");
    });

    it("When I navigate to individual section pages, Then I should see the custom page titles", () => {
      $(HubPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Marcus");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
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
      $(RelationshipsPage.husbandOrWife()).click();
      $(RelationshipsPage.submit()).click();
      $(RelationshipsPage.sonOrDaughter()).click();
      $(RelationshipsPage.submit()).click();
      $(RelationshipsPage.submit()).click();
      $(RelationshipsPage.sonOrDaughter()).click();
      $(RelationshipsPage.submit()).click();
      $(SectionSummaryPage.submit()).click();
      $(HubPage.submit()).click();
      let expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Person 1 individual interstitial");

      $(IndividualInterstitialPage.submit()).click();
      expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Person 1 proxy question");
    });

    it("When I navigate to list edit and remove pages Then I should see the custom page titles", () => {
      $(HubPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Marcus");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.listEditLink(1)).click();
      let expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Edit person 1");

      $(ListCollectorEditPage.previous()).click();
      $(ListCollectorPage.listRemoveLink(1)).click();
      expectedPageTitle = browser.getTitle();
      expect(expectedPageTitle).to.equal("Remove person 1");
    });
  });
});
