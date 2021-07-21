import CheckboxVisibleTruePage from "../../../generated_pages/checkbox_detail_answer_textfield/checkbox-visible-true.page.js";
import CheckboxVisibleFalsePage from "../../../generated_pages/checkbox_detail_answer_textfield/checkbox-visible-false.page.js";
import CheckboxVisibleNonePage from "../../../generated_pages/checkbox_detail_answer_textfield/checkbox-visible-none.page.js";
import MutuallyExclusivePage from "../../../generated_pages/checkbox_detail_answer_textfield/mutually-exclusive.page.js";

describe("Given the checkbox detail_answer questionnaire,", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_checkbox_detail_answer_textfield.json");
  });
  it("When a checkbox has a detail_answer with visible set to true, Then the detail answer write-in field should be shown", () => {
    expect($(CheckboxVisibleTruePage.otherDetail()).isDisplayed()).to.be.true;
  });
  it("When a checkbox has a detail_answer with visible set to true and another answer is checked, then the detail answer write-in field should still be shown", () => {
    $(CheckboxVisibleTruePage.coffee()).click();
    expect($(CheckboxVisibleTruePage.otherDetail()).isDisplayed()).to.be.true;
  });
  it("When a checkbox has a detail_answer with visible set to false, Then the detail answer write-in field should not be shown", () => {
    $(CheckboxVisibleTruePage.coffee()).click();
    $(CheckboxVisibleTruePage.submit()).click();
    expect($(CheckboxVisibleFalsePage.otherDetail()).isDisplayed()).to.be.false;
  });
  it("When a checkbox has a detail_answer with visible not set, Then the detail answer write-in field should not be shown", () => {
    $(CheckboxVisibleTruePage.coffee()).click();
    $(CheckboxVisibleTruePage.submit()).click();
    $(CheckboxVisibleFalsePage.iceCream()).click();
    $(CheckboxVisibleFalsePage.submit()).click();
    expect($(CheckboxVisibleNonePage.otherDetail()).isDisplayed()).to.be.false;
  });
  it("When a mutually exclusive checkbox has a detail_answer with visible set to true, Then the detail answer write-in field should be shown", () => {
    $(CheckboxVisibleTruePage.coffee()).click();
    $(CheckboxVisibleTruePage.submit()).click();
    $(CheckboxVisibleFalsePage.iceCream()).click();
    $(CheckboxVisibleFalsePage.submit()).click();
    $(CheckboxVisibleNonePage.blue()).click();
    $(CheckboxVisibleNonePage.submit()).click();
    expect($(MutuallyExclusivePage.otherDetail()).isDisplayed()).to.be.true;
  });
});
