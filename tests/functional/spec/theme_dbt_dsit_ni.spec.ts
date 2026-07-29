import { test, expect } from '../fixtures/test'
import RadioPage from '../generated_pages/theme_dbt_dsit_ni/radio.page'

test.describe('Theme DBT-DSIT-NI', () => {
  test.describe('Given I launch a DBT-DSIT-NI themed questionnaire', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_theme_dbt_dsit_ni.json')
    })

    test('When I navigate to the radio page, Then I should see DBT-DSIT-NI theme content', async ({ page }) => {
      const radioPage = new RadioPage(page)
      await expect(page).toHaveURL(new RegExp(radioPage.pageName))
      await expect(page.locator('#dbt-logo-alt').first()).toContainText('Department for Business and Trade logo')
      await expect(page.locator('#dsit-logo-alt').first()).toContainText('Department for Science, Innovation and Technology logo')
      await expect(page.locator('#finance-ni-logo-alt').first()).toContainText('Northern Ireland Department of Finance logo')
    })
  })
})
