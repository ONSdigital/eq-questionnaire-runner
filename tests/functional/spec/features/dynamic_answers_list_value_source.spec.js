import DriverPage from "../../generated_pages/dynamic_answers_list_source/any-supermarket.page";
import DynamicAnswerPage from "../../generated_pages/dynamic_answers_list_source/dynamic-answer.page";
import DynamicAnswerOnlyPage from "../../generated_pages/dynamic_answers_list_source/dynamic-answer-only.page";
import ListCollectorPage from "../../generated_pages/dynamic_answers_list_source/list-collector.page";
import ListCollectorAddPage from "../../generated_pages/dynamic_answers_list_source/list-collector-add.page";
import ListCollectorRemovePage from "../../generated_pages/dynamic_answers_list_source/list-collector-remove.page";
import SetMinimumPage from "../../generated_pages/dynamic_answers_list_source/minimum-spending.page";
import SectionSummaryPage from "../../generated_pages/dynamic_answers_list_source/list-collector-section-summary.page";
import HubPage from "../../base_pages/hub.page";
import OnlineShoppingPage from "../../generated_pages/dynamic_answers_list_source/dynamic-answer-separate-section.page";
import { click } from "../../helpers";
import { expect } from "@wdio/globals";
import SetMinMaxBlockPage from "../../generated_pages/calculated_summary/set-min-max-block.page";

