import { test, expect } from '../../../fixtures/test'
import CheckboxNumericDetailPage from '../../../generated_pages/checkbox_detail_answer_numeric/checkbox-numeric-detail.page'
import SubmitPage from '../../../generated_pages/checkbox_detail_answer_numeric/submit.page'

test.describe('Checkbox with a numeric "detail_answer" option', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    const checkboxNumericDetailPage = new CheckboxNumericDetailPage(page)
    await openQuestionnaire('test_checkbox_detail_answer_numeric.json')
    await checkboxNumericDetailPage.other().click()
  })

  test('Given a numeric detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', async ({
    page
  }) => {
    const checkboxNumericDetailPage = new CheckboxNumericDetailPage(page)
    await expect(checkboxNumericDetailPage.otherDetail()).toBeVisible()
  })

  test('Given a numeric detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', async ({
    page
  }) => {
    const checkboxNumericDetailPage = new CheckboxNumericDetailPage(page)
    const submitPage = new SubmitPage(page)
    await expect(checkboxNumericDetailPage.otherDetail()).toBeVisible()
    await checkboxNumericDetailPage.submit().click()
    await expect(submitPage.checkboxNumericDetailAnswer()).toHaveText('Other')
  })

  test('Given a numeric detail answer, When the user provides text, Then that text should be displayed on the summary screen', async ({ page }) => {
    const checkboxNumericDetailPage = new CheckboxNumericDetailPage(page)
    const submitPage = new SubmitPage(page)
    await checkboxNumericDetailPage.otherDetail().fill('15')
    await checkboxNumericDetailPage.submit().click()
    await expect(submitPage.checkboxNumericDetailAnswer()).toContainText('15')
  })

  test('Given a numeric detail answer, When the user provides text, An error should be displayed', async ({ page }) => {
    const checkboxNumericDetailPage = new CheckboxNumericDetailPage(page)
    await checkboxNumericDetailPage.otherDetail().fill('fhdjkshfjkds')
    await checkboxNumericDetailPage.submit().click()
    await expect(checkboxNumericDetailPage.error()).toBeVisible()
    await expect(checkboxNumericDetailPage.errorNumber(1)).toHaveText('Please enter an integer')
  })

  test('Given a numeric detail answer, When the user provides a number larger than 20, An error should be displayed', async ({ page }) => {
    const checkboxNumericDetailPage = new CheckboxNumericDetailPage(page)
    await checkboxNumericDetailPage.otherDetail().fill('250')
    await checkboxNumericDetailPage.submit().click()
    await expect(checkboxNumericDetailPage.error()).toBeVisible()
    await expect(checkboxNumericDetailPage.errorNumber(1)).toHaveText('Number is too large')
  })

  test('Given a numeric detail answer, When the user provides a number less than 0, An error should be displayed', async ({ page }) => {
    const checkboxNumericDetailPage = new CheckboxNumericDetailPage(page)
    await checkboxNumericDetailPage.otherDetail().fill('-1')
    await checkboxNumericDetailPage.submit().click()
    await expect(checkboxNumericDetailPage.error()).toBeVisible()
    await expect(checkboxNumericDetailPage.errorNumber(1)).toHaveText('Number cannot be less than zero')
  })

  test('Given a numeric detail answer, When the user provides text, An error should be displayed and the text in the textbox should be kept', async ({
    page
  }) => {
    const checkboxNumericDetailPage = new CheckboxNumericDetailPage(page)
    await checkboxNumericDetailPage.otherDetail().fill('biscuits')
    await checkboxNumericDetailPage.submit().click()
    await expect(checkboxNumericDetailPage.error()).toBeVisible()
    await expect(checkboxNumericDetailPage.errorNumber(1)).toHaveText('Please enter an integer')
    await page.waitForTimeout(1000)
    await expect(checkboxNumericDetailPage.otherDetail()).toHaveValue('biscuits')
  })

  test('Given a numeric detail answer, When the user enters "0" and submits, Then "0" should be displayed on the summary screen', async ({ page }) => {
    const checkboxNumericDetailPage = new CheckboxNumericDetailPage(page)
    const submitPage = new SubmitPage(page)
    await checkboxNumericDetailPage.otherDetail().fill('0')
    await checkboxNumericDetailPage.submit().click()
    await expect(submitPage.checkboxNumericDetailAnswer()).toContainText('0')
  })
})
