import CheckboxVisibleTruePage from "../../../generated_pages/checkbox_detail_answer_textfield/checkbox-visible-true.page.js";
import CheckboxVisibleFalsePage from "../../../generated_pages/checkbox_detail_answer_textfield/checkbox-visible-false.page.js";
import CheckboxVisibleNonePage from "../../../generated_pages/checkbox_detail_answer_textfield/checkbox-visible-none.page.js";
import MutuallyExclusivePage from "../../../generated_pages/checkbox_detail_answer_textfield/mutually-exclusive.page.js";
import { click } from "../../../helpers";

describe("Given the checkbox detail_answer questionnaire,", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_checkbox_detail_answer_textfield.json");
  });
  it("When a checkbox has a detail_answer with visible set to true, Then the detail answer write-in field should be shown", async () => {
    await expect(await $(CheckboxVisibleTruePage.otherDetail()).isDisplayed()).toBe(true);
  });
  it("When a checkbox has a detail_answer with visible set to true and another answer is checked, then the detail answer write-in field should still be shown", async () => {
    await $(CheckboxVisibleTruePage.coffee()).click();
    await expect(await $(CheckboxVisibleTruePage.otherDetail()).isDisplayed()).toBe(true);
  });
  it("When a checkbox has a detail_answer with visible set to false, Then the detail answer write-in field should not be shown", async () => {
    await $(CheckboxVisibleTruePage.coffee()).click();
    await click(CheckboxVisibleTruePage.submit());
    await expect(await $(CheckboxVisibleFalsePage.otherDetail()).isDisplayed()).toBe(false);
  });
  it("When a checkbox has a detail_answer with visible not set, Then the detail answer write-in field should not be shown", async () => {
    await $(CheckboxVisibleTruePage.coffee()).click();
    await click(CheckboxVisibleTruePage.submit());
    await $(CheckboxVisibleFalsePage.iceCream()).click();
    await click(CheckboxVisibleFalsePage.submit());
    await expect(await $(CheckboxVisibleNonePage.otherDetail()).isDisplayed()).toBe(false);
  });
  it("When a mutually exclusive checkbox has a detail_answer with visible set to true, Then the detail answer write-in field should be shown", async () => {
    await $(CheckboxVisibleTruePage.coffee()).click();
    await click(CheckboxVisibleTruePage.submit());
    await $(CheckboxVisibleFalsePage.iceCream()).click();
    await click(CheckboxVisibleFalsePage.submit());
    await $(CheckboxVisibleNonePage.blue()).click();
    await click(CheckboxVisibleNonePage.submit());
    await expect(await $(MutuallyExclusivePage.otherDetail()).isDisplayed()).toBe(true);
  });
});
