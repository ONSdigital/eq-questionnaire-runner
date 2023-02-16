import FirstNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/first-number-block.page.js";
import SecondNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/second-number-block.page.js";
import ThirdNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/third-number-block.page.js";
import ThirdAndAHalfNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/third-and-a-half-number-block.page.js";
import SkipFourthBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/skip-fourth-block.page.js";
import FourthNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/fourth-number-block.page.js";
import FourthAndAHalfNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/fourth-and-a-half-number-block.page.js";
import FifthNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/fifth-number-block.page.js";
import SixthNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/sixth-number-block.page.js";
import CurrencyTotalPlaybackPageWithFourth from "../../generated_pages/calculated_summary/currency-total-playback-with-fourth.page.js";
import SetMinMaxBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/set-min-max-block.page.js";
import CurrencyTotalPlaybackPageSkippedFourth from "../../generated_pages/new_calculated_summary_repeating_section/currency-total-playback-skipped-fourth.page.js";
import UnitTotalPlaybackPage from "../../generated_pages/new_calculated_summary_repeating_section/unit-total-playback.page.js";
import PercentageTotalPlaybackPage from "../../generated_pages/new_calculated_summary_repeating_section/percentage-total-playback.page.js";
import NumberTotalPlaybackPage from "../../generated_pages/new_calculated_summary_repeating_section/number-total-playback.page.js";
import BreakdownPage from "../../generated_pages/new_calculated_summary_repeating_section/breakdown.page.js";
import SecondCurrencyTotalPlaybackPage from "../../generated_pages/new_calculated_summary_repeating_section/second-currency-total-playback.page.js";
import CalculatedSummaryTotalConfirmation from "../../generated_pages/new_calculated_summary_repeating_section/calculated-summary-total-confirmation.page.js";
import SubmitPage from "../../generated_pages/new_calculated_summary_repeating_section/personal-details-section-summary.page.js";
import ThankYouPage from "../../base_pages/thank-you.page.js";
import HubPage from "../../base_pages/hub.page.js";
import PrimaryPersonListCollectorPage from "../../generated_pages/new_calculated_summary_repeating_section/primary-person-list-collector.page";
import PrimaryPersonListCollectorAddPage from "../../generated_pages/new_calculated_summary_repeating_section/primary-person-list-collector-add.page.js";
import ListCollectorPage from "../../generated_pages/new_calculated_summary_repeating_section/list-collector.page";
import ListCollectorAddPage from "../../generated_pages/new_calculated_summary_repeating_section/list-collector-add.page";

