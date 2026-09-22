import { test, expect } from '../../../fixtures/test'
import CountryCheckboxPage from '../../../generated_pages/routing_checkbox_contains_all/country-checkbox.page'
import CountryInterstitialPage from '../../../generated_pages/routing_checkbox_contains_all/country-interstitial-india-and-malta.page'
import CountryInterstitialOtherPage from '../../../generated_pages/routing_checkbox_contains_all/country-interstitial-not-india-and-malta.page'

test.describe('Feature: Routing - ALL-IN Operator', () => {
  test.describe('Equals', () => {
    test.describe('Given I start the ALL-IN operator routing survey', () => {
      test.beforeEach(async ({ openQuestionnaire }) => {
        await openQuestionnaire('test_routing_checkbox_contains_all.json')
      })

      test('When I do select India and Malta, Then I should be routed to the correct answer interstitial page', async ({ page }) => {
        const countryCheckboxPage = new CountryCheckboxPage(page)
        const countryInterstitialPage = new CountryInterstitialPage(page)
        await countryCheckboxPage.india().click()
        await countryCheckboxPage.malta().click()
        await countryCheckboxPage.submit().click()
        await expect(page).toHaveURL(new RegExp(countryInterstitialPage.pageName))
      })

      test('When I do select India only, Then I should be routed to the correct answer interstitial page', async ({ page }) => {
        const countryCheckboxPage = new CountryCheckboxPage(page)
        const countryInterstitialOtherPage = new CountryInterstitialOtherPage(page)
        await countryCheckboxPage.india().click()
        await countryCheckboxPage.submit().click()
        await expect(page).toHaveURL(new RegExp(countryInterstitialOtherPage.pageName))
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
