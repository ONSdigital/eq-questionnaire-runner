import ReferenceDatePage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/reference-date.page";
import DynamicCheckboxPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/dynamic-checkbox.page";
import DynamicRadioPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/dynamic-radio.page";
import DynamicDropdownPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/dynamic-dropdown.page";
import DynamicMutuallyExclusivePage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/dynamic-mutually-exclusive.page";
import SubmitPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/submit.page";

const dropdownOptionValues = ["2020-12-28", "2020-12-29", "2020-12-30", "2020-12-31", "2021-01-01", "2021-01-02", "2021-01-03"];
const dropdownOptionValuesWithStaticOption = [...dropdownOptionValues, "I did not work"];

const testCases = [
  {
    schemaName: "test_dynamic_answer_options_function_driven_with_static_options.json",
    answerOptionCount: 8,
    dropdownOptionValues: dropdownOptionValuesWithStaticOption,
  },
  {
    schemaName: "test_dynamic_answer_options_function_driven.json",
    answerOptionCount: 7,
    dropdownOptionValues: dropdownOptionValues,
  },
];

const openQuestionnaireAndSetUp = (schema) => {
  browser.openQuestionnaire(schema);
  // Set reference date
  $(ReferenceDatePage.day()).setValue("1");
  $(ReferenceDatePage.month()).setValue("1");
  $(ReferenceDatePage.year()).setValue("2021");
  $(ReferenceDatePage.submit()).click();
};

testCases.forEach((testCase) => {
  describe(`Feature: Dynamically generated answer options driven by a function (${testCase.schemaName})`, () => {
    describe("Selecting/Deselecting", () => {
      before("Open questionnaire", () => {
        openQuestionnaireAndSetUp(testCase.schemaName);
      });

      describe("Given a dynamic answer options questionnaire and I am on a dynamic checkbox answer page", () => {
        it("When I click a checkbox option, then the checkbox should be selected", () => {
          for (let i = 0; i < testCase.answerOptionCount; i++) {
            $(DynamicCheckboxPage.answerByIndex(i)).click();
            expect($(DynamicCheckboxPage.answerByIndex(i)).isSelected()).to.be.true;
          }
        });

        it("When I click a selected option, then it should be deselected", () => {
          for (let i = 0; i < testCase.answerOptionCount; i++) {
            $(DynamicCheckboxPage.answerByIndex(i)).click();
            expect($(DynamicCheckboxPage.answerByIndex(i)).isSelected()).to.be.false;
          }
        });

        it("When I submit the page, then I should be taken to the next page", () => {
          $(DynamicCheckboxPage.submit()).click();
          expect(browser.getUrl()).to.contain(DynamicRadioPage.pageName);
        });
      });

      describe("Given a dynamic answer options questionnaire and I am on the radio answer page", () => {
        it("When I click a radio option, then the radio should be selected", () => {
          for (let i = 0; i < testCase.answerOptionCount; i++) {
            $(DynamicRadioPage.answerByIndex(i)).click();
            expect($(DynamicRadioPage.answerByIndex(i)).isSelected()).to.be.true;
          }
        });

        it("When I submit the page, then I should be taken to the next page", () => {
          $(DynamicRadioPage.submit()).click();
          expect(browser.getUrl()).to.contain(DynamicDropdownPage.pageName);
        });
      });

      describe("Given a dynamic answer options questionnaire and I am on the dropdown page", () => {
        it("When I select a dropdown option, then the option should be selected", () => {
          for (const value of testCase.dropdownOptionValues) {
            $(DynamicDropdownPage.answer()).selectByAttribute("value", value);
            expect($(DynamicDropdownPage.answer()).getValue()).to.equal(value);
          }
        });

        it("When I submit the page, then I should be taken to the next page", () => {
          $(DynamicDropdownPage.submit()).click();
          expect(browser.getUrl()).to.contain(DynamicMutuallyExclusivePage.pageName);
        });
      });

      describe("Given a dynamic answer options questionnaire and I am on the mutually exclusive page", () => {
        it("When I click a dynamic checkbox option, then the checkbox should be selected", () => {
          for (let i = 0; i < testCase.answerOptionCount; i++) {
            $(DynamicMutuallyExclusivePage.answerByIndex(i)).click();
            expect($(DynamicMutuallyExclusivePage.answerByIndex(i)).isSelected()).to.be.true;
          }
        });

        it("When I click a selected option, then it should be deselected", () => {
          for (let i = 0; i < testCase.answerOptionCount; i++) {
            $(DynamicMutuallyExclusivePage.answerByIndex(i)).click();
            expect($(DynamicMutuallyExclusivePage.answerByIndex(i)).isSelected()).to.be.false;
          }
        });

        it("When I click the static checkbox option, then the static checkbox should be selected", () => {
          // Test exclusive option (Static option)
          $(DynamicMutuallyExclusivePage.staticIDidNotWork()).click();
          expect($(DynamicMutuallyExclusivePage.staticIDidNotWork()).isSelected()).to.be.true;
        });

        it("When I click the selected static checkbox option, then that checkbox should be deselected", () => {
          // Test exclusive option (Static option)
          $(DynamicMutuallyExclusivePage.staticIDidNotWork()).click();
          expect($(DynamicMutuallyExclusivePage.staticIDidNotWork()).isSelected()).to.be.false;
        });
      });
    });

    describe("Summary page", () => {
      beforeEach("Open questionnaire", () => {
        openQuestionnaireAndSetUp(testCase.schemaName);
      });

      describe("Given a dynamic answer options questionnaire", () => {
        it("When I submit my questions without answering, then the summary should display `No answer provided` for each question", () => {
          $(DynamicCheckboxPage.submit()).click();
          $(DynamicRadioPage.submit()).click();
          $(DynamicRadioPage.submit()).click();
          $(DynamicMutuallyExclusivePage.submit()).click();

          expect(browser.getUrl()).to.contain(SubmitPage.pageName);
          expect($(SubmitPage.dynamicCheckboxAnswer()).getText()).to.equal("No answer provided");
          expect($(SubmitPage.dynamicRadioAnswer()).getText()).to.equal("No answer provided");
          expect($(SubmitPage.dynamicDropdownAnswer()).getText()).to.equal("No answer provided");
          expect($(SubmitPage.dynamicMutuallyExclusiveDynamicAnswer()).getText()).to.equal("No answer provided");
        });

        it("When I select a dynamically generated answer option for each question, then my selected answers should be displayed on the summary", () => {
          // Answer Checkbox
          $(DynamicCheckboxPage.answerByIndex(2)).click(); // Wednesday 30 December 2020
          $(DynamicCheckboxPage.answerByIndex(3)).click(); // Thursday 30 December 2020
          $(DynamicCheckboxPage.submit()).click();

          // Answer Radio
          $(DynamicRadioPage.answerByIndex(1)).click(); // Tuesday 29 December 2020
          $(DynamicRadioPage.submit()).click();

          // Answer Dropdown
          $(DynamicDropdownPage.answer()).selectByAttribute("value", "2021-01-02"); // Saturday 2 January 2021
          $(DynamicDropdownPage.submit()).click();

          // Answer Mutually exclusive
          $(DynamicMutuallyExclusivePage.answerByIndex(0)).click(); //  Monday 28 December 2020
          $(DynamicMutuallyExclusivePage.answerByIndex(6)).click(); //  Sunday 3 January 2021
          $(DynamicMutuallyExclusivePage.submit()).click();

          expect(browser.getUrl()).to.contain(SubmitPage.pageName);
          expect($(SubmitPage.dynamicCheckboxAnswer()).getText()).to.equal("Wednesday 30 December 2020\nThursday 31 December 2020");
          expect($(SubmitPage.dynamicRadioAnswer()).getText()).to.equal("Tuesday 29 December 2020");
          expect($(SubmitPage.dynamicDropdownAnswer()).getText()).to.equal("Saturday 2 January 2021");
          expect($(SubmitPage.dynamicMutuallyExclusiveDynamicAnswer()).getText()).to.equal("Monday 28 December 2020\nSunday 3 January 2021");
        });
      });
    });
  });
});

