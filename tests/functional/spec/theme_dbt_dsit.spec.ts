import { test, expect } from '../fixtures/test'
import RadioPage from '../generated_pages/theme_dbt_dsit/radio.page'

test.describe('Theme DBT-DSIT', () => {
  test.describe('Given I launch a DBT-DSIT themed questionnaire', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_theme_dbt_dsit.json')
    })

    test('When I navigate to the radio page, Then I should see DBT-DSIT theme content', async ({ page }) => {
      const radioPage = new RadioPage(page)
      await expect(page).toHaveURL(new RegExp(radioPage.pageName))
      await expect(page.locator('#dbt-logo-alt').first()).toContainText('Department for Business and Trade logo')
      await expect(page.locator('#dsit-logo-alt').first()).toContainText('Department for Science, Innovation and Technology logo')
    })
  })
})
