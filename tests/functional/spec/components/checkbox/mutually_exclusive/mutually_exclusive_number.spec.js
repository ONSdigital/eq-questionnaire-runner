import NumberPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-number.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive/mutually-exclusive-number-section-summary.page";

describe("Component: Mutually Exclusive Number With Single Checkbox Override", () => {
  beforeEach(async ()=> {
    await browser.openQuestionnaire("test_mutually_exclusive.json");
    browser.url("/questionnaire/mutually-exclusive-number");
  });

  describe("Given the user has entered a value for the non-exclusive number answer", () => {
    it("When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.", async ()=> {
      // Given
      await $(await NumberPage.number()).setValue("123");
      await expect(await $(await NumberPage.number()).getValue()).to.contain("123");

      // When
      await $(await NumberPage.numberExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(await NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(await NumberPage.number()).getValue()).to.contain("");

      await $(await NumberPage.submit()).click();

      await expect(await $(await SummaryPage.numberExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(await SummaryPage.numberExclusiveAnswer()).getText()).to.not.have.string("123");
    });
  });

  describe("Given the user has clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive number answer and removes focus, Then only the non-exclusive number answer should be answered.", async ()=> {
      // Given
      await $(await NumberPage.numberExclusiveIPreferNotToSay()).click();
      await expect(await $(await NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // When
      await $(await NumberPage.number()).setValue("123");

      // Then
      await expect(await $(await NumberPage.number()).getValue()).to.contain("123");
      await expect(await $(await NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await $(await NumberPage.submit()).click();

      await expect(await $(await SummaryPage.numberAnswer()).getText()).to.have.string("123");
      await expect(await $(await SummaryPage.numberAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive number answer, Then only the non-exclusive number answer should be answered.", async ()=> {
      // Given
      await expect(await $(await NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await $(await NumberPage.number()).setValue("123");

      // Then
      await expect(await $(await NumberPage.number()).getValue()).to.contain("123");
      await expect(await $(await NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await $(await NumberPage.submit()).click();

      await expect(await $(await SummaryPage.numberAnswer()).getText()).to.have.string("123");
      await expect(await $(await SummaryPage.numberAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });

  describe("Given the user has not answered the non-exclusive number answer", () => {
    it("When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.", async ()=> {
      // Given
      await expect(await $(await NumberPage.number()).getValue()).to.contain("");

      // When
      await $(await NumberPage.numberExclusiveIPreferNotToSay()).click();
      await expect(await $(await NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.true;

      // Then
      await $(await NumberPage.submit()).click();

      await expect(await $(await SummaryPage.numberExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(await SummaryPage.numberExclusiveAnswer()).getText()).to.not.have.string("123");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async ()=> {
      // Given
      await expect(await $(await NumberPage.number()).getValue()).to.contain("");
      await expect(await $(await NumberPage.numberExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await $(await NumberPage.submit()).click();

      // Then
      await expect(await $(await SummaryPage.numberAnswer()).getText()).to.contain("No answer provided");
    });
  });
});
