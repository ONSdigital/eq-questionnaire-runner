import sectionOne from "../../../generated_pages/section_enabled_checkbox/section-1-block.page";
import sectionTwo from "../../../generated_pages/section_enabled_checkbox/section-2-block.page";
import SubmitPage from "../../../generated_pages/section_enabled_checkbox/submit.page";
import { click, verifyUrlContains } from "../../../helpers";
describe("Feature: Section Enabled Based On Checkbox Answers", () => {
  beforeEach("Open survey", async () => {
    await browser.openQuestionnaire("test_section_enabled_checkbox.json");
  });

  it("When the user selects `Section 2` and submits, Then section 2 should be displayed", async () => {
    await $(sectionOne.section1Section2()).click();
    await click(sectionOne.submit());

    await verifyUrlContains("section-2-block");
  });

  it("When the user selects `Section 3` and submits, Then section 2 should not be displayed and section 3 should be displayed", async () => {
    await $(sectionOne.section1Section3()).click();
    await click(sectionOne.submit());

    await verifyUrlContains("section-3-block");
  });

  it("When the user selects `Section 2` and `Section 3` and submits, Then section 2 and section 3 should be displayed", async () => {
    await $(sectionOne.section1Section2()).click();
    await $(sectionOne.section1Section3()).click();
    await click(sectionOne.submit());

    await verifyUrlContains("section-2-block");
    await click(sectionTwo.submit());
    await verifyUrlContains("section-3-block");
  });

  it("When the user selects `Neither` and submits, Then they should be taken straight to the summary", async () => {
    await $(sectionOne.section1ExclusiveNeither()).click();
    await click(sectionOne.submit());

    await verifyUrlContains(SubmitPage.url());
    await expect(await $(SubmitPage.section2Question()).isExisting()).toBe(false);
    await expect(await $(SubmitPage.section3Question()).isExisting()).toBe(false);
  });
});
