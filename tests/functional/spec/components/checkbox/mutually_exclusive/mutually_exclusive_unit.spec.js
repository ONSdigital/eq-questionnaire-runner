import UnitPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-unit.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-unit-section-summary.page";
import { click } from "../../../../helpers";

describe("Component: Mutually Exclusive Unit With Single Checkbox Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
    await browser.pause(1000);
    await browser.url(UnitPage.url());
  });

  describe("Given the user has entered a value for the non-exclusive unit answer", () => {
    it("When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.", async () => {
      // Given
      await $(UnitPage.unit()).setValue("10");
      await expect(await $(UnitPage.unit()).getValue()).toBe("10");

      // When
      await $(UnitPage.unitExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await expect(await $(UnitPage.unit()).getValue()).toBe("");

      await click(UnitPage.submit());

      await expect(await $(SummaryPage.unitExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.unitExclusiveAnswer()).getText()).not.toBe("10");
    });
  });

  describe("Given the user has clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive unit answer and removes focus, Then only the non-exclusive unit answer should be answered.", async () => {
      // Given
      await $(UnitPage.unitExclusiveIPreferNotToSay()).click();
      await expect(await $(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).toBe(true);

      // When
      await $(UnitPage.unit()).setValue("10");

      // Then
      await expect(await $(UnitPage.unit()).getValue()).toContain("10");
      await expect(await $(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      await click(UnitPage.submit());

      await expect(await $(SummaryPage.unitAnswer()).getText()).toContain("10");
      await expect(await $(SummaryPage.unitAnswer()).getText()).not.toBe("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive unit answer, Then only the non-exclusive unit answer should be answered.", async () => {
      // Given
      await expect(await $(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // When
      await $(UnitPage.unit()).setValue("10");

      // Then
      await expect(await $(UnitPage.unit()).getValue()).toBe("10");
      await expect(await $(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      await click(UnitPage.submit());

      await expect(await $(SummaryPage.unitAnswer()).getText()).toContain("10");
      await expect(await $(SummaryPage.unitAnswer()).getText()).not.toBe("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive unit answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", async () => {
      // Given
      await expect(await $(UnitPage.unit()).getValue()).toBe("");

      // When
      await $(UnitPage.unitExclusiveIPreferNotToSay()).click();
      await expect(await $(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).toBe(true);

      // Then
      await click(UnitPage.submit());

      await expect(await $(SummaryPage.unitExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.unitExclusiveAnswer()).getText()).not.toBe("10");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async () => {
      // Given
      await expect(await $(UnitPage.unit()).getValue()).toBe("");
      await expect(await $(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // When
      await click(UnitPage.submit());

      // Then
      await expect(await $(SummaryPage.unitAnswer()).getText()).toBe("No answer provided");
    });
  });
});
