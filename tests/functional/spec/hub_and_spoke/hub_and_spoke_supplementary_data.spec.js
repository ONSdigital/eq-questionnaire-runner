import HubPage from "../../base_pages/hub.page.js";
import { clickSyncMode, verifyUrlContainsSyncMode } from "../../helpers";
import LoadedSuccessfullyBlockPage from "../../generated_pages/hub_section_required_with_repeat_supplementary/loaded-successfully-block.page";
import IntroductionBlockPage from "../../generated_pages/hub_section_required_with_repeat_supplementary/introduction-block.page";
import ListCollectorEmployeesPage from "../../generated_pages/hub_section_required_with_repeat_supplementary/list-collector-employees.page.js";
import LengthOfEmploymentPage from "../../generated_pages/hub_section_required_with_repeat_supplementary/length-of-employment.page.js";
import Section3Page from "../../generated_pages/hub_section_required_with_repeat_supplementary/section-3-summary.page.js";
import { getRandomString } from "../../jwt_helper";

describe("Feature: Hub and Spoke", () => {
  describe("Given a user opens a schema with hub required sections based on a repeating section using supplementary data", () => {
    beforeEach("Load survey", () => {
      const responseId = getRandomString(16);

      browser.openQuestionnaire("test_hub_section_required_with_repeat_supplementary.json.json", {
        version: "v2",
        sdsDatasetId: "203b2f9d-c500-8175-98db-86ffcfdccfa3",
        responseId,
      });
    });

    it("When all the repeating sections are complete, Then the hub should be displayed", () => {
      clickSyncMode(LoadedSuccessfullyBlockPage.submit());
      clickSyncMode(IntroductionBlockPage.submit());

      // Complete the repeating sections using supplementary data
      clickSyncMode(ListCollectorEmployeesPage.submit());
      $(LengthOfEmploymentPage.day()).setValue(1);
      $(LengthOfEmploymentPage.month()).setValue(1);
      $(LengthOfEmploymentPage.year()).setValue(1930);
      clickSyncMode(LengthOfEmploymentPage.submit());
      clickSyncMode(Section3Page.submit());
      $(LengthOfEmploymentPage.day()).setValue(1);
      $(LengthOfEmploymentPage.month()).setValue(1);
      $(LengthOfEmploymentPage.year()).setValue(1930);
      clickSyncMode(LengthOfEmploymentPage.submit());
      clickSyncMode(Section3Page.submit());
      verifyUrlContainsSyncMode(HubPage.url());
    });

    it("When the repeating sections are incomplete. Then the hub should not be displayed", () => {
      clickSyncMode(LoadedSuccessfullyBlockPage.submit());
      clickSyncMode(IntroductionBlockPage.submit());

      // Don't complete the repeating sections that use supplementary data
      clickSyncMode(ListCollectorEmployeesPage.submit());
      $(LengthOfEmploymentPage.day()).setValue(1);
      $(LengthOfEmploymentPage.month()).setValue(1);
      $(LengthOfEmploymentPage.year()).setValue(1930);
      clickSyncMode(LengthOfEmploymentPage.submit());
      clickSyncMode(Section3Page.submit());

      browser.url(HubPage.url());
      verifyUrlContainsSyncMode("length-of-employment");
    });
  });
});
