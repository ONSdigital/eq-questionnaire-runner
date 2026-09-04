import { test, expect } from '../fixtures/test'
import InterstitialDefinitionPage from '../generated_pages/interstitial_definition/interstitial-definition.page'

test.describe('Component: Interstitial Definition', () => {
  test.describe('Given I launch the interstitial definition questionnaire', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_interstitial_definition.json')
    })

    test('When there is a definition on an interstitial, then the page is displayed correctly', async ({ page }) => {
      const interstitialDefinitionPage = new InterstitialDefinitionPage(page)
      await expect(interstitialDefinitionPage.definitionTitle()).toBeVisible()
      await expect(interstitialDefinitionPage.definitionContent()).toHaveAttribute('aria-hidden', 'true')
    })

    test('When I click on a definition title, the content is displayed for just that definition', async ({ page }) => {
      const interstitialDefinitionPage = new InterstitialDefinitionPage(page)
      await interstitialDefinitionPage.definitionTitle().click()

      await expect(interstitialDefinitionPage.definitionTitle()).toBeVisible()
      await expect(interstitialDefinitionPage.definitionContent()).toHaveAttribute('aria-hidden', 'false')
      await expect(interstitialDefinitionPage.definitionContent()).toHaveText('In a way that accomplishes a desired aim or result')
    })
  })
})
