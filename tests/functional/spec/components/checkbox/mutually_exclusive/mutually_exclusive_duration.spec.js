import DurationPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-duration.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-duration-section-summary.page";
import { click } from "../../../../helpers";

describe("Component: Mutually Exclusive Duration With Single Checkbox Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
    await browser.pause(100);
    await browser.url("/questionnaire/mutually-exclusive-duration");
  });

  describe("Given the user has entered a value for the non-exclusive duration answer", () => {
    it("When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.", async () => {
      // Given
      await $(DurationPage.durationYears()).setValue("1");
      await $(DurationPage.durationMonths()).setValue("7");

      await expect(await $(DurationPage.durationYears()).getValue()).to.contain("1");
      await expect(await $(DurationPage.durationMonths()).getValue()).to.contain("7");

      // When
      await $(DurationPage.durationExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(DurationPage.durationYears()).getValue()).to.contain("");
      await expect(await $(DurationPage.durationMonths()).getValue()).to.contain("");

      await click(DurationPage.submit());

      await expect(await $(SummaryPage.durationExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SummaryPage.durationExclusiveAnswer()).getText()).to.not.have.string("1 year 7 months");
    });
  });

  describe("Given the user has clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive duration answer and removes focus, Then only the non-exclusive duration answer should be answered.", async () => {
      // Given
      await $(DurationPage.durationExclusiveIPreferNotToSay()).click();
      await expect(await $(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      await $(DurationPage.durationYears()).setValue("1");
      await $(DurationPage.durationMonths()).setValue("7");

      // Then
      await expect(await $(DurationPage.durationYears()).getValue()).to.contain("1");
      await expect(await $(DurationPage.durationMonths()).getValue()).to.contain("7");
      await expect(await $(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await click(DurationPage.submit());

      await expect(await $(SummaryPage.durationAnswer()).getText()).to.have.string("1 year 7 months");
      await expect(await $(SummaryPage.durationAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive duration answer, Then only the non-exclusive duration answer should be answered.", async () => {
      // Given
      await expect(await $(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await $(DurationPage.durationYears()).setValue("1");
      await $(DurationPage.durationMonths()).setValue("7");

      // Then
      await expect(await $(DurationPage.durationYears()).getValue()).to.contain("1");
      await expect(await $(DurationPage.durationMonths()).getValue()).to.contain("7");
      await expect(await $(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await click(DurationPage.submit());

      await expect(await $(SummaryPage.durationAnswer()).getText()).to.have.string("1 year 7 months");
      await expect(await $(SummaryPage.durationAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive duration answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", async () => {
      // Given
      await browser.url("/questionnaire/mutually-exclusive-duration");
      await expect(await $(DurationPage.durationYears()).getValue()).to.contain("");
      await expect(await $(DurationPage.durationMonths()).getValue()).to.contain("");

      // When
      await $(DurationPage.durationExclusiveIPreferNotToSay()).click();
      await expect(await $(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      await click(DurationPage.submit());

      await expect(await $(SummaryPage.durationExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SummaryPage.durationExclusiveAnswer()).getText()).to.not.have.string("1 year 7 months");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async () => {
      // Given
      await browser.url("/questionnaire/mutually-exclusive-duration");
      await expect(await $(DurationPage.durationYears()).getValue()).to.contain("");
      await expect(await $(DurationPage.durationMonths()).getValue()).to.contain("");
      await expect(await $(DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await click(DurationPage.submit());

      // Then
      await expect(await $(SummaryPage.durationAnswer()).getText()).to.contain("No answer provided");
    });
  });
});
