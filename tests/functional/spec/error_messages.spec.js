import AboutYou from "../generated_pages/multiple_answers/about-you-block.page";
import BlockPage from "../generated_pages/percentage/block.page";
import { click } from "../helpers";

async function answerAllButOne() {
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
}

describe("Error Messages", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_multiple_answers.json");
  });

  it("Given a question has errors, When errors are displayed, Then the error messages are correct", async () => {
    const errorMessageMap = {
      1: "Enter an answer",
      2: "Enter a date",
      3: "Select at least one answer",
      4: "Select an answer",
      5: "Enter an answer",
      6: "Enter a date",
      7: "Select an answer",
      8: "Enter an answer",
      9: "Enter a duration",
      10: "Enter a date",
      11: "Enter an answer",
      12: "Enter an answer",
      13: "Enter a UK mobile number",
      14: "Enter an answer",
    };

    await click(AboutYou.submit());
    await expect(await $(AboutYou.errorHeader()).getText()).to.equal("There are 14 problems with your answer");

    for (const [index, errorMessage] of Object.entries(errorMessageMap)) {
      await expect(await $(AboutYou.errorNumber(index)).getText()).to.contain(errorMessage);
    }
  });

  it("Given a question has errors, When errors are displayed, Then the error message for each answer is correct", async () => {
    await click(AboutYou.submit());

    await expect(await $(AboutYou.textfieldErrorItem()).getText()).to.equal("Enter an answer");
    await expect(await $(AboutYou.dateErrorItem()).getText()).to.equal("Enter a date");
    await expect(await $(AboutYou.checkboxErrorItem()).getText()).to.contain("Select at least one answer");
    await expect(await $(AboutYou.radioErrorItem()).getText()).to.contain("Select an answer");
    await expect(await $(AboutYou.currencyErrorItem()).getText()).to.equal("Enter an answer");
    await expect(await $(AboutYou.monthYearDateErrorItem()).getText()).to.equal("Enter a date");
    await expect(await $(AboutYou.dropdownErrorItem()).getText()).to.equal("Select an answer");
    await expect(await $(AboutYou.unitErrorItem()).getText()).to.equal("Enter an answer");
    await expect(await $(AboutYou.durationErrorItem()).getText()).to.equal("Enter a duration");
    await expect(await $(AboutYou.yearDateErrorItem()).getText()).to.equal("Enter a date");
    await expect(await $(AboutYou.numberErrorItem()).getText()).to.equal("Enter an answer");
    await expect(await $(AboutYou.percentageErrorItem()).getText()).to.equal("Enter an answer");
    await expect(await $(AboutYou.mobileNumberErrorItem()).getText()).to.equal("Enter a UK mobile number");
    await expect(await $(AboutYou.textareaErrorItem()).getText()).to.equal("Enter an answer");
  });

  it("Given a question has multiple errors, When the errors are displayed, Then the error messages are in a numbered list", async () => {
    await click(AboutYou.submit());
    await expect(await $(AboutYou.errorList()).isDisplayed()).to.be.true;
  });

  it("Given a question has 1 error, When the error is displayed, Then error message isn't in a numbered list", async () => {
    await answerAllButOne();

    await click(AboutYou.submit());
    await expect(await $(AboutYou.singleErrorLink()).isDisplayed()).to.be.true;
  });

  it("Given a question has 1 error, When the error is displayed, Then error header is correct", async () => {
    await answerAllButOne();

    await click(AboutYou.submit());
    await expect(await $(AboutYou.errorHeader()).getText()).to.equal("There is a problem with your answer");
  });

  it("Given a question has errors, When an error message is clicked, Then the correct answer is focused", async () => {
    await click(AboutYou.submit());

    await $(AboutYou.errorNumber(1)).click();
    await expect(await $(AboutYou.textfield()).isFocused()).to.be.true;

    await $(AboutYou.errorNumber(2)).click();
    await expect(await $(AboutYou.dateday()).isFocused()).to.be.true;

    await $(AboutYou.errorNumber(3)).click();
    await expect(await $(AboutYou.checkboxBmw()).isFocused()).to.be.true;

    await $(AboutYou.errorNumber(4)).click();
    await expect(await $(AboutYou.radioYes()).isFocused()).to.be.true;

    await $(AboutYou.errorNumber(5)).click();
    await expect(await $(AboutYou.currency()).isFocused()).to.be.true;

    await $(AboutYou.errorNumber(6)).click();
    await expect(await $(AboutYou.monthYearDateMonth()).isFocused()).to.be.true;

    await $(AboutYou.errorNumber(7)).click();
    await expect(await $(AboutYou.dropdown()).isFocused()).to.be.true;

    await $(AboutYou.errorNumber(8)).click();
    await expect(await $(AboutYou.unit()).isFocused()).to.be.true;

    await $(AboutYou.errorNumber(9)).click();
    await expect(await $(AboutYou.durationYears()).isFocused()).to.be.true;

    await $(AboutYou.errorNumber(10)).click();
    await expect(await $(AboutYou.yearDateYear()).isFocused()).to.be.true;

    await $(AboutYou.errorNumber(11)).click();
    await expect(await $(AboutYou.number()).isFocused()).to.be.true;

    await $(AboutYou.errorNumber(12)).click();
    await expect(await $(AboutYou.percentage()).isFocused()).to.be.true;

    await $(AboutYou.errorNumber(13)).click();
    await expect(await $(AboutYou.mobileNumber()).isFocused()).to.be.true;

    await $(AboutYou.errorNumber(14)).click();
    await expect(await $(AboutYou.textarea()).isFocused()).to.be.true;
  });
});
describe("Error Message NaN value", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_percentage.json");
  });
  it("Given a NaN value was entered on percentage question, When the error is displayed, Then the error message is correct", async () => {
    await $(BlockPage.answer()).setValue("NaN");
    await click(BlockPage.submit());
    await expect(await $(BlockPage.errorHeader()).getText()).to.equal("There is a problem with your answer");
    await expect(await $(BlockPage.answerErrorItem()).getText()).to.equal("Enter a number");
  });
  it("Given a NaN value with separators was entered on percentage question, When the error is displayed, Then the error message is correct", async () => {
    await $(BlockPage.answer()).setValue(",NaN_");
    await click(BlockPage.submit());
    await expect(await $(BlockPage.errorHeader()).getText()).to.equal("There is a problem with your answer");
    await expect(await $(BlockPage.answerErrorItem()).getText()).to.equal("Enter a number");
  });
});
