import { test, expect } from '../../../fixtures/test'
import CountryCheckboxPage from '../../../generated_pages/routing_checkbox_contains_in/country-checkbox.page'
import CountryInterstitialPage from '../../../generated_pages/routing_checkbox_contains_in/country-interstitial-india.page'
import CountryInterstitialOtherPage from '../../../generated_pages/routing_checkbox_contains_in/country-interstitial-not-india.page'

test.describe('Feature: Routing - IN Operator', () => {
  test.describe('Equals', () => {
    test.describe('Given I start the IN operator routing survey', () => {
      test.beforeEach(async ({ openQuestionnaire }) => {
        await openQuestionnaire('test_routing_checkbox_contains_in.json')
      })

      test('When I do select India, Then I should be routed to the the correct answer interstitial page', async ({ page }) => {
        const countryCheckboxPage = new CountryCheckboxPage(page)
        const countryInterstitialPage = new CountryInterstitialPage(page)
        await countryCheckboxPage.india().click()
        await countryCheckboxPage.submit().click()
        await expect(page).toHaveURL(new RegExp(countryInterstitialPage.pageName))
      })

      test('When I do not select India, Then I should be routed to the the incorrect answer interstitial page', async ({ page }) => {
        const countryCheckboxPage = new CountryCheckboxPage(page)
        const countryInterstitialOtherPage = new CountryInterstitialOtherPage(page)
        await countryCheckboxPage.liechtenstein().click()
        await countryCheckboxPage.submit().click()
        await expect(page).toHaveURL(new RegExp(countryInterstitialOtherPage.pageName))
      })
    })
  })
})
