import { createOpenQuestionnaire, test, expect } from '../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../fixtures/test'
import AccommodationDetailsSummaryBlockPage from '../../generated_pages/hub_and_spoke/accommodation-section-summary.page'
import AnyoneRelated from '../../generated_pages/hub_and_spoke/anyone-related.page'
import DoesAnyoneLiveHere from '../../generated_pages/hub_and_spoke/does-anyone-live-here.page'
import EmploymentStatusBlockPage from '../../generated_pages/hub_and_spoke/employment-status.page'
import EmploymentTypeBlockPage from '../../generated_pages/hub_and_spoke/employment-type.page'
import HouseholdSummary from '../../generated_pages/hub_and_spoke/household-section-summary.page'
import HowManyPeopleLiveHere from '../../generated_pages/hub_and_spoke/how-many-people-live-here.page'
import HubPage from '../../base_pages/hub.page'
import ProxyPage from '../../generated_pages/hub_and_spoke/proxy.page'
import RelationshipsSummary from '../../generated_pages/hub_and_spoke/relationships-section-summary.page'
import ListCollectorSectionSummaryPage from '../../generated_pages/hub_section_required_with_repeat/list-collector-section-summary.page'
import ProxyRepeatPage from '../../generated_pages/hub_section_required_with_repeat/proxy.page'

import DateOfBirthPage from '../../generated_pages/hub_section_required_with_repeat/date-of-birth.page'
import PrimaryPersonListCollectorPage from '../../generated_pages/hub_section_required_with_repeat/primary-person-list-collector.page'
import PrimaryPersonListCollectorAddPage from '../../generated_pages/hub_section_required_with_repeat/primary-person-list-collector-add.page'
import ListCollectorPage from '../../generated_pages/hub_section_required_with_repeat/list-collector.page'
import ListCollectorAddPage from '../../generated_pages/hub_section_required_with_repeat/list-collector-add.page'
import RepeatingSummaryPage from '../../generated_pages/hub_section_required_with_repeat/personal-details-section-summary.page'

