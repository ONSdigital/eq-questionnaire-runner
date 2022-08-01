import DatePage from "../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-date.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-date-section-summary.page";

describe("Component: Mutually Exclusive Day Month Year Date With Multiple Radio Override", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_mutually_exclusive_multiple.json");
    browser.url("/questionnaire/mutually-exclusive-date");
  });

  describe("Given the user has entered a value for the non-exclusive month year date answer", () => {
    beforeEach(() => {
      // Given
      $(DatePage.dateday()).setValue("17");
      $(DatePage.datemonth()).setValue("3");
      $(DatePage.dateyear()).setValue("2018");
      expect($(DatePage.dateday()).getValue()).to.contain("17");
      expect($(DatePage.datemonth()).getValue()).to.contain("3");
      expect($(DatePage.dateyear()).getValue()).to.contain("2018");
    });
    it("When then user clicks the first mutually exclusive radio answer, Then only the first mutually exclusive radio should be answered.", () => {
      // When
      $(DatePage.dateExclusiveIPreferNotToSay()).click();

      // Then
      expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;
      expect($(DatePage.dateday()).getValue()).to.contain("");
      expect($(DatePage.datemonth()).getValue()).to.contain("");
      expect($(DatePage.dateyear()).getValue()).to.contain("");

      $(DatePage.submit()).click();

      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("I have never worked");
      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("17 March 2018");
    });

    it("When then user clicks the second mutually exclusive radio answer, Then only the second mutually exclusive radio should be answered.", () => {
      // When
      $(DatePage.dateExclusiveIHaveNeverWorked()).click();

      // Then
      expect($(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.true;
      expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(DatePage.dateday()).getValue()).to.contain("");
      expect($(DatePage.datemonth()).getValue()).to.contain("");
      expect($(DatePage.dateyear()).getValue()).to.contain("");

      $(DatePage.submit()).click();

      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.have.string("I have never worked");
      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("I prefer not to say");
      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("17 March 2018");
    });
  });

  describe("Given the user has clicked the first mutually exclusive radio answer", () => {
    it("When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.", () => {
      // Given
      $(DatePage.dateExclusiveIPreferNotToSay()).click();
      expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      // When
      $(DatePage.dateday()).setValue("17");
      $(DatePage.datemonth()).setValue("3");
      $(DatePage.dateyear()).setValue("2018");

      // Then
      expect($(DatePage.dateday()).getValue()).to.contain("17");
      expect($(DatePage.datemonth()).getValue()).to.contain("3");
      expect($(DatePage.dateyear()).getValue()).to.contain("2018");

      expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      $(DatePage.submit()).click();

      expect($(SummaryPage.dateAnswer()).getText()).to.have.string("17 March 2018");
      expect($(SummaryPage.dateAnswer()).getText()).to.not.have.string("I prefer not to say");
      expect($(SummaryPage.dateAnswer()).getText()).to.not.have.string("I have never worked");
    });
  });

  describe("Given the user has clicked the second mutually exclusive radio answer", () => {
    it("When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.", () => {
      // Given
      $(DatePage.dateExclusiveIHaveNeverWorked()).click();
      expect($(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.true;
      expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      $(DatePage.dateday()).setValue("17");
      $(DatePage.datemonth()).setValue("3");
      $(DatePage.dateyear()).setValue("2018");

      // Then
      expect($(DatePage.dateday()).getValue()).to.contain("17");
      expect($(DatePage.datemonth()).getValue()).to.contain("3");
      expect($(DatePage.dateyear()).getValue()).to.contain("2018");

      expect($(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      $(DatePage.submit()).click();

      expect($(SummaryPage.dateAnswer()).getText()).to.have.string("17 March 2018");
      expect($(SummaryPage.dateAnswer()).getText()).to.not.have.string("I prefer not to say");
      expect($(SummaryPage.dateAnswer()).getText()).to.not.have.string("I have never worked");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive month year date answer, Then only the non-exclusive month year date answer should be answered.", () => {
      // Given
      expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      // When
      $(DatePage.dateday()).setValue("17");
      $(DatePage.datemonth()).setValue("3");
      $(DatePage.dateyear()).setValue("2018");

      // Then
      expect($(DatePage.dateday()).getValue()).to.contain("17");
      expect($(DatePage.datemonth()).getValue()).to.contain("3");
      expect($(DatePage.dateyear()).getValue()).to.contain("2018");
      expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      $(DatePage.submit()).click();
      expect($(SummaryPage.dateAnswer()).getText()).to.have.string("17 March 2018");
      expect($(SummaryPage.dateAnswer()).getText()).to.not.have.string("I prefer not to say");
      expect($(SummaryPage.dateAnswer()).getText()).to.not.have.string("I have never worked");
    });
  });

  describe("Given the user has not answered the non-exclusive month year date answer", () => {
    beforeEach(() => {
      // Given
      expect($(DatePage.dateday()).getValue()).to.contain("");
      expect($(DatePage.datemonth()).getValue()).to.contain("");
      expect($(DatePage.dateyear()).getValue()).to.contain("");
    });
    it("When the user clicks the first mutually exclusive radio answer, Then only the first exclusive radio should be answered.", () => {
      // When
      $(DatePage.dateExclusiveIPreferNotToSay()).click();
      expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      // Then
      $(DatePage.submit()).click();

      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("I have never worked");
      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("17 March 2018");
    });

    it("When the user clicks the second mutually exclusive radio answer, Then only the second exclusive radio should be answered.", () => {
      // When
      $(DatePage.dateExclusiveIHaveNeverWorked()).click();
      expect($(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.true;
      expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // Then
      $(DatePage.submit()).click();

      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.have.string("I have never worked");
      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("I prefer not to say");
      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("17 March 2018");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", () => {
      // Given
      expect($(DatePage.dateday()).getValue()).to.contain("");
      expect($(DatePage.datemonth()).getValue()).to.contain("");
      expect($(DatePage.dateyear()).getValue()).to.contain("");
      expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      // When
      $(DatePage.submit()).click();

      // Then
      expect($(SummaryPage.dateAnswer()).getText()).to.contain("No answer provided");
    });
  });

  describe("Given the user has clicked a mutually exclusive option", () => {
    it("When the user clicks another mutually exclusive option, Then only the most recently clicked mutually exclusive option should be checked.", () => {
      // Given
      $(DatePage.dateExclusiveIPreferNotToSay()).click();
      expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      expect($(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      // When
      $(DatePage.dateExclusiveIHaveNeverWorked()).click();
      expect($(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      expect($(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.true;
      $(DatePage.submit()).click();

      // Then
      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.have.string("I have never worked");
      expect($(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });
});
