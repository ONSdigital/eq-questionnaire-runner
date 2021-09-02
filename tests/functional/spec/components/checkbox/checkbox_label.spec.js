import DefaultLabelPage from "../../../generated_pages/checkbox_instruction/default-label-checkbox.page";
import NoLabelPage from "../../../generated_pages/checkbox_instruction/no-label-checkbox.page";

describe("Given the checkbox label variants questionnaire,", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_checkbox_instruction.json");
  });
  it("Given an instruction has not been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then the default instruction should be visible", () => {
    expect($("body").getText()).to.have.string("Select all that apply");
  });
  it("Given an instruction has been set to null in the schema for a checkbox answer, When the checkbox answer is displayed, Then the instruction should not be visible", () => {
    $(DefaultLabelPage.red()).click();
    $(DefaultLabelPage.submit()).click();
    expect($("body").getText()).to.not.have.string("Select all that apply");
  });
  it("Given a custom instruction has been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then the custom instruction should be visible", () => {
    $(DefaultLabelPage.red()).click();
    $(DefaultLabelPage.submit()).click();
    $(NoLabelPage.rugby()).click();
    $(NoLabelPage.submit()).click();
    expect($("body").getText()).to.have.string("Select your answer");
  });
});
