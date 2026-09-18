import { test, expect } from '../fixtures/test'
import RadioPage from '../generated_pages/theme_northernireland/radio.page'

test.describe('Theme Northern Ireland', () => {
  test.describe('Given I launch a Northern Ireland themed questionnaire', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_theme_northernireland.json')
    })

    test('When I navigate to the radio page, Then I should see Northern Ireland theme content', async ({ page }) => {
      const radioPage = new RadioPage(page)
      await expect(page).toHaveURL(new RegExp(radioPage.pageName))
      await expect(page.locator('#finance-ni-logo-alt').first()).toContainText('Northern Ireland Department of Finance logo')
    })
  })
})
