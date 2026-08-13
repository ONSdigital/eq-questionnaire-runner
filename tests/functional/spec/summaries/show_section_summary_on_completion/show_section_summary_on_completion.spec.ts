import { createOpenQuestionnaire, test } from '../../../fixtures/test'
import type { BrowserContext, Page } from '../../../fixtures/test'
import EmploymentStatusBlockPage from '../../../generated_pages/show_section_summary_on_completion/employment-status.page'
import EmploymentSectionSummary from '../../../generated_pages/show_section_summary_on_completion/employment-section-summary.page'
import ProxyQuestionPage from '../../../generated_pages/show_section_summary_on_completion/proxy.page'
import AccommodationSectionSummary from '../../../generated_pages/show_section_summary_on_completion/accommodation-section-summary.page'
import HubPage from '../../../base_pages/hub.page.js'
import { verifyUrlContains } from '../../../helpers'

test.describe('Feature: Show section summary on completion', () => {
  test.describe.configure({ mode: 'serial' })

  let context: BrowserContext
  let page: Page
  let openQuestionnaire: ReturnType<typeof createOpenQuestionnaire>

  test.beforeAll('Launch survey', async ({ browser }) => {
    context = await browser.newContext()
    page = await context.newPage()
    openQuestionnaire = createOpenQuestionnaire(page)
    await openQuestionnaire('test_show_section_summary_on_completion.json')
  })

  test.afterAll(async () => {
    await context.close()
  })

  test.describe('Given I am completing a section with the summary turned off for the forward journey', () => {
    test('When I reach the end of that section, Then I go straight to the hub', async () => {
      const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
      const hubPage = new HubPage(page)
      await employmentStatusBlockPage.workingAsAnEmployee().click()
      await employmentStatusBlockPage.submit().click()

      await verifyUrlContains(page, hubPage.url())
    })
  })

  test.describe('Given I have completed a section with the summary turned off for the forward journey', () => {
    test('When I return to a completed section from the hub, Then I am returned to that section summary', async () => {
      const employmentSectionSummary = new EmploymentSectionSummary(page)
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink('employment-section').click()

      await verifyUrlContains(page, employmentSectionSummary.url())
    })
  })

  test.describe('Given I am completing a section with the summary turned on for the forward journey', () => {
    test.beforeEach('Get to hub', async () => {
      const hubPage = new HubPage(page)
      await page.goto(hubPage.url())
    })

    test('When I reach the end of that section, Then I will be taken to the section summary to enable me to amend an answer', async () => {
      const accommodationSectionSummary = new AccommodationSectionSummary(page)
      const hubPage = new HubPage(page)
      const proxyQuestionPage = new ProxyQuestionPage(page)
      await hubPage.summaryRowLink('accommodation-section').click()
      await proxyQuestionPage.noIMAnsweringForMyself().click()
      await proxyQuestionPage.submit().click()

      await verifyUrlContains(page, accommodationSectionSummary.url())
    })
  })

  test.describe('Given I have completed a section with the summary turned on for the forward journey', () => {
    test.beforeEach('Get to hub', async () => {
      const hubPage = new HubPage(page)
      await page.goto(hubPage.url())
    })

    test('When I return to a completed section from the hub, Then I am returned to the correct section summary', async () => {
      const accommodationSectionSummary = new AccommodationSectionSummary(page)
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink('accommodation-section').click()

      await verifyUrlContains(page, accommodationSectionSummary.url())
    })
  })
})
