import DessertPage from "../../../generated_pages/summary/dessert.page.js";
import DessertConfirmationPage from "../../../generated_pages/summary/dessert-confirmation.page";
import NumbersPage from "../../../generated_pages/summary/numbers.page.js";
import RadioPage from "../../../generated_pages/summary/radio.page.js";
import SummaryPage from "../../../generated_pages/summary/summary.page.js";

describe("Summary Screen", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_summary.json");
  });

  it("Given a survey has been completed when a summary page is displayed then it should contain all answers", () => {
    completeAllQuestions();

    expect($(SummaryPage.radioAnswer()).getText()).to.contain("Bacon");
    expect($(SummaryPage.dessertGroupTitle()).getText()).to.contain("Dessert");
    expect($(SummaryPage.dessertAnswer()).getText()).to.contain("Crème Brûlée");
    expect($(SummaryPage.dessertConfirmationAnswer()).getText()).to.contain("Yes");
    expect($(SummaryPage.numbersCurrencyAnswer()).getText()).to.contain("£1,234.00");
    expect($(SummaryPage.numbersUnitAnswer()).getText()).to.contain("123,456 km²");
    expect($(SummaryPage.numbersDecimalAnswer()).getText()).to.contain("123,456.78");
  });

  it("Given a survey has been completed when a summary page is displayed then I should be able to submit the answers", () => {
    completeAllQuestions();

    $(SummaryPage.submit()).click();
    expect(browser.getUrl()).to.contain("thank-you");
  });

  it("Given a survey has been completed when a summary page edit link is clicked then it should return to that question", () => {
    completeAllQuestions();

    $(SummaryPage.radioAnswerEdit()).click();

    expect($(RadioPage.bacon()).isSelected()).to.be.true;
  });

  it("Given a survey has been completed when a summary page edit link is clicked then it should return to that question then back to summary", () => {
    completeAllQuestions();

    $(SummaryPage.radioAnswerEdit()).click();
    $(RadioPage.sausage()).click();
    $(RadioPage.submit()).click();
    expect($(SummaryPage.radioAnswer()).getText()).to.contain("Sausage");
  });

  it("Given the edit link is used when a question is updated then the summary screen should show the new answer", () => {
    completeAllQuestions();

    $(SummaryPage.numbersUnitAnswerEdit()).click();
    expect($(NumbersPage.unit()).isFocused()).to.be.true;
    $(NumbersPage.unit()).setValue("654321");
    $(NumbersPage.submit()).click();
    expect($(SummaryPage.numbersUnitAnswer()).getText()).to.contain("654,321 km²");
  });

  it("Given a number value of zero is entered when on the summary screen then formatted 0 should be displayed", () => {
    $(RadioPage.submit()).click();
    $(DessertPage.answer()).setValue("Cake");
    $(DessertPage.submit()).click();
    $(DessertConfirmationPage.yes()).click();
    $(DessertConfirmationPage.submit()).click();
    $(NumbersPage.currency()).setValue("0");
    $(NumbersPage.submit()).click();
    expect($(SummaryPage.numbersCurrencyAnswer()).getText()).to.contain("£0.00");
  });

  it("Given no value is entered when on the summary screen then the correct response should be displayed", () => {
    $(RadioPage.submit()).click();
    $(DessertPage.answer()).setValue("Cake");
    $(DessertPage.submit()).click();
    $(DessertConfirmationPage.yes()).click();
    $(DessertConfirmationPage.submit()).click();
    $(NumbersPage.submit()).click();
    expect($(SummaryPage.numbersCurrencyAnswer()).getText()).to.contain("No answer provided");
  });

  it("Given a survey has been completed, when submission content has not been set in the schema, then the default content should be displayed", () => {
    completeAllQuestions();

    expect($(SummaryPage.questionText()).getText()).to.contain("Check your answers and submit");
    expect($(SummaryPage.submit()).getText()).to.contain("Submit answers");
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

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
  }
});
