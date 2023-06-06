import ListCollectorPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers_based_on_list_collector/list-collector.page";
import ListCollectorAddPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers_based_on_list_collector/list-collector-add.page";
import DynamicAnswerPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers_based_on_list_collector/dynamic-answer.page";
import DynamicAnswerOnlyPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers_based_on_list_collector/dynamic-answer-only.page";
import TotalBlockPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers_based_on_list_collector/total-block.page";
import DriverPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers_based_on_list_collector/any-supermarket.page";
import SectionSummaryPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers_based_on_list_collector/section-summary.page";
import ListCollectorRemovePage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers_based_on_list_collector/list-collector-remove.page";
import ListCollectorEditPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers_based_on_list_collector/list-collector-edit.page";

describe("Feature: Sum of dynamic answers based on list and optional static answers equal to validation against total ", () => {
  const labels = ".ons-label";
  const percentageInputs = 'input[class="ons-input ons-input--text ons-input-type__input ons-input-number--w-3"]';
  const currencyInputs = 'input[class="ons-input ons-input--text ons-input-type__input"]';
  const group = 'div[id="group-2"]';
  const summaryTitles = 'dt[class="ons-summary__item-title"]';
  beforeEach(async () => {
    await browser.openQuestionnaire("test_validation_sum_against_total_dynamic_answers_based_on_list_collector.json");
  });

  describe("Given I start a grouped answer with multi rule validation survey and enter 10 into the total", () => {
    it("When I continue and enter nothing, all zeros or 10 at breakdown level, Then I should be able to get to the summary", async () => {
      await addTwoSupermarkets();
      await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
      await expect(await $$(labels).length).to.equal(3);
      await $$(percentageInputs)[0].setValue(33);
      await $$(percentageInputs)[1].setValue(33);
      await $(DynamicAnswerPage.percentageOfShoppingElsewhere()).setValue(33);
      await $(DynamicAnswerPage.submit()).click();
      await expect(await $(DynamicAnswerPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to 100");
    });
  });
  describe("Given I start a grouped answer with multi rule validation survey and enter 10 into the total", () => {
    it("When I continue and enter nothing, all zeros or 10 at breakdown level, Then I should be able to get to the summary", async () => {
      await addTwoSupermarkets();
      await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
      await expect(await $$(labels).length).to.equal(3);
      await $$(percentageInputs)[0].setValue(34);
      await $$(percentageInputs)[1].setValue(33);
      await $(DynamicAnswerPage.percentageOfShoppingElsewhere()).setValue(33);
      await $(DynamicAnswerPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(TotalBlockPage.pageName);
    });
  });
  describe("Given I start a grouped answer with multi rule validation survey and enter 10 into the total", () => {
    it("When I continue and enter nothing, all zeros or 10 at breakdown level, Then I should be able to get to the summary", async () => {
      await addTwoSupermarkets();
      await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
      await expect(await $$(labels).length).to.equal(3);
      await $$(percentageInputs)[0].setValue(34);
      await $$(percentageInputs)[1].setValue(33);
      await $(DynamicAnswerPage.percentageOfShoppingElsewhere()).setValue(33);
      await $(DynamicAnswerPage.submit()).click();
      await $(TotalBlockPage.total()).setValue(100);
      await $(TotalBlockPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(DynamicAnswerOnlyPage.pageName);
      await $$(currencyInputs)[0].setValue(50);
      await $$(currencyInputs)[1].setValue(0);
      await $(DynamicAnswerOnlyPage.submit()).click();
      await expect(await $(DynamicAnswerOnlyPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to £100.00");
    });
  });
  describe("Given I start a grouped answer with multi rule validation survey and enter 10 into the total", () => {
    it("When I continue and enter nothing, all zeros or 10 at breakdown level, Then I should be able to get to the summary", async () => {
      await addTwoSupermarkets();
      await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
      await expect(await $$(labels).length).to.equal(3);
      await $$(percentageInputs)[0].setValue(34);
      await $$(percentageInputs)[1].setValue(33);
      await $(DynamicAnswerPage.percentageOfShoppingElsewhere()).setValue(33);
      await $(DynamicAnswerPage.submit()).click();
      await $(TotalBlockPage.total()).setValue(100);
      await $(TotalBlockPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(DynamicAnswerOnlyPage.pageName);
      await $$(currencyInputs)[0].setValue(50);
      await $$(currencyInputs)[1].setValue(50);
      await $(DynamicAnswerOnlyPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.pageName);
    });
  });
  describe("Given I start a grouped answer with multi rule validation survey and enter 10 into the total", () => {
    it("When I continue and enter nothing, all zeros or 10 at breakdown level, Then I should be able to get to the summary", async () => {
      await addTwoSupermarkets();
      await expect(await $$(labels).length).to.equal(3);
      await $$(percentageInputs)[0].setValue(34);
      await $$(percentageInputs)[1].setValue(33);
      await $(DynamicAnswerPage.percentageOfShoppingElsewhere()).setValue(33);
      await $(DynamicAnswerPage.submit()).click();
      await $(TotalBlockPage.total()).setValue(100);
      await $(TotalBlockPage.submit()).click();
      await $$(currencyInputs)[0].setValue(50);
      await $$(currencyInputs)[1].setValue(50);
      await $(DynamicAnswerOnlyPage.submit()).click();
      await $(SectionSummaryPage.supermarketsListAddLink()).click();
      await $(ListCollectorAddPage.supermarketName()).setValue("Morrisons");
      await $(ListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
      await expect(await $$(labels).length).to.equal(4);
    });
  });
  describe("Given I start a grouped answer with multi rule validation survey and enter 10 into the total", () => {
    it("When I continue and enter nothing, all zeros or 10 at breakdown level, Then I should be able to get to the summary", async () => {
      await addTwoSupermarkets();
      await expect(await $$(labels).length).to.equal(3);
      await $$(percentageInputs)[0].setValue(34);
      await $$(percentageInputs)[1].setValue(33);
      await $(DynamicAnswerPage.percentageOfShoppingElsewhere()).setValue(33);
      await $(DynamicAnswerPage.submit()).click();
      await $(TotalBlockPage.total()).setValue(100);
      await $(TotalBlockPage.submit()).click();
      await $$(currencyInputs)[0].setValue(50);
      await $$(currencyInputs)[1].setValue(50);
      await $(DynamicAnswerOnlyPage.submit()).click();
      await $(SectionSummaryPage.supermarketsListRemoveLink(1)).click();
      await $(ListCollectorRemovePage.yes()).click();
      await $(ListCollectorRemovePage.submit()).click();
      await expect(await browser.getUrl()).to.contain(DynamicAnswerPage.pageName);
      await expect(await $$(labels).length).to.equal(2);
    });
  });
  describe("Given I start a grouped answer with multi rule validation survey and enter 10 into the total", () => {
    it("When I continue and enter nothing, all zeros or 10 at breakdown level, Then I should be able to get to the summary", async () => {
      await addTwoSupermarkets();
      await expect(await $$(labels).length).to.equal(3);
      await $$(percentageInputs)[0].setValue(34);
      await $$(percentageInputs)[1].setValue(33);
      await $(DynamicAnswerPage.percentageOfShoppingElsewhere()).setValue(33);
      await $(DynamicAnswerPage.submit()).click();
      await $(TotalBlockPage.total()).setValue(100);
      await $(TotalBlockPage.submit()).click();
      await $$(currencyInputs)[0].setValue(50);
      await $$(currencyInputs)[1].setValue(50);
      await $(DynamicAnswerOnlyPage.submit()).click();
      await $(SectionSummaryPage.supermarketsListEditLink(1)).click();
      await $(ListCollectorEditPage.supermarketName()).setValue("Aldi");
      await $(ListCollectorEditPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(SectionSummaryPage.pageName);
      await expect(await $(group).$$(summaryTitles)[0].getText()).to.equal("Percentage of shopping at Aldi");
    });
  });
});

async function addTwoSupermarkets() {
  await $(DriverPage.yes()).click();
  await $(DriverPage.submit()).click();
  await $(ListCollectorAddPage.supermarketName()).setValue("Tesco");
  await $(ListCollectorAddPage.submit()).click();
  await $(ListCollectorPage.yes()).click();
  await $(ListCollectorPage.submit()).click();
  await $(ListCollectorAddPage.supermarketName()).setValue("Asda");
  await $(ListCollectorAddPage.submit()).click();
  await $(ListCollectorPage.no()).click();
  await $(ListCollectorPage.submit()).click();
}
