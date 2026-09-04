import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { BrowserContext, Page } from '../../../fixtures/test'
import ConfirmDateOfBirthPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/confirm-dob.page'
import DateOfBirthPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/date-of-birth.page'
import FirstListCollectorAddPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/list-collector-add.page'
import FirstListCollectorPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/list-collector.page'
import HubPage from '../../../base_pages/hub.page'
import PersonalDetailsSummaryPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/personal-details-section-summary.page'
import PrimaryPersonAddPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/primary-person-list-collector-add.page'
import PrimaryPersonPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/primary-person-list-collector.page'
import ProxyPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/proxy.page'
import SecondListCollectorAddPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/another-list-collector-block-add.page'
import SecondListCollectorInterstitialPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/next-interstitial.page'
import SecondListCollectorPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/another-list-collector-block.page'
import SectionSummaryPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/section-summary.page'
import SexPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/sex.page'
import VisitorsDateOfBirthPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-date-of-birth.page'
import VisitorsListCollectorAddPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-block-add.page'
import VisitorsListCollectorPage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-block.page'
import VisitorsListCollectorRemovePage from '../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-block-remove.page'

test.describe('Feature: Repeating Sections with Hub and Spoke', () => {
  test.describe.configure({ mode: 'serial' })

  test.describe('Given the user has added some members to the household and is on the Hub', () => {
    let context: BrowserContext
    let page: Page
    let openQuestionnaire: ReturnType<typeof createOpenQuestionnaire>

    test.beforeAll('Open survey and add household members', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      const firstListCollectorAddPage = new FirstListCollectorAddPage(page)
      const firstListCollectorPage = new FirstListCollectorPage(page)
      const hubPage = new HubPage(page)
      const primaryPersonAddPage = new PrimaryPersonAddPage(page)
      const primaryPersonPage = new PrimaryPersonPage(page)
      const secondListCollectorAddPage = new SecondListCollectorAddPage(page)
      const secondListCollectorInterstitialPage = new SecondListCollectorInterstitialPage(page)
      const secondListCollectorPage = new SecondListCollectorPage(page)
      const visitorsListCollectorPage = new VisitorsListCollectorPage(page)
      await openQuestionnaire('test_repeating_sections_with_hub_and_spoke.json')
      // Accept cookies, this is done due to headless window size where cookie banner
      // is pushing the submit button outside window
      await hubPage.acceptCookies().click()
      // Ensure we are on the Hub
      await expect(page).toHaveURL(new RegExp(hubPage.url()))
      // Ensure the first section is not started
      await expect(hubPage.summaryRowState('section')).toHaveText('Not started')
      // Start first section to add household members
      await hubPage.summaryRowLink('section').click()

      // Add a primary person
      await primaryPersonPage.yes().click()
      await primaryPersonPage.submit().click()
      await primaryPersonAddPage.firstName().fill('Marcus')
      await primaryPersonAddPage.lastName().fill('Twin')
      await primaryPersonPage.submit().click()

      // Add other household members (First list collector)
      await firstListCollectorPage.yes().click()
      await firstListCollectorPage.submit().click()
      await firstListCollectorAddPage.firstName().fill('Jean')
      await firstListCollectorAddPage.lastName().fill('Clemens')
      await firstListCollectorAddPage.submit().click()

      await firstListCollectorPage.yes().click()
      await firstListCollectorPage.submit().click()
      await firstListCollectorAddPage.firstName().fill('Samuel')
      await firstListCollectorAddPage.lastName().fill('Clemens')
      await firstListCollectorAddPage.submit().click()

      // Go to second list collector
      await firstListCollectorPage.no().click()
      await firstListCollectorPage.submit().click()
      await secondListCollectorInterstitialPage.submit().click()

      // Add other household members (Second list collector)
      await secondListCollectorPage.yes().click()
      await secondListCollectorPage.submit().click()
      await secondListCollectorAddPage.firstName().fill('John')
      await secondListCollectorAddPage.lastName().fill('Doe')
      await secondListCollectorAddPage.submit().click()

      // Go back to the Hub
      await secondListCollectorPage.no().click()
      await secondListCollectorPage.submit().click()
      await visitorsListCollectorPage.no().click()
      await visitorsListCollectorPage.submit().click()
    })

    test.afterAll(async () => {
      await context.close()
    })

    test.beforeEach('Navigate to the Hub', async () => {
      const hubPage = new HubPage(page)
      await page.goto(hubPage.url())
    })

    test('Then a section for each household member should be displayed', async () => {
      const hubPage = new HubPage(page)
      await expect(page).toHaveURL(new RegExp(hubPage.url()))

      await expect(hubPage.summaryRowState('section')).toHaveText('Completed')
      await expect(hubPage.summaryRowTitle('personal-details-section-1')).toContainText('Marcus Twin')
      await expect(hubPage.summaryRowState('personal-details-section-1')).toHaveText('Not started')
      await expect(hubPage.summaryRowState('personal-details-section-2')).toHaveText('Not started')
      await expect(hubPage.summaryRowTitle('personal-details-section-2')).toContainText('Jean Clemens')
      await expect(hubPage.summaryRowState('personal-details-section-3')).toHaveText('Not started')
      await expect(hubPage.summaryRowTitle('personal-details-section-3')).toContainText('Samuel Clemens')
      await expect(hubPage.summaryRowState('personal-details-section-4')).toHaveText('Not started')
      await expect(hubPage.summaryRowTitle('personal-details-section-4')).toContainText('John Doe')

      await expect(hubPage.summaryRowState('section-5')).not.toBeVisible()
    })

    test('When the user starts a repeating section and clicks the Previous link on the first question, Then they should be taken back to the Hub', async () => {
      const hubPage = new HubPage(page)
      const proxyPage = new ProxyPage(page)
      await hubPage.summaryRowLink('personal-details-section-2').click()
      await proxyPage.previous().click()

      await expect(page).toHaveURL(new RegExp(hubPage.url()))
    })

    test("When the user partially completes a repeating section, Then that section should be marked as 'Partially completed' on the Hub", async () => {
      const confirmDateOfBirthPage = new ConfirmDateOfBirthPage(page)
      const dateOfBirthPage = new DateOfBirthPage(page)
      const hubPage = new HubPage(page)
      const proxyPage = new ProxyPage(page)
      await hubPage.summaryRowLink('personal-details-section-1').click()
      await proxyPage.yes().click()
      await proxyPage.submit().click()

      await dateOfBirthPage.day().fill('01')
      await dateOfBirthPage.month().fill('03')
      await dateOfBirthPage.year().fill('2000')
      await dateOfBirthPage.submit().click()

      await confirmDateOfBirthPage.confirmDateOfBirthYesPersonNameIsAgeOld().click()
      await confirmDateOfBirthPage.submit().click()

      await page.goto(hubPage.url())

      await expect(page).toHaveURL(new RegExp(hubPage.url()))
      await expect(hubPage.summaryRowState('personal-details-section-1')).toHaveText('Partially completed')
    })

    test('When the user continues with a partially completed repeating section, Then they are taken to the first incomplete block', async () => {
      const hubPage = new HubPage(page)
      const sexPage = new SexPage(page)
      await hubPage.summaryRowLink('personal-details-section-1').click()

      await expect(sexPage.questionText()).toHaveText('What is Marcus Twin’s sex?')
    })

    test("When the user completes a repeating section, Then that section should be marked as 'Completed' on the Hub", async () => {
      const confirmDateOfBirthPage = new ConfirmDateOfBirthPage(page)
      const dateOfBirthPage = new DateOfBirthPage(page)
      const hubPage = new HubPage(page)
      const personalDetailsSummaryPage = new PersonalDetailsSummaryPage(page)
      const proxyPage = new ProxyPage(page)
      const sexPage = new SexPage(page)
      await hubPage.summaryRowLink('personal-details-section-2').click()
      await proxyPage.yes().click()
      await proxyPage.submit().click()

      await dateOfBirthPage.day().fill('09')
      await dateOfBirthPage.month().fill('09')
      await dateOfBirthPage.year().fill('1995')
      await dateOfBirthPage.submit().click()

      await confirmDateOfBirthPage.confirmDateOfBirthYesPersonNameIsAgeOld().click()
      await confirmDateOfBirthPage.submit().click()

      await sexPage.female().click()
      await sexPage.submit().click()

      await personalDetailsSummaryPage.submit().click()

      await expect(page).toHaveURL(new RegExp(hubPage.url()))
      await expect(hubPage.summaryRowState('personal-details-section-2')).toHaveText('Completed')
    })

    test("When the user clicks 'View answers' for a completed repeating section, Then they are taken to the summary", async () => {
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink('personal-details-section-2').click()
      await expect(page).toHaveURL(/\/sections\/personal-details-section/)
    })

    test('When the user views the summary for a repeating section, Then the page title is shown', async () => {
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink('personal-details-section-2').click()
      await expect(page).toHaveTitle('… - Test Repeating Sections with Hub & Spoke')
    })

    test('When the user adds 2 visitors to the household then a section for each visitor should be display on the hub', async () => {
      const hubPage = new HubPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      const visitorsListCollectorAddPage = new VisitorsListCollectorAddPage(page)
      const visitorsListCollectorPage = new VisitorsListCollectorPage(page)
      // Ensure no other sections exist
      await expect(hubPage.summaryRowState('personal-details-section-5')).not.toBeVisible()
      await expect(hubPage.summaryRowState('visitors-section-1')).not.toBeVisible()

      // Start section for first visitor
      await hubPage.summaryRowLink('section').click()

      // Add first visitor
      await sectionSummaryPage.visitorListAddLink().click()
      await visitorsListCollectorAddPage.visitorFirstName().fill('Joe')
      await visitorsListCollectorAddPage.visitorLastName().fill('Public')
      await visitorsListCollectorAddPage.submit().click()
      await expect(page).toHaveURL(/\/questionnaire\/visitors-block/)

      // Add second visitor
      await visitorsListCollectorPage.yes().click()
      await visitorsListCollectorPage.submit().click()
      await visitorsListCollectorAddPage.visitorFirstName().fill('Yvonne')
      await visitorsListCollectorAddPage.visitorLastName().fill('Yoe')
      await visitorsListCollectorAddPage.submit().click()

      // Exit the visitors list collector
      await visitorsListCollectorPage.no().click()
      await visitorsListCollectorPage.submit().click()

      await sectionSummaryPage.submit().click()

      await expect(hubPage.summaryRowState('visitors-section-1')).toHaveText('Not started')
      await expect(hubPage.summaryRowTitle('visitors-section-1')).toContainText('Joe Public')
      await expect(hubPage.summaryRowState('visitors-section-2')).toHaveText('Not started')
      await expect(hubPage.summaryRowTitle('visitors-section-2')).toContainText('Yvonne Yoe')

      await expect(hubPage.summaryRowState('visitors-section-3')).not.toBeVisible()
    })

    test("When the user clicks 'Continue' from the Hub, Then they should progress to the first incomplete section", async () => {
      const confirmDateOfBirthPage = new ConfirmDateOfBirthPage(page)
      const hubPage = new HubPage(page)
      await hubPage.submit().click()
      await expect(confirmDateOfBirthPage.questionText()).toHaveText('What is Marcus Twin’s sex?')
    })

    test('When the user answers on their behalf, Then they are shown the non proxy question variant', async () => {
      const confirmDateOfBirthPage = new ConfirmDateOfBirthPage(page)
      const dateOfBirthPage = new DateOfBirthPage(page)
      const hubPage = new HubPage(page)
      const proxyPage = new ProxyPage(page)
      const sexPage = new SexPage(page)
      await hubPage.summaryRowLink('personal-details-section-4').click()
      await proxyPage.noIMAnsweringForMyself().click()
      await proxyPage.submit().click()

      await dateOfBirthPage.day().fill('07')
      await dateOfBirthPage.month().fill('07')
      await dateOfBirthPage.year().fill('1970')
      await dateOfBirthPage.submit().click()

      await confirmDateOfBirthPage.confirmDateOfBirthYesIAmAgeOld().click()
      await confirmDateOfBirthPage.submit().click()

      await expect(sexPage.questionText()).toHaveText('What is your sex?')
    })

    test('When the user answers on on behalf of someone else, Then they are shown the proxy question variant for the relevant repeating section', async () => {
      const confirmDateOfBirthPage = new ConfirmDateOfBirthPage(page)
      const dateOfBirthPage = new DateOfBirthPage(page)
      const hubPage = new HubPage(page)
      const proxyPage = new ProxyPage(page)
      const sexPage = new SexPage(page)
      await hubPage.summaryRowLink('personal-details-section-3').click()
      await proxyPage.yes().click()
      await proxyPage.submit().click()

      await dateOfBirthPage.day().fill('11')
      await dateOfBirthPage.month().fill('11')
      await dateOfBirthPage.year().fill('1990')
      await dateOfBirthPage.submit().click()

      await confirmDateOfBirthPage.confirmDateOfBirthYesPersonNameIsAgeOld().click()
      await confirmDateOfBirthPage.submit().click()
      await expect(sexPage.questionText()).toHaveText('What is Samuel Clemens’ sex?')
    })

    test('When the user completes all sections, Then the Hub should be in the completed state', async () => {
      const hubPage = new HubPage(page)
      const personalDetailsSummaryPage = new PersonalDetailsSummaryPage(page)
      const sexPage = new SexPage(page)
      const visitorsDateOfBirthPage = new VisitorsDateOfBirthPage(page)
      // Complete remaining sections
      await hubPage.submit().click()
      await sexPage.male().click()
      await sexPage.submit().click()
      await personalDetailsSummaryPage.submit().click()

      await hubPage.submit().click()
      await sexPage.submit().click()
      await personalDetailsSummaryPage.submit().click()

      await hubPage.submit().click()
      await sexPage.female().click()
      await sexPage.submit().click()
      await personalDetailsSummaryPage.submit().click()

      await hubPage.submit().click()
      await visitorsDateOfBirthPage.day().fill('03')
      await visitorsDateOfBirthPage.month().fill('09')
      await visitorsDateOfBirthPage.year().fill('1975')
      await visitorsDateOfBirthPage.submit().click()

      await hubPage.submit().click()
      await visitorsDateOfBirthPage.day().fill('31')
      await visitorsDateOfBirthPage.month().fill('07')
      await visitorsDateOfBirthPage.year().fill('1999')
      await visitorsDateOfBirthPage.submit().click()

      await expect(hubPage.submit()).toHaveText('Submit survey')
      await expect(hubPage.heading()).toHaveText('Submit survey')
    })

    test('When the user adds a new visitor, Then the Hub should not be in the completed state', async () => {
      const hubPage = new HubPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      const visitorsListCollectorAddPage = new VisitorsListCollectorAddPage(page)
      const visitorsListCollectorPage = new VisitorsListCollectorPage(page)
      await hubPage.summaryRowLink('section').click()

      // Add another visitor
      await sectionSummaryPage.visitorListAddLink().click()
      await visitorsListCollectorAddPage.visitorFirstName().fill('Anna')
      await visitorsListCollectorAddPage.visitorLastName().fill('Doe')
      await visitorsListCollectorAddPage.submit().click()

      await visitorsListCollectorPage.no().click()
      await visitorsListCollectorPage.submit().click()

      await sectionSummaryPage.submit().click()

      // New visitor added to hub
      await expect(hubPage.summaryRowState('visitors-section-3')).toHaveText('Not started')
      await expect(hubPage.summaryRowState('visitors-section-3')).toBeVisible()

      await expect(hubPage.submit()).not.toContainText('Submit survey')
      await expect(hubPage.submit()).toHaveText('Continue')

      await expect(hubPage.heading()).not.toContainText('Submit survey')
      await expect(hubPage.heading()).toHaveText('Choose another section to complete')
    })

    test('When the user removes a visitor, Then their section is not longer displayed on he Hub', async () => {
      const hubPage = new HubPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      const visitorsListCollectorPage = new VisitorsListCollectorPage(page)
      const visitorsListCollectorRemovePage = new VisitorsListCollectorRemovePage(page)
      // Ensure final householder exists
      await expect(hubPage.summaryRowState('visitors-section-3')).toBeVisible()

      await hubPage.summaryRowLink('section').click()

      // Remove final visitor
      await sectionSummaryPage.visitorListRemoveLink(3).click()

      await visitorsListCollectorRemovePage.yes().click()
      await visitorsListCollectorPage.submit().click()
      await sectionSummaryPage.submit().click()

      // Ensure final householder no longer exists
      await expect(hubPage.summaryRowState('visitors-section-3')).not.toBeVisible()
    })

    test('When the user submits, it should show the thank you page', async () => {
      const hubPage = new HubPage(page)
      await hubPage.submit().click()
      await expect(page).toHaveURL(/thank-you/)
    })
  })
})
