import DessertPage from "../../../generated_pages/submit_with_summary/dessert.page.js";
import DessertConfirmationPage from "../../../generated_pages/submit_with_summary/dessert-confirmation.page";
import NumbersPage from "../../../generated_pages/submit_with_summary/numbers.page.js";
import RadioPage from "../../../generated_pages/submit_with_summary/radio.page.js";
import SubmitPage from "../../../generated_pages/submit_with_summary/submit.page.js";

describe("Submit Page with Summary", () => {
  beforeEach("Load the questionnaire", () => {
    browser.openQuestionnaire("test_submit_with_summary.json");
  });

  it("Given a questionnaire with a summary has been completed when the submit page is displayed, then it should contain a summary of all answers", () => {
    completeAllQuestions();

    expect($(SubmitPage.radioAnswer()).getText()).to.contain("Bacon");
    expect($(SubmitPage.dessertGroupTitle()).getText()).to.contain("Dessert");
    expect($(SubmitPage.dessertAnswer()).getText()).to.contain("Crème Brûlée");
    expect($(SubmitPage.dessertConfirmationAnswer()).getText()).to.contain("Yes");
    expect($(SubmitPage.numbersCurrencyAnswer()).getText()).to.contain("£1,234.00");
    expect($(SubmitPage.numbersUnitAnswer()).getText()).to.contain("123,456 km²");
    expect($(SubmitPage.numbersDecimalAnswer()).getText()).to.contain("123,456.78");
  });

  it("Given a questionnaire with a summary has been completed when the submit page is displayed then I should be able to submit the answers", () => {
    completeAllQuestions();

    $(SubmitPage.submit()).click();
    expect(browser.getUrl()).to.contain("thank-you");
  });

  it("Given a questionnaire with a summary has been completed when a summary page edit link is clicked then it should return to that question", () => {
    completeAllQuestions();

    $(SubmitPage.radioAnswerEdit()).click();

    expect($(RadioPage.bacon()).isSelected()).to.be.true;
  });

  it("Given a questionnaire with a summary has been completed and a summary page edit link is clicked, when I click previous, then it should return to the summary", () => {
    completeAllQuestions();

    $(SubmitPage.radioAnswerEdit()).click();
    $(RadioPage.previous()).click();

    expect(browser.getUrl()).to.contain(SubmitPage.pageName);
  });

  it("Given a questionnaire with a summary has been completed when a summary page edit link is clicked then it should return to that question then back to summary", () => {
    completeAllQuestions();

    $(SubmitPage.radioAnswerEdit()).click();
    $(RadioPage.sausage()).click();
    $(RadioPage.submit()).click();
    expect($(SubmitPage.radioAnswer()).getText()).to.contain("Sausage");
  });

  it("Given the edit link is used when a question is updated then the submit page summary should show the new answer", () => {
    completeAllQuestions();

    $(SubmitPage.numbersUnitAnswerEdit()).click();
    expect($(NumbersPage.unit()).isFocused()).to.be.true;
    $(NumbersPage.unit()).setValue("654321");
    $(NumbersPage.submit()).click();
    expect($(SubmitPage.numbersUnitAnswer()).getText()).to.contain("654,321 km²");
  });

  it("Given a number value of zero is entered when on the submit page then formatted 0 should be displayed on the summary", () => {
    $(RadioPage.submit()).click();
    $(DessertPage.answer()).setValue("Cake");
    $(DessertPage.submit()).click();
    $(DessertConfirmationPage.yes()).click();
    $(DessertConfirmationPage.submit()).click();
    $(NumbersPage.currency()).setValue("0");
    $(NumbersPage.submit()).click();
    expect($(SubmitPage.numbersCurrencyAnswer()).getText()).to.contain("£0.00");
  });

  it("Given no value is entered when on the submit page summary then the correct response should be displayed", () => {
    $(RadioPage.submit()).click();
    $(DessertPage.answer()).setValue("Cake");
    $(DessertPage.submit()).click();
    $(DessertConfirmationPage.yes()).click();
    $(DessertConfirmationPage.submit()).click();
    $(NumbersPage.submit()).click();
    expect($(SubmitPage.numbersCurrencyAnswer()).getText()).to.contain("No answer provided");
  });

  it("Given a questionnaire with a summary has been completed, when submission content has not been set in the schema, then the default content should be displayed", () => {
    completeAllQuestions();

    expect($(SubmitPage.heading()).getText()).to.contain("Check your answers and submit");
    expect($(SubmitPage.submit()).getText()).to.contain("Submit answers");
  });

  function completeAllQuestions() {
    $(RadioPage.bacon()).click();
    $(RadioPage.submit()).click();
    $(DessertPage.answer()).setValue("Crème Brûlée");
    $(DessertPage.submit()).click();
    $(DessertConfirmationPage.yes()).click();
    $(DessertConfirmationPage.submit()).click();
    $(NumbersPage.currency()).setValue("1234");
    $(NumbersPage.unit()).setValue("123456");
    $(NumbersPage.decimal()).setValue("123456.78");
    $(NumbersPage.submit()).click();

    expect(browser.getUrl()).to.contain(SubmitPage.pageName);
  }
});
