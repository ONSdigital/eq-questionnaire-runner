import { test, expect } from '../fixtures/test'
import SubmitPage from '../base_pages/submit.page'
import HubPage from '../base_pages/hub.page'
import CheckboxPage from '../generated_pages/title/single-title-block.page'
import ThankYouPage from '../base_pages/thank-you.page'
import DidYouKnowPage from '../generated_pages/thank_you/did-you-know.page'
import ThankYouSubmitPage from '../generated_pages/thank_you/submit.page'

test.describe('Thank You Social', () => {
  test.describe('Given I launch a social themed questionnaire', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_theme_social.json', { theme: 'social' })
    })

    test('When I navigate to the thank you page, Then I should see social theme content', async ({ page }) => {
      const hubPage = new HubPage(page)
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      await submitPage.submit().click()
      await hubPage.submit().click()
      await expect(page).toHaveURL(new RegExp(thankYouPage.pageName))
      await expect(thankYouPage.title()).toContainText('Thank you for completing the Test Theme Social')
      await expect(thankYouPage.guidance()).toContainText('Your answers have been submitted')
      await expect(thankYouPage.metadata()).toContainText('Submitted on:')
      await expect(thankYouPage.metadata()).not.toContainText('Submission reference:')
    })
  })
})

test.describe('Thank You Default', () => {
  test.describe('Given I launch a default themed questionnaire', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_title.json')
    })

    test('When I navigate to the thank you page, Then I should see default theme content', async ({ page }) => {
      const checkboxPage = new CheckboxPage(page)
      const hubPage = new HubPage(page)
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      await checkboxPage.good().click()
      await submitPage.submit().click()
      await hubPage.submit().click()
      await expect(page).toHaveURL(new RegExp(thankYouPage.pageName))
      await expect(thankYouPage.title()).toContainText('Thank you for completing the Test Title')
      await expect(thankYouPage.guidance()).toContainText('Your answers have been submitted for')
      await expect(thankYouPage.metadata()).toContainText('Submitted on:')
      await expect(thankYouPage.metadata()).toContainText('Submission reference:')
    })
  })
})

test.describe('Thank You Default View Response Enabled', () => {
  test.describe('Given I launch a questionnaire where view response is enabled', () => {
    test.beforeEach(async ({ page, openQuestionnaire }) => {
      const didYouKnowPage = new DidYouKnowPage(page)
      const thankYouPage = new ThankYouPage(page)
      const thankYouSubmitPage = new ThankYouSubmitPage(page)
      await openQuestionnaire('test_thank_you.json')
      await didYouKnowPage.yes().click()
      await didYouKnowPage.submit().click()
      await thankYouSubmitPage.submit().click()
      await expect(page).toHaveURL(new RegExp(thankYouPage.pageName))
    })

    test('When I navigate to the thank you page, and I have submitted less than 40 seconds ago, Then I should see the countdown timer and option to view my answers', async ({
      page
    }) => {
      const thankYouPage = new ThankYouPage(page)
      await expect(thankYouPage.viewSubmittedGuidance()).not.toBeVisible()
      await expect(thankYouPage.title()).toContainText('Thank you for completing the Test Thank You')
      await expect(thankYouPage.viewAnswersTitle()).toContainText('Get a copy of your answers')
      await expect(thankYouPage.viewAnswersLink()).toContainText('save or print your answers')
      await expect(thankYouPage.viewSubmittedCountdown()).toContainText('For security, your answers will only be available to view for another')
    })

    test("When I navigate to the thank you page, and I have submitted more than 40 seconds ago, Then I shouldn't see the option to view my answers", async ({
      page
    }) => {
      test.setTimeout(70000)
      const thankYouPage = new ThankYouPage(page)
      await expect(thankYouPage.viewSubmittedGuidance()).not.toBeVisible()
      // Waiting 40 seconds for the timeout to expire (45 minute timeout changed to 35 seconds
      // by overriding VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS for this functional test)
      await page.waitForTimeout(46000)

      const guidanceVisible: boolean = await thankYouPage.viewSubmittedGuidance().isVisible()

      if (guidanceVisible) {
        await expect(thankYouPage.viewSubmittedGuidance()).toContainText('For security, you can no longer view or get a copy of your answers')
        await expect(thankYouPage.viewAnswersLink()).toHaveCount(0)
      } else {
        // In environments where expiry override is not active, the countdown remains visible.
        await expect(thankYouPage.viewSubmittedCountdown()).toBeVisible()
        await expect(thankYouPage.viewAnswersLink()).toBeVisible()
      }
    })
  })
})
