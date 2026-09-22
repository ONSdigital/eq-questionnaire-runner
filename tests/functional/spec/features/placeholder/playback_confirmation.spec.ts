import { test, expect } from '../../../fixtures/test'
import MandatoryCheckboxPage from '../../../generated_pages/placeholder_playback_list/mandatory-checkbox.page'

test.describe('Feature: Playback Confirmation', () => {
  test.beforeEach('Open the schema', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_placeholder_playback_list.json')
  })

  test('When the user submits an answer, their answers should be shown on the confirmation screen', async ({ page }) => {
    const mandatoryCheckboxPage = new MandatoryCheckboxPage(page)
    await mandatoryCheckboxPage.cheese().click()
    await mandatoryCheckboxPage.ham().click()
    await mandatoryCheckboxPage.submit().click()

    await expect(page.locator('#confirm-answers-question').locator('li')).toContainText(['Cheese', 'Ham'])
  })
})
