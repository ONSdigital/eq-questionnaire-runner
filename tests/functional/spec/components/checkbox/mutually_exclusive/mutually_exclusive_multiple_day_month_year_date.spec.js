import DatePage from "../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-date.page";
import SummaryPage from "../../../../generated_pages/mutually_exclusive_multiple/mutually-exclusive-date-section-summary.page";
import { click } from "../../../../helpers";

describe("Component: Mutually Exclusive Day Month Year Date With Multiple Radio Override", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_mutually_exclusive_multiple.json");
    await browser.pause(100);
    await browser.url("/questionnaire/mutually-exclusive-date");
  });
  describe("Given the user has entered a value for the non-exclusive month year date answer", () => {
    beforeEach(async () => {
      // Given
      await $(DatePage.dateday()).setValue("17");
      await $(DatePage.datemonth()).setValue("3");
      await $(DatePage.dateyear()).setValue("2018");
      await expect(await $(DatePage.dateday()).getValue()).to.contain("17");
      await expect(await $(DatePage.datemonth()).getValue()).to.contain("3");
      await expect(await $(DatePage.dateyear()).getValue()).to.contain("2018");
    });
    it("When then user clicks the first mutually exclusive radio answer, Then only the first mutually exclusive radio should be answered.", async () => {
      // When
      await $(DatePage.dateExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;
      await expect(await $(DatePage.dateday()).getValue()).to.contain("");
      await expect(await $(DatePage.datemonth()).getValue()).to.contain("");
      await expect(await $(DatePage.dateyear()).getValue()).to.contain("");

      await click(DatePage.submit());

      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("I have never worked");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("17 March 2018");
    });

    it("When then user clicks the second mutually exclusive radio answer, Then only the second mutually exclusive radio should be answered.", async () => {
      // When
      await $(DatePage.dateExclusiveIHaveNeverWorked()).click();

      // Then
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.true;
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      await expect(await $(DatePage.dateday()).getValue()).to.contain("");
      await expect(await $(DatePage.datemonth()).getValue()).to.contain("");
      await expect(await $(DatePage.dateyear()).getValue()).to.contain("");

      await click(DatePage.submit());

      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.have.string("I have never worked");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("I prefer not to say");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("17 March 2018");
    });
  });

  describe("Given the user has clicked the first mutually exclusive radio answer", () => {
    it("When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.", async () => {
      // Given
      await $(DatePage.dateExclusiveIPreferNotToSay()).click();
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      // When
      await $(DatePage.dateday()).setValue("17");
      await $(DatePage.datemonth()).setValue("3");
      await $(DatePage.dateyear()).setValue("2018");

      // Then
      await expect(await $(DatePage.dateday()).getValue()).to.contain("17");
      await expect(await $(DatePage.datemonth()).getValue()).to.contain("3");
      await expect(await $(DatePage.dateyear()).getValue()).to.contain("2018");

      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      await click(DatePage.submit());

      await expect(await $(SummaryPage.dateAnswer()).getText()).to.have.string("17 March 2018");
      await expect(await $(SummaryPage.dateAnswer()).getText()).to.not.have.string("I prefer not to say");
      await expect(await $(SummaryPage.dateAnswer()).getText()).to.not.have.string("I have never worked");
    });
  });

  describe("Given the user has clicked the second mutually exclusive radio answer", () => {
    it("When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.", async () => {
      // Given
      await $(DatePage.dateExclusiveIHaveNeverWorked()).click();
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.true;
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // When
      await $(DatePage.dateday()).setValue("17");
      await $(DatePage.datemonth()).setValue("3");
      await $(DatePage.dateyear()).setValue("2018");

      // Then
      await expect(await $(DatePage.dateday()).getValue()).to.contain("17");
      await expect(await $(DatePage.datemonth()).getValue()).to.contain("3");
      await expect(await $(DatePage.dateyear()).getValue()).to.contain("2018");

      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      await click(DatePage.submit());

      await expect(await $(SummaryPage.dateAnswer()).getText()).to.have.string("17 March 2018");
      await expect(await $(SummaryPage.dateAnswer()).getText()).to.not.have.string("I prefer not to say");
      await expect(await $(SummaryPage.dateAnswer()).getText()).to.not.have.string("I have never worked");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive month year date answer, Then only the non-exclusive month year date answer should be answered.", async () => {
      // Given
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      // When
      await $(DatePage.dateday()).setValue("17");
      await $(DatePage.datemonth()).setValue("3");
      await $(DatePage.dateyear()).setValue("2018");

      // Then
      await expect(await $(DatePage.dateday()).getValue()).to.contain("17");
      await expect(await $(DatePage.datemonth()).getValue()).to.contain("3");
      await expect(await $(DatePage.dateyear()).getValue()).to.contain("2018");
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      await click(DatePage.submit());
      await expect(await $(SummaryPage.dateAnswer()).getText()).to.have.string("17 March 2018");
      await expect(await $(SummaryPage.dateAnswer()).getText()).to.not.have.string("I prefer not to say");
      await expect(await $(SummaryPage.dateAnswer()).getText()).to.not.have.string("I have never worked");
    });
  });

  describe("Given the user has not answered the non-exclusive month year date answer", () => {
    beforeEach(async () => {
      // Given
      await expect(await $(DatePage.dateday()).getValue()).to.contain("");
      await expect(await $(DatePage.datemonth()).getValue()).to.contain("");
      await expect(await $(DatePage.dateyear()).getValue()).to.contain("");
    });
    it("When the user clicks the first mutually exclusive radio answer, Then only the first exclusive radio should be answered.", async () => {
      // When
      await $(DatePage.dateExclusiveIPreferNotToSay()).click();
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      // Then
      await click(DatePage.submit());

      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.have.string("I prefer not to say");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("I have never worked");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("17 March 2018");
    });

    it("When the user clicks the second mutually exclusive radio answer, Then only the second exclusive radio should be answered.", async () => {
      // When
      await $(DatePage.dateExclusiveIHaveNeverWorked()).click();
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.true;
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;

      // Then
      await click(DatePage.submit());

      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.have.string("I have never worked");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("I prefer not to say");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("17 March 2018");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async () => {
      // Given
      await expect(await $(DatePage.dateday()).getValue()).to.contain("");
      await expect(await $(DatePage.datemonth()).getValue()).to.contain("");
      await expect(await $(DatePage.dateyear()).getValue()).to.contain("");
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      // When
      await click(DatePage.submit());

      // Then
      await expect(await $(SummaryPage.dateAnswer()).getText()).to.contain("No answer provided");
    });
  });

  describe("Given the user has clicked a mutually exclusive option", () => {
    it("When the user clicks another mutually exclusive option, Then only the most recently clicked mutually exclusive option should be checked.", async () => {
      // Given
      await $(DatePage.dateExclusiveIPreferNotToSay()).click();
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.true;
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.false;

      // When
      await $(DatePage.dateExclusiveIHaveNeverWorked()).click();
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).to.be.false;
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).to.be.true;
      await click(DatePage.submit());

      // Then
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.have.string("I have never worked");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).to.not.have.string("I prefer not to say");
    });
  });
});
