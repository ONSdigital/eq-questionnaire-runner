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

const openQuestionnaireAndSetUp = async (schema) => {
  await browser.openQuestionnaire(schema);
  // Set reference date
  await $(await ReferenceDatePage.day()).setValue("1");
  await $(await ReferenceDatePage.month()).setValue("1");
  await $(await ReferenceDatePage.year()).setValue("2021");
  await $(await ReferenceDatePage.submit()).click();
};

testCases.forEachasync (async (testCase) => {
  describe(`Feature: Dynamically generated answer options driven by a function (${testCase.schemaName})`, () => {
    describe("Selecting/Deselecting", () => {
      before("Open questionnaire", async ()=> {
        openQuestionnaireAndSetUp(testCase.schemaName);
      });

      describe("Given a dynamic answer options questionnaire and I am on a dynamic checkbox answer page", () => {
        it("When I click a checkbox option, then the checkbox should be selected", async ()=> {
          for (let i = 0; i < testCase.answerOptionCount; i++) {
            await $(await DynamicCheckboxPage.answerByIndex(i)).click();
            await expect(await $(await DynamicCheckboxPage.answerByIndex(i)).isSelected()).to.be.true;
          }
        });

        it("When I click a selected option, then it should be deselected", async ()=> {
          for (let i = 0; i < testCase.answerOptionCount; i++) {
            await $(await DynamicCheckboxPage.answerByIndex(i)).click();
            await expect(await $(await DynamicCheckboxPage.answerByIndex(i)).isSelected()).to.be.false;
          }
        });

        it("When I submit the page, then I should be taken to the next page", async ()=> {
          await $(await DynamicCheckboxPage.submit()).click();
          await expect(browser.getUrl()).to.contain(DynamicRadioPage.pageName);
        });
      });

      describe("Given a dynamic answer options questionnaire and I am on the radio answer page", () => {
        it("When I click a radio option, then the radio should be selected", async ()=> {
          for (let i = 0; i < testCase.answerOptionCount; i++) {
            await $(await DynamicRadioPage.answerByIndex(i)).click();
            await expect(await $(await DynamicRadioPage.answerByIndex(i)).isSelected()).to.be.true;
          }
        });

        it("When I submit the page, then I should be taken to the next page", async ()=> {
          await $(await DynamicRadioPage.submit()).click();
          await expect(browser.getUrl()).to.contain(DynamicDropdownPage.pageName);
        });
      });

      describe("Given a dynamic answer options questionnaire and I am on the dropdown page", () => {
        it("When I select a dropdown option, then the option should be selected", async ()=> {
          for (const value of testCase.dropdownOptionValues) {
            await $(await DynamicDropdownPage.answer()).selectByAttribute("value", value);
            await expect(await $(await DynamicDropdownPage.answer()).getValue()).to.equal(value);
          }
        });

        it("When I submit the page, then I should be taken to the next page", async ()=> {
          await $(await DynamicDropdownPage.submit()).click();
          await expect(browser.getUrl()).to.contain(DynamicMutuallyExclusivePage.pageName);
        });
      });

      describe("Given a dynamic answer options questionnaire and I am on the mutually exclusive page", () => {
        it("When I click a dynamic checkbox option, then the checkbox should be selected", async ()=> {
          for (let i = 0; i < testCase.answerOptionCount; i++) {
            await $(await DynamicMutuallyExclusivePage.answerByIndex(i)).click();
            await expect(await $(await DynamicMutuallyExclusivePage.answerByIndex(i)).isSelected()).to.be.true;
          }
        });

        it("When I click a selected option, then it should be deselected", async ()=> {
          for (let i = 0; i < testCase.answerOptionCount; i++) {
            await $(await DynamicMutuallyExclusivePage.answerByIndex(i)).click();
            await expect(await $(await DynamicMutuallyExclusivePage.answerByIndex(i)).isSelected()).to.be.false;
          }
        });

        it("When I click the static checkbox option, then the static checkbox should be selected", async ()=> {
          // Test exclusive option (Static option)
          await $(await DynamicMutuallyExclusivePage.staticIDidNotWork()).click();
          await expect(await $(await DynamicMutuallyExclusivePage.staticIDidNotWork()).isSelected()).to.be.true;
        });

        it("When I click the selected static checkbox option, then that checkbox should be deselected", async ()=> {
          // Test exclusive option (Static option)
          await $(await DynamicMutuallyExclusivePage.staticIDidNotWork()).click();
          await expect(await $(await DynamicMutuallyExclusivePage.staticIDidNotWork()).isSelected()).to.be.false;
        });
      });
    });

    describe("Summary page", () => {
      beforeEach("Open questionnaire", async ()=> {
        openQuestionnaireAndSetUp(testCase.schemaName);
      });

      describe("Given a dynamic answer options questionnaire", () => {
        it("When I submit my questions without answering, then the summary should display `No answer provided` for each question", async ()=> {
          await $(await DynamicCheckboxPage.submit()).click();
          await $(await DynamicRadioPage.submit()).click();
          await $(await DynamicRadioPage.submit()).click();
          await $(await DynamicMutuallyExclusivePage.submit()).click();

          await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
          await expect(await $(await SubmitPage.dynamicCheckboxAnswer()).getText()).to.equal("No answer provided");
          await expect(await $(await SubmitPage.dynamicRadioAnswer()).getText()).to.equal("No answer provided");
          await expect(await $(await SubmitPage.dynamicDropdownAnswer()).getText()).to.equal("No answer provided");
          await expect(await $(await SubmitPage.dynamicMutuallyExclusiveDynamicAnswer()).getText()).to.equal("No answer provided");
        });

        it("When I select a dynamically generated answer option for each question, then my selected answers should be displayed on the summary", async ()=> {
          // Answer Checkbox
          await $(await DynamicCheckboxPage.answerByIndex(2)).click(); // Wednesday 30 December 2020
          await $(await DynamicCheckboxPage.answerByIndex(3)).click(); // Thursday 30 December 2020
          await $(await DynamicCheckboxPage.submit()).click();

          // Answer Radio
          await $(await DynamicRadioPage.answerByIndex(1)).click(); // Tuesday 29 December 2020
          await $(await DynamicRadioPage.submit()).click();

          // Answer Dropdown
          await $(await DynamicDropdownPage.answer()).selectByAttribute("value", "2021-01-02"); // Saturday 2 January 2021
          await $(await DynamicDropdownPage.submit()).click();

          // Answer Mutually exclusive
          await $(await DynamicMutuallyExclusivePage.answerByIndex(0)).click(); //  Monday 28 December 2020
          await $(await DynamicMutuallyExclusivePage.answerByIndex(6)).click(); //  Sunday 3 January 2021
          await $(await DynamicMutuallyExclusivePage.submit()).click();

          await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
          await expect(await $(await SubmitPage.dynamicCheckboxAnswer()).getText()).to.equal("Wednesday 30 December 2020\nThursday 31 December 2020");
          await expect(await $(await SubmitPage.dynamicRadioAnswer()).getText()).to.equal("Tuesday 29 December 2020");
          await expect(await $(await SubmitPage.dynamicDropdownAnswer()).getText()).to.equal("Saturday 2 January 2021");
          await expect(await $(await SubmitPage.dynamicMutuallyExclusiveDynamicAnswer()).getText()).to.equal("Monday 28 December 2020\nSunday 3 January 2021");
        });
      });
    });
  });
});

