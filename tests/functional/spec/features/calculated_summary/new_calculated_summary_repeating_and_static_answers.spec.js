import HubPage from "../../../base_pages/hub.page";
import AnySupermarketPage from "../../../generated_pages/new_calculated_summary_repeating_and_static_answers/any-supermarket.page.js";
import ListCollectorPage from "../../../generated_pages/new_calculated_summary_repeating_and_static_answers/list-collector.page.js";
import ExtraSpendingBlockPage from "../../../generated_pages/new_calculated_summary_repeating_and_static_answers/extra-spending-block.page.js";
import CalculatedSummarySpendingPage from "../../../generated_pages/new_calculated_summary_repeating_and_static_answers/calculated-summary-spending.page.js";
import CalculatedSummaryVisitsPage from "../../../generated_pages/new_calculated_summary_repeating_and_static_answers/calculated-summary-visits.page.js";
import ListCollectorAddPage from "../../../generated_pages/new_calculated_summary_repeating_and_static_answers/list-collector-add.page";
import DynamicAnswerPage from "../../../generated_pages/new_calculated_summary_repeating_and_static_answers/dynamic-answer.page";
import Section1SummaryPage from "../../../generated_pages/new_calculated_summary_repeating_and_static_answers/section-1-summary.page";
import ExtraSpendingMethodBlockPage from "../../../generated_pages/new_calculated_summary_repeating_and_static_answers/extra-spending-method-block.page";
import ListCollectorRemovePage from "../../../generated_pages/new_calculated_summary_repeating_and_static_answers/list-collector-remove.page";

