import { test, expect } from '../../../fixtures/test'
import type { Page } from '../../../fixtures/test'
import AddressBlockPage from '../../../generated_pages/custom_question_summary/address.page'
import AgeBlock from '../../../generated_pages/custom_question_summary/age.page'
import NameBlockPage from '../../../generated_pages/custom_question_summary/name.page'
import SubmitPage from '../../../generated_pages/custom_question_summary/submit.page'

test.describe('Summary Screen', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_custom_question_summary.json')
  })

  test('Given a survey has question summary concatenations and has been completed when on the summary page then the correct response should be displayed formatted correctly', async ({
    page
  }) => {
    const submitPage = new SubmitPage(page)
    const addressSummary = submitPage.summaryRowState('address-question-concatenated-answer')
    const ageSummary = submitPage.summaryRowState('age-question-concatenated-answer')
    await completeAllQuestions(page)
    await expect(submitPage.summaryRowState('name-question-concatenated-answer')).toHaveText('John Smith')
    await expect(addressSummary.locator('br')).toHaveCount(2)
    await expect(addressSummary).toHaveText(/Cardiff Road\s*Newport\s*NP10 8XG/)
    await expect(ageSummary.locator('br')).toHaveCount(1)
    await expect(ageSummary).toHaveText(/7\s*This age is an estimate/)
  })

  test('Given no values are entered in a question with multiple answers and concatenation set, when on the summary screen then the correct response should be displayed', async ({
    page
  }) => {
    const addressBlockPage = new AddressBlockPage(page)
    const ageBlock = new AgeBlock(page)
    const nameBlockPage = new NameBlockPage(page)
    const submitPage = new SubmitPage(page)
    await nameBlockPage.submit().click()
    await addressBlockPage.submit().click()
    await ageBlock.submit().click()
    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    await expect(submitPage.summaryRowState('name-question-concatenated-answer')).toHaveText('No answer provided')
  })

  async function completeAllQuestions (page: Page): Promise<void> {
    const nameBlockPage = new NameBlockPage(page)
    const addressBlockPage = new AddressBlockPage(page)
    const ageBlock = new AgeBlock(page)

    await nameBlockPage.first().fill('John')
    await nameBlockPage.last().fill('Smith')
    await nameBlockPage.submit().click()
    await addressBlockPage.line1().fill('Cardiff Road')
    await addressBlockPage.townCity().fill('Newport')
    await addressBlockPage.postcode().fill('NP10 8XG')
    await addressBlockPage.submit().click()
    await ageBlock.number().fill('7')
    await ageBlock.singleCheckboxThisAgeIsAnEstimate().click()
    await ageBlock.submit().click()
  }
})
