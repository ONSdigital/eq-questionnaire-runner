import TextFieldPage from "../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-textfield.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-textfield-section-summary.page";

describe("Component: Mutually Exclusive Textfield With Multiple Radio Override", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_mutually_exclusive_multiple.json");
    browser.url("/questionnaire/mutually-exclusive-textfield");
  });

  describe("Given the user has entered a value for the non-exclusive textfield answer", () => {
    beforeEach(() => {
      // Given
      $(TextFieldPage.textfield()).setValue("Blue");
      expect($(TextFieldPage.textfield()).getValue()).to.contain("Blue");
    });
    it("When then user clicks the first mutually exclusive radio answer, Then only the first mutually exclusive radio should be answered.", () => {
      // When
      $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();

      // Then
      expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).to.be.false;
      expect($(TextFieldPage.textfield()).getValue()).to.contain("");

      $(TextFieldPage.submit()).click();

      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.not.have.string("I dont have a favorite colour");
      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.not.have.string("Blue");
    });
    it("When then user clicks the first mutually exclusive radio answer, Then only the first mutually exclusive radio should be answered.", () => {
      // When
      $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).click();

      // Then
      expect($(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).to.be.true;
      expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(TextFieldPage.textfield()).getValue()).to.contain("");

      $(TextFieldPage.submit()).click();

      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.have.string("I dont have a favorite colour");
      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.not.have.string("I prefer not to say");
      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.not.have.string("Blue");
    });
  });

  describe("Given the user has clicked the first mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive textfield answer and removes focus, Then only the non-exclusive textfield answer should be answered.", () => {
      // Given
      $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();
      expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).to.be.false;

      // When
      $(TextFieldPage.textfield()).setValue("Blue");

      // Then
      expect($(TextFieldPage.textfield()).getValue()).to.contain("Blue");
      expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).to.be.false;

      $(TextFieldPage.submit()).click();

      expect($(SummaryPage.textfieldAnswer()).getText()).to.have.string("Blue");
      expect($(SummaryPage.textfieldAnswer()).getText()).to.not.have.string("I prefer not to say");
      expect($(SummaryPage.textfieldAnswer()).getText()).to.not.have.string("I dont have a favorite colour");
    });
  });

  describe("Given the user has clicked the second mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive textfield answer and removes focus, Then only the non-exclusive textfield answer should be answered.", () => {
      // Given
      $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).click();
      expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).to.be.true;

      // When
      $(TextFieldPage.textfield()).setValue("Blue");

      // Then
      expect($(TextFieldPage.textfield()).getValue()).to.contain("Blue");
      expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).to.be.false;

      $(TextFieldPage.submit()).click();

      expect($(SummaryPage.textfieldAnswer()).getText()).to.have.string("Blue");
      expect($(SummaryPage.textfieldAnswer()).getText()).to.not.have.string("I prefer not to say");
      expect($(SummaryPage.textfieldAnswer()).getText()).to.not.have.string("I dont have a favorite colour");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive textfield answer, Then only the non-exclusive textfield answer should be answered.", () => {
      // Given
      expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).to.be.false;

      // When
      $(TextFieldPage.textfield()).setValue("Blue");

      // Then
      expect($(TextFieldPage.textfield()).getValue()).to.contain("Blue");
      expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).to.be.false;

      $(TextFieldPage.submit()).click();

      expect($(SummaryPage.textfieldAnswer()).getText()).to.have.string("Blue");
      expect($(SummaryPage.textfieldAnswer()).getText()).to.not.have.string("I prefer not to say");
      expect($(SummaryPage.textfieldAnswer()).getText()).to.not.have.string("I dont have a favorite colour");
    });
  });

  describe("Given the user has not answered the non-exclusive textfield answer", () => {
    beforeEach(() => {
      // Given
      expect($(TextFieldPage.textfield()).getValue()).to.contain("");
    });
    it("When the user clicks the first mutually exclusive radio answer, Then only the first exclusive radio should be answered.", () => {
      // When
      $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();
      expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).to.be.false;

      // Then
      $(TextFieldPage.submit()).click();

      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.not.have.string("I dont have a favorite colour");
      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.not.have.string("Blue");
    });
    it("When the user clicks the second mutually exclusive radio answer, Then only the second exclusive radio should be answered.", () => {
      // When
      $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).click();
      expect($(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).to.be.true;
      expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // Then
      $(TextFieldPage.submit()).click();

      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.have.string("I dont have a favorite colour");
      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.not.have.string("I prefer not to say");
      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.not.have.string("Blue");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", () => {
      // Given
      expect($(TextFieldPage.textfield()).getValue()).to.contain("");
      expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).to.be.false;

      // When
      $(TextFieldPage.submit()).click();

      // Then
      expect($(SummaryPage.textfieldAnswer()).getText()).to.contain("No answer provided");
    });
  });

  describe("Given the user has clicked a mutually exclusive option", () => {
    it("When the user clicks another mutually exclusive option, Then only the most recently clicked mutually exclusive option should be checked.", () => {
      // Given
      $(TextFieldPage.textfieldExclusiveIPreferNotToSay()).click();
      expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).to.be.false;

      // When
      $(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).click();
      expect($(TextFieldPage.textfieldExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(TextFieldPage.textfieldExclusiveIDontHaveAFavoriteColour()).isSelected()).to.be.true;
      $(TextFieldPage.submit()).click();

      // Then
      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.have.string("I dont have a favorite colour");
      expect($(SummaryPage.textfieldExclusiveAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });
});
