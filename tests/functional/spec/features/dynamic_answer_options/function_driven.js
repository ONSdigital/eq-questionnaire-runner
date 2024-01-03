import ReferenceDatePage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/reference-date.page";
import DynamicCheckboxPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/dynamic-checkbox.page";
import DynamicRadioPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/dynamic-radio.page";
import DynamicDropdownPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/dynamic-dropdown.page";
import DynamicMutuallyExclusivePage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/dynamic-mutually-exclusive.page";
import SubmitPage from "../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/submit.page";
import { click } from "../../../helpers";
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
    dropdownOptionValues,
  },
];

const openQuestionnaireAndSetUp = async (schema) => {
  await browser.openQuestionnaire(schema);
  // Set reference date
  await $(ReferenceDatePage.day()).setValue("1");
  await $(ReferenceDatePage.month()).setValue("1");
  await $(ReferenceDatePage.year()).setValue("2021");
  await click(ReferenceDatePage.submit());
};

testCases.forEach((testCase) => {
  describe(`Feature: Dynamically generated answer options driven by a function (${testCase.schemaName})`, () => {
    describe("Selecting/Deselecting", () => {
      before("Open questionnaire", async () => {
        await openQuestionnaireAndSetUp(testCase.schemaName);
      });

      describe("Given a dynamic answer options questionnaire and I am on a dynamic checkbox answer page", () => {
        it("When I click a checkbox option, then the checkbox should be selected", async () => {
          for (let i = 0; i < testCase.answerOptionCount; i++) {
            await $(DynamicCheckboxPage.answerByIndex(i)).click();
            await expect(await $(DynamicCheckboxPage.answerByIndex(i)).isSelected()).toBe(true);
          }
        });

        it("When I click a selected option, then it should be deselected", async () => {
          for (let i = 0; i < testCase.answerOptionCount; i++) {
            await $(DynamicCheckboxPage.answerByIndex(i)).click();
            await expect(await $(DynamicCheckboxPage.answerByIndex(i)).isSelected()).toBe(false);
          }
        });

        it("When I submit the page, then I should be taken to the next page", async () => {
          await click(DynamicCheckboxPage.submit());
          await expect(browser).toHaveUrlContaining(DynamicRadioPage.pageName);
        });
      });

      describe("Given a dynamic answer options questionnaire and I am on the radio answer page", () => {
        it("When I click a radio option, then the radio should be selected", async () => {
          for (let i = 0; i < (testCase.answerOptionCount); i++) {
            await $(DynamicRadioPage.answerByIndex(i)).click();
            await expect(await $(DynamicRadioPage.answerByIndex(i)).isSelected()).toBe(true);
          }
        });

        it("When I submit the page, then I should be taken to the next page", async () => {
          await click(DynamicRadioPage.submit());
          await expect(browser).toHaveUrlContaining(DynamicDropdownPage.pageName);
        });
      });

      describe("Given a dynamic answer options questionnaire and I am on the dropdown page", () => {
        it("When I select a dropdown option, then the option should be selected", async () => {
          for (const value of testCase.dropdownOptionValues) {
            await $(DynamicDropdownPage.answer()).selectByAttribute("value", value);
            await expect(await $(DynamicDropdownPage.answer()).getValue()).toBe(value);
          }
        });

        it("When I submit the page, then I should be taken to the next page", async () => {
          await click(DynamicDropdownPage.submit());
          await expect(browser).toHaveUrlContaining(DynamicMutuallyExclusivePage.pageName);
        });
      });

      describe("Given a dynamic answer options questionnaire and I am on the mutually exclusive page", () => {
        it("When I click a dynamic checkbox option, then the checkbox should be selected", async () => {
          for (let i = 0; i < (testCase.answerOptionCount); i++) {
            await $(DynamicMutuallyExclusivePage.answerByIndex(i)).click();
            await expect(await $(DynamicMutuallyExclusivePage.answerByIndex(i)).isSelected()).toBe(true);
          }
        });

        it("When I click a selected option, then it should be deselected", async () => {
          for (let i = 0; i < (testCase.answerOptionCount); i++) {
            await $(DynamicMutuallyExclusivePage.answerByIndex(i)).click();
            await expect(await $(DynamicMutuallyExclusivePage.answerByIndex(i)).isSelected()).toBe(false);
          }
        });

        it("When I click the static checkbox option, then the static checkbox should be selected", async () => {
          // Test exclusive option (Static option)
          await $(DynamicMutuallyExclusivePage.staticIDidNotWork()).click();
          await expect(await $(DynamicMutuallyExclusivePage.staticIDidNotWork()).isSelected()).toBe(true);
        });

        it("When I click the selected static checkbox option, then that checkbox should be deselected", async () => {
          // Test exclusive option (Static option)
          await $(DynamicMutuallyExclusivePage.staticIDidNotWork()).click();
          await expect(await $(DynamicMutuallyExclusivePage.staticIDidNotWork()).isSelected()).toBe(false);
        });
      });
    });

    describe("Summary page", () => {
      beforeEach("Open questionnaire", async () => {
        await openQuestionnaireAndSetUp(testCase.schemaName);
      });

      describe("Given a dynamic answer options questionnaire", () => {
        it("When I submit my questions without answering, then the summary should display `No answer provided` for each question", async () => {
          await click(DynamicCheckboxPage.submit());
          await click(DynamicRadioPage.submit());
          await click(DynamicRadioPage.submit());
          await click(DynamicMutuallyExclusivePage.submit());

          await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
          await expect(await $(SubmitPage.dynamicCheckboxAnswer()).getText()).toBe("No answer provided");
          await expect(await $(SubmitPage.dynamicRadioAnswer()).getText()).toBe("No answer provided");
          await expect(await $(SubmitPage.dynamicDropdownAnswer()).getText()).toBe("No answer provided");
          await expect(await $(SubmitPage.dynamicMutuallyExclusiveDynamicAnswer()).getText()).toBe("No answer provided");
        });

        it("When I select a dynamically generated answer option for each question, then my selected answers should be displayed on the summary", async () => {
          // Answer Checkbox
          await $(DynamicCheckboxPage.answerByIndex(2)).click(); // Wednesday 30 December 2020
          await $(DynamicCheckboxPage.answerByIndex(3)).click(); // Thursday 30 December 2020
          await click(DynamicCheckboxPage.submit());

          // Answer Radio
          await $(DynamicRadioPage.answerByIndex(1)).click(); // Tuesday 29 December 2020
          await click(DynamicRadioPage.submit());

          // Answer Dropdown
          await $(DynamicDropdownPage.answer()).selectByAttribute("value", "2021-01-02"); // Saturday 2 January 2021
          await click(DynamicDropdownPage.submit());

          // Answer Mutually exclusive
          await $(DynamicMutuallyExclusivePage.answerByIndex(0)).click(); //  Monday 28 December 2020
          await $(DynamicMutuallyExclusivePage.answerByIndex(6)).click(); //  Sunday 3 January 2021
          await click(DynamicMutuallyExclusivePage.submit());

          await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
          await expect(await $(SubmitPage.dynamicCheckboxAnswer()).getText()).toBe("Wednesday 30 December 2020\nThursday 31 December 2020");
          await expect(await $(SubmitPage.dynamicRadioAnswer()).getText()).toBe("Tuesday 29 December 2020");
          await expect(await $(SubmitPage.dynamicDropdownAnswer()).getText()).toBe("Saturday 2 January 2021");
          await expect(await $(SubmitPage.dynamicMutuallyExclusiveDynamicAnswer()).getText()).toBe("Monday 28 December 2020\nSunday 3 January 2021");
        });
      });
    });
  });
});

