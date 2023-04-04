import DriverPage from "../generated_pages/dynamic_answers_list/any-supermarket.page";
import DynamicAnswerPage from "../generated_pages/dynamic_answers_list/dynamic-answer.page";
import ListCollectorPage from "../generated_pages/dynamic_answers_list/list-collector.page";
import ListCollectorAddPage from "../generated_pages/dynamic_answers_list/list-collector-add.page";
import ListCollectorRemovePage from "../generated_pages/dynamic_answers_list/list-collector-remove.page";
import SectionSummaryPage from "../generated_pages/dynamic_answers_list/section-summary.page";
import { expect } from "chai";

describe("Dynamic answers list value source", () => {
  const labels = 'label[class="ons-label"]';
  const inputs = 'input[class="ons-input ons-input--text ons-input-type__input ons-input-number--w-3"]';
  const group = 'div[id="group-2"]';
  const summaryTitles = 'dt[class="ons-summary__item-title"]';
  const summaryValues = 'dd[class="ons-summary__values"]';
  const summaryActions = 'dd[class="ons-summary__actions"]';
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_dynamic_answers_list.json");
  });

  it("Given list items have been added, When the dynamic answers are displayed, Then the correct answers should be visible", async () => {
    await addTwoSupermarkets();
    await expect(await $$(labels)[0].getText()).to.equal("Percentage of shopping at Tesco");
    await expect(await $$(labels)[1].getText()).to.equal("Percentage of shopping at Aldi");
    await expect(await $$(labels).length).to.equal(2);
  });
  it("Given list items have been added, When additional items are added using add link, Then the correct dynamic answers are displayed", async () => {
    await $(DriverPage.yes()).click();
    await $(DriverPage.submit()).click();
    await $(ListCollectorAddPage.supermarketName()).setValue("Tesco");
    await $(ListCollectorAddPage.submit()).click();
    await $(ListCollectorPage.no()).click();
    await $(ListCollectorPage.submit()).click();
    await expect(await $$(labels)[0].getText()).to.equal("Percentage of shopping at Tesco");
    await expect(await $$(labels).length).to.equal(1);
    await $(DynamicAnswerPage.submit()).click();
    await $(SectionSummaryPage.supermarketsListAddLink()).click();
    await $(ListCollectorAddPage.supermarketName()).setValue("Aldi");
    await $(ListCollectorAddPage.submit()).click();
    await $(ListCollectorPage.no()).click();
    await $(ListCollectorPage.submit()).click();
    await expect(await $$(labels)[0].getText()).to.equal("Percentage of shopping at Tesco");
    await expect(await $$(labels)[1].getText()).to.equal("Percentage of shopping at Aldi");
    await expect(await $$(labels).length).to.equal(2);
  });
  it("Given list items have been added and the dynamic answers are submitted, When the summary is displayed, Then the correct answers should be visible and have correct values", async () => {
    await addTwoSupermarkets();
    await $$(inputs)[0].setValue(12);
    await $$(inputs)[1].setValue(21);
    await $(DynamicAnswerPage.submit()).click();
    await expect(await $(group).$$(summaryTitles)[0].getText()).to.equal("Percentage of shopping at Tesco");
    await expect(await $(group).$$(summaryValues)[0].getText()).to.equal("12%");
    await expect(await $(group).$$(summaryTitles)[1].getText()).to.equal("Percentage of shopping at Aldi");
    await expect(await $(group).$$(summaryValues)[1].getText()).to.equal("21%");
    await expect(await $(group).$$(summaryTitles).length).to.equal(2);
    await expect(await $(group).$$(summaryValues).length).to.equal(2);
  });
  it("Given list items have been added and the dynamic answers are submitted, When the dynamic answers are revisited, Then they should be visible and have correct values", async () => {
    await addTwoSupermarkets();
    await $$(inputs)[0].setValue(12);
    await $$(inputs)[1].setValue(21);
    await $(DynamicAnswerPage.submit()).click();
    await $(SectionSummaryPage.previous()).click();
    await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
    await expect(await $$(inputs)[0].getValue()).to.equal("12");
    await expect(await $$(inputs)[1].getValue()).to.equal("21");
    await expect(await $$(labels)[0].getText()).to.equal("Percentage of shopping at Tesco");
    await expect(await $$(labels)[1].getText()).to.equal("Percentage of shopping at Aldi");
  });
  it("Given list items have been added and the dynamic answers are submitted, When the dynamic answers are resubmitted with different values, Then they should be displayed correctly on summary", async () => {
    await addTwoSupermarkets();
    await $$(inputs)[0].setValue(12);
    await $$(inputs)[1].setValue(21);
    await $(DynamicAnswerPage.submit()).click();
    await $(SectionSummaryPage.previous()).click();
    await $$(inputs)[0].setValue(21);
    await $$(inputs)[1].setValue(12);
    await $(DynamicAnswerPage.submit()).click();
    await expect(await $(group).$$(summaryValues)[0].getText()).to.equal("21%");
    await expect(await $(group).$$(summaryValues)[1].getText()).to.equal("12%");
  });
  it("Given list items have been added and the dynamic answers are submitted, When the summary edit answer link is used for dynamic answer, Then the focus is on correct answer option", async () => {
    await addTwoSupermarkets();
    await $$(inputs)[0].setValue(12);
    await $$(inputs)[1].setValue(21);
    await $(DynamicAnswerPage.submit()).click();
    await $(group).$$(summaryActions)[0].$("a").click();
    await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
    await expect(await $$(inputs)[0].isFocused()).to.be.true;
    await $(DynamicAnswerPage.submit()).click();
    await $(group).$$(summaryActions)[1].$("a").click();
    await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
    await expect(await $$(inputs)[1].isFocused()).to.be.true;
  });
  it("Given list items have been added and the dynamic answers are submitted, When the dynamic answers are resubmitted with answers updated, Then they should be displayed correctly on summary", async () => {
    await addTwoSupermarkets();
    await $$(inputs)[0].setValue(12);
    await $$(inputs)[1].setValue(21);
    await $(DynamicAnswerPage.submit()).click();
    await $(group).$$(summaryActions)[0].$("a").click();
    await $$(inputs)[0].setValue(21);
    await $(DynamicAnswerPage.submit()).click();
    await expect(await $(group).$$(summaryValues)[0].getText()).to.equal("21%");
    await expect(await $(group).$$(summaryValues)[1].getText()).to.equal("21%");
  });
  it("Given list items have been added and the dynamic answers are submitted, When the list items are removed and answers updated, Then they should be displayed correctly on summary", async () => {
    await addTwoSupermarkets();
    await $$(inputs)[0].setValue(12);
    await $$(inputs)[1].setValue(21);
    await $(DynamicAnswerPage.submit()).click();
    await $(SectionSummaryPage.supermarketsListRemoveLink(1)).click();
    await $(ListCollectorRemovePage.yes()).click();
    await $(ListCollectorRemovePage.submit()).click();
    await $(DynamicAnswerPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(SectionSummaryPage.pageName);
    await expect(await $(group).$$(summaryTitles)[0].getText()).to.equal("What percent of your shopping do you do at each of the following supermarket?");
    await expect(await $(group).$$(summaryValues)[0].getText()).to.equal("21%");
    await expect(await $(group).$$(summaryTitles).length).to.equal(1);
    await expect(await $(group).$$(summaryValues).length).to.equal(1);
  });
  it("Given list items have been added and the dynamic answers are submitted, When the driving question is changed to 'No', Then after changing answer to 'Yes' all answers should re-appear on summary", async () => {
    await addTwoSupermarkets();
    await $$(inputs)[0].setValue(12);
    await $$(inputs)[1].setValue(21);
    await $(DynamicAnswerPage.submit()).click();
    await $(SectionSummaryPage.anySupermarketAnswerEdit()).click();
    await $(DriverPage.no()).click();
    await $(DriverPage.submit()).click();
    await expect(await $(SectionSummaryPage.supermarketsListEditLink(1)).isExisting()).to.be.false;
    await expect(await $(SectionSummaryPage.supermarketsListAddLink()).isExisting()).to.be.false;
    await expect(await $(group).isExisting()).to.be.false;
    await $(SectionSummaryPage.anySupermarketAnswerEdit()).click();
    await $(DriverPage.yes()).click();
    await $(DriverPage.submit()).click();
    await expect(await $(SectionSummaryPage.supermarketsListEditLink(1)).isExisting()).to.be.true;
    await expect(await $(SectionSummaryPage.supermarketsListAddLink()).isExisting()).to.be.true;
    await expect(await $(group).$$(summaryTitles)[0].getText()).to.equal("Percentage of shopping at Tesco");
    await expect(await $(group).$$(summaryValues)[0].getText()).to.equal("12%");
    await expect(await $(group).$$(summaryTitles)[1].getText()).to.equal("Percentage of shopping at Aldi");
    await expect(await $(group).$$(summaryValues)[1].getText()).to.equal("21%");
    await expect(await $(group).$$(summaryTitles).length).to.equal(2);
    await expect(await $(group).$$(summaryValues).length).to.equal(2);
  });
});

async function addTwoSupermarkets() {
  await $(DriverPage.yes()).click();
  await $(DriverPage.submit()).click();
  await $(ListCollectorAddPage.supermarketName()).setValue("Tesco");
  await $(ListCollectorAddPage.submit()).click();
  await $(ListCollectorPage.yes()).click();
  await $(ListCollectorPage.submit()).click();
  await $(ListCollectorAddPage.supermarketName()).setValue("Aldi");
  await $(ListCollectorAddPage.submit()).click();
  await $(ListCollectorPage.no()).click();
  await $(ListCollectorPage.submit()).click();
}
