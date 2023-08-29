import TextFieldPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-textfield.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-textfield-section-summary.page";
import { click } from "../../../../helpers";

describe("Component: Mutually Exclusive Textfield With Single Checkbox Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
    await browser.pause(100);
    await browser.url("/questionnaire/mutually-exclusive-textfield");
  });

  describe("Given the user has entered a value for the non-exclusive textfield answer", () => {
    it("When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.", async () => {
      // Given
      await $(TextFieldPage.textfield()).setValue("Blue");
      await expect(await $(TextFieldPage.textfield()).getValue()).to.contain("Blue");

      // When
      await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(TextFieldPage.textfield()).getValue()).to.contain("");

      await click(TextFieldPage.submit());

      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).to.not.have.string("Blue");
    });
  });

  describe("Given the user has clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive textfield answer and removes focus, Then only the non-exclusive textfield answer should be answered.", async () => {
      // Given
      await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      await $(TextFieldPage.textfield()).setValue("Blue");

      // Then
      await expect(await $(TextFieldPage.textfield()).getValue()).to.contain("Blue");
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await click(TextFieldPage.submit());

      await expect(await $(SummaryPage.textfieldAnswer()).getText()).to.have.string("Blue");
      await expect(await $(SummaryPage.textfieldAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive textfield answer, Then only the non-exclusive textfield answer should be answered.", async () => {
      // Given
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await $(TextFieldPage.textfield()).setValue("Blue");

      // Then
      await expect(await $(TextFieldPage.textfield()).getValue()).to.contain("Blue");
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await click(TextFieldPage.submit());

      await expect(await $(SummaryPage.textfieldAnswer()).getText()).to.have.string("Blue");
      await expect(await $(SummaryPage.textfieldAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive textfield answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", async () => {
      // Given
      await expect(await $(TextFieldPage.textfield()).getValue()).to.contain("");

      // When
      await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      await click(TextFieldPage.submit());

      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SummaryPage.textfieldExclusiveAnswer()).getText()).to.not.have.string("Blue");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async () => {
      // Given
      await expect(await $(TextFieldPage.textfield()).getValue()).to.contain("");
      await expect(await $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await click(TextFieldPage.submit());

      // Then
      await expect(await $(SummaryPage.textfieldAnswer()).getText()).to.contain("No answer provided");
    });
  });
});