test.describe('Feature: Hub and Spoke', () => {
  const hubAndSpokeSchema = 'test_hub_and_spoke.json'

  test.describe('Given I am completing the test_hub_context schema,', () => {
    test.beforeEach('load the survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire(hubAndSpokeSchema)
    })

    test('When a user first views the Hub, The Hub should be in a continue state', async ({ page }) => {
      const hubPage = new HubPage(page)
      await expect(hubPage.submit()).toHaveText('Continue')
      await expect(hubPage.heading()).toHaveText('Choose another section to complete')
      await expect(hubPage.summaryRowState('employment-section')).toHaveText('Not started')
      await expect(hubPage.summaryRowState('accommodation-section')).toHaveText('Not started')
      await expect(hubPage.summaryRowState('household-section')).toHaveText('Not started')
    })

    test('When a user utilises a screen reader, The visually hidden text read aloud should be the state and name of each section in the hub', async ({
      page
    }) => {
      const hubPage = new HubPage(page)
      await expect(hubPage.summaryRowLink('employment-section')).toContainText('Start section: Employment')
      await expect(hubPage.summaryRowLink('accommodation-section')).toContainText('Start section: Accommodation')
      await expect(hubPage.summaryRowLink('household-section')).toContainText('Start section: Household residents')
    })

    test('When a user views the Hub, any section with show_on_hub set to true should appear', async ({ page }) => {
      const hubPage = new HubPage(page)
      await expect(hubPage.summaryItems()).toContainText('Employment')
      await expect(hubPage.summaryItems()).toContainText('Accommodation')
      await expect(hubPage.summaryItems()).toContainText('Household residents')
    })

    test('When a user views the Hub, any section with show_on_hub set to false should not appear', async ({ page }) => {
      const hubPage = new HubPage(page)
      await expect(hubPage.summaryItems()).not.toContainText('Relationships')
    })

    test("When the user click the 'Save and sign out' button then they should be redirected to the correct log out url", async ({ page }) => {
      const hubPage = new HubPage(page)
      await hubPage.saveSignOut().click()
      await expect(page).toHaveURL(/\/signed-out/)
    })

    test.skip('When a user views the Hub, Then the page title should be Choose another section to complete', async ({ page }) => {
      // To be investigated. This test is skipped because the page title is not consistently ready in time during GitHub Actions runs, causing flakiness.
      await expect(page).toHaveTitle('Choose another section to complete - Test Hub & Spoke')
    })
  })

  test.describe('Given a user has not started a section', () => {
    test.beforeEach('Open survey', async ({ page, openQuestionnaire }) => {
      const hubPage = new HubPage(page)
      await openQuestionnaire(hubAndSpokeSchema)
      await expect(hubPage.summaryRowState('employment-section')).toHaveText('Not started')
      await expect(hubPage.summaryRowState('accommodation-section')).toHaveText('Not started')
      await expect(hubPage.summaryRowState('household-section')).toHaveText('Not started')
      await expect(hubPage.summaryRowLink('employment-section')).toContainText('Start section: Employment')
      await expect(hubPage.summaryRowLink('accommodation-section')).toContainText('Start section: Accommodation')
      await expect(hubPage.summaryRowLink('household-section')).toContainText('Start section: Household residents')
    })

    test('When the user starts a section, Then the first question in the section should be displayed', async ({ page }) => {
      const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
      const hubPage = new HubPage(page)
      await hubPage.submit().click()
      await expect(page).toHaveURL(new RegExp(employmentStatusBlockPage.url()))
    })

    test('When the user starts a section and clicks the Previous link on the first question, Then they should be taken back to the Hub', async ({ page }) => {
      const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
      const hubPage = new HubPage(page)
      await hubPage.submit().click()
      await employmentStatusBlockPage.previous().click()
      await verifyUrlPathIs(page, hubPage.url())
    })
  })

  test.describe('Given a user has started a section', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Start section', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
      const hubPage = new HubPage(page)
      await openQuestionnaire(hubAndSpokeSchema)
      await hubPage.summaryRowLink('employment-section').click()
      await employmentStatusBlockPage.exclusiveNoneOfTheseApply().click()
      await employmentStatusBlockPage.submit().click()
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When the user returns to the Hub, Then the Hub should be in a continue state', async () => {
      const hubPage = new HubPage(page)
      await page.goto(hubPage.url())
      await expect(hubPage.submit()).toHaveText('Continue')
      await expect(hubPage.heading()).toHaveText('Choose another section to complete')
    })

    test("When the user returns to the Hub, Then the section should be marked as 'Partially completed'", async () => {
      const hubPage = new HubPage(page)
      await page.goto(hubPage.url())
      await expect(hubPage.summaryRowState('employment-section')).toHaveText('Partially completed')
      await expect(hubPage.summaryRowLink('employment-section')).toContainText('Continue with section: Employment')
    })

    test('When the user returns to the Hub and restarts the same section, Then they should be redirected to the first incomplete block', async () => {
      const employmentTypeBlockPage = new EmploymentTypeBlockPage(page)
      const hubPage = new HubPage(page)
      await page.goto(hubPage.url())
      await hubPage.summaryRowLink('employment-section').click()
      await expect(page).toHaveURL(new RegExp(employmentTypeBlockPage.url()))
    })
  })

  test.describe('Given a user has completed a section', () => {
    test.beforeEach('Complete section', async ({ page, openQuestionnaire }) => {
      const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
      const employmentTypeBlockPage = new EmploymentTypeBlockPage(page)
      const hubPage = new HubPage(page)
      await openQuestionnaire(hubAndSpokeSchema)
      await hubPage.summaryRowLink('employment-section').click()
      await employmentStatusBlockPage.exclusiveNoneOfTheseApply().click()
      await employmentStatusBlockPage.submit().click()
      await employmentTypeBlockPage.studying().click()
    })

    test("When the user clicks the 'Continue' button, it should return them to the hub", async ({ page }) => {
      const employmentTypeBlockPage = new EmploymentTypeBlockPage(page)
      const hubPage = new HubPage(page)
      await employmentTypeBlockPage.submit().click()
      await verifyUrlPathIs(page, hubPage.url())
    })

    test('When the user returns to the Hub, Then the Hub should be in a continue state', async ({ page }) => {
      const employmentTypeBlockPage = new EmploymentTypeBlockPage(page)
      const hubPage = new HubPage(page)
      await employmentTypeBlockPage.submit().click()
      await expect(hubPage.submit()).toHaveText('Continue')
      await expect(hubPage.heading()).toHaveText('Choose another section to complete')
    })

    test("When the user returns to the Hub, Then the section should be marked as 'Completed'", async ({ page }) => {
      const employmentTypeBlockPage = new EmploymentTypeBlockPage(page)
      const hubPage = new HubPage(page)
      await employmentTypeBlockPage.submit().click()
      await expect(hubPage.summaryRowState('employment-section')).toHaveText('Completed')
      await expect(hubPage.summaryRowLink('employment-section')).toContainText('View answers: Employment')
    })

    test("When the user returns to the Hub and clicks the 'View answers' link on the Hub, if this no summary they are returned to the first block", async ({
      page
    }) => {
      const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
      const employmentTypeBlockPage = new EmploymentTypeBlockPage(page)
      const hubPage = new HubPage(page)
      await employmentTypeBlockPage.submit().click()
      await hubPage.summaryRowLink('employment-section').click()
      await expect(page).toHaveURL(new RegExp(employmentStatusBlockPage.url()))
    })

    test('When the user returns to the Hub and continues, Then they should progress to the next section', async ({ page }) => {
      const employmentTypeBlockPage = new EmploymentTypeBlockPage(page)
      const hubPage = new HubPage(page)
      const proxyPage = new ProxyPage(page)
      await employmentTypeBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(hubPage.url()))
      await hubPage.submit().click()
      await expect(page).toHaveURL(new RegExp(proxyPage.url()))
    })
  })

  test.describe('Given a user has completed a section and is on the Hub page', () => {
    test.beforeEach('Complete section', async ({ page, openQuestionnaire }) => {
      const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
      const hubPage = new HubPage(page)
      await openQuestionnaire(hubAndSpokeSchema)
      await hubPage.summaryRowLink('employment-section').click()
      await employmentStatusBlockPage.workingAsAnEmployee().click()
      await employmentStatusBlockPage.submit().click()

      await expect(hubPage.summaryRowState('employment-section')).toHaveText('Completed')
    })

    test(
      "When the user clicks the 'View answers' link and incompletes the section, " +
        "Then they the should be taken to the next incomplete question on 'Continue",
      async ({ page }) => {
        const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
        const employmentTypeBlockPage = new EmploymentTypeBlockPage(page)
        const hubPage = new HubPage(page)
        await hubPage.summaryRowLink('employment-section').click()
        await expect(page).toHaveURL(new RegExp(employmentStatusBlockPage.url()))
        await employmentStatusBlockPage.exclusiveNoneOfTheseApply().click()
        await employmentStatusBlockPage.submit().click()
        await expect(page).toHaveURL(new RegExp(employmentTypeBlockPage.url()))
      }
    )

    test(
      "When the user clicks the 'View answers' link and incompletes the section and returns to the hub, " +
        "Then the section should be marked as 'Partially completed'",
      async ({ page }) => {
        const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
        const hubPage = new HubPage(page)
        await hubPage.summaryRowLink('employment-section').click()
        await expect(page).toHaveURL(new RegExp(employmentStatusBlockPage.url()))
        await employmentStatusBlockPage.exclusiveNoneOfTheseApply().click()
        await employmentStatusBlockPage.submit().click()
        await page.goto(hubPage.url())
        await verifyUrlPathIs(page, hubPage.url())
        await expect(hubPage.summaryRowState('employment-section')).toHaveText('Partially completed')
        await expect(hubPage.summaryRowLink('employment-section')).toContainText('Continue with section: Employment')
      }
    )
  })

  test.describe('Given a user has completed all sections', () => {
    test.beforeEach('Complete all sections', async ({ page, openQuestionnaire }) => {
      const accommodationDetailsSummaryBlockPage = new AccommodationDetailsSummaryBlockPage(page)
      const anyoneRelated = new AnyoneRelated(page)
      const doesAnyoneLiveHere = new DoesAnyoneLiveHere(page)
      const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
      const employmentTypeBlockPage = new EmploymentTypeBlockPage(page)
      const householdSummary = new HouseholdSummary(page)
      const hubPage = new HubPage(page)
      const proxyPage = new ProxyPage(page)
      const relationshipsSummary = new RelationshipsSummary(page)
      await openQuestionnaire(hubAndSpokeSchema)
      await hubPage.summaryRowLink('employment-section').click()
      await employmentStatusBlockPage.exclusiveNoneOfTheseApply().click()
      await employmentStatusBlockPage.submit().click()
      await employmentTypeBlockPage.studying().click()
      await employmentTypeBlockPage.submit().click()
      await hubPage.submit().click()
      await proxyPage.yes().click()
      await proxyPage.submit().click()
      await accommodationDetailsSummaryBlockPage.submit().click()
      await hubPage.submit().click()
      await doesAnyoneLiveHere.no().click()
      await doesAnyoneLiveHere.submit().click()
      await householdSummary.submit().click()
      await hubPage.submit().click()
      await anyoneRelated.yes().click()
      await anyoneRelated.submit().click()
      await relationshipsSummary.submit().click()
    })

    test('It should return them to the hub', async ({ page }) => {
      const hubPage = new HubPage(page)
      await verifyUrlPathIs(page, hubPage.url())
    })

    test('When the user returns to the Hub, Then the Hub should be in a completed state', async ({ page }) => {
      const hubPage = new HubPage(page)
      await expect(hubPage.submit()).toHaveText('Submit survey')
      await expect(hubPage.heading()).toHaveText('Submit survey')
    })

    test('When the user submits, it should show the thankyou page', async ({ page }) => {
      const hubPage = new HubPage(page)
      await hubPage.submit().click()
      await expect(page).toHaveURL(/thank-you/)
    })
  })

  test.describe('Given a user opens a schema with required sections', () => {
    test.beforeEach('Load survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_hub_complete_sections.json')
    })

    test('The hub should not show first of all', async ({ page }) => {
      const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
      await expect(page).toHaveURL(new RegExp(employmentStatusBlockPage.url()))
    })

    test('The hub should only display when required sections are complete', async ({ page }) => {
      const employmentStatusBlockPage = new EmploymentStatusBlockPage(page)
      const employmentTypeBlockPage = new EmploymentTypeBlockPage(page)
      const hubPage = new HubPage(page)
      await employmentStatusBlockPage.exclusiveNoneOfTheseApply().click()
      await employmentStatusBlockPage.submit().click()
      await employmentTypeBlockPage.studying().click()
      await employmentTypeBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(hubPage.url()))
    })
  })

  test.describe('Given a user opens a schema with hub required sections based on a repeating section', () => {
    test.beforeEach('Load survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_hub_section_required_with_repeat.json')
    })

    test('When all the repeating sections are complete, Then the hub should be displayed', async ({ page }) => {
      const dateOfBirthPage = new DateOfBirthPage(page)
      const hubPage = new HubPage(page)
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const listCollectorSectionSummaryPage = new ListCollectorSectionSummaryPage(page)
      const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      const proxyRepeatPage = new ProxyRepeatPage(page)
      const repeatingSummaryPage = new RepeatingSummaryPage(page)
      await primaryPersonListCollectorPage.yes().click()
      await primaryPersonListCollectorPage.submit().click()
      await primaryPersonListCollectorAddPage.firstName().fill('Marcus')
      await primaryPersonListCollectorAddPage.lastName().fill('Twin')
      await primaryPersonListCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('John')
      await listCollectorAddPage.lastName().fill('Doe')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await listCollectorSectionSummaryPage.submit().click()

      // Try to access the hub
      await page.goto(hubPage.url())

      // Redirected to the repeating sections to be completed
      await proxyRepeatPage.yes().click()
      await proxyRepeatPage.submit().click()
      await dateOfBirthPage.day().fill('12')
      await dateOfBirthPage.month().fill('4')
      await dateOfBirthPage.year().fill('2021')
      await dateOfBirthPage.submit().click()
      await repeatingSummaryPage.submit().click()
      await proxyRepeatPage.yes().click()
      await proxyRepeatPage.submit().click()
      await dateOfBirthPage.day().fill('1')
      await dateOfBirthPage.month().fill('1')
      await dateOfBirthPage.year().fill('2000')
      await repeatingSummaryPage.submit().click()
      await expect(page).toHaveURL(new RegExp(hubPage.url()))
    })

    test('When the repeating sections are incomplete, Then the hub should not be displayed', async ({ page }) => {
      const hubPage = new HubPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const listCollectorSectionSummaryPage = new ListCollectorSectionSummaryPage(page)
      const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      const proxyRepeatPage = new ProxyRepeatPage(page)
      await primaryPersonListCollectorPage.yes().click()
      await primaryPersonListCollectorPage.submit().click()
      await primaryPersonListCollectorAddPage.firstName().fill('Marcus')
      await primaryPersonListCollectorAddPage.lastName().fill('Twin')
      await primaryPersonListCollectorAddPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await listCollectorSectionSummaryPage.submit().click()

      // Don't complete all the repeating questions
      await proxyRepeatPage.yes().click()
      await proxyRepeatPage.submit().click()

      await page.goto(hubPage.url())
      await expect(page).toHaveURL(/date-of-birth/)
    })
  })

  test.describe("Given a section is complete and the user has been returned to a section summary by clicking the 'View answers' link ", () => {
    test.beforeEach('Complete section', async ({ page, openQuestionnaire }) => {
      const doesAnyoneLiveHere = new DoesAnyoneLiveHere(page)
      const householdSummary = new HouseholdSummary(page)
      const hubPage = new HubPage(page)
      await openQuestionnaire(hubAndSpokeSchema)
      await hubPage.summaryRowLink('household-section').click()
      await doesAnyoneLiveHere.no().click()
      await doesAnyoneLiveHere.submit().click()
      await householdSummary.submit().click()
      await expect(hubPage.summaryRowLink('household-section')).toContainText('View answers: Household residents')
    })

    test('When there are no changes, continue returns directly to the hub', async ({ page }) => {
      const householdSummary = new HouseholdSummary(page)
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink('household-section').click()
      await householdSummary.submit().click()
      await verifyUrlPathIs(page, hubPage.url())
      await expect(hubPage.summaryRowLink('household-section')).toContainText('View answers: Household residents')
    })

    test('When there are changes, which would set the section to in_progress it routes accordingly', async ({ page }) => {
      const doesAnyoneLiveHere = new DoesAnyoneLiveHere(page)
      const householdSummary = new HouseholdSummary(page)
      const howManyPeopleLiveHere = new HowManyPeopleLiveHere(page)
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink('household-section').click()
      await householdSummary.doesAnyoneLiveHereAnswerEdit().click()
      await doesAnyoneLiveHere.yes().click()
      await doesAnyoneLiveHere.submit().click()
      await householdSummary.submit().click()
      await expect(page).toHaveURL(new RegExp(howManyPeopleLiveHere.url()))
    })
  })
})

async function verifyUrlPathIs (page: Page, expectedUrlPath: string): Promise<void> {
  // Hub and Spoke URLs are "/questionnaire/", so we need strict checking of the URL path
  const actualUrlPath = new URL(await page.url()).pathname
  await expect(actualUrlPath).toBe(expectedUrlPath)
}
