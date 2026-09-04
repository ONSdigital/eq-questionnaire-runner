import { test, expect } from '../../../fixtures/test'
import ListCollectorPage from '../../../generated_pages/placeholder_based_on_first_item_in_list/list-collector.page'
import ListCollectorAddPage from '../../../generated_pages/placeholder_based_on_first_item_in_list/list-collector-add.page'
import ListStatusInterstitial from '../../../generated_pages/placeholder_based_on_first_item_in_list/list-status.page'
import FavouriteDrinkQuestion from '../../../generated_pages/placeholder_based_on_first_item_in_list/favourite-drink.page'
import ListStatusQuestion from '../../../generated_pages/placeholder_based_on_first_item_in_list/list-status-2.page'
import SummaryPage from '../../../generated_pages/placeholder_based_on_first_item_in_list/personal-details-section-summary.page'
import HubPage from '../../../base_pages/hub.page'

test.describe('Component: Definition', () => {
  test.describe('Load the Survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_placeholder_based_on_first_item_in_list.json')
    })

    test('Given I am the first person in the list, When I get to the question page, Then I should see the default answer option', async ({ page }) => {
      const favouriteDrinkQuestion = new FavouriteDrinkQuestion(page)
      const hubPage = new HubPage(page)
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const listStatusInterstitial = new ListStatusInterstitial(page)
      const listStatusQuestion = new ListStatusQuestion(page)
      await hubPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Marcus')
      await listCollectorAddPage.lastName().fill('Twin')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await hubPage.submit().click()

      await listStatusInterstitial.submit().click()
      await favouriteDrinkQuestion.answer().fill('Orange Juice')
      await favouriteDrinkQuestion.submit().click()

      await expect(listStatusQuestion.listStatus2TeaLabel()).toHaveText('Tea')
    })

    test('Given I am not the first person in the list, When I get to the question page, Then I should see the correct answer option', async ({ page }) => {
      const favouriteDrinkQuestion = new FavouriteDrinkQuestion(page)
      const hubPage = new HubPage(page)
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const listStatusInterstitial = new ListStatusInterstitial(page)
      const listStatusQuestion = new ListStatusQuestion(page)
      const summaryPage = new SummaryPage(page)
      await hubPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Marcus')
      await listCollectorAddPage.lastName().fill('Twin')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('John')
      await listCollectorAddPage.lastName().fill('Doe')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await hubPage.submit().click()

      await listStatusInterstitial.submit().click()
      await favouriteDrinkQuestion.answer().fill('Orange Juice')
      await favouriteDrinkQuestion.submit().click()
      await listStatusQuestion.listStatus2Tea().click()
      await listStatusQuestion.submit().click()
      await summaryPage.submit().click()
      await hubPage.submit().click()
      await listStatusInterstitial.submit().click()
      await favouriteDrinkQuestion.answer().fill('Lemonade')
      await favouriteDrinkQuestion.submit().click()

      await expect(listStatusQuestion.listStatus2TeaLabel()).toHaveText('Orange Juice')
    })
  })
})
