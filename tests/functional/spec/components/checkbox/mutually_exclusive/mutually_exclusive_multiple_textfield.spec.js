import TextFieldPage from "../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-textfield.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-textfield-section-summary.page";
import { click, waitForQuestionnaireToLoad } from "../../../../helpers";

describe("Component: Mutually Exclusive Textfield With Multiple Radio Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive_multiple.json");
    await waitForQuestionnaireToLoad();
    await browser.url("/questionnaire/mutually-exclusive-textfield");
  });

  describe("Given the user has entered a value for the non-exclusive textfield answer", () => {
    beforeEach(async () => {
      // Given
      await $(TextFieldPage.textfield()).setValue("Blue");
      await expect(await $(TextFieldPage.textfield()).getValue()).toBe("Blue");
    });
    it("When then user clicks the first mutually exclusive radio answer, Then only the first mutually exclusive radio should be answered.", async () => {
      // When
      await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await expect(await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).toBe(false);
      await expect(await $(TextFieldPage.textfield()).getValue()).toBe("");

      await click(TextFieldPage.submit());

      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).not.toBe("I dont have a favorite colour");
      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).not.toBe("Blue");
    });
    it("When then user clicks the first mutually exclusive radio answer, Then only the first mutually exclusive radio should be answered.", async () => {
      // When
      await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).click();

      // Then
      await expect(await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).toBe(true);
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(TextFieldPage.textfield()).getValue()).toBe("");

      await click(TextFieldPage.submit());

      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).toBe("I dont have a favorite colour");
      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).not.toBe("I prefer not to say");
      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).not.toBe("Blue");
    });
  });

  describe("Given the user has clicked the first mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive textfield answer and removes focus, Then only the non-exclusive textfield answer should be answered.", async () => {
      // Given
      await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await expect(await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).toBe(false);

      // When
      await $(TextFieldPage.textfield()).setValue("Blue");

      // Then
      await expect(await $(TextFieldPage.textfield()).getValue()).toBe("Blue");
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).toBe(false);

      await click(TextFieldPage.submit());

      await expect(await $(SummaryPage.textfieldAnswer()).getText()).toBe("Blue");
      await expect(await $(SummaryPage.textfieldAnswer()).getText()).not.toBe("I prefer not to say");
      await expect(await $(SummaryPage.textfieldAnswer()).getText()).not.toBe("I dont have a favorite colour");
    });
  });

  describe("Given the user has clicked the second mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive textfield answer and removes focus, Then only the non-exclusive textfield answer should be answered.", async () => {
      // Given
      await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).click();
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).toBe(true);

      // When
      await $(TextFieldPage.textfield()).setValue("Blue");

      // Then
      await expect(await $(TextFieldPage.textfield()).getValue()).toBe("Blue");
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).toBe(false);

      await click(TextFieldPage.submit());

      await expect(await $(SummaryPage.textfieldAnswer()).getText()).toBe("Blue");
      await expect(await $(SummaryPage.textfieldAnswer()).getText()).not.toBe("I prefer not to say");
      await expect(await $(SummaryPage.textfieldAnswer()).getText()).not.toBe("I dont have a favorite colour");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive textfield answer, Then only the non-exclusive textfield answer should be answered.", async () => {
      // Given
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).toBe(false);

      // When
      await $(TextFieldPage.textfield()).setValue("Blue");

      // Then
      await expect(await $(TextFieldPage.textfield()).getValue()).toBe("Blue");
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).toBe(false);

      await click(TextFieldPage.submit());

      await expect(await $(SummaryPage.textfieldAnswer()).getText()).toBe("Blue");
      await expect(await $(SummaryPage.textfieldAnswer()).getText()).not.toBe("I prefer not to say");
      await expect(await $(SummaryPage.textfieldAnswer()).getText()).not.toBe("I dont have a favorite colour");
    });
  });

  describe("Given the user has not answered the non-exclusive textfield answer", () => {
    beforeEach(async () => {
      // Given
      await expect(await $(TextFieldPage.textfield()).getValue()).toBe("");
    });
    it("When the user clicks the first mutually exclusive radio answer, Then only the first exclusive radio should be answered.", async () => {
      // When
      await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await expect(await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).toBe(false);

      // Then
      await click(TextFieldPage.submit());

      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).not.toBe("I dont have a favorite colour");
      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).not.toBe("Blue");
    });
    it("When the user clicks the second mutually exclusive radio answer, Then only the second exclusive radio should be answered.", async () => {
      // When
      await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).click();
      await expect(await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).toBe(true);
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // Then
      await click(TextFieldPage.submit());

      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).toBe("I dont have a favorite colour");
      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).not.toBe("I prefer not to say");
      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).not.toBe("Blue");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async () => {
      // Given
      await expect(await $(TextFieldPage.textfield()).getValue()).toBe("");
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).toBe(false);

      // When
      await click(TextFieldPage.submit());

      // Then
      await expect(await $(SummaryPage.textfieldAnswer()).getText()).toBe("No answer provided");
    });
  });

  describe("Given the user has clicked a mutually exclusive option", () => {
    it("When the user clicks another mutually exclusive option, Then only the most recently clicked mutually exclusive option should be checked.", async () => {
      // Given
      await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await expect(await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).toBe(false);

      // When
      await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).click();
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).toBe(true);
      await click(TextFieldPage.submit());

      // Then
      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).toBe("I dont have a favorite colour");
      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).not.toBe("I prefer not to say");
    });
  });
});
