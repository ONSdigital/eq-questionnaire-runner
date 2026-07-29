import { test, expect } from '../../../fixtures/test'
import NumberOfEmployeesTotalBlockPage from '../../../generated_pages/confirmation_question/number-of-employees-total-block.page'
import ConfirmZeroEmployeesBlockPage from '../../../generated_pages/confirmation_question/confirm-zero-employees-block.page'
import SubmitPage from '../../../generated_pages/confirmation_question/submit.page'

test.describe('Feature: Routing incompletes block if routing backwards', () => {
  test('Given a confirmation question flow, When I answer zero employees and confirm, Then I should reach the summary', async ({ page, openQuestionnaire }) => {
    const numberOfEmployeesTotalBlockPage = new NumberOfEmployeesTotalBlockPage(page)
    const confirmZeroEmployeesBlockPage = new ConfirmZeroEmployeesBlockPage(page)
    const submitPage = new SubmitPage(page)

    await openQuestionnaire('test_confirmation_question.json')
    await numberOfEmployeesTotalBlockPage.numberOfEmployeesTotal().fill('0')
    await numberOfEmployeesTotalBlockPage.submit().click()
    await confirmZeroEmployeesBlockPage.yesThisIsCorrect().click()
    await confirmZeroEmployeesBlockPage.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
  })
})
