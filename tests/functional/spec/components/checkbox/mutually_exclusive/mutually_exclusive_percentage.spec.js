import PercentagePage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-percentage.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-percentage-section-summary.page";
import { click } from "../../../../helpers";

describe("Component: Mutually Exclusive Percentage With Single Checkbox Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
    await browser.pause(100);
    await browser.url("/questionnaire/mutually-exclusive-percentage");
  });

  describe("Given the user has entered a value for the non-exclusive percentage answer", () => {
    it("When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.", async () => {
      // Given
      await $(PercentagePage.percentage()).setValue("99");
      await expect(await $(PercentagePage.percentage()).getValue()).toEqual("99");

      // When
      await $(PercentagePage.percentageExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await expect(await $(PercentagePage.percentage()).getValue()).toEqual("");

      await click(PercentagePage.submit());

      await expect(await $(SummaryPage.percentageExclusiveAnswer()).getText()).toEqual("I prefer not to say");
      await expect(await $(SummaryPage.percentageExclusiveAnswer()).getText()).not.toEqual("99");
    });
  });

  describe("Given the user has clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive percentage answer and removes focus, Then only the non-exclusive percentage answer should be answered.", async () => {
      // Given
      await browser.url("/questionnaire/mutually-exclusive-percentage");
      await $(PercentagePage.percentageExclusiveIPreferNotToSay()).click();
      await expect(await $(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).toBe(true);

      // When
      await $(PercentagePage.percentage()).setValue("99");

      // Then
      await expect(await $(PercentagePage.percentage()).getValue()).toContain("99");
      await expect(await $(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      await click(PercentagePage.submit());

      await expect(await $(SummaryPage.percentageAnswer()).getText()).toContain("99");
      await expect(await $(SummaryPage.percentageAnswer()).getText()).not.toEqual("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive percentage answer, Then only the non-exclusive percentage answer should be answered.", async () => {
      // Given
      await expect(await $(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // When
      await $(PercentagePage.percentage()).setValue("99");

      // Then
      await expect(await $(PercentagePage.percentage()).getValue()).toContain("99");
      await expect(await $(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      await click(PercentagePage.submit());

      await expect(await $(SummaryPage.percentageAnswer()).getText()).toContain("99");
      await expect(await $(SummaryPage.percentageAnswer()).getText()).not.toEqual("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive percentage answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", async () => {
      // Given
      await expect(await $(PercentagePage.percentage()).getValue()).toEqual("");

      // When
      await $(PercentagePage.percentageExclusiveIPreferNotToSay()).click();
      await expect(await $(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).toBe(true);

      // Then
      await click(PercentagePage.submit());

      await expect(await $(SummaryPage.percentageExclusiveAnswer()).getText()).toEqual("I prefer not to say");
      await expect(await $(SummaryPage.percentageExclusiveAnswer()).getText()).not.toEqual("British\nIrish");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async () => {
      // Given
      await expect(await $(PercentagePage.percentage()).getValue()).toEqual("");
      await expect(await $(PercentagePage.percentageExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // When
      await click(PercentagePage.submit());

      // Then
      await expect(await $(SummaryPage.percentageAnswer()).getText()).toEqual("No answer provided");
    });
  });
});
