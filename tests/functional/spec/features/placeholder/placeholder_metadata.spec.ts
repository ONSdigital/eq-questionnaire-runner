import { test, expect } from '../../../fixtures/test'
import MandatoryRadioPage from '../../../generated_pages/placeholder_metadata/mandatory-radio.page'
import SubmitPage from '../../../generated_pages/placeholder_metadata/submit.page'

test.describe('Placeholder metadata check', () => {
  test.describe('Given I launch placeholder metadata question', () => {
    test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_placeholder_metadata.json')
    })

    test('When I see responding unit question, Then I see radio options with first option as metadata placeholder (ru_name)', async ({ page }) => {
      const mandatoryRadioPage = new MandatoryRadioPage(page)
      await expect(mandatoryRadioPage.answerRuNameLabel()).toHaveText('Apple')
    })

    test('When I answer responding unit question, Then I see confirmation page with my selected placeholder metadata option (ru_name)', async ({ page }) => {
      const mandatoryRadioPage = new MandatoryRadioPage(page)
      const submitPage = new SubmitPage(page)
      await mandatoryRadioPage.answerRuName().click()
      await mandatoryRadioPage.submit().click()

      await expect(submitPage.mandatoryRadioAnswer()).toHaveText('Apple')
      await expect(submitPage.guidance()).toHaveText('Please submit this survey to complete it')
    })
  })
})
