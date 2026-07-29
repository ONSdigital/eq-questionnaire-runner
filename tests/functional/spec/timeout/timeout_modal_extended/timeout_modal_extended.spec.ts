import { test } from '../../../fixtures/test'
import { TimeoutModalTestCase } from '../timeout_modal'

test.describe('Timeout Modal Extended', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_timeout_modal.json')
  })

  TimeoutModalTestCase.testCaseExtended('timeout-modal-interstitial')
})
