import sectionOne from "../../../generated_pages/section_enabled_checkbox/section-1-block.page";
import sectionTwo from "../../../generated_pages/section_enabled_checkbox/section-2-block.page";
import summary from "../../../generated_pages/section_enabled_checkbox/summary.page";

describe("Feature: Section Enabled Based On Checkbox Answers", () => {
  beforeEach("Open survey", () => {
    browser.openQuestionnaire("test_section_enabled_checkbox.json");
  });

  it("When the user selects `Section 2` and submits, Then section 2 should be displayed", () => {
    $(sectionOne.section1Section2()).click();
    $(sectionOne.submit()).click();

    expect(browser.getUrl()).to.contain("section-2-block");
  });

  it("When the user selects `Section 3` and submits, Then section 2 should not be displayed and section 3 should be displayed", () => {
    $(sectionOne.section1Section3()).click();
    $(sectionOne.submit()).click();

    expect(browser.getUrl()).to.contain("section-3-block");
  });

  it("When the user selects `Section 2` and `Section 3` and submits, Then section 2 and section 3 should be displayed", () => {
    $(sectionOne.section1Section2()).click();
    $(sectionOne.section1Section3()).click();
    $(sectionOne.submit()).click();

    expect(browser.getUrl()).to.contain("section-2-block");
    $(sectionTwo.submit()).click();
    expect(browser.getUrl()).to.contain("section-3-block");
  });

  it("When the user selects `Neither` and submits, Then they should be taken straight to the summary", () => {
    $(sectionOne.section1ExclusiveNeither()).click();
    $(sectionOne.submit()).click();

    expect(browser.getUrl()).to.contain(summary.url());
    expect($(summary.section2Question()).isExisting()).to.be.false;
    expect($(summary.section3Question()).isExisting()).to.be.false;
  });
});
