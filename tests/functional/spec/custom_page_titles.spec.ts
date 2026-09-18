import { createOpenQuestionnaire, test, expect } from '../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../fixtures/test'
import DateOfBirthPage from '../generated_pages/custom_page_titles/date-of-birth.page'
import HubPage from '../base_pages/hub.page'
import IndividualInterstitialPage from '../generated_pages/custom_page_titles/individual-interstitial.page'
import ListCollectorAddPage from '../generated_pages/custom_page_titles/list-collector-add.page'
import ListCollectorEditPage from '../generated_pages/custom_page_titles/list-collector-edit.page'
import ListCollectorPage from '../generated_pages/custom_page_titles/list-collector.page'
import ProxyPage from '../generated_pages/custom_page_titles/proxy.page'
import RelationshipsPage from '../generated_pages/custom_page_titles/relationships.page'

test.describe('Feature: Custom Page Titles', () => {
  const schema = 'test_custom_page_titles.json'

  test.describe('Given I am completing the test_custom_page_titles survey,', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('load the survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire(schema)
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When I navigate to the list collector page, Then I should see the custom page title', async () => {
      const hubPage = new HubPage(page)
      await hubPage.submit().click()
      await expect(page).toHaveTitle('Custom page title - Test Custom Page Titles')
    })

    test('When I navigate to the add person page, Then I should see the custom page title', async () => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await expect(page).toHaveTitle('Add person 1 - Test Custom Page Titles')

      await listCollectorAddPage.firstName().fill('Marcus')
      await listCollectorAddPage.lastName().fill('Twin')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await expect(page).toHaveTitle('Add person 2 - Test Custom Page Titles')
    })

    test('When I navigate to relationship collector pages, Then I should see the custom page titles', async () => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const relationshipsPage = new RelationshipsPage(page)
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
      await expect(page).toHaveTitle('How Person 1 is related to Person 2 - Test Custom Page Titles')

      await relationshipsPage.husbandOrWife().click()
      await relationshipsPage.submit().click()
      await expect(page).toHaveTitle('How Person 1 is related to Person 3 - Test Custom Page Titles')

      await relationshipsPage.sonOrDaughter().click()
      await relationshipsPage.submit().click()
      await expect(page).toHaveTitle('How Person 2 is related to Person 3 - Test Custom Page Titles')

      await relationshipsPage.sonOrDaughter().click()
      await relationshipsPage.submit().click()
      await expect(page).toHaveTitle('Custom section summary page title - Test Custom Page Titles')
    })

    test('When I navigate to list edit and remove pages Then I should see the custom page titles', async () => {
      const listCollectorEditPage = new ListCollectorEditPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.listEditLink(1).click()
      await expect(page).toHaveTitle('Edit person 1 - Test Custom Page Titles')
      await listCollectorEditPage.previous().click()
      await listCollectorPage.listRemoveLink(1).click()
      await expect(page).toHaveTitle('Remove person 1 - Test Custom Page Titles')
    })

    test('When I navigate to a repeating section which has custom page title, Then all page titles in the section should have the correct prefix', async () => {
      const dateOfBirthPage = new DateOfBirthPage(page)
      const hubPage = new HubPage(page)
      const individualInterstitialPage = new IndividualInterstitialPage(page)
      const proxyPage = new ProxyPage(page)
      await page.goto(hubPage.url())
      await hubPage.submit().click()
      await expect(page).toHaveTitle('Individual interstitial: Person 1 - Test Custom Page Titles')
      await individualInterstitialPage.submit().click()
      await expect(page).toHaveTitle('Proxy question: Person 1 - Test Custom Page Titles')
      await proxyPage.submit().click()
      await expect(page).toHaveTitle('What is your date of birth?: Person 1 - Test Custom Page Titles')
      await dateOfBirthPage.submit().click()
      await expect(page).toHaveTitle('Summary: Person 1 - Test Custom Page Titles')
    })
  })
})