describe("Calculated summary with repeating answers", () => {
  const currencyInputs = 'input[class="ons-input ons-input--text ons-input-type__input ons-input-number--w-20"]';
  const daysInputs = 'input[class="ons-input ons-input--text ons-input-type__input ons-input-number--w-1"]';
  const group = 'div[id="group"]';
  const summaryValues = 'dd[class="ons-summary__values"]';
  const summaryActions = 'dd[class="ons-summary__actions"]';

  const assertSummaryValues = async (values) => {
    // check each summary value provided is present and that the number of them matches what is on the page
    // needs to include both dynamic and static answers on any summary with both
    await values.map(async (value, index) => {
      await expect(await $(group).$$(summaryValues)[index].getText()).to.equal(value);
    });
    await expect(await $(group).$$(summaryValues).length).to.equal(values.length);
  };

  const dynamicAnswerChangeLink = (answerIndex) => $(group).$$(summaryActions)[answerIndex].$("a");

  before("Completing the list collector and dynamic answer", async () => {
    await browser.openQuestionnaire("test_new_calculated_summary_repeating_and_static_answers.json");
    await $(HubPage.submit()).click();
    await $(AnySupermarketPage.yes()).click();
    await $(AnySupermarketPage.submit()).click();
    await $(ListCollectorAddPage.supermarketName()).setValue("Tesco");
    await $(ListCollectorAddPage.submit()).click();
    await $(ListCollectorPage.yes()).click();
    await $(ListCollectorPage.submit()).click();
    await $(ListCollectorAddPage.supermarketName()).setValue("Lidl");
    await $(ListCollectorAddPage.submit()).click();
    await $(ListCollectorPage.no()).click();
    await $(ListCollectorPage.submit()).click();
    await $$(currencyInputs)[0].setValue(300);
    await $$(currencyInputs)[1].setValue(200);
    await $$(currencyInputs)[2].setValue(30);
    await $$(currencyInputs)[3].setValue(20);
    await $$(daysInputs)[0].setValue(4);
    await $$(daysInputs)[1].setValue(2);
    await $(DynamicAnswerPage.submit()).click();
    await $(ExtraSpendingBlockPage.extraSpending()).setValue(0);
  });

  it("Given I complete all list collector dynamic answers for two calculated summaries one of which also has static answers, I'm taken to each one in turn, showing the correct answers", async () => {
    await $(ExtraSpendingBlockPage.submit()).click();
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total cost of your weekly shopping to be £550.00. Is this correct?"
    );
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryAnswer()).getText()).to.contain("£550.00");
    await assertSummaryValues(["£300.00", "£200.00", "£30.00", "£20.00", "£0.00"]);
    await $(CalculatedSummarySpendingPage.submit()).click();
    await expect(await $(CalculatedSummaryVisitsPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total visits to the shop to be 6. Is this correct?"
    );
    await assertSummaryValues(["4", "2"]);
    await expect(await $(group).$$(summaryValues).length).to.equal(2);
  });

  it("Given I click on a change link, when I use the previous button, I return to the calculated summary", async () => {
    await dynamicAnswerChangeLink(1).click();
    await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
    await $(DynamicAnswerPage.previous()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummaryVisitsPage.pageName);
  });

  it("Given I click on a change link, edit an answer and continue, I return to the calculated summary to reconfirm it", async () => {
    await dynamicAnswerChangeLink(0).click();
    await $$(daysInputs)[1].setValue(3);
    await $(DynamicAnswerPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(CalculatedSummaryVisitsPage.pageName);
    await expect(await $(CalculatedSummaryVisitsPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total visits to the shop to be 7. Is this correct?"
    );
    await assertSummaryValues(["4", "3"]);
    await $(CalculatedSummaryVisitsPage.submit()).click();
  });

  it("Given I go back and change an answer that opens up a new question before the calculated summary, I am taken to the new question, and then the calculated summary", async () => {
    await $(Section1SummaryPage.extraSpendingAnswerEdit()).click();
    await $(ExtraSpendingBlockPage.extraSpending()).setValue(50);
    await $(ExtraSpendingBlockPage.submit()).click();

    // new question
    await expect(await browser.getUrl()).to.contain(ExtraSpendingMethodBlockPage.pageName);
    await $(ExtraSpendingMethodBlockPage.yes()).click();
    await $(ExtraSpendingMethodBlockPage.submit()).click();

    // then calculated summary
    await expect(await browser.getUrl()).to.contain(CalculatedSummarySpendingPage.pageName);
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total cost of your weekly shopping to be £600.00. Is this correct?"
    );

    // then jump straight back to section summary (as other calculated summary is unchanged
    await $(CalculatedSummarySpendingPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(Section1SummaryPage.pageName);
  });

  it("Given I add a new item to the list, I return to the list collector block, then the dynamic answers, then both calculated summaries to confirm newly added answers", async () => {
    await $(Section1SummaryPage.supermarketsListAddLink()).click();
    await $(ListCollectorAddPage.supermarketName()).setValue("Sainsburys");
    await $(ListCollectorAddPage.submit()).click();
    await $(ListCollectorPage.no()).click();
    await $(ListCollectorPage.submit()).click();

    // return to dynamic answer
    await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
    await $$(currencyInputs)[2].setValue(100);
    await $$(currencyInputs)[5].setValue(10);
    await $$(daysInputs)[2].setValue(7);
    await $(DynamicAnswerPage.submit()).click();

    // Currently when a section is incomplete, you are taken to each block in the section in turn, if the return_to is inaccessible
    // this has been changed for calculated summaries to go to the first incomplete block, but not yet in the general case
    // so the expected behaviour is to revisit these two blocks before the calculated summary
    await $(ExtraSpendingBlockPage.submit()).click();
    await $(ExtraSpendingMethodBlockPage.submit()).click();

    // first calc summary
    await expect(await browser.getUrl()).to.contain(CalculatedSummarySpendingPage.pageName);
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total cost of your weekly shopping to be £710.00. Is this correct?"
    );
    await assertSummaryValues(["£300.00", "£200.00", "£100.00", "£30.00", "£20.00", "£10.00", "£0.00"]);

    // second calculated summary
    await $(CalculatedSummarySpendingPage.submit()).click();
    await expect(await $(CalculatedSummaryVisitsPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total visits to the shop to be 14. Is this correct?"
    );
    await assertSummaryValues(["4", "3", "2"]);
    await $(CalculatedSummaryVisitsPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(Section1SummaryPage.pageName);
  });

  it("Given I remove an item from the list which changes the calculated summaries, I return to each calculated summary to confirm new total with answers removed", async () => {
    await expect(await $(Section1SummaryPage.supermarketsListLabel(1)).getText()).to.equal("Tesco");
    await expect(await $(Section1SummaryPage.supermarketsListLabel(2)).getText()).to.equal("Lidl");
    await expect(await $(Section1SummaryPage.supermarketsListLabel(3)).getText()).to.equal("Sainsburys");
    await expect(await $(Section1SummaryPage.supermarketsListLabel(4)).isExisting()).to.be.false;
    await $(Section1SummaryPage.supermarketsListRemoveLink(1)).click();

    await expect(await browser.getUrl()).to.contain(ListCollectorRemovePage.pageName);
    await $(ListCollectorRemovePage.yes()).click();
    await $(ListCollectorRemovePage.submit()).click();

    // section is now incomplete so step through each block until calculated summary is re-confirmed
    await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
    await $(DynamicAnswerPage.submit()).click();
    await $(ExtraSpendingBlockPage.submit()).click();
    await $(ExtraSpendingMethodBlockPage.submit()).click();

    // Tesco is now gone
    await expect(await $(CalculatedSummarySpendingPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total cost of your weekly shopping to be £380.00. Is this correct?"
    );
    await assertSummaryValues(["£200.00", "£100.00", "£20.00", "£10.00", "£50.00"]);
    await $(CalculatedSummarySpendingPage.submit()).click();
    await expect(await $(CalculatedSummaryVisitsPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total visits to the shop to be 10. Is this correct?"
    );
    await assertSummaryValues(["3", "7"]);
    await $(CalculatedSummaryVisitsPage.submit()).click();

    await expect(await $(Section1SummaryPage.supermarketsListLabel(1)).getText()).to.equal("Lidl");
    await expect(await $(Section1SummaryPage.supermarketsListLabel(2)).getText()).to.equal("Sainsburys");
    await expect(await $(Section1SummaryPage.supermarketsListLabel(3)).isExisting()).to.be.false;
  });
});
