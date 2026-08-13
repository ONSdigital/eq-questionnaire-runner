import { test, expect } from '../fixtures/test'
import IntroductionPage from '../generated_pages/introduction/introduction.page'

test.describe('My Account header link', () => {
  test('Given I start a survey, When I visit a page then I should not see the My account button', async ({ page, openQuestionnaire }) => {
    const introductionPage = new IntroductionPage(page)
    await openQuestionnaire('test_introduction.json')
    await page.waitForTimeout(100)
    await expect(page).toHaveURL(/introduction/)
    await expect(introductionPage.myAccountLink()).not.toBeVisible()
  })
})
