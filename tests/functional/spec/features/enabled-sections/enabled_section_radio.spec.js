import sectionOne from "../../../generated_pages/section_enabled_radio/section-1-block.page";
import SubmitPage from "../../../generated_pages/section_enabled_radio/submit.page";

describe("Feature: Section Enabled Based On Radio Answers", () => {
  beforeEach("Open survey", async () => {
    await browser.openQuestionnaire("test_new_section_enabled_radio.json");
  });

  it("When the user answers `Yes, enable section 2` and submits, Then section 2 should be displayed", async () => {
    await $(sectionOne.yesEnableSection2()).click();
    await $(sectionOne.submit()).click();

    await expect(browser.getUrl()).to.contain("section-2-block");
  });

  it("When the user answers `No, disable section 2` and submits, Then they should be taking straight to the summary", async () => {
    await $(sectionOne.noDisableSection2()).click();
    await $(sectionOne.submit()).click();

    await expect(browser.getUrl()).to.contain(SubmitPage.url());
    await expect(await $(SubmitPage.section2Question()).isExisting()).to.be.false;
  });

  describe("Given that section 2 is enabled", () => {
    beforeEach("Enable section 2", async () => {
      await $(sectionOne.yesEnableSection2()).click();
      await $(sectionOne.submit()).click();

      await expect(browser.getUrl()).to.contain("section-2-block");
    });

    it("When the user changes the answers and disables section 2, Then they should be taken straight to the summary", async () => {
      browser.back();
      await expect(browser.getUrl()).to.contain("section-1-block");

      await $(sectionOne.noDisableSection2()).click();
      await $(sectionOne.submit()).click();
      await expect(browser.getUrl()).to.contain(SubmitPage.url());
    });
  });
});