describe("Feature: Calculated Summary Repeating Section", () => {
  describe("Given I have a Calculated Summary in a Repeating Section", () => {
    before("Get to Calculated Summary", async ()=> {
      await browser.openQuestionnaire("test_new_calculated_summary_repeating_section.json");
      await $(await HubPage.submit()).click();
      await $(await PrimaryPersonListCollectorPage.yes()).click();
      await $(await PrimaryPersonListCollectorPage.submit()).click();
      await $(await PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(await PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await $(await PrimaryPersonListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.no()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await HubPage.submit()).click();

      getToFirstCalculatedSummary();

      const browserUrl = browser.getUrl();

      await expect(browserUrl).to.contain(CurrencyTotalPlaybackPageWithFourth.pageName);
    });

    it("Given I have completed all questions, When I am on the calculated summary and there is no custom page title, Then the page title should use the calculation's title", async ()=> {
      await expect(browser.getTitle()).to.equal("Grand total of previous values - A test schema to demo Calculated Summary");
    });

    it("Given I complete every question, When I get to the currency summary, Then I should see the correct total", async ()=> {
      // Totals and titles should be shown
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £20.71. Is this correct?"
      );
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.calculatedSummaryQuestion()).getText()).to.contain("Grand total of previous values");
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.calculatedSummaryAnswer()).getText()).to.contain("£20.71");

      // Answers included in calculation should be shown
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.firstNumberAnswerLabel()).getText()).to.contain("First answer label");
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.firstNumberAnswer()).getText()).to.contain("£1.23");
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.secondNumberAnswerLabel()).getText()).to.contain("Second answer in currency label");
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.secondNumberAnswer()).getText()).to.contain("£4.56");
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.secondNumberAnswerAlsoInTotalLabel()).getText()).to.contain(
        "Second answer label also in currency total (optional)"
      );
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.secondNumberAnswerAlsoInTotal()).getText()).to.contain("£0.12");
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswerLabel()).getText()).to.contain("Third answer label");
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswer()).getText()).to.contain("£3.45");
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswerLabel()).getText()).to.contain("Fourth answer label (optional)");
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswer()).getText()).to.contain("£9.01");
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotalLabel()).getText()).to.contain(
        "Fourth answer label also in total (optional)"
      );
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotal()).getText()).to.contain("£2.34");

      // Answers not included in calculation should not be shown
      await expect(await $$( UnitTotalPlaybackPage.secondNumberAnswerUnitTotal())).to.be.empty;
      await expect(await $$( UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal())).to.be.empty;
      await expect(await $$( NumberTotalPlaybackPage.fifthNumberAnswer())).to.be.empty;
      await expect(await $$( NumberTotalPlaybackPage.sixthNumberAnswer())).to.be.empty;
    });

    it("Given I reach the calculated summary page, Then the Change link url should contain return_to, return_to_answer_id and return_to_block_id query params", async ()=> {
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.firstNumberAnswerEdit()).getAttribute("href")).to.contain(
        "first-number-block/?return_to=calculated-summary&return_to_answer_id=first-number-answer&return_to_block_id=currency-total-playback-with-fourth#first-number-answer"
      );
    });

    it("Given I edit an answer from the calculated summary page and click the Previous button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing", async ()=> {
      await $(await CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswerEdit()).click();
      await $(await ThirdNumberBlockPage.previous()).click();
      await expect(browser.getUrl()).to.contain("currency-total-playback-with-fourth/?return_to=calculated-summary#third-number-answer");
    });

    it("Given I edit an answer from the calculated summary page and click the Submit button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing", async ()=> {
      await $(await CurrencyTotalPlaybackPageWithFourth.thirdNumberAnswerEdit()).click();
      await $(await ThirdNumberBlockPage.submit()).click();
      await expect(browser.getUrl()).to.contain("currency-total-playback-with-fourth/?return_to=calculated-summary#third-number-answer");
    });

    it("Given I change an answer, When I get to the currency summary, Then I should see the new total", async ()=> {
      await $(await CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswerEdit()).click();
      await $(await FourthNumberBlockPage.fourthNumber()).setValue(19.01);
      await $(await FourthNumberBlockPage.submit()).click();

      await expect(browser.getUrl()).to.contain(CurrencyTotalPlaybackPageWithFourth.pageName);
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £30.71. Is this correct?"
      );
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.calculatedSummaryAnswer()).getText()).to.contain("£30.71");
    });

    it("Given I leave an answer empty, When I get to the currency summary, Then I should see no answer provided and new total", async ()=> {
      await $(await CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotalEdit()).click();
      await $(await FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal()).setValue("");
      await $(await FourthAndAHalfNumberBlockPage.submit()).click();

      await expect(browser.getUrl()).to.contain(CurrencyTotalPlaybackPageWithFourth.pageName);
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £28.37. Is this correct?"
      );
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.calculatedSummaryAnswer()).getText()).to.contain("£28.37");
      await expect(await $(await CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotal()).getText()).to.contain("No answer provided");
    });

    it("Given I skip the fourth page, When I get to the playback, Then I can should not see it in the total", async ()=> {
      await $(await CurrencyTotalPlaybackPageWithFourth.previous()).click();
      await $(await SixthNumberBlockPage.previous()).click();
      await $(await FifthNumberBlockPage.previous()).click();
      await $(await FourthAndAHalfNumberBlockPage.previous()).click();
      await $(await FourthNumberBlockPage.previous()).click();

      await $(await SkipFourthBlockPage.yes()).click();
      await $(await SkipFourthBlockPage.submit()).click();

      await $(await FifthNumberBlockPage.submit()).click();
      await $(await SixthNumberBlockPage.submit()).click();

      const expectedUrl = browser.getUrl();

      await expect(expectedUrl).to.contain(CurrencyTotalPlaybackPageSkippedFourth.pageName);
      await expect(await $$( CurrencyTotalPlaybackPageWithFourth.fourthNumberAnswer())).to.be.empty;
      await expect(await $$( CurrencyTotalPlaybackPageWithFourth.fourthAndAHalfNumberAnswerAlsoInTotal())).to.be.empty;
      await expect(await $(await CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £9.36. Is this correct?"
      );
      await expect(await $(await CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryAnswer()).getText()).to.contain("£9.36");
    });

    it("Given I complete every question, When I get to the unit summary, Then I should see the correct total", async ()=> {
      // Totals and titles should be shown
      await $(await CurrencyTotalPlaybackPageWithFourth.submit()).click();
      await expect(await $(await UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of unit values entered to be 1,467 cm. Is this correct?"
      );
      await expect(await $(await UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain("Grand total of previous values");
      await expect(await $(await UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("1,467 cm");

      // Answers included in calculation should be shown
      await expect(await $(await UnitTotalPlaybackPage.secondNumberAnswerUnitTotalLabel()).getText()).to.contain("Second answer label in unit total");
      await expect(await $(await UnitTotalPlaybackPage.secondNumberAnswerUnitTotal()).getText()).to.contain("789 cm");
      await expect(await $(await UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotalLabel()).getText()).to.contain("Third answer label in unit total");
      await expect(await $(await UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal()).getText()).to.contain("678 cm");
    });

    it("Given the calculated summary has a custom title, When I am on the unit calculated summary, Then the page title should use the custom title", async ()=> {
      await expect(browser.getTitle()).to.equal("Total Unit Values - A test schema to demo Calculated Summary");
    });

    it("Given I complete every question, When I get to the percentage summary, Then I should see the correct total", async ()=> {
      // Totals and titles should be shown
      await $(await UnitTotalPlaybackPage.submit()).click();
      await expect(await $(await UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of percentage values entered to be 79%. Is this correct?"
      );
      await expect(await $(await UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain("Grand total of previous values");
      await expect(await $(await UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("79%");

      // Answers included in calculation should be shown
      await expect(await $(await PercentageTotalPlaybackPage.fifthPercentAnswerLabel()).getText()).to.contain("Fifth answer label percentage tota");
      await expect(await $(await PercentageTotalPlaybackPage.fifthPercentAnswer()).getText()).to.contain("56%");
      await expect(await $(await PercentageTotalPlaybackPage.sixthPercentAnswerLabel()).getText()).to.contain("Sixth answer label percentage tota");
      await expect(await $(await PercentageTotalPlaybackPage.sixthPercentAnswer()).getText()).to.contain("23%");
    });

    it("Given the calculated summary has a custom title with the list item position, When I am on the percentage calculated summary, Then the page title should use the custom title with the list item position", async ()=> {
      await expect(browser.getTitle()).to.equal("Percentage Calculated Summary: Person 1 - A test schema to demo Calculated Summary");
    });

    it("Given I complete every question, When I get to the number summary, Then I should see the correct total", async ()=> {
      // Totals and titles should be shown
      await $(await UnitTotalPlaybackPage.submit()).click();
      await expect(await $(await UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of number values entered to be 124.58. Is this correct?"
      );
      await expect(await $(await UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain("Grand total of previous values");
      await expect(await $(await UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("124.58");

      // Answers included in calculation should be shown
      await expect(await $(await NumberTotalPlaybackPage.fifthNumberAnswerLabel()).getText()).to.contain("Fifth answer label number total");
      await expect(await $(await NumberTotalPlaybackPage.fifthNumberAnswer()).getText()).to.contain("78.91");
      await expect(await $(await NumberTotalPlaybackPage.sixthNumberAnswerLabel()).getText()).to.contain("Sixth answer label number total");
      await expect(await $(await NumberTotalPlaybackPage.sixthNumberAnswer()).getText()).to.contain("45.67");
    });

    it("Given I have a calculated summary total that is used as a placeholder in another calculated summary, When I get to the calculated summary page displaying the placeholder, Then I should see the correct total", async ()=> {
      await $(await NumberTotalPlaybackPage.submit()).click();
      await expect(browser.getUrl()).to.contain(BreakdownPage.pageName);
      await $(await BreakdownPage.answer1()).setValue(100.0);
      await $(await BreakdownPage.answer2()).setValue(24.58);
      await $(await BreakdownPage.submit()).click();
      await expect(browser.getUrl()).to.contain(SecondCurrencyTotalPlaybackPage.pageName);
      await expect(await $(await SecondCurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of number values entered to be £124.58. Is this correct?"
      );
      await expect($("body").getText()).to.have.string("Enter two values that add up to the previous calculated summary total of £124.58");
      await expect(await $(await SecondCurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("124.58");
    });

    it("Given I complete every calculated summary, When I go to a page with calculated summary piping, Then I should the see the piped calculated summary total for each summary", async ()=> {
      await $(await SecondCurrencyTotalPlaybackPage.submit()).click();

      const content = $("h1 + ul").getText();
      const textsToAssert = [
        "Total currency values (if Q4 not skipped): £28.37",
        "Total currency values (if Q4 skipped)): £9.36",
        "Total unit values: 1,467",
        "Total percentage values: 79",
        "Total number values: 124.58",
      ];

      textsToAssert.forEachasync (async (text) => await expectasync (content).to.containasync (text));
    });

    it("Given I have an answer minimum based on a calculated summary total, When I enter an invalid answer, Then I should see an error message on the page", async ()=> {
      await $(await CalculatedSummaryTotalConfirmation.submit()).click();
      await expect(browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      await $(await SetMinMaxBlockPage.setMinimum()).setValue(8.0);
      await $(await SetMinMaxBlockPage.submit()).click();
      await expect(await $(await SetMinMaxBlockPage.errorNumber(1)).getText()).to.contain("Enter an answer more than or equal to £9.36");
      await $(await SetMinMaxBlockPage.setMinimum()).setValue(10.0);
      await $(await SetMinMaxBlockPage.submit()).click();
    });

    it("Given I have an answer maximum based on a calculated summary total, When I enter an invalid answer, Then I should see an error message on the page", async ()=> {
      await $(await SubmitPage.submit()).click();
      await expect(browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      await $(await SetMinMaxBlockPage.setMaximum()).setValue(10.0);
      await $(await SetMinMaxBlockPage.submit()).click();
      await expect(await $(await SetMinMaxBlockPage.errorNumber(1)).getText()).to.contain("Enter an answer less than or equal to £9.36");
      await $(await SetMinMaxBlockPage.setMaximum()).setValue(7.0);
      await $(await SetMinMaxBlockPage.submit()).click();
    });

    it("Given I confirm the totals and am on the summary, When I edit and change an answer, Then I must re-confirm the dependant calculated summary page and min max question page before I can return to the summary", async ()=> {
      await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      await $(await SubmitPage.thirdNumberAnswerEdit()).click();
      await $(await ThirdNumberBlockPage.thirdNumber()).setValue(3.5);
      await $(await ThirdNumberBlockPage.submit()).click();
      await $(await ThirdAndAHalfNumberBlockPage.submit()).click();
      await $(await SkipFourthBlockPage.submit()).click();
      await $(await FifthNumberBlockPage.submit()).click();
      await $(await SixthNumberBlockPage.submit()).click();

      await expect(await $(await CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £9.41. Is this correct?"
      );

      await $(await CurrencyTotalPlaybackPageSkippedFourth.submit()).click();
      await $(await UnitTotalPlaybackPage.submit()).click();
      await $(await PercentageTotalPlaybackPage.submit()).click();
      await $(await NumberTotalPlaybackPage.submit()).click();
      await $(await BreakdownPage.submit()).click();
      await $(await SecondCurrencyTotalPlaybackPage.submit()).click();
      await $(await CalculatedSummaryTotalConfirmation.submit()).click();
      await expect(browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      await $(await SetMinMaxBlockPage.setMinimum()).setValue(10.0);
      await $(await SetMinMaxBlockPage.setMaximum()).setValue(9.0);
      await $(await SetMinMaxBlockPage.submit()).click();
      await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("Given I confirm the totals and am on the summary, When I edit and change an answer that has a dependent minimum value from a calculated summary total, And the minimum value has been changed, Then I must re-validate before I get to the summary", async ()=> {
      await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      await $(await SubmitPage.thirdNumberAnswerEdit()).click();
      await $(await ThirdNumberBlockPage.thirdNumber()).setValue(10.0);
      await $(await ThirdNumberBlockPage.submit()).click();
      await $(await ThirdAndAHalfNumberBlockPage.submit()).click();
      await $(await SkipFourthBlockPage.submit()).click();
      await $(await FifthNumberBlockPage.submit()).click();
      await $(await SixthNumberBlockPage.submit()).click();

      await expect(await $(await CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £15.91. Is this correct?"
      );

      await $(await CurrencyTotalPlaybackPageSkippedFourth.submit()).click();
      await $(await UnitTotalPlaybackPage.submit()).click();
      await $(await PercentageTotalPlaybackPage.submit()).click();
      await $(await NumberTotalPlaybackPage.submit()).click();
      await $(await BreakdownPage.submit()).click();
      await $(await SecondCurrencyTotalPlaybackPage.submit()).click();
      await $(await CalculatedSummaryTotalConfirmation.submit()).click();
      await expect(browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      await $(await SetMinMaxBlockPage.submit()).click();
      await expect(await $(await SetMinMaxBlockPage.errorNumber(1)).getText()).to.contain("Enter an answer more than or equal to £15.91");
      await $(await SetMinMaxBlockPage.setMinimum()).setValue(16.0);
      await $(await SetMinMaxBlockPage.submit()).click();
      await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("Given I confirm the totals and am on the summary, When I edit and change an answer that has a dependent maximum value from a calculated summary total, And the maximum value has been changed, Then I must re-validate before I get to the summary", async ()=> {
      await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      await $(await SubmitPage.thirdNumberAnswerEdit()).click();
      await $(await ThirdNumberBlockPage.thirdNumber()).setValue(1.0);
      await $(await ThirdNumberBlockPage.submit()).click();
      await $(await ThirdAndAHalfNumberBlockPage.submit()).click();
      await $(await SkipFourthBlockPage.submit()).click();
      await $(await FifthNumberBlockPage.submit()).click();
      await $(await SixthNumberBlockPage.submit()).click();

      await expect(await $(await CurrencyTotalPlaybackPageSkippedFourth.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £6.91. Is this correct?"
      );

      await $(await CurrencyTotalPlaybackPageSkippedFourth.submit()).click();
      await $(await UnitTotalPlaybackPage.submit()).click();
      await $(await PercentageTotalPlaybackPage.submit()).click();
      await $(await NumberTotalPlaybackPage.submit()).click();
      await $(await BreakdownPage.submit()).click();
      await $(await SecondCurrencyTotalPlaybackPage.submit()).click();
      await $(await CalculatedSummaryTotalConfirmation.submit()).click();
      await expect(browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      await $(await SetMinMaxBlockPage.submit()).click();
      await expect(await $(await SetMinMaxBlockPage.errorNumber(1)).getText()).to.contain("Enter an answer less than or equal to £6.91");
      await $(await SetMinMaxBlockPage.setMaximum()).setValue(6.0);
      await $(await SetMinMaxBlockPage.submit()).click();
      await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("Given I am on the summary, When I submit the questionnaire, Then I should see the thank you page", async ()=> {
      await $(await SubmitPage.submit()).click();
      await $(await HubPage.submit()).click();
      await expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    });
  });

  describe("Given I have a Calculated Summary in a Repeating Section", () => {
    before("Get to Final Summary", async ()=> {
      await browser.openQuestionnaire("test_new_calculated_summary_repeating_section.json");
      await $(await HubPage.submit()).click();
      await $(await PrimaryPersonListCollectorPage.no()).click();
      await $(await PrimaryPersonListCollectorPage.submit()).click();
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Jean");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Jane");
      await $(await ListCollectorAddPage.lastName()).setValue("Doe");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.no()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await HubPage.submit()).click();
      getToFirstCalculatedSummary();
      getToSubmitPage();
      await $(await SubmitPage.submit()).click();
      await $(await HubPage.submit()).click();
      getToFirstCalculatedSummary();
      getToSubmitPage();
      await $(await SubmitPage.submit()).click();
    });

    it("Given I am on the submit page, When I have completed two repeating sections containing a calculated summary, Then the section status for both repeating sections should be complete", async ()=> {
      await expect(browser.getUrl()).to.contain(HubPage.pageName);
      await expect(await $(await HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Completed");
      await expect(await $(await HubPage.summaryRowState("personal-details-section-2")).getText()).to.equal("Completed");
    });

    it("Given I change an answer with a dependent calculated summary question, When I return to the hub, Then only the section status for the repeating section I updated should be incomplete", async ()=> {
      await expect(browser.getUrl()).to.contain(HubPage.pageName);
      await $(await HubPage.summaryRowLink("personal-details-section-1")).click();
      await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      await $(await SubmitPage.skipFourthBlockAnswerEdit()).click();
      await $(await SkipFourthBlockPage.yes()).click();
      await $(await SkipFourthBlockPage.submit()).click();
      browser.url(HubPage.url());
      await expect(await $(await HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Partially completed");
      await expect(await $(await HubPage.summaryRowState("personal-details-section-2")).getText()).to.equal("Completed");
    });

    it("Given I return to a partially completed section with a calculated summary, When I answer the dependent questions and return to the hub, Then the section status for the repeating section I updated should be complete", async ()=> {
      await expect(browser.getUrl()).to.contain(HubPage.pageName);
      await expect(await $(await HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Partially completed");
      await $(await HubPage.summaryRowLink("personal-details-section-1")).click();
      await expect(browser.getUrl()).to.contain(CurrencyTotalPlaybackPageSkippedFourth.pageName);
      await $(await CurrencyTotalPlaybackPageSkippedFourth.submit()).click();
      await $(await UnitTotalPlaybackPage.submit()).click();
      await $(await PercentageTotalPlaybackPage.submit()).click();
      await $(await NumberTotalPlaybackPage.submit()).click();
      await $(await BreakdownPage.submit()).click();
      await $(await SecondCurrencyTotalPlaybackPage.submit()).click();
      await $(await CalculatedSummaryTotalConfirmation.submit()).click();
      await $(await SetMinMaxBlockPage.setMinimum()).setValue(10.0);
      await $(await SetMinMaxBlockPage.setMaximum()).setValue(6.0);
      await $(await SetMinMaxBlockPage.submit()).click();
      await $(await SubmitPage.submit()).click();
      await expect(browser.getUrl()).to.contain(HubPage.pageName);
      await expect(await $(await HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Completed");
      await expect(await $(await HubPage.summaryRowState("personal-details-section-2")).getText()).to.equal("Completed");
    });
  });
});

const getToFirstCalculatedSummary = async ()=> {
  await $(await FirstNumberBlockPage.firstNumber()).setValue(1.23);
  await $(await FirstNumberBlockPage.submit()).click();

  await $(await SecondNumberBlockPage.secondNumber()).setValue(4.56);
  await $(await SecondNumberBlockPage.secondNumberUnitTotal()).setValue(789);
  await $(await SecondNumberBlockPage.secondNumberAlsoInTotal()).setValue(0.12);
  await $(await SecondNumberBlockPage.submit()).click();

  await $(await ThirdNumberBlockPage.thirdNumber()).setValue(3.45);
  await $(await ThirdNumberBlockPage.submit()).click();
  await $(await ThirdAndAHalfNumberBlockPage.thirdAndAHalfNumberUnitTotal()).setValue(678);
  await $(await ThirdAndAHalfNumberBlockPage.submit()).click();

  await $(await SkipFourthBlockPage.no()).click();
  await $(await SkipFourthBlockPage.submit()).click();

  await $(await FourthNumberBlockPage.fourthNumber()).setValue(9.01);
  await $(await FourthNumberBlockPage.submit()).click();
  await $(await FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal()).setValue(2.34);
  await $(await FourthAndAHalfNumberBlockPage.submit()).click();

  await $(await FifthNumberBlockPage.fifthPercent()).setValue(56);
  await $(await FifthNumberBlockPage.fifthNumber()).setValue(78.91);
  await $(await FifthNumberBlockPage.submit()).click();

  await $(await SixthNumberBlockPage.sixthPercent()).setValue(23);
  await $(await SixthNumberBlockPage.sixthNumber()).setValue(45.67);
  await $(await SixthNumberBlockPage.submit()).click();
};

const getToSubmitPage = async ()=> {
  await $(await CurrencyTotalPlaybackPageSkippedFourth.submit()).click();
  await $(await UnitTotalPlaybackPage.submit()).click();
  await $(await PercentageTotalPlaybackPage.submit()).click();
  await $(await NumberTotalPlaybackPage.submit()).click();
  await $(await BreakdownPage.answer1()).setValue(100.0);
  await $(await BreakdownPage.answer2()).setValue(24.58);
  await $(await BreakdownPage.submit()).click();
  await $(await SecondCurrencyTotalPlaybackPage.submit()).click();
  await $(await CalculatedSummaryTotalConfirmation.submit()).click();
};
