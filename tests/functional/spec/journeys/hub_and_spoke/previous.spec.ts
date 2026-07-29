import { test, expect } from '../../../fixtures/test'
import EmploymentStatusBlockPage from '../../../generated_pages/hub_and_spoke/employment-status.page'
import EmploymentTypePage from '../../../generated_pages/hub_and_spoke/employment-type.page'
import HubPage from '../../../base_pages/hub.page'
import ProxyPage from '../../../generated_pages/hub_and_spoke/proxy.page'

const schema = 'test_hub_complete_sections.json'

test.describe('Choose another section link', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire(schema)
  })

  test('When a user gets to initial question, then the previous location link should not be displayed', async ({ page }) => {
    const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
    await expect(employmentStatusBlockPage.previous()).not.toBeVisible()
  })

  test('When a user gets to the hub, then the previous location link should not be displayed', async ({ page }) => {
    const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
    const hubPage = new HubPage(page)
    await employmentStatusBlockPage.workingAsAnEmployee().click()
    await employmentStatusBlockPage.submit().click()
    await expect(hubPage.previous()).not.toBeVisible()
  })

  test('When a user gets to subsequent question, then the previous location link should be displayed', async ({ page }) => {
    const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
    const employmentTypePage = new EmploymentTypePage(page)
    await employmentStatusBlockPage.exclusiveNoneOfTheseApply().click()
    await employmentStatusBlockPage.submit().click()
    await expect(employmentTypePage.previous()).toBeVisible()
  })

  test('When a user gets to subsequent questions past the hub, then the previous location link should be displayed', async ({ page }) => {
    const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
    const hubPage = new HubPage(page)
    const proxyPage = new ProxyPage(page)
    await employmentStatusBlockPage.workingAsAnEmployee().click()
    await employmentStatusBlockPage.submit().click()
    await hubPage.summaryRowLink('accommodation-section').click()
    await expect(proxyPage.previous()).toBeVisible()
  })
})
