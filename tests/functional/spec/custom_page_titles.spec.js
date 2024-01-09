import DateOfBirthPage from "../generated_pages/custom_page_titles/date-of-birth.page.js";
import HubPage from "../base_pages/hub.page.js";
import IndividualInterstitialPage from "../generated_pages/custom_page_titles/individual-interstitial.page.js";
import ListCollectorAddPage from "../generated_pages/custom_page_titles/list-collector-add.page.js";
import ListCollectorEditPage from "../generated_pages/custom_page_titles/list-collector-edit.page.js";
import ListCollectorPage from "../generated_pages/custom_page_titles/list-collector.page.js";
import ProxyPage from "../generated_pages/custom_page_titles/proxy.page.js";
import RelationshipsPage from "../generated_pages/custom_page_titles/relationships.page.js";
import { click } from "../helpers";

describe("Feature: Custom Page Titles", () => {
  const schema = "test_custom_page_titles.json";

  describe("Given I am completing the test_custom_page_titles survey,", () => {
    before("load the survey", async () => {
      await browser.openQuestionnaire(schema);
    });

    it("When I navigate to the list collector page, Then I should see the custom page title", async () => {
      await click(HubPage.submit());
      const expectedPageTitle = await browser.getTitle();
      await expect(expectedPageTitle).toBe("Custom page title - Test Custom Page Titles");
    });

    it("When I navigate to the add person page, Then I should see the custom page title", async () => {
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      let expectedPageTitle = await browser.getTitle();
      await expect(expectedPageTitle).toBe("Add person 1 - Test Custom Page Titles");

      await $(ListCollectorAddPage.firstName()).setValue("Marcus");
      await $(ListCollectorAddPage.lastName()).setValue("Twin");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      expectedPageTitle = await browser.getTitle();
      await expect(expectedPageTitle).toBe("Add person 2 - Test Custom Page Titles");
    });

    it("When I navigate to relationship collector pages, Then I should see the custom page titles", async () => {
      await $(ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Olivia");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      let expectedPageTitle = await browser.getTitle();
      await expect(await expectedPageTitle).toBe("How Person 1 is related to Person 2 - Test Custom Page Titles");

      await $(RelationshipsPage.husbandOrWife()).click();
      await click(RelationshipsPage.submit());
      expectedPageTitle = await browser.getTitle();
      await expect(expectedPageTitle).toBe("How Person 1 is related to Person 3 - Test Custom Page Titles");

      await $(RelationshipsPage.sonOrDaughter()).click();
      await click(RelationshipsPage.submit());
      expectedPageTitle = await browser.getTitle();
      await expect(expectedPageTitle).toBe("How Person 2 is related to Person 3 - Test Custom Page Titles");

      await $(RelationshipsPage.sonOrDaughter()).click();
      await click(RelationshipsPage.submit());
      expectedPageTitle = await browser.getTitle();
      await expect(expectedPageTitle).toBe("Custom section summary page title - Test Custom Page Titles");
    });

    it("When I navigate to list edit and remove pages Then I should see the custom page titles", async () => {
      await $(ListCollectorPage.listEditLink(1)).click();
      let expectedPageTitle = await browser.getTitle();
      await expect(expectedPageTitle).toBe("Edit person 1 - Test Custom Page Titles");
      await $(ListCollectorEditPage.previous()).click();
      await $(ListCollectorPage.listRemoveLink(1)).click();
      expectedPageTitle = await browser.getTitle();
      await expect(expectedPageTitle).toBe("Remove person 1 - Test Custom Page Titles");
    });

    it("When I navigate to a repeating section which has custom page title, Then all page titles in the section should have the correct prefix", async () => {
      await browser.url(HubPage.url());
      await click(HubPage.submit());
      await expect(await browser.getTitle()).toBe("Individual interstitial: Person 1 - Test Custom Page Titles");
      await click(IndividualInterstitialPage.submit());
      await expect(await browser.getTitle()).toBe("Proxy question: Person 1 - Test Custom Page Titles");
      await click(ProxyPage.submit());
      await expect(await browser.getTitle()).toBe("What is your date of birth?: Person 1 - Test Custom Page Titles");
      await click(DateOfBirthPage.submit());
      await expect(await browser.getTitle()).toBe("Summary: Person 1 - Test Custom Page Titles");
    });
  });
});
