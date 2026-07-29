import { test, expect } from '../../fixtures/test'
import NumberOfEmployeesTotalBlockPage from '../../generated_pages/confirmation_question/number-of-employees-total-block.page'
import ConfirmZeroEmployeesBlockPage from '../../generated_pages/confirmation_question/confirm-zero-employees-block.page'
import SubmitPage from '../../generated_pages/confirmation_question/submit.page'

test.describe('Feature: Confirmation Question', () => {
  test.describe('Given I have a completed the confirmation question', () => {
    test.beforeEach('Get to summary', async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_confirmation_question.json')
    })

    test('When I view the summary, Then the confirmation question should not be displayed', async ({ page }) => {
      const confirmZeroEmployeesBlockPage = new ConfirmZeroEmployeesBlockPage(page)
      const numberOfEmployeesTotalBlockPage = new NumberOfEmployeesTotalBlockPage(page)
      const submitPage = new SubmitPage(page)
      await numberOfEmployeesTotalBlockPage.numberOfEmployeesTotal().fill('0')
      await numberOfEmployeesTotalBlockPage.submit().click()
      await confirmZeroEmployeesBlockPage.yesThisIsCorrect().click()
      await confirmZeroEmployeesBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
      await expect(submitPage.numberOfEmployeesTotal()).toHaveText('0')
      await expect(submitPage.confirmZeroEmployeesAnswer()).toHaveCount(0)
    })
  })

  test.describe('Given a confirmation Question', () => {
    test("When I answer 'No' to the confirmation question, Then I should be routed back to the source question", async ({ page, openQuestionnaire }) => {
      const confirmZeroEmployeesBlockPage = new ConfirmZeroEmployeesBlockPage(page)
      const numberOfEmployeesTotalBlockPage = new NumberOfEmployeesTotalBlockPage(page)
      await openQuestionnaire('test_confirmation_question.json')
      await numberOfEmployeesTotalBlockPage.submit().click()
      await confirmZeroEmployeesBlockPage.noINeedToCorrectThis().click()
      await confirmZeroEmployeesBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(numberOfEmployeesTotalBlockPage.pageName))
    })
  })

  test.describe('Given a number of employees Question', () => {
    test(
      "When I don't answer the number of employees question and go to summary, " +
        'Then default value should be displayed for the the number of employees question',
      async ({ page, openQuestionnaire }) => {
        const confirmZeroEmployeesBlockPage = new ConfirmZeroEmployeesBlockPage(page)
        const numberOfEmployeesTotalBlockPage = new NumberOfEmployeesTotalBlockPage(page)
        const submitPage = new SubmitPage(page)
        await openQuestionnaire('test_confirmation_question.json')
        await numberOfEmployeesTotalBlockPage.submit().click()
        await confirmZeroEmployeesBlockPage.yesThisIsCorrect().click()
        await confirmZeroEmployeesBlockPage.submit().click()
        await expect(submitPage.numberOfEmployeesTotal()).toHaveText('0')
      }
    )
  })
})
