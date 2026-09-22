import { test, expect } from '../../../fixtures/test'
import ListCollectorPage from '../../../generated_pages/skip_condition_list/list-collector.page'
import ListCollectorAddPage from '../../../generated_pages/skip_condition_list/list-collector-add.page'
import LessThanTwoInterstitialPage from '../../../generated_pages/skip_condition_list/less-than-two-interstitial.page'
import TwoInterstitialPage from '../../../generated_pages/skip_condition_list/two-interstitial.page'
import MoreThanTwoInterstitialPage from '../../../generated_pages/skip_condition_list/more-than-two-interstitial.page'

test.describe('Feature: Routing on lists', () => {
  test.describe('Given I start skip condition list survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_skip_condition_list.json')
    })

    test("When I don't add a person to the list, Then the less than two people skippable page should be shown", async ({ page }) => {
      const lessThanTwoInterstitialPage = new LessThanTwoInterstitialPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await expect(page).toHaveURL(new RegExp(lessThanTwoInterstitialPage.pageName))
    })

    test('When I add one person to the list, Then the less than two people skippable page should be shown', async ({ page }) => {
      const lessThanTwoInterstitialPage = new LessThanTwoInterstitialPage(page)
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Marcus')
      await listCollectorAddPage.lastName().fill('Twin')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await expect(page).toHaveURL(new RegExp(lessThanTwoInterstitialPage.pageName))
    })

    test('When I add two people to the list, Then the two people skippable page should be shown', async ({ page }) => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const twoInterstitialPage = new TwoInterstitialPage(page)
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Marcus')
      await listCollectorAddPage.lastName().fill('Twin')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Samuel')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await expect(page).toHaveURL(new RegExp(twoInterstitialPage.pageName))
    })

    test('When I add three people to the list, Then the more than two people skippable page should be shown', async ({ page }) => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const moreThanTwoInterstitialPage = new MoreThanTwoInterstitialPage(page)
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Marcus')
      await listCollectorAddPage.lastName().fill('Twin')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Samuel')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Olivia')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await expect(page).toHaveURL(new RegExp(moreThanTwoInterstitialPage.pageName))
    })
  })
})
