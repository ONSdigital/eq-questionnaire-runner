import RadioDropdownPage from "../../../generated_pages/radio_detail_answer_dropdown/optional-radio-with-dropdown-detail-answer-block.page";
import SubmitPage from "../../../generated_pages/radio_detail_answer_dropdown/submit.page";
import DropdownMandatoryPage from "../../../generated_pages/dropdown_mandatory/dropdown-mandatory.page";
import { click } from "../../../helpers";
describe("Optional Radio with a Dropdown detail answer", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_radio_detail_answer_dropdown.json");
  });

  describe("Given an optional radio with a dropdown detail answer", () => {
    it("When a placeholder is set for the detail answer, Then that value should be displayed as the first option", async () => {
      await $(RadioDropdownPage.fruit()).click();

      await expect(await $(RadioDropdownPage.fruitDetail()).getText()).toContain("Select fruit");
    });

    it("When a placeholder is not set for the detail answer, Then the default placeholder should be displayed as the first option", async () => {
      await $(RadioDropdownPage.jam()).click();

      await expect(await $(RadioDropdownPage.jamDetail()).getText()).toContain("Select an answer");
    });

    it("When the user does not provide an answer and submits, Then the summary should display 'No answer provided'", async () => {
      await click(RadioDropdownPage.submit());

      await expect(await $(SubmitPage.optionalRadioWithDropdownDetailAnswer()).getText()).toBe("No answer provided");
    });

    it("When the user selects an option with an optional detail answer but does not provide a detail answer, Then the summary should display the chosen option without the detail answer", async () => {
      await $(RadioDropdownPage.fruit()).click();
      await click(RadioDropdownPage.submit());

      await expect(await $(SubmitPage.optionalRadioWithDropdownDetailAnswer()).getText()).toBe("Fruit");
    });

    it("When the user selects an option with an optional detail answer and provides a detail answer, Then the summary should display the chosen option and the detail answer", async () => {
      await $(RadioDropdownPage.fruit()).click();
      await $(RadioDropdownPage.fruitDetail()).selectByAttribute("value", "Mango");
      await click(RadioDropdownPage.submit());

      await expect(await $(SubmitPage.optionalRadioWithDropdownDetailAnswer()).getText()).toBe("Fruit\nMango");
    });

    it("When the user selects the default dropdown option after submitting a detail answer, Then the summary should not display the detail answer", async () => {
      await $(RadioDropdownPage.fruit()).click();
      await $(RadioDropdownPage.fruitDetail()).selectByAttribute("value", "Mango");
      await click(RadioDropdownPage.submit());
      await $(SubmitPage.previous()).click();
      await $(RadioDropdownPage.fruitDetail()).selectByVisibleText("Select fruit");
      await click(RadioDropdownPage.submit());

      await expect(await $(SubmitPage.optionalRadioWithDropdownDetailAnswer()).getText()).toBe("Fruit");
    });

    it("When the user selects an option with an mandatory detail answer but does not provide a detail answer, Then an error should be displayed when the user submits", async () => {
      await $(RadioDropdownPage.jam()).click();
      await click(RadioDropdownPage.submit());

      await expect(await $(DropdownMandatoryPage.errorNumber(1)).getText()).toBe("Please select the type of Jam");
    });

    it("When the user selects an option with an mandatory detail answer and provides a detail answer, Then the summary should display the chosen option and its detail answer", async () => {
      await $(RadioDropdownPage.jam()).click();
      await $(RadioDropdownPage.jamDetail()).selectByAttribute("value", "Strawberry");
      await click(RadioDropdownPage.submit());

      await expect(await $(SubmitPage.optionalRadioWithDropdownDetailAnswer()).getText()).toBe("Jam\nStrawberry");
    });

    it("When the user removes a previously submitted detail answer by selecting another radio option, Then the summary should only display the new radio option", async () => {
      await $(RadioDropdownPage.jam()).click();
      await $(RadioDropdownPage.jamDetail()).selectByAttribute("value", "Raspberry");
      await click(RadioDropdownPage.submit());
      await $(SubmitPage.previous()).click();
      await $(RadioDropdownPage.fruit()).click();
      await click(RadioDropdownPage.submit());

      await expect(await $(SubmitPage.optionalRadioWithDropdownDetailAnswer()).getText()).toBe("Fruit");
    });
  });
});