describe(`Feature: Dynamically generated answer options driven by a function with static options`, () => {
  describe("Given a dynamic answer options questionnaire with static options", () => {
    before("Open questionnaire", async ()=> {
      openQuestionnaireAndSetUp("test_dynamic_answer_options_function_driven_with_static_options.json");
    });

    it("When I select a static answer option for each question, then my selected answer(s) should be displayed on the summary", async ()=> {
      // Answer Checkbox
      await $(await DynamicCheckboxPage.answerByIndex(7)).click();
      await $(await DynamicCheckboxPage.submit()).click();

      // Answer Radio
      await $(await DynamicRadioPage.answerByIndex(7)).click();
      await $(await DynamicRadioPage.submit()).click();

      // Answer Dropdown
      await $(await DynamicDropdownPage.answer()).selectByAttribute("value", "I did not work");
      await $(await DynamicDropdownPage.submit()).click();

      // Answer Mutually exclusive

      // Test static option for mutually exclusive from non exclusive choices
      await $(await DynamicMutuallyExclusivePage.answerByIndex(7)).click();
      await $(await DynamicMutuallyExclusivePage.submit()).click();
      await expect(await $(await SubmitPage.dynamicMutuallyExclusiveDynamicAnswer()).getText()).to.equal("None of the above");

      // Test exclusive static choice
      await $(await SubmitPage.previous()).click();
      await $(await DynamicMutuallyExclusivePage.staticIDidNotWork()).click();
      await $(await DynamicMutuallyExclusivePage.submit()).click();

      await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      await expect(await $(await SubmitPage.dynamicCheckboxAnswer()).getText()).to.equal("I did not work");
      await expect(await $(await SubmitPage.dynamicRadioAnswer()).getText()).to.equal("I did not work");
      await expect(await $(await SubmitPage.dynamicDropdownAnswer()).getText()).to.equal("I did not work");
      await expect(await $(await SubmitPage.dynamicMutuallyExclusiveStaticAnswer()).getText()).to.equal("I did not work");
    });

    it("When I edit and change the reference date which the other questions are dependent on, then all dependent answers are removed", async ()=> {
      await $(await SubmitPage.referenceDateAnswerEdit()).click();
      await $(await ReferenceDatePage.day()).setValue("2");
      await $(await ReferenceDatePage.submit()).click();

      await expect(await $(await DynamicCheckboxPage.answerByIndex(7)).isSelected()).to.be.false;

      await $(await DynamicCheckboxPage.answerByIndex(7)).click();
      await $(await DynamicCheckboxPage.submit()).click();

      await expect(await $(await DynamicRadioPage.answerByIndex(7)).isSelected()).to.be.false;

      await $(await DynamicRadioPage.answerByIndex(7)).click();
      await $(await DynamicRadioPage.submit()).click();

      await expect(await $(await DynamicDropdownPage.answer()).getText()).to.contain("Select an answer");

      await $(await DynamicDropdownPage.answer()).selectByAttribute("value", "I did not work");
      await $(await DynamicDropdownPage.submit()).click();

      // The Mutually exclusive answer is not removed as it is a different answer_id to the dependent, however the block must be re-submitted
      await expect(await $(await DynamicMutuallyExclusivePage.staticIDidNotWork()).isSelected()).to.be.true;
      await $(await DynamicMutuallyExclusivePage.submit()).click();

      await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });
});
