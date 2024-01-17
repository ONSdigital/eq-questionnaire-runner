import SetMinMax from "../generated_pages/numbers/set-min-max-block.page.js";
import TestMinMax from "../generated_pages/numbers/test-min-max-block.page.js";
import DetailAnswer from "../generated_pages/numbers/detail-answer-block.page";
import SubmitPage from "../generated_pages/numbers/submit.page";
import currencyBlock from "../generated_pages/variants_question/currency-block.page.js";
import firstNumberBlock from "../generated_pages/variants_question/first-number-block.page.js";
import secondNumberBlock from "../generated_pages/variants_question/second-number-block.page.js";
import currencySectionSummary from "../generated_pages/variants_question/currency-section-summary.page.js";
import { click } from "../helpers";

describe("Number validation", () => {
  before(async () => {
    await browser.openQuestionnaire("test_numbers.json");
  });

  describe("Given I am completing the test numbers questionnaire,", () => {
    it("When a minimum value with decimals is used and I enter a value less than the minimum, Then the error message includes the minimum value with the decimals values", async () => {
      await $(SetMinMax.setMinimum()).setValue(-1000.99);
      await $(SetMinMax.setMaximum()).setValue(1000);
      await click(SetMinMax.submit());
      await expect(await $(SetMinMax.errorNumber(1)).getText()).toBe("Enter an answer more than or equal to -1,000.98");
    });

    it("When a maximum value with decimals is used and I enter a value greater than the maximum, Then the error message includes the minimum value with the decimal values", async () => {
      await $(SetMinMax.setMinimum()).setValue(100);
      await $(SetMinMax.setMaximum()).setValue(10000.99);
      await click(SetMinMax.submit());
      await expect(await $(SetMinMax.errorNumber(1)).getText()).toBe("Enter an answer less than or equal to 10,000.98");
    });

    it("When I am on the set minimum and maximum page, Then each field has a label", async () => {
      await expect(await $(SetMinMax.setMinimumLabelDescription()).getText()).toBe("This is a description of the minimum value");
      await expect(await $(SetMinMax.setMaximumLabelDescription()).getText()).toBe("This is a description of the maximum value");
    });

    it("When I enter values outside of the set range, Then the correct error messages are displayed", async () => {
      await $(SetMinMax.setMinimum()).setValue("10");
      await $(SetMinMax.setMaximum()).setValue("1020");
      await click(SetMinMax.submit());

      await $(TestMinMax.testRange()).setValue("9");
      await $(TestMinMax.testRangeExclusive()).setValue("10");
      await $(TestMinMax.testMin()).setValue("-124");
      await $(TestMinMax.testMax()).setValue("12345");
      await $(TestMinMax.testMinExclusive()).setValue("123");
      await $(TestMinMax.testMaxExclusive()).setValue("12345");
      await $(TestMinMax.testPercent()).setValue("101");
      await $(TestMinMax.testDecimal()).setValue("5.4");
      await click(TestMinMax.submit());

      await expect(await $(TestMinMax.errorNumber(1)).getText()).toBe("Enter an answer more than or equal to 10");
      await expect(await $(TestMinMax.errorNumber(2)).getText()).toBe("Enter an answer more than 10");
      await expect(await $(TestMinMax.errorNumber(3)).getText()).toBe("Enter an answer more than or equal to -123");
      await expect(await $(TestMinMax.errorNumber(4)).getText()).toBe("Enter an answer less than or equal to 1,234");
      await expect(await $(TestMinMax.errorNumber(5)).getText()).toBe("Enter an answer more than 123");
      await expect(await $(TestMinMax.errorNumber(6)).getText()).toBe("Enter an answer less than 1,234");
      await expect(await $(TestMinMax.errorNumber(7)).getText()).toBe("Enter an answer less than or equal to 100");
      await expect(await $(TestMinMax.errorNumber(8)).getText()).toBe("Enter an answer more than or equal to £10.00");
    });

    it("When I enter values inside the set range but provide too many decimal places, Then the correct error messages are displayed", async () => {
      await $(TestMinMax.testRange()).setValue("12.344");
      await $(TestMinMax.testRangeExclusive()).setValue("11");
      await $(TestMinMax.testMin()).setValue("123");
      await $(TestMinMax.testMax()).setValue("1019");
      await $(TestMinMax.testMinExclusive()).setValue("124");
      await $(TestMinMax.testMaxExclusive()).setValue("1233");
      await $(TestMinMax.testPercent()).setValue("100");
      await $(TestMinMax.testRange()).setValue("12.123456");
      await $(TestMinMax.testDecimal()).setValue("11.123456");
      await click(TestMinMax.submit());

      await expect(await $(TestMinMax.errorNumber(1)).getText()).toBe("Enter a number rounded to 2 decimal places");
      await expect(await $(TestMinMax.errorNumber(2)).getText()).toBe("Enter a number rounded to 5 decimal places");
    });

    it("When I enter values inside the set range, Then I should be able to submit the survey", async () => {
      await $(TestMinMax.testRange()).setValue("1019");
      await $(TestMinMax.testDecimal()).setValue("11.10000");
      await $(TestMinMax.testPercent()).setValue("99");
      await click(TestMinMax.submit());
      await $(DetailAnswer.other()).click();
      await $(DetailAnswer.otherDetail()).setValue("1019");
      await click(TestMinMax.submit());
      await $(currencyBlock.usDollars()).click();
      await click(currencyBlock.submit());
      await $(firstNumberBlock.firstNumber()).setValue("50");
      await click(firstNumberBlock.submit());
      await $(secondNumberBlock.secondNumber()).setValue("321");
      await click(secondNumberBlock.submit());
      await click(currencySectionSummary.submit());

      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
    });

    it("When I edit and change the maximum value, Then I must re-validate and submit any dependent answers before I can return to the summary", async () => {
      await $(SubmitPage.setMaximumEdit()).click();
      await $(SetMinMax.setMaximum()).setValue("1018");
      await click(SetMinMax.submit());
      await $(TestMinMax.testRange()).setValue("1018");
      await click(TestMinMax.submit());
      await click(DetailAnswer.submit());

      await expect(await $(DetailAnswer.errorNumber(1)).getText()).toBe("Enter an answer less than or equal to 1,018");

      await $(DetailAnswer.otherDetail()).setValue("1001");
      await click(DetailAnswer.submit());
      await click(secondNumberBlock.submit());
      await click(currencySectionSummary.submit());

      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
    });

    it("When I edit and change the minimum value, Then I must re-validate and submit any dependent answers again before I can return to the summary", async () => {
      await $(SubmitPage.setMinimumEdit()).click();
      await $(SetMinMax.setMinimum()).setValue("11");
      await click(SetMinMax.submit());
      await click(TestMinMax.submit());

      await expect(await $(TestMinMax.errorNumber(1)).getText()).toBe("Enter an answer more than 11");

      await $(TestMinMax.testRangeExclusive()).setValue("12");
      await click(TestMinMax.submit());

      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
    });

    it("When a number with more than 3 decimal places has been entered, Then it should be displayed correctly on the summary", async () => {
      await expect(await $(SubmitPage.testDecimal()).getText()).toBe("£11.10000");
    });
  });
});