describe("Dynamic answers list value source", () => {
  const summaryTitles = ".ons-summary__item-title";
  const summaryValues = ".ons-summary__values";
  const summaryActions = ".ons-summary__actions";
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_dynamic_answers_list_source.json");
  });

  it("Given list items have been added, When the dynamic answers are displayed, Then the correct answers should be visible", async () => {
    await addTwoSupermarkets();
    await expect(await $$(DynamicAnswerPage.labels())[0].getText()).toBe("Percentage of shopping at Tesco");
    await expect(await $$(DynamicAnswerPage.labels())[1].getText()).toBe("Percentage of shopping at Aldi");
    await expect(await $$(DynamicAnswerPage.labels()).length).toBe(4);
  });
  it("Given list items have been added, When additional items are added using add link, Then the correct dynamic answers are displayed", async () => {
    await $(DriverPage.yes()).click();
    await click(DriverPage.submit());
    await $(ListCollectorAddPage.supermarketName()).setValue("Tesco");
    await $(ListCollectorAddPage.setMaximum()).setValue(10000);
    await click(ListCollectorAddPage.submit());
    await $(ListCollectorPage.no()).click();
    await click(ListCollectorPage.submit());
    await expect(await $$(DynamicAnswerPage.labels())[0].getText()).toBe("Percentage of shopping at Tesco");
    await expect(await $$(DynamicAnswerPage.labels()).length).toBe(2);
    await setMinimumAndGetSectionSummary();
    await $(SectionSummaryPage.supermarketsListAddLink()).click();
    await $(ListCollectorAddPage.supermarketName()).setValue("Aldi");
    await $(ListCollectorAddPage.setMaximum()).setValue(10000);
    await click(ListCollectorAddPage.submit());
    await $(ListCollectorPage.no()).click();
    await click(ListCollectorPage.submit());
    await expect(await $$(DynamicAnswerPage.labels())[0].getText()).toBe("Percentage of shopping at Tesco");
    await expect(await $$(DynamicAnswerPage.labels())[1].getText()).toBe("Percentage of shopping at Aldi");
    await expect(await $$(DynamicAnswerPage.labels()).length).toBe(4);
  });
  it("Given list items have been added and the dynamic answers are submitted, When the summary is displayed, Then the correct answers should be visible and have correct values", async () => {
    await addTwoSupermarkets();
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await $$(DynamicAnswerPage.inputs())[2].setValue(3);
    await $$(DynamicAnswerPage.inputs())[3].setValue(7);
    await setMinimumAndGetSectionSummary();
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryTitles)[0].getText()).toBe("Percentage of shopping at Tesco");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues)[0].getText()).toBe("12%");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryTitles)[1].getText()).toBe("Percentage of shopping at Aldi");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues)[1].getText()).toBe("21%");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues)[2].getText()).toBe("3");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues)[3].getText()).toBe("7");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryTitles).length).toBe(8);
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues).length).toBe(8);
  });
  it("Given list items have been added and the dynamic answers are submitted, When the dynamic answers are revisited, Then they should be visible and have correct values", async () => {
    await addTwoSupermarkets();
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await setMinimumAndGetSectionSummary();
    await $(SectionSummaryPage.previous()).click();
    await $(DynamicAnswerOnlyPage.previous()).click();
    await $(SetMinimumPage.previous()).click();
    await expect(browser).toHaveUrlContaining(DynamicAnswerPage.pageName);
    await expect(await $$(DynamicAnswerPage.inputs())[0].getValue()).toBe("12");
    await expect(await $$(DynamicAnswerPage.inputs())[1].getValue()).toBe("21");
    await expect(await $$(DynamicAnswerPage.labels())[0].getText()).toBe("Percentage of shopping at Tesco");
    await expect(await $$(DynamicAnswerPage.labels())[1].getText()).toBe("Percentage of shopping at Aldi");
  });
  it("Given list items have been added and the dynamic answers are submitted, When the dynamic answers are resubmitted with different values, Then they should be displayed correctly on summary", async () => {
    await addTwoSupermarkets();
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await setMinimumAndGetSectionSummary();
    await $(SectionSummaryPage.previous()).click();
    await $(DynamicAnswerOnlyPage.previous()).click();
    await $(SetMinimumPage.previous()).click();
    await $$(DynamicAnswerPage.inputs())[0].setValue(21);
    await $$(DynamicAnswerPage.inputs())[1].setValue(12);
    await click(DynamicAnswerPage.submit());
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues)[0].getText()).toBe("21%");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues)[1].getText()).toBe("12%");
  });
  it("Given list items have been added and the dynamic answers are submitted, When the summary edit answer link is used for dynamic answer, Then the focus is on correct answer option", async () => {
    await addTwoSupermarkets();
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await setMinimumAndGetSectionSummary();
    await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryActions)[0].$("a").click();
    await expect(browser).toHaveUrlContaining(DynamicAnswerPage.pageName);
    await expect(await $$(DynamicAnswerPage.inputs())[0].isFocused()).toBe(true);
    await click(DynamicAnswerPage.submit());
    await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryActions)[1].$("a").click();
    await expect(browser).toHaveUrlContaining(DynamicAnswerPage.pageName);
    await expect(await $$(DynamicAnswerPage.inputs())[1].isFocused()).toBe(true);
  });
  it("Given list items have been added and the dynamic answers are submitted, When the dynamic answers are resubmitted with answers updated, Then they should be displayed correctly on summary", async () => {
    await addTwoSupermarkets();
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await setMinimumAndGetSectionSummary();
    await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryActions)[0].$("a").click();
    await $$(DynamicAnswerPage.inputs())[0].setValue(21);
    await click(DynamicAnswerPage.submit());
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues)[0].getText()).toBe("21%");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues)[1].getText()).toBe("21%");
  });
  it("Given list items have been added and the dynamic answers are submitted, When the list items are removed and answers updated, Then they should be displayed correctly on summary", async () => {
    await addTwoSupermarkets();
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await setMinimumAndGetSectionSummary();
    await $(SectionSummaryPage.supermarketsListRemoveLink(1)).click();
    await $(ListCollectorRemovePage.yes()).click();
    await click(ListCollectorRemovePage.submit());
    await click(DynamicAnswerPage.submit());
    await click(DynamicAnswerOnlyPage.submit());
    await expect(browser).toHaveUrlContaining(SectionSummaryPage.pageName);
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryTitles)[0].getText()).toBe("Percentage of shopping at Aldi");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues)[0].getText()).toBe("21%");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryTitles).length).toBe(5);
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues).length).toBe(5);
  });
  it("Given list items have been added and the dynamic answers are submitted, When the driving question is changed to 'No' and subsequently changed back to 'Yes', Then all answers should re-appear on summary", async () => {
    await addTwoSupermarkets();
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await $$(DynamicAnswerPage.inputs())[2].setValue(3);
    await $$(DynamicAnswerPage.inputs())[3].setValue(7);
    await setMinimumAndGetSectionSummary();
    await $(SectionSummaryPage.anySupermarketAnswerEdit()).click();
    await $(DriverPage.no()).click();
    await click(DriverPage.submit());
    await expect(await $("body").getText()).not.toBe("Percentage of shopping at Tesco");
    await expect(await $("body").getText()).not.toBe("Percentage of shopping at Aldi");
    await $(SectionSummaryPage.anySupermarketAnswerEdit()).click();
    await $(DriverPage.yes()).click();
    await click(DriverPage.submit());

    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryTitles)[0].getText()).toBe("Percentage of shopping at Tesco");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues)[0].getText()).toBe("12%");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryTitles)[1].getText()).toBe("Percentage of shopping at Aldi");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues)[1].getText()).toBe("21%");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues)[2].getText()).toBe("3");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues)[3].getText()).toBe("7");
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryTitles).length).toBe(8);
    await expect(await $(SectionSummaryPage.listCollectorGroupContent(2)).$$(summaryValues).length).toBe(8);
  });

  it("Given list items have been added, When the dynamic answers are displayed in a separate section, Then the correct answers should be visible", async () => {
    await addTwoSupermarketsAndGetToNextSection();
    await expect(await $$(OnlineShoppingPage.labels())[0].getText()).toBe("Percentage of online shopping at Tesco");
    await expect(await $$(OnlineShoppingPage.labels())[1].getText()).toBe("Percentage of online shopping at Aldi");
    await expect(await $$(OnlineShoppingPage.labels()).length).toBe(4);
  });

  it("Given the minimum value is set to 1000.99, When the maximum amount of spending entered should be between 1000.99 and 10000 and 1000.98 is entered, Then the value should not be accepted", async () => {
    // Go through until maximum spending is achieved, then enter the spending to 1000.98 and then an error should appear.
    await $(DriverPage.yes()).click();
    await click(DriverPage.submit());
    await $(ListCollectorAddPage.supermarketName()).setValue("Tesco");
    await $(ListCollectorAddPage.setMaximum()).setValue(1000.98);
    await click(ListCollectorAddPage.submit());
    await expect(await $(ListCollectorAddPage.errorNumber(1)).getText()).toBe("Enter an answer more than or equal to 1,000.99");
  });
});

