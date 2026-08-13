import { test, expect } from '../../../fixtures/test'
import EmploymentStatusBlockPage from '../../../generated_pages/hub_and_spoke/employment-status.page'
import ProxyPage from '../../../generated_pages/hub_and_spoke/proxy.page'
import HubPage from '../../../base_pages/hub.page'

test.describe('Choose another section link', () => {
  test('When a user first views the Hub, then the link should not be displayed', async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_hub_and_spoke.json')
    await expect(page.locator('#main-content')).not.toContainText('Choose another section and return to this later')
  })

  test('When a user views the first question and the hub is not available, then the link should not be displayed', async ({ page, openQuestionnaire }) => {
    await openQuestionnaire('test_hub_complete_sections.json')
    await expect(page.locator('#main-content')).not.toContainText('Choose another section and return to this later')
  })

  test('When a user starts a new section and the hub is available, then the link should be displayed', async ({ page, openQuestionnaire }) => {
    const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
    const hubPage = new HubPage(page)
    await openQuestionnaire('test_hub_complete_sections.json')
    await employmentStatusBlockPage.workingAsAnEmployee().click()
    await employmentStatusBlockPage.submit().click()
    await hubPage.summaryRowLink('accommodation-section').click()
    await expect(page.locator('#main-content')).toContainText('Choose another section and return to this later')
  })

  test('When a user gets to a section summary and the hub is available, then the link should not be displayed', async ({ page, openQuestionnaire }) => {
    const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
    const hubPage = new HubPage(page)
    const proxyPage = new ProxyPage(page)
    await openQuestionnaire('test_hub_complete_sections.json')
    await employmentStatusBlockPage.workingAsAnEmployee().click()
    await employmentStatusBlockPage.submit().click()
    await hubPage.summaryRowLink('accommodation-section').click()
    await proxyPage.noIMAnsweringForMyself().click()
    await proxyPage.submit().click()
    await expect(page.locator('#main-content')).not.toContainText('Choose another section and return to this later')
  })
})
