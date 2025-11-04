import CurrencyPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-currency.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-currency-section-summary.page";
import { click, waitForQuestionnaireToLoad } from "../../../../helpers";

describe("Component: Mutually Exclusive Currency With Single Checkbox Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
    await waitForQuestionnaireToLoad();
    await browser.url("/questionnaire/mutually-exclusive-currency");
  });

  describe("Given the user has entered a value for the non-exclusive currency answer", () => {
    it("When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.", async () => {
      // Given
      await $(CurrencyPage.currency()).setValue("123");
      await expect(await $(CurrencyPage.currency()).getValue()).toBe("123");

      // When
      await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await expect(await $(CurrencyPage.currency()).getValue()).toBe("");

      await click(CurrencyPage.submit());

      await expect(await $(SummaryPage.currencyExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.currencyExclusiveAnswer()).getText()).not.toBe("123");
    });
  });

  describe("Given the user has clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive currency answer and removes focus, Then only the non-exclusive currency answer should be answered.", async () => {
      // Given
      await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).click();
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).toBe(true);

      // When
      await $(CurrencyPage.currency()).setValue("123");

      // Then
      await $(CurrencyPage.currency()).getValue();
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      await click(CurrencyPage.submit());

      await expect(await $(SummaryPage.currencyAnswer()).getText()).toBe("£123");
      await expect(await $(SummaryPage.currencyAnswer()).getText()).not.toBe("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive currency answer, Then only the non-exclusive currency answer should be answered.", async () => {
      // Given
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // When
      await $(CurrencyPage.currency()).setValue("123");

      // Then
      await expect(await $(CurrencyPage.currency()).getValue()).toBe("123");
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      await click(CurrencyPage.submit());

      await expect(await $(SummaryPage.currencyAnswer()).getText()).toBe("£123");
      await expect(await $(SummaryPage.currencyAnswer()).getText()).not.toBe("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive currency answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", async () => {
      // Given
      await expect(await $(CurrencyPage.currency()).getValue()).toBe("");

      // When
      await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).click();
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).toBe(true);

      // Then
      await click(CurrencyPage.submit());

      await expect(await $(SummaryPage.currencyExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.currencyExclusiveAnswer()).getText()).not.toBe("123");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async () => {
      // Given
      await expect(await $(CurrencyPage.currency()).getValue()).toBe("");
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // When
      await click(CurrencyPage.submit());

      // Then
      await expect(await $(SummaryPage.currencyAnswer()).getText()).toBe("No answer provided");
    });
  });
});
