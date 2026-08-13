import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../fixtures/test'
import { getRandomString } from '../../../jwt_helper'
import ALevelsPage from '../../../generated_pages/last_viewed_question_guidance_hub/a-levels.page'
import EducationSectionSummaryPage from '../../../generated_pages/last_viewed_question_guidance_hub/education-section-summary.page'
import GcsesPage from '../../../generated_pages/last_viewed_question_guidance_hub/gcses.page'
import HobbiesPage from '../../../generated_pages/last_viewed_question_guidance_hub/hobbies.page'
import PaidWorkPage from '../../../generated_pages/last_viewed_question_guidance_hub/paid-work.page'
import SportsPage from '../../../generated_pages/last_viewed_question_guidance_hub/sports.page'
import UnPaidWorkPage from '../../../generated_pages/last_viewed_question_guidance_hub/unpaid-work.page'
import WorkInterstitialPage from '../../../generated_pages/last_viewed_question_guidance_hub/work-interstitial.page'
import HubPage from '../../../base_pages/hub.page'

test.describe('Last viewed question guidance', () => {
  const resumableLaunchParams = {
    responseId: getRandomString(16),
    userId: 'test_user'
  }

  test.describe('Given the hub has a required section, which has not been completed', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Open survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_last_viewed_question_guidance_hub.json', resumableLaunchParams)
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When the respondent launches the survey, then last question guidance is not shown', async () => {
      const workInterstitialPage = new WorkInterstitialPage(page)
      await expect(page).toHaveURL(new RegExp(workInterstitialPage.url()))
      await expect(workInterstitialPage.lastViewedQuestionGuidance()).not.toBeVisible()
    })

    test('When the respondent saves and resumes from a section which is not started, then last question guidance is not shown', async () => {
      const workInterstitialPage = new WorkInterstitialPage(page)
      await workInterstitialPage.saveSignOut().click()
      await openQuestionnaire('test_last_viewed_question_guidance_hub.json', resumableLaunchParams)
      await page.waitForTimeout(100)
      await expect(page).toHaveURL(new RegExp(workInterstitialPage.url()))
      await expect(workInterstitialPage.lastViewedQuestionGuidance()).not.toBeVisible()
    })

    test('When the respondent saves and resumes from a section which is in progress, then last question guidance is shown', async () => {
      const paidWorkPage = new PaidWorkPage(page)
      const workInterstitialPage = new WorkInterstitialPage(page)
      await workInterstitialPage.submit().click()
      await paidWorkPage.saveSignOut().click()
      await openQuestionnaire('test_last_viewed_question_guidance_hub.json', resumableLaunchParams)
      const paidWorkGuidanceHref = await paidWorkPage.lastViewedQuestionGuidanceLink().getAttribute('href')
      expect(paidWorkGuidanceHref).toContain(workInterstitialPage.url())
      await expect(paidWorkPage.lastViewedQuestionGuidance()).toBeVisible()
    })
  })

  test.describe('Given the respondent has completed the required section and is on the hub', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Open survey and complete first section', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      const paidWorkPage = new PaidWorkPage(page)
      const unPaidWorkPage = new UnPaidWorkPage(page)
      const workInterstitialPage = new WorkInterstitialPage(page)
      await openQuestionnaire('test_last_viewed_question_guidance_hub.json')
      await workInterstitialPage.submit().click()
      await paidWorkPage.yes().click()
      await paidWorkPage.submit().click()
      await unPaidWorkPage.yes().click()
      await unPaidWorkPage.submit().click()
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When the respondent selects a section which is not started, then last question guidance is not shown', async () => {
      const gcsesPage = new GcsesPage(page)
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink('education-section').click()
      await expect(page).toHaveURL(new RegExp(gcsesPage.url()))
      await expect(gcsesPage.lastViewedQuestionGuidance()).not.toBeVisible()
    })

    test('When the respondent selects a section which is in progress, then last question guidance is shown', async () => {
      const aLevelsPage = new ALevelsPage(page)
      const gcsesPage = new GcsesPage(page)
      const hubPage = new HubPage(page)
      await hubPage.submit().click()
      await gcsesPage.yes().click()
      await gcsesPage.submit().click()
      await page.goto(hubPage.url())
      await hubPage.summaryRowLink('education-section').click()
      await expect(page).toHaveURL(new RegExp(aLevelsPage.url()))
      const aLevelsGuidanceHref = await aLevelsPage.lastViewedQuestionGuidanceLink().getAttribute('href')
      expect(aLevelsGuidanceHref).toContain(gcsesPage.url())
      await expect(aLevelsPage.lastViewedQuestionGuidance()).toBeVisible()
    })

    test('When the respondent selects a section which is complete , then last question guidance is not shown on the summary or any link clicked from the summary', async () => {
      const aLevelsPage = new ALevelsPage(page)
      const educationSectionSummaryPage = new EducationSectionSummaryPage(page)
      const hubPage = new HubPage(page)
      await aLevelsPage.yes().click()
      await aLevelsPage.submit().click()
      await expect(page).toHaveURL(new RegExp(educationSectionSummaryPage.url()))
      await expect(aLevelsPage.lastViewedQuestionGuidance()).not.toBeVisible()
      await educationSectionSummaryPage.submit().click()
      await hubPage.summaryRowLink('education-section').click()
      await expect(page).toHaveURL(new RegExp(educationSectionSummaryPage.url()))
      await educationSectionSummaryPage.alevelsAnswerEdit().click()
      await expect(aLevelsPage.lastViewedQuestionGuidance()).not.toBeVisible()
    })

    test('When the user clicks continue on the hub and it takes you to a section which is not started, then last question guidance is not shown', async () => {
      const hubPage = new HubPage(page)
      const sportsPage = new SportsPage(page)
      await page.goto(hubPage.url())
      await hubPage.submit().click()
      await expect(page).toHaveURL(new RegExp(sportsPage.url()))
      await expect(sportsPage.lastViewedQuestionGuidance()).not.toBeVisible()
    })

    test('When the user clicks continue on the hub and it takes you to a section which is in progress, then last question guidance is shown', async () => {
      const hobbiesPage = new HobbiesPage(page)
      const hubPage = new HubPage(page)
      const sportsPage = new SportsPage(page)
      await hubPage.submit().click()
      await sportsPage.yes().click()
      await sportsPage.submit().click()
      await page.goto(hubPage.url())
      await hubPage.submit().click()
      await expect(page).toHaveURL(new RegExp(hobbiesPage.url()))
      const hobbiesGuidanceHref = await hobbiesPage.lastViewedQuestionGuidanceLink().getAttribute('href')
      expect(hobbiesGuidanceHref).toContain(sportsPage.url())
      await expect(hobbiesPage.lastViewedQuestionGuidance()).toBeVisible()
    })

    test('When the user clicks continue on the hub and it takes you to a section which is complete but doesnt have a summary, then last question guidance is not shown', async () => {
      const hobbiesPage = new HobbiesPage(page)
      const hubPage = new HubPage(page)
      const sportsPage = new SportsPage(page)
      await hobbiesPage.yes().click()
      await hobbiesPage.submit().click()
      await hubPage.summaryRowLink('interests-section').click()
      await expect(page).toHaveURL(new RegExp(sportsPage.url()))
      await expect(sportsPage.lastViewedQuestionGuidance()).not.toBeVisible()
    })
  })
})
