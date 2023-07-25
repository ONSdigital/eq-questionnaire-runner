import FirstNumberBlockPage from "../../../generated_pages/new_calculated_summary_repeating_section/first-number-block.page.js";
import SecondNumberBlockPage from "../../../generated_pages/new_calculated_summary_repeating_section/second-number-block.page.js";
import ThirdNumberBlockPage from "../../../generated_pages/new_calculated_summary_repeating_section/third-number-block.page.js";
import ThirdAndAHalfNumberBlockPage from "../../../generated_pages/new_calculated_summary_repeating_section/third-and-a-half-number-block.page.js";
import SkipFourthBlockPage from "../../../generated_pages/new_calculated_summary_repeating_section/skip-fourth-block.page.js";
import FourthNumberBlockPage from "../../../generated_pages/new_calculated_summary_repeating_section/fourth-number-block.page.js";
import FourthAndAHalfNumberBlockPage from "../../../generated_pages/new_calculated_summary_repeating_section/fourth-and-a-half-number-block.page.js";
import FifthNumberBlockPage from "../../../generated_pages/new_calculated_summary_repeating_section/fifth-number-block.page.js";
import SixthNumberBlockPage from "../../../generated_pages/new_calculated_summary_repeating_section/sixth-number-block.page.js";
import CurrencyTotalPlaybackPage from "../../../generated_pages/new_calculated_summary_repeating_section/currency-total-playback.page.js";
import SetMinMaxBlockPage from "../../../generated_pages/new_calculated_summary_repeating_section/set-min-max-block.page.js";
import UnitTotalPlaybackPage from "../../../generated_pages/new_calculated_summary_repeating_section/unit-total-playback.page.js";
import PercentageTotalPlaybackPage from "../../../generated_pages/new_calculated_summary_repeating_section/percentage-total-playback.page.js";
import NumberTotalPlaybackPage from "../../../generated_pages/new_calculated_summary_repeating_section/number-total-playback.page.js";
import BreakdownPage from "../../../generated_pages/new_calculated_summary_repeating_section/breakdown.page.js";
import SecondCurrencyTotalPlaybackPage from "../../../generated_pages/new_calculated_summary_repeating_section/second-currency-total-playback.page.js";
import CalculatedSummaryTotalConfirmation from "../../../generated_pages/new_calculated_summary_repeating_section/calculated-summary-total-confirmation.page.js";
import SubmitPage from "../../../generated_pages/new_calculated_summary_repeating_section/personal-details-section-summary.page.js";
import ThankYouPage from "../../../base_pages/thank-you.page.js";
import HubPage from "../../../base_pages/hub.page.js";
import PrimaryPersonListCollectorPage from "../../../generated_pages/new_calculated_summary_repeating_section/primary-person-list-collector.page";
import PrimaryPersonListCollectorAddPage from "../../../generated_pages/new_calculated_summary_repeating_section/primary-person-list-collector-add.page.js";
import ListCollectorPage from "../../../generated_pages/new_calculated_summary_repeating_section/list-collector.page";
import ListCollectorAddPage from "../../../generated_pages/new_calculated_summary_repeating_section/list-collector-add.page";
import SkipFirstNumberBlockPageSectionOne from "../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/skip-first-block.page";
import FirstNumberBlockPageSectionOne from "../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/first-number-block.page";
import FirstAndAHalfNumberBlockPageSectionOne from "../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/first-and-a-half-number-block.page";
import SecondNumberBlockPageSectionOne from "../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/second-number-block.page";
import CalculatedSummarySectionOne from "../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/currency-total-playback-1.page";
import CalculatedSummarySectionTwo from "../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/currency-total-playback-2.page";
import ThirdNumberBlockPageSectionTwo from "../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/third-number-block.page";
import SectionSummarySectionOne from "../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/questions-section-summary.page";
import SectionSummarySectionTwo from "../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/calculated-summary-section-summary.page";
import DependencyQuestionSectionTwo from "../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/mutually-exclusive-checkbox.page";
import MinMaxSectionTwo from "../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/set-min-max-block.page";

