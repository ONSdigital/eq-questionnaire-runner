import AboutYou from "../../generated_pages/multiple_answers/about-you-block.page";

function answerAllButOne() {
  $(AboutYou.textfield()).setValue("John Doe");
  $(AboutYou.dateday()).setValue("1");
  $(AboutYou.datemonth()).setValue("1");
  $(AboutYou.dateyear()).setValue("1995");
  $(AboutYou.checkboxBmw()).click();
  $(AboutYou.radioYes()).click();
  $(AboutYou.currency()).setValue("50000");
  $(AboutYou.monthYearDateMonth()).setValue("10");
  $(AboutYou.monthYearDateYear()).setValue("2021");
  $(AboutYou.dropdown()).selectByAttribute("value", "Silver");
  $(AboutYou.unit()).setValue("10000");
  $(AboutYou.durationMonths()).setValue("3");
  $(AboutYou.durationYears()).setValue("3");
  $(AboutYou.yearDateYear()).setValue("2019");
  $(AboutYou.number()).setValue("5");
  $(AboutYou.percentage()).setValue("3");
  $(AboutYou.mobileNumber()).setValue("07700900111");
}

describe("Error Messages", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_multiple_answers.json");
  });

  it("Given a question has errors, When errors are displayed, Then the error messages are correct", () => {
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

    $(AboutYou.submit()).click();
    expect($(AboutYou.errorHeader()).getText()).to.equal("There are 14 problems with your answer");

    for (const [index, errorMessage] of Object.entries(errorMessageMap)) {
      expect($(AboutYou.errorNumber(index)).getText()).to.contain(errorMessage);
    }
  });

  it("Given a question has errors, When errors are displayed, Then the error message for each answer is correct", () => {
    $(AboutYou.submit()).click();

    expect($(AboutYou.textfieldErrorItem()).getText()).to.equal("Enter an answer");
    expect($(AboutYou.dateErrorItem()).getText()).to.equal("Enter a date");
    expect($(AboutYou.checkboxErrorItem()).getText()).to.contain("Select at least one answer");
    expect($(AboutYou.radioErrorItem()).getText()).to.contain("Select an answer");
    expect($(AboutYou.currencyErrorItem()).getText()).to.equal("Enter an answer");
    expect($(AboutYou.monthYearDateErrorItem()).getText()).to.equal("Enter a date");
    expect($(AboutYou.dropdownErrorItem()).getText()).to.equal("Select an answer");
    expect($(AboutYou.unitErrorItem()).getText()).to.equal("Enter an answer");
    expect($(AboutYou.durationErrorItem()).getText()).to.equal("Enter a duration");
    expect($(AboutYou.yearDateErrorItem()).getText()).to.equal("Enter a date");
    expect($(AboutYou.numberErrorItem()).getText()).to.equal("Enter an answer");
    expect($(AboutYou.percentageErrorItem()).getText()).to.equal("Enter an answer");
    expect($(AboutYou.mobileNumberErrorItem()).getText()).to.equal("Enter a UK mobile number");
    expect($(AboutYou.textareaErrorItem()).getText()).to.equal("Enter an answer");
  });

  it("Given a question has 1 error, When the error is displayed, Then error header is correct", () => {
    answerAllButOne();

    $(AboutYou.submit()).click();
    expect($(AboutYou.errorHeader()).getText()).to.equal("There is a problem with your answer");
  });

  it("Given a question has errors, When an error message is clicked, Then the correct answer is focused", () => {
    $(AboutYou.submit()).click();

    $(AboutYou.errorNumber(1)).click();
    expect($(AboutYou.textfield()).isFocused()).to.be.true;

    $(AboutYou.errorNumber(2)).click();
    expect($(AboutYou.dateday()).isFocused()).to.be.true;

    $(AboutYou.errorNumber(3)).click();
    expect($(AboutYou.checkboxBmw()).isFocused()).to.be.true;

    $(AboutYou.errorNumber(4)).click();
    expect($(AboutYou.radioYes()).isFocused()).to.be.true;

    $(AboutYou.errorNumber(5)).click();
    expect($(AboutYou.currency()).isFocused()).to.be.true;

    $(AboutYou.errorNumber(6)).click();
    expect($(AboutYou.monthYearDateMonth()).isFocused()).to.be.true;

    $(AboutYou.errorNumber(7)).click();
    expect($(AboutYou.dropdown()).isFocused()).to.be.true;

    $(AboutYou.errorNumber(8)).click();
    expect($(AboutYou.unit()).isFocused()).to.be.true;

    $(AboutYou.errorNumber(9)).click();
    expect($(AboutYou.durationYears()).isFocused()).to.be.true;

    $(AboutYou.errorNumber(10)).click();
    expect($(AboutYou.yearDateYear()).isFocused()).to.be.true;

    $(AboutYou.errorNumber(11)).click();
    expect($(AboutYou.number()).isFocused()).to.be.true;

    $(AboutYou.errorNumber(12)).click();
    expect($(AboutYou.percentage()).isFocused()).to.be.true;

    $(AboutYou.errorNumber(13)).click();
    expect($(AboutYou.mobileNumber()).isFocused()).to.be.true;

    $(AboutYou.errorNumber(14)).click();
    expect($(AboutYou.textarea()).isFocused()).to.be.true;
  });
});
