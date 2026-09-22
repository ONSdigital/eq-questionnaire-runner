import { test, expect } from '../../fixtures/test'
import { checkItemsInList } from '../../helpers'
import HubPage from '../../base_pages/hub.page'
import AnyoneUsuallyLiveAtPage from '../../generated_pages/list_collector_driving_question/anyone-usually-live-at.page'
import AnyoneElseLiveAtListCollectorPage from '../../generated_pages/list_collector_driving_question/anyone-else-live-at.page'
import AnyoneElseLiveAtListCollectorAddPage from '../../generated_pages/list_collector_driving_question/anyone-else-live-at-add.page'
import AnyoneElseLiveAtListCollectorRemovePage from '../../generated_pages/list_collector_driving_question/anyone-else-live-at-remove.page'
import SectionSummaryPage from '../../generated_pages/list_collector_driving_question/section-summary.page'

test.describe('List Collector Driving Question', () => {
  test.beforeEach('Load the survey', async ({ page, openQuestionnaire }) => {
    const hubPage = new HubPage(page)
    await openQuestionnaire('test_list_collector_driving_question.json')
    await hubPage.submit().click()
  })

  test.describe('Given a happy journey through the list collector', () => {
    test('The collector shows all of the household members in the summary', async ({ page }) => {
      const anyoneElseLiveAtListCollectorAddPage = new AnyoneElseLiveAtListCollectorAddPage(page)
      const anyoneElseLiveAtListCollectorPage = new AnyoneElseLiveAtListCollectorPage(page)
      const anyoneUsuallyLiveAtPage = new AnyoneUsuallyLiveAtPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      await anyoneUsuallyLiveAtPage.yes().click()
      await anyoneUsuallyLiveAtPage.submit().click()
      await anyoneElseLiveAtListCollectorAddPage.firstName().fill('Marcus')
      await anyoneElseLiveAtListCollectorAddPage.lastName().fill('Twin')
      await anyoneElseLiveAtListCollectorAddPage.submit().click()
      await anyoneElseLiveAtListCollectorPage.yes().click()
      await anyoneElseLiveAtListCollectorPage.submit().click()
      await anyoneElseLiveAtListCollectorAddPage.firstName().fill('Suzy')
      await anyoneElseLiveAtListCollectorAddPage.lastName().fill('Clemens')
      await anyoneElseLiveAtListCollectorAddPage.submit().click()
      await anyoneElseLiveAtListCollectorPage.no().click()
      await anyoneElseLiveAtListCollectorPage.submit().click()

      const peopleExpected = ['Marcus Twin', 'Suzy Clemens']

      await checkItemsInList(peopleExpected, (index) => sectionSummaryPage.peopleListLabel(index))
    })
  })

  test.describe('Given the user answers no to the driving question', () => {
    test('The summary add link returns to the driving question', async ({ page }) => {
      const anyoneUsuallyLiveAtPage = new AnyoneUsuallyLiveAtPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      await anyoneUsuallyLiveAtPage.no().click()
      await anyoneUsuallyLiveAtPage.submit().click()
      await sectionSummaryPage.peopleListAddLink().click()
      await expect(page).toHaveURL(new RegExp(anyoneUsuallyLiveAtPage.url()))
    })
  })

  test.describe('Given the user answers yes to the driving question, adds someone and later removes them', () => {
    test('The summary add link should return to the original list collector', async ({ page }) => {
      const anyoneElseLiveAtListCollectorAddPage = new AnyoneElseLiveAtListCollectorAddPage(page)
      const anyoneElseLiveAtListCollectorPage = new AnyoneElseLiveAtListCollectorPage(page)
      const anyoneElseLiveAtListCollectorRemovePage = new AnyoneElseLiveAtListCollectorRemovePage(page)
      const anyoneUsuallyLiveAtPage = new AnyoneUsuallyLiveAtPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      await anyoneUsuallyLiveAtPage.yes().click()
      await anyoneUsuallyLiveAtPage.submit().click()
      await anyoneElseLiveAtListCollectorAddPage.firstName().fill('Marcus')
      await anyoneElseLiveAtListCollectorAddPage.lastName().fill('Twin')
      await anyoneElseLiveAtListCollectorAddPage.submit().click()
      await anyoneElseLiveAtListCollectorPage.no().click()
      await anyoneElseLiveAtListCollectorPage.submit().click()
      await sectionSummaryPage.peopleListRemoveLink(1).click()
      await anyoneElseLiveAtListCollectorRemovePage.yes().click()
      await anyoneElseLiveAtListCollectorRemovePage.submit().click()
      await sectionSummaryPage.peopleListAddLink().click()
      await expect(page).toHaveURL(new RegExp(anyoneElseLiveAtListCollectorAddPage.pageName))
    })
  })
})
