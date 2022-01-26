import ReferenceDatePage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/reference-date.page";
import DynamicCheckboxPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-checkbox.page";
import DynamicRadioPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-radio.page";
import DynamicDropdownPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-dropdown.page";
import DynamicMutuallyExclusivePage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-mutually-exclusive.page";

describe(`Feature: Dynamically generated mandatory answer options driven by a function with static options`, () => {
  describe("Given a mandatory dynamic answer options questionnaire with static options", () => {
    before("Open questionnaire", () => {
      browser.openQuestionnaire("test_dynamic_answer_options_function_driven_with_static_options_mandatory.json");
      // Set reference date
      $(ReferenceDatePage.day()).setValue("1");
      $(ReferenceDatePage.month()).setValue("1");
      $(ReferenceDatePage.year()).setValue("2021");
      $(ReferenceDatePage.submit()).click();
    });

    it("When I do not answer the Checkbox question and submit, then an error message and the question error panel should be displayed.", () => {
      $(DynamicCheckboxPage.submit()).click();
      expect($(DynamicCheckboxPage.errorHeader()).getText()).to.contain("There is a problem with your answer");
      expect($(DynamicCheckboxPage.answerErrorItem()).getText()).to.contain("Select at least one answer");
      expect($(DynamicCheckboxPage.questionErrorPanel()).isExisting()).to.be.true;
    });

    it("When I do not answer the Radio question and submit, then an error message and the question error panel should be displayed.", () => {
      // Get to Radio question
      $(DynamicCheckboxPage.answerByIndex(0)).click();
      $(DynamicCheckboxPage.submit()).click();

      $(DynamicRadioPage.submit()).click();
      expect($(DynamicRadioPage.errorHeader()).getText()).to.contain("There is a problem with your answer");
      expect($(DynamicRadioPage.answerErrorItem()).getText()).to.contain("Select an answer");
      expect($(DynamicRadioPage.questionErrorPanel()).isExisting()).to.be.true;
    });

    it("When I do not answer the Dropdown question and submit, then an error message and the question error panel should be displayed.", () => {
      // Get to Dropdown question
      $(DynamicRadioPage.answerByIndex(0)).click();
      $(DynamicRadioPage.submit()).click();

      $(DynamicDropdownPage.submit()).click();
      expect($(DynamicDropdownPage.errorHeader()).getText()).to.contain("There is a problem with your answer");
      expect($(DynamicDropdownPage.answerErrorItem()).getText()).to.contain("Select an answer");
      expect($(DynamicDropdownPage.questionErrorPanel()).isExisting()).to.be.true;
    });

    it("When I do not answer the Mutually Exclusive Checkbox question and submit, then an error message and the question error panel should be displayed.", () => {
      // Get to Mutually Exclusive question
      $(DynamicDropdownPage.answer()).selectByAttribute("value", "2021-01-02");
      $(DynamicDropdownPage.submit()).click();

      $(DynamicMutuallyExclusivePage.submit()).click();
      expect($(DynamicMutuallyExclusivePage.errorHeader()).getText()).to.contain("There is a problem with your answer");
      expect($(DynamicMutuallyExclusivePage.errorNumber(1)).getText()).to.contain("Select at least one answer");
      expect($(DynamicMutuallyExclusivePage.questionErrorPanel()).isExisting()).to.be.true;
    });
  });
});
