import { createOpenQuestionnaire, test, expect } from '../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../fixtures/test'
import SubmitPage from '../generated_pages/confirmation_email/submit.page'
import ThankYouPage from '../base_pages/thank-you.page'
import ConfirmationEmailPage from '../base_pages/confirmation-email.page'
import ConfirmationEmailSentPage from '../base_pages/confirmation-email-sent.page'
import ConfirmEmailPage from '../base_pages/confirm-email.page'
import { verifyUrlContains } from '../helpers'

const errorPanel = '[data-ga="error"]'

test.describe('Email confirmation', () => {
  test.describe.configure({ mode: 'serial' })

  test.describe('Given I launch the test email confirmation survey', () => {
    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll(async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_confirmation_email.json')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When I complete the survey and am on the thank you page, Then there is option to enter an email address', async () => {
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      await submitPage.submit().click()
      await submitPage.submit().click()
      await verifyUrlContains(page, thankYouPage.pageName)
      await expect(thankYouPage.email()).toBeVisible()
    })

    test('When I submit the form without providing an email address, Then I get an error message', async () => {
      const thankYouPage = new ThankYouPage(page)
      await thankYouPage.submit().click()
      await verifyUrlContains(page, thankYouPage.pageName)
      await expect(page.locator(errorPanel)).toBeVisible()
      await expect(page.locator(errorPanel)).toHaveText('Enter an email address')
    })

    test('When I submit the form without providing a correctly formatted email address, Then I get an error message', async () => {
      const thankYouPage = new ThankYouPage(page)
      await thankYouPage.email().fill('incorrect-format')
      await thankYouPage.submit().click()
      await verifyUrlContains(page, thankYouPage.pageName)
      await expect(page.locator(errorPanel)).toBeVisible()
      await expect(page.locator(errorPanel)).toHaveText('Enter an email address in a valid format, for example name@example.com')
    })

    test('When I submit the form with a valid email address, Then I go to the confirm email page', async () => {
      const confirmEmailPage = new ConfirmEmailPage(page)
      const thankYouPage = new ThankYouPage(page)
      await thankYouPage.email().fill('name@example.com')
      await thankYouPage.submit().click()
      await verifyUrlContains(page, 'confirmation-email/confirm')
      await expect(confirmEmailPage.questionTitle()).toHaveText('Is this email address correct?')
    })

    test('When I submit the confirm email page without providing an answer, Then I get an error message', async () => {
      const confirmEmailPage = new ConfirmEmailPage(page)
      await confirmEmailPage.submit().click()
      await verifyUrlContains(page, 'confirmation-email/confirm')
      await expect(confirmEmailPage.errorPanel()).toBeVisible()
      await expect(confirmEmailPage.errorPanel()).toContainText('Select an answer')
    })

    test("When I answer 'Yes' and submit the confirm email page, Then I go to email sent page", async () => {
      const confirmationEmailSentPage = new ConfirmationEmailSentPage(page)
      const confirmEmailPage = new ConfirmEmailPage(page)
      await confirmEmailPage.yes().click()
      await confirmEmailPage.submit().click()
      await verifyUrlContains(page, 'confirmation-email/sent')
      await expect(confirmationEmailSentPage.confirmationText()).toHaveText('A confirmation email has been sent to name@example.com')
    })

    test('When I go to the confirmation email page and submit without providing an email address, Then I get an error message', async () => {
      const confirmationEmailPage = new ConfirmationEmailPage(page)
      const confirmationEmailSentPage = new ConfirmationEmailSentPage(page)
      await confirmationEmailSentPage.sendAnotherEmail().click()
      await confirmationEmailPage.submit().click()
      await verifyUrlContains(page, 'confirmation-email/send')
      await expect(confirmationEmailPage.errorPanel()).toBeVisible()
      await expect(confirmationEmailPage.errorPanel()).toHaveText('Enter an email address')
    })

    test('When I submit the form without providing a correctly formatted email address on the confirmation email page, Then I get an error message', async () => {
      const confirmationEmailPage = new ConfirmationEmailPage(page)
      await confirmationEmailPage.email().fill('incorrect-format')
      await confirmationEmailPage.submit().click()
      await verifyUrlContains(page, 'confirmation-email/send')
      await expect(confirmationEmailPage.errorPanel()).toBeVisible()
      await expect(confirmationEmailPage.errorPanel()).toHaveText('Enter an email address in a valid format, for example name@example.com')
    })

    test('When I submit the form with a valid email and confirm it is correct, Then I go to the email confirmation page', async () => {
      const confirmationEmailPage = new ConfirmationEmailPage(page)
      const confirmationEmailSentPage = new ConfirmationEmailSentPage(page)
      const confirmEmailPage = new ConfirmEmailPage(page)
      await confirmationEmailPage.email().fill('name@example.com')
      await confirmationEmailPage.submit().click()
      await confirmEmailPage.yes().click()
      await confirmEmailPage.submit().click()
      await verifyUrlContains(page, 'confirmation-email/sent')
      await expect(confirmationEmailSentPage.confirmationText()).toHaveText('A confirmation email has been sent to name@example.com')
    })
  })

  test.describe('Given I launch the test email confirmation survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_confirmation_email.json')
    })

    test("When I enter an email and answer 'No' on the confirm email page, Then I go the confirmation send page with the email pre-filled", async ({
      page
    }) => {
      const confirmationEmailPage = new ConfirmationEmailPage(page)
      const confirmEmailPage = new ConfirmEmailPage(page)
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      await submitPage.submit().click()
      await submitPage.submit().click()
      await thankYouPage.email().fill('name@example.com')
      await thankYouPage.submit().click()
      await confirmEmailPage.no().click()
      await confirmEmailPage.submit().click()
      await verifyUrlContains(page, 'confirmation-email/send')
      await expect(confirmationEmailPage.email()).toHaveValue('name@example.com')
    })
  })
})

test.describe('Email confirmation', () => {
  test.describe('Given I launch the test email confirmation survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_confirmation_email.json')
    })

    test('When I view the email confirmation page, Then I should not see the feedback call to action', async ({ page }) => {
      const confirmationEmailSentPage = new ConfirmationEmailSentPage(page)
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      await submitPage.submit().click()
      await submitPage.submit().click()
      await thankYouPage.email().fill('name@example.com')
      await thankYouPage.submit().click()
      await expect(confirmationEmailSentPage.feedbackLink()).not.toBeVisible()
    })
  })
})
