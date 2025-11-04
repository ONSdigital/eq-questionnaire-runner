import NumberPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-number.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-number-section-summary.page";
import { click, waitForQuestionnaireToLoad } from "../../../../helpers";

describe("Component: Mutually Exclusive Number With Single Checkbox Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
    await waitForQuestionnaireToLoad();
    await browser.url("/questionnaire/mutually-exclusive-number");
  });

  describe("Given the user has entered a value for the non-exclusive number answer", () => {
    it("When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.", async () => {
      // Given
      await $(NumberPage.number()).setValue("123");
      await expect(await $(NumberPage.number()).getValue()).toBe("123");

      // When
      await $(NumberPage.numberExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await expect(await $(NumberPage.number()).getValue()).toBe("");

      await click(NumberPage.submit());

      await expect(await $(SummaryPage.numberExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.numberExclusiveAnswer()).getText()).not.toBe("123");
    });
  });

  describe("Given the user has clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive number answer and removes focus, Then only the non-exclusive number answer should be answered.", async () => {
      // Given
      await $(NumberPage.numberExclusiveIPreferNotToSay()).click();
      await expect(await $(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).toBe(true);

      // When
      await $(NumberPage.number()).setValue("123");

      // Then
      await expect(await $(NumberPage.number()).getValue()).toBe("123");
      await expect(await $(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      await click(NumberPage.submit());

      await expect(await $(SummaryPage.numberAnswer()).getText()).toBe("123");
      await expect(await $(SummaryPage.numberAnswer()).getText()).not.toBe("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive number answer, Then only the non-exclusive number answer should be answered.", async () => {
      // Given
      await expect(await $(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // When
      await $(NumberPage.number()).setValue("123");

      // Then
      await expect(await $(NumberPage.number()).getValue()).toBe("123");
      await expect(await $(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      await click(NumberPage.submit());

      await expect(await $(SummaryPage.numberAnswer()).getText()).toBe("123");
      await expect(await $(SummaryPage.numberAnswer()).getText()).not.toBe("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive number answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", async () => {
      // Given
      await expect(await $(NumberPage.number()).getValue()).toBe("");

      // When
      await $(NumberPage.numberExclusiveIPreferNotToSay()).click();
      await expect(await $(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).toBe(true);

      // Then
      await click(NumberPage.submit());

      await expect(await $(SummaryPage.numberExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.numberExclusiveAnswer()).getText()).not.toBe("123");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async () => {
      // Given
      await expect(await $(NumberPage.number()).getValue()).toBe("");
      await expect(await $(NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // When
      await click(NumberPage.submit());

      // Then
      await expect(await $(SummaryPage.numberAnswer()).getText()).toBe("No answer provided");
    });
  });
});
