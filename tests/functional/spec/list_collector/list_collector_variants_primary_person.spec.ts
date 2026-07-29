import { createOpenQuestionnaire, test, expect } from '../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../fixtures/test'
import VariantBlockPage from '../../generated_pages/list_collector_variants_primary_person/variant-block.page'
import PrimaryPersonListCollectorPage from '../../generated_pages/list_collector_variants_primary_person/primary-person-list-collector.page'
import ListCollectorAddPage from '../../generated_pages/list_collector_variants_primary_person/list-collector-add.page'
import ListCollectorPage from '../../generated_pages/list_collector_variants_primary_person/list-collector.page'
import EditPersonPage from '../../generated_pages/list_collector_variants_primary_person/list-collector-edit.page'
import SubmitPage from '../../generated_pages/list_collector_variants_primary_person/submit.page'
import ThankYouPage from '../../base_pages/thank-you.page'

test.describe('List collector with variants primary person', () => {
  test.describe('Given that person lives in house', () => {
    test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_list_collector_variants_primary_person.json')
    })

    test('When the user is asked questions about whether they like variant, Then they are routed to section asking if they live in the house', async ({
      page
    }) => {
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      const variantBlockPage = new VariantBlockPage(page)
      await variantBlockPage.yes().click()
      await variantBlockPage.submit().click()
      await expect(primaryPersonListCollectorPage.legend()).toHaveText('Do you live here? (variant)')
    })
  })

  test.describe("Given the user starts on the 'Do you like variant' question", () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Load the survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_list_collector_variants_primary_person.json')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When the user says that they do live there, Then they are shown as the primary person', async () => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      const variantBlockPage = new VariantBlockPage(page)
      await variantBlockPage.yes().click()
      await variantBlockPage.submit().click()
      await primaryPersonListCollectorPage.youLiveHereYes().click()
      await primaryPersonListCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('John')
      await listCollectorAddPage.lastName().fill('Doe')
      await listCollectorAddPage.submit().click()
      await expect(listCollectorPage.listLabel(1)).toHaveText('John Doe (You)')
    })

    test('When the user adds another person, Then they are shown in the list collector summary', async () => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.yesLabel().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Samuel')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
      await expect(listCollectorPage.listLabel(2)).toHaveText('Samuel Clemens')
    })

    test("When the user goes back and answers 'No' for 'Do you live here' question, Then the primary person is not shown", async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      await listCollectorPage.previous().click()
      await primaryPersonListCollectorPage.youLiveHereNo().click()
      await primaryPersonListCollectorPage.submit().click()
      await expect(listCollectorPage.listLabel(1)).toHaveText('Samuel Clemens')
    })

    test('When the user adds another person, Then the user is able to add members of the household', async () => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await expect(listCollectorAddPage.questionText()).toHaveText('What is the name of the person?')
      await listCollectorAddPage.firstName().fill('Samuel')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
    })

    test('When the user adds the primary person again, Then the primary person is first in the list', async () => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      await listCollectorPage.previous().click()
      await primaryPersonListCollectorPage.youLiveHereYes().click()
      await primaryPersonListCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Mark')
      await listCollectorAddPage.lastName().fill('Twin')
      await listCollectorAddPage.submit().click()
      await expect(listCollectorPage.listLabel(1)).toHaveText('Mark Twin (You)')
    })

    test('When the user views the summary, Then it does not show the remove link for the primary person', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      await expect(listCollectorPage.listRemoveLink(1)).not.toBeVisible()
      await expect(listCollectorPage.listRemoveLink(2)).toBeVisible()
    })

    test("When the user changes the primary person's name on the summary, Then the name should be updated", async () => {
      const editPersonPage = new EditPersonPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.listEditLink(1).click()
      await editPersonPage.firstName().fill('John')
      await editPersonPage.lastName().fill('Doe')
      await editPersonPage.submit().click()
      await expect(listCollectorPage.listLabel(1)).toHaveText('John Doe (You)')
      await expect(listCollectorPage.listLabel(2)).toHaveText('Samuel Clemens')
    })

    test("When the user answers 'no' to add any person, Then the questionnaire shows the confirmation page", async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const submitPage = new SubmitPage(page)
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.url()))
    })

    test('When the user attempts to submit, Then they are shown the confirmation page', async () => {
      const submitPage = new SubmitPage(page)
      await expect(submitPage.guidance()).toHaveText('Please submit this survey to complete it')
    })

    test('When user updates the variant answer, Then it should come back to summary screen with updated answer', async () => {
      const submitPage = new SubmitPage(page)
      const variantBlockPage = new VariantBlockPage(page)
      await submitPage.variantAnswerEdit().click()
      await variantBlockPage.no().click()
      await variantBlockPage.submit().click()
      await expect(submitPage.variantAnswer()).toHaveText('No')
    })

    test('When the user submits, Then they are allowed to submit the survey', async () => {
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      await submitPage.submit().click()
      await expect(page).toHaveURL(new RegExp(thankYouPage.pageName))
    })
  })
})

test.describe("Given the user starts on the 'Do you like variant' question", () => {
  test.describe.configure({ mode: 'serial' })

  let context: BrowserContext
  let page: Page
  let openQuestionnaire: OpenQuestionnaire

  test.beforeAll('Load the survey', async ({ browser }) => {
    context = await browser.newContext()
    page = await context.newPage()
    openQuestionnaire = createOpenQuestionnaire(page)
    await openQuestionnaire('test_list_collector_variants_primary_person.json')
  })

  test.afterAll(async () => {
    await context.close()
  })

  test("When the user answers 'No' for variant question, Then they are routed to section asking if they live in the house", async () => {
    const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
    const variantBlockPage = new VariantBlockPage(page)
    await variantBlockPage.no().click()
    await variantBlockPage.submit().click()
    await expect(primaryPersonListCollectorPage.legend()).toHaveText('Do you live here?')
  })

  test('When the user says they do not live there and anyone else, Then confirmation screen is displayed', async () => {
    const listCollectorPage = new ListCollectorPage(page)
    const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
    const submitPage = new SubmitPage(page)
    await primaryPersonListCollectorPage.youLiveHereNo().click()
    await primaryPersonListCollectorPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()

    await expect(submitPage.guidance()).toHaveText('Please submit this survey to complete it')
  })
})
