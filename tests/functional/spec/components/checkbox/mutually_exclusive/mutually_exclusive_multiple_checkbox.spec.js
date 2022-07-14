import MandatoryCheckboxPage from "../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-checkbox.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-checkbox-section-summary.page";

describe("Component: Mutually Exclusive Checkbox With Multiple Radio Override", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_mutually_exclusive_multiple.json");
  });

  describe("Given the user has clicked multiple non-exclusive options", () => {
    beforeEach(() => {
      // Given
      $(MandatoryCheckboxPage.checkboxBritish()).click();
      $(MandatoryCheckboxPage.checkboxIrish()).click();
      $(MandatoryCheckboxPage.checkboxOther()).click();
      $(MandatoryCheckboxPage.checkboxOtherDetail()).setValue("The other option");

      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxOtherDetail()).getValue()).to.contain("The other option");
    });

    it("When then user clicks the first mutually exclusive option, Then only the first mutually exclusive option should be checked.", () => {
      // When
      $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.false;

      // Then
      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxOtherDetail()).getValue()).to.contain("");

      $(MandatoryCheckboxPage.submit()).click();

      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("British\nIrish");
    });

    it("When then user clicks the second mutually exclusive option, Then only the second mutually exclusive option should be checked.", () => {
      // When
      $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).click();
      expect($(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // Then
      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxOtherDetail()).getValue()).to.contain("");

      $(MandatoryCheckboxPage.submit()).click();

      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string("I am an alien");
      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("British\nIrish");
    });
  });

  describe("Given the user has clicked the first mutually exclusive option", () => {
    it("When the user returns to the question, Then the mutually exclusive option should remain checked.", () => {
      // Given
      $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      $(MandatoryCheckboxPage.submit()).click();

      // When
      $(SummaryPage.previous()).click();

      // Then
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;
    });
  });

  describe("Given the user has clicked the second mutually exclusive option", () => {
    it("When the user returns to the question, Then the mutually exclusive option should remain checked.", () => {
      // Given
      $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).click();
      $(MandatoryCheckboxPage.submit()).click();

      // When
      $(SummaryPage.previous()).click();

      // Then
      expect($(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.true;
    });
  });

  describe("Given the user has clicked the first mutually exclusive option", () => {
    it("When the user clicks the non-exclusive options, Then only the non-exclusive options should be checked.", () => {
      // Given
      $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      $(MandatoryCheckboxPage.checkboxBritish()).click();
      $(MandatoryCheckboxPage.checkboxIrish()).click();

      // Then
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.true;

      $(MandatoryCheckboxPage.submit()).click();

      expect($(SummaryPage.checkboxAnswer()).getText()).to.have.string("British\nIrish");
      expect($(SummaryPage.checkboxAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has clicked the second mutually exclusive option", () => {
    it("When the user clicks the non-exclusive options, Then only the non-exclusive options should be checked.", () => {
      // Given
      $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).click();
      expect($(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.true;

      // When
      $(MandatoryCheckboxPage.checkboxBritish()).click();
      $(MandatoryCheckboxPage.checkboxIrish()).click();

      // Then
      expect($(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.true;

      $(MandatoryCheckboxPage.submit()).click();

      expect($(SummaryPage.checkboxAnswer()).getText()).to.have.string("British\nIrish");
      expect($(SummaryPage.checkboxAnswer()).getText()).to.not.have.string("I am an alien");
    });
  });

  describe("Given the user has not clicked a mutually exclusive option", () => {
    it("When the user clicks multiple non-exclusive options, Then only the non-exclusive options should be checked.", () => {
      // Given
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.false;

      // When
      $(MandatoryCheckboxPage.checkboxBritish()).click();
      $(MandatoryCheckboxPage.checkboxIrish()).click();

      // Then
      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.true;

      $(MandatoryCheckboxPage.submit()).click();

      expect($(SummaryPage.checkboxAnswer()).getText()).to.have.string("British\nIrish");
      expect($(SummaryPage.checkboxAnswer()).getText()).to.not.have.string("I prefer not to say");
      expect($(SummaryPage.checkboxAnswer()).getText()).to.not.have.string("I am an alien");
    });
  });

  describe("Given the user has not clicked any of the non-exclusive options", () => {
    beforeEach(() => {
      // Given
      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;
    });
    it("When the user clicks the first mutually exclusive option, Then only the first exclusive option should be checked.", () => {
      // When
      $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.false;
      $(MandatoryCheckboxPage.submit()).click();

      // Then
      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("I am an alien");
      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("British\nIrish");
    });
    it("When the user clicks the second mutually exclusive option, Then only the second exclusive option should be checked.", () => {
      // When
      $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).click();
      expect($(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      $(MandatoryCheckboxPage.submit()).click();

      // Then
      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string("I am an alien");
      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("I prefer not to say");
      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("British\nIrish");
    });
  });

  describe("Given the user has clicked a mutually exclusive option", () => {
    it("When the user clicks another mutually exclusive option, Then only the most recently clicked mutually exclusive option should be checked.", () => {
      // Given
      $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.false;

      // When
      $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).click();
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.true;
      $(MandatoryCheckboxPage.submit()).click();

      // Then
      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string("I am an alien");
      expect($(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not clicked any options and the question is mandatory", () => {
    it("When the user clicks the Continue button, Then a validation error message should be displayed.", () => {
      // Given
      expect($(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.false;

      // When
      $(MandatoryCheckboxPage.submit()).click();

      // Then
      expect($(MandatoryCheckboxPage.errorHeader()).getText()).to.contain("There is a problem with your answer");
      expect($(MandatoryCheckboxPage.errorNumber(1)).getText()).to.contain("Enter an answer");
      expect($(MandatoryCheckboxPage.questionErrorPanel()).isExisting()).to.be.true;
    });
  });
});