describe(`Feature: Dynamically generated answer options driven by a function with static options`, () => {
  describe("Given a dynamic answer options questionnaire with static options", () => {
    beforeEach("Open questionnaire", () => {
      openQuestionnaireAndSetUp("test_dynamic_answer_options_function_driven_with_static_options.json");
    });

    it("When I select a static answer option for each question, then my selected answer(s) should be displayed on the summary", () => {
      // Answer Checkbox
      $(DynamicCheckboxPage.answerByIndex(7)).click();
      $(DynamicCheckboxPage.submit()).click();

      // Answer Radio
      $(DynamicRadioPage.answerByIndex(7)).click();
      $(DynamicRadioPage.submit()).click();

      // Answer Dropdown
      $(DynamicDropdownPage.answer()).selectByAttribute("value", "I did not work");
      $(DynamicDropdownPage.submit()).click();

      // Answer Mutually exclusive

      // Test static option for mutually exclusive from non exclusive choices
      $(DynamicMutuallyExclusivePage.answerByIndex(7)).click();
      $(DynamicMutuallyExclusivePage.submit()).click();
      expect($(SubmitPage.dynamicMutuallyExclusiveDynamicAnswer()).getText()).to.equal("None of the above");

      // Test exclusive static choice
      $(SubmitPage.previous()).click();
      $(DynamicMutuallyExclusivePage.staticIDidNotWork()).click();
      $(DynamicMutuallyExclusivePage.submit()).click();

      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      expect($(SubmitPage.dynamicCheckboxAnswer()).getText()).to.equal("I did not work");
      expect($(SubmitPage.dynamicRadioAnswer()).getText()).to.equal("I did not work");
      expect($(SubmitPage.dynamicDropdownAnswer()).getText()).to.equal("I did not work");
      expect($(SubmitPage.dynamicMutuallyExclusiveStaticAnswer()).getText()).to.equal("I did not work");
    });
  });
});
