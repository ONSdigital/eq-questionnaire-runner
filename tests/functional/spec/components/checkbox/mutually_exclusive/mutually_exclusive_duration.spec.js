import DurationPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-duration.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-duration-section-summary.page";

describe("Component: Mutually Exclusive Duration With Single Checkbox Override", () => {
  beforeEach(async ()=> {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
    browser.url("/questionnaire/mutually-exclusive-duration");
  });

  describe("Given the user has entered a value for the non-exclusive duration answer", () => {
    it("When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.", async ()=> {
      // Given
      await $(await DurationPage.durationYears()).setValue("1");
      await $(await DurationPage.durationMonths()).setValue("7");

      await expect(await $(await DurationPage.durationYears()).getValue()).to.contain("1");
      await expect(await $(await DurationPage.durationMonths()).getValue()).to.contain("7");

      // When
      await $(await DurationPage.durationExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(await DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(await DurationPage.durationYears()).getValue()).to.contain("");
      await expect(await $(await DurationPage.durationMonths()).getValue()).to.contain("");

      await $(await DurationPage.submit()).click();

      await expect(await $(await SummaryPage.durationExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(await SummaryPage.durationExclusiveAnswer()).getText()).to.not.have.string("1 year 7 months");
    });
  });

  describe("Given the user has clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive duration answer and removes focus, Then only the non-exclusive duration answer should be answered.", async ()=> {
      // Given
      await $(await DurationPage.durationExclusiveIPreferNotToSay()).click();
      await expect(await $(await DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      await $(await DurationPage.durationYears()).setValue("1");
      await $(await DurationPage.durationMonths()).setValue("7");

      // Then
      await expect(await $(await DurationPage.durationYears()).getValue()).to.contain("1");
      await expect(await $(await DurationPage.durationMonths()).getValue()).to.contain("7");
      await expect(await $(await DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await $(await DurationPage.submit()).click();

      await expect(await $(await SummaryPage.durationAnswer()).getText()).to.have.string("1 year 7 months");
      await expect(await $(await SummaryPage.durationAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive duration answer, Then only the non-exclusive duration answer should be answered.", async ()=> {
      // Given
      await expect(await $(await DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await $(await DurationPage.durationYears()).setValue("1");
      await $(await DurationPage.durationMonths()).setValue("7");

      // Then
      await expect(await $(await DurationPage.durationYears()).getValue()).to.contain("1");
      await expect(await $(await DurationPage.durationMonths()).getValue()).to.contain("7");
      await expect(await $(await DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await $(await DurationPage.submit()).click();

      await expect(await $(await SummaryPage.durationAnswer()).getText()).to.have.string("1 year 7 months");
      await expect(await $(await SummaryPage.durationAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive duration answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", async ()=> {
      // Given
      await expect(await $(await DurationPage.durationYears()).getValue()).to.contain("");
      await expect(await $(await DurationPage.durationMonths()).getValue()).to.contain("");

      // When
      await $(await DurationPage.durationExclusiveIPreferNotToSay()).click();
      await expect(await $(await DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      await $(await DurationPage.submit()).click();

      await expect(await $(await SummaryPage.durationExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(await SummaryPage.durationExclusiveAnswer()).getText()).to.not.have.string("1 year 7 months");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async ()=> {
      // Given
      await expect(await $(await DurationPage.durationYears()).getValue()).to.contain("");
      await expect(await $(await DurationPage.durationMonths()).getValue()).to.contain("");
      await expect(await $(await DurationPage.durationExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await $(await DurationPage.submit()).click();

      // Then
      await expect(await $(await SummaryPage.durationAnswer()).getText()).to.contain("No answer provided");
    });
  });
});
