import DriverPage from "../../generated_pages/dynamic_answers_list_source/any-supermarket.page";
import DynamicAnswerPage from "../../generated_pages/dynamic_answers_list_source/dynamic-answer.page";
import DynamicAnswerOnlyPage from "../../generated_pages/dynamic_answers_list_source/dynamic-answer-only.page";
import ListCollectorPage from "../../generated_pages/dynamic_answers_list_source/list-collector.page";
import ListCollectorAddPage from "../../generated_pages/dynamic_answers_list_source/list-collector-add.page";
import ListCollectorRemovePage from "../../generated_pages/dynamic_answers_list_source/list-collector-remove.page";
import SetMinimumPage from "../../generated_pages/dynamic_answers_list_source/minimum-spending.page";
import SectionSummaryPage from "../../generated_pages/dynamic_answers_list_source/section-summary.page";

describe("Dynamic answers list value source", () => {
  const summaryTitles = ".ons-summary__item-title";
  const summaryValues = ".ons-summary__values";
  const summaryActions = ".ons-summary__actions";
  const timeout = 2000;
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_dynamic_answers_list_source.json");
  });

  it("Given list items have been added, When the dynamic answers are displayed, Then the correct answers should be visible", async () => {
    await addTwoSupermarkets(timeout);
    await expect(await $$(DynamicAnswerPage.labels())[0].getText()).to.equal("Percentage of shopping at Tesco");
    await expect(await $$(DynamicAnswerPage.labels())[1].getText()).to.equal("Percentage of shopping at Aldi");
    await expect(await $$(DynamicAnswerPage.labels()).length).to.equal(4);
  });
  it("Given list items have been added, When additional items are added using add link, Then the correct dynamic answers are displayed", async () => {
    await $(DriverPage.yes()).click();
    await $(DriverPage.submit()).click();
    await $(ListCollectorAddPage.supermarketName()).setValue("Tesco");
    await $(ListCollectorAddPage.setMaximum()).setValue(10000);
    await $(ListCollectorAddPage.submit()).click();
    await $(ListCollectorPage.no()).click();
    await $(ListCollectorPage.submit()).click();
    await $(DynamicAnswerPage.labels()).waitForExist({ timeout: timeout });
    await expect(await $$(DynamicAnswerPage.labels())[0].getText()).to.equal("Percentage of shopping at Tesco");
    await expect(await $$(DynamicAnswerPage.labels()).length).to.equal(2);
    await setMinimumAndGetSectionSummary(timeout);
    await $(SectionSummaryPage.supermarketsListAddLink()).click();
    await $(ListCollectorAddPage.supermarketName()).setValue("Aldi");
    await $(ListCollectorAddPage.setMaximum()).setValue(10000);
    await $(ListCollectorAddPage.submit()).click();
    await $(ListCollectorPage.no()).click();
    await $(ListCollectorPage.submit()).click();
    await $(DynamicAnswerPage.inputs()).waitForExist({ timeout: timeout });
    await expect(await $$(DynamicAnswerPage.labels())[0].getText()).to.equal("Percentage of shopping at Tesco");
    await expect(await $$(DynamicAnswerPage.labels())[1].getText()).to.equal("Percentage of shopping at Aldi");
    await expect(await $$(DynamicAnswerPage.labels()).length).to.equal(4);
  });
  it("Given list items have been added and the dynamic answers are submitted, When the summary is displayed, Then the correct answers should be visible and have correct values", async () => {
    await addTwoSupermarkets(timeout);
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await $$(DynamicAnswerPage.inputs())[2].setValue(3);
    await $$(DynamicAnswerPage.inputs())[3].setValue(7);
    await setMinimumAndGetSectionSummary(timeout);
    await $(SectionSummaryPage.groupContent(2)).waitForExist({ timeout: timeout });
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryTitles)[0].getText()).to.equal("Percentage of shopping at Tesco");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues)[0].getText()).to.equal("12%");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryTitles)[1].getText()).to.equal("Percentage of shopping at Aldi");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues)[1].getText()).to.equal("21%");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues)[2].getText()).to.equal("3");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues)[3].getText()).to.equal("7");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryTitles).length).to.equal(8);
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues).length).to.equal(8);
  });
  it("Given list items have been added and the dynamic answers are submitted, When the dynamic answers are revisited, Then they should be visible and have correct values", async () => {
    await addTwoSupermarkets(timeout);
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await setMinimumAndGetSectionSummary(timeout);
    await $(SectionSummaryPage.previous()).click();
    await $(DynamicAnswerOnlyPage.previous()).click();
    await $(SetMinimumPage.previous()).click();
    await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
    await $(DynamicAnswerPage.inputs()).waitForExist({ timeout: timeout });
    await $(DynamicAnswerPage.labels()).waitForExist({ timeout: timeout });
    await expect(await $$(DynamicAnswerPage.inputs())[0].getValue()).to.equal("12");
    await expect(await $$(DynamicAnswerPage.inputs())[1].getValue()).to.equal("21");
    await expect(await $$(DynamicAnswerPage.labels())[0].getText()).to.equal("Percentage of shopping at Tesco");
    await expect(await $$(DynamicAnswerPage.labels())[1].getText()).to.equal("Percentage of shopping at Aldi");
  });
  it("Given list items have been added and the dynamic answers are submitted, When the dynamic answers are resubmitted with different values, Then they should be displayed correctly on summary", async () => {
    await addTwoSupermarkets(timeout);
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await setMinimumAndGetSectionSummary(timeout);
    await $(SectionSummaryPage.previous()).click();
    await $(DynamicAnswerOnlyPage.previous()).click();
    await $(SetMinimumPage.previous()).click();
    await $$(DynamicAnswerPage.inputs())[0].waitForExist({ timeout: timeout });
    await $$(DynamicAnswerPage.inputs())[0].setValue(21);
    await $$(DynamicAnswerPage.inputs())[1].setValue(12);
    await $(DynamicAnswerPage.submit()).click();
    await $(SectionSummaryPage.groupContent(2)).waitForExist({ timeout: timeout });
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues)[0].getText()).to.equal("21%");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues)[1].getText()).to.equal("12%");
  });
  it("Given list items have been added and the dynamic answers are submitted, When the summary edit answer link is used for dynamic answer, Then the focus is on correct answer option", async () => {
    await addTwoSupermarkets(timeout);
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await setMinimumAndGetSectionSummary(timeout);
    await $(SectionSummaryPage.groupContent(2)).$$(summaryActions)[0].$("a").click();
    await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
    await expect(await $$(DynamicAnswerPage.inputs())[0].isFocused()).to.be.true;
    await $(DynamicAnswerPage.submit()).click();
    await $(SectionSummaryPage.groupContent(2)).waitForExist({ timeout: timeout });
    await $(SectionSummaryPage.groupContent(2)).$$(summaryActions)[1].$("a").click();
    await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
    await expect(await $$(DynamicAnswerPage.inputs())[1].isFocused()).to.be.true;
  });
  it("Given list items have been added and the dynamic answers are submitted, When the dynamic answers are resubmitted with answers updated, Then they should be displayed correctly on summary", async () => {
    await addTwoSupermarkets(timeout);
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await setMinimumAndGetSectionSummary(timeout);
    await $(SectionSummaryPage.groupContent(2)).$$(summaryActions)[0].$("a").click();
    await $$(DynamicAnswerPage.inputs())[0].setValue(21);
    await $(DynamicAnswerPage.submit()).click();
    await $(SectionSummaryPage.groupContent(2)).waitForExist({ timeout: timeout });
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues)[0].getText()).to.equal("21%");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues)[1].getText()).to.equal("21%");
  });
  it("Given list items have been added and the dynamic answers are submitted, When the list items are removed and answers updated, Then they should be displayed correctly on summary", async () => {
    await addTwoSupermarkets(timeout);
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await setMinimumAndGetSectionSummary(timeout);
    await $(SectionSummaryPage.supermarketsListRemoveLink(1)).waitForExist({ timeout: timeout });
    await $(SectionSummaryPage.supermarketsListRemoveLink(1)).click();
    await $(ListCollectorRemovePage.yes()).click();
    await $(ListCollectorRemovePage.submit()).click();
    await $(DynamicAnswerPage.submit()).click();
    await $(SetMinimumPage.setMinimum()).setValue(2);
    await $(SetMinimumPage.submit()).click();
    await $(DynamicAnswerOnlyPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(SectionSummaryPage.pageName);
    await $(SectionSummaryPage.groupContent(2)).waitForExist({ timeout: timeout });
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryTitles)[0].getText()).to.equal("Percentage of shopping at Aldi");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues)[0].getText()).to.equal("21%");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryTitles).length).to.equal(5);
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues).length).to.equal(5);
  });
  it("Given list items have been added and the dynamic answers are submitted, When the driving question is changed to 'No', Then after changing answer to 'Yes' all answers should re-appear on summary", async () => {
    await addTwoSupermarkets(timeout);
    await $$(DynamicAnswerPage.inputs())[0].setValue(12);
    await $$(DynamicAnswerPage.inputs())[1].setValue(21);
    await $$(DynamicAnswerPage.inputs())[2].setValue(3);
    await $$(DynamicAnswerPage.inputs())[3].setValue(7);
    await setMinimumAndGetSectionSummary(timeout);
    await $(SectionSummaryPage.anySupermarketAnswerEdit()).click();
    await $(DriverPage.no()).click();
    await $(DriverPage.submit()).click();
    await expect(await $(SectionSummaryPage.supermarketsListEditLink(1)).isExisting()).to.be.false;
    await expect(await $(SectionSummaryPage.supermarketsListAddLink()).isExisting()).to.be.false;
    await $(SectionSummaryPage.anySupermarketAnswerEdit()).click();
    await $(DriverPage.yes()).click();
    await $(DriverPage.submit()).click();
    await $(SectionSummaryPage.groupContent(2)).waitForExist({ timeout: timeout });
    await expect(await $(SectionSummaryPage.supermarketsListEditLink(1)).isExisting()).to.be.true;
    await expect(await $(SectionSummaryPage.supermarketsListAddLink()).isExisting()).to.be.true;
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryTitles)[0].getText()).to.equal("Percentage of shopping at Tesco");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues)[0].getText()).to.equal("12%");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryTitles)[1].getText()).to.equal("Percentage of shopping at Aldi");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues)[1].getText()).to.equal("21%");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues)[2].getText()).to.equal("3");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues)[3].getText()).to.equal("7");
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryTitles).length).to.equal(8);
    await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryValues).length).to.equal(8);
  });
});

async function addTwoSupermarkets(timeout) {
  await $(DriverPage.yes()).click();
  await $(DriverPage.submit()).click();
  await $(ListCollectorAddPage.supermarketName()).setValue("Tesco");
  await $(ListCollectorAddPage.setMaximum()).setValue(10000);
  await $(ListCollectorAddPage.submit()).click();
  await $(ListCollectorPage.yes()).click();
  await $(ListCollectorPage.submit()).click();
  await $(ListCollectorAddPage.supermarketName()).setValue("Aldi");
  await $(ListCollectorAddPage.setMaximum()).setValue(10000);
  await $(ListCollectorAddPage.submit()).click();
  await $(ListCollectorPage.no()).click();
  await $(ListCollectorPage.submit()).click();
  await $(DynamicAnswerPage.inputs()).waitForExist({ timeout: timeout });
}

async function setMinimumAndGetSectionSummary(timeout) {
  await $(DynamicAnswerPage.submit()).click();
  await $(SetMinimumPage.setMinimum()).setValue(2);
  await $(SetMinimumPage.submit()).click();
  await $(DynamicAnswerOnlyPage.submit()).click();
  await $(SectionSummaryPage.groupContent(2)).waitForExist({ timeout: timeout });
}