describe(`Feature: Dynamically generated answer options driven by a function with static options`, () => {
  describe("Given a dynamic answer options questionnaire with static options", () => {
    before("Open questionnaire", async () => {
      await openQuestionnaireAndSetUp("test_dynamic_answer_options_function_driven_with_static_options.json");
    });

    it("When I select a static answer option for each question, then my selected answer(s) should be displayed on the summary", async () => {
      // Answer Checkbox
      await $(DynamicCheckboxPage.answerByIndex(7)).click();
      await click(DynamicCheckboxPage.submit());

      // Answer Radio
      await $(DynamicRadioPage.answerByIndex(7)).click();
      await click(DynamicRadioPage.submit());

      // Answer Dropdown
      await $(DynamicDropdownPage.answer()).selectByAttribute("value", "I did not work");
      await click(DynamicDropdownPage.submit());

      // Answer Mutually exclusive

      // Test static option for mutually exclusive from non exclusive choices
      await $(DynamicMutuallyExclusivePage.answerByIndex(7)).click();
      await click(DynamicMutuallyExclusivePage.submit());
      await expect(await $(SubmitPage.dynamicMutuallyExclusiveDynamicAnswer()).getText()).toBe("None of the above");

      // Test exclusive static choice
      await $(SubmitPage.previous()).click();
      await $(DynamicMutuallyExclusivePage.staticIDidNotWork()).click();
      await click(DynamicMutuallyExclusivePage.submit());

      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
      await expect(await $(SubmitPage.dynamicCheckboxAnswer()).getText()).toBe("I did not work");
      await expect(await $(SubmitPage.dynamicRadioAnswer()).getText()).toBe("I did not work");
      await expect(await $(SubmitPage.dynamicDropdownAnswer()).getText()).toBe("I did not work");
      await expect(await $(SubmitPage.dynamicMutuallyExclusiveStaticAnswer()).getText()).toBe("I did not work");
    });

    it("When I edit and change the reference date which the other questions are dependent on, then all dependent answers are removed", async () => {
      await $(SubmitPage.referenceDateAnswerEdit()).click();
      await $(ReferenceDatePage.day()).setValue("2");
      await click(ReferenceDatePage.submit());

      await expect(await $(DynamicCheckboxPage.answerByIndex(7)).isSelected()).toBe(false);

      await $(DynamicCheckboxPage.answerByIndex(7)).click();
      await click(DynamicCheckboxPage.submit());

      await expect(await $(DynamicRadioPage.answerByIndex(7)).isSelected()).toBe(false);

      await $(DynamicRadioPage.answerByIndex(7)).click();
      await click(DynamicRadioPage.submit());

      await expect(await $(DynamicDropdownPage.answer()).getText()).toContain("Select an answer");

      await $(DynamicDropdownPage.answer()).selectByAttribute("value", "I did not work");
      await click(DynamicDropdownPage.submit());

      // The Mutually exclusive answer is not removed as it is a different answer_id to the dependent, however the block must be re-submitted
      await expect(await $(DynamicMutuallyExclusivePage.staticIDidNotWork()).isSelected()).toBe(true);
      await click(DynamicMutuallyExclusivePage.submit());

      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
    });
  });
});