async function addTwoSupermarkets() {
  await $(DriverPage.yes()).click();
  await click(DriverPage.submit());
  await $(ListCollectorAddPage.supermarketName()).setValue("Tesco");
  await $(ListCollectorAddPage.setMaximum()).setValue(10000);
  await click(ListCollectorAddPage.submit());
  await $(ListCollectorPage.yes()).click();
  await click(ListCollectorPage.submit());
  await $(ListCollectorAddPage.supermarketName()).setValue("Aldi");
  await $(ListCollectorAddPage.setMaximum()).setValue(10000);
  await click(ListCollectorAddPage.submit());
  await $(ListCollectorPage.no()).click();
  await click(ListCollectorPage.submit());
}

async function addTwoSupermarketsAndGetToNextSection() {
  await $(DriverPage.yes()).click();
  await click(DriverPage.submit());
  await $(ListCollectorAddPage.supermarketName()).setValue("Tesco");
  await $(ListCollectorAddPage.setMaximum()).setValue(10000);
  await click(ListCollectorAddPage.submit());
  await $(ListCollectorPage.yes()).click();
  await click(ListCollectorPage.submit());
  await $(ListCollectorAddPage.supermarketName()).setValue("Aldi");
  await $(ListCollectorAddPage.setMaximum()).setValue(10000);
  await click(ListCollectorAddPage.submit());
  await $(ListCollectorPage.no()).click();
  await click(ListCollectorPage.submit());
  await $$(DynamicAnswerPage.inputs())[0].setValue(12);
  await $$(DynamicAnswerPage.inputs())[1].setValue(21);
  await $$(DynamicAnswerPage.inputs())[2].setValue(3);
  await $$(DynamicAnswerPage.inputs())[3].setValue(7);
  await setMinimumAndGetSectionSummary();
  await click(SectionSummaryPage.submit());
  await click(HubPage.submit());
}

async function setMinimumAndGetSectionSummary() {
  await click(DynamicAnswerPage.submit());
  await $(SetMinimumPage.setMinimum()).setValue(2);
  await click(SetMinimumPage.submit());
  await click(DynamicAnswerOnlyPage.submit());
}
