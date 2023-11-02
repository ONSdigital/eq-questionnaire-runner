import CheckboxDropdownPage from "../../../generated_pages/checkbox_detail_answer_dropdown/optional-checkbox-with-dropdown-detail-answer-block.page";
import SubmitPage from "../../../generated_pages/checkbox_detail_answer_dropdown/submit.page";
import DropdownMandatoryPage from "../../../generated_pages/dropdown_mandatory/dropdown-mandatory.page";
import { click } from "../../../helpers";
describe("Optional Checkbox with a Dropdown detail answer", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_checkbox_detail_answer_dropdown.json");
  });

  describe("Given an optional checkbox with a dropdown detail answer", () => {
    it("When a placeholder is set for the detail answer, Then that value should be displayed as the first option", async () => {
      await $(CheckboxDropdownPage.fruit()).click();

      await expect(await $(CheckboxDropdownPage.fruitDetail()).getText()).toContain("Select fruit");
    });

    it("When a placeholder is not set for the detail answer, Then the default placeholder should be displayed as the first option", async () => {
      await $(CheckboxDropdownPage.jam()).click();

      await expect(await $(CheckboxDropdownPage.jamDetail()).getText()).toContain("Select an answer");
    });

    it("When the user does not provide an answer and submits, Then the summary should display 'No answer provided'", async () => {
      await click(CheckboxDropdownPage.submit());

      await expect(await $(SubmitPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).toBe("No answer provided");
    });

    it("When the user selects an option with an optional detail answer but does not provide a detail answer, Then the summary should display the chosen option without the detail answer", async () => {
      await $(CheckboxDropdownPage.fruit()).click();
      await click(CheckboxDropdownPage.submit());

      await expect(await $(SubmitPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).toBe("Fruit");
    });

    it("When the user selects an option with an optional detail answer and provides a detail answer, Then the summary should display the chosen option and the detail answer", async () => {
      await $(CheckboxDropdownPage.fruit()).click();
      await $(CheckboxDropdownPage.fruitDetail()).selectByAttribute("value", "Mango");
      await click(CheckboxDropdownPage.submit());

      await expect(await $(SubmitPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).toBe("Fruit\nMango");
    });

    it("When the user selects the default dropdown option after submitting a detail answer, Then the summary should not display the detail answer", async () => {
      await $(CheckboxDropdownPage.fruit()).click();
      await $(CheckboxDropdownPage.fruitDetail()).selectByAttribute("value", "Mango");
      await click(CheckboxDropdownPage.submit());
      await $(SubmitPage.previous()).click();
      await $(CheckboxDropdownPage.fruitDetail()).selectByVisibleText("Select fruit");
      await click(CheckboxDropdownPage.submit());

      await expect(await $(SubmitPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).toBe("Fruit");
    });

    it("When the user selects an option with an mandatory detail answer but does not provide a detail answer, Then an error should be displayed when the user submits", async () => {
      await $(CheckboxDropdownPage.jam()).click();
      await click(CheckboxDropdownPage.submit());

      await expect(await $(DropdownMandatoryPage.errorNumber(1)).getText()).toBe("Please select the type of Jam");
    });

    it("When the user selects an option with an mandatory detail answer and provides a detail answer, Then the summary should display the chosen option and its details", async () => {
      await $(CheckboxDropdownPage.jam()).click();
      await $(CheckboxDropdownPage.jamDetail()).selectByAttribute("value", "Strawberry");
      await click(CheckboxDropdownPage.submit());

      await expect(await $(SubmitPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).toBe("Jam\nStrawberry");
    });

    it("When the user removes a previously submitted detail answer, Then the summary should not display the removed detail answer", async () => {
      await $(CheckboxDropdownPage.fruit()).click();
      await $(CheckboxDropdownPage.fruitDetail()).selectByAttribute("value", "Mango");
      await click(CheckboxDropdownPage.submit());
      await $(SubmitPage.previous()).click();
      await $(CheckboxDropdownPage.fruit()).click();
      await click(CheckboxDropdownPage.submit());

      await expect(await $(SubmitPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).toBe("No answer provided");
    });

    it("When the user selects multiple options with detail answers and submits, Then the summary should display all the chosen options and their detail answer", async () => {
      await $(CheckboxDropdownPage.fruit()).click();
      await $(CheckboxDropdownPage.fruitDetail()).selectByAttribute("value", "Mango");
      await $(CheckboxDropdownPage.jam()).click();
      await $(CheckboxDropdownPage.jamDetail()).selectByAttribute("value", "Strawberry");
      await click(CheckboxDropdownPage.submit());

      await expect(await $(SubmitPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).toBe("Fruit\nMango\nJam\nStrawberry");
    });
  });
});
