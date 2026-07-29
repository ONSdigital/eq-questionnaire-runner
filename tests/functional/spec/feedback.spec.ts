import { test, expect } from '../fixtures/test'
import SchemaFeedbackPage from '../generated_pages/feedback/feedback.page'
import SubmitPage from '../generated_pages/feedback/submit.page'
import FeedbackPage from '../base_pages/feedback.page'
import FeedbackSentPage from '../base_pages/feedback-sent.page'
import ThankYouPage from '../base_pages/thank-you.page'
import { verifyUrlContains } from '../helpers'

test.describe('Feedback', () => {
  test.describe('Given I launch and complete the test feedback survey', () => {
    test.beforeEach(async ({ page, openQuestionnaire }) => {
      const schemaFeedbackPage = new SchemaFeedbackPage(page)
      const submitPage = new SubmitPage(page)
      await openQuestionnaire('test_feedback.json')
      await schemaFeedbackPage.submit().click()
      await submitPage.submit().click()
    })

    test('When I view the thank you page, Then I can see the feedback call to action', async ({ page }) => {
      const thankYouPage = new ThankYouPage(page)
      await verifyUrlContains(page, thankYouPage.pageName)
      await expect(thankYouPage.feedback()).toContainText('What do you think about this service?')
      await expect(thankYouPage.feedbackLink()).toHaveText('Give feedback')
      await expect(thankYouPage.feedbackLink()).toHaveAttribute('href', /\/submitted\/feedback\/send/)
    })

    test('When I try to submit without providing feedback, then I stay on the feedback page and get an error message', async ({ page }) => {
      const feedbackPage = new FeedbackPage(page)
      await page.goto(feedbackPage.url())
      await verifyUrlContains(page, feedbackPage.pageName)
      await expect(feedbackPage.feedbackTitle()).toHaveText('Give feedback about this service')
      await feedbackPage.submit().click()
      await verifyUrlContains(page, feedbackPage.pageName)
      await expect(feedbackPage.errorPanel()).toBeVisible()
      await expect(feedbackPage.errorHeader()).toHaveText('There are 2 problems with your feedback')
      await expect(feedbackPage.errorNumber(1)).toHaveText('Select what your feedback is about')
      await expect(feedbackPage.errorNumber(2)).toHaveText('Enter your feedback')
    })

    test('When I enter valid feedback, Then I can submit the feedback page and get confirmation that the feedback has been sent', async ({ page }) => {
      const feedbackPage = new FeedbackPage(page)
      const feedbackSentPage = new FeedbackSentPage(page)
      await page.goto(feedbackPage.url())
      await feedbackPage.feedbackTypeGeneralFeedback().click()
      await feedbackPage.feedbackText().fill('Well done!')
      await feedbackPage.submit().click()
      await verifyUrlContains(page, feedbackSentPage.pageName)
      await expect(feedbackSentPage.feedbackThankYouText()).toHaveText('Thank you for your feedback')
    })

    test('When I click the done button on the feedback sent page, Then I am taken to the thank you page', async ({ page }) => {
      const feedbackPage = new FeedbackPage(page)
      const feedbackSentPage = new FeedbackSentPage(page)
      const thankYouPage = new ThankYouPage(page)
      await page.goto(feedbackPage.url())
      await feedbackPage.feedbackTypeGeneralFeedback().click()
      await feedbackPage.feedbackText().fill('Well done!')
      await feedbackPage.submit().click()
      await feedbackSentPage.doneButton().click()
      await verifyUrlContains(page, 'thank-you')
      await expect(thankYouPage.title()).toHaveText('Thank you for completing the Test Feedback')
    })
  })
})
