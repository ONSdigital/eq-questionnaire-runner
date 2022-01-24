import ageBlock from "../generated_pages/variants_question/age-block.page.js";
import ageConfirmationBlock from "../generated_pages/variants_question/age-confirmation-block.page.js";
import basicVariantsSummary from "../generated_pages/variants_question/basic-question-variant-section-summary.page.js";
import currencyBlock from "../generated_pages/variants_question/currency-block.page.js";
import currencySectionSummary from "../generated_pages/variants_question/currency-section-summary.page.js";
import firstNumberBlock from "../generated_pages/variants_question/first-number-block.page.js";
import nameBlock from "../generated_pages/variants_question/name-block.page.js";
import proxyBlock from "../generated_pages/variants_question/proxy-block.page.js";
import secondNumberBlock from "../generated_pages/variants_question/second-number-block.page.js";

describe("QuestionVariants", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_new_variants_question.json");
  });

  it("Given I am completing the survey, then the correct questions are shown based on my previous answers", () => {
    $(nameBlock.firstName()).setValue("Guido");
    $(nameBlock.lastName()).setValue("van Rossum");
    $(nameBlock.submit()).click();

    expect($(proxyBlock.questionText()).getText()).to.contain("Are you Guido van Rossum?");

    $(proxyBlock.noIAmAnsweringOnTheirBehalf()).click();
    $(proxyBlock.submit()).click();

    expect($(ageBlock.questionText()).getText()).to.contain("What age is Guido van Rossum");

    $(ageBlock.age()).setValue(63);
    $(ageBlock.submit()).click();

    expect($(ageConfirmationBlock.questionText()).getText()).to.contain("Guido van Rossum is over 16?");

    $(ageConfirmationBlock.ageConfirmYes()).click();
    $(ageConfirmationBlock.submit()).click();

    expect($(basicVariantsSummary.ageQuestion()).getText()).to.contain("What age is Guido van Rossum");
    expect($(basicVariantsSummary.ageAnswer()).getText()).to.contain("63");

    $(basicVariantsSummary.submit()).click();

    $(currencyBlock.sterling()).click();
    $(currencyBlock.submit()).click();

    expect($(firstNumberBlock.firstNumberLabel()).getText()).to.contain("First answer in GBP");

    $(firstNumberBlock.firstNumber()).setValue(123);
    $(firstNumberBlock.submit()).click();

    $(secondNumberBlock.secondNumber()).setValue(321);
    $(secondNumberBlock.submit()).click();

    expect($(currencySectionSummary.currencyAnswer()).getText()).to.contain("Sterling");
    expect($(currencySectionSummary.firstNumberAnswer()).getText()).to.contain("£");

    $(currencySectionSummary.currencyAnswerEdit()).click();
    $(currencyBlock.usDollars()).click();
    $(currencyBlock.submit()).click();

    expect($(currencySectionSummary.firstNumberAnswer()).getText()).to.contain("$");
  });
});
