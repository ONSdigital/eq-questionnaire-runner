import FirstNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/first-number-block.page.js";
import SecondNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/second-number-block.page.js";
import ThirdNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/third-number-block.page.js";
import ThirdAndAHalfNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/third-and-a-half-number-block.page.js";
import SkipFourthBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/skip-fourth-block.page.js";
import FourthNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/fourth-number-block.page.js";
import FourthAndAHalfNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/fourth-and-a-half-number-block.page.js";
import FifthNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/fifth-number-block.page.js";
import SixthNumberBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/sixth-number-block.page.js";
import CurrencyTotalPlaybackPage from "../../generated_pages/new_calculated_summary_repeating_section/currency-total-playback.page.js";
import SetMinMaxBlockPage from "../../generated_pages/new_calculated_summary_repeating_section/set-min-max-block.page.js";
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
import SkipFirstNumberBlockPageSectionOne from "../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/skip-first-block.page";
import FirstNumberBlockPageSectionOne from "../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/first-number-block.page";
import FirstAndAHalfNumberBlockPageSectionOne from "../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/first-and-a-half-number-block.page";
import SecondNumberBlockPageSectionOne from "../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/second-number-block.page";
import CalculatedSummarySectionOne from "../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/currency-total-playback-1.page";
import CalculatedSummarySectionTwo from "../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/currency-total-playback-2.page";
import ThirdNumberBlockPageSectionTwo from "../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/third-number-block.page";
import SectionSummarySectionOne from "../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/questions-section-summary.page";
import SectionSummarySectionTwo from "../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/calculated-summary-section-summary.page";
import DependencyQuestionSectionTwo from "../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/mutually-exclusive-checkbox.page";

