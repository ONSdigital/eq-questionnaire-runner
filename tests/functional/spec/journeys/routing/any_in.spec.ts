import { test, expect } from '../../../fixtures/test'
import CountryCheckboxPage from '../../../generated_pages/routing_checkbox_contains_any/country-checkbox.page'
import CountryInterstitialPage from '../../../generated_pages/routing_checkbox_contains_any/country-interstitial-india-or-malta-or-both.page'
import CountryInterstitialOtherPage from '../../../generated_pages/routing_checkbox_contains_any/country-interstitial-not-india-or-malta-or-both.page'

test.describe('Feature: Routing - ANY-IN Operator', () => {
  test.describe('Equals', () => {
    test.describe('Given I start the ANY-IN operator routing survey', () => {
      test.beforeEach(async ({ openQuestionnaire }) => {
        await openQuestionnaire('test_routing_checkbox_contains_any.json')
      })

      test('When I do select India and Malta, Then I should be routed to the correct answer interstitial page', async ({ page }) => {
        const countryCheckboxPage = new CountryCheckboxPage(page)
        const countryInterstitialPage = new CountryInterstitialPage(page)
        await countryCheckboxPage.india().click()
        await countryCheckboxPage.malta().click()
        await countryCheckboxPage.submit().click()
        await expect(page).toHaveURL(new RegExp(countryInterstitialPage.pageName))
      })

      test('When I do select India or Malta, Then I should be routed to the correct answer interstitial page', async ({ page }) => {
        const countryCheckboxPage = new CountryCheckboxPage(page)
        const countryInterstitialPage = new CountryInterstitialPage(page)
        await countryCheckboxPage.india().click()
        await countryCheckboxPage.submit().click()
        await expect(page).toHaveURL(new RegExp(countryInterstitialPage.pageName))
      })

      test('When I do not select India or Malta, Then I should be routed to the incorrect answer interstitial page', async ({ page }) => {
        const countryCheckboxPage = new CountryCheckboxPage(page)
        const countryInterstitialOtherPage = new CountryInterstitialOtherPage(page)
        await countryCheckboxPage.liechtenstein().click()
        await countryCheckboxPage.submit().click()
        await expect(page).toHaveURL(new RegExp(countryInterstitialOtherPage.pageName))
      })
    })
  })
})
