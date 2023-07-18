import SetMinMax from "../generated_pages/numbers/set-min-max-block.page.js";
import TestMinMax from "../generated_pages/numbers/test-min-max-block.page.js";
import DetailAnswer from "../generated_pages/numbers/detail-answer-block.page";
import SubmitPage from "../generated_pages/numbers/submit.page";
import currencyBlock from "../generated_pages/variants_question/currency-block.page.js";
import firstNumberBlock from "../generated_pages/variants_question/first-number-block.page.js";
import secondNumberBlock from "../generated_pages/variants_question/second-number-block.page.js";
import currencySectionSummary from "../generated_pages/variants_question/currency-section-summary.page.js";

describe("Number validation", () => {
  before(async () => {
    await browser.openQuestionnaire("test_numbers.json");
  });
  describe("Given I am completing the test numbers questionnaire,", () => {
    it("When I am on the set minimum and maximum page, Then each field has a label", async () => {
      await expect(await $(SetMinMax.setMinimumLabelDescription()).getText()).to.contain("This is a description of the minimum value");
      await expect(await $(SetMinMax.setMaximumLabelDescription()).getText()).to.contain("This is a description of the maximum value");
    });

    it("When I enter values outside of the set range, Then the correct error messages are displayed", async () => {
      await $(SetMinMax.setMinimum()).setValue("10");
      await $(SetMinMax.setMaximum()).setValue("1020");
      await $(SetMinMax.submit()).click();

      await $(TestMinMax.testRange()).setValue("9");
      await $(TestMinMax.testRangeExclusive()).setValue("10");
      await $(TestMinMax.testMin()).setValue("-124");
      await $(TestMinMax.testMax()).setValue("12345");
      await $(TestMinMax.testMinExclusive()).setValue("123");
      await $(TestMinMax.testMaxExclusive()).setValue("12345");
      await $(TestMinMax.testPercent()).setValue("101");
      await $(TestMinMax.testDecimal()).setValue("5.4");
      await $(TestMinMax.submit()).click();

      await expect(await $(TestMinMax.errorNumber(1)).getText()).to.contain("Enter an answer more than or equal to 10");
      await expect(await $(TestMinMax.errorNumber(2)).getText()).to.contain("Enter an answer more than 10");
      await expect(await $(TestMinMax.errorNumber(3)).getText()).to.contain("Enter an answer more than or equal to -123");
      await expect(await $(TestMinMax.errorNumber(4)).getText()).to.contain("Enter an answer less than or equal to 1,234");
      await expect(await $(TestMinMax.errorNumber(5)).getText()).to.contain("Enter an answer more than 123");
      await expect(await $(TestMinMax.errorNumber(6)).getText()).to.contain("Enter an answer less than 1,234");
      await expect(await $(TestMinMax.errorNumber(7)).getText()).to.contain("Enter an answer less than or equal to 100");
      await expect(await $(TestMinMax.errorNumber(8)).getText()).to.contain("Enter an answer more than or equal to £10.00");
    });

    it("When I enter values inside the set range but provide too many decimal places, Then the correct error messages are displayed", async () => {
      await $(TestMinMax.testRange()).setValue("1020");
      await $(TestMinMax.testRangeExclusive()).setValue("11");
      await $(TestMinMax.testMin()).setValue("123");
      await $(TestMinMax.testMax()).setValue("1019");
      await $(TestMinMax.testMinExclusive()).setValue("124");
      await $(TestMinMax.testMaxExclusive()).setValue("1233");
      await $(TestMinMax.testPercent()).setValue("100");
      await $(TestMinMax.testRange()).setValue("12.344");
      await $(TestMinMax.testDecimal()).setValue("11.234");
      await $(TestMinMax.submit()).click();

      await expect(await $(TestMinMax.errorNumber(1)).getText()).to.contain("Enter a number rounded to 2 decimal places");
      await expect(await $(TestMinMax.errorNumber(2)).getText()).to.contain("Enter a number rounded to 2 decimal places");
    });

    it("When I enter values inside the set range, Then I should be able to submit the survey", async () => {
      await $(TestMinMax.testRange()).setValue("12");
      await $(TestMinMax.testDecimal()).setValue("11.23");
      await $(TestMinMax.submit()).click();
      await $(DetailAnswer.other()).click();
      await $(DetailAnswer.otherDetail()).setValue("1020");
      await $(DetailAnswer.submit()).click();
      await $(currencyBlock.usDollars()).click();
      await $(currencyBlock.submit()).click();
      await $(firstNumberBlock.firstNumber()).setValue(50);
      await $(firstNumberBlock.submit()).click();
      await $(secondNumberBlock.secondNumber()).setValue(321);
      await $(secondNumberBlock.submit()).click();
      await $(currencySectionSummary.submit()).click();

      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("When I edit and change the maximum value, Then I must re-validate and submit any dependent answers before I can return to the summary", async () => {
      await $(SubmitPage.setMaximumEdit()).click();
      await $(SetMinMax.setMaximum()).setValue("1019");
      await $(SetMinMax.submit()).click();
      await $(TestMinMax.submit()).click();
      await $(DetailAnswer.submit()).click();

      await expect(await $(DetailAnswer.errorNumber(1)).getText()).to.contain("Enter an answer less than or equal to 1,019");

      await $(DetailAnswer.otherDetail()).setValue("1019");
      await $(DetailAnswer.submit()).click();
      await $(secondNumberBlock.submit()).click();
      await $(currencySectionSummary.submit()).click();

      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("When I edit and change the minimum value, Then I must re-validate and submit any dependent answers again before I can return to the summary", async () => {
      await $(SubmitPage.setMinimumEdit()).click();
      await $(SetMinMax.setMinimum()).setValue("11");
      await $(SetMinMax.submit()).click();
      await $(TestMinMax.submit()).click();

      await expect(await $(TestMinMax.errorNumber(1)).getText()).to.contain("Enter an answer more than 11");

      await $(TestMinMax.testRangeExclusive()).setValue("12");
      await $(TestMinMax.submit()).click();

      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });
});
