import DessertPage from "../../../generated_pages/submit_with_summary/dessert.page.js";
import DessertConfirmationPage from "../../../generated_pages/submit_with_summary/dessert-confirmation.page";
import NumbersPage from "../../../generated_pages/submit_with_summary/numbers.page.js";
import RadioPage from "../../../generated_pages/submit_with_summary/radio.page.js";
import SubmitPage from "../../../generated_pages/submit_with_summary/submit.page.js";
import { click } from "../../../helpers";
describe("Submit Page with Summary", () => {
  beforeEach("Load the questionnaire", async () => {
    await browser.openQuestionnaire("test_submit_with_summary.json");
  });

  it("Given a questionnaire with a summary has been completed when the submit page is displayed, then it should contain a summary of all answers", async () => {
    await completeAllQuestions();

    await expect(await $(SubmitPage.radioAnswer()).getText()).to.contain("Bacon");
    await expect(await $(SubmitPage.dessertGroupTitle()).getText()).to.contain("Dessert");
    await expect(await $(SubmitPage.dessertAnswer()).getText()).to.contain("Crème Brûlée");
    await expect(await $(SubmitPage.dessertConfirmationAnswer()).getText()).to.contain("Yes");
    await expect(await $(SubmitPage.numbersCurrencyAnswer()).getText()).to.contain("£1,234.00");
    await expect(await $(SubmitPage.numbersUnitAnswer()).getText()).to.contain("123,456 km²");
    await expect(await $(SubmitPage.numbersDecimalAnswer()).getText()).to.contain("123,456.78");
  });

  it("Given a questionnaire with a summary has been completed when the submit page is displayed then I should be able to submit the answers", async () => {
    await completeAllQuestions();

    await click(SubmitPage.submit());
    await expect(await browser.getUrl()).to.contain("thank-you");
  });

  it("Given a questionnaire with a summary has been completed when a summary page edit link is clicked then it should return to that question", async () => {
    await completeAllQuestions();

    await $(SubmitPage.radioAnswerEdit()).click();

    await expect(await $(RadioPage.bacon()).isSelected()).to.be.true;
  });

  it("Given a questionnaire with a summary has been completed and a summary page edit link is clicked, when I click previous, then it should return to the summary", async () => {
    await completeAllQuestions();

    await $(SubmitPage.radioAnswerEdit()).click();
    await $(RadioPage.previous()).click();

    await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
  });

  it("Given a questionnaire with a summary has been completed when a summary page edit link is clicked then it should return to that question then back to summary", async () => {
    await completeAllQuestions();

    await $(SubmitPage.radioAnswerEdit()).click();
    await $(RadioPage.sausage()).click();
    await click(RadioPage.submit());
    await expect(await $(SubmitPage.radioAnswer()).getText()).to.contain("Sausage");
  });

  it("Given the edit link is used when a question is updated then the submit page summary should show the new answer", async () => {
    await completeAllQuestions();

    await $(SubmitPage.numbersUnitAnswerEdit()).click();
    await expect(await $(NumbersPage.unit()).isFocused()).to.be.true;
    await $(NumbersPage.unit()).setValue("654321");
    await click(NumbersPage.submit());
    await expect(await $(SubmitPage.numbersUnitAnswer()).getText()).to.contain("654,321 km²");
  });

  it("Given a number value of zero is entered when on the submit page then formatted 0 should be displayed on the summary", async () => {
    await click(RadioPage.submit());
    await $(DessertPage.answer()).setValue("Cake");
    await click(DessertPage.submit());
    await $(DessertConfirmationPage.yes()).click();
    await click(DessertConfirmationPage.submit());
    await $(NumbersPage.currency()).setValue("0");
    await click(NumbersPage.submit());
    await expect(await $(SubmitPage.numbersCurrencyAnswer()).getText()).to.contain("£0.00");
  });

  it("Given no value is entered when on the submit page summary then the correct response should be displayed", async () => {
    await click(RadioPage.submit());
    await $(DessertPage.answer()).setValue("Cake");
    await click(DessertPage.submit());
    await $(DessertConfirmationPage.yes()).click();
    await click(DessertConfirmationPage.submit());
    await click(NumbersPage.submit());
    await expect(await $(SubmitPage.numbersCurrencyAnswer()).getText()).to.contain("No answer provided");
  });

  it("Given a questionnaire with a summary has been completed, when submission content has not been set in the schema, then the default content should be displayed", async () => {
    await completeAllQuestions();

    await expect(await $(SubmitPage.heading()).getText()).to.contain("Check your answers and submit");
    await expect(await $(SubmitPage.submit()).getText()).to.contain("Submit answers");
  });

  async function completeAllQuestions() {
    await $(RadioPage.bacon()).click();
    await click(RadioPage.submit());
    await $(DessertPage.answer()).setValue("Crème Brûlée");
    await click(DessertPage.submit());
    await $(DessertConfirmationPage.yes()).click();
    await click(DessertConfirmationPage.submit());
    await $(NumbersPage.currency()).setValue("1234");
    await $(NumbersPage.unit()).setValue("123456");
    await $(NumbersPage.decimal()).setValue("123456.78");
    await click(NumbersPage.submit());

    await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
  }
});
