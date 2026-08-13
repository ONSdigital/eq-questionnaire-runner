import { test, expect } from '../fixtures/test'
import MobileNumberBlockPage from '../generated_pages/mobile_number/mobile-number-block.page'
import SubmitPage from '../generated_pages/mobile_number/submit.page'

test.describe('Mobile number validation', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_mobile_number.json')
  })

  test('Given I am asked to enter Mobile no, When I enter a valid mobile number with no prefix and submit, Then confirmation section is displayed with entered mobile number', async ({
    page
  }) => {
    const mobileNumberBlockPage = new MobileNumberBlockPage(page)
    const submitPage = new SubmitPage(page)
    await mobileNumberBlockPage.mobileNumber().fill('7712345678')
    await mobileNumberBlockPage.submit().click()
    await expect(submitPage.mobileNumberAnswer()).toHaveText('7712345678')
  })

  test('Given I am asked to enter Mobile no, When I enter a valid mobile number with prefix (+44) and submit, Then confirmation section is displayed with entered mobile number', async ({
    page
  }) => {
    const mobileNumberBlockPage = new MobileNumberBlockPage(page)
    const submitPage = new SubmitPage(page)
    await mobileNumberBlockPage.mobileNumber().fill('+447712345678')
    await mobileNumberBlockPage.submit().click()
    await expect(submitPage.mobileNumberAnswer()).toHaveText('+447712345678')
  })

  test('Given I am asked to enter Mobile no, When I enter an invalid mobile number and submit, Then an error screen with invalid number information is displayed', async ({
    page
  }) => {
    const mobileNumberBlockPage = new MobileNumberBlockPage(page)
    await mobileNumberBlockPage.mobileNumber().fill('12345678')
    await mobileNumberBlockPage.submit().click()
    await expect(mobileNumberBlockPage.errorNumber(1)).toContainText('Enter a UK mobile number in a valid format')
  })
})
