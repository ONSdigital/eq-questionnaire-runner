import MandatoryCheckboxPage from "../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-checkbox.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-checkbox-section-summary.page";

describe("Component: Mutually Exclusive Checkbox With Multiple Radio Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive_multiple.json");
  });

  describe("Given the user has clicked multiple non-exclusive options", () => {
    beforeEach(async () => {
      // Given
      await $(MandatoryCheckboxPage.checkboxBritish()).click();
      await $(MandatoryCheckboxPage.checkboxIrish()).click();
      await $(MandatoryCheckboxPage.checkboxOther()).click();
      await $(MandatoryCheckboxPage.checkboxOtherDetail()).setValue("The other option");

      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxOtherDetail()).getValue()).to.contain("The other option");
    });

    it("When then user clicks the first mutually exclusive option, Then only the first mutually exclusive option should be checked.", async () => {
      // When
      await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.false;

      // Then
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxOtherDetail()).getValue()).to.contain("");

      await $(MandatoryCheckboxPage.submit()).click();

      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("British\nIrish");
    });

    it("When then user clicks the second mutually exclusive option, Then only the second mutually exclusive option should be checked.", async () => {
      // When
      await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).click();
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // Then
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxOtherDetail()).getValue()).to.contain("");

      await $(MandatoryCheckboxPage.submit()).click();

      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string("I am an alien");
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("British\nIrish");
    });
  });

  describe("Given the user has clicked the first mutually exclusive option", () => {
    it("When the user returns to the question, Then the mutually exclusive option should remain checked.", async () => {
      // Given
      await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      await $(MandatoryCheckboxPage.submit()).click();

      // When
      await $(SummaryPage.previous()).click();

      // Then
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;
    });
  });

  describe("Given the user has clicked the second mutually exclusive option", () => {
    it("When the user returns to the question, Then the mutually exclusive option should remain checked.", async () => {
      // Given
      await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).click();
      await $(MandatoryCheckboxPage.submit()).click();

      // When
      await $(SummaryPage.previous()).click();

      // Then
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.true;
    });
  });

  describe("Given the user has clicked the first mutually exclusive option", () => {
    it("When the user clicks the non-exclusive options, Then only the non-exclusive options should be checked.", async () => {
      // Given
      await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      await $(MandatoryCheckboxPage.checkboxBritish()).click();
      await $(MandatoryCheckboxPage.checkboxIrish()).click();

      // Then
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.true;

      await $(MandatoryCheckboxPage.submit()).click();

      await expect(await $(SummaryPage.checkboxAnswer()).getText()).to.have.string("British\nIrish");
      await expect(await $(SummaryPage.checkboxAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has clicked the second mutually exclusive option", () => {
    it("When the user clicks the non-exclusive options, Then only the non-exclusive options should be checked.", async () => {
      // Given
      await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).click();
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.true;

      // When
      await $(MandatoryCheckboxPage.checkboxBritish()).click();
      await $(MandatoryCheckboxPage.checkboxIrish()).click();

      // Then
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.true;

      await $(MandatoryCheckboxPage.submit()).click();

      await expect(await $(SummaryPage.checkboxAnswer()).getText()).to.have.string("British\nIrish");
      await expect(await $(SummaryPage.checkboxAnswer()).getText()).to.not.have.string("I am an alien");
    });
  });

  describe("Given the user has not clicked a mutually exclusive option", () => {
    it("When the user clicks multiple non-exclusive options, Then only the non-exclusive options should be checked.", async () => {
      // Given
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.false;

      // When
      await $(MandatoryCheckboxPage.checkboxBritish()).click();
      await $(MandatoryCheckboxPage.checkboxIrish()).click();

      // Then
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.true;

      await $(MandatoryCheckboxPage.submit()).click();

      await expect(await $(SummaryPage.checkboxAnswer()).getText()).to.have.string("British\nIrish");
      await expect(await $(SummaryPage.checkboxAnswer()).getText()).to.not.have.string("I prefer not to say");
      await expect(await $(SummaryPage.checkboxAnswer()).getText()).to.not.have.string("I am an alien");
    });
  });

  describe("Given the user has not clicked any of the non-exclusive options", () => {
    beforeEach(async () => {
      // Given
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;
    });
    it("When the user clicks the first mutually exclusive option, Then only the first exclusive option should be checked.", async () => {
      // When
      await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.false;
      await $(MandatoryCheckboxPage.submit()).click();

      // Then
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("I am an alien");
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("British\nIrish");
    });
    it("When the user clicks the second mutually exclusive option, Then only the second exclusive option should be checked.", async () => {
      // When
      await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).click();
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      await $(MandatoryCheckboxPage.submit()).click();

      // Then
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string("I am an alien");
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("I prefer not to say");
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("British\nIrish");
    });
  });

  describe("Given the user has clicked a mutually exclusive option", () => {
    it("When the user clicks another mutually exclusive option, Then only the most recently clicked mutually exclusive option should be checked.", async () => {
      // Given
      await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.false;

      // When
      await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).click();
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.true;
      await $(MandatoryCheckboxPage.submit()).click();

      // Then
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string("I am an alien");
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not clicked any options and the question is mandatory", () => {
    it("When the user clicks the Continue button, Then a validation error message should be displayed.", async () => {
      // Given
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIAmAnAlien()).isSelected()).to.be.false;

      // When
      await $(MandatoryCheckboxPage.submit()).click();

      // Then
      await expect(await $(MandatoryCheckboxPage.errorHeader()).getText()).to.contain("There is a problem with your answer");
      await expect(await $(MandatoryCheckboxPage.errorNumber(1)).getText()).to.contain("Select at least one answer");
      await expect(await $(MandatoryCheckboxPage.questionErrorPanel()).isExisting()).to.be.true;
    });
  });
});
