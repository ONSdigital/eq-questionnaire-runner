import { createOpenQuestionnaire, test, expect } from '../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../fixtures/test'
import { checkItemsInList } from '../../helpers'
import HubPage from '../../base_pages/hub.page'
import PrimaryPersonListCollectorPage from '../../generated_pages/list_collector_driving_checkbox/primary-person-list-collector.page'
import PrimaryPersonListCollectorAddPage from '../../generated_pages/list_collector_driving_checkbox/primary-person-list-collector-add.page'
import AnyoneUsuallyLiveAtPage from '../../generated_pages/list_collector_driving_checkbox/anyone-usually-live-at.page'
import ListCollectorAddPage from '../../generated_pages/list_collector_driving_checkbox/list-collector-add.page'
import ListCollectorPage from '../../generated_pages/list_collector_driving_checkbox/list-collector.page'
import ListCollectorTemporaryAwayPage from '../../generated_pages/list_collector_driving_checkbox/list-collector-temporary-away-stay.page'
import ListCollectorTemporaryAwayAddPage from '../../generated_pages/list_collector_driving_checkbox/list-collector-temporary-away-stay-add.page'
import SummaryPage from '../../generated_pages/list_collector_driving_checkbox/section-summary.page'

test.describe('List Collector Driving Checkbox Question', () => {
  test.describe.configure({ mode: 'serial' })

  let context: BrowserContext
  let page: Page
  let openQuestionnaire: OpenQuestionnaire

  test.beforeAll('Load the survey', async ({ browser }) => {
    context = await browser.newContext()
    page = await context.newPage()
    openQuestionnaire = createOpenQuestionnaire(page)
    const hubPage = new HubPage(page)
    await openQuestionnaire('test_list_collector_driving_checkbox.json')
    await hubPage.submit().click()
  })

  test.afterAll(async () => {
    await context.close()
  })

  test.describe('Given a happy journey through the list collectors', () => {
    test('All of the household members and visitors are shown in the summary', async () => {
      const anyoneUsuallyLiveAtPage = new AnyoneUsuallyLiveAtPage(page)
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const listCollectorTemporaryAwayPage = new ListCollectorTemporaryAwayPage(page)
      const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      const summaryPage = new SummaryPage(page)
      await primaryPersonListCollectorPage.yesIUsuallyLiveHere().click()
      await primaryPersonListCollectorPage.submit().click()
      await primaryPersonListCollectorAddPage.firstName().fill('Marcus')
      await primaryPersonListCollectorAddPage.lastName().fill('Twin')
      await primaryPersonListCollectorAddPage.submit().click()
      await anyoneUsuallyLiveAtPage.familyMembersAndPartners().click()
      await anyoneUsuallyLiveAtPage.submit().click()
      await listCollectorAddPage.firstName().fill('Suzy')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.noIDoNotNeedToAddAPerson().click()
      await listCollectorPage.submit().click()
      await listCollectorTemporaryAwayPage.noThereAreNumberOfPeoplePeopleLivingHere().click()
      await listCollectorTemporaryAwayPage.submit().click()

      const householdMembersExpected = ['Marcus Twin (You)', 'Suzy Clemens']
      await checkItemsInList(householdMembersExpected, (index) => summaryPage.peopleListLabel(index))
    })
  })

  test.describe('Given the primary person is removed', () => {
    test("Then they aren't shown on the summary screen", async () => {
      const anyoneUsuallyLiveAtPage = new AnyoneUsuallyLiveAtPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const listCollectorTemporaryAwayPage = new ListCollectorTemporaryAwayPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      const summaryPage = new SummaryPage(page)
      await summaryPage.previous().click()
      await listCollectorTemporaryAwayPage.previous().click()
      await listCollectorPage.previous().click()
      await anyoneUsuallyLiveAtPage.previous().click()
      await primaryPersonListCollectorPage.noIDonTUsuallyLiveHere().click()
      await primaryPersonListCollectorPage.submit().click()

      const householdMembersExpected = ['Suzy Clemens']
      await checkItemsInList(householdMembersExpected, (index) => summaryPage.peopleListLabel(index))
    })
  })

  test.describe('Given the user chooses yes from the second list collector', () => {
    test('Then they are taken to the correct list add screen', async () => {
      const listCollectorTemporaryAwayAddPage = new ListCollectorTemporaryAwayAddPage(page)
      const listCollectorTemporaryAwayPage = new ListCollectorTemporaryAwayPage(page)
      const summaryPage = new SummaryPage(page)
      await summaryPage.previous().click()
      await listCollectorTemporaryAwayPage.yesINeedToAddSomeone().click()
      await listCollectorTemporaryAwayPage.submit().click()
      await listCollectorTemporaryAwayAddPage.firstName().fill('Christopher')
      await listCollectorTemporaryAwayAddPage.lastName().fill('Pike')
      await listCollectorTemporaryAwayAddPage.submit().click()
      await listCollectorTemporaryAwayPage.noThereAreNumberOfPeoplePeopleLivingHere().click()
      await listCollectorTemporaryAwayPage.submit().click()

      const householdMembersExpected = ['Suzy Clemens', 'Christopher Pike']
      await checkItemsInList(householdMembersExpected, (index) => summaryPage.peopleListLabel(index))
    })
  })
})

