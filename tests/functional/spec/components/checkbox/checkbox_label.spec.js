import DefaultLabelPage from "../../../generated_pages/checkbox_label/default-label-checkbox.page";
import NoLabelPage from "../../../generated_pages/checkbox_label/no-label-checkbox.page";

describe("Given the checkbox label variants questionnaire,", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_checkbox_label.json");
  });
  it("Given a label has not been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then the default label should be visible", () => {
    expect($("body").getText()).to.have.string("Select all that apply");
  });
  it("Given a label has been set to null in the schema for a checkbox answer, When the checkbox answer is displayed, Then the label should not be visible", () => {
    $(DefaultLabelPage.red()).click();
    $(DefaultLabelPage.submit()).click();
    expect($("body").getText()).to.not.have.string("Select all that apply");
  });
  it("Given a custom label has been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then the custom label should be visible", () => {
    $(DefaultLabelPage.red()).click();
    $(DefaultLabelPage.submit()).click();
    $(NoLabelPage.rugby()).click();
    $(NoLabelPage.submit()).click();
    expect($("body").getText()).to.have.string("Select your answer");
  });
});
