import { test, expect } from '../fixtures/test'
import RadioPage from '../generated_pages/theme_desnz_ni/radio.page'

test.describe('Theme DESNZ-NI', () => {
  test.describe('Given I launch a DESNZ-NI themed questionnaire', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_theme_desnz_ni.json')
    })

    test('When I navigate to the radio page, Then I should see DESNZ-NI theme content', async ({ page }) => {
      const radioPage = new RadioPage(page)
      await expect(page).toHaveURL(new RegExp(radioPage.pageName))
      await expect(page.locator('#desnz-logo-alt').first()).toContainText('Department for Energy Security and Net Zero')
      await expect(page.locator('#finance-ni-logo-alt').first()).toContainText('Northern Ireland Department of Finance logo')
    })
  })
})
