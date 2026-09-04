import { test, expect } from '../../../fixtures/test'
import RadioNumericDetailPage from '../../../generated_pages/radio_detail_answer_numeric/radio-numeric-detail.page'
import SubmitPage from '../../../generated_pages/radio_detail_answer_numeric/submit.page'

test.describe('Radio with a numeric "detail_answer" option', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    const radioNumericDetailPage = new RadioNumericDetailPage(page)
    await openQuestionnaire('test_radio_detail_answer_numeric.json')
    await radioNumericDetailPage.other().click()
  })

  test('Given a numeric detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', async ({
    page
  }) => {
    const radioNumericDetailPage = new RadioNumericDetailPage(page)
    await expect(radioNumericDetailPage.otherDetail()).toBeVisible()
  })

  test('Given a numeric detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', async ({
    page
  }) => {
    const radioNumericDetailPage = new RadioNumericDetailPage(page)
    const submitPage = new SubmitPage(page)
    await expect(radioNumericDetailPage.otherDetail()).toBeVisible()
    await radioNumericDetailPage.submit().click()
    await expect(submitPage.radioAnswerNumericDetail()).toHaveText('Other')
  })

  test('Given a numeric detail answer, When the user provides text, Then that text should be displayed on the summary screen', async ({ page }) => {
    const radioNumericDetailPage = new RadioNumericDetailPage(page)
    const submitPage = new SubmitPage(page)
    await radioNumericDetailPage.otherDetail().fill('15')
    await radioNumericDetailPage.submit().click()
    await expect(submitPage.radioAnswerNumericDetail()).toContainText('15')
  })

  test('Given a numeric detail answer, When the user provides text, An error should be displayed', async ({ page }) => {
    const radioNumericDetailPage = new RadioNumericDetailPage(page)
    await radioNumericDetailPage.otherDetail().fill('fhdjkshfjkds')
    await radioNumericDetailPage.submit().click()
    await expect(radioNumericDetailPage.error()).toBeVisible()
    await expect(radioNumericDetailPage.errorNumber(1)).toHaveText('Please enter an integer')
  })

  test('Given a numeric detail answer, When the user provides a number larger than 20, An error should be displayed', async ({ page }) => {
    const radioNumericDetailPage = new RadioNumericDetailPage(page)
    await radioNumericDetailPage.otherDetail().fill('250')
    await radioNumericDetailPage.submit().click()
    await expect(radioNumericDetailPage.error()).toBeVisible()
    await expect(radioNumericDetailPage.errorNumber(1)).toHaveText('Number is too large')
  })

  test('Given a numeric detail answer, When the user provides a number less than 0, An error should be displayed', async ({ page }) => {
    const radioNumericDetailPage = new RadioNumericDetailPage(page)
    await radioNumericDetailPage.otherDetail().fill('-1')
    await radioNumericDetailPage.submit().click()
    await expect(radioNumericDetailPage.error()).toBeVisible()
    await expect(radioNumericDetailPage.errorNumber(1)).toHaveText('Number cannot be less than zero')
  })

  test('Given a numeric detail answer, When the user provides text, An error should be displayed and the text in the textbox should be kept', async ({
    page
  }) => {
    const radioNumericDetailPage = new RadioNumericDetailPage(page)
    await radioNumericDetailPage.otherDetail().fill('biscuits')
    await radioNumericDetailPage.submit().click()
    await expect(radioNumericDetailPage.error()).toBeVisible()
    await expect(radioNumericDetailPage.errorNumber(1)).toHaveText('Please enter an integer')
    await expect(radioNumericDetailPage.otherDetail()).toHaveValue('biscuits')
  })

  test('Given a numeric detail answer, When the user enters "0" and submits, Then "0" should be displayed on the summary screen', async ({ page }) => {
    const radioNumericDetailPage = new RadioNumericDetailPage(page)
    const submitPage = new SubmitPage(page)
    await radioNumericDetailPage.otherDetail().fill('0')
    await radioNumericDetailPage.submit().click()
    await expect(submitPage.radioAnswerNumericDetail()).toContainText('0')
  })
})
