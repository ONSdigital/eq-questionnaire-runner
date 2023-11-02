import ReferenceDatePage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/reference-date.page";
import DynamicCheckboxPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-checkbox.page";
import DynamicRadioPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-radio.page";
import DynamicDropdownPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-dropdown.page";
import DynamicMutuallyExclusivePage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-mutually-exclusive.page";
import { click } from "../../../helpers";
describe(`Feature: Dynamically generated mandatory answer options driven by a function with static options`, () => {
  describe("Given a mandatory dynamic answer options questionnaire with static options", () => {
    before("Open questionnaire", async () => {
      await browser.openQuestionnaire("test_dynamic_answer_options_function_driven_with_static_options_mandatory.json");
      // Set reference date
      await $(ReferenceDatePage.day()).setValue("1");
      await $(ReferenceDatePage.month()).setValue("1");
      await $(ReferenceDatePage.year()).setValue("2021");
      await click(ReferenceDatePage.submit());
    });

    it("When I do not answer the Checkbox question and submit, then an error message and the question error panel should be displayed.", async () => {
      await click(DynamicCheckboxPage.submit());
      await expect(await $(DynamicCheckboxPage.errorHeader()).getText()).toBe("There is a problem with your answer");
      await expect(await $(DynamicCheckboxPage.answerErrorItem()).getText()).toContain("Select at least one answer");
      await expect(await $(DynamicCheckboxPage.questionErrorPanel()).isExisting()).toBe(true);
    });

    it("When I do not answer the Radio question and submit, then an error message and the question error panel should be displayed.", async () => {
      // Get to Radio question
      await $(DynamicCheckboxPage.answerByIndex(0)).click();
      await click(DynamicCheckboxPage.submit());

      await click(DynamicRadioPage.submit());
      await expect(await $(DynamicRadioPage.errorHeader()).getText()).toBe("There is a problem with your answer");
      await expect(await $(DynamicRadioPage.answerErrorItem()).getText()).toContain("Select an answer");
      await expect(await $(DynamicRadioPage.questionErrorPanel()).isExisting()).toBe(true);
    });

    it("When I do not answer the Dropdown question and submit, then an error message and the question error panel should be displayed.", async () => {
      // Get to Dropdown question
      await $(DynamicRadioPage.answerByIndex(0)).click();
      await click(DynamicRadioPage.submit());

      await click(DynamicDropdownPage.submit());
      await expect(await $(DynamicDropdownPage.errorHeader()).getText()).toBe("There is a problem with your answer");
      await expect(await $(DynamicDropdownPage.answerErrorItem()).getText()).toBe("Select an answer");
      await expect(await $(DynamicDropdownPage.questionErrorPanel()).isExisting()).toBe(true);
    });

    it("When I do not answer the Mutually Exclusive Checkbox question and submit, then an error message and the question error panel should be displayed.", async () => {
      // Get to Mutually Exclusive question
      await $(DynamicDropdownPage.answer()).selectByAttribute("value", "2021-01-02");
      await click(DynamicDropdownPage.submit());

      await click(DynamicMutuallyExclusivePage.submit());
      await expect(await $(DynamicMutuallyExclusivePage.errorHeader()).getText()).toBe("There is a problem with your answer");
      await expect(await $(DynamicMutuallyExclusivePage.errorNumber(1)).getText()).toContain("Select at least one answer");
      await expect(await $(DynamicMutuallyExclusivePage.questionErrorPanel()).isExisting()).toBe(true);
    });
  });
});
