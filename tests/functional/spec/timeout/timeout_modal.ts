import { test, expect } from '../../fixtures/test'
import type { Page } from '../../fixtures/test'
import TimeoutModalBasePage from '../../base_pages/timeout-modal.page'

const timeoutModal = (page: Page): TimeoutModalBasePage => new TimeoutModalBasePage(page)

const checkTimeoutModal = async (page: Page): Promise<void> => {
  await timeoutModal(page).timer().waitFor({ timeout: 70000 })
  await expect(timeoutModal(page).timer()).toHaveText('To protect your information, your progress will be saved and you will be signed out in 59 seconds.')
}

class TimeoutModalCases {
  testCaseExpired (): void {
    test('When the timeout modal is displayed and I do not extend my session, Then I am redirected to the session expired page', async ({ page }) => {
      // Set a longer timeout for this test to account for the wait time
      test.setTimeout(140000)
      await checkTimeoutModal(page)
      await page.waitForTimeout(65000)
      await expect(page).toHaveURL(/\/session-expired/)
      await expect(page.locator('#main-content')).toContainText('Sorry, you need to sign in again')
      await expect(page.locator('#main-content')).not.toContainText('To protect your information, your progress will be saved and you will be signed out in')
    })
  }

  testCaseExtended (expectedPath: string): void {
    test('When the timeout modal is displayed and I continue, Then my session is extended', async ({ page }) => {
      // Set a longer timeout for this test to account for the wait time
      test.setTimeout(140000)
      await checkTimeoutModal(page)
      await timeoutModal(page).submit().click()
      await expect(timeoutModal(page).timer()).toBeHidden()
      await page.waitForTimeout(65000)
      await page.reload()
      await expect(page).toHaveURL(new RegExp(expectedPath))
      await expect(page.locator('#main-content')).not.toContainText('Sorry, you need to sign in again')
    })
  }

  testCaseExtendedNewWindow (expectedPath: string): void {
    test('When the timeout modal is displayed and I open a new window then return, Then my session is extended', async ({ page }) => {
      // Set a longer timeout for this test to account for the wait time
      test.setTimeout(140000)
      await checkTimeoutModal(page)
      const newPage = await page.context().newPage()
      await newPage.goto('about:blank')
      await newPage.close()
      await page.reload()
      await page.waitForTimeout(65000)
      await expect(page).toHaveURL(new RegExp(expectedPath))
    })
  }
}

export const TimeoutModalTestCase = new TimeoutModalCases()
