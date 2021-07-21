import UnitPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-unit.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-unit-section-summary.page";

describe("Component: Mutually Exclusive Unit With Single Checkbox Override", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_mutually_exclusive.json");
    browser.url("/questionnaire/mutually-exclusive-unit");
  });

  describe("Given the user has entered a value for the non-exclusive unit answer", () => {
    it("When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.", () => {
      // Given
      $(UnitPage.unit()).setValue("10");
      expect($(UnitPage.unit()).getValue()).to.contain("10");

      // When
      $(UnitPage.unitExclusiveIPreferNotToSay()).click();

      // Then
      expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(UnitPage.unit()).getValue()).to.contain("");

      $(UnitPage.submit()).click();

      expect($(SummaryPage.unitExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      expect($(SummaryPage.unitExclusiveAnswer()).getText()).to.not.have.string("10");
    });
  });

  describe("Given the user has clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive unit answer and removes focus, Then only the non-exclusive unit answer should be answered.", () => {
      // Given
      $(UnitPage.unitExclusiveIPreferNotToSay()).click();
      expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      $(UnitPage.unit()).setValue("10");

      // Then
      expect($(UnitPage.unit()).getValue()).to.contain("10");
      expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      $(UnitPage.submit()).click();

      expect($(SummaryPage.unitAnswer()).getText()).to.have.string("10");
      expect($(SummaryPage.unitAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive unit answer, Then only the non-exclusive unit answer should be answered.", () => {
      // Given
      expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      $(UnitPage.unit()).setValue("10");

      // Then
      expect($(UnitPage.unit()).getValue()).to.contain("10");
      expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      $(UnitPage.submit()).click();

      expect($(SummaryPage.unitAnswer()).getText()).to.have.string("10");
      expect($(SummaryPage.unitAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive unit answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", () => {
      // Given
      expect($(UnitPage.unit()).getValue()).to.contain("");

      // When
      $(UnitPage.unitExclusiveIPreferNotToSay()).click();
      expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      $(UnitPage.submit()).click();

      expect($(SummaryPage.unitExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      expect($(SummaryPage.unitExclusiveAnswer()).getText()).to.not.have.string("10");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", () => {
      // Given
      expect($(UnitPage.unit()).getValue()).to.contain("");
      expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      $(UnitPage.submit()).click();

      // Then
      expect($(SummaryPage.unitAnswer()).getText()).to.contain("No answer provided");
    });
  });
});
