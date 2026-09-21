import { test, expect } from '../fixtures/test'
import InitialPage from '../generated_pages/checkbox/mandatory-checkbox.page'
import HubPage from '../base_pages/hub.page'

test.describe('Given I am not authenticated and have no cookie,', () => {
  test('When I visit a page in runner, Then the cookie banner shouldn‘t be displayed', async ({ page }) => {
    const initialPage = new InitialPage(page)
    await page.goto('/')
    await expect(initialPage.acceptCookies()).not.toBeVisible()
  })
})

test.describe('Given I start a survey,', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_checkbox.json')
  })

  test('When I open the page, Then the cookie banner should be displayed', async ({ page }) => {
    const initialPage = new InitialPage(page)
    await expect(initialPage.acceptCookies()).toBeVisible()
  })

  test.skip('When I delete all cookies from the browser and refresh the page, Then the cookie banner shouldn‘t be displayed', async ({ page }) => {
    const initialPage = new InitialPage(page)
    // To be investigated. This test is skipped due to an issue in GitHub Actions with deleting cookies and the flakiness of waiting for acceptCookies().
    await page.context().clearCookies()
    await page.reload()
    await expect(initialPage.acceptCookies()).not.toBeVisible()
  })

  test('When I sign out and click the browser back button, Then the cookie banner should be displayed', async ({ page }) => {
    const initialPage = new InitialPage(page)
    await initialPage.saveSignOut().click()
    await page.goBack()
    await expect(initialPage.acceptCookies()).toBeVisible()
  })

  test('When I accept the cookies and refresh the page, Then the cookie banner shouldn‘t be displayed', async ({ page }) => {
    const initialPage = new InitialPage(page)
    await initialPage.acceptCookies().click()
    await page.reload()
    await expect(initialPage.acceptCookies()).not.toBeVisible()
  })
})

test.describe('Given I start a survey with multiple languages,', () => {
  test.beforeEach(async ({ page }) => {
    await page.context().clearCookies()
  })

  test('When I open the page in english, Then the cookie banner should be displayed in english', async ({ page, openQuestionnaire }) => {
    const hubPage = new HubPage(page)
    await openQuestionnaire('test_language.json', {
      language: 'en'
    })
    await expect(hubPage.acceptCookies()).toHaveText('Accept additional cookies')
  })

  test('When I open the page in welsh, Then the cookie banner should be displayed in welsh', async ({ page, openQuestionnaire }) => {
    const hubPage = new HubPage(page)
    await openQuestionnaire('test_language.json', {
      language: 'cy'
    })
    await expect(hubPage.acceptCookies()).toHaveText('Derbyn cwcis ychwanegol')
  })

  test('When I open the page in english, Then change the language to welsh the cookie banner should be displayed in welsh', async ({
    page,
    openQuestionnaire
  }) => {
    const hubPage = new HubPage(page)
    await openQuestionnaire('test_language.json', {
      language: 'en'
    })
    await expect(hubPage.acceptCookies()).toHaveText('Accept additional cookies')
    const welshHref = await hubPage.switchLanguage('cy').getAttribute('href')
    if (welshHref === null || welshHref.length === 0) {
      throw new Error('Expected Welsh language link to include an href')
    }
    await page.goto(new URL(welshHref, page.url()).toString())
    await expect(hubPage.acceptCookies()).toHaveText('Derbyn cwcis ychwanegol')
  })
})
