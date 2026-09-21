import { createOpenQuestionnaire, test, expect } from '../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../fixtures/test'
import { checkItemsInList } from '../../helpers'
import YouLiveHerePage from '../../generated_pages/list_collector_variants/you-live-here-block.page'
import ListCollectorPage from '../../generated_pages/list_collector_variants/list-collector.page'
import ListCollectorAddPage from '../../generated_pages/list_collector_variants/list-collector-add.page'
import ListCollectorEditPage from '../../generated_pages/list_collector_variants/list-collector-edit.page'
import ListCollectorRemovePage from '../../generated_pages/list_collector_variants/list-collector-remove.page'
import SubmitPage from '../../base_pages/submit.page'
import ThankYouPage from '../../base_pages/thank-you.page'

test.describe('List Collector With Variants', () => {
  test.describe('Given that a person lives in house', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Load the survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_list_collector_variants.json')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('The user is asked questions about whether they live there', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const youLiveHerePage = new YouLiveHerePage(page)
      await youLiveHerePage.yes().click()
      await youLiveHerePage.submit().click()
      await expect(listCollectorPage.questionText()).toHaveText('Does anyone else live at 1 Pleasant Lane?')
    })

    test('The user is able to add members of the household', async () => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.anyoneElseYes().click()
      await listCollectorPage.submit().click()
      await expect(listCollectorAddPage.questionText()).toHaveText('What is the name of the person?')
      await listCollectorAddPage.firstName().fill('Samuel')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
    })

    test('The user can see all household members in the summary', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const peopleExpected = ['Samuel Clemens']
      await checkItemsInList(peopleExpected, (index) => listCollectorPage.listLabel(index))
    })

    test('The questionnaire has the correct question text on the change and remove pages', async () => {
      const listCollectorEditPage = new ListCollectorEditPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const listCollectorRemovePage = new ListCollectorRemovePage(page)
      await listCollectorPage.listEditLink(1).click()
      await expect(listCollectorEditPage.questionText()).toHaveText('What is the name of the person?')
      await listCollectorEditPage.previous().click()
      await listCollectorPage.listRemoveLink(1).click()
      await expect(listCollectorRemovePage.questionText()).toHaveText('Are you sure you want to remove this person?')
      await listCollectorRemovePage.previous().click()
    })

    test('The questionnaire shows the confirmation page when no more people to add', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const submitPage = new SubmitPage(page)
      await listCollectorPage.anyoneElseNo().click()
      await listCollectorPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.url()))
    })

    test('The questionnaire allows submission', async () => {
      const submitPage = new SubmitPage(page)
      await submitPage.submit().click()
      await expect(page).toHaveURL(/thank-you/)
    })
  })

  test.describe('Given a person does not live in house', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Load the survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_list_collector_variants.json')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('The user is asked questions about whether they live there', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const youLiveHerePage = new YouLiveHerePage(page)
      await youLiveHerePage.no().click()
      await youLiveHerePage.submit().click()
      await expect(listCollectorPage.questionText()).toHaveText('Does anyone live at 1 Pleasant Lane?')
    })

    test('The user is able to add members of the household', async () => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.anyoneElseYes().click()
      await listCollectorPage.submit().click()
      await expect(listCollectorAddPage.questionText()).toHaveText('What is the name of the person who isn’t you?')
      await listCollectorAddPage.firstName().fill('Samuel')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
    })

    test('The user can see all household members in the summary', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const peopleExpected = ['Samuel Clemens']
      await checkItemsInList(peopleExpected, (index) => listCollectorPage.listLabel(index))
    })

    test('The questionnaire has the correct question text on the change and remove pages', async () => {
      const listCollectorEditPage = new ListCollectorEditPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const listCollectorRemovePage = new ListCollectorRemovePage(page)
      await listCollectorPage.listEditLink(1).click()
      await expect(listCollectorEditPage.questionText()).toHaveText('What is the name of the person who isn’t you?')
      await listCollectorEditPage.previous().click()
      await listCollectorPage.listRemoveLink(1).click()
      await expect(listCollectorRemovePage.questionText()).toHaveText('Are you sure you want to remove this person who isn’t you?')
      await listCollectorRemovePage.previous().click()
    })

    test('The questionnaire shows the confirmation page when no more people to add', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const submitPage = new SubmitPage(page)
      await listCollectorPage.anyoneElseNo().click()
      await listCollectorPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.url()))
    })

    test('The questionnaire allows submission', async () => {
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      await submitPage.submit().click()
      await expect(page).toHaveURL(new RegExp(thankYouPage.url()))
    })
  })
})
