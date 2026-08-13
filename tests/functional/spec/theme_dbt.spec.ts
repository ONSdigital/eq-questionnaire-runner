import { test, expect } from '../fixtures/test'
import RadioPage from '../generated_pages/theme_dbt/radio.page'

test.describe('Theme DBT', () => {
  test.describe('Given I launch a DBT themed questionnaire', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_theme_dbt.json')
    })

    test('When I navigate to the radio page, Then I should see DBT theme content', async ({ page }) => {
      const radioPage = new RadioPage(page)
      await expect(page).toHaveURL(new RegExp(radioPage.pageName))
      await expect(page.locator('#dbt-logo-alt').first()).toContainText('Department for Business and Trade')
    })
  })
})
