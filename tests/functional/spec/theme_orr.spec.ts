import { test, expect } from '../fixtures/test'
import RadioPage from '../generated_pages/theme_orr/radio.page'

test.describe('Theme Rail and Road', () => {
  test.describe('Given I launch a Rail and Road themed questionnaire', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_theme_orr.json')
    })

    test('When I navigate to the radio page, Then I should see Rail and Road theme content', async ({ page }) => {
      const radioPage = new RadioPage(page)
      await expect(page).toHaveURL(new RegExp(radioPage.pageName))
      await expect(page.locator('#orr-logo-mobile-alt').first()).toContainText('Office of Rail and Road logo')
    })
  })
})