describe("Feature: Calculated Summary Repeating Section", () => {
  describe("Given I have a Calculated Summary in a Repeating Section", () => {
    before("Get to Calculated Summary", async () => {
      await browser.openQuestionnaire("test_new_calculated_summary_repeating_section.json");
      await $(HubPage.submit()).click();
      await $(PrimaryPersonListCollectorPage.yes()).click();
      await $(PrimaryPersonListCollectorPage.submit()).click();
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await $(PrimaryPersonListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();
      await $(HubPage.submit()).click();

      await getToFirstCalculatedSummary();

      const browserUrl = await browser.getUrl();

      await expect(await browserUrl).to.contain(CurrencyTotalPlaybackPage.pageName);
    });

    it("Given I have completed all questions, When I am on the calculated summary and there is no custom page title, Then the page title should use the calculation's title", async () => {
      await expect(await browser.getTitle()).to.equal("Grand total of previous values - A test schema to demo Calculated Summary");
    });

    it("Given I complete every question, When I get to the currency summary, Then I should see the correct total", async () => {
      // Totals and titles should be shown
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £20.71. Is this correct?"
      );
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain("Grand total of previous values");
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("£20.71");

      // Answers included in calculation should be shown
      await expect(await $(CurrencyTotalPlaybackPage.firstNumberAnswerLabel()).getText()).to.contain("First answer label");
      await expect(await $(CurrencyTotalPlaybackPage.firstNumberAnswer()).getText()).to.contain("£1.23");
      await expect(await $(CurrencyTotalPlaybackPage.secondNumberAnswerLabel()).getText()).to.contain("Second answer in currency label");
      await expect(await $(CurrencyTotalPlaybackPage.secondNumberAnswer()).getText()).to.contain("£4.56");
      await expect(await $(CurrencyTotalPlaybackPage.secondNumberAnswerAlsoInTotalLabel()).getText()).to.contain(
        "Second answer label also in currency total (optional)"
      );
      await expect(await $(CurrencyTotalPlaybackPage.secondNumberAnswerAlsoInTotal()).getText()).to.contain("£0.12");
      await expect(await $(CurrencyTotalPlaybackPage.thirdNumberAnswerLabel()).getText()).to.contain("Third answer label");
      await expect(await $(CurrencyTotalPlaybackPage.thirdNumberAnswer()).getText()).to.contain("£3.45");
      await expect(await $(CurrencyTotalPlaybackPage.fourthNumberAnswerLabel()).getText()).to.contain("Fourth answer label (optional)");
      await expect(await $(CurrencyTotalPlaybackPage.fourthNumberAnswer()).getText()).to.contain("£9.01");
      await expect(await $(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotalLabel()).getText()).to.contain(
        "Fourth answer label also in total (optional)"
      );
      await expect(await $(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotal()).getText()).to.contain("£2.34");

      // Answers not included in calculation should not be shown
      await expect(await $$(UnitTotalPlaybackPage.secondNumberAnswerUnitTotal())).to.be.empty;
      await expect(await $$(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal())).to.be.empty;
      await expect(await $$(NumberTotalPlaybackPage.fifthNumberAnswer())).to.be.empty;
      await expect(await $$(NumberTotalPlaybackPage.sixthNumberAnswer())).to.be.empty;
    });

    it("Given I reach the calculated summary page, Then the Change link url should contain return_to, return_to_answer_id and return_to_block_id query params", async () => {
      await expect(await $(CurrencyTotalPlaybackPage.firstNumberAnswerEdit()).getAttribute("href")).to.contain(
        "first-number-block/?return_to=calculated-summary&return_to_answer_id=first-number-answer&return_to_block_id=currency-total-playback#first-number-answer"
      );
    });

    it("Given I edit an answer from the calculated summary page and click the Previous button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing", async () => {
      await $(CurrencyTotalPlaybackPage.thirdNumberAnswerEdit()).click();
      await $(ThirdNumberBlockPage.previous()).click();
      await expect(await browser.getUrl()).to.contain("currency-total-playback/?return_to=calculated-summary#third-number-answer");
    });

    it("Given I edit an answer from the calculated summary page and click the Submit button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing", async () => {
      await $(CurrencyTotalPlaybackPage.thirdNumberAnswerEdit()).click();
      await $(ThirdNumberBlockPage.submit()).click();
      await expect(await browser.getUrl()).to.contain("currency-total-playback/?return_to=calculated-summary#third-number-answer");
    });

    it("Given I change an answer, When I get to the currency summary, Then I should see the new total", async () => {
      await $(CurrencyTotalPlaybackPage.fourthNumberAnswerEdit()).click();
      await $(FourthNumberBlockPage.fourthNumber()).setValue(19.01);
      await $(FourthNumberBlockPage.submit()).click();

      await expect(await browser.getUrl()).to.contain(CurrencyTotalPlaybackPage.pageName);
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £30.71. Is this correct?"
      );
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("£30.71");
    });

    it("Given I leave an answer empty, When I get to the currency summary, Then I should see no answer provided and new total", async () => {
      await $(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotalEdit()).click();
      await $(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal()).setValue("");
      await $(FourthAndAHalfNumberBlockPage.submit()).click();

      await expect(await browser.getUrl()).to.contain(CurrencyTotalPlaybackPage.pageName);
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £28.37. Is this correct?"
      );
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("£28.37");
      await expect(await $(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotal()).getText()).to.contain("No answer provided");
    });

    it("Given I skip the fourth page, When I get to the playback, Then I can should not see it in the total", async () => {
      await $(CurrencyTotalPlaybackPage.previous()).click();
      await $(SixthNumberBlockPage.previous()).click();
      await $(FifthNumberBlockPage.previous()).click();
      await $(FourthAndAHalfNumberBlockPage.previous()).click();
      await $(FourthNumberBlockPage.previous()).click();

      await $(SkipFourthBlockPage.yes()).click();
      await $(SkipFourthBlockPage.submit()).click();

      await $(FifthNumberBlockPage.submit()).click();
      await $(SixthNumberBlockPage.submit()).click();

      const expectedUrl = await browser.getUrl();

      await expect(expectedUrl).to.contain(CurrencyTotalPlaybackPage.pageName);
      await expect(await $$(CurrencyTotalPlaybackPage.fourthNumberAnswer())).to.be.empty;
      await expect(await $$(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotal())).to.be.empty;
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £9.36. Is this correct?"
      );
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("£9.36");
    });

    it("Given I complete every question, When I get to the unit summary, Then I should see the correct total", async () => {
      // Totals and titles should be shown
      await $(CurrencyTotalPlaybackPage.submit()).click();
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

    it("Given the calculated summary has a custom title with the list item position, When I am on the percentage calculated summary, Then the page title should use the custom title with the list item position", async () => {
      await expect(await browser.getTitle()).to.equal("Percentage Calculated Summary: Person 1 - A test schema to demo Calculated Summary");
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

    it("Given I have a calculated summary total that is used as a placeholder in another calculated summary, When I get to the calculated summary page displaying the placeholder, Then I should see the correct total", async () => {
      await $(NumberTotalPlaybackPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(BreakdownPage.pageName);
      await $(BreakdownPage.answer1()).setValue(100.0);
      await $(BreakdownPage.answer2()).setValue(24.58);
      await $(BreakdownPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(SecondCurrencyTotalPlaybackPage.pageName);
      await expect(await $(SecondCurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of number values entered to be £124.58. Is this correct?"
      );
      await expect(await $("body").getText()).to.have.string("Enter two values that add up to the previous calculated summary total of £124.58");
      await expect(await $(SecondCurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("124.58");
    });

    it("Given I complete every calculated summary, When I go to a page with calculated summary piping, Then I should the see the piped calculated summary total for each summary", async () => {
      await $(SecondCurrencyTotalPlaybackPage.submit()).click();

      const content = $("h1 + ul").getText();
      const textsToAssert = ["Total currency values: £9.36", "Total unit values: 1,467", "Total percentage values: 79", "Total number values: 124.58"];

      textsToAssert.forEach(async (text) => await expect(content).to.contain(text));
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

      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £9.41. Is this correct?"
      );

      await $(CurrencyTotalPlaybackPage.submit()).click();
      await $(UnitTotalPlaybackPage.submit()).click();
      await $(PercentageTotalPlaybackPage.submit()).click();
      await $(NumberTotalPlaybackPage.submit()).click();
      await $(BreakdownPage.submit()).click();
      await $(SecondCurrencyTotalPlaybackPage.submit()).click();
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

      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £15.91. Is this correct?"
      );

      await $(CurrencyTotalPlaybackPage.submit()).click();
      await $(UnitTotalPlaybackPage.submit()).click();
      await $(PercentageTotalPlaybackPage.submit()).click();
      await $(NumberTotalPlaybackPage.submit()).click();
      await $(BreakdownPage.submit()).click();
      await $(SecondCurrencyTotalPlaybackPage.submit()).click();
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

      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £6.91. Is this correct?"
      );

      await $(CurrencyTotalPlaybackPage.submit()).click();
      await $(UnitTotalPlaybackPage.submit()).click();
      await $(PercentageTotalPlaybackPage.submit()).click();
      await $(NumberTotalPlaybackPage.submit()).click();
      await $(BreakdownPage.submit()).click();
      await $(SecondCurrencyTotalPlaybackPage.submit()).click();
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
      await $(HubPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(ThankYouPage.pageName);
    });
  });

  describe("Given I have a Calculated Summary in a Repeating Section", async () => {
    before("Get to Final Summary", async () => {
      await browser.openQuestionnaire("test_new_calculated_summary_repeating_section.json");
      await $(HubPage.submit()).click();
      await $(PrimaryPersonListCollectorPage.no()).click();
      await $(PrimaryPersonListCollectorPage.submit()).click();
      await $(ListCollectorPage.yes()).click();
      await $(ListCollectorPage.submit()).click();
      await $(ListCollectorAddPage.firstName()).setValue("Jean");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(ListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.yes()).click();
      await $(ListCollectorPage.submit()).click();
      await $(ListCollectorAddPage.firstName()).setValue("Jane");
      await $(ListCollectorAddPage.lastName()).setValue("Doe");
      await $(ListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();
      await $(HubPage.submit()).click();
      await getToFirstCalculatedSummary();
      await getToSubmitPage();
      await $(SubmitPage.submit()).click();
      await $(HubPage.submit()).click();
      await getToFirstCalculatedSummary();
      await getToSubmitPage();
      await $(SubmitPage.submit()).click();
    });

    it("Given I am on the submit page, When I have completed two repeating sections containing a calculated summary, Then the section status for both repeating sections should be complete", async () => {
      await expect(await browser.getUrl()).to.contain(HubPage.pageName);
      await expect(await $(HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Completed");
      await expect(await $(HubPage.summaryRowState("personal-details-section-2")).getText()).to.equal("Completed");
    });

    it("Given I change an answer with a dependent calculated summary question, When I return to the hub, Then only the section status for the repeating section I updated should be incomplete", async () => {
      await expect(await browser.getUrl()).to.contain(HubPage.pageName);
      await $(HubPage.summaryRowLink("personal-details-section-1")).click();
      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
      await $(SubmitPage.skipFourthBlockAnswerEdit()).click();
      await $(SkipFourthBlockPage.yes()).click();
      await $(SkipFourthBlockPage.submit()).click();
      await browser.url(HubPage.url());
      await expect(await $(HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Partially completed");
      await expect(await $(HubPage.summaryRowState("personal-details-section-2")).getText()).to.equal("Completed");
    });

    it("Given I return to a partially completed section with a calculated summary, When I answer the dependent questions and return to the hub, Then the section status for the repeating section I updated should be complete", async () => {
      await expect(await browser.getUrl()).to.contain(HubPage.pageName);
      await expect(await $(HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Partially completed");
      await $(HubPage.summaryRowLink("personal-details-section-1")).click();
      await expect(await browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      await $(SetMinMaxBlockPage.setMinimum()).setValue(10.0);
      await $(SetMinMaxBlockPage.setMaximum()).setValue(6.0);
      await $(SetMinMaxBlockPage.submit()).click();
      await $(SubmitPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(HubPage.pageName);
      await expect(await $(HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Completed");
      await expect(await $(HubPage.summaryRowState("personal-details-section-2")).getText()).to.equal("Completed");
    });
  });

  describe("Given I have a Calculated Summary in a Repeating Section with a Dependency based on a calculated summary in another section", () => {
    before("Get to the Dependent question page", async () => {
      await browser.openQuestionnaire("test_new_calculated_summary_cross_section_dependencies_repeating.json");
      await $(HubPage.submit()).click();
      await $(PrimaryPersonListCollectorPage.yes()).click();
      await $(PrimaryPersonListCollectorPage.submit()).click();
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await $(PrimaryPersonListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();
      await $(HubPage.submit()).click();

      await $(SkipFirstNumberBlockPageSectionOne.no()).click();
      await $(SkipFirstNumberBlockPageSectionOne.submit()).click();
      await $(FirstNumberBlockPageSectionOne.firstNumber()).setValue(10);
      await $(FirstNumberBlockPageSectionOne.submit()).click();
      await $(FirstAndAHalfNumberBlockPageSectionOne.firstAndAHalfNumberAlsoInTotal()).setValue(20);
      await $(FirstAndAHalfNumberBlockPageSectionOne.submit()).click();
      await $(SecondNumberBlockPageSectionOne.secondNumberAlsoInTotal()).setValue(30);
      await $(SecondNumberBlockPageSectionOne.submit()).click();
      await $(CalculatedSummarySectionOne.submit()).click();
      await $(SectionSummarySectionOne.submit()).click();
      await $(HubPage.submit()).click();
      await $(ThirdNumberBlockPageSectionTwo.thirdNumber()).setValue(20);
      await $(ThirdNumberBlockPageSectionTwo.thirdNumberAlsoInTotal()).setValue(20);
      await $(ThirdNumberBlockPageSectionTwo.submit()).click();
      await $(CalculatedSummarySectionTwo.submit()).click();
    });

    it("Given I have a placeholder displaying a calculated summary value source, When the calculated summary value is from a previous section, Then the value displayed should be correct", async () => {
      await expect(await browser.getUrl()).to.contain(DependencyQuestionSectionTwo.pageName);
      await expect(await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue1Label()).getText()).to.contain(
        "60 - calculated summary answer (previous section)"
      );
      await expect(await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue2Label()).getText()).to.contain(
        "40 - calculated summary answer (current section)"
      );
    });

    it("Given I have validation using a calculated summary value source, When the calculated summary value is from a previous section, Then the value used to validate should be correct", async () => {
      await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue1()).click();
      await $(DependencyQuestionSectionTwo.submit()).click();
      await expect(await browser.getUrl()).to.contain(MinMaxSectionTwo.pageName);
      await $(MinMaxSectionTwo.setMinimum()).setValue(59.0);
      await $(MinMaxSectionTwo.setMaximum()).setValue(1.0);
      await $(MinMaxSectionTwo.submit()).click();
      await expect(await $(MinMaxSectionTwo.errorNumber(1)).getText()).to.contain("Enter an answer more than or equal to £60.00");
      await $(MinMaxSectionTwo.setMinimum()).setValue(61.0);
      await $(MinMaxSectionTwo.setMaximum()).setValue(40.0);
      await $(MinMaxSectionTwo.submit()).click();
    });

    it("Given I remove answers from the path for a calculated summary in a previous section by changing an answer, When I return to the question with the calculated summary value source, Then the value displayed should be correct", async () => {
      await $(SectionSummarySectionTwo.submit()).click();
      await $(HubPage.summaryRowLink("questions-section")).click();
      await $(SectionSummarySectionOne.skipFirstBlockAnswerEdit()).click();
      await $(SkipFirstNumberBlockPageSectionOne.yes()).click();
      await $(SkipFirstNumberBlockPageSectionOne.submit()).click();
      await $(SectionSummarySectionOne.submit()).click();
      await $(HubPage.summaryRowLink("calculated-summary-section-1")).click();
      await expect(await $("body").getText()).to.have.string("30 - calculated summary answer (previous section)");
      await $(SectionSummarySectionTwo.checkboxAnswerEdit()).click();
      await expect(await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue1Label()).getText()).to.contain(
        "30 - calculated summary answer (previous section)"
      );
      await expect(await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue2Label()).getText()).to.contain(
        "40 - calculated summary answer (current section)"
      );
    });
  });
});

const getToFirstCalculatedSummary = async () => {
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
};

const getToSubmitPage = async () => {
  await $(CurrencyTotalPlaybackPage.submit()).click();
  await $(UnitTotalPlaybackPage.submit()).click();
  await $(PercentageTotalPlaybackPage.submit()).click();
  await $(NumberTotalPlaybackPage.submit()).click();
  await $(BreakdownPage.answer1()).setValue(100.0);
  await $(BreakdownPage.answer2()).setValue(24.58);
  await $(BreakdownPage.submit()).click();
  await $(SecondCurrencyTotalPlaybackPage.submit()).click();
  await $(CalculatedSummaryTotalConfirmation.submit()).click();
};