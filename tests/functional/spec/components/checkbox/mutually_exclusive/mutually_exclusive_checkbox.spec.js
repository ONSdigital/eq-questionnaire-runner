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

      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).toBe(true);
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).toBe(true);
      await expect(await $(MandatoryCheckboxPage.checkboxOther()).isSelected()).toBe(true);
      await expect(await $(MandatoryCheckboxPage.checkboxOtherDetail()).getValue()).toBe("The other option");

      // When
      await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).toBe(true);

      // Then
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).toBe(false);
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).toBe(false);
      await expect(await $(MandatoryCheckboxPage.checkboxOther()).isSelected()).toBe(false);
      await expect(await $(MandatoryCheckboxPage.checkboxOtherDetail()).getValue()).toBe("");

      await click(MandatoryCheckboxPage.submit());

      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).not.toBe("British\nIrish");
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
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).toBe(true);
    });
  });

  describe("Given the user has clicked the mutually exclusive option", () => {
    it("When the user clicks the non-exclusive options, Then only the non-exclusive options should be checked.", async () => {
      // Given
      await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).toBe(true);

      // When
      await $(MandatoryCheckboxPage.checkboxBritish()).click();
      await $(MandatoryCheckboxPage.checkboxIrish()).click();

      // Then
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).toBe(true);
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).toBe(true);

      await click(MandatoryCheckboxPage.submit());

      await expect(await $(SummaryPage.checkboxAnswer()).getText()).toBe("British\nIrish");
      await expect(await $(SummaryPage.checkboxAnswer()).getText()).not.toBe("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive option", () => {
    it("When the user clicks multiple non-exclusive options, Then only the non-exclusive options should be checked.", async () => {
      // Given
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // When
      await $(MandatoryCheckboxPage.checkboxBritish()).click();
      await $(MandatoryCheckboxPage.checkboxIrish()).click();

      // Then
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).toBe(true);
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).toBe(true);

      await click(MandatoryCheckboxPage.submit());

      await expect(await $(SummaryPage.checkboxAnswer()).getText()).toBe("British\nIrish");
      await expect(await $(SummaryPage.checkboxAnswer()).getText()).not.toBe("I prefer not to say");
    });
  });

  describe("Given the user has not clicked any of the non-exclusive options", () => {
    it("When the user clicks the mutually exclusive option, Then only the exclusive option should be checked.", async () => {
      // Given
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).toBe(false);
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).toBe(false);
      await expect(await $(MandatoryCheckboxPage.checkboxOther()).isSelected()).toBe(false);

      // When
      await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).click();
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await click(MandatoryCheckboxPage.submit());

      // Then
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.checkboxExclusiveAnswer()).getText()).not.toBe("British\nIrish");
    });
  });

  describe("Given the user has not clicked any options and the question is mandatory", () => {
    it("When the user clicks the Continue button, Then a validation error message should be displayed.", async () => {
      // Given
      await expect(await $(MandatoryCheckboxPage.checkboxBritish()).isSelected()).toBe(false);
      await expect(await $(MandatoryCheckboxPage.checkboxIrish()).isSelected()).toBe(false);
      await expect(await $(MandatoryCheckboxPage.checkboxOther()).isSelected()).toBe(false);
      await expect(await $(MandatoryCheckboxPage.checkboxExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // When
      await click(MandatoryCheckboxPage.submit());

      // Then
      await expect(await $(MandatoryCheckboxPage.errorHeader()).getText()).toBe("There is a problem with your answer");
      await expect(await $(MandatoryCheckboxPage.errorNumber(1)).getText()).toContain("Select at least one answer");
      await expect(await $(MandatoryCheckboxPage.questionErrorPanel()).isExisting()).toBe(true);
    });
  });
});
