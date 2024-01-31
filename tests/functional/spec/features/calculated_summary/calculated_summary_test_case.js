import CurrencyTotalPlaybackPage from "../../../generated_pages/calculated_summary/currency-total-playback.page";
import UnitTotalPlaybackPage from "../../../generated_pages/calculated_summary/unit-total-playback.page";
import NumberTotalPlaybackPage from "../../../generated_pages/calculated_summary/number-total-playback.page";
import ThirdNumberBlockPage from "../../../generated_pages/calculated_summary/third-number-block.page";
import FourthNumberBlockPage from "../../../generated_pages/calculated_summary/fourth-number-block.page";
import FourthAndAHalfNumberBlockPage from "../../../generated_pages/calculated_summary/fourth-and-a-half-number-block.page";
import SixthNumberBlockPage from "../../../generated_pages/calculated_summary/sixth-number-block.page";
import FifthNumberBlockPage from "../../../generated_pages/calculated_summary/fifth-number-block.page";
import SkipFourthBlockPage from "../../../generated_pages/calculated_summary/skip-fourth-block.page";
import PercentageTotalPlaybackPage from "../../../generated_pages/calculated_summary/percentage-total-playback.page";
import CalculatedSummaryTotalConfirmation from "../../../generated_pages/calculated_summary/calculated-summary-total-confirmation.page";
import SetMinMaxBlockPage from "../../../generated_pages/calculated_summary/set-min-max-block.page";
import SubmitPage from "../../../generated_pages/calculated_summary/submit.page";
import ThirdAndAHalfNumberBlockPage from "../../../generated_pages/calculated_summary/third-and-a-half-number-block.page";
import ThankYouPage from "../../../base_pages/thank-you.page";
import FirstNumberBlockPage from "../../../generated_pages/calculated_summary/first-number-block.page";
import SecondNumberBlockPage from "../../../generated_pages/calculated_summary/second-number-block.page";
import HubPage from "../../../base_pages/hub.page";
import SkipFirstNumberBlockPageSectionOne from "../../../generated_pages/calculated_summary_cross_section_dependencies/skip-first-block.page";
import FirstNumberBlockPageSectionOne from "../../../generated_pages/calculated_summary_cross_section_dependencies/first-number-block.page";
import FirstAndAHalfNumberBlockPageSectionOne from "../../../generated_pages/calculated_summary_cross_section_dependencies/first-and-a-half-number-block.page";
import SecondNumberBlockPageSectionOne from "../../../generated_pages/calculated_summary_cross_section_dependencies/second-number-block.page";
import CalculatedSummarySectionOne from "../../../generated_pages/calculated_summary_cross_section_dependencies/currency-total-playback-1.page";
import CalculatedSummarySectionTwo from "../../../generated_pages/calculated_summary_cross_section_dependencies/currency-total-playback-2.page";
import ThirdNumberBlockPageSectionTwo from "../../../generated_pages/calculated_summary_cross_section_dependencies/third-number-block.page";
import SectionSummarySectionOne from "../../../generated_pages/calculated_summary_cross_section_dependencies/questions-section-summary.page";
import SectionSummarySectionTwo from "../../../generated_pages/calculated_summary_cross_section_dependencies/calculated-summary-section-summary.page";
import DependencyQuestionSectionTwo from "../../../generated_pages/calculated_summary_cross_section_dependencies/mutually-exclusive-checkbox.page";
import MinMaxSectionTwo from "../../../generated_pages/calculated_summary_cross_section_dependencies/set-min-max-block.page";
import { assertSummaryValues, click } from "../../../helpers";
import { expect } from "@wdio/globals";

