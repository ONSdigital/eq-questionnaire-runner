import sectionOne from "../../../generated_pages/section_enabled_radio/section-1-block.page";
import summary from "../../../generated_pages/section_enabled_radio/summary.page";

describe("Feature: Section Enabled Based On Radio Answers", () => {
  beforeEach("Open survey", () => {
    browser.openQuestionnaire("test_section_enabled_radio.json");
  });

  it("When the user answers `Yes, enable section 2` and submits, Then section 2 should be displayed", () => {
    $(sectionOne.yesEnableSection2()).click();
    $(sectionOne.submit()).click();

    expect(browser.getUrl()).to.contain("section-2-block");
  });

  it("When the user answers `No, disable section 2` and submits, Then they should be taking straight to the summary", () => {
    $(sectionOne.noDisableSection2()).click();
    $(sectionOne.submit()).click();

    expect(browser.getUrl()).to.contain(summary.url());
    expect($(summary.section2Question()).isExisting()).to.be.false;
  });

  describe("Given that section 2 is enabled", () => {
    beforeEach("Enable section 2", () => {
      $(sectionOne.yesEnableSection2()).click();
      $(sectionOne.submit()).click();

      expect(browser.getUrl()).to.contain("section-2-block");
    });

    it("When the user changes the answers and disables section 2, Then they should be taken straight to the summary", () => {
      browser.back();
      expect(browser.getUrl()).to.contain("section-1-block");

      $(sectionOne.noDisableSection2()).click();
      $(sectionOne.submit()).click();
      expect(browser.getUrl()).to.contain(summary.url());
    });
  });
});
