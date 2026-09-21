import { createOpenQuestionnaire, test, expect } from '../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../fixtures/test'
import ListCollectorPage from '../../generated_pages/list_collector_primary_person/list-collector.page'
import ListCollectorAddPage from '../../generated_pages/list_collector_primary_person/list-collector-add.page'
import ListCollectorEditPage from '../../generated_pages/list_collector_primary_person/list-collector-edit.page'
import PrimaryPersonListCollectorPage from '../../generated_pages/list_collector_primary_person/primary-person-list-collector.page'
import PrimaryPersonListCollectorAddPage from '../../generated_pages/list_collector_primary_person/primary-person-list-collector-add.page'
import SectionSummaryPage from '../../generated_pages/list_collector/section-summary.page'
import SubmitPage from '../../base_pages/submit.page'
import ThankYouPage from '../../base_pages/thank-you.page'
import AnyoneUsuallyLiveAtPage from '../../generated_pages/list_collector_primary_person/anyone-usually-live-at.page'

test.describe('Primary Person List Collector Survey', () => {
  test.describe("Given the user starts on the 'do you live here' question", () => {
    test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_list_collector_primary_person.json')
    })

    test.skip("When the user says they do not live there, and changes their answer to yes, then the user can't navigate to the list collector", async ({
      page
    }) => {
      const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      await primaryPersonListCollectorPage.noLabel().click()
      await primaryPersonListCollectorPage.submit().click()
      await primaryPersonListCollectorAddPage.previous().click()
      await primaryPersonListCollectorPage.yesLabel().click()
      await primaryPersonListCollectorPage.submit().click()
      await page.goto('questionnaire/list-collector')
      await expect(primaryPersonListCollectorPage.questionText()).toHaveText('Do you live here')
    })
  })

  test.describe("Given the user starts on the 'do you live here' question", () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Load the survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_list_collector_primary_person.json')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When the user says that they do live there, then they are shown as the primary person', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      await primaryPersonListCollectorPage.yesLabel().click()
      await primaryPersonListCollectorPage.submit().click()
      await primaryPersonListCollectorAddPage.firstName().fill('Mark')
      await primaryPersonListCollectorAddPage.lastName().fill('Twin')
      await primaryPersonListCollectorAddPage.submit().click()
      await expect(listCollectorPage.listLabel(1)).toHaveText('Mark Twin (You)')
    })

    test('When the user adds another person, they are shown in the summary', async () => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.yesLabel().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Samuel')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
      await expect(listCollectorPage.listLabel(2)).toHaveText('Samuel Clemens')
    })

    test('When the user goes back and answers No, the primary person is not shown', async () => {
      const anyoneUsuallyLiveAtPage = new AnyoneUsuallyLiveAtPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      await listCollectorPage.previous().click()
      await primaryPersonListCollectorPage.no().click()
      await primaryPersonListCollectorPage.submit().click()
      await anyoneUsuallyLiveAtPage.no().click()
      await anyoneUsuallyLiveAtPage.submit().click()
      await expect(listCollectorPage.listLabel(1)).toHaveText('Samuel Clemens')
    })

    test('When the user adds the primary person again, then the primary person is first in the list', async () => {
      const anyoneUsuallyLiveAtPage = new AnyoneUsuallyLiveAtPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      await listCollectorPage.previous().click()
      await anyoneUsuallyLiveAtPage.previous().click()
      await primaryPersonListCollectorPage.yes().click()
      await primaryPersonListCollectorPage.submit().click()
      await primaryPersonListCollectorAddPage.firstName().fill('Mark')
      await primaryPersonListCollectorAddPage.lastName().fill('Twin')
      await primaryPersonListCollectorAddPage.submit().click()
      await expect(listCollectorPage.listLabel(1)).toHaveText('Mark Twin (You)')
    })

    test('When the user views the summary, then it does not show the remove link for the primary person', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      await expect(listCollectorPage.listRemoveLink(1)).not.toBeVisible()
      await expect(listCollectorPage.listRemoveLink(2)).toBeVisible()
    })

    test("When the user changes the primary person's name on the summary, then the name should be updated", async () => {
      const listCollectorEditPage = new ListCollectorEditPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.listEditLink(1).click()
      await listCollectorEditPage.firstName().fill('Mark')
      await listCollectorEditPage.lastName().fill('Twain')
      await listCollectorEditPage.submit().click()
      await expect(listCollectorPage.listLabel(1)).toHaveText('Mark Twain (You)')
      await expect(listCollectorPage.listLabel(2)).toHaveText('Samuel Clemens')
    })

    test('When the user views the summary, then it does not show the does anyone usually live here question', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await expect(page.locator('#main-content')).not.toContainText('usually live here')
    })

    test('When the user attempts to submit, then they are shown the confirmation page', async () => {
      const sectionSummaryPage = new SectionSummaryPage(page)
      const submitPage = new SubmitPage(page)
      await sectionSummaryPage.submit().click()
      await expect(submitPage.guidance()).toHaveText('Thank you for your answers, do you wish to submit')
    })

    test('When the user submits, then they are allowed to submit the survey', async () => {
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      await submitPage.submit().click()
      await expect(page).toHaveURL(new RegExp(thankYouPage.pageName))
    })
  })

  test.describe("Given the user starts on the 'do you live here' question", () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Load the survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_list_collector_primary_person.json')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When the user says they do not live there, then an empty list is displayed', async () => {
      const anyoneUsuallyLiveAtPage = new AnyoneUsuallyLiveAtPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      await primaryPersonListCollectorPage.no().click()
      await primaryPersonListCollectorPage.submit().click()
      await anyoneUsuallyLiveAtPage.no().click()
      await expect(listCollectorPage.listLabel(1)).not.toBeVisible()
    })

    test('When the user clicks on the add person button multiple times, then only one person is added', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      await listCollectorPage.previous().click()
      await primaryPersonListCollectorPage.yes().click()
      await primaryPersonListCollectorPage.submit().click()
      await primaryPersonListCollectorAddPage.firstName().fill('Mark')
      await primaryPersonListCollectorAddPage.lastName().fill('Twain')
      await primaryPersonListCollectorPage.submit().click()
      await primaryPersonListCollectorPage.submit().click()
      await expect(listCollectorPage.listLabel(1)).toHaveText('Mark Twain (You)')
      await expect(listCollectorPage.listLabel(2)).not.toBeVisible()
    })
  })
})