describe("Feature: Calculated Summary Repeating Section", () => {
  describe("Given I have a Calculated Summary in a Repeating Section", () => {
    before("Get to Calculated Summary", () => {
      browser.openQuestionnaire("test_new_calculated_summary_repeating_section.json");
      $(HubPage.submit()).click();
      $(PrimaryPersonListCollectorPage.yes()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      $(PrimaryPersonListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      $(HubPage.submit()).click();

      getToFirstCalculatedSummary();

      const browserUrl = browser.getUrl();

      expect(browserUrl).to.contain(CurrencyTotalPlaybackPage.pageName);
    });

    it("Given I have completed all questions, When I am on the calculated summary and there is no custom page title, Then the page title should use the calculation's title", () => {
      expect(browser.getTitle()).to.equal("Grand total of previous values - A test schema to demo Calculated Summary");
    });

    it("Given I complete every question, When I get to the currency summary, Then I should see the correct total", () => {
      // Totals and titles should be shown
      expect($(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £20.71. Is this correct?"
      );
      expect($(CurrencyTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain("Grand total of previous values");
      expect($(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("£20.71");

      // Answers included in calculation should be shown
      expect($(CurrencyTotalPlaybackPage.firstNumberAnswerLabel()).getText()).to.contain("First answer label");
      expect($(CurrencyTotalPlaybackPage.firstNumberAnswer()).getText()).to.contain("£1.23");
      expect($(CurrencyTotalPlaybackPage.secondNumberAnswerLabel()).getText()).to.contain("Second answer in currency label");
      expect($(CurrencyTotalPlaybackPage.secondNumberAnswer()).getText()).to.contain("£4.56");
      expect($(CurrencyTotalPlaybackPage.secondNumberAnswerAlsoInTotalLabel()).getText()).to.contain("Second answer label also in currency total (optional)");
      expect($(CurrencyTotalPlaybackPage.secondNumberAnswerAlsoInTotal()).getText()).to.contain("£0.12");
      expect($(CurrencyTotalPlaybackPage.thirdNumberAnswerLabel()).getText()).to.contain("Third answer label");
      expect($(CurrencyTotalPlaybackPage.thirdNumberAnswer()).getText()).to.contain("£3.45");
      expect($(CurrencyTotalPlaybackPage.fourthNumberAnswerLabel()).getText()).to.contain("Fourth answer label (optional)");
      expect($(CurrencyTotalPlaybackPage.fourthNumberAnswer()).getText()).to.contain("£9.01");
      expect($(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotalLabel()).getText()).to.contain("Fourth answer label also in total (optional)");
      expect($(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotal()).getText()).to.contain("£2.34");

      // Answers not included in calculation should not be shown
      expect($$(UnitTotalPlaybackPage.secondNumberAnswerUnitTotal())).to.be.empty;
      expect($$(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal())).to.be.empty;
      expect($$(NumberTotalPlaybackPage.fifthNumberAnswer())).to.be.empty;
      expect($$(NumberTotalPlaybackPage.sixthNumberAnswer())).to.be.empty;
    });

    it("Given I reach the calculated summary page, Then the Change link url should contain return_to, return_to_answer_id and return_to_block_id query params", () => {
      expect($(CurrencyTotalPlaybackPage.firstNumberAnswerEdit()).getAttribute("href")).to.contain(
        "first-number-block/?return_to=calculated-summary&return_to_answer_id=first-number-answer&return_to_block_id=currency-total-playback#first-number-answer"
      );
    });

    it("Given I edit an answer from the calculated summary page and click the Previous button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing", () => {
      $(CurrencyTotalPlaybackPage.thirdNumberAnswerEdit()).click();
      $(ThirdNumberBlockPage.previous()).click();
      expect(browser.getUrl()).to.contain("currency-total-playback/?return_to=calculated-summary#third-number-answer");
    });

    it("Given I edit an answer from the calculated summary page and click the Submit button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing", () => {
      $(CurrencyTotalPlaybackPage.thirdNumberAnswerEdit()).click();
      $(ThirdNumberBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain("currency-total-playback/?return_to=calculated-summary#third-number-answer");
    });

    it("Given I change an answer, When I get to the currency summary, Then I should see the new total", () => {
      $(CurrencyTotalPlaybackPage.fourthNumberAnswerEdit()).click();
      $(FourthNumberBlockPage.fourthNumber()).setValue(19.01);
      $(FourthNumberBlockPage.submit()).click();

      expect(browser.getUrl()).to.contain(CurrencyTotalPlaybackPage.pageName);
      expect($(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £30.71. Is this correct?"
      );
      expect($(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("£30.71");
    });

    it("Given I leave an answer empty, When I get to the currency summary, Then I should see no answer provided and new total", () => {
      $(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotalEdit()).click();
      $(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal()).setValue("");
      $(FourthAndAHalfNumberBlockPage.submit()).click();

      expect(browser.getUrl()).to.contain(CurrencyTotalPlaybackPage.pageName);
      expect($(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £28.37. Is this correct?"
      );
      expect($(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("£28.37");
      expect($(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotal()).getText()).to.contain("No answer provided");
    });

    it("Given I skip the fourth page, When I get to the playback, Then I can should not see it in the total", () => {
      $(CurrencyTotalPlaybackPage.previous()).click();
      $(SixthNumberBlockPage.previous()).click();
      $(FifthNumberBlockPage.previous()).click();
      $(FourthAndAHalfNumberBlockPage.previous()).click();
      $(FourthNumberBlockPage.previous()).click();

      $(SkipFourthBlockPage.yes()).click();
      $(SkipFourthBlockPage.submit()).click();

      $(FifthNumberBlockPage.submit()).click();
      $(SixthNumberBlockPage.submit()).click();

      const expectedUrl = browser.getUrl();

      expect(expectedUrl).to.contain(CurrencyTotalPlaybackPage.pageName);
      expect($$(CurrencyTotalPlaybackPage.fourthNumberAnswer())).to.be.empty;
      expect($$(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotal())).to.be.empty;
      expect($(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £9.36. Is this correct?"
      );
      expect($(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("£9.36");
    });

    it("Given I complete every question, When I get to the unit summary, Then I should see the correct total", () => {
      // Totals and titles should be shown
      $(CurrencyTotalPlaybackPage.submit()).click();
      expect($(UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of unit values entered to be 1,467 cm. Is this correct?"
      );
      expect($(UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain("Grand total of previous values");
      expect($(UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("1,467 cm");

      // Answers included in calculation should be shown
      expect($(UnitTotalPlaybackPage.secondNumberAnswerUnitTotalLabel()).getText()).to.contain("Second answer label in unit total");
      expect($(UnitTotalPlaybackPage.secondNumberAnswerUnitTotal()).getText()).to.contain("789 cm");
      expect($(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotalLabel()).getText()).to.contain("Third answer label in unit total");
      expect($(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal()).getText()).to.contain("678 cm");
    });

    it("Given the calculated summary has a custom title, When I am on the unit calculated summary, Then the page title should use the custom title", () => {
      expect(browser.getTitle()).to.equal("Total Unit Values - A test schema to demo Calculated Summary");
    });

    it("Given I complete every question, When I get to the percentage summary, Then I should see the correct total", () => {
      // Totals and titles should be shown
      $(UnitTotalPlaybackPage.submit()).click();
      expect($(UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of percentage values entered to be 79%. Is this correct?"
      );
      expect($(UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain("Grand total of previous values");
      expect($(UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("79%");

      // Answers included in calculation should be shown
      expect($(PercentageTotalPlaybackPage.fifthPercentAnswerLabel()).getText()).to.contain("Fifth answer label percentage tota");
      expect($(PercentageTotalPlaybackPage.fifthPercentAnswer()).getText()).to.contain("56%");
      expect($(PercentageTotalPlaybackPage.sixthPercentAnswerLabel()).getText()).to.contain("Sixth answer label percentage tota");
      expect($(PercentageTotalPlaybackPage.sixthPercentAnswer()).getText()).to.contain("23%");
    });

    it("Given the calculated summary has a custom title with the list item position, When I am on the percentage calculated summary, Then the page title should use the custom title with the list item position", () => {
      expect(browser.getTitle()).to.equal("Percentage Calculated Summary: Person 1 - A test schema to demo Calculated Summary");
    });

    it("Given I complete every question, When I get to the number summary, Then I should see the correct total", () => {
      // Totals and titles should be shown
      $(UnitTotalPlaybackPage.submit()).click();
      expect($(UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of number values entered to be 124.58. Is this correct?"
      );
      expect($(UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).to.contain("Grand total of previous values");
      expect($(UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("124.58");

      // Answers included in calculation should be shown
      expect($(NumberTotalPlaybackPage.fifthNumberAnswerLabel()).getText()).to.contain("Fifth answer label number total");
      expect($(NumberTotalPlaybackPage.fifthNumberAnswer()).getText()).to.contain("78.91");
      expect($(NumberTotalPlaybackPage.sixthNumberAnswerLabel()).getText()).to.contain("Sixth answer label number total");
      expect($(NumberTotalPlaybackPage.sixthNumberAnswer()).getText()).to.contain("45.67");
    });

    it("Given I have a calculated summary total that is used as a placeholder in another calculated summary, When I get to the calculated summary page displaying the placeholder, Then I should see the correct total", () => {
      $(NumberTotalPlaybackPage.submit()).click();
      expect(browser.getUrl()).to.contain(BreakdownPage.pageName);
      $(BreakdownPage.answer1()).setValue(100.0);
      $(BreakdownPage.answer2()).setValue(24.58);
      $(BreakdownPage.submit()).click();
      expect(browser.getUrl()).to.contain(SecondCurrencyTotalPlaybackPage.pageName);
      expect($(SecondCurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of number values entered to be £124.58. Is this correct?"
      );
      expect($("body").getText()).to.have.string("Enter two values that add up to the previous calculated summary total of £124.58");
      expect($(SecondCurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).to.contain("124.58");
    });

    it("Given I complete every calculated summary, When I go to a page with calculated summary piping, Then I should the see the piped calculated summary total for each summary", () => {
      $(SecondCurrencyTotalPlaybackPage.submit()).click();

      const content = $("h1 + ul").getText();
      const textsToAssert = ["Total currency values: £9.36", "Total unit values: 1,467", "Total percentage values: 79", "Total number values: 124.58"];

      textsToAssert.forEach((text) => expect(content).to.contain(text));
    });

    it("Given I have an answer minimum based on a calculated summary total, When I enter an invalid answer, Then I should see an error message on the page", () => {
      $(CalculatedSummaryTotalConfirmation.submit()).click();
      expect(browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      $(SetMinMaxBlockPage.setMinimum()).setValue(8.0);
      $(SetMinMaxBlockPage.submit()).click();
      expect($(SetMinMaxBlockPage.errorNumber(1)).getText()).to.contain("Enter an answer more than or equal to £9.36");
      $(SetMinMaxBlockPage.setMinimum()).setValue(10.0);
      $(SetMinMaxBlockPage.submit()).click();
    });

    it("Given I have an answer maximum based on a calculated summary total, When I enter an invalid answer, Then I should see an error message on the page", () => {
      $(SubmitPage.submit()).click();
      expect(browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      $(SetMinMaxBlockPage.setMaximum()).setValue(10.0);
      $(SetMinMaxBlockPage.submit()).click();
      expect($(SetMinMaxBlockPage.errorNumber(1)).getText()).to.contain("Enter an answer less than or equal to £9.36");
      $(SetMinMaxBlockPage.setMaximum()).setValue(7.0);
      $(SetMinMaxBlockPage.submit()).click();
    });

    it("Given I confirm the totals and am on the summary, When I edit and change an answer, Then I must re-confirm the dependant calculated summary page and min max question page before I can return to the summary", () => {
      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      $(SubmitPage.thirdNumberAnswerEdit()).click();
      $(ThirdNumberBlockPage.thirdNumber()).setValue(3.5);
      $(ThirdNumberBlockPage.submit()).click();
      $(ThirdAndAHalfNumberBlockPage.submit()).click();
      $(SkipFourthBlockPage.submit()).click();
      $(FifthNumberBlockPage.submit()).click();
      $(SixthNumberBlockPage.submit()).click();

      expect($(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £9.41. Is this correct?"
      );

      $(CurrencyTotalPlaybackPage.submit()).click();
      $(UnitTotalPlaybackPage.submit()).click();
      $(PercentageTotalPlaybackPage.submit()).click();
      $(NumberTotalPlaybackPage.submit()).click();
      $(BreakdownPage.submit()).click();
      $(SecondCurrencyTotalPlaybackPage.submit()).click();
      $(CalculatedSummaryTotalConfirmation.submit()).click();
      expect(browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      $(SetMinMaxBlockPage.setMinimum()).setValue(10.0);
      $(SetMinMaxBlockPage.setMaximum()).setValue(9.0);
      $(SetMinMaxBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("Given I confirm the totals and am on the summary, When I edit and change an answer that has a dependent minimum value from a calculated summary total, And the minimum value has been changed, Then I must re-validate before I get to the summary", () => {
      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      $(SubmitPage.thirdNumberAnswerEdit()).click();
      $(ThirdNumberBlockPage.thirdNumber()).setValue(10.0);
      $(ThirdNumberBlockPage.submit()).click();
      $(ThirdAndAHalfNumberBlockPage.submit()).click();
      $(SkipFourthBlockPage.submit()).click();
      $(FifthNumberBlockPage.submit()).click();
      $(SixthNumberBlockPage.submit()).click();

      expect($(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £15.91. Is this correct?"
      );

      $(CurrencyTotalPlaybackPage.submit()).click();
      $(UnitTotalPlaybackPage.submit()).click();
      $(PercentageTotalPlaybackPage.submit()).click();
      $(NumberTotalPlaybackPage.submit()).click();
      $(BreakdownPage.submit()).click();
      $(SecondCurrencyTotalPlaybackPage.submit()).click();
      $(CalculatedSummaryTotalConfirmation.submit()).click();
      expect(browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      $(SetMinMaxBlockPage.submit()).click();
      expect($(SetMinMaxBlockPage.errorNumber(1)).getText()).to.contain("Enter an answer more than or equal to £15.91");
      $(SetMinMaxBlockPage.setMinimum()).setValue(16.0);
      $(SetMinMaxBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("Given I confirm the totals and am on the summary, When I edit and change an answer that has a dependent maximum value from a calculated summary total, And the maximum value has been changed, Then I must re-validate before I get to the summary", () => {
      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      $(SubmitPage.thirdNumberAnswerEdit()).click();
      $(ThirdNumberBlockPage.thirdNumber()).setValue(1.0);
      $(ThirdNumberBlockPage.submit()).click();
      $(ThirdAndAHalfNumberBlockPage.submit()).click();
      $(SkipFourthBlockPage.submit()).click();
      $(FifthNumberBlockPage.submit()).click();
      $(SixthNumberBlockPage.submit()).click();

      expect($(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).to.contain(
        "We calculate the total of currency values entered to be £6.91. Is this correct?"
      );

      $(CurrencyTotalPlaybackPage.submit()).click();
      $(UnitTotalPlaybackPage.submit()).click();
      $(PercentageTotalPlaybackPage.submit()).click();
      $(NumberTotalPlaybackPage.submit()).click();
      $(BreakdownPage.submit()).click();
      $(SecondCurrencyTotalPlaybackPage.submit()).click();
      $(CalculatedSummaryTotalConfirmation.submit()).click();
      expect(browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      $(SetMinMaxBlockPage.submit()).click();
      expect($(SetMinMaxBlockPage.errorNumber(1)).getText()).to.contain("Enter an answer less than or equal to £6.91");
      $(SetMinMaxBlockPage.setMaximum()).setValue(6.0);
      $(SetMinMaxBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("Given I am on the summary, When I submit the questionnaire, Then I should see the thank you page", () => {
      $(SubmitPage.submit()).click();
      $(HubPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    });
  });

  describe("Given I have a Calculated Summary in a Repeating Section", () => {
    before("Get to Final Summary", () => {
      browser.openQuestionnaire("test_new_calculated_summary_repeating_section.json");
      $(HubPage.submit()).click();
      $(PrimaryPersonListCollectorPage.no()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Jean");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Jane");
      $(ListCollectorAddPage.lastName()).setValue("Doe");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      $(HubPage.submit()).click();
      getToFirstCalculatedSummary();
      getToSubmitPage();
      $(SubmitPage.submit()).click();
      $(HubPage.submit()).click();
      getToFirstCalculatedSummary();
      getToSubmitPage();
      $(SubmitPage.submit()).click();
    });

    it("Given I am on the submit page, When I have completed two repeating sections containing a calculated summary, Then the section status for both repeating sections should be complete", () => {
      expect(browser.getUrl()).to.contain(HubPage.pageName);
      expect($(HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Completed");
      expect($(HubPage.summaryRowState("personal-details-section-2")).getText()).to.equal("Completed");
    });

    it("Given I change an answer with a dependent calculated summary question, When I return to the hub, Then only the section status for the repeating section I updated should be incomplete", () => {
      expect(browser.getUrl()).to.contain(HubPage.pageName);
      $(HubPage.summaryRowLink("personal-details-section-1")).click();
      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      $(SubmitPage.skipFourthBlockAnswerEdit()).click();
      $(SkipFourthBlockPage.yes()).click();
      $(SkipFourthBlockPage.submit()).click();
      browser.url(HubPage.url());
      expect($(HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Partially completed");
      expect($(HubPage.summaryRowState("personal-details-section-2")).getText()).to.equal("Completed");
    });

    it("Given I return to a partially completed section with a calculated summary, When I answer the dependent questions and return to the hub, Then the section status for the repeating section I updated should be complete", () => {
      expect(browser.getUrl()).to.contain(HubPage.pageName);
      expect($(HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Partially completed");
      $(HubPage.summaryRowLink("personal-details-section-1")).click();
      expect(browser.getUrl()).to.contain(SetMinMaxBlockPage.pageName);
      $(SetMinMaxBlockPage.setMinimum()).setValue(10.0);
      $(SetMinMaxBlockPage.setMaximum()).setValue(6.0);
      $(SetMinMaxBlockPage.submit()).click();
      $(SubmitPage.submit()).click();
      expect(browser.getUrl()).to.contain(HubPage.pageName);
      expect($(HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Completed");
      expect($(HubPage.summaryRowState("personal-details-section-2")).getText()).to.equal("Completed");
    });
  });

  describe("Given I have a Calculated Summary in a Repeating Section with a Dependency based on a calculated summary in another section", () => {
    before("Get to the Dependent question page", () => {
      browser.openQuestionnaire("test_new_calculated_summary_cross_section_dependencies_repeating.json");
      $(HubPage.submit()).click();
      $(PrimaryPersonListCollectorPage.yes()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      $(PrimaryPersonListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      $(HubPage.submit()).click();

      $(SkipFirstNumberBlockPageSectionOne.no()).click();
      $(SkipFirstNumberBlockPageSectionOne.submit()).click();
      $(FirstNumberBlockPageSectionOne.firstNumber()).setValue(10);
      $(FirstNumberBlockPageSectionOne.submit()).click();
      $(FirstAndAHalfNumberBlockPageSectionOne.firstAndAHalfNumberAlsoInTotal()).setValue(20);
      $(FirstAndAHalfNumberBlockPageSectionOne.submit()).click();
      $(SecondNumberBlockPageSectionOne.secondNumberAlsoInTotal()).setValue(30);
      $(SecondNumberBlockPageSectionOne.submit()).click();
      $(CalculatedSummarySectionOne.submit()).click();
      $(SectionSummarySectionOne.submit()).click();
      $(HubPage.submit()).click();
      $(ThirdNumberBlockPageSectionTwo.thirdNumber()).setValue(20);
      $(ThirdNumberBlockPageSectionTwo.thirdNumberAlsoInTotal()).setValue(20);
      $(ThirdNumberBlockPageSectionTwo.submit()).click();
      $(CalculatedSummarySectionTwo.submit()).click();
    });

    it("Given I have a placeholder displaying a calculated summary value source, When the calculated summary value is from a previous section, Then the value displayed should be correct", () => {
      expect(browser.getUrl()).to.contain(DependencyQuestionSectionTwo.pageName);
      expect($(DependencyQuestionSectionTwo.checkboxAnswerCalcValue1Label()).getText()).to.contain("60 - calculated summary answer (previous section)");
      expect($(DependencyQuestionSectionTwo.checkboxAnswerCalcValue2Label()).getText()).to.contain("40 - calculated summary answer (current section)");
    });

    it("Given I remove answers from the path for a calculated summary in a previous section by changing an answer, When I return to the question with the calculated summary value source, Then the value displayed should be correct", () => {
      $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue1()).click();
      $(DependencyQuestionSectionTwo.submit()).click();
      $(SectionSummarySectionTwo.submit()).click();
      $(HubPage.summaryRowLink("questions-section")).click();
      $(SectionSummarySectionOne.skipFirstBlockAnswerEdit()).click();
      $(SkipFirstNumberBlockPageSectionOne.yes()).click();
      $(SkipFirstNumberBlockPageSectionOne.submit()).click();
      $(SectionSummarySectionOne.submit()).click();
      $(HubPage.summaryRowLink("calculated-summary-section-1")).click();
      expect($("body").getText()).to.have.string("30 - calculated summary answer (previous section)");
      $(SectionSummarySectionTwo.checkboxAnswerEdit()).click();
      expect($(DependencyQuestionSectionTwo.checkboxAnswerCalcValue1Label()).getText()).to.contain("30 - calculated summary answer (previous section)");
      expect($(DependencyQuestionSectionTwo.checkboxAnswerCalcValue2Label()).getText()).to.contain("40 - calculated summary answer (current section)");
    });
  });
});

const getToFirstCalculatedSummary = () => {
  $(FirstNumberBlockPage.firstNumber()).setValue(1.23);
  $(FirstNumberBlockPage.submit()).click();

  $(SecondNumberBlockPage.secondNumber()).setValue(4.56);
  $(SecondNumberBlockPage.secondNumberUnitTotal()).setValue(789);
  $(SecondNumberBlockPage.secondNumberAlsoInTotal()).setValue(0.12);
  $(SecondNumberBlockPage.submit()).click();

  $(ThirdNumberBlockPage.thirdNumber()).setValue(3.45);
  $(ThirdNumberBlockPage.submit()).click();
  $(ThirdAndAHalfNumberBlockPage.thirdAndAHalfNumberUnitTotal()).setValue(678);
  $(ThirdAndAHalfNumberBlockPage.submit()).click();

  $(SkipFourthBlockPage.no()).click();
  $(SkipFourthBlockPage.submit()).click();

  $(FourthNumberBlockPage.fourthNumber()).setValue(9.01);
  $(FourthNumberBlockPage.submit()).click();
  $(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal()).setValue(2.34);
  $(FourthAndAHalfNumberBlockPage.submit()).click();

  $(FifthNumberBlockPage.fifthPercent()).setValue(56);
  $(FifthNumberBlockPage.fifthNumber()).setValue(78.91);
  $(FifthNumberBlockPage.submit()).click();

  $(SixthNumberBlockPage.sixthPercent()).setValue(23);
  $(SixthNumberBlockPage.sixthNumber()).setValue(45.67);
  $(SixthNumberBlockPage.submit()).click();
};

const getToSubmitPage = () => {
  $(CurrencyTotalPlaybackPage.submit()).click();
  $(UnitTotalPlaybackPage.submit()).click();
  $(PercentageTotalPlaybackPage.submit()).click();
  $(NumberTotalPlaybackPage.submit()).click();
  $(BreakdownPage.answer1()).setValue(100.0);
  $(BreakdownPage.answer2()).setValue(24.58);
  $(BreakdownPage.submit()).click();
  $(SecondCurrencyTotalPlaybackPage.submit()).click();
  $(CalculatedSummaryTotalConfirmation.submit()).click();
};
