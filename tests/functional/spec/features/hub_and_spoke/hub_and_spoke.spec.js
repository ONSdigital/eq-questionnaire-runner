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
import { click } from "../../../helpers";
describe("Feature: Hub and Spoke", () => {
  const hubAndSpokeSchema = "test_hub_and_spoke.json";

  describe("Given I am completing the test_hub_context schema,", () => {
    beforeEach("load the survey", async () => {
      await browser.openQuestionnaire(hubAndSpokeSchema);
    });

    it("When a user first views the Hub, The Hub should be in a continue state", async () => {
      await expect(await $(HubPage.submit()).getText()).toBe("Continue");
      await expect(await $(HubPage.heading()).getText()).toBe("Choose another section to complete");
      await expect(await $(HubPage.summaryRowState("employment-section")).getText()).toBe("Not started");
      await expect(await $(HubPage.summaryRowState("accommodation-section")).getText()).toBe("Not started");
      await expect(await $(HubPage.summaryRowState("household-section")).getText()).toBe("Not started");
    });

    it("When a user views the Hub, any section with show_on_hub set to true should appear", async () => {
      await expect(await $(HubPage.summaryItems()).getText()).toContain("Employment");
      await expect(await $(HubPage.summaryItems()).getText()).toContain("Accommodation");
      await expect(await $(HubPage.summaryItems()).getText()).toContain("Household residents");
    });

    it("When a user views the Hub, any section with show_on_hub set to false should not appear", async () => {
      await expect(await $(HubPage.summaryItems()).getText()).not.toBe("Relationships");
    });

    it("When the user click the 'Save and sign out' button then they should be redirected to the correct log out url", async () => {
      await $(HubPage.saveSignOut()).click();

      const expectedUrl = await browser.getUrl();

      await expect(expectedUrl).toContain("/signed-out");
    });

    it("When a user views the Hub, Then the page title should be Choose another section to complete", async () => {
      const pageTitle = await browser.getTitle();
      await expect(pageTitle).toBe("Choose another section to complete - Hub & Spoke");
    });
  });

  describe("Given a user has not started a section", () => {
    beforeEach("Open survey", async () => {
      await browser.openQuestionnaire(hubAndSpokeSchema);
      await expect(await $(HubPage.summaryRowState("employment-section")).getText()).toBe("Not started");
      await expect(await $(HubPage.summaryRowState("accommodation-section")).getText()).toBe("Not started");
      await expect(await $(HubPage.summaryRowState("household-section")).getText()).toBe("Not started");
    });

    it("When the user starts a section, Then the first question in the section should be displayed", async () => {
      await click(HubPage.submit());
      const expectedUrl = await browser.getUrl();
      await expect(expectedUrl).toContain(EmploymentStatusBlockPage.url());
    });

    it("When the user starts a section and clicks the Previous link on the first question, Then they should be taken back to the Hub", async () => {
      await click(HubPage.submit());
      await $(EmploymentStatusBlockPage.previous()).click();
      const expectedUrl = await browser.getUrl();
      await expect(expectedUrl).toContain(HubPage.url());
    });
  });

  describe("Given a user has started a section", () => {
    before("Start section", async () => {
      await browser.openQuestionnaire(hubAndSpokeSchema);
      await $(HubPage.summaryRowLink("employment-section")).click();
      await $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await click(EmploymentStatusBlockPage.submit());
    });

    it("When the user returns to the Hub, Then the Hub should be in a continue state", async () => {
      await browser.url(HubPage.url());
      await expect(await $(HubPage.submit()).getText()).toBe("Continue");
      await expect(await $(HubPage.heading()).getText()).toBe("Choose another section to complete");
    });

    it("When the user returns to the Hub, Then the section should be marked as 'Partially completed'", async () => {
      await browser.url(HubPage.url());
      await expect(await $(HubPage.summaryRowState("employment-section")).getText()).toBe("Partially completed");
    });

    it("When the user returns to the Hub and restarts the same section, Then they should be redirected to the first incomplete block", async () => {
      await browser.url(HubPage.url());
      await $(HubPage.summaryRowLink("employment-section")).click();
      const expectedUrl = await browser.getUrl();
      await expect(expectedUrl).toContain(EmploymentTypeBlockPage.url());
    });
  });

  describe("Given a user has completed a section", () => {
    beforeEach("Complete section", async () => {
      await browser.openQuestionnaire(hubAndSpokeSchema);
      await $(HubPage.summaryRowLink("employment-section")).click();
      await $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await click(EmploymentStatusBlockPage.submit());
      await $(EmploymentTypeBlockPage.studying()).click();
    });

    it("When the user clicks the 'Continue' button, it should return them to the hub", async () => {
      await click(EmploymentTypeBlockPage.submit());
      const expectedUrl = await browser.getUrl();
      await expect(expectedUrl).toContain(HubPage.url());
    });

    it("When the user returns to the Hub, Then the Hub should be in a continue state", async () => {
      await click(EmploymentTypeBlockPage.submit());
      await expect(await $(HubPage.submit()).getText()).toBe("Continue");
      await expect(await $(HubPage.heading()).getText()).toBe("Choose another section to complete");
    });

    it("When the user returns to the Hub, Then the section should be marked as 'Completed'", async () => {
      await click(EmploymentTypeBlockPage.submit());
      await expect(await $(HubPage.summaryRowState("employment-section")).getText()).toBe("Completed");
    });

    it("When the user returns to the Hub and clicks the 'View answers' link on the Hub, if this no summary they are returned to the first block", async () => {
      await click(EmploymentTypeBlockPage.submit());
      await $(HubPage.summaryRowLink("employment-section")).click();
      const expectedUrl = await browser.getUrl();
      await expect(expectedUrl).toContain(EmploymentStatusBlockPage.url());
    });

    it("When the user returns to the Hub and continues, Then they should progress to the next section", async () => {
      await click(EmploymentTypeBlockPage.submit());
      await expect(browser).toHaveUrlContaining(HubPage.url());
      await click(HubPage.submit());
      const expectedUrl = await browser.getUrl();
      await expect(expectedUrl).toContain(ProxyPage.url());
    });
  });

  describe("Given a user has completed a section and is on the Hub page", () => {
    beforeEach("Complete section", async () => {
      await browser.openQuestionnaire(hubAndSpokeSchema);
      await $(HubPage.summaryRowLink("employment-section")).click();
      await $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
      await click(EmploymentStatusBlockPage.submit());

      await expect(await $(HubPage.summaryRowState("employment-section")).getText()).toBe("Completed");
    });

    it("When the user clicks the 'View answers' link and incompletes the section, Then they the should be taken to the next incomplete question on 'Continue", async () => {
      await $(HubPage.summaryRowLink("employment-section")).click();
      await expect(browser).toHaveUrlContaining(EmploymentStatusBlockPage.url());
      await $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await click(EmploymentStatusBlockPage.submit());
      const expectedUrl = await browser.getUrl();
      await expect(expectedUrl).toContain(EmploymentTypeBlockPage.url());
    });

    it("When the user clicks the 'View answers' link and incompletes the section and returns to the hub, Then the section should be marked as 'Partially completed'", async () => {
      await $(HubPage.summaryRowLink("employment-section")).click();
      await expect(browser).toHaveUrlContaining(EmploymentStatusBlockPage.url());
      await $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await click(EmploymentStatusBlockPage.submit());
      await browser.url(HubPage.url());
      const expectedUrl = await browser.getUrl();
      await expect(expectedUrl).toContain(HubPage.url());
      await expect(await $(HubPage.summaryRowState("employment-section")).getText()).toBe("Partially completed");
    });
  });

  describe("Given a user has completed all sections", () => {
    beforeEach("Complete all sections", async () => {
      await browser.openQuestionnaire(hubAndSpokeSchema);
      await $(HubPage.summaryRowLink("employment-section")).click();
      await $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await click(EmploymentStatusBlockPage.submit());
      await $(EmploymentTypeBlockPage.studying()).click();
      await click(EmploymentTypeBlockPage.submit());
      await click(HubPage.submit());
      await $(ProxyPage.yes()).click();
      await click(ProxyPage.submit());
      await click(AccomodationDetailsSummaryBlockPage.submit());
      await click(HubPage.submit());
      await $(DoesAnyoneLiveHere.no()).click();
      await click(DoesAnyoneLiveHere.submit());
      await click(HouseholdSummary.submit());
      await click(HubPage.submit());
      await $(AnyoneRelated.yes()).click();
      await click(AnyoneRelated.submit());
      await click(RelationshipsSummary.submit());
    });

    it("It should return them to the hub", async () => {
      const expectedUrl = await browser.getUrl();
      await expect(expectedUrl).toContain(HubPage.url());
    });

    it("When the user returns to the Hub, Then the Hub should be in a completed state", async () => {
      await expect(await $(HubPage.submit()).getText()).toBe("Submit survey");
      await expect(await $(HubPage.heading()).getText()).toBe("Submit survey");
    });

    it("When the user submits, it should show the thankyou page", async () => {
      await click(HubPage.submit());
      const expectedUrl = await browser.getUrl();
      await expect(expectedUrl).toContain("thank-you");
    });
  });

  describe("Given a user opens a schema with required sections", () => {
    beforeEach("Load survey", async () => {
      await browser.openQuestionnaire("test_hub_complete_sections.json");
    });

    it("The hub should not show first of all", async () => {
      await expect(browser).toHaveUrlContaining(EmploymentStatusBlockPage.url());
    });

    it("The hub should only display when required sections are complete", async () => {
      await $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await click(EmploymentStatusBlockPage.submit());
      await $(EmploymentTypeBlockPage.studying()).click();
      await click(EmploymentTypeBlockPage.submit());
      await expect(browser).toHaveUrlContaining(HubPage.url());
    });
  });

  describe("Given a section is complete and the user has been returned to a section summary by clicking the 'View answers' link ", () => {
    beforeEach("Complete section", async () => {
      await browser.openQuestionnaire(hubAndSpokeSchema);
      await $(HubPage.summaryRowLink("household-section")).click();
      await $(DoesAnyoneLiveHere.no()).click();
      await click(DoesAnyoneLiveHere.submit());
      await click(HouseholdSummary.submit());
    });

    it("When there are no changes, continue returns directly to the hub", async () => {
      await $(HubPage.summaryRowLink("household-section")).click();
      await click(HouseholdSummary.submit());
      const expectedUrl = await browser.getUrl();
      await expect(expectedUrl).toContain(HubPage.url());
    });

    it("When there are changes, which would set the section to in_progress it routes accordingly", async () => {
      await $(HubPage.summaryRowLink("household-section")).click();
      await $(HouseholdSummary.doesAnyoneLiveHereAnswerEdit()).click();
      await $(DoesAnyoneLiveHere.yes()).click();
      await click(DoesAnyoneLiveHere.submit());
      await click(HouseholdSummary.submit());
      const expectedUrl = await browser.getUrl();
      await expect(expectedUrl).toContain(HowManyPeopleLiveHere.url());
    });
  });
});
