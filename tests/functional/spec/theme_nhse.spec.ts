import { test, expect } from '../fixtures/test'
import RadioPage from '../generated_pages/theme_ons_nhs/radio.page'

test.describe('Theme NHSE', () => {
  test.describe('Given I launch a NHSE themed questionnaire', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_theme_ons_nhs.json')
    })

    test('When I navigate to the radio page, Then I should see NHSE theme content', async ({ page }) => {
      const radioPage = new RadioPage(page)
      await expect(page).toHaveURL(new RegExp(radioPage.pageName))
      await expect(page.locator('#ons-logo-stacked-en-alt').first()).toContainText('Office for National Statistics')
      await expect(page.locator('#nhs-logo-alt').first()).toContainText('National Heath Service')
    })
  })
})
