import SetMinMax from "../generated_pages/numbers/set-min-max-block.page.js";
import TestMinMax from "../generated_pages/numbers/test-min-max-block.page.js";
import DetailAnswer from "../generated_pages/numbers/detail-answer-block.page";
import SubmitPage from "../generated_pages/numbers/submit.page";

describe("Number validation", () => {
  before(() => {
    browser.openQuestionnaire("test_numbers.json");
  });
  describe("Given I am completing the test numbers questionnaire,", () => {
    it("When I am on the set minimum and maximum page, Then each field has a label", () => {
      expect($(SetMinMax.setMinimumLabelDescription()).getText()).to.contain("This is a description of the minimum value");
      expect($(SetMinMax.setMaximumLabelDescription()).getText()).to.contain("This is a description of the maximum value");
    });

    it("When I enter values outside of the set range, Then the correct error messages are displayed", () => {
      $(SetMinMax.setMinimum()).setValue("10");
      $(SetMinMax.setMaximum()).setValue("1020");
      $(SetMinMax.submit()).click();

      $(TestMinMax.testRange()).setValue("9");
      $(TestMinMax.testRangeExclusive()).setValue("10");
      $(TestMinMax.testMin()).setValue("0");
      $(TestMinMax.testMax()).setValue("12345");
      $(TestMinMax.testMinExclusive()).setValue("123");
      $(TestMinMax.testMaxExclusive()).setValue("12345");
      $(TestMinMax.testPercent()).setValue("101");
      $(TestMinMax.testDecimal()).setValue("5.4");
      $(TestMinMax.submit()).click();

      expect($(TestMinMax.errorNumber(1)).getText()).to.contain("Enter an answer more than or equal to 10");
      expect($(TestMinMax.errorNumber(2)).getText()).to.contain("Enter an answer more than 10");
      expect($(TestMinMax.errorNumber(3)).getText()).to.contain("Enter an answer more than or equal to 123");
      expect($(TestMinMax.errorNumber(4)).getText()).to.contain("Enter an answer less than or equal to 1,234");
      expect($(TestMinMax.errorNumber(5)).getText()).to.contain("Enter an answer more than 123");
      expect($(TestMinMax.errorNumber(6)).getText()).to.contain("Enter an answer less than 1,234");
      expect($(TestMinMax.errorNumber(7)).getText()).to.contain("Enter an answer less than or equal to 100");
      expect($(TestMinMax.errorNumber(8)).getText()).to.contain("Enter an answer more than or equal to £10.00");
    });

    it("When I enter values inside the set range but provide too many decimal places, Then the correct error messages are displayed", () => {
      $(TestMinMax.testRange()).setValue("1020");
      $(TestMinMax.testRangeExclusive()).setValue("11");
      $(TestMinMax.testMin()).setValue("123");
      $(TestMinMax.testMax()).setValue("1019");
      $(TestMinMax.testMinExclusive()).setValue("124");
      $(TestMinMax.testMaxExclusive()).setValue("1233");
      $(TestMinMax.testPercent()).setValue("100");
      $(TestMinMax.testRange()).setValue("12.344");
      $(TestMinMax.testDecimal()).setValue("11.234");
      $(TestMinMax.submit()).click();

      expect($(TestMinMax.errorNumber(1)).getText()).to.contain("Enter a number rounded to 2 decimal places");
      expect($(TestMinMax.errorNumber(2)).getText()).to.contain("Enter a number rounded to 2 decimal places");
    });

    it("When I enter values inside the set range, Then I should be able to submit the survey", () => {
      $(TestMinMax.testRange()).setValue("12");
      $(TestMinMax.testDecimal()).setValue("11.23");
      $(TestMinMax.testPercent()).setValue("99");
      $(TestMinMax.submit()).click();
      $(DetailAnswer.other()).click();
      $(DetailAnswer.otherDetail()).setValue("1020");
      $(DetailAnswer.submit()).click();

      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("When I edit and change the maximum value, Then I must re-validate and submit any dependent answers before I can return to the summary", () => {
      $(SubmitPage.setMaximumEdit()).click();
      $(SetMinMax.setMaximum()).setValue("1019");
      $(SetMinMax.submit()).click();
      $(TestMinMax.submit()).click();
      $(DetailAnswer.submit()).click();

      expect($(DetailAnswer.errorNumber(1)).getText()).to.contain("Enter an answer less than or equal to 1,019");

      $(DetailAnswer.otherDetail()).setValue("1019");
      $(DetailAnswer.submit()).click();

      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("When I edit and change the minimum value, Then I must re-validate and submit any dependent answers again before I can return to the summary", () => {
      $(SubmitPage.setMinimumEdit()).click();
      $(SetMinMax.setMinimum()).setValue("11");
      $(SetMinMax.submit()).click();
      $(TestMinMax.submit()).click();

      expect($(TestMinMax.errorNumber(1)).getText()).to.contain("Enter an answer more than 11");

      $(TestMinMax.testRangeExclusive()).setValue("12");
      $(TestMinMax.submit()).click();

      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });
  });
});
