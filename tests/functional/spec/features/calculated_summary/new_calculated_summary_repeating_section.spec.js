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
import { click } from "../../../helpers";
import { expect } from "@wdio/globals";

describe("Feature: Calculated Summary Repeating Section", () => {
  describe("Given I have a Calculated Summary in a Repeating Section", () => {
    before("Get to Calculated Summary", async () => {
      await browser.openQuestionnaire("test_new_calculated_summary_repeating_section.json");
      await click(HubPage.submit());
      await $(PrimaryPersonListCollectorPage.yes()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await click(PrimaryPersonListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await click(HubPage.submit());

      await getToFirstCalculatedSummary();

      await expect(browser).toHaveUrlContaining(CurrencyTotalPlaybackPage.pageName);
    });

    it("Given I have completed all questions, When I am on the calculated summary and there is no custom page title, Then the page title should use the calculation's title", async () => {
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
        "first-number-block/?return_to=calculated-summary&return_to_answer_id=first-number-answer&return_to_block_id=currency-total-playback#first-number-answer",
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

    it("Given the calculated summary has a custom title with the list item position, When I am on the percentage calculated summary, Then the page title should use the custom title with the list item position", async () => {
      await expect(await browser.getTitle()).toBe("Percentage Calculated Summary: Person 1 - A test schema to demo Calculated Summary");
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

    it("Given I have a calculated summary total that is used as a placeholder in another calculated summary, When I get to the calculated summary page displaying the placeholder, Then I should see the correct total", async () => {
      await click(NumberTotalPlaybackPage.submit());
      await expect(browser).toHaveUrlContaining(BreakdownPage.pageName);
      await $(BreakdownPage.answer1()).setValue(100.0);
      await $(BreakdownPage.answer2()).setValue(24.58);
      await click(BreakdownPage.submit());
      await expect(browser).toHaveUrlContaining(SecondCurrencyTotalPlaybackPage.pageName);
      await expect(await $(SecondCurrencyTotalPlaybackPage.calculatedSummaryTitle()).getText()).toBe(
        "We calculate the total of number values entered to be £124.58. Is this correct?",
      );
      await expect(await $("body").getText()).toContain("Enter two values that add up to the previous calculated summary total of £124.58");
      await expect(await $(SecondCurrencyTotalPlaybackPage.calculatedSummaryAnswer()).getText()).toBe("£124.58");
    });

    it("Given I complete every calculated summary, When I go to a page with calculated summary piping, Then I should the see the piped calculated summary total for each summary", async () => {
      await click(SecondCurrencyTotalPlaybackPage.submit());

      const content = $("h1 + ul").getText();
      const textsToAssert = ["Total currency values: £9.36", "Total unit values: 1,467", "Total percentage values: 79", "Total number values: 124.58"];

      textsToAssert.forEach(async (text) => await expect(content).toBe(text));
    });

    it("Given I have an answer minimum based on a calculated summary total, When I enter an invalid answer, Then I should see an error message on the page", async () => {
      await click(CalculatedSummaryTotalConfirmation.submit());
      await expect(browser).toHaveUrlContaining(SetMinMaxBlockPage.pageName);
      await $(SetMinMaxBlockPage.setMinimum()).setValue(8.0);
      await click(SetMinMaxBlockPage.submit());
      await expect(await $(SetMinMaxBlockPage.errorNumber(1)).getText()).toBe("Enter an answer more than or equal to £9.36");
      await $(SetMinMaxBlockPage.setMinimum()).setValue(10.0);
    });

    it("Given I have an answer maximum based on a calculated summary total, When I enter an invalid answer, Then I should see an error message on the page", async () => {
      await $(SetMinMaxBlockPage.setMaximum()).setValue(10.0);
      await click(SetMinMaxBlockPage.submit());
      await expect(await $(SetMinMaxBlockPage.errorNumber(1)).getText()).toBe("Enter an answer less than or equal to £9.36");
      await $(SetMinMaxBlockPage.setMaximum()).setValue(7.0);
      await click(SetMinMaxBlockPage.submit());
    });

    it("Given I confirm the totals and am on the summary, When I edit and change an answer, Then I go to each incomplete page in turn before I return to the summary", async () => {
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

    it("Given I am on the summary, When I submit the questionnaire, Then I should see the thank you page", async () => {
      await click(SubmitPage.submit());
      await click(HubPage.submit());
      await expect(browser).toHaveUrlContaining(ThankYouPage.pageName);
    });
  });

  describe("Given I have a Calculated Summary in a Repeating Section", async () => {
    before("Get to Final Summary", async () => {
      await browser.openQuestionnaire("test_new_calculated_summary_repeating_section.json");
      await click(HubPage.submit());
      await $(PrimaryPersonListCollectorPage.no()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Jean");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Jane");
      await $(ListCollectorAddPage.lastName()).setValue("Doe");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await click(HubPage.submit());
      await getToFirstCalculatedSummary();
      await getToSubmitPage();
      await click(SubmitPage.submit());
      await click(HubPage.submit());
      await getToFirstCalculatedSummary();
      await getToSubmitPage();
      await click(SubmitPage.submit());
    });

    it("Given I am on the submit page, When I have completed two repeating sections containing a calculated summary, Then the section status for both repeating sections should be complete", async () => {
      await expect(browser).toHaveUrlContaining(HubPage.pageName);
      await expect(await $(HubPage.summaryRowState("personal-details-section-1")).getText()).toBe("Completed");
      await expect(await $(HubPage.summaryRowState("personal-details-section-2")).getText()).toBe("Completed");
    });

    it("Given I change an answer with a dependent calculated summary question, When I return to the hub, Then only the section status for the repeating section I updated should be incomplete", async () => {
      await expect(browser).toHaveUrlContaining(HubPage.pageName);
      await $(HubPage.summaryRowLink("personal-details-section-1")).click();
      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
      await $(SubmitPage.skipFourthBlockAnswerEdit()).click();
      await $(SkipFourthBlockPage.yes()).click();
      await click(SkipFourthBlockPage.submit());
      await browser.url(HubPage.url());
      await expect(await $(HubPage.summaryRowState("personal-details-section-1")).getText()).toBe("Partially completed");
      await expect(await $(HubPage.summaryRowState("personal-details-section-2")).getText()).toBe("Completed");
    });

    it("Given I return to a partially completed section with a calculated summary, When I answer the dependent questions and return to the hub, Then the section status for the repeating section I updated should be complete", async () => {
      await expect(browser).toHaveUrlContaining(HubPage.pageName);
      await expect(await $(HubPage.summaryRowState("personal-details-section-1")).getText()).toBe("Partially completed");
      await $(HubPage.summaryRowLink("personal-details-section-1")).click();
      await expect(browser).toHaveUrlContaining(SetMinMaxBlockPage.pageName);
      await $(SetMinMaxBlockPage.setMinimum()).setValue(10.0);
      await $(SetMinMaxBlockPage.setMaximum()).setValue(6.0);
      await click(SetMinMaxBlockPage.submit());
      await click(SubmitPage.submit());
      await expect(browser).toHaveUrlContaining(HubPage.pageName);
      await expect(await $(HubPage.summaryRowState("personal-details-section-1")).getText()).toBe("Completed");
      await expect(await $(HubPage.summaryRowState("personal-details-section-2")).getText()).toBe("Completed");
    });
  });

  describe("Given I have a Calculated Summary in a Repeating Section with a Dependency based on a calculated summary in another section", () => {
    before("Get to the Dependent question page", async () => {
      await browser.openQuestionnaire("test_new_calculated_summary_cross_section_dependencies_repeating.json");
      await click(HubPage.submit());
      await $(PrimaryPersonListCollectorPage.yes()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await click(PrimaryPersonListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
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
      await $(HubPage.summaryRowLink("calculated-summary-section-1")).click();
      await expect(await $("body").getText()).toContain("30 - calculated summary answer (previous section)");
      await $(SectionSummarySectionTwo.checkboxAnswerEdit()).click();
      await expect(await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue1Label()).getText()).toBe("30 - calculated summary answer (previous section)");
      await expect(await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue2Label()).getText()).toBe("40 - calculated summary answer (current section)");
    });
  });
});

const getToFirstCalculatedSummary = async () => {
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
};

const getToSubmitPage = async () => {
  await click(CurrencyTotalPlaybackPage.submit());
  await click(UnitTotalPlaybackPage.submit());
  await click(PercentageTotalPlaybackPage.submit());
  await click(NumberTotalPlaybackPage.submit());
  await $(BreakdownPage.answer1()).setValue(100.0);
  await $(BreakdownPage.answer2()).setValue(24.58);
  await click(BreakdownPage.submit());
  await click(SecondCurrencyTotalPlaybackPage.submit());
  await click(CalculatedSummaryTotalConfirmation.submit());
};
