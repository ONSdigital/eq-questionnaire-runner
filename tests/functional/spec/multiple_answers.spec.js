import AboutYou from "../generated_pages/multiple_answers/about-you-block.page";
import AgeBlock from "../generated_pages/multiple_answers/age-block.page";
import SubmitPage from "../generated_pages/multiple_answers/submit.page.js";

function answerAllQuestions() {
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
  $(AboutYou.textarea()).setValue("Fuel type petrol");
  $(AboutYou.submit()).click();

  $(AgeBlock.age()).setValue("10");
  $(AgeBlock.ageEstimateThisAgeIsAnEstimate()).click();
  $(AgeBlock.submit()).click();
}

describe("Multiple Answers", () => {
  describe("Given I have completed a questionnaire that has multiple answers per question", () => {
    beforeEach("Load the questionnaire and answer all questions", () => {
      browser.openQuestionnaire("test_multiple_answers.json");
      answerAllQuestions();
    });

    it("When I am on the summary, Then all answers are displayed", () => {
      expect($(SubmitPage.textfieldAnswer()).getText()).to.equal("John Doe");
      expect($(SubmitPage.dateAnswer()).getText()).to.equal("1 January 1995");
      expect($(SubmitPage.checkboxAnswer()).getText()).to.equal("BMW");
      expect($(SubmitPage.radioAnswer()).getText()).to.equal("Yes");
      expect($(SubmitPage.currencyAnswer()).getText()).to.equal("£50,000.00");
      expect($(SubmitPage.monthYearDateAnswer()).getText()).to.equal("October 2021");
      expect($(SubmitPage.dropdownAnswer()).getText()).to.equal("Silver");
      expect($(SubmitPage.unitAnswer()).getText()).to.equal("10,000 mi");
      expect($(SubmitPage.durationAnswer()).getText()).to.equal("3 years 3 months");
      expect($(SubmitPage.yearDateAnswer()).getText()).to.equal("2019");
      expect($(SubmitPage.numberAnswer()).getText()).to.equal("5");
      expect($(SubmitPage.percentageAnswer()).getText()).to.equal("3%");
      expect($(SubmitPage.mobileNumberAnswer()).getText()).to.equal("07700900111");
      expect($(SubmitPage.textareaAnswer()).getText()).to.equal("Fuel type petrol");

      expect($(SubmitPage.ageAnswer()).getText()).to.equal("10");
      expect($(SubmitPage.ageEstimateAnswer()).getText()).to.equal("This age is an estimate");
    });

    it("When I click 'Change' an answer, Then I should be taken to the correct page and the answer input should be focused", () => {
      $(SubmitPage.currencyAnswerEdit()).click();
      expect(browser.getUrl()).to.contain(AboutYou.url());
      expect(browser.getUrl()).to.contain(AboutYou.currency());
      expect($(AboutYou.currency()).isFocused()).to.be.true;
    });
  });

  describe("Given I have launched a questionnaire that has multiple answers per question", () => {
    beforeEach("Load the questionnaire", () => {
      browser.openQuestionnaire("test_multiple_answers.json");
    });

    it("When I am on the question page, Then all answers should have a label/legend", () => {
      expect($(AboutYou.dateLegend()).getText()).to.equal("What is your date of birth?");
      expect($(AboutYou.monthYearDateLegend()).getText()).to.equal("When would you like the car by?");
      expect($(AboutYou.radioLegend()).getText()).to.equal("Would you like the sports package?");
      expect($(AboutYou.durationLegend()).getText()).to.equal("How long have you had your licence?");
      expect($(AboutYou.checkboxLegend()).getText()).to.equal("What are your favourite car brands?");
      expect($(AboutYou.textfieldLabel()).getText()).to.equal("Your name");
      expect($(AboutYou.currencyLabel()).getText()).to.equal("What is your budget?");
      expect($(AboutYou.dropdownLabel()).getText()).to.equal("Select a colour");
      expect($(AboutYou.unitLabel()).getText()).to.equal("Max mileage");
      expect($(AboutYou.numberLabel()).getText()).to.equal("How many seats?");
      expect($(AboutYou.percentageLabel()).getText()).to.equal("Max CO2 emissions");
      expect($(AboutYou.mobileNumberLabel()).getText()).to.equal("What is your mobile number?");
      expect($(AboutYou.textareaLabel()).getText()).to.equal("Other comments");
    });
  });
});
