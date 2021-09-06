import DefaultInstructionPage from "../../../generated_pages/checkbox_instruction/default-instruction-checkbox.page";
import NoInstructionPage from "../../../generated_pages/checkbox_instruction/no-instruction-checkbox.page";
import customInstructionPage from "../../../generated_pages/checkbox_instruction/custom-instruction-checkbox.page";

describe("Given the checkbox label variants questionnaire,", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_checkbox_instruction.json");
  });
  it("Given an instruction has not been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then the default instruction should be visible", () => {
    expect($("body").getText()).to.have.string("Select all that apply");
  });
  it("Given an instruction has been set to null in the schema for a checkbox answer, When the checkbox answer is displayed, Then the instruction should not be visible", () => {
    $(DefaultInstructionPage.red()).click();
    $(DefaultInstructionPage.submit()).click();
    expect($("body").getText()).to.not.have.string("Select all that apply");
  });
  it("Given a custom instruction has been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then the custom instruction should be visible", () => {
    $(DefaultInstructionPage.red()).click();
    $(DefaultInstructionPage.submit()).click();
    $(NoInstructionPage.rugby()).click();
    $(NoInstructionPage.submit()).click();
    expect($("body").getText()).to.have.string("Select your answer");
  });
  it("Given a custom label and instruction have been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then both the custom instruction and label should be visible", () => {
    $(DefaultInstructionPage.red()).click();
    $(DefaultInstructionPage.submit()).click();
    $(NoInstructionPage.rugby()).click();
    $(NoInstructionPage.submit()).click();
    $(customInstructionPage.monday()).click();
    $(customInstructionPage.submit()).click();
    expect($("body").getText()).to.have.string("Days of the Week");
    expect($("body").getText()).to.have.string("Select your answer");
  });
});
