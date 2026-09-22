import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../fixtures/test'
import { getRandomString } from '../../../jwt_helper'
import AddressConfirmationPage from '../../../generated_pages/last_viewed_question_guidance/address-confirmation.page'
import HouseholdInterstitialPage from '../../../generated_pages/last_viewed_question_guidance/household-interstitial.page'
import PrimaryPersonListCollectorPage from '../../../generated_pages/last_viewed_question_guidance/primary-person-list-collector.page'

test.describe('Last viewed question guidance', () => {
  const resumableLaunchParams = {
    responseId: getRandomString(16),
    userId: 'test_user'
  }

  test.describe('Given the last viewed question guidance questionnaire', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Open survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_last_viewed_question_guidance.json', resumableLaunchParams)
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When the respondent first launches the survey, then last question guidance is not shown', async () => {
      const householdInterstitialPage = new HouseholdInterstitialPage(page)
      await expect(page).toHaveURL(new RegExp(householdInterstitialPage.url()))
      await expect(householdInterstitialPage.lastViewedQuestionGuidance()).not.toBeVisible()
    })

    test('When the respondent resumes on the first block of a section, then last question guidance is not shown', async () => {
      const householdInterstitialPage = new HouseholdInterstitialPage(page)
      await householdInterstitialPage.saveSignOut().click()
      await openQuestionnaire('test_last_viewed_question_guidance.json', resumableLaunchParams)
      await page.waitForTimeout(100)
      await expect(page).toHaveURL(new RegExp(householdInterstitialPage.url()))
      await expect(householdInterstitialPage.lastViewedQuestionGuidance()).not.toBeVisible()
    })

    test('When the respondent saves and resumes from a section which is in progress, then last question guidance is shown', async () => {
      const addressConfirmationPage = new AddressConfirmationPage(page)
      const householdInterstitialPage = new HouseholdInterstitialPage(page)
      await householdInterstitialPage.submit().click()
      await addressConfirmationPage.saveSignOut().click()
      await openQuestionnaire('test_last_viewed_question_guidance.json', resumableLaunchParams)
      await page.waitForTimeout(100)
      await expect(page).toHaveURL(new RegExp(addressConfirmationPage.url()))
      const addressGuidanceHref = await addressConfirmationPage.lastViewedQuestionGuidanceLink().getAttribute('href')
      expect(addressGuidanceHref).toContain(householdInterstitialPage.url())
      await expect(addressConfirmationPage.lastViewedQuestionGuidance()).toBeVisible()
    })

    test('When the respondent answers the question and saves and continues, then last question guidance is not shown on the next question', async () => {
      const addressConfirmationPage = new AddressConfirmationPage(page)
      const householdInterstitialPage = new HouseholdInterstitialPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      await addressConfirmationPage.yes().click()
      await addressConfirmationPage.submit().click()
      await expect(page).toHaveURL(new RegExp(primaryPersonListCollectorPage.url()))
      await expect(householdInterstitialPage.lastViewedQuestionGuidance()).not.toBeVisible()
    })

    test('When the respondent uses the previous link from the next question, then last question guidance is not shown', async () => {
      const addressConfirmationPage = new AddressConfirmationPage(page)
      const householdInterstitialPage = new HouseholdInterstitialPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      await addressConfirmationPage.submit().click()
      await primaryPersonListCollectorPage.previous().click()
      await expect(householdInterstitialPage.lastViewedQuestionGuidance()).not.toBeVisible()
    })
  })
})
