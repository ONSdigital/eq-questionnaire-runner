import AccomodationDetailsSummaryBlockPage from "../../../generated_pages/hub_and_spoke/accommodation-section-summary.page.js";
import AnyoneRelated from "../../../generated_pages/hub_and_spoke/anyone-related.page.js";
import DoesAnyoneLiveHere from "../../../generated_pages/hub_and_spoke/does-anyone-live-here.page.js";
import EmploymentStatusBlockPage from "../../../generated_pages/hub_and_spoke/employment-status.page.js";
import EmploymentTypeBlockPage from "../../../generated_pages/hub_and_spoke/employment-type.page.js";
import HouseholdSummary from "../../../generated_pages/hub_and_spoke/household-section-summary.page.js";
import HowManyPeopleLiveHere from "../../../generated_pages/hub_and_spoke/how-many-people-live-here.page.js";
import HubPage from "../../../base_pages/hub.page.js";
import ProxyPage from "../../../generated_pages/hub_and_spoke/proxy.page.js";
import RelationshipsSummary from "../../../generated_pages/hub_and_spoke/relationships-section-summary.page.js";

describe("Feature: Hub and Spoke", () => {
  const hubAndSpokeSchema = "test_hub_and_spoke.json";

  describe("Given I am completing the test_hub_context schema,", () => {
    beforeEach("load the survey", async ()=> {
      await browser.openQuestionnaire(hubAndSpokeSchema);
    });

    it("When a user first views the Hub, The Hub should be in a continue state", async ()=> {
      await expect(await $(await HubPage.submit()).getText()).to.contain("Continue");
      await expect(await $(await HubPage.heading()).getText()).to.contain("Choose another section to complete");
      await expect(await $(await HubPage.summaryRowState("employment-section")).getText()).to.contain("Not started");
      await expect(await $(await HubPage.summaryRowState("accommodation-section")).getText()).to.contain("Not started");
      await expect(await $(await HubPage.summaryRowState("household-section")).getText()).to.contain("Not started");
    });

    it("When a user views the Hub, any section with show_on_hub set to true should appear", async ()=> {
      await expect(await $(await HubPage.summaryItems()).getText()).to.contain("Employment");
      await expect(await $(await HubPage.summaryItems()).getText()).to.contain("Accommodation");
      await expect(await $(await HubPage.summaryItems()).getText()).to.contain("Household residents");
    });

    it("When a user views the Hub, any section with show_on_hub set to false should not appear", async ()=> {
      await expect(await $(await HubPage.summaryItems()).getText()).not.to.contain("Relationships");
    });

    it("When the user click the 'Save and sign out' button then they should be redirected to the correct log out url", async ()=> {
      await $(await HubPage.saveSignOut()).click();

      const expectedUrl = browser.getUrl();

      await expect(expectedUrl).to.contain("/surveys/todo");
    });

    it("When a user views the Hub, Then the page title should be Choose another section to complete", async ()=> {
      const pageTitle = browser.getTitle();
      await expect(pageTitle).to.equal("Choose another section to complete - Hub & Spoke");
    });
  });

  describe("Given a user has not started a section", () => {
    beforeEach("Open survey", async ()=> {
      await browser.openQuestionnaire(hubAndSpokeSchema);
      await expect(await $(await HubPage.summaryRowState("employment-section")).getText()).to.contain("Not started");
      await expect(await $(await HubPage.summaryRowState("accommodation-section")).getText()).to.contain("Not started");
      await expect(await $(await HubPage.summaryRowState("household-section")).getText()).to.contain("Not started");
    });

    it("When the user starts a section, Then the first question in the section should be displayed", async ()=> {
      await $(await HubPage.submit()).click();
      const expectedUrl = browser.getUrl();
      await expect(expectedUrl).to.contain(EmploymentStatusBlockPage.url());
    });

    it("When the user starts a section and clicks the Previous link on the first question, Then they should be taken back to the Hub", async ()=> {
      await $(await HubPage.submit()).click();
      await $(await EmploymentStatusBlockPage.previous()).click();
      const expectedUrl = browser.getUrl();
      await expect(expectedUrl).to.contain(HubPage.url());
    });
  });

  describe("Given a user has started a section", () => {
    before("Start section", async ()=> {
      await browser.openQuestionnaire(hubAndSpokeSchema);
      await $(await HubPage.summaryRowLink("employment-section")).click();
      await $(await EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await $(await EmploymentStatusBlockPage.submit()).click();
    });

    it("When the user returns to the Hub, Then the Hub should be in a continue state", async ()=> {
      browser.url(HubPage.url());
      await expect(await $(await HubPage.submit()).getText()).to.contain("Continue");
      await expect(await $(await HubPage.heading()).getText()).to.contain("Choose another section to complete");
    });

    it("When the user returns to the Hub, Then the section should be marked as 'Partially completed'", async ()=> {
      browser.url(HubPage.url());
      await expect(await $(await HubPage.summaryRowState("employment-section")).getText()).to.contain("Partially completed");
    });

    it("When the user returns to the Hub and restarts the same section, Then they should be redirected to the first incomplete block", async ()=> {
      browser.url(HubPage.url());
      await $(await HubPage.summaryRowLink("employment-section")).click();
      const expectedUrl = browser.getUrl();
      await expect(expectedUrl).to.contain(EmploymentTypeBlockPage.url());
    });
  });

  describe("Given a user has completed a section", () => {
    beforeEach("Complete section", async ()=> {
      await browser.openQuestionnaire(hubAndSpokeSchema);
      await $(await HubPage.summaryRowLink("employment-section")).click();
      await $(await EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await $(await EmploymentStatusBlockPage.submit()).click();
      await $(await EmploymentTypeBlockPage.studying()).click();
    });

    it("When the user clicks the 'Continue' button, it should return them to the hub", async ()=> {
      await $(await EmploymentTypeBlockPage.submit()).click();
      const expectedUrl = browser.getUrl();
      await expect(expectedUrl).to.contain(HubPage.url());
    });

    it("When the user returns to the Hub, Then the Hub should be in a continue state", async ()=> {
      await $(await EmploymentTypeBlockPage.submit()).click();
      await expect(await $(await HubPage.submit()).getText()).to.contain("Continue");
      await expect(await $(await HubPage.heading()).getText()).to.contain("Choose another section to complete");
    });

    it("When the user returns to the Hub, Then the section should be marked as 'Completed'", async ()=> {
      await $(await EmploymentTypeBlockPage.submit()).click();
      await expect(await $(await HubPage.summaryRowState("employment-section")).getText()).to.contain("Completed");
    });

    it("When the user returns to the Hub and clicks the 'View answers' link on the Hub, if this no summary they are returned to the first block", async ()=> {
      await $(await EmploymentTypeBlockPage.submit()).click();
      await $(await HubPage.summaryRowLink("employment-section")).click();
      const expectedUrl = browser.getUrl();
      await expect(expectedUrl).to.contain(EmploymentStatusBlockPage.url());
    });

    it("When the user returns to the Hub and continues, Then they should progress to the next section", async ()=> {
      await $(await EmploymentTypeBlockPage.submit()).click();
      await expect(browser.getUrl()).to.contain(HubPage.url());
      await $(await HubPage.submit()).click();
      const expectedUrl = browser.getUrl();
      await expect(expectedUrl).to.contain(ProxyPage.url());
    });
  });

  describe("Given a user has completed a section and is on the Hub page", () => {
    beforeEach("Complete section", async ()=> {
      await browser.openQuestionnaire(hubAndSpokeSchema);
      await $(await HubPage.summaryRowLink("employment-section")).click();
      await $(await EmploymentStatusBlockPage.workingAsAnEmployee()).click();
      await $(await EmploymentStatusBlockPage.submit()).click();

      await expect(await $(await HubPage.summaryRowState("employment-section")).getText()).to.contain("Completed");
    });

    it("When the user clicks the 'View answers' link and incompletes the section, Then they the should be taken to the next incomplete question on 'Continue", async ()=> {
      await $(await HubPage.summaryRowLink("employment-section")).click();
      await expect(browser.getUrl()).to.contain(EmploymentStatusBlockPage.url());
      await $(await EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await $(await EmploymentStatusBlockPage.submit()).click();
      const expectedUrl = browser.getUrl();
      await expect(expectedUrl).to.contain(EmploymentTypeBlockPage.url());
    });

    it("When the user clicks the 'View answers' link and incompletes the section and returns to the hub, Then the section should be marked as 'Partially completed'", async ()=> {
      await $(await HubPage.summaryRowLink("employment-section")).click();
      await expect(browser.getUrl()).to.contain(EmploymentStatusBlockPage.url());
      await $(await EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await $(await EmploymentStatusBlockPage.submit()).click();
      browser.url(HubPage.url());
      const expectedUrl = browser.getUrl();
      await expect(expectedUrl).to.contain(HubPage.url());
      await expect(await $(await HubPage.summaryRowState("employment-section")).getText()).to.contain("Partially completed");
    });
  });

  describe("Given a user has completed all sections", () => {
    beforeEach("Complete all sections", async ()=> {
      await browser.openQuestionnaire(hubAndSpokeSchema);
      await $(await HubPage.summaryRowLink("employment-section")).click();
      await $(await EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await $(await EmploymentStatusBlockPage.submit()).click();
      await $(await EmploymentTypeBlockPage.studying()).click();
      await $(await EmploymentTypeBlockPage.submit()).click();
      await $(await HubPage.submit()).click();
      await $(await ProxyPage.yes()).click();
      await $(await ProxyPage.submit()).click();
      await $(await AccomodationDetailsSummaryBlockPage.submit()).click();
      await $(await HubPage.submit()).click();
      await $(await DoesAnyoneLiveHere.no()).click();
      await $(await DoesAnyoneLiveHere.submit()).click();
      await $(await HouseholdSummary.submit()).click();
      await $(await HubPage.submit()).click();
      await $(await AnyoneRelated.yes()).click();
      await $(await AnyoneRelated.submit()).click();
      await $(await RelationshipsSummary.submit()).click();
    });

    it("It should return them to the hub", async ()=> {
      const expectedUrl = browser.getUrl();
      await expect(expectedUrl).to.contain(HubPage.url());
    });

    it("When the user returns to the Hub, Then the Hub should be in a completed state", async ()=> {
      await expect(await $(await HubPage.submit()).getText()).to.contain("Submit survey");
      await expect(await $(await HubPage.heading()).getText()).to.contain("Submit survey");
    });

    it("When the user submits, it should show the thankyou page", async ()=> {
      await $(await HubPage.submit()).click();
      const expectedUrl = browser.getUrl();
      await expect(expectedUrl).to.contain("thank-you");
    });
  });

  describe("Given a user opens a schema with required sections", () => {
    beforeEach("Load survey", async ()=> {
      await browser.openQuestionnaire("test_hub_complete_sections.json");
    });

    it("The hub should not show first of all", async ()=> {
      await expect(browser.getUrl()).to.contain(EmploymentStatusBlockPage.url());
    });

    it("The hub should only display when required sections are complete", async ()=> {
      await $(await EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await $(await EmploymentStatusBlockPage.submit()).click();
      await $(await EmploymentTypeBlockPage.studying()).click();
      await $(await EmploymentTypeBlockPage.submit()).click();
      await expect(browser.getUrl()).to.contain(HubPage.url());
    });
  });

  describe("Given a section is complete and the user has been returned to a section summary by clicking the 'View answers' link ", () => {
    beforeEach("Complete section", async ()=> {
      await browser.openQuestionnaire(hubAndSpokeSchema);
      await $(await HubPage.summaryRowLink("household-section")).click();
      await $(await DoesAnyoneLiveHere.no()).click();
      await $(await DoesAnyoneLiveHere.submit()).click();
      await $(await HouseholdSummary.submit()).click();
    });

    it("When there are no changes, continue returns directly to the hub", async ()=> {
      await $(await HubPage.summaryRowLink("household-section")).click();
      await $(await HouseholdSummary.submit()).click();
      const expectedUrl = browser.getUrl();
      await expect(expectedUrl).to.contain(HubPage.url());
    });

    it("When there are changes, which would set the section to in_progress it routes accordingly", async ()=> {
      await $(await HubPage.summaryRowLink("household-section")).click();
      await $(await HouseholdSummary.doesAnyoneLiveHereAnswerEdit()).click();
      await $(await DoesAnyoneLiveHere.yes()).click();
      await $(await DoesAnyoneLiveHere.submit()).click();
      await $(await HouseholdSummary.submit()).click();
      const expectedUrl = browser.getUrl();
      await expect(expectedUrl).to.contain(HowManyPeopleLiveHere.url());
    });
  });
});
