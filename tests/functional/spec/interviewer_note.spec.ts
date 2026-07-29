import { createOpenQuestionnaire, test, expect } from '../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../fixtures/test'
import ConfirmPage from '../generated_pages/interviewer_note/confirm-block.page'
import FavouriteTeamPage from '../generated_pages/interviewer_note/favourite-team-block.page'
import FinalInterstitialPage from '../generated_pages/interviewer_note/final-interstitial-block.page'
import InitialInterstitialPage from '../generated_pages/interviewer_note/initial-interstitial-block.page'

test.describe('Given I start a survey', () => {
  test.describe.configure({ mode: 'serial' })

  let context: BrowserContext
  let page: Page
  let openQuestionnaire: OpenQuestionnaire

  test.beforeAll(async ({ browser }) => {
    context = await browser.newContext()
    page = await context.newPage()
    openQuestionnaire = createOpenQuestionnaire(page)
    await openQuestionnaire('test_interviewer_note.json')
  })

  test.afterAll(async () => {
    await context.close()
  })

  test('When I view interstitial page and the interviewer_note is set to true then I should be able to see interviewer note', async () => {
    const initialInterstitialPage = new InitialInterstitialPage(page)
    await expect(initialInterstitialPage.questionText()).toContainText('Interviewer note')
  })

  test('When I view question page and the interviewer_note is set to true then I should be able to see interviewer note', async () => {
    const favouriteTeamPage = new FavouriteTeamPage(page)
    const initialInterstitialPage = new InitialInterstitialPage(page)
    await initialInterstitialPage.submit().click()
    await expect(favouriteTeamPage.questionText()).toContainText('Interviewer note')
  })

  test('When I view question page and the interviewer_note is set to false then I should not be able to see interviewer note', async () => {
    const confirmPage = new ConfirmPage(page)
    const favouriteTeamPage = new FavouriteTeamPage(page)
    await favouriteTeamPage.favouriteTeam().fill('TNS')
    await favouriteTeamPage.submit().click()
    await expect(confirmPage.questionText()).not.toContainText('Interviewer note')
  })

  test('When I view interstitial page and the interviewer_note is not set then I should not be able to see interviewer note', async () => {
    const confirmPage = new ConfirmPage(page)
    const finalInterstitialPage = new FinalInterstitialPage(page)
    await confirmPage.yes().click()
    await confirmPage.submit().click()
    await expect(finalInterstitialPage.questionText()).not.toContainText('Interviewer note')
  })
})
