import DefaultInstructionPage from "../../../generated_pages/checkbox_instruction/default-instruction-checkbox.page";
import NoInstructionPage from "../../../generated_pages/checkbox_instruction/no-instruction-checkbox.page";
import CustomInstructionPage from "../../../generated_pages/checkbox_instruction/custom-instruction-checkbox.page";
import { click } from "../../../helpers";
describe("Given the checkbox label variants questionnaire,", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_checkbox_instruction.json");
  });
  it("Given an instruction has not been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then the default instruction should be visible", async () => {
    await expect(await $("body").getText()).toContain("Select all that apply");
  });
  it("Given an instruction has been set to null in the schema for a checkbox answer, When the checkbox answer is displayed, Then the instruction should not be visible", async () => {
    await $(DefaultInstructionPage.red()).click();
    await click(DefaultInstructionPage.submit());
    await expect(await $("body").getText()).not.toEqual("Select all that apply");
  });
  it("Given a custom instruction has been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then the custom instruction should be visible", async () => {
    await $(DefaultInstructionPage.red()).click();
    await click(DefaultInstructionPage.submit());
    await $(NoInstructionPage.rugby()).click();
    await click(NoInstructionPage.submit());
    await expect(await $("body").getText()).toContain("Select your answer");
  });
  it("Given a label and custom instruction have been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then both the custom instruction and label should be visible", async () => {
    await $(DefaultInstructionPage.red()).click();
    await click(DefaultInstructionPage.submit());
    await $(NoInstructionPage.rugby()).click();
    await click(NoInstructionPage.submit());
    await $(CustomInstructionPage.monday()).click();
    await click(CustomInstructionPage.submit());
    await expect(await $("body").getText()).toContain("Days of the Week");
    await expect(await $("body").getText()).toContain("Select your answer");
  });
});
