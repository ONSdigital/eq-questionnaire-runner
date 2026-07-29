import { test, expect } from '../fixtures/test'
import SetMinMax from '../generated_pages/numbers/set-min-max-block.page'
import TestMinMax from '../generated_pages/numbers/test-min-max-block.page'
import DetailAnswer from '../generated_pages/numbers/detail-answer-block.page'
import SubmitPage from '../generated_pages/numbers/submit.page'
import IntroductionPage from '../generated_pages/introduction/introduction.page'
import IntroInterstitialPage from '../generated_pages/introduction/general-business-information-completed.page'
import IntroThankYouPagePage from '../base_pages/thank-you.page'
import CurrencyBlock from '../generated_pages/variants_question/currency-block.page'
import FirstNumberBlock from '../generated_pages/variants_question/first-number-block.page'
import SecondNumberBlock from '../generated_pages/variants_question/second-number-block.page'
import CurrencySectionSummary from '../generated_pages/variants_question/currency-section-summary.page'
import { getRandomString } from '../jwt_helper'

test.describe('Save sign out / Exit', () => {
  test.describe.configure({ mode: 'serial' })
  const responseId = getRandomString(16)

  test('Given I am on an introduction page, When I click the exit button, Then I am redirected to sign out page and my session is cleared', async ({
    page,
    openQuestionnaire
  }) => {
    const introductionPage = new IntroductionPage(page)
    await openQuestionnaire('test_introduction.json')
    await introductionPage.exitButton().click()

    await expect(page).toHaveURL(/\/surveys\/todo/)

    await page.goBack()
    await expect(page.locator('#main-content')).toContainText('Sorry, you need to sign in again')
  })

  test('Given I am completing a questionnaire, When I select save and sign out, Then I am redirected to the signed out page', async ({
    page,
    openQuestionnaire
  }) => {
    const setMinMax = new SetMinMax(page)
    const testMinMax = new TestMinMax(page)
    await openQuestionnaire('test_numbers.json', { userId: 'test_user', responseId })
    await setMinMax.setMinimum().fill('10')
    await setMinMax.setMaximum().fill('1020')
    await setMinMax.submit().click()
    await testMinMax.saveSignOut().click()

    await expect(page).toHaveURL(/\/signed-out/)

    await page.goBack()
    await expect(page.locator('#main-content')).toContainText('Sorry, you need to sign in again')
  })

  test('Given I have started a questionnaire, When I return to the questionnaire, Then I am returned to the page I was on and can then complete the questionnaire', async ({
    page,
    openQuestionnaire
  }) => {
    const currencyBlock = new CurrencyBlock(page)
    const currencySectionSummary = new CurrencySectionSummary(page)
    const detailAnswer = new DetailAnswer(page)
    const firstNumberBlock = new FirstNumberBlock(page)
    const secondNumberBlock = new SecondNumberBlock(page)
    const submitPage = new SubmitPage(page)
    const testMinMax = new TestMinMax(page)
    await openQuestionnaire('test_numbers.json', { userId: 'test_user', responseId })

    await testMinMax.testRange().fill('10')
    await testMinMax.testMin().fill('123')
    await testMinMax.testMax().fill('1000')
    await testMinMax.testPercent().fill('100')
    await testMinMax.submit().click()
    await detailAnswer.answer1().click()
    await detailAnswer.submit().click()
    await currencyBlock.usDollars().click()
    await currencyBlock.submit().click()
    await firstNumberBlock.firstNumber().fill('50')
    await firstNumberBlock.submit().click()
    await secondNumberBlock.secondNumber().fill('321')
    await secondNumberBlock.submit().click()
    await currencySectionSummary.submit().click()

    await submitPage.submit().click()
    await expect(page).toHaveURL(/thank-you/)
  })

  test('Given I have started a social questionnaire, When I select save and sign out, Then I am redirected to the signed out page and the correct access code link is shown', async ({
    page,
    openQuestionnaire
  }) => {
    const submitPage = new SubmitPage(page)
    const resumeSurveyLink = page.locator('main a[href*="/en/start"]')
    await openQuestionnaire('test_theme_social.json', { theme: 'social' })
    await submitPage.saveSignOut().click()
    await expect(page).toHaveURL(/\/signed-out/)
    await expect(page.locator('#main-content')).toContainText('Your progress has been saved')
    await expect(page.locator('#main-content')).toContainText('To resume the survey,')
    await expect(resumeSurveyLink).toHaveCount(1)
    await expect(resumeSurveyLink).toHaveAttribute('href', /\/en\/start/)
  })

  test('Given I have started a business questionnaire, When I select save and sign out, Then I am redirected to the signed out page and the correct access code link is shown', async ({
    page,
    openQuestionnaire
  }) => {
    const introductionPage = new IntroductionPage(page)
    const introInterstitialPage = new IntroInterstitialPage(page)
    const myAccountLink = page.locator('main a[href*="/surveys/todo"]')
    await openQuestionnaire('test_introduction.json')
    await introductionPage.getStarted().click()
    await introInterstitialPage.saveSignOut().click()
    await expect(page).toHaveURL(/\/signed-out/)
    await expect(page.locator('#main-content')).toContainText('Your progress has been saved')
    await expect(page.locator('#main-content')).toContainText('To find further information or resume the survey,')
    await expect(myAccountLink).toHaveCount(1)
    await expect(myAccountLink).toHaveAttribute('href', /\/surveys\/todo/)
  })

  test('Given a business questionnaire, When I navigate the questionnaire, Then I see the correct sign out buttons', async ({ page, openQuestionnaire }) => {
    const introductionPage = new IntroductionPage(page)
    const introInterstitialPage = new IntroInterstitialPage(page)
    const introThankYouPagePage = new IntroThankYouPagePage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire('test_introduction.json')

    await expect(introductionPage.exitButton()).toHaveText('Exit')
    await introductionPage.getStarted().click()

    await expect(introInterstitialPage.saveSignOut()).toHaveText('Save and exit survey')
    await introInterstitialPage.submit().click()

    await expect(submitPage.saveSignOut()).toHaveText('Save and exit survey')
    await submitPage.submit().click()

    await expect(introThankYouPagePage.exitButton()).not.toBeVisible()
  })
})
