import ListCollectorPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers/list-collector.page";
import ListCollectorAddPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers/list-collector-add.page";
import DynamicAnswerPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers/dynamic-answer.page";
import DynamicAnswerOnlyPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers/dynamic-answer-only.page";
import TotalBlockPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers/total-block.page";
import DriverPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers/any-supermarket.page";
import SectionSummaryPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers/dynamic-answers-section-summary.page";
import ListCollectorRemovePage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers/list-collector-remove.page";
import ListCollectorEditPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers/list-collector-edit.page";
import HubPage from "../../../../base_pages/hub.page";
import TotalBlockOtherPage from "../../../../generated_pages/validation_sum_against_total_dynamic_answers/total-block-other.page";
import { click, verifyUrlContains } from "../../../../helpers";

describe("Feature: Sum of dynamic answers based on list and optional static answers equal to validation against total ", () => {
  const summaryTitles = 'dt[class="ons-summary__item-title"]';
  beforeEach(async () => {
    await browser.openQuestionnaire("test_validation_sum_against_total_dynamic_answers.json");
  });

  describe("Given I add list items with hardcoded total used for validation of dynamic answers", () => {
    it("When I continue and enter numbers on dynamic and static answers page that don't add up to that total, Then validation error should be displayed with appropriate message", async () => {
      await $(TotalBlockPage.acceptCookies()).click();
      await addTwoSupermarkets();
      await verifyUrlContains(DynamicAnswerPage.pageName);
      await expect(await $$(DynamicAnswerPage.labels()).length).toBe(3);
      await $$(DynamicAnswerPage.inputs())[0].setValue(33);
      await $$(DynamicAnswerPage.inputs())[1].setValue(33);
      await $(DynamicAnswerPage.percentageOfShoppingElsewhere()).setValue(33);
      await click(DynamicAnswerPage.submit());
      await expect(await $(DynamicAnswerPage.errorNumber(1)).getText()).toBe("Enter answers that add up to 100");
    });
  });
  describe("Given I add list items with hardcoded total used for validation of dynamic answers", () => {
    it("When I continue and enter numbers on dynamic and static answers page that add up to that total, Then I should be able to get to the subsequent question", async () => {
      await addTwoSupermarkets();
      await verifyUrlContains(DynamicAnswerPage.pageName);
      await expect(await $$(DynamicAnswerPage.labels()).length).toBe(3);
      await $$(DynamicAnswerPage.inputs())[0].setValue(34);
      await $$(DynamicAnswerPage.inputs())[1].setValue(33);
      await $(DynamicAnswerPage.percentageOfShoppingElsewhere()).setValue(33);
      await click(DynamicAnswerPage.submit());
      await verifyUrlContains(TotalBlockOtherPage.pageName);
    });
  });
  describe("Given I add list items with custom total used for validation of dynamic answers", () => {
    it("When I continue and enter numbers on dynamic answers only page that don't add up to that total, Then validation error should be displayed with appropriate message", async () => {
      await addTwoSupermarkets();
      await verifyUrlContains(DynamicAnswerPage.pageName);
      await expect(await $$(DynamicAnswerPage.labels()).length).toBe(3);
      await $$(DynamicAnswerPage.inputs())[0].setValue(34);
      await $$(DynamicAnswerPage.inputs())[1].setValue(33);
      await $(DynamicAnswerPage.percentageOfShoppingElsewhere()).setValue(33);
      await click(DynamicAnswerPage.submit());
      await $(TotalBlockOtherPage.totalOther()).setValue(100);
      await click(TotalBlockOtherPage.submit());
      await verifyUrlContains(DynamicAnswerOnlyPage.pageName);
      await $$(DynamicAnswerOnlyPage.inputs())[0].setValue(50);
      await $$(DynamicAnswerOnlyPage.inputs())[1].setValue(0);
      await click(DynamicAnswerOnlyPage.submit());
      await expect(await $(DynamicAnswerOnlyPage.errorNumber(1)).getText()).toBe("Enter answers that add up to £100.00");
    });
  });
  describe("Given I add list items with custom total used for validation of dynamic answers", () => {
    it("When I continue and enter numbers on dynamic answers only page that add up to that total, Then I should be able to get to the summary", async () => {
      await addTwoSupermarkets();
      await verifyUrlContains(DynamicAnswerPage.pageName);
      await fillDynamicAnswers();
      await verifyUrlContains(SectionSummaryPage.pageName);
    });
  });
  describe("Given I add list items and fill all the dynamic answers", () => {
    it("When I continue and add another list item, Then I should be revisiting dynamic answers which should be updated to reflect the changes", async () => {
      await addTwoSupermarkets();
      await expect(await $$(DynamicAnswerPage.labels()).length).toBe(3);
      await fillDynamicAnswers();
      await $(SectionSummaryPage.supermarketsListAddLink()).click();
      await $(ListCollectorAddPage.supermarketName()).setValue("Morrisons");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await verifyUrlContains(DynamicAnswerPage.pageName);
      await expect(await $$(DynamicAnswerPage.labels()).length).toBe(4);
    });
  });
  describe("Given I add list items and fill all the dynamic answers", () => {
    it("When I continue and remove existing list item, Then I should be revisiting dynamic answers which should be updated to reflect the changes", async () => {
      await addTwoSupermarkets();
      await fillDynamicAnswers();
      await $(SectionSummaryPage.supermarketsListRemoveLink(1)).click();
      await $(ListCollectorRemovePage.yes()).click();
      await click(ListCollectorRemovePage.submit());
      await verifyUrlContains(DynamicAnswerPage.pageName);
      await expect(await $$(DynamicAnswerPage.labels()).length).toBe(2);
    });
  });
  describe("Given I add list items and fill all the dynamic answers", () => {
    it("When I continue and edit existing list item, Then I should return straight to the summary because the dynamic answers do not depend on the supermarket name", async () => {
      await addTwoSupermarkets();
      await fillDynamicAnswers();
      await $(SectionSummaryPage.supermarketsListEditLink(1)).click();
      await $(ListCollectorEditPage.supermarketName()).setValue("Aldi");
      await click(ListCollectorEditPage.submit());
      await verifyUrlContains(SectionSummaryPage.pageName);
      await expect(await $(SectionSummaryPage.groupContent(2)).$$(summaryTitles)[0].getText()).toBe("Percentage of shopping at Aldi");
    });
  });
  describe("Given I add list items and fill all the dynamic answers", () => {
    it("When I journey backwards, Then I should be revisiting all the previous blocks", async () => {
      await addTwoSupermarkets();
      await fillDynamicAnswers();
      await verifyUrlContains(SectionSummaryPage.pageName);
      await $(SectionSummaryPage.previous()).click();
      await $(DynamicAnswerOnlyPage.previous()).click();
      await $(TotalBlockOtherPage.previous()).click();
      await $(DynamicAnswerPage.previous()).click();
      await $(ListCollectorPage.previous()).click();
      await verifyUrlContains(DriverPage.pageName);
    });
  });
});

