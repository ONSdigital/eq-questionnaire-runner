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
      await expect(await $(DatePage.dateday()).getValue()).toBe("17");
      await expect(await $(DatePage.datemonth()).getValue()).toBe("3");
      await expect(await $(DatePage.dateyear()).getValue()).toBe("2018");
    });
    it("When then user clicks the first mutually exclusive radio answer, Then only the first mutually exclusive radio should be answered.", async () => {
      // When
      await $(DatePage.dateExclusiveIPreferNotToSay()).click();

      // Then
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).toBe(false);
      await expect(await $(DatePage.dateday()).getValue()).toBe("");
      await expect(await $(DatePage.datemonth()).getValue()).toBe("");
      await expect(await $(DatePage.dateyear()).getValue()).toBe("");

      await click(DatePage.submit());

      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).not.toBe("I have never worked");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).not.toBe("17 March 2018");
    });

    it("When then user clicks the second mutually exclusive radio answer, Then only the second mutually exclusive radio should be answered.", async () => {
      // When
      await $(DatePage.dateExclusiveIHaveNeverWorked()).click();

      // Then
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).toBe(true);
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(DatePage.dateday()).getValue()).toBe("");
      await expect(await $(DatePage.datemonth()).getValue()).toBe("");
      await expect(await $(DatePage.dateyear()).getValue()).toBe("");

      await click(DatePage.submit());

      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).toBe("I have never worked");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).not.toBe("I prefer not to say");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).not.toBe("17 March 2018");
    });
  });

  describe("Given the user has clicked the first mutually exclusive radio answer", () => {
    it("When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.", async () => {
      // Given
      await $(DatePage.dateExclusiveIPreferNotToSay()).click();
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).toBe(false);

      // When
      await $(DatePage.dateday()).setValue("17");
      await $(DatePage.datemonth()).setValue("3");
      await $(DatePage.dateyear()).setValue("2018");

      // Then
      await expect(await $(DatePage.dateday()).getValue()).toBe("17");
      await expect(await $(DatePage.datemonth()).getValue()).toBe("3");
      await expect(await $(DatePage.dateyear()).getValue()).toBe("2018");

      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      await click(DatePage.submit());

      await expect(await $(SummaryPage.dateAnswer()).getText()).toBe("17 March 2018");
      await expect(await $(SummaryPage.dateAnswer()).getText()).not.toBe("I prefer not to say");
      await expect(await $(SummaryPage.dateAnswer()).getText()).not.toBe("I have never worked");
    });
  });

  describe("Given the user has clicked the second mutually exclusive radio answer", () => {
    it("When the user enters a value for the non-exclusive month year date answer and removes focus, Then only the non-exclusive month year date answer should be answered.", async () => {
      // Given
      await $(DatePage.dateExclusiveIHaveNeverWorked()).click();
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).toBe(true);
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // When
      await $(DatePage.dateday()).setValue("17");
      await $(DatePage.datemonth()).setValue("3");
      await $(DatePage.dateyear()).setValue("2018");

      // Then
      await expect(await $(DatePage.dateday()).getValue()).toBe("17");
      await expect(await $(DatePage.datemonth()).getValue()).toBe("3");
      await expect(await $(DatePage.dateyear()).getValue()).toBe("2018");

      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).toBe(false);

      await click(DatePage.submit());

      await expect(await $(SummaryPage.dateAnswer()).getText()).toBe("17 March 2018");
      await expect(await $(SummaryPage.dateAnswer()).getText()).not.toBe("I prefer not to say");
      await expect(await $(SummaryPage.dateAnswer()).getText()).not.toBe("I have never worked");
    });
  });

  describe("Given the user has not clicked the mutually exclusive checkbox answer", () => {
    it("When the user enters a value for the non-exclusive month year date answer, Then only the non-exclusive month year date answer should be answered.", async () => {
      // Given
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).toBe(false);

      // When
      await $(DatePage.dateday()).setValue("17");
      await $(DatePage.datemonth()).setValue("3");
      await $(DatePage.dateyear()).setValue("2018");

      // Then
      await expect(await $(DatePage.dateday()).getValue()).toBe("17");
      await expect(await $(DatePage.datemonth()).getValue()).toBe("3");
      await expect(await $(DatePage.dateyear()).getValue()).toBe("2018");
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).toBe(false);

      await click(DatePage.submit());
      await expect(await $(SummaryPage.dateAnswer()).getText()).toBe("17 March 2018");
      await expect(await $(SummaryPage.dateAnswer()).getText()).not.toBe("I prefer not to say");
      await expect(await $(SummaryPage.dateAnswer()).getText()).not.toBe("I have never worked");
    });
  });

  describe("Given the user has not answered the non-exclusive month year date answer", () => {
    beforeEach(async () => {
      // Given
      await expect(await $(DatePage.dateday()).getValue()).toBe("");
      await expect(await $(DatePage.datemonth()).getValue()).toBe("");
      await expect(await $(DatePage.dateyear()).getValue()).toBe("");
    });
    it("When the user clicks the first mutually exclusive radio answer, Then only the first exclusive radio should be answered.", async () => {
      // When
      await $(DatePage.dateExclusiveIPreferNotToSay()).click();
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).toBe(false);

      // Then
      await click(DatePage.submit());

      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).toBe("I prefer not to say");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).not.toBe("I have never worked");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).not.toBe("17 March 2018");
    });

    it("When the user clicks the second mutually exclusive radio answer, Then only the second exclusive radio should be answered.", async () => {
      // When
      await $(DatePage.dateExclusiveIHaveNeverWorked()).click();
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).toBe(true);
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).toBe(false);

      // Then
      await click(DatePage.submit());

      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).toBe("I have never worked");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).not.toBe("I prefer not to say");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).not.toBe("17 March 2018");
    });
  });

  describe("Given the user has not answered the question and the question is optional", () => {
    it("When the user clicks the Continue button, Then it should display `No answer provided`", async () => {
      // Given
      await expect(await $(DatePage.dateday()).getValue()).toBe("");
      await expect(await $(DatePage.datemonth()).getValue()).toBe("");
      await expect(await $(DatePage.dateyear()).getValue()).toBe("");
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).toBe(false);

      // When
      await click(DatePage.submit());

      // Then
      await expect(await $(SummaryPage.dateAnswer()).getText()).toBe("No answer provided");
    });
  });

  describe("Given the user has clicked a mutually exclusive option", () => {
    it("When the user clicks another mutually exclusive option, Then only the most recently clicked mutually exclusive option should be checked.", async () => {
      // Given
      await $(DatePage.dateExclusiveIPreferNotToSay()).click();
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).toBe(true);
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).toBe(false);

      // When
      await $(DatePage.dateExclusiveIHaveNeverWorked()).click();
      await expect(await $(DatePage.dateExclusiveIPreferNotToSay()).isSelected()).toBe(false);
      await expect(await $(DatePage.dateExclusiveIHaveNeverWorked()).isSelected()).toBe(true);
      await click(DatePage.submit());

      // Then
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).toBe("I have never worked");
      await expect(await $(SummaryPage.dateExclusiveAnswer()).getText()).not.toBe("I prefer not to say");
    });
  });
});
