import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { BrowserContext, Page } from '../../../fixtures/test'
import { checkItemsInList } from '../../../helpers'
import AnyoneLiveAtListCollector from '../../../generated_pages/answer_action_redirect_to_list_add_block_checkbox/anyone-else-live-at.page'
import AnyoneLiveAtListCollectorAddPage from '../../../generated_pages/answer_action_redirect_to_list_add_block_checkbox/anyone-else-live-at-add.page'
import AnyoneLiveAtListCollectorRemovePage from '../../../generated_pages/answer_action_redirect_to_list_add_block_checkbox/anyone-else-live-at-remove.page'
import AnyoneUsuallyLiveAt from '../../../generated_pages/answer_action_redirect_to_list_add_block_checkbox/anyone-usually-live-at.page'

test.describe('Answer Action: Redirect To List Add Question (Checkbox)', () => {
  test.describe.configure({ mode: 'serial' })

  test.describe('Given the user is on a question with a "RedirectToListAddBlock" action enabled', () => {
    let context: BrowserContext
    let page: Page
    let openQuestionnaire: ReturnType<typeof createOpenQuestionnaire>

    test.beforeAll('Launch survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_answer_action_redirect_to_list_add_block_checkbox.json')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When the user selects "No", Then, they should be taken to the list collector.', async () => {
      const anyoneLiveAtListCollector = new AnyoneLiveAtListCollector(page)
      const anyoneUsuallyLiveAt = new AnyoneUsuallyLiveAt(page)
      await anyoneUsuallyLiveAt.no().click()
      await anyoneUsuallyLiveAt.submit().click()
      await expect(page).toHaveURL(new RegExp(anyoneLiveAtListCollector.pageName))
    })

    test('When the user selects "Yes" then they should be taken to the list collector add question.', async () => {
      const anyoneLiveAtListCollectorAddPage = new AnyoneLiveAtListCollectorAddPage(page)
      const anyoneUsuallyLiveAt = new AnyoneUsuallyLiveAt(page)
      await page.goto(anyoneUsuallyLiveAt.url())
      await anyoneUsuallyLiveAt.iThinkSo().click()
      await anyoneUsuallyLiveAt.submit().click()
      await expect(page).toHaveURL(new RegExp(anyoneLiveAtListCollectorAddPage.pageName))
      await expect(page).toHaveURL(/\?previous=anyone-usually-live-at/)
    })

    test('When the user clicks the "Previous" link from the add question then they should be taken to the block they came from, not the list collector', async () => {
      const anyoneLiveAtListCollectorAddPage = new AnyoneLiveAtListCollectorAddPage(page)
      const anyoneUsuallyLiveAt = new AnyoneUsuallyLiveAt(page)
      await anyoneLiveAtListCollectorAddPage.previous().click()
      await expect(page).toHaveURL(new RegExp(anyoneUsuallyLiveAt.pageName))
    })

    test('When the user adds a household member, Then, they are taken to the list collector and the household members are displayed', async () => {
      const anyoneLiveAtListCollector = new AnyoneLiveAtListCollector(page)
      const anyoneLiveAtListCollectorAddPage = new AnyoneLiveAtListCollectorAddPage(page)
      const anyoneUsuallyLiveAt = new AnyoneUsuallyLiveAt(page)
      await anyoneUsuallyLiveAt.submit().click()
      await anyoneLiveAtListCollectorAddPage.firstName().fill('Marcus')
      await anyoneLiveAtListCollectorAddPage.lastName().fill('Twin')
      await anyoneLiveAtListCollectorAddPage.submit().click()
      await expect(page).toHaveURL(new RegExp(anyoneLiveAtListCollector.pageName))

      const peopleExpected = ['Marcus Twin']
      await checkItemsInList(peopleExpected, (index) => anyoneLiveAtListCollector.listLabel(index))
    })

    test('When the user click the "Previous" link from the list collector, Then, they are taken to the last complete block', async () => {
      const anyoneLiveAtListCollector = new AnyoneLiveAtListCollector(page)
      const anyoneUsuallyLiveAt = new AnyoneUsuallyLiveAt(page)
      await anyoneLiveAtListCollector.previous().click()
      await expect(page).toHaveURL(new RegExp(anyoneUsuallyLiveAt.pageName))
    })

    test('When the user resubmits the first block and then list is not empty, Then they are taken to the list collector', async () => {
      const anyoneLiveAtListCollector = new AnyoneLiveAtListCollector(page)
      const anyoneUsuallyLiveAt = new AnyoneUsuallyLiveAt(page)
      await anyoneUsuallyLiveAt.submit().click()
      await expect(page).toHaveURL(new RegExp(anyoneLiveAtListCollector.pageName))
    })

    test('When the users removes the only person (Marcus Twain), Then, they are shown an empty list collector', async () => {
      const anyoneLiveAtListCollector = new AnyoneLiveAtListCollector(page)
      const anyoneLiveAtListCollectorRemovePage = new AnyoneLiveAtListCollectorRemovePage(page)
      await anyoneLiveAtListCollector.listRemoveLink(1).click()
      await anyoneLiveAtListCollectorRemovePage.yes().click()
      await anyoneLiveAtListCollectorRemovePage.submit().click()
      await expect(page).toHaveURL(new RegExp(anyoneLiveAtListCollector.pageName))
      await expect(anyoneLiveAtListCollector.listLabel(1)).not.toBeVisible()
    })

    test('When the user resubmits the first block and then list is empty, Then they are taken to the add question', async () => {
      const anyoneLiveAtListCollector = new AnyoneLiveAtListCollector(page)
      const anyoneLiveAtListCollectorAddPage = new AnyoneLiveAtListCollectorAddPage(page)
      const anyoneUsuallyLiveAt = new AnyoneUsuallyLiveAt(page)
      await expect(page).toHaveURL(new RegExp(anyoneLiveAtListCollector.pageName))

      await anyoneLiveAtListCollector.previous().click()
      await expect(page).toHaveURL(new RegExp(anyoneUsuallyLiveAt.pageName))

      await anyoneUsuallyLiveAt.submit().click()
      await expect(page).toHaveURL(new RegExp(anyoneLiveAtListCollectorAddPage.pageName))
    })
  })
})