async function addTwoSupermarkets() {
  await $(TotalBlockPage.total()).setValue(100);
  await click(TotalBlockPage.submit());
  await $(HubPage.summaryRowLink("dynamic-answers-section")).click();
  await $(DriverPage.yes()).click();
  await click(DriverPage.submit());
  await $(ListCollectorAddPage.supermarketName()).setValue("Tesco");
  await click(ListCollectorAddPage.submit());
  await $(ListCollectorPage.yes()).click();
  await click(ListCollectorPage.submit());
  await $(ListCollectorAddPage.supermarketName()).setValue("Asda");
  await click(ListCollectorAddPage.submit());
  await $(ListCollectorPage.no()).click();
  await click(ListCollectorPage.submit());
}

async function fillDynamicAnswers() {
  await $$(DynamicAnswerPage.inputs())[0].setValue(34);
  await $$(DynamicAnswerPage.inputs())[1].setValue(33);
  await $(DynamicAnswerPage.percentageOfShoppingElsewhere()).setValue(33);
  await click(DynamicAnswerPage.submit());
  await $(TotalBlockOtherPage.totalOther()).setValue(100);
  await click(TotalBlockOtherPage.submit());
  await $$(DynamicAnswerOnlyPage.inputs())[0].setValue(50);
  await $$(DynamicAnswerOnlyPage.inputs())[1].setValue(50);
  await click(DynamicAnswerOnlyPage.submit());
}
