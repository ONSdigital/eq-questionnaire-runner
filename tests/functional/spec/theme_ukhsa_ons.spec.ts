import { test, expect } from '../fixtures/test'
import RadioPage from '../generated_pages/theme_dbt_ni/radio.page'

test.describe('Theme UKHSA-ONS', () => {
  test.describe('Given I launch a UKHSA-ONS themed questionnaire', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_theme_ukhsa_ons.json')
    })

    test('When I navigate to the radio page, Then I should see UKHSA-ONS theme content', async ({ page }) => {
      const radioPage = new RadioPage(page)
      await expect(page).toHaveURL(new RegExp(radioPage.pageName))
      await expect(page.locator('#ons-logo-stacked-en-alt').first()).toContainText('Office for National Statistics')
      await expect(page.locator('#ukhsa-logo-alt').first()).toContainText('UK Health Security Agency')
    })
  })
})
