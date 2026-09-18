import TimeoutInterstitialPage from '../../../generated_pages/timeout_modal/timeout-modal-interstitial.page'
import TimeoutSubmitPage from '../../../generated_pages/timeout_modal/submit.page'
import { test } from '../../../fixtures/test'
import { TimeoutModalTestCase } from '../timeout_modal'

test.describe('Timeout Modal Post Submission Extended', () => {
  test.beforeEach(async ({ page, openQuestionnaire }) => {
    const timeoutInterstitialPage = new TimeoutInterstitialPage(page)
    const timeoutSubmitPage = new TimeoutSubmitPage(page)
    await openQuestionnaire('test_timeout_modal.json')
    await timeoutInterstitialPage.submit().click()
    await timeoutSubmitPage.submit().click()
  })

  TimeoutModalTestCase.testCaseExtended('thank-you')
})
