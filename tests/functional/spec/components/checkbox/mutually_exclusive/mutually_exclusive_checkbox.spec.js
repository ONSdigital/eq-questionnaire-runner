import MandatoryCheckboxPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-checkbox.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-checkbox-section-summary.page";
import { click } from "../../../../helpers";

describe("Component: Mutually Exclusive Checkbox With Single Checkbox Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
  });

  describe("Given the user has clicked multiple non-exclusive options", () => {
    it("When then user clicks the mutually exclusive option, Then only the mutually exclusive option should be checked.", async () => {
      // Given
      await $(MandatoryCheckboxPage.checkboxBritish()).click();
      await $(MandatoryCheckboxPage.checkboxIrish()).click();
      await $(MandatoryCheckboxPage.checkboxOther()).click();
      await $(MandatoryCheckboxPage.checkboxOtherDetail()).setValue("The other option");

      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxOtherDetail()).getValue()).to.contain("The other option");

      // When
      await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxOtherDetail()).getValue()).to.contain("");

      await click(MandatoryCheckboxPage.submit());

      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("British\nIrish");
    });
  });

  describe('Given the user has clicked the mutually exclusive "other" option', () => {
    it("When the user returns to the question, Then the mutually exclusive other option should remain checked.", async () => {
      // Given
      await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      await click(MandatoryCheckboxPage.submit());

      // When
      await $(SummaryPage.previous()).click();

      // Then
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;
    });
  });

  describe("Given the user has clicked the mutually exclusive option", () => {
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

      await click(MandatoryCheckboxPage.submit());

      await expect(await $(SummaryPage.checkboxAnswer()).getText()).to.have.string("British\nIrish");
      await expect(await $(SummaryPage.checkboxAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive option", () => {
    it("When the user clicks multiple non-exclusive options, Then only the non-exclusive options should be checked.", async () => {
      // Given
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await $(MandatoryCheckboxPage.checkboxBritish()).click();
      await $(MandatoryCheckboxPage.checkboxIrish()).click();

      // Then
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.true;
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.true;

      await click(MandatoryCheckboxPage.submit());

      await expect(await $(SummaryPage.checkboxAnswer()).getText()).to.have.string("British\nIrish");
      await expect(await $(SummaryPage.checkboxAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not clicked any of the non-exclusive options", () => {
    it("When the user clicks the mutually exclusive option, Then only the exclusive option should be checked.", async () => {
      // Given
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;

      // When
      await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await click(MandatoryCheckboxPage.submit());

      // Then
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).to.not.have.string("British\nIrish");
    });
  });

  describe("Given the user has not clicked any options and the question is mandatory", () => {
    it("When the user clicks the Continue button, Then a validation error message should be displayed.", async () => {
      // Given
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxOther()).isSelected()).to.be.false;
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await click(MandatoryCheckboxPage.submit());

      // Then
      await expect(await $(MandatoryCheckboxPage.errorHeader()).getText()).to.contain("There is a problem with your answer");
      await expect(await $(MandatoryCheckboxPage.errorNumber(1)).getText()).to.contain("Select at least one answer");
      await expect(await $(MandatoryCheckboxPage.questionErrorPanel()).isExisting()).to.be.true;
    });
  });
});
