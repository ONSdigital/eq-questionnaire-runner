import ReferenceDatePage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/reference-date.page";
import DynamicCheckboxPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-checkbox.page";
import DynamicRadioPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-radio.page";
import DynamicDropdownPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-dropdown.page";
import DynamicMutuallyExclusivePage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-mutually-exclusive.page";

describe(`Feature: Dynamically generated mandatory answer options driven by a function with static options`, () => {
  describe("Given a mandatory dynamic answer options questionnaire with static options", () => {
    before("Open questionnaire", async ()=> {
      await browser.openQuestionnaire("test_dynamic_answer_options_function_driven_with_static_options_mandatory.json");
      // Set reference date
      await $(ReferenceDatePage.day()).setValue("1");
      await $(ReferenceDatePage.month()).setValue("1");
      await $(ReferenceDatePage.year()).setValue("2021");
      await $(ReferenceDatePage.submit()).click();
    });

    it("When I do not answer the Checkbox question and submit, then an error message and the question error panel should be displayed.", async ()=> {
      await $(DynamicCheckboxPage.submit()).click();
      await expect(await $(DynamicCheckboxPage.errorHeader()).getText()).to.contain("There is a problem with your answer");
      await expect(await $(DynamicCheckboxPage.answerErrorItem()).getText()).to.contain("Select at least one answer");
      await expect(await $(DynamicCheckboxPage.questionErrorPanel()).isExisting()).to.be.true;
    });

    it("When I do not answer the Radio question and submit, then an error message and the question error panel should be displayed.", async ()=> {
      // Get to Radio question
      await $(DynamicCheckboxPage.answerByIndex(0)).click();
      await $(DynamicCheckboxPage.submit()).click();

      await $(DynamicRadioPage.submit()).click();
      await expect(await $(DynamicRadioPage.errorHeader()).getText()).to.contain("There is a problem with your answer");
      await expect(await $(DynamicRadioPage.answerErrorItem()).getText()).to.contain("Select an answer");
      await expect(await $(DynamicRadioPage.questionErrorPanel()).isExisting()).to.be.true;
    });

    it("When I do not answer the Dropdown question and submit, then an error message and the question error panel should be displayed.", async ()=> {
      // Get to Dropdown question
      await $(DynamicRadioPage.answerByIndex(0)).click();
      await $(DynamicRadioPage.submit()).click();

      await $(DynamicDropdownPage.submit()).click();
      await expect(await $(DynamicDropdownPage.errorHeader()).getText()).to.contain("There is a problem with your answer");
      await expect(await $(DynamicDropdownPage.answerErrorItem()).getText()).to.contain("Select an answer");
      await expect(await $(DynamicDropdownPage.questionErrorPanel()).isExisting()).to.be.true;
    });

    it("When I do not answer the Mutually Exclusive Checkbox question and submit, then an error message and the question error panel should be displayed.", async ()=> {
      // Get to Mutually Exclusive question
      await $(DynamicDropdownPage.answer()).selectByAttribute("value", "2021-01-02");
      await $(DynamicDropdownPage.submit()).click();

      await $(DynamicMutuallyExclusivePage.submit()).click();
      await expect(await $(DynamicMutuallyExclusivePage.errorHeader()).getText()).to.contain("There is a problem with your answer");
      await expect(await $(DynamicMutuallyExclusivePage.errorNumber(1)).getText()).to.contain("Select at least one answer");
      await expect(await $(DynamicMutuallyExclusivePage.questionErrorPanel()).isExisting()).to.be.true;
    });
  });
});
