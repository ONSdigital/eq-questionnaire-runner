import AboutYou from "../generated_pages/multiple_answers/about-you-block.page";
import AgeBlock from "../generated_pages/multiple_answers/age-block.page";
import SubmitPage from "../generated_pages/multiple_answers/submit.page.js";
import { click } from "../helpers";

async function answerAllQuestions() {
  await $(AboutYou.textfield()).setValue("John Doe");
  await $(AboutYou.dateday()).setValue("1");
  await $(AboutYou.datemonth()).setValue("1");
  await $(AboutYou.dateyear()).setValue("1995");
  await $(AboutYou.checkboxBmw()).click();
  await $(AboutYou.radioYes()).click();
  await $(AboutYou.currency()).setValue("50000");
  await $(AboutYou.monthYearDateMonth()).setValue("10");
  await $(AboutYou.monthYearDateYear()).setValue("2021");
  await $(AboutYou.dropdown()).selectByAttribute("value", "Silver");
  await $(AboutYou.unit()).setValue("10000");
  await $(AboutYou.durationMonths()).setValue("3");
  await $(AboutYou.durationYears()).setValue("3");
  await $(AboutYou.yearDateYear()).setValue("2019");
  await $(AboutYou.number()).setValue("5");
  await $(AboutYou.percentage()).setValue("3");
  await $(AboutYou.mobileNumber()).setValue("07700900111");
  await $(AboutYou.textarea()).setValue("Fuel type petrol");
  await click(AboutYou.submit());

  await $(AgeBlock.age()).setValue("10");
  await $(AgeBlock.ageEstimateThisAgeIsAnEstimate()).click();
  await click(AgeBlock.submit());
}

describe("Multiple Answers", () => {
  describe("Given I have completed a questionnaire that has multiple answers per question", () => {
    beforeEach("Load the questionnaire and answer all questions", async () => {
      await browser.openQuestionnaire("test_multiple_answers.json");
      await answerAllQuestions();
    });

    it("When I am on the summary, Then all answers are displayed", async () => {
      await expect(await $(SubmitPage.textfieldAnswer()).getText()).toBe("John Doe");
      await expect(await $(SubmitPage.dateAnswer()).getText()).toBe("1 January 1995");
      await expect(await $(SubmitPage.checkboxAnswer()).getText()).toBe("BMW");
      await expect(await $(SubmitPage.radioAnswer()).getText()).toBe("Yes");
      await expect(await $(SubmitPage.currencyAnswer()).getText()).toBe("£50,000.00");
      await expect(await $(SubmitPage.monthYearDateAnswer()).getText()).toBe("October 2021");
      await expect(await $(SubmitPage.dropdownAnswer()).getText()).toBe("Silver");
      await expect(await $(SubmitPage.unitAnswer()).getText()).toBe("10,000 mi");
      await expect(await $(SubmitPage.durationAnswer()).getText()).toBe("3 years 3 months");
      await expect(await $(SubmitPage.yearDateAnswer()).getText()).toBe("2019");
      await expect(await $(SubmitPage.numberAnswer()).getText()).toBe("5");
      await expect(await $(SubmitPage.percentageAnswer()).getText()).toBe("3%");
      await expect(await $(SubmitPage.mobileNumberAnswer()).getText()).toBe("07700900111");
      await expect(await $(SubmitPage.textareaAnswer()).getText()).toBe("Fuel type petrol");

      await expect(await $(SubmitPage.ageAnswer()).getText()).toBe("10");
      await expect(await $(SubmitPage.ageEstimateAnswer()).getText()).toBe("This age is an estimate");
    });

    it("When I click 'Change' an answer, Then I should be taken to the correct page and the answer input should be focused", async () => {
      await $(SubmitPage.currencyAnswerEdit()).click();
      await expect(browser).toHaveUrlContaining(AboutYou.url());
      await expect(browser).toHaveUrlContaining(AboutYou.currency());
      await expect(await $(AboutYou.currency()).isFocused()).toBe(true);
    });
  });

  describe("Given I have launched a questionnaire that has multiple answers per question", () => {
    beforeEach("Load the questionnaire", async () => {
      await browser.openQuestionnaire("test_multiple_answers.json");
    });

    it("When I am on the question page, Then all answers should have a label/legend", async () => {
      await expect(await $(AboutYou.dateLegend()).getText()).toBe("What is your date of birth?");
      await expect(await $(AboutYou.monthYearDateLegend()).getText()).toBe("When would you like the car by?");
      await expect(await $(AboutYou.radioLegend()).getText()).toBe("Would you like the sports package?");
      await expect(await $(AboutYou.durationLegend()).getText()).toBe("How long have you had your licence?");
      await expect(await $(AboutYou.checkboxLegend()).getText()).toBe("What are your favourite car brands?");
      await expect(await $(AboutYou.textfieldLabel()).getText()).toBe("Your name");
      await expect(await $(AboutYou.currencyLabel()).getText()).toBe("What is your budget?");
      await expect(await $(AboutYou.dropdownLabel()).getText()).toBe("Select a colour");
      await expect(await $(AboutYou.unitLabel()).getText()).toBe("Max mileage");
      await expect(await $(AboutYou.numberLabel()).getText()).toBe("How many seats?");
      await expect(await $(AboutYou.percentageLabel()).getText()).toBe("Max CO2 emissions");
      await expect(await $(AboutYou.mobileNumberLabel()).getText()).toBe("What is your mobile number?");
      await expect(await $(AboutYou.textareaLabel()).getText()).toBe("Other comments");
    });
  });
});
