import { test, expect } from '../../../fixtures/test'
import CountryCheckboxPage from '../../../generated_pages/routing_not/country-checkbox.page'
import CountryInterstitialPage from '../../../generated_pages/routing_not/country-interstitial-not-india.page'
import IndiaInterstitialPage from '../../../generated_pages/routing_not/country-interstitial-india.page'

test.describe('Feature: Routing - Not Operator', () => {
  test.describe('Equals', () => {
    test.describe('Given I start the not operator routing survey', () => {
      test.beforeEach(async ({ openQuestionnaire }) => {
        await openQuestionnaire('test_routing_not.json')
      })

      test('When I do not select India, Then I should be routed to the not India interstitial page', async ({ page }) => {
        const countryCheckboxPage = new CountryCheckboxPage(page)
        const countryInterstitialPage = new CountryInterstitialPage(page)
        await countryCheckboxPage.azerbaijan().click()
        await countryCheckboxPage.submit().click()
        await expect(page).toHaveURL(new RegExp(countryInterstitialPage.pageName))
      })

      test('When I select India, Then I should be routed to the India interstitial page', async ({ page }) => {
        const countryCheckboxPage = new CountryCheckboxPage(page)
        const indiaInterstitialPage = new IndiaInterstitialPage(page)
        await countryCheckboxPage.india().click()
        await countryCheckboxPage.submit().click()
        await expect(page).toHaveURL(new RegExp(indiaInterstitialPage.pageName))
      })
    })
  })
})
