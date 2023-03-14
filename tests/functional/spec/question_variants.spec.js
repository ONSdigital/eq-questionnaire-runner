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
  beforeEach(async () => {
    await browser.openQuestionnaire("test_variants_question.json");
  });

  it("Given I am completing the survey, then the correct questions are shown based on my previous answers", async () => {
    await $(nameBlock.firstName()).setValue("Guido");
    await $(nameBlock.lastName()).setValue("van Rossum");
    await $(nameBlock.submit()).click();

    await expect(await $(proxyBlock.questionText()).getText()).to.contain("Are you Guido van Rossum?");

    await $(proxyBlock.noIAmAnsweringOnTheirBehalf()).click();
    await $(proxyBlock.submit()).click();

    await expect(await $(ageBlock.questionText()).getText()).to.contain("What age is Guido van Rossum");

    await $(ageBlock.age()).setValue(63);
    await $(ageBlock.submit()).click();

    await expect(await $(ageConfirmationBlock.questionText()).getText()).to.contain("Guido van Rossum is over 16?");

    await $(ageConfirmationBlock.ageConfirmYes()).click();
    await $(ageConfirmationBlock.submit()).click();

    await expect(await $(basicVariantsSummary.ageQuestion()).getText()).to.contain("What age is Guido van Rossum");
    await expect(await $(basicVariantsSummary.ageAnswer()).getText()).to.contain("63");

    await $(basicVariantsSummary.submit()).click();

    await $(currencyBlock.sterling()).click();
    await $(currencyBlock.submit()).click();

    await expect(await $(firstNumberBlock.firstNumberLabel()).getText()).to.contain("First answer in GBP");

    await $(firstNumberBlock.firstNumber()).setValue(123);
    await $(firstNumberBlock.submit()).click();

    await $(secondNumberBlock.secondNumber()).setValue(321);
    await $(secondNumberBlock.submit()).click();

    await expect(await $(currencySectionSummary.currencyAnswer()).getText()).to.contain("Sterling");
    await expect(await $(currencySectionSummary.firstNumberAnswer()).getText()).to.contain("£");

    await $(currencySectionSummary.currencyAnswerEdit()).click();
    await $(currencyBlock.usDollars()).click();
    await $(currencyBlock.submit()).click();

    await expect(await $(currencySectionSummary.firstNumberAnswer()).getText()).to.contain("$");
  });
});
