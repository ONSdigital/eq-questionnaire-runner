import MonthYearDatePage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-month-year-date.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-month-year-date-section-summary.page";
import { click, waitForPageToLoad } from "../../../../helpers";

describe("Component: Mutually Exclusive Month Year Date With Single Checkbox Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
    await waitForPageToLoad();
    await browser.url("/questionnaire/mutually-exclusive-month-year-date");
  });

  describe("Given the user has entered a value for the non-exclusive month year date answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.", async () => {
      // Given
      await $(MonthYearDatePage.monthYearDateMonth()).setValue("3");
      await $(MonthYearDatePage.monthYearDateYear()).setValue("2018");
      await expect(await $(MonthYearDatePage.monthYearDateMonth()).getValue()).toBe("3");
      await expect(await $(MonthYearDatePage.monthYearDateYear()).getValue()).toBe("2018");

      // When
      await $(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await expect(await $(MonthYearDatePage.monthYearDateMonth()).getValue()).toBe("");
      await expect(await $(MonthYearDatePage.monthYearDateYear()).getValue()).toBe("");

      await click(MonthYearDatePage.submit());

      await expect(await $(SummaryPage.monthYearDateExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.monthYearDateExclusiveAnswer()).getText()).not.toBe("March 2018");
    });
  });

  describe("Given the user has clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.", async () => {
      // Given
      await $(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).click();
      await expect(await $(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).toBe(true);

      // When
      await $(MonthYearDatePage.monthYearDateMonth()).setValue("3");
      await $(MonthYearDatePage.monthYearDateYear()).setValue("2018");

      // Then
      await expect(await $(MonthYearDatePage.monthYearDateMonth()).getValue()).toBe("3");
      await expect(await $(MonthYearDatePage.monthYearDateYear()).getValue()).toBe("2018");

      await expect(await $(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      await click(MonthYearDatePage.submit());

      await expect(await $(SummaryPage.monthYearDateAnswer()).getText()).toBe("March 2018");
      await expect(await $(SummaryPage.monthYearDateAnswer()).getText()).not.toBe("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive month year date answer, Then only the non-exclusive month year date answer should be answered.", async () => {
      // Given
      await expect(await $(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // When
      await $(MonthYearDatePage.monthYearDateMonth()).setValue("3");
      await $(MonthYearDatePage.monthYearDateYear()).setValue("2018");

      // Then
      await expect(await $(MonthYearDatePage.monthYearDateMonth()).getValue()).toBe("3");
      await expect(await $(MonthYearDatePage.monthYearDateYear()).getValue()).toBe("2018");
      await expect(await $(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      await click(MonthYearDatePage.submit());

      await expect(await $(SummaryPage.monthYearDateAnswer()).getText()).toBe("March 2018");
      await expect(await $(SummaryPage.monthYearDateAnswer()).getText()).not.toBe("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive month year date answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", async () => {
      // Given
      await expect(await $(MonthYearDatePage.monthYearDateMonth()).getValue()).toBe("");
      await expect(await $(MonthYearDatePage.monthYearDateYear()).getValue()).toBe("");

      // When
      await $(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).click();
      await expect(await $(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).toBe(true);

      // Then
      await click(MonthYearDatePage.submit());

      await expect(await $(SummaryPage.monthYearDateExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.monthYearDateExclusiveAnswer()).getText()).not.toBe("March 2018");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async () => {
      // Given
      await expect(await $(MonthYearDatePage.monthYearDateMonth()).getValue()).toBe("");
      await expect(await $(MonthYearDatePage.monthYearDateYear()).getValue()).toBe("");
      await expect(await $(MonthYearDatePage.monthYearDateExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // When
      await click(MonthYearDatePage.submit());

      // Then
      await expect(await $(SummaryPage.monthYearDateAnswer()).getText()).toBe("No answer provided");
    });
  });
});
