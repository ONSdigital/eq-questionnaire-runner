import { test, expect } from '../../../fixtures/test'
import InitialChoicePage from '../../../generated_pages/routing_not_affected_by_answers_not_on_path/initial-choice.page'
import InvalidPathPage from '../../../generated_pages/routing_not_affected_by_answers_not_on_path/invalid-path.page'
import InvalidPathInterstitialPage from '../../../generated_pages/routing_not_affected_by_answers_not_on_path/invalid-path-interstitial.page'
import ValidPathPage from '../../../generated_pages/routing_not_affected_by_answers_not_on_path/valid-path.page'
import ValidFinalInterstitialPage from '../../../generated_pages/routing_not_affected_by_answers_not_on_path/valid-final-interstitial.page'

test.describe('Answers not on path are not considered when routing', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_routing_not_affected_by_answers_not_on_path.json')
  })

  test('Given the user enters an answer on the first path, When they return to the second path, They should be routed to the valid path interstitial', async ({
    page
  }) => {
    const initialChoicePage = new InitialChoicePage(page)
    const invalidPathInterstitialPage = new InvalidPathInterstitialPage(page)
    const invalidPathPage = new InvalidPathPage(page)
    const validFinalInterstitialPage = new ValidFinalInterstitialPage(page)
    const validPathPage = new ValidPathPage(page)
    await initialChoicePage.goHereFirst().click()
    await initialChoicePage.submit().click()

    await expect(page).toHaveURL(new RegExp(invalidPathPage.pageName))
    await invalidPathPage.answer().fill('123')
    await invalidPathPage.submit().click()

    // We now have an answer in the store on the 'invalid' path

    await expect(page).toHaveURL(new RegExp(invalidPathInterstitialPage.pageName))
    await invalidPathInterstitialPage.previous().click()
    await invalidPathPage.previous().click()

    // Take the second route

    await initialChoicePage.goHereSecond().click()
    await initialChoicePage.submit().click()

    await validPathPage.answer().fill('321')
    await validPathPage.submit().click()

    // We should be routed to the valid interstitial page since the invalid path answer should not be considered whilst routing.
    await expect(page).toHaveURL(new RegExp(validFinalInterstitialPage.pageName))
  })
})
