import DoesAnyoneLiveHere from "../../../generated_pages/hub_and_spoke/does-anyone-live-here.page.js";
import HouseholdSummary from "../../../generated_pages/hub_and_spoke/household-section-summary.page.js";
import HowManyPeopleLiveHere from "../../../generated_pages/hub_and_spoke/how-many-people-live-here.page.js";
import HubPage from "../../../base_pages/hub.page.js";
import { click, verifyUrlContains } from "../../../helpers";
import { getRandomString } from "../../../jwt_helper";
import LoadedSuccessfullyBlockPage from "../../../generated_pages/hub_section_required_with_repeat_supplementary/loaded-successfully-block.page";
import IntroductionBlockPage from "../../../generated_pages/hub_section_required_with_repeat_supplementary/introduction-block.page";
import ListCollectorEmployeesPage from "../../../generated_pages/hub_section_required_with_repeat_supplementary/list-collector-employees.page.js";
import LengthOfEmploymentPage from "../../../generated_pages/hub_section_required_with_repeat_supplementary/length-of-employment.page.js";
import Section3Page from "../../../generated_pages/hub_section_required_with_repeat_supplementary/section-3-summary.page.js";

describe("Feature: Hub and Spoke With Supplementary Data", () => {
  const hubAndSpokeSchema = "test_hub_and_spoke.json";

  describe("Given a user opens a schema with hub required sections based on a repeating section using supplementary data", () => {
    beforeEach("Load survey", async () => {
      const responseId = getRandomString(16);

      await browser.openQuestionnaire("test_hub_section_required_with_repeat_supplementary.json", {
        version: "v2",
        sdsDatasetId: "203b2f9d-c500-8175-98db-86ffcfdccfa3",
        responseId,
      });
    });

    // Don't use async/await here to resolve issues with the flakiness of this test
    it("When all the repeating sections are complete, Then the hub should be displayed", () => {
      return browser.pause(1000)
        .then(() => browser.url(LoadedSuccessfullyBlockPage.url()))
        .then(() => click(LoadedSuccessfullyBlockPage.submit()))
        .then(() => click(IntroductionBlockPage.submit()))
        .then(() => click(ListCollectorEmployeesPage.submit()))
        .then(() => $(LengthOfEmploymentPage.day()).setValue(1))
        .then(() => $(LengthOfEmploymentPage.month()).setValue(1))
        .then(() => $(LengthOfEmploymentPage.year()).setValue(1930))
        .then(() => click(LengthOfEmploymentPage.submit()))
        .then(() => click(Section3Page.submit()))
        .then(() => $(LengthOfEmploymentPage.day()).setValue(1))
        .then(() => $(LengthOfEmploymentPage.month()).setValue(1))
        .then(() => $(LengthOfEmploymentPage.year()).setValue(1930))
        .then(() => click(LengthOfEmploymentPage.submit()))
        .then(() => click(Section3Page.submit()))
        .then(() => verifyUrlContains(HubPage.url()));
    });

    it("When the repeating sections are incomplete. Then the hub should not be displayed", async () => {
      await click(LoadedSuccessfullyBlockPage.submit());
      await click(IntroductionBlockPage.submit());

      // Don't complete the repeating sections that use supplementary data
      await click(ListCollectorEmployeesPage.submit());
      await $(LengthOfEmploymentPage.day()).setValue(1);
      await $(LengthOfEmploymentPage.month()).setValue(1);
      await $(LengthOfEmploymentPage.year()).setValue(1930);
      await click(LengthOfEmploymentPage.submit());
      await click(Section3Page.submit());

      await browser.url(HubPage.url());
      await verifyUrlContains("length-of-employment");
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
