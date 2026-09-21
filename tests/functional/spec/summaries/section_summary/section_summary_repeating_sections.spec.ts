import { test, expect } from '../../../fixtures/test'
import PrimaryPersonPage from '../../../generated_pages/repeating_section_summaries/primary-person-list-collector.page'
import PrimaryPersonAddPage from '../../../generated_pages/repeating_section_summaries/primary-person-list-collector-add.page'
import FirstListCollectorPage from '../../../generated_pages/repeating_section_summaries/list-collector.page'
import FirstListCollectorAddPage from '../../../generated_pages/repeating_section_summaries/list-collector-add.page'
import PersonalSummaryPage from '../../../generated_pages/repeating_section_summaries/personal-details-section-summary.page'
import ProxyPage from '../../../generated_pages/repeating_section_summaries/proxy.page'
import DateOfBirthPage from '../../../generated_pages/repeating_section_summaries/date-of-birth.page'
import HubPage from '../../../base_pages/hub.page'

test.describe('Feature: Repeating Section Summaries', () => {
  test.describe('Given the user has added some members to the household and is on the Hub', () => {
    test.beforeEach('Open survey and add household members', async ({ page, openQuestionnaire }) => {
      const firstListCollectorAddPage = new FirstListCollectorAddPage(page)
      const firstListCollectorPage = new FirstListCollectorPage(page)
      const hubPage = new HubPage(page)
      const primaryPersonAddPage = new PrimaryPersonAddPage(page)
      const primaryPersonPage = new PrimaryPersonPage(page)
      await openQuestionnaire('test_repeating_section_summaries.json')
      // Ensure the questionnaire fully loads
      await page.waitForTimeout(100)
      // Ensure we are on the Hub
      await expect(page).toHaveURL(new RegExp(hubPage.url()))
      // Start first section to add household members
      await hubPage.summaryRowLink('section').click()

      // Add a primary person
      await primaryPersonPage.yes().click()
      await primaryPersonPage.submit().click()
      await primaryPersonAddPage.firstName().fill('Mark')
      await primaryPersonAddPage.lastName().fill('Twain')
      await primaryPersonPage.submit().click()

      // Add other household members

      await firstListCollectorPage.yes().click()
      await firstListCollectorPage.submit().click()
      await firstListCollectorAddPage.firstName().fill('Jean')
      await firstListCollectorAddPage.lastName().fill('Clemens')
      await firstListCollectorAddPage.submit().click()

      await firstListCollectorPage.no().click()
      await firstListCollectorPage.submit().click()
    })

    test.describe('When the user finishes a repeating section', () => {
      test.beforeEach('Enter information for a repeating section', async ({ page }) => {
        const dateOfBirthPage = new DateOfBirthPage(page)
        const hubPage = new HubPage(page)
        const proxyPage = new ProxyPage(page)
        await hubPage.summaryRowLink('personal-details-section-1').click()
        await proxyPage.yes().click()
        await proxyPage.submit().click()

        await dateOfBirthPage.day().fill('30')
        await dateOfBirthPage.month().fill('11')
        await dateOfBirthPage.year().fill('1835')
        await dateOfBirthPage.submit().click()
      })

      test.beforeEach('Navigate to the Section Summary', async ({ page }) => {
        const hubPage = new HubPage(page)
        await page.goto(hubPage.url())
        await hubPage.summaryRowLink('personal-details-section-1').click()
      })

      test('the title set in the repeating block is used for the section summary title', async ({ page }) => {
        const personalSummaryPage = new PersonalSummaryPage(page)
        await expect(personalSummaryPage.heading()).toHaveText('Mark Twain')
      })

      test('renders their name as part of the question title on the section summary', async ({ page }) => {
        const personalSummaryPage = new PersonalSummaryPage(page)
        await expect(personalSummaryPage.dateOfBirthQuestion()).toContainText('Mark Twain’s')
      })

      test('renders the correct date of birth answer', async ({ page }) => {
        const personalSummaryPage = new PersonalSummaryPage(page)
        await expect(personalSummaryPage.dateOfBirthAnswer()).toHaveText('30 November 1835')
      })
    })
  })
})
