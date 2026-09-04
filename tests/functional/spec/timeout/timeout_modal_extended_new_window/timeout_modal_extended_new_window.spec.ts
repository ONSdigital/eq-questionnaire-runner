import { test } from '../../../fixtures/test'
import { TimeoutModalTestCase } from '../timeout_modal'

test.describe('Timeout Modal Extended New Window', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_timeout_modal.json')
  })

  TimeoutModalTestCase.testCaseExtendedNewWindow('timeout-modal-interstitial')
})
