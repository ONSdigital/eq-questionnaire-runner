import { test, expect } from '../fixtures/test'
import HubPage from '../base_pages/hub.page'

test.describe('Page Layout', () => {
  test('Given a page in the questionnaire, When I visit the page, Then the page width should be as expected', async ({ page }) => {
    const hubPage = new HubPage(page)
    await page.goto(hubPage.url())

    const cssWidthSelector = await page.locator('div[class*="ons-col-"][class*="@m"]').getAttribute('class')
    await expect(cssWidthSelector).toContain('ons-col-8@m')
  })
})