class TestCase {
  testCase(schema) {
    before("Get to Calculated Summary", async () => {
      await browser.openQuestionnaire(schema);

      await $(FirstNumberBlockPage.firstNumber()).setValue(1.23);
      await click(FirstNumberBlockPage.submit());

      await $(SecondNumberBlockPage.secondNumber()).setValue(4.56);
      await $(SecondNumberBlockPage.secondNumberUnitTotal()).setValue(789);
      await $(SecondNumberBlockPage.secondNumberAlsoInTotal()).setValue(0.12);
      await click(SecondNumberBlockPage.submit());

      await $(ThirdNumberBlockPage.thirdNumber()).setValue(3.45);
      await click(ThirdNumberBlockPage.submit());
      await $(ThirdAndAHalfNumberBlockPage.thirdAndAHalfNumberUnitTotal()).setValue(678);
      await click(ThirdAndAHalfNumberBlockPage.submit());

      await $(SkipFourthBlockPage.no()).click();
      await click(SkipFourthBlockPage.submit());

      await $(FourthNumberBlockPage.fourthNumber()).setValue(9.01);
      await click(FourthNumberBlockPage.submit());
      await $(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal()).setValue(2.34);
      await click(FourthAndAHalfNumberBlockPage.submit());

      await $(FifthNumberBlockPage.fifthPercent()).setValue(56);
      await $(FifthNumberBlockPage.fifthNumber()).setValue(78.91);
      await click(FifthNumberBlockPage.submit());

      await $(SixthNumberBlockPage.sixthPercent()).setValue(23);
      await $(SixthNumberBlockPage.sixthNumber()).setValue(45.67);
      await click(SixthNumberBlockPage.submit());

      await expect(await $(CurrencyTotalPlaybackPage.submit()).getText()).toBe("Yes, I confirm this is correct");
      await expect(browser).toHaveUrlContaining(CurrencyTotalPlaybackPage.pageName);
    });

    it("Given I have completed all questions, When I am on the calculated summary, Then the page title should use the calculation's title", async () => {
      await expect(await browser.getTitle()).toBe("Grand total of previous values - A test schema to demo Calculated Summary");
    });

    it("Given I complete every question, When I get to the currency summary, Then I should see the correct total", async () => {
      // Totals and titles should be shown
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).toBe(
        "We calculate the total of currency values entered to be £20.71. Is this correct?",
      );
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryQuestion()).getText()).toBe("Grand total of previous values");
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).toBe("£20.71");

      // Answers included in calculation should be shown
      await expect(await $(CurrencyTotalPlaybackPage.firstNumberAnswerLabel()).getText()).toBe("First answer label");
      await expect(await $(CurrencyTotalPlaybackPage.firstNumberAnswer()).getText()).toBe("£1.23");
      await expect(await $(CurrencyTotalPlaybackPage.secondNumberAnswerLabel()).getText()).toBe("Second answer in currency label");
      await expect(await $(CurrencyTotalPlaybackPage.secondNumberAnswer()).getText()).toBe("£4.56");
      await expect(await $(CurrencyTotalPlaybackPage.secondNumberAnswerAlsoInTotalLabel()).getText()).toBe(
        "Second answer label also in currency total (optional)",
      );
      await expect(await $(CurrencyTotalPlaybackPage.secondNumberAnswerAlsoInTotal()).getText()).toBe("£0.12");
      await expect(await $(CurrencyTotalPlaybackPage.thirdNumberAnswerLabel()).getText()).toBe("Third answer label");
      await expect(await $(CurrencyTotalPlaybackPage.thirdNumberAnswer()).getText()).toBe("£3.45");
      await expect(await $(CurrencyTotalPlaybackPage.fourthNumberAnswerLabel()).getText()).toBe("Fourth answer label (optional)");
      await expect(await $(CurrencyTotalPlaybackPage.fourthNumberAnswer()).getText()).toBe("£9.01");
      await expect(await $(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotalLabel()).getText()).toBe(
        "Fourth answer label also in total (optional)",
      );
      await expect(await $(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotal()).getText()).toBe("£2.34");

      // Answers not included in calculation should not be shown
      await expect(await $$(UnitTotalPlaybackPage.secondNumberAnswerUnitTotal())).toHaveLength(0);
      await expect(await $$(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal())).toHaveLength(0);
      await expect(await $$(NumberTotalPlaybackPage.fifthNumberAnswer())).toHaveLength(0);
      await expect(await $$(NumberTotalPlaybackPage.sixthNumberAnswer())).toHaveLength(0);
    });

    it("Given I reach the calculated summary page, Then the Change link url should contain return_to, return_to_answer_id and return_to_block_id query params", async () => {
      await expect(await $(CurrencyTotalPlaybackPage.firstNumberAnswerEdit()).getAttribute("href")).toContain(
        "/questionnaire/first-number-block/?return_to=calculated-summary&return_to_answer_id=first-number-answer&return_to_block_id=currency-total-playback#first-number-answer",
      );
    });

    it("Given I edit an answer from the calculated summary page and click the Previous button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing", async () => {
      await $(CurrencyTotalPlaybackPage.thirdNumberAnswerEdit()).click();
      await $(ThirdNumberBlockPage.previous()).click();
      await expect(browser).toHaveUrlContaining("currency-total-playback/#third-number-answer");
    });

    it("Given I edit an answer from the calculated summary page and click the Submit button, Then I am taken to the calculated summary page that I clicked the change link from and the browser url should contain an anchor referencing the answer id of the answer I am changing", async () => {
      await $(CurrencyTotalPlaybackPage.thirdNumberAnswerEdit()).click();
      await click(ThirdNumberBlockPage.submit());
      await expect(browser).toHaveUrlContaining("currency-total-playback/#third-number-answer");
    });

    it("Given I change an answer, When I get to the currency summary, Then I should see the new total", async () => {
      await $(CurrencyTotalPlaybackPage.fourthNumberAnswerEdit()).click();
      await $(FourthNumberBlockPage.fourthNumber()).setValue(19.01);
      await click(FourthNumberBlockPage.submit());

      await expect(browser).toHaveUrlContaining(CurrencyTotalPlaybackPage.pageName);
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).toBe(
        "We calculate the total of currency values entered to be £30.71. Is this correct?",
      );
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).toBe("£30.71");
    });

    it("Given I leave an answer empty, When I get to the currency summary, Then I should see no answer provided and new total", async () => {
      await $(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotalEdit()).click();
      await $(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal()).setValue("");
      await click(FourthAndAHalfNumberBlockPage.submit());

      await expect(browser).toHaveUrlContaining(CurrencyTotalPlaybackPage.pageName);
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).toBe(
        "We calculate the total of currency values entered to be £28.37. Is this correct?",
      );
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).toBe("£28.37");
      await expect(await $(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotal()).getText()).toBe("No answer provided");
    });

    it("Given I skip the fourth page, When I get to the playback, Then I can should not see it in the total", async () => {
      await $(CurrencyTotalPlaybackPage.previous()).click();
      await $(SixthNumberBlockPage.previous()).click();
      await $(FifthNumberBlockPage.previous()).click();
      await $(FourthAndAHalfNumberBlockPage.previous()).click();
      await $(FourthNumberBlockPage.previous()).click();

      await $(SkipFourthBlockPage.yes()).click();
      await click(SkipFourthBlockPage.submit());

      await click(FifthNumberBlockPage.submit());
      await click(SixthNumberBlockPage.submit());

      await expect(browser).toHaveUrlContaining(CurrencyTotalPlaybackPage.pageName);
      await expect(await $$(CurrencyTotalPlaybackPage.fourthNumberAnswer())).toHaveLength(0);
      await expect(await $$(CurrencyTotalPlaybackPage.fourthAndAHalfNumberAnswerAlsoInTotal())).toHaveLength(0);
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).toBe(
        "We calculate the total of currency values entered to be £9.36. Is this correct?",
      );
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).toBe("£9.36");
    });

    it("Given I complete every question, When I get to the unit summary, Then I should see the correct total", async () => {
      // Totals and titles should be shown
      await click(CurrencyTotalPlaybackPage.submit());
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).toBe(
        "We calculate the total of unit values entered to be 1,467 cm. Is this correct?",
      );
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).toBe("Grand total of previous values");
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).toBe("1,467 cm");

      // Answers included in calculation should be shown
      await expect(await $(UnitTotalPlaybackPage.secondNumberAnswerUnitTotalLabel()).getText()).toBe("Second answer label in unit total");
      await expect(await $(UnitTotalPlaybackPage.secondNumberAnswerUnitTotal()).getText()).toBe("789 cm");
      await expect(await $(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotalLabel()).getText()).toBe("Third answer label in unit total");
      await expect(await $(UnitTotalPlaybackPage.thirdAndAHalfNumberAnswerUnitTotal()).getText()).toBe("678 cm");
    });

    it("Given the calculated summary has a custom title, When I am on the unit calculated summary, Then the page title should use the custom title", async () => {
      await expect(await browser.getTitle()).toBe("Total Unit Values - A test schema to demo Calculated Summary");
    });

    it("Given I complete every question, When I get to the percentage summary, Then I should see the correct total", async () => {
      // Totals and titles should be shown
      await click(UnitTotalPlaybackPage.submit());
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).toBe(
        "We calculate the total of percentage values entered to be 79%. Is this correct?",
      );
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).toBe("Grand total of previous values");
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).toBe("79%");

      // Answers included in calculation should be shown
      await expect(await $(PercentageTotalPlaybackPage.fifthPercentAnswerLabel()).getText()).toBe("Fifth answer label percentage total");
      await expect(await $(PercentageTotalPlaybackPage.fifthPercentAnswer()).getText()).toBe("56%");
      await expect(await $(PercentageTotalPlaybackPage.sixthPercentAnswerLabel()).getText()).toBe("Sixth answer label percentage total");
      await expect(await $(PercentageTotalPlaybackPage.sixthPercentAnswer()).getText()).toBe("23%");
    });

    it("Given I complete every question, When I get to the number summary, Then I should see the correct total", async () => {
      // Totals and titles should be shown
      await click(UnitTotalPlaybackPage.submit());
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryTitle()).getText()).toBe(
        "We calculate the total of number values entered to be 124.58. Is this correct?",
      );
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryQuestion()).getText()).toBe("Grand total of previous values");
      await expect(await $(UnitTotalPlaybackPage.calculatedSummaryAnswer()).getText()).toBe("124.58");

      // Answers included in calculation should be shown
      await expect(await $(NumberTotalPlaybackPage.fifthNumberAnswerLabel()).getText()).toBe("Fifth answer label number total");
      await expect(await $(NumberTotalPlaybackPage.fifthNumberAnswer()).getText()).toBe("78.91");
      await expect(await $(NumberTotalPlaybackPage.sixthNumberAnswerLabel()).getText()).toBe("Sixth answer label number total");
      await expect(await $(NumberTotalPlaybackPage.sixthNumberAnswer()).getText()).toBe("45.67");
    });

    it("Given I complete every calculated summary, When I go to a page with calculated summary piping, Then I should the see the piped calculated summary total for each summary", async () => {
      await click(NumberTotalPlaybackPage.submit());

      const content = await $("h1 + ul").getText();
      const textsToAssert = [
        "Total currency values: £9.36",
        "Total unformatted unit values: 1,467",
        "Total formatted unit values: 1,467 cm",
        "Total unformatted percentage values: 79",
        "Total formatted percentage values: 79%",
        "Total number values: 124.58",
      ];

      for (const text of textsToAssert) {
        await expect(content).toContain(text);
      }
    });

    it("Given I have an answer minimum based on a calculated summary total, When I enter an invalid answer, Then I should see an error message on the page", async () => {
      await click(CalculatedSummaryTotalConfirmation.submit());
      await expect(browser).toHaveUrlContaining(SetMinMaxBlockPage.pageName);
      await $(SetMinMaxBlockPage.setMinimum()).setValue(8.0);
      await click(SetMinMaxBlockPage.submit());
      await expect(await $(SetMinMaxBlockPage.errorNumber(1)).getText()).toBe("Enter an answer more than or equal to £9.36");
      await $(SetMinMaxBlockPage.setMinimum()).setValue(10.0);
      await click(SetMinMaxBlockPage.submit());
    });

    it("Given I have an answer maximum based on a calculated summary total, When I enter an invalid answer, Then I should see an error message on the page", async () => {
      await click(SubmitPage.submit());
      await expect(browser).toHaveUrlContaining(SetMinMaxBlockPage.pageName);
      await $(SetMinMaxBlockPage.setMaximum()).setValue(10.0);
      await click(SetMinMaxBlockPage.submit());
      await expect(await $(SetMinMaxBlockPage.errorNumber(1)).getText()).toBe("Enter an answer less than or equal to £9.36");
      await $(SetMinMaxBlockPage.setMaximum()).setValue(7.0);
      await click(SetMinMaxBlockPage.submit());
    });

    it("Given I confirm the totals and am on the summary, When I edit and change an answer, Then I must re-confirm the dependant calculated summary page and min max question page before I can return to the summary", async () => {
      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
      await $(SubmitPage.thirdNumberAnswerEdit()).click();
      await $(ThirdNumberBlockPage.thirdNumber()).setValue(3.5);
      await click(ThirdNumberBlockPage.submit());

      // first incomplete block
      await expect(browser).toHaveUrlContaining(CurrencyTotalPlaybackPage.pageName);
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).toBe(
        "We calculate the total of currency values entered to be £9.41. Is this correct?",
      );
      await click(CurrencyTotalPlaybackPage.submit());

      // second incomplete block
      await expect(browser).toHaveUrlContaining(SetMinMaxBlockPage.pageName);
      await $(SetMinMaxBlockPage.setMinimum()).setValue(10.0);
      await $(SetMinMaxBlockPage.setMaximum()).setValue(9.0);
      await click(SetMinMaxBlockPage.submit());

      // back to summary
      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
    });

    it("Given I confirm the totals and am on the summary, When I edit and change an answer that has a dependent minimum value from a calculated summary total, And the minimum value has been changed, Then I must re-validate before I get to the summary", async () => {
      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
      await $(SubmitPage.thirdNumberAnswerEdit()).click();
      await $(ThirdNumberBlockPage.thirdNumber()).setValue(10.0);
      await click(ThirdNumberBlockPage.submit());
      await expect(browser).toHaveUrlContaining(CurrencyTotalPlaybackPage.pageName);
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).toBe(
        "We calculate the total of currency values entered to be £15.91. Is this correct?",
      );
      await click(CurrencyTotalPlaybackPage.submit());
      await expect(browser).toHaveUrlContaining(SetMinMaxBlockPage.pageName);
      await click(SetMinMaxBlockPage.submit());
      await expect(await $(SetMinMaxBlockPage.errorNumber(1)).getText()).toBe("Enter an answer more than or equal to £15.91");
      await $(SetMinMaxBlockPage.setMinimum()).setValue(16.0);
      await click(SetMinMaxBlockPage.submit());
      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
    });

    it("Given I confirm the totals and am on the summary, When I edit and change an answer that has a dependent maximum value from a calculated summary total, And the maximum value has been changed, Then I must re-validate before I get to the summary", async () => {
      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
      await $(SubmitPage.thirdNumberAnswerEdit()).click();
      await $(ThirdNumberBlockPage.thirdNumber()).setValue(1.0);
      await click(ThirdNumberBlockPage.submit());
      await expect(browser).toHaveUrlContaining(CurrencyTotalPlaybackPage.pageName);
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).toBe(
        "We calculate the total of currency values entered to be £6.91. Is this correct?",
      );
      await click(CurrencyTotalPlaybackPage.submit());
      await expect(browser).toHaveUrlContaining(SetMinMaxBlockPage.pageName);
      await click(SetMinMaxBlockPage.submit());
      await expect(await $(SetMinMaxBlockPage.errorNumber(1)).getText()).toBe("Enter an answer less than or equal to £6.91");
      await $(SetMinMaxBlockPage.setMaximum()).setValue(6.0);
      await click(SetMinMaxBlockPage.submit());
      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
    });

    it("Given I am on a page with a placeholder containing a calculated summary value, When I have updated the calculated summary so that additional answers are on the path, Then the placeholder should display the updated value", async () => {
      await $(SubmitPage.skipFourthBlockAnswerEdit()).click();
      await $(SkipFourthBlockPage.no()).click();
      await click(SkipFourthBlockPage.submit());
      await $(SubmitPage.skipFourthBlockAnswerEdit()).click();
      await browser.url(CalculatedSummaryTotalConfirmation.url());
      await expect(browser).toHaveUrlContaining(CalculatedSummaryTotalConfirmation.pageName);
      const content = await $("h1 + ul").getText();
      const textsToAssert = [
        "Total currency values: £25.92",
        "Total unformatted unit values: 1,467",
        "Total formatted unit values: 1,467 cm",
        "Total unformatted percentage values: 79",
        "Total formatted percentage values: 79%",
        "Total number values: 124.58",
      ];

      for (const text of textsToAssert) {
        await expect(content).toContain(text);
      }
      await browser.url(SubmitPage.url());
    });

    it("Given I am on a page with a dependent question based on a calculated summary value, When I have updated the calculated summary so that additional answers are on the path, Then the question should display the updated value", async () => {
      await $(SubmitPage.setMinimumAnswerEdit()).click();
      await expect(browser).toHaveUrlContaining(SetMinMaxBlockPage.pageName);
      await expect(await $(SetMinMaxBlockPage.questionTitle()).getText()).toContain(
        "Set minimum and maximum values based on your calculated summary total of £25.92",
      );
      await click(SetMinMaxBlockPage.submit());
      await expect(await $(SetMinMaxBlockPage.errorNumber(1)).getText()).toBe("Enter an answer more than or equal to £25.92");
      await $(SetMinMaxBlockPage.setMinimum()).setValue(30.0);
      await $(SetMinMaxBlockPage.setMaximum()).setValue(6.0);
      await click(SetMinMaxBlockPage.submit());
    });

    it("Given I am on the summary, When I submit the questionnaire, Then I should see the thank you page", async () => {
      await click(SubmitPage.submit());
      await expect(browser).toHaveUrlContaining(ThankYouPage.pageName);
    });
  }

  testCrossSectionDependencies(schema) {
    before("Get to the question containing calculated summary values with cross section dependencies", async () => {
      await browser.openQuestionnaire(schema);
      await click(HubPage.submit());
      await $(SkipFirstNumberBlockPageSectionOne.no()).click();
      await click(SkipFirstNumberBlockPageSectionOne.submit());
      await $(FirstNumberBlockPageSectionOne.firstNumber()).setValue(10);
      await click(FirstNumberBlockPageSectionOne.submit());
      await $(FirstAndAHalfNumberBlockPageSectionOne.firstAndAHalfNumberAlsoInTotal()).setValue(20);
      await click(FirstAndAHalfNumberBlockPageSectionOne.submit());
      await $(SecondNumberBlockPageSectionOne.secondNumberAlsoInTotal()).setValue(30);
      await click(SecondNumberBlockPageSectionOne.submit());
      await click(CalculatedSummarySectionOne.submit());
      await click(SectionSummarySectionOne.submit());
      await click(HubPage.submit());
      await $(ThirdNumberBlockPageSectionTwo.thirdNumber()).setValue(20);
      await $(ThirdNumberBlockPageSectionTwo.thirdNumberAlsoInTotal()).setValue(20);
      await click(ThirdNumberBlockPageSectionTwo.submit());
      await click(CalculatedSummarySectionTwo.submit());
    });

    it("Given I have a placeholder displaying a calculated summary value source, When the calculated summary value is from a previous section, Then the value displayed should be correct", async () => {
      await expect(browser).toHaveUrlContaining(DependencyQuestionSectionTwo.pageName);
      await expect(await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue1Label()).getText()).toBe("60 - calculated summary answer (previous section)");
      await expect(await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue2Label()).getText()).toBe("40 - calculated summary answer (current section)");
    });

    it("Given I have validation using a calculated summary value source, When the calculated summary value is from a previous section, Then the value used to validate should be correct", async () => {
      await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue1()).click();
      await click(DependencyQuestionSectionTwo.submit());
      await expect(browser).toHaveUrlContaining(MinMaxSectionTwo.pageName);
      await $(MinMaxSectionTwo.setMinimum()).setValue(59.0);
      await $(MinMaxSectionTwo.setMaximum()).setValue(1.0);
      await click(MinMaxSectionTwo.submit());
      await expect(await $(MinMaxSectionTwo.errorNumber(1)).getText()).toBe("Enter an answer more than or equal to £60.00");
      await $(MinMaxSectionTwo.setMinimum()).setValue(61.0);
      await $(MinMaxSectionTwo.setMaximum()).setValue(40.0);
      await click(MinMaxSectionTwo.submit());
    });

    it("Given I remove answers from the path for a calculated summary in a previous section by changing an answer, When I return to the question with the calculated summary value source, Then the value displayed should be correct", async () => {
      await click(SectionSummarySectionTwo.submit());
      await $(HubPage.summaryRowLink("questions-section")).click();
      await $(SectionSummarySectionOne.skipFirstBlockAnswerEdit()).click();
      await $(SkipFirstNumberBlockPageSectionOne.yes()).click();
      await click(SkipFirstNumberBlockPageSectionOne.submit());
      await click(SectionSummarySectionOne.submit());
      await $(HubPage.summaryRowLink("calculated-summary-section")).click();
      await expect(await $("body").getText()).toContain("30 - calculated summary answer (previous section)");
      await $(SectionSummarySectionTwo.checkboxAnswerEdit()).click();
      await expect(await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue1Label()).getText()).toBe("30 - calculated summary answer (previous section)");
      await expect(await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue2Label()).getText()).toBe("40 - calculated summary answer (current section)");
    });
  }

  testNegative(schema, firstAnswerValue, secondAnswerValue, thirdAnswerValue, fourthAnswerValue, expectedTotalValue, expectedAnswerValues) {
    before("Get to Calculated Summary", async () => {
      await browser.openQuestionnaire(schema);

      await $(FirstNumberBlockPage.firstNumber()).setValue(firstAnswerValue);
      await click(FirstNumberBlockPage.submit());

      await $(SecondNumberBlockPage.secondNumber()).setValue(secondAnswerValue);
      await $(SecondNumberBlockPage.secondNumberUnitTotal()).setValue(789);
      await $(SecondNumberBlockPage.secondNumberAlsoInTotal()).setValue(0);
      await click(SecondNumberBlockPage.submit());

      await $(ThirdNumberBlockPage.thirdNumber()).setValue(thirdAnswerValue);
      await click(ThirdNumberBlockPage.submit());
      await $(ThirdAndAHalfNumberBlockPage.thirdAndAHalfNumberUnitTotal()).setValue(678);
      await click(ThirdAndAHalfNumberBlockPage.submit());

      await $(SkipFourthBlockPage.no()).click();
      await click(SkipFourthBlockPage.submit());

      await $(FourthNumberBlockPage.fourthNumber()).setValue(fourthAnswerValue);
      await click(FourthNumberBlockPage.submit());
      await $(FourthAndAHalfNumberBlockPage.fourthAndAHalfNumberAlsoInTotal()).setValue(0);
      await click(FourthAndAHalfNumberBlockPage.submit());

      await $(FifthNumberBlockPage.fifthPercent()).setValue(56);
      await $(FifthNumberBlockPage.fifthNumber()).setValue(78.91);
      await click(FifthNumberBlockPage.submit());

      await $(SixthNumberBlockPage.sixthPercent()).setValue(23);
      await $(SixthNumberBlockPage.sixthNumber()).setValue(45);
      await click(SixthNumberBlockPage.submit());

      await expect(browser).toHaveUrlContaining(CurrencyTotalPlaybackPage.pageName);
    });
    it("Given I have entered a range of positive and negative values, When I reach the calculated summary, Then the total is correct", async () => {
      await assertSummaryValues(expectedAnswerValues);
      await expect(await $(CurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).toBe(
        `We calculate the total of currency values entered to be ${expectedTotalValue}. Is this correct?`,
      );
    });
  }
}

export const CalculatedSummaryTestCase = new TestCase();
