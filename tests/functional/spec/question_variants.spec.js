const ageBlock = require('../generated_pages/variants_question/age-block.page.js');
const ageConfirmationBlock = require('../generated_pages/variants_question/age-confirmation-block.page.js');
const currencyBlock = require('../generated_pages/variants_question/currency-block.page.js');
const firstNumberBlock = require('../generated_pages/variants_question/first-number-block.page.js');
const nameBlock = require('../generated_pages/variants_question/name-block.page.js');
const proxyBlock = require('../generated_pages/variants_question/proxy-block.page.js');
const secondNumberBlock = require('../generated_pages/variants_question/second-number-block.page.js');

const SectionSummaryPage = require('../base_pages/section-summary.page.js');

describe('QuestionVariants', function() {
  beforeEach(function() {
    browser.openQuestionnaire('test_variants_question.json');
  });

  it('Given I am completing the survey, then the correct questions are shown based on my previous answers', function () {
    $(nameBlock.firstName()).setValue('Guido');
    $(nameBlock.lastName()).setValue('van Rossum');
    $(nameBlock.submit()).click();

    expect($(proxyBlock.questionText()).getText()).to.contain('Are you Guido van Rossum?');

    $(proxyBlock.noIAmAnsweringOnTheirBehalf()).click();
    $(proxyBlock.submit()).click();

    expect($(ageBlock.questionText()).getText()).to.contain('What age is Guido van Rossum');

    $(ageBlock.age()).setValue(63);
    $(ageBlock.submit()).click();

    expect($(ageConfirmationBlock.questionText()).getText()).to.contain('Guido van Rossum is over 16?');

    $(ageConfirmationBlock.ageConfirmYes()).click();
    $(ageConfirmationBlock.submit()).click();

    expect($(SectionSummaryPage.summaryRowTitle(1)).getText()).to.contain('What age is Guido van Rossum');
    expect($(SectionSummaryPage.summaryRowValue(1)).getText()).to.contain('63');

    $(SectionSummaryPage.submit()).click();

    $(currencyBlock.sterling()).click();
    $(currencyBlock.submit()).click();

    expect($(firstNumberBlock.firstNumberLabel()).getText()).to.contain('First answer in GBP');

    $(firstNumberBlock.firstNumber()).setValue(123);
    $(firstNumberBlock.submit()).click();

    $(secondNumberBlock.secondNumber()).setValue(321);
    $(secondNumberBlock.submit()).click();

    expect($(SectionSummaryPage.summaryRowValue(1)).getText()).to.contain('Sterling');
    expect($(SectionSummaryPage.summaryRowValue(2)).getText()).to.contain('£');

    $(SectionSummaryPage.summaryRowAction(1)).click();
    $(currencyBlock.usDollars()).click();
    $(currencyBlock.submit()).click();

    expect($(SectionSummaryPage.summaryRowValue(2)).getText()).to.contain('$');

    });
});
