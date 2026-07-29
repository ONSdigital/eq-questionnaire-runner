import { test, expect } from '../../../fixtures/test'
import FoodPage from '../../../generated_pages/skip_condition_set/food-block.page'
import DrinkPage from '../../../generated_pages/skip_condition_set/drink-block.page'
import SubmitPage from '../../../generated_pages/skip_condition_set/submit.page'

test.describe('Skip Conditions - Set', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_skip_condition_set.json')
  })

  test('Given I complete the first page, Then I should see the summary page', async ({ page }) => {
    const foodPage = new FoodPage(page)
    const submitPage = new SubmitPage(page)
    await foodPage.bacon().click()
    await foodPage.submit().click()
    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
  })

  test('Given I do not complete the first page, Then I should see the drink page', async ({ page }) => {
    const drinkPage = new DrinkPage(page)
    const foodPage = new FoodPage(page)
    await foodPage.submit().click()
    await expect(page).toHaveURL(new RegExp(drinkPage.pageName))
  })
})
