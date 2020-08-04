import sectionOne from "../../../generated_pages/section_enabled_hub/section-1-block.page";
import hubPage from "../../../base_pages/hub.page";

describe("Feature: Section Enabled With Hub", () => {
  beforeEach("Open survey", () => {
    browser.openQuestionnaire("test_section_enabled_hub.json");
  });

  it("When the user selects `Section 2` and submits, Then only section 2 should be displayed on the hub", () => {
    $(sectionOne.section1Section2()).click();
    $(sectionOne.submit()).click();

    expect($(hubPage.summaryRowState("section-2")).isDisplayed()).to.be.true;
    expect($(hubPage.summaryRowTitle("section-2")).getText()).to.equal("Section 2");

    expect($(hubPage.summaryRowState("section-3")).isDisplayed()).to.be.false;
  });

  it("When the user selects `Section 3` and submits, Then section 2 should not be displayed and section 3 should be displayed", () => {
    $(sectionOne.section1Section3()).click();
    $(sectionOne.submit()).click();

    expect($(hubPage.summaryRowState("section-3")).isDisplayed()).to.be.true;
    expect($(hubPage.summaryRowTitle("section-3")).getText()).to.equal("Section 3");

    expect($(hubPage.summaryRowState("section-2")).isDisplayed()).to.be.false;
  });

  it("When the user selects `Section 2` and `Section 3` and submits, Then section 2 and section 3 should be displayed", () => {
    $(sectionOne.section1Section2()).click();
    $(sectionOne.section1Section3()).click();
    $(sectionOne.submit()).click();

    expect($(hubPage.summaryRowState("section-2")).isDisplayed()).to.be.true;
    expect($(hubPage.summaryRowTitle("section-2")).getText()).to.equal("Section 2");

    expect($(hubPage.summaryRowState("section-3")).isDisplayed()).to.be.true;
    expect($(hubPage.summaryRowTitle("section-3")).getText()).to.equal("Section 3");
  });

  it("When the user selects `Neither` and submits,  Then hub should not display any other section and should be in the `Completed` state.", () => {
    $(sectionOne.section1ExclusiveNeither()).click();
    $(sectionOne.submit()).click();

    expect($(hubPage.summaryRowState("section-2")).isDisplayed()).to.be.false;
    expect($(hubPage.summaryRowState("section-3")).isDisplayed()).to.be.false;

    expect($(hubPage.submit()).getText()).to.equal("Submit survey");
    expect($(hubPage.heading()).getText()).to.equal("Submit survey");
  });
});
