import CurrencyTotalPlaybackPageWithFourth from "../../generated_pages/calculated_summary/currency-total-playback-with-fourth.page";
import UnitTotalPlaybackPage from "../../generated_pages/calculated_summary/unit-total-playback.page";
import NumberTotalPlaybackPage from "../../generated_pages/calculated_summary/number-total-playback.page";
import ThirdNumberBlockPage from "../../generated_pages/calculated_summary/third-number-block.page";
import FourthNumberBlockPage from "../../generated_pages/calculated_summary/fourth-number-block.page";
import FourthAndAHalfNumberBlockPage from "../../generated_pages/calculated_summary/fourth-and-a-half-number-block.page";
import SixthNumberBlockPage from "../../generated_pages/calculated_summary/sixth-number-block.page";
import FifthNumberBlockPage from "../../generated_pages/calculated_summary/fifth-number-block.page";
import SkipFourthBlockPage from "../../generated_pages/calculated_summary/skip-fourth-block.page";
import CurrencyTotalPlaybackPageSkippedFourth from "../../generated_pages/calculated_summary/currency-total-playback-skipped-fourth.page";
import PercentageTotalPlaybackPage from "../../generated_pages/calculated_summary/percentage-total-playback.page";
import CalculatedSummaryTotalConfirmation from "../../generated_pages/calculated_summary/calculated-summary-total-confirmation.page";
import SetMinMaxBlockPage from "../../generated_pages/calculated_summary/set-min-max-block.page";
import SubmitPage from "../../generated_pages/calculated_summary/submit.page";
import ThirdAndAHalfNumberBlockPage from "../../generated_pages/calculated_summary/third-and-a-half-number-block.page";
import ThankYouPage from "../../base_pages/thank-you.page";
import FirstNumberBlockPage from "../../generated_pages/calculated_summary/first-number-block.page";
import SecondNumberBlockPage from "../../generated_pages/calculated_summary/second-number-block.page";

