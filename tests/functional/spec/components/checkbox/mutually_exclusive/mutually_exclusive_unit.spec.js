import UnitPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-unit.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-unit-section-summary.page";

describe("Component: Mutually Exclusive Unit With Single Checkbox Override", () => {
  beforeEach(async ()=> {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
    browser.url("/questionnaire/mutually-exclusive-unit");
  });

  describe("Given the user has entered a value for the non-exclusive unit answer", () => {
    it("When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.", async ()=> {
      // Given
      await $(await UnitPage.unit()).setValue("10");
      await expect(await $(await UnitPage.unit()).getValue()).to.contain("10");

      // When
      await $(await UnitPage.unitExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(await UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(await UnitPage.unit()).getValue()).to.contain("");

      await $(await UnitPage.submit()).click();

      await expect(await $(await SummaryPage.unitExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(await SummaryPage.unitExclusiveAnswer()).getText()).to.not.have.string("10");
    });
  });

  describe("Given the user has clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive unit answer and removes focus, Then only the non-exclusive unit answer should be answered.", async ()=> {
      // Given
      await $(await UnitPage.unitExclusiveIPreferNotToSay()).click();
      await expect(await $(await UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      await $(await UnitPage.unit()).setValue("10");

      // Then
      await expect(await $(await UnitPage.unit()).getValue()).to.contain("10");
      await expect(await $(await UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await $(await UnitPage.submit()).click();

      await expect(await $(await SummaryPage.unitAnswer()).getText()).to.have.string("10");
      await expect(await $(await SummaryPage.unitAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive unit answer, Then only the non-exclusive unit answer should be answered.", async ()=> {
      // Given
      await expect(await $(await UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await $(await UnitPage.unit()).setValue("10");

      // Then
      await expect(await $(await UnitPage.unit()).getValue()).to.contain("10");
      await expect(await $(await UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await $(await UnitPage.submit()).click();

      await expect(await $(await SummaryPage.unitAnswer()).getText()).to.have.string("10");
      await expect(await $(await SummaryPage.unitAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive unit answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", async ()=> {
      // Given
      await expect(await $(await UnitPage.unit()).getValue()).to.contain("");

      // When
      await $(await UnitPage.unitExclusiveIPreferNotToSay()).click();
      await expect(await $(await UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      await $(await UnitPage.submit()).click();

      await expect(await $(await SummaryPage.unitExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(await SummaryPage.unitExclusiveAnswer()).getText()).to.not.have.string("10");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async ()=> {
      // Given
      await expect(await $(await UnitPage.unit()).getValue()).to.contain("");
      await expect(await $(await UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await $(await UnitPage.submit()).click();

      // Then
      await expect(await $(await SummaryPage.unitAnswer()).getText()).to.contain("No answer provided");
    });
  });
});
