import { test, expect } from '../fixtures/test'
import AgeBlock from '../generated_pages/variants_question/age-block.page'
import AgeConfirmationBlock from '../generated_pages/variants_question/age-confirmation-block.page'
import BasicVariantsSummary from '../generated_pages/variants_question/basic-question-variant-section-summary.page'
import CurrencyBlock from '../generated_pages/variants_question/currency-block.page'
import CurrencySectionSummary from '../generated_pages/variants_question/currency-section-summary.page'
import FirstNumberBlock from '../generated_pages/variants_question/first-number-block.page'
import NameBlock from '../generated_pages/variants_question/name-block.page'
import ProxyBlock from '../generated_pages/variants_question/proxy-block.page'
import SecondNumberBlock from '../generated_pages/variants_question/second-number-block.page'

test.describe('QuestionVariants', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_variants_question.json')
  })

  test('Given I am completing the survey, then the correct questions are shown based on my previous answers', async ({ page }) => {
    const ageBlock = new AgeBlock(page)
    const ageConfirmationBlock = new AgeConfirmationBlock(page)
    const basicVariantsSummary = new BasicVariantsSummary(page)
    const currencyBlock = new CurrencyBlock(page)
    const currencySectionSummary = new CurrencySectionSummary(page)
    const firstNumberBlock = new FirstNumberBlock(page)
    const nameBlock = new NameBlock(page)
    const proxyBlock = new ProxyBlock(page)
    const secondNumberBlock = new SecondNumberBlock(page)
    await nameBlock.firstName().fill('Guido')
    await nameBlock.lastName().fill('van Rossum')
    await nameBlock.submit().click()

    await expect(proxyBlock.questionText()).toHaveText('Are you Guido van Rossum?')

    await proxyBlock.noIAmAnsweringOnTheirBehalf().click()
    await proxyBlock.submit().click()

    await expect(ageBlock.questionText()).toHaveText('What age is Guido van Rossum?')

    await ageBlock.age().fill('63')
    await ageBlock.submit().click()

    await expect(ageConfirmationBlock.questionText()).toHaveText('Guido van Rossum is over 16?')

    await ageConfirmationBlock.ageConfirmYes().click()
    await ageConfirmationBlock.submit().click()

    await expect(basicVariantsSummary.ageQuestion()).toHaveText('What age is Guido van Rossum?')
    await expect(basicVariantsSummary.ageAnswer()).toHaveText('63')

    await basicVariantsSummary.submit().click()

    await currencyBlock.sterling().click()
    await currencyBlock.submit().click()

    await expect(firstNumberBlock.firstNumberLabel()).toHaveText('First answer in GBP')

    await firstNumberBlock.firstNumber().fill('123')
    await firstNumberBlock.submit().click()

    await secondNumberBlock.secondNumber().fill('321')
    await secondNumberBlock.submit().click()

    await expect(currencySectionSummary.currencyAnswer()).toHaveText('Sterling')
    await expect(currencySectionSummary.firstNumberAnswer()).toContainText('£')

    await currencySectionSummary.currencyAnswerEdit().click()
    await currencyBlock.usDollars().click()
    await currencyBlock.submit().click()

    await expect(currencySectionSummary.firstNumberAnswer()).toContainText('$')
  })
})
