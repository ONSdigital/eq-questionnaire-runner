import HubPage from "../../../base_pages/hub.page.js";
import { click } from "../../../helpers";
import LoadedSuccessfullyBlockPage from "../../../generated_pages/hub_section_required_with_repeat_supplementary/loaded-successfully-block.page";
import IntroductionBlockPage from "../../../generated_pages/hub_section_required_with_repeat_supplementary/introduction-block.page";
import ListCollectorEmployeesPage from "../../../generated_pages/hub_section_required_with_repeat_supplementary/list-collector-employees.page.js";
import LengthOfEmploymentPage from "../../../generated_pages/hub_section_required_with_repeat_supplementary/length-of-employment.page.js";
import Section3Page from "../../../generated_pages/hub_section_required_with_repeat_supplementary/section-3-summary.page.js";
import { getRandomString } from "../../../jwt_helper";

describe("Feature: Hub and Spoke with Supplementary Data", () => {
  describe("Given a user opens a schema with hub required sections based on a repeating section using supplementary data", () => {
    beforeEach("Load survey", async () => {
      const responseId = getRandomString(16);
      await browser.openQuestionnaire("test_hub_section_required_with_repeat_supplementary.json", {
        version: "v2",
        sdsDatasetId: "203b2f9d-c500-8175-98db-86ffcfdccfa3",
        responseId,
      });
    });

    it("When all the repeating sections are complete, Then the hub should be displayed", async () => {
      await click(LoadedSuccessfullyBlockPage.submit());
      await click(IntroductionBlockPage.submit());

      // Complete the repeating sections using supplementary data
      await click(ListCollectorEmployeesPage.submit());
      await $(LengthOfEmploymentPage.day()).setValue(1);
      await $(LengthOfEmploymentPage.month()).setValue(1);
      await $(LengthOfEmploymentPage.year()).setValue(1930);
      await click(LengthOfEmploymentPage.submit());
      await click(Section3Page.submit());
      await $(LengthOfEmploymentPage.day()).setValue(1);
      await $(LengthOfEmploymentPage.month()).setValue(1);
      await $(LengthOfEmploymentPage.year()).setValue(1930);
      await click(LengthOfEmploymentPage.submit());
      await click(Section3Page.submit());
      await expect(browser).toHaveUrlContaining(HubPage.url());
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
      await expect(browser).toHaveUrlContaining("length-of-employment");
    });
  });
});
