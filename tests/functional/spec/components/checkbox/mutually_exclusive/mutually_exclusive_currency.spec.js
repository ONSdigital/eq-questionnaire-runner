import CurrencyPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-currency.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-currency-section-summary.page";
import { click } from "../../../../helpers";

describe("Component: Mutually Exclusive Currency With Single Checkbox Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
    await browser.pause(100);
    await browser.url("/questionnaire/mutually-exclusive-currency");
  });

  describe("Given the user has entered a value for the non-exclusive currency answer", () => {
    it("When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.", async () => {
      // Given
      await $(CurrencyPage.currency()).setValue("123");
      await expect(await $(CurrencyPage.currency()).getValue()).to.contain("123");

      // When
      await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(CurrencyPage.currency()).getValue()).to.contain("");

      await click(CurrencyPage.submit());

      await expect(await $(SummaryPage.currencyExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SummaryPage.currencyExclusiveAnswer()).getText()).to.not.have.string("123");
    });
  });

  describe("Given the user has clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive currency answer and removes focus, Then only the non-exclusive currency answer should be answered.", async () => {
      // Given
      await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).click();
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      await $(CurrencyPage.currency()).setValue("123");

      // Then
      await $(CurrencyPage.currency()).getValue();
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await click(CurrencyPage.submit());

      await expect(await $(SummaryPage.currencyAnswer()).getText()).to.have.string("123");
      await expect(await $(SummaryPage.currencyAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive currency answer, Then only the non-exclusive currency answer should be answered.", async () => {
      // Given
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await $(CurrencyPage.currency()).setValue("123");

      // Then
      await expect(await $(CurrencyPage.currency()).getValue()).to.contain("123");
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await click(CurrencyPage.submit());

      await expect(await $(SummaryPage.currencyAnswer()).getText()).to.have.string("123");
      await expect(await $(SummaryPage.currencyAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive currency answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", async () => {
      // Given
      await expect(await $(CurrencyPage.currency()).getValue()).to.contain("");

      // When
      await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).click();
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      await click(CurrencyPage.submit());

      await expect(await $(SummaryPage.currencyExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SummaryPage.currencyExclusiveAnswer()).getText()).to.not.have.string("123");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async () => {
      // Given
      await expect(await $(CurrencyPage.currency()).getValue()).to.contain("");
      await expect(await $(CurrencyPage.currencyExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await click(CurrencyPage.submit());

      // Then
      await expect(await $(SummaryPage.currencyAnswer()).getText()).to.contain("No answer provided");
    });
  });
});
