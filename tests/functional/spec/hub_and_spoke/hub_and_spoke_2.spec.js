import HubPage from "../../base_pages/hub.page.js";
import { click, clickSuppData, verifyUrlContains } from "../../helpers";
import LoadedSuccessfullyBlockPage from "../../generated_pages/hub_section_required_with_repeat_supplementary/loaded-successfully-block.page";
import IntroductionBlockPage from "../../generated_pages/hub_section_required_with_repeat_supplementary/introduction-block.page";
import ListCollectorEmployeesPage from "../../generated_pages/hub_section_required_with_repeat_supplementary/list-collector-employees.page.js";
import LengthOfEmploymentPage from "../../generated_pages/hub_section_required_with_repeat_supplementary/length-of-employment.page.js";
import Section3Page from "../../generated_pages/hub_section_required_with_repeat_supplementary/section-3-summary.page.js";

describe("Feature: Hub and Spoke", () => {
  describe("Given a user opens a schema with hub required sections based on a repeating section using supplementary data", () => {
    beforeEach("Load survey", () => {
      browser.openSDSQuestionnaire("test_hub_section_required_with_repeat_supplementary.json");
    });

    it("When all the repeating sections are complete, Then the hub should be displayed", () => {
      clickSuppData(LoadedSuccessfullyBlockPage.submit());
      clickSuppData(IntroductionBlockPage.submit());

      // Complete the repeating sections using supplementary data
      clickSuppData(ListCollectorEmployeesPage.submit());
      $(LengthOfEmploymentPage.day()).setValue(1);
      $(LengthOfEmploymentPage.month()).setValue(1);
      $(LengthOfEmploymentPage.year()).setValue(1930);
      clickSuppData(LengthOfEmploymentPage.submit());
      click(Section3Page.submit());
      $(LengthOfEmploymentPage.day()).setValue(1);
      $(LengthOfEmploymentPage.month()).setValue(1);
      $(LengthOfEmploymentPage.year()).setValue(1930);
      clickSuppData(LengthOfEmploymentPage.submit());
      clickSuppData(Section3Page.submit());
      verifyUrlContains(HubPage.url());
    });

    it("When the repeating sections are incomplete. Then the hub should not be displayed", () => {
      clickSuppData(LoadedSuccessfullyBlockPage.submit());
      clickSuppData(IntroductionBlockPage.submit());

      // Don't complete the repeating sections that use supplementary data
      clickSuppData(ListCollectorEmployeesPage.submit());
      $(LengthOfEmploymentPage.day()).setValue(1);
      $(LengthOfEmploymentPage.month()).setValue(1);
      $(LengthOfEmploymentPage.year()).setValue(1930);
      clickSuppData(LengthOfEmploymentPage.submit());
      clickSuppData(Section3Page.submit());

      browser.url(HubPage.url());
      verifyUrlContains("length-of-employment");
    });
  });
});
