import DessertBlockPage from "../../../generated_pages/summary/dessert-block.page.js";
import DessertBlockPageSubmission from "../../../generated_pages/summary_with_submission_text/dessert-block.page.js";
import RadioPage from "../../../generated_pages/summary/radio.page.js";
import SummaryPage from "../../../generated_pages/summary/summary.page.js";
import TestNumberPage from "../../../generated_pages/summary/test-number-block.page.js";


describe("Summary Screen", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_summary.json");
  });

  it("Given a survey has been completed when a summary page is displayed then it should contain all answers", () => {
    completeAllQuestions();

    expect($(SummaryPage.radioAnswer()).getText()).to.contain("Bacon");
    expect($(SummaryPage.testCurrency()).getText()).to.contain("£1,234.00");
    expect($(SummaryPage.squareKilometres()).getText()).to.contain("123,456 km²");
    expect($(SummaryPage.testDecimal()).getText()).to.contain("123,456.78");
    expect($(SummaryPage.dessertGroupTitle()).getText()).to.contain("Dessert");
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

    expect($(SummaryPage.squareKilometres()).getText()).to.contain("123,456 km²");
    $(SummaryPage.squareKilometresEdit()).click();
    expect($(TestNumberPage.squareKilometres()).isFocused()).to.be.true;
    $(TestNumberPage.squareKilometres()).setValue("654321");
    $(TestNumberPage.submit()).click();
    expect($(SummaryPage.squareKilometres()).getText()).to.contain("654,321 km²");
  });

  it("Given a number value of zero is entered when on the summary screen then formatted 0 should be displayed", () => {
    $(RadioPage.submit()).click();
    $(TestNumberPage.testCurrency()).setValue("0");
    $(TestNumberPage.submit()).click();
    $(DessertBlockPage.submit()).click();
    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.testCurrency()).getText()).to.contain("£0.00");
  });

  it("Given no value is entered when on the summary screen then the correct response should be displayed", () => {
    $(RadioPage.submit()).click();
    $(TestNumberPage.submit()).click();
    $(DessertBlockPage.submit()).click();
    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.testCurrency()).getText()).to.contain("No answer provided");
  });

  it("Given a survey has been completed, when submission content has not been set in the schema, then the default content should be displayed", () => {
    completeAllQuestions();

    expect($(SummaryPage.questionText()).getText()).to.contain("Check your answers and submit");
    expect($(SummaryPage.submit()).getText()).to.contain("Submit answers");
  });

  function completeAllQuestions() {
    $(RadioPage.bacon()).click();
    $(RadioPage.submit()).click();
    $(TestNumberPage.testCurrency()).setValue("1234");
    $(TestNumberPage.squareKilometres()).setValue("123456");
    $(TestNumberPage.testDecimal()).setValue("123456.78");
    $(TestNumberPage.submit()).click();
    $(DessertBlockPage.dessert()).setValue("Crème Brûlée");
    $(DessertBlockPage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
  }
});

describe("Summary Screen", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_summary_with_submission_text.json");
  });

  it("Given a survey has been completed, when submission content has been set in the schema, then the correct content should be displayed", () => {
    $(DessertBlockPageSubmission.dessert()).setValue("Crème Brûlée");
    $(DessertBlockPageSubmission.submit()).click();
    expect($(SummaryPage.questionText()).getText()).to.contain("Submission title");
    expect($(SummaryPage.warning()).getText()).to.contain("Submission warning");
    expect($(SummaryPage.guidance()).getText()).to.contain("Submission guidance");
    expect($(SummaryPage.submit()).getText()).to.contain("Submission button");
  });
});
