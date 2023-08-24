import TextFieldPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-textarea.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-textarea-section-summary.page";
import { click } from "../../../../helpers";

describe("Component: Mutually Exclusive TextArea With Single Checkbox Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
    await browser.pause(100);
    await browser.url("/questionnaire/mutually-exclusive-textarea");
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive textarea answer, Then only the non-exclusive textarea answer should be answered.", async () => {
      // Given
      await expect(await $(TextFieldPage.textareaExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await $(TextFieldPage.textarea()).setValue("Blue");

      // Then
      await expect(await $(TextFieldPage.textarea()).getValue()).to.contain("Blue");
      await expect(await $(TextFieldPage.textareaExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await click(TextFieldPage.submit());

      await expect(await $(SummaryPage.textareaAnswer()).getText()).to.have.string("Blue");
      await expect(await $(SummaryPage.textareaAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive textarea answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", async () => {
      // Given
      await expect(await $(TextFieldPage.textarea()).getValue()).to.contain("");

      // When
      await $(TextFieldPage.textareaExclusiveIPreferNotToSay()).click();
      await expect(await $(TextFieldPage.textareaExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      await click(TextFieldPage.submit());

      await expect(await $(SummaryPage.textareaExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SummaryPage.textareaExclusiveAnswer()).getText()).to.not.have.string("Blue");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async () => {
      // Given
      await expect(await $(TextFieldPage.textarea()).getValue()).to.contain("");
      await expect(await $(TextFieldPage.textareaExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await click(TextFieldPage.submit());

      // Then
      await expect(await $(SummaryPage.textareaAnswer()).getText()).to.contain("No answer provided");
    });
  });
});
