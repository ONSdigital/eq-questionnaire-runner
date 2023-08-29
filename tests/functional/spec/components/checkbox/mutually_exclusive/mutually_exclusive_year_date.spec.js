import YearDatePage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-year-date.page";
import SubmitPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-year-date-section-summary.page";
import { click } from "../../../../helpers";

describe("Component: Mutually Exclusive Year Date With Single Checkbox Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
    await browser.pause(100);
    await browser.url("/questionnaire/mutually-exclusive-year-date");
  });

  describe("Given the user has entered a value for the non-exclusive year date answer", () => {
    it("When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.", async () => {
      // Given
      await $(YearDatePage.yearDateYear()).setValue("2018");
      await expect(await $(YearDatePage.yearDateYear()).getValue()).to.contain("2018");

      // When
      await $(YearDatePage.yearDateExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(YearDatePage.yearDateYear()).getValue()).to.contain("");

      await click(YearDatePage.submit());

      await expect(await $(SubmitPage.yearDateExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SubmitPage.yearDateExclusiveAnswer()).getText()).to.not.have.string("2018");
    });
  });

  describe("Given the user has clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive year date answer and removes focus, Then only the non-exclusive year date answer should be answered.", async () => {
      // Given
      await $(YearDatePage.yearDateExclusiveIPreferNotToSay()).click();
      await expect(await $(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      await $(YearDatePage.yearDateYear()).setValue("2018");

      // Then
      await expect(await $(YearDatePage.yearDateYear()).getValue()).to.contain("2018");
      await expect(await $(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await click(YearDatePage.submit());

      await expect(await $(SubmitPage.yearDateAnswer()).getText()).to.have.string("2018");
      await expect(await $(SubmitPage.yearDateAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive year date answer, Then only the non-exclusive year date answer should be answered.", async () => {
      // Given
      await expect(await $(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await $(YearDatePage.yearDateYear()).setValue("2018");

      // Then
      await expect(await $(YearDatePage.yearDateYear()).getValue()).to.contain("2018");
      await expect(await $(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await click(YearDatePage.submit());

      await expect(await $(SubmitPage.yearDateAnswer()).getText()).to.have.string("2018");
      await expect(await $(SubmitPage.yearDateAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive year date answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", async () => {
      // Given
      await expect(await $(YearDatePage.yearDateYear()).getValue()).to.contain("");

      // When
      await $(YearDatePage.yearDateExclusiveIPreferNotToSay()).click();
      await expect(await $(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      await click(YearDatePage.submit());

      await expect(await $(SubmitPage.yearDateExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SubmitPage.yearDateExclusiveAnswer()).getText()).to.not.have.string("2018");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async () => {
      // Given
      await expect(await $(YearDatePage.yearDateYear()).getValue()).to.contain("");
      await expect(await $(YearDatePage.yearDateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await click(YearDatePage.submit());

      // Then
      await expect(await $(SubmitPage.yearDateAnswer()).getText()).to.contain("No answer provided");
    });
  });
});