class TestCase {
  testCase(schema) {
    before("Get to Calculated Summary", async () => {
      await browser.openQuestionnaire(schema);

      await $(FirstNumberBlockPage.firstNumber()).setValue(1.23);
      await $(FirstNumberBlockPage.submit()).click();

      await $(SecondNumberBlockPage.secondNumber()).setValue(4.56);
      await $(SecondNumberBlockPage.secondNumberUnitTotal()).setValue(789);
      await $(SecondNumberBlockPage.secondNumberAlsoInTotal()).setValue(0.12);
      await $(SecondNumberBlockPage.submit()).click();

      await $(ThirdNumberBlockPage.thirdNumber()).setValue(3.45);
      await $(ThirdNumberBlockPage.submit()).click();
      await $(ThirdAndAHalfNumberBlockPage.thirdAndAHalfNumberUnitTotal()).setValue(678);
      await $(ThirdAndAHalfNumberBlockPage.submit()).click();

      await $(SkipFourthBlockPage.no()).click();
      await $(SkipFourthBlockPage.submit()).click();

      await $(FourthNumberBlockPage.fourthNumber()).setValue(9.01);
      await $(FourthNumberBlockPage.submit()).click();
      await $(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal()).setValue(2.34);
      await $(FourthAndAHalfNumberBlockPage.submit()).click();

      await $(FifthNumberBlockPage.fifthPercent()).setValue(56);
      await $(FifthNumberBlockPage.fifthNumber()).setValue(78.91);
      await $(FifthNumberBlockPage.submit()).click();

      await $(SixthNumberBlockPage.sixthPercent()).setValue(23);
      await $(SixthNumberBlockPage.sixthNumber()).setValue(45.67);
      await $(SixthNumberBlockPage.submit()).click();

      const browserUrl = await browser.getUrl();

      await expect(await browserUrl).to.contain(CurrencyTotalPlaybackPageWithFourth.pageName);
    });

    it("Given I have completed all questions, When I am on the calculated summary, Then the page title should use the calculation's title", async () => {
      await expect(await browser.getTitle()).to.equal("Grand total of previous values - A test schema to demo Calculated Summary");
    });

    it("Given I complete every question, When I get to the currency summary, Then I should see the correct total", async () => {
      // Totals and titles should be shown
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £20.71. Is this correct?"
      );
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryQuestion()).getText()).to.contain("Grand total of previous values");
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryAnswer()).getText()).to.contain("£20.71");

      // Answers included in calculation should be shown
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.firstNumberAnswerLabel()).getText()).to.contain("First answer label");
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.firstNumberAnswer()).getText()).to.contain("£1.23");
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.secondNumberAnswerLabel()).getText()).to.contain("Second answer in currency label");
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.secondNumberAnswer()).getText()).to.contain("£4.56");
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.secondNumberAnswerAlsoInTotalLabel()).getText()).to.contain(
        "Second answer label also in currency total (optional)"
      );
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.secondNumberAnswerAlsoInTotal()).getText()).to.contain("£0.12");
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswerLabel()).getText()).to.contain("Third answer label");
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswer()).getText()).to.contain("£3.45");
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswerLabel()).getText()).to.contain("Fourth answer label (optional)");
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswer()).getText()).to.contain("£9.01");
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotalLabel()).getText()).to.contain(
        "Fourth answer label also in total (optional)"
      );
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotal()).getText()).to.contain("£2.34");

      // Answers not included in calculation should not be shown
      await expect(await $$(UnitTotalPlaybackPage.secondNumberAnswerUnitTotal())).to.be.empty;
      await expect(await $$(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal())).to.be.empty;
      await expect(await $$(NumberTotalPlaybackPage.fifthNumberAnswer())).to.be.empty;
      await expect(await $$(NumberTotalPlaybackPage.sixthNumberAnswer())).to.be.empty;
    });

    it("Given I reach the calculated summary page, Then the Change link url should contain return_to, return_to_answer_id and return_to_block_id query params", async () => {
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.firstNumberAnswerEdit()).getAttribute("href")).to.contain(
        "/questionnaire/first-number-block/?return_to=calculated-summary&return_to_answer_id=first-number-answer&return_to_block_id=currency-total-playback-with-fourth#first-number-answer"
      );
    });

    it("Given I edit an answer from the calculated summary page and click the Previous button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing", async () => {
      await $(CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswerEdit()).click();
      await $(ThirdNumberBlockPage.previous()).click();
      await expect(await browser.getUrl()).to.contain("/questionnaire/currency-total-playback-with-fourth/?return_to=calculated-summary#third-number-answer");
    });

    it("Given I edit an answer from the calculated summary page and click the Submit button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing", async () => {
      await $(CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswerEdit()).click();
      await $(ThirdNumberBlockPage.submit()).click();
      await expect(await browser.getUrl()).to.contain("/questionnaire/currency-total-playback-with-fourth/?return_to=calculated-summary#third-number-answer");
    });

    it("Given I change an answer, When I get to the currency summary, Then I should see the new total", async () => {
      await $(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswerEdit()).click();
      await $(FourthNumberBlockPage.fourthNumber()).setValue(19.01);
      await $(FourthNumberBlockPage.submit()).click();

      await expect(await browser.getUrl()).to.contain(CurrencyTotalPlaybackPageWithFourth.pageName);
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £30.71. Is this correct?"
      );
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryAnswer()).getText()).to.contain("£30.71");
    });

    it("Given I leave an answer empty, When I get to the currency summary, Then I should see no answer provided and new total", async () => {
      await $(CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotalEdit()).click();
      await $(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal()).setValue("");
      await $(FourthAndAHalfNumberBlockPage.submit()).click();

      await expect(await browser.getUrl()).to.contain(CurrencyTotalPlaybackPageWithFourth.pageName);
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £28.37. Is this correct?"
      );
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.calculatedSummaryAnswer()).getText()).to.contain("£28.37");
      await expect(await $(CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotal()).getText()).to.contain("No answer provided");
    });

    it("Given I skip the fourth page, When I get to the playback, Then I can should not see it in the total", async () => {
      await $(CurrencyTotalPlaybackPageWithFourth.previous()).click();
      await $(SixthNumberBlockPage.previous()).click();
      await $(FifthNumberBlockPage.previous()).click();
      await $(FourthAndAHalfNumberBlockPage.previous()).click();
      await $(FourthNumberBlockPage.previous()).click();

      await $(SkipFourthBlockPage.yes()).click();
      await $(SkipFourthBlockPage.submit()).click();

      await $(FifthNumberBlockPage.submit()).click();
      await $(SixthNumberBlockPage.submit()).click();

      const expectedUrl = await browser.getUrl();

      await expect(expectedUrl).to.contain(CurrencyTotalPlaybackPageSkippedFourth.pageName);
      await expect(await $$(CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswer())).to.be.empty;
      await expect(await $$(CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotal())).to.be.empty;
      await expect(await $(CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £9.36. Is this correct?"
      );
      await expect(await $(CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryAnswer()).getText()).to.contain("£9.36");
    });

    it("Given I complete every question, When I get to the unit summary, Then I should see the correct total", async () => {
      // Totals and titles should be shown
      await $(CurrencyTotalPlaybackPageWithFourth.submit()).click();
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of unit values entered to be 1,467 cm. Is this correct?"
      );
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain("Grand total of previous values");
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("1,467 cm");

      // Answers included in calculation should be shown
      await expect(await $(UnitTotalPlaybackPage.secondNumberAnswerUnitTotalLabel()).getText()).to.contain("Second answer label in unit total");
      await expect(await $(UnitTotalPlaybackPage.secondNumberAnswerUnitTotal()).getText()).to.contain("789 cm");
      await expect(await $(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotalLabel()).getText()).to.contain("Third answer label in unit total");
      await expect(await $(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal()).getText()).to.contain("678 cm");
    });

    it("Given the calculated summary has a custom title, When I am on the unit calculated summary, Then the page title should use the custom title", async () => {
      await expect(await browser.getTitle()).to.equal("Total Unit Values - A test schema to demo Calculated Summary");
    });

    it("Given I complete every question, When I get to the percentage summary, Then I should see the correct total", async () => {
      // Totals and titles should be shown
      await $(UnitTotalPlaybackPage.submit()).click();
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of percentage values entered to be 79%. Is this correct?"
      );
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain("Grand total of previous values");
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("79%");

      // Answers included in calculation should be shown
      await expect(await $(PercentageTotalPlaybackPage.fifthPercentAnswerLabel()).getText()).to.contain("Fifth answer label percentage tota");
      await expect(await $(PercentageTotalPlaybackPage.fifthPercentAnswer()).getText()).to.contain("56%");
      await expect(await $(PercentageTotalPlaybackPage.sixthPercentAnswerLabel()).getText()).to.contain("Sixth answer label percentage tota");
      await expect(await $(PercentageTotalPlaybackPage.sixthPercentAnswer()).getText()).to.contain("23%");
    });

    it("Given I complete every question, When I get to the number summary, Then I should see the correct total", async () => {
      // Totals and titles should be shown
      await $(UnitTotalPlaybackPage.submit()).click();
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of number values entered to be 124.58. Is this correct?"
      );
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain("Grand total of previous values");
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("124.58");

      // Answers included in calculation should be shown
      await expect(await $(NumberTotalPlaybackPage.fifthNumberAnswerLabel()).getText()).to.contain("Fifth answer label number total");
      await expect(await $(NumberTotalPlaybackPage.fifthNumberAnswer()).getText()).to.contain("78.91");
      await expect(await $(NumberTotalPlaybackPage.sixthNumberAnswerLabel()).getText()).to.contain("Sixth answer label number total");
      await expect(await $(NumberTotalPlaybackPage.sixthNumberAnswer()).getText()).to.contain("45.67");
    });

    it("Given I complete every calculated summary, When I go to a page with calculated summary piping, Then I should the see the piped calculated summary total for each summary", async () => {
      await $(NumberTotalPlaybackPage.submit()).click();

      const content = $("h1 + ul").getText();
      const textsToAssert = [
        "Total currency values (if Q4 not skipped): £28.37",
        "Total currency values (if Q4 skipped)): £9.36",
        "Total unit values: 1,467",
        "Total percentage values: 79",
        "Total number values: 124.58",
      ];

      textsToAssert.forEach(async (text) => await expect(content).to.containasync(text));
    });

    it("Given I have an answer minimum based on a calculated summary total, When I enter an invalid answer, Then I should see an error message on the page", async () => {
      await $(CalculatedSummaryTotalConfirmation.submit()).click();
      await expect(await browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      await $(SetMinMaxBlockPage.setMinimum()).setValue(8.0);
      await $(SetMinMaxBlockPage.submit()).click();
      await expect(await $(SetMinMaxBlockPage.errorNumber(1)).getText()).to.contain("Enter an answer more than or equal to £9.36");
      await $(SetMinMaxBlockPage.setMinimum()).setValue(10.0);
      await $(SetMinMaxBlockPage.submit()).click();
    });

    it("Given I have an answer maximum based on a calculated summary total, When I enter an invalid answer, Then I should see an error message on the page", async () => {
      await $(SubmitPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      await $(SetMinMaxBlockPage.setMaximum()).setValue(10.0);
      await $(SetMinMaxBlockPage.submit()).click();
      await expect(await $(SetMinMaxBlockPage.errorNumber(1)).getText()).to.contain("Enter an answer less than or equal to £9.36");
      await $(SetMinMaxBlockPage.setMaximum()).setValue(7.0);
      await $(SetMinMaxBlockPage.submit()).click();
    });

    it("Given I confirm the totals and am on the summary, When I edit and change an answer, Then I must re-confirm the dependant calculated summary page and min max question page before I can return to the summary", async () => {
      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
      await $(SubmitPage.thirdNumberAnswerEdit()).click();
      await $(ThirdNumberBlockPage.thirdNumber()).setValue(3.5);
      await $(ThirdNumberBlockPage.submit()).click();
      await $(ThirdAndAHalfNumberBlockPage.submit()).click();
      await $(SkipFourthBlockPage.submit()).click();
      await $(FifthNumberBlockPage.submit()).click();
      await $(SixthNumberBlockPage.submit()).click();

      await expect(await $(CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £9.41. Is this correct?"
      );

      await $(CurrencyTotalPlaybackPageSkippedFourth.submit()).click();
      await $(UnitTotalPlaybackPage.submit()).click();
      await $(PercentageTotalPlaybackPage.submit()).click();
      await $(NumberTotalPlaybackPage.submit()).click();
      await $(CalculatedSummaryTotalConfirmation.submit()).click();
      await expect(await browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      await $(SetMinMaxBlockPage.setMinimum()).setValue(10.0);
      await $(SetMinMaxBlockPage.setMaximum()).setValue(9.0);
      await $(SetMinMaxBlockPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("Given I confirm the totals and am on the summary, When I edit and change an answer that has a dependent minimum value from a calculated summary total, And the minimum value has been changed, Then I must re-validate before I get to the summary", async () => {
      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
      await $(SubmitPage.thirdNumberAnswerEdit()).click();
      await $(ThirdNumberBlockPage.thirdNumber()).setValue(10.0);
      await $(ThirdNumberBlockPage.submit()).click();
      await $(ThirdAndAHalfNumberBlockPage.submit()).click();
      await $(SkipFourthBlockPage.submit()).click();
      await $(FifthNumberBlockPage.submit()).click();
      await $(SixthNumberBlockPage.submit()).click();

      await expect(await $(CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £15.91. Is this correct?"
      );

      await $(CurrencyTotalPlaybackPageSkippedFourth.submit()).click();
      await $(UnitTotalPlaybackPage.submit()).click();
      await $(PercentageTotalPlaybackPage.submit()).click();
      await $(NumberTotalPlaybackPage.submit()).click();
      await $(CalculatedSummaryTotalConfirmation.submit()).click();
      await expect(await browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      await $(SetMinMaxBlockPage.submit()).click();
      await expect(await $(SetMinMaxBlockPage.errorNumber(1)).getText()).to.contain("Enter an answer more than or equal to £15.91");
      await $(SetMinMaxBlockPage.setMinimum()).setValue(16.0);
      await $(SetMinMaxBlockPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("Given I confirm the totals and am on the summary, When I edit and change an answer that has a dependent maximum value from a calculated summary total, And the maximum value has been changed, Then I must re-validate before I get to the summary", async () => {
      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
      await $(SubmitPage.thirdNumberAnswerEdit()).click();
      await $(ThirdNumberBlockPage.thirdNumber()).setValue(1.0);
      await $(ThirdNumberBlockPage.submit()).click();
      await $(ThirdAndAHalfNumberBlockPage.submit()).click();
      await $(SkipFourthBlockPage.submit()).click();
      await $(FifthNumberBlockPage.submit()).click();
      await $(SixthNumberBlockPage.submit()).click();

      await expect(await $(CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £6.91. Is this correct?"
      );

      await $(CurrencyTotalPlaybackPageSkippedFourth.submit()).click();
      await $(UnitTotalPlaybackPage.submit()).click();
      await $(PercentageTotalPlaybackPage.submit()).click();
      await $(NumberTotalPlaybackPage.submit()).click();
      await $(CalculatedSummaryTotalConfirmation.submit()).click();
      await expect(await browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      await $(SetMinMaxBlockPage.submit()).click();
      await expect(await $(SetMinMaxBlockPage.errorNumber(1)).getText()).to.contain("Enter an answer less than or equal to £6.91");
      await $(SetMinMaxBlockPage.setMaximum()).setValue(6.0);
      await $(SetMinMaxBlockPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("Given I am on the summary, When I submit the questionnaire, Then I should see the thank you page", async () => {
      await $(SubmitPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(ThankYouPage.pageName);
    });
  }
}

export const CalculatedSummaryTestCase = new TestCase();
