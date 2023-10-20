import sectionOne from "../../../generated_pages/section_enabled_radio/section-1-block.page";
import SubmitPage from "../../../generated_pages/section_enabled_radio/submit.page";
import { click } from "../../../helpers";
describe("Feature: Section Enabled Based On Radio Answers", () => {
  beforeEach("Open survey", async () => {
    await browser.openQuestionnaire("test_section_enabled_radio.json");
  });

  it("When the user answers `Yes, enable section 2` and submits, Then section 2 should be displayed", async () => {
    await $(sectionOne.yesEnableSection2()).click();
    await click(sectionOne.submit());

    await expect(await browser.getUrl()).toContain("section-2-block");
  });

  it("When the user answers `No, disable section 2` and submits, Then they should be taking straight to the summary", async () => {
    await $(sectionOne.noDisableSection2()).click();
    await click(sectionOne.submit());

    await expect(await browser.getUrl()).toContain(SubmitPage.url());
    await expect(await $(SubmitPage.section2Question()).isExisting()).toBe(false);
  });

  describe("Given that section 2 is enabled", () => {
    beforeEach("Enable section 2", async () => {
      await $(sectionOne.yesEnableSection2()).click();
      await click(sectionOne.submit());

      await expect(await browser.getUrl()).toContain("section-2-block");
    });

    it("When the user changes the answers and disables section 2, Then they should be taken straight to the summary", async () => {
      await browser.back();
      await expect(await browser.getUrl()).toContain("section-1-block");

      await $(sectionOne.noDisableSection2()).click();
      await click(sectionOne.submit());
      await expect(await browser.getUrl()).toContain(SubmitPage.url());
    });
  });
});
