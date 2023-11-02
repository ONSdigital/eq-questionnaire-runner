import ageBlock from "../generated_pages/variants_question/age-block.page.js";
import ageConfirmationBlock from "../generated_pages/variants_question/age-confirmation-block.page.js";
import basicVariantsSummary from "../generated_pages/variants_question/basic-question-variant-section-summary.page.js";
import currencyBlock from "../generated_pages/variants_question/currency-block.page.js";
import currencySectionSummary from "../generated_pages/variants_question/currency-section-summary.page.js";
import firstNumberBlock from "../generated_pages/variants_question/first-number-block.page.js";
import nameBlock from "../generated_pages/variants_question/name-block.page.js";
import proxyBlock from "../generated_pages/variants_question/proxy-block.page.js";
import secondNumberBlock from "../generated_pages/variants_question/second-number-block.page.js";
import { click } from "../helpers";

describe("QuestionVariants", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_variants_question.json");
  });

  it("Given I am completing the survey, then the correct questions are shown based on my previous answers", async () => {
    await $(nameBlock.firstName()).setValue("Guido");
    await $(nameBlock.lastName()).setValue("van Rossum");
    await click(nameBlock.submit());

    await expect(await $(proxyBlock.questionText()).getText()).toBe("Are you Guido van Rossum?");

    await $(proxyBlock.noIAmAnsweringOnTheirBehalf()).click();
    await click(proxyBlock.submit());

    await expect(await $(ageBlock.questionText()).getText()).toBe("What age is Guido van Rossum?");

    await $(ageBlock.age()).setValue(63);
    await click(ageBlock.submit());

    await expect(await $(ageConfirmationBlock.questionText()).getText()).toBe("Guido van Rossum is over 16?");

    await $(ageConfirmationBlock.ageConfirmYes()).click();
    await click(ageConfirmationBlock.submit());

    await expect(await $(basicVariantsSummary.ageQuestion()).getText()).toBe("What age is Guido van Rossum?");
    await expect(await $(basicVariantsSummary.ageAnswer()).getText()).toBe("63");

    await click(basicVariantsSummary.submit());

    await $(currencyBlock.sterling()).click();
    await click(currencyBlock.submit());

    await expect(await $(firstNumberBlock.firstNumberLabel()).getText()).toBe("First answer in GBP");

    await $(firstNumberBlock.firstNumber()).setValue(123);
    await click(firstNumberBlock.submit());

    await $(secondNumberBlock.secondNumber()).setValue(321);
    await click(secondNumberBlock.submit());

    await expect(await $(currencySectionSummary.currencyAnswer()).getText()).toBe("Sterling");
    await expect(await $(currencySectionSummary.firstNumberAnswer()).getText()).toContain("£");

    await $(currencySectionSummary.currencyAnswerEdit()).click();
    await $(currencyBlock.usDollars()).click();
    await click(currencyBlock.submit());

    await expect(await $(currencySectionSummary.firstNumberAnswer()).getText()).toContain("$");
  });
});