test.describe('Given the user says no one else lives in the house', () => {
  test.beforeEach('Load the survey', async ({ page, openQuestionnaire }) => {
    const hubPage = new HubPage(page)
    await openQuestionnaire('test_list_collector_driving_checkbox.json')
    await hubPage.submit().click()
  })

  test('The user is asked if they need to add anyone that is temporarily away', async ({ page }) => {
    const anyoneUsuallyLiveAtPage = new AnyoneUsuallyLiveAtPage(page)
    const listCollectorTemporaryAwayPage = new ListCollectorTemporaryAwayPage(page)
    const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
    const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
    await primaryPersonListCollectorPage.yesIUsuallyLiveHere().click()
    await primaryPersonListCollectorPage.submit().click()
    await primaryPersonListCollectorAddPage.firstName().fill('Marcus')
    await primaryPersonListCollectorAddPage.lastName().fill('Twin')
    await primaryPersonListCollectorAddPage.submit().click()
    await anyoneUsuallyLiveAtPage.exclusiveNoneOfTheseApplyNoOneUsuallyLivesHere().click()
    await anyoneUsuallyLiveAtPage.submit().click()

    await expect(listCollectorTemporaryAwayPage.questionText()).toHaveText('You said 1 person lives at 12 Lovely Villas. Do you need to add anyone?')
  })
})

test.describe('Given a person does not live in the house', () => {
  test.beforeEach('Load the survey', async ({ page, openQuestionnaire }) => {
    const hubPage = new HubPage(page)
    await openQuestionnaire('test_list_collector_driving_checkbox.json')
    await hubPage.submit().click()
  })

  test('The user is asked whether they live there', async ({ page }) => {
    const anyoneUsuallyLiveAtPage = new AnyoneUsuallyLiveAtPage(page)
    const listCollectorTemporaryAwayPage = new ListCollectorTemporaryAwayPage(page)
    const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
    await primaryPersonListCollectorPage.noIDonTUsuallyLiveHere().click()
    await primaryPersonListCollectorPage.submit().click()
    await expect(anyoneUsuallyLiveAtPage.questionText()).toHaveText('Do any of the following usually live at 12 Lovely Villas on 21 March?')

    await anyoneUsuallyLiveAtPage.exclusiveNoneOfTheseApplyNoOneUsuallyLivesHere().click()
    await anyoneUsuallyLiveAtPage.submit().click()
    await expect(listCollectorTemporaryAwayPage.questionText()).toHaveText('You said 0 people lives at 12 Lovely Villas. Do you need to add anyone?')

    await listCollectorTemporaryAwayPage.noThereAreNumberOfPeoplePeopleLivingHere().click()
    await anyoneUsuallyLiveAtPage.submit().click()
  })
})
