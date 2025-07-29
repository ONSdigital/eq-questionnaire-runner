import AccomodationDetailsSummaryBlockPage from "../../generated_pages/hub_and_spoke/accommodation-section-summary.page.js";
import AnyoneRelated from "../../generated_pages/hub_and_spoke/anyone-related.page.js";
import DoesAnyoneLiveHere from "../../generated_pages/hub_and_spoke/does-anyone-live-here.page.js";
import EmploymentStatusBlockPage from "../../generated_pages/hub_and_spoke/employment-status.page.js";
import EmploymentTypeBlockPage from "../../generated_pages/hub_and_spoke/employment-type.page.js";
import HouseholdSummary from "../../generated_pages/hub_and_spoke/household-section-summary.page.js";
import HowManyPeopleLiveHere from "../../generated_pages/hub_and_spoke/how-many-people-live-here.page.js";
import HubPage from "../../base_pages/hub.page.js";
import ProxyPage from "../../generated_pages/hub_and_spoke/proxy.page.js";
import RelationshipsSummary from "../../generated_pages/hub_and_spoke/relationships-section-summary.page.js";
import ListCollectorSectionSummaryPage from "../../generated_pages/hub_section_required_with_repeat/list-collector-section-summary.page.js";
import ProxyRepeatPage from "../../generated_pages/hub_section_required_with_repeat/proxy.page.js";
import { click, verifyUrlContains } from "../../helpers";
import DateOfBirthPage from "../../generated_pages/hub_section_required_with_repeat/date-of-birth.page";
import PrimaryPersonListCollectorPage from "../../generated_pages/hub_section_required_with_repeat/primary-person-list-collector.page";
import PrimaryPersonListCollectorAddPage from "../../generated_pages/hub_section_required_with_repeat/primary-person-list-collector-add.page";
import ListCollectorPage from "../../generated_pages/hub_section_required_with_repeat/list-collector.page";
import ListCollectorAddPage from "../../generated_pages/hub_section_required_with_repeat/list-collector-add.page";
import RepeatingSummaryPage from "../../generated_pages/hub_section_required_with_repeat/personal-details-section-summary.page";

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

    it("When a user utilises a screen reader, The visually hidden text read aloud should be the state and name of each section in the hub", async () => {
      await expect(await $(HubPage.summaryRowLink("employment-section")).getHTML()).toContain("Start section: Employment");
      await expect(await $(HubPage.summaryRowLink("accommodation-section")).getHTML()).toContain("Start section: Accommodation");
      await expect(await $(HubPage.summaryRowLink("household-section")).getHTML()).toContain("Start section: Household residents");
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
      await verifyUrlContains("/signed-out");
    });

    it.skip("When a user views the Hub, Then the page title should be Choose another section to complete", async () => {
      // This test is skipped because the page title is not consistently ready in time during GitHub Actions runs, causing flakiness.
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
      await expect(await $(HubPage.summaryRowLink("employment-section")).getHTML()).toContain("Start section: Employment");
      await expect(await $(HubPage.summaryRowLink("accommodation-section")).getHTML()).toContain("Start section: Accommodation");
      await expect(await $(HubPage.summaryRowLink("household-section")).getHTML()).toContain("Start section: Household residents");
    });

    it("When the user starts a section, Then the first question in the section should be displayed", async () => {
      await click(HubPage.submit());
      await verifyUrlContains(EmploymentStatusBlockPage.url());
    });

    it("When the user starts a section and clicks the Previous link on the first question, Then they should be taken back to the Hub", async () => {
      await click(HubPage.submit());
      await $(EmploymentStatusBlockPage.previous()).click();
      await verifyUrlPathIs(HubPage.url());
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
      await expect(await $(HubPage.summaryRowLink("employment-section")).getHTML()).toContain("Continue with section: Employment");
    });

    it("When the user returns to the Hub and restarts the same section, Then they should be redirected to the first incomplete block", async () => {
      await browser.url(HubPage.url());
      await $(HubPage.summaryRowLink("employment-section")).click();
      await verifyUrlContains(EmploymentTypeBlockPage.url());
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
      await verifyUrlPathIs(HubPage.url());
    });

    it("When the user returns to the Hub, Then the Hub should be in a continue state", async () => {
      await click(EmploymentTypeBlockPage.submit());
      await expect(await $(HubPage.submit()).getText()).toBe("Continue");
      await expect(await $(HubPage.heading()).getText()).toBe("Choose another section to complete");
    });

    it("When the user returns to the Hub, Then the section should be marked as 'Completed'", async () => {
      await click(EmploymentTypeBlockPage.submit());
      await expect(await $(HubPage.summaryRowState("employment-section")).getText()).toBe("Completed");
      await expect(await $(HubPage.summaryRowLink("employment-section")).getHTML()).toContain("View answers: Employment");
    });

    it("When the user returns to the Hub and clicks the 'View answers' link on the Hub, if this no summary they are returned to the first block", async () => {
      await click(EmploymentTypeBlockPage.submit());
      await $(HubPage.summaryRowLink("employment-section")).click();
      await verifyUrlContains(EmploymentStatusBlockPage.url());
    });

    it("When the user returns to the Hub and continues, Then they should progress to the next section", async () => {
      await click(EmploymentTypeBlockPage.submit());
      await verifyUrlContains(HubPage.url());
      await click(HubPage.submit());
      await verifyUrlContains(ProxyPage.url());
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
      await verifyUrlContains(EmploymentStatusBlockPage.url());
      await $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await click(EmploymentStatusBlockPage.submit());
      await verifyUrlContains(EmploymentTypeBlockPage.url());
    });

    it("When the user clicks the 'View answers' link and incompletes the section and returns to the hub, Then the section should be marked as 'Partially completed'", async () => {
      await $(HubPage.summaryRowLink("employment-section")).click();
      await verifyUrlContains(EmploymentStatusBlockPage.url());
      await $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await click(EmploymentStatusBlockPage.submit());
      await browser.url(HubPage.url());
      await verifyUrlPathIs(HubPage.url());
      await expect(await $(HubPage.summaryRowState("employment-section")).getText()).toBe("Partially completed");
      await expect(await $(HubPage.summaryRowLink("employment-section")).getHTML()).toContain("Continue with section: Employment");
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
      await verifyUrlPathIs(HubPage.url());
    });

    it("When the user returns to the Hub, Then the Hub should be in a completed state", async () => {
      await expect(await $(HubPage.submit()).getText()).toBe("Submit survey");
      await expect(await $(HubPage.heading()).getText()).toBe("Submit survey");
    });

    it("When the user submits, it should show the thankyou page", async () => {
      await click(HubPage.submit());
      await verifyUrlContains("thank-you");
    });
  });

  describe("Given a user opens a schema with required sections", () => {
    beforeEach("Load survey", async () => {
      await browser.openQuestionnaire("test_hub_complete_sections.json");
    });

    it("The hub should not show first of all", async () => {
      await verifyUrlContains(EmploymentStatusBlockPage.url());
    });

    it("The hub should only display when required sections are complete", async () => {
      await $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      await click(EmploymentStatusBlockPage.submit());
      await $(EmploymentTypeBlockPage.studying()).click();
      await click(EmploymentTypeBlockPage.submit());
      await verifyUrlContains(HubPage.url());
    });
  });

  describe("Given a user opens a schema with hub required sections based on a repeating section", () => {
    beforeEach("Load survey", async () => {
      await browser.openQuestionnaire("test_hub_section_required_with_repeat.json");
    });

    it("When all the repeating sections are complete, Then the hub should be displayed", async () => {
      await $(PrimaryPersonListCollectorPage.yes()).click();
      await $(PrimaryPersonListCollectorPage.submit()).click();
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await click(PrimaryPersonListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      await $(ListCollectorPage.submit()).click();
      await $(ListCollectorAddPage.firstName()).setValue("John");
      await $(ListCollectorAddPage.lastName()).setValue("Doe");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();
      await click(ListCollectorSectionSummaryPage.submit());

      // Try to access the hub
      await browser.url(HubPage.url());

      // Redirected to the repeating sections to be completed
      await $(ProxyRepeatPage.yes()).click();
      await $(ProxyRepeatPage.submit()).click();
      await $(DateOfBirthPage.day()).setValue(12);
      await $(DateOfBirthPage.month()).setValue(4);
      await $(DateOfBirthPage.year()).setValue(2021);
      await click(DateOfBirthPage.submit());
      await $(RepeatingSummaryPage.submit()).click();
      await $(ProxyRepeatPage.yes()).click();
      await $(ProxyRepeatPage.submit()).click();
      await $(DateOfBirthPage.day()).setValue(1);
      await $(DateOfBirthPage.month()).setValue(1);
      await $(DateOfBirthPage.year()).setValue(2000);
      await $(RepeatingSummaryPage.submit()).click();
      await verifyUrlContains(HubPage.url());
    });

    it("When the repeating sections are incomplete, Then the hub should not be displayed", async () => {
      await $(PrimaryPersonListCollectorPage.yes()).click();
      await $(PrimaryPersonListCollectorPage.submit()).click();
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await click(PrimaryPersonListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();
      await click(ListCollectorSectionSummaryPage.submit());

      // Don't complete all the repeating questions
      await $(ProxyRepeatPage.yes()).click();
      await $(ProxyRepeatPage.submit()).click();

      await browser.url(HubPage.url());
      await verifyUrlContains("date-of-birth");
    });
  });

  describe("Given a section is complete and the user has been returned to a section summary by clicking the 'View answers' link ", () => {
    beforeEach("Complete section", async () => {
      await browser.openQuestionnaire(hubAndSpokeSchema);
      await $(HubPage.summaryRowLink("household-section")).click();
      await $(DoesAnyoneLiveHere.no()).click();
      await click(DoesAnyoneLiveHere.submit());
      await click(HouseholdSummary.submit());
      await expect(await $(HubPage.summaryRowLink("household-section")).getHTML()).toContain("View answers: Household residents");
    });

    it("When there are no changes, continue returns directly to the hub", async () => {
      await $(HubPage.summaryRowLink("household-section")).click();
      await click(HouseholdSummary.submit());
      await verifyUrlPathIs(HubPage.url());
      await expect(await $(HubPage.summaryRowLink("household-section")).getHTML()).toContain("View answers: Household residents");
    });

    it("When there are changes, which would set the section to in_progress it routes accordingly", async () => {
      await $(HubPage.summaryRowLink("household-section")).click();
      await $(HouseholdSummary.doesAnyoneLiveHereAnswerEdit()).click();
      await $(DoesAnyoneLiveHere.yes()).click();
      await click(DoesAnyoneLiveHere.submit());
      await click(HouseholdSummary.submit());
      await verifyUrlContains(HowManyPeopleLiveHere.url());
    });
  });
});

async function verifyUrlPathIs(expectedUrlPath) {
  // Hub and Spoke URLs are "/questionnaire/", so we need strict checking of the URL path
  const actualUrlPath = new URL(await browser.getUrl()).pathname;
  await expect(actualUrlPath).toBe(expectedUrlPath);
}
