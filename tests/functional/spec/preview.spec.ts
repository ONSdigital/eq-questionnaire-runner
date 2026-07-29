import { test, expect } from '../fixtures/test'
import type { Page } from '../fixtures/test'
import IntroductionPageHub from '../generated_pages/introduction_hub/introduction.page'
import IntroductionPageLinear from '../generated_pages/introduction/introduction.page'

test.describe('Introduction preview questions', () => {
  const introductionSchemaHub = 'test_introduction_hub.json'
  const introductionSchemaLinear = 'test_introduction.json'
  const showAllButton = 'button:has-text("Show all")'
  const hideAllButton = 'button:has-text("Hide all")'
  const previewSummaryContent = '#summary-accordion-1-content'
  const previewSectionTitle = '.ons-summary__group-title'
  const previewQuestion = '.ons-summary__item'
  const printButton = 'button[data-qa="btn-print"]'
  const pdfButton = 'a[data-qa="btn-pdf"]'
  // const detailsHeading = ".ons-details__heading";
  const startSurveyButton = '.qa-btn-get-started'
  const noRadio = '#report-radio-answer-1'
  const submitButton = 'button[data-qa="btn-submit"]'
  const answerFromDay = '#answer-from-day'
  const answerFromMonth = '#answer-from-month'
  const answerFromYear = '#answer-from-year'
  const answerToDay = '#answer-to-day'
  const answerToMonth = '#answer-to-month'
  const answerToYear = '#answer-to-year'

  async function testPreview (page: Page): Promise<void> {
    const firstPreviewQuestion = page.locator(previewQuestion).first()

    // :TODO: Add data attributes to elements below so we don't rely on tags or classes that are subject to DS changes
    await expect(firstPreviewQuestion.locator('h3')).toHaveText('Are you able to report for the calendar month 1 January 2017 to 1 February 2017?')
    await expect(firstPreviewQuestion.locator('.ons-question__description')).toHaveText('Your return should relate to the calendar year 2021.')
    await expect(firstPreviewQuestion.locator('.ons-panel__body').first()).toHaveText('Please provide figures for the period in which you were trading.')
    await expect(page.locator(showAllButton)).toHaveCount(0)
    await expect(page.locator(printButton)).toBeEnabled()
    await expect(page.locator(pdfButton)).toBeEnabled()
    await expect(firstPreviewQuestion.locator('p').nth(2)).toHaveText('You can answer with one of the following options:')
    await expect(firstPreviewQuestion.locator('li')).toHaveText(['Yes', 'No'])
  }

  test('Given I start the hub survey, When I view the preview page, Then all preview elements should be visible and any metadata piped answers are resolved', async ({
    page,
    openQuestionnaire
  }) => {
    const introductionPageHub = new IntroductionPageHub(page)
    await openQuestionnaire(introductionSchemaHub)

    await introductionPageHub.previewQuestions().click()
    await expect(page).toHaveURL(/questionnaire\/preview/)
    await page.locator(showAllButton).click()

    await testPreview(page)
  })

  test('Given I start the linear survey, When I view the preview page, Then all preview elements should be visible and any metadata piped answers are resolved', async ({
    page,
    openQuestionnaire
  }) => {
    const introductionPageLinear = new IntroductionPageLinear(page)
    await openQuestionnaire(introductionSchemaLinear)

    await introductionPageLinear.previewQuestions().click()
    await expect(page).toHaveURL(/questionnaire\/preview/)
    await expect(page.locator(previewSectionTitle)).toHaveText('Main section')

    await testPreview(page)
  })

  test('Given I complete some of a survey and the piped answers should be being populated, Then preview answers should still be showing placeholders', async ({
    page,
    openQuestionnaire
  }) => {
    const introductionPageLinear = new IntroductionPageLinear(page)
    await openQuestionnaire(introductionSchemaLinear)
    await page.locator(startSurveyButton).click()
    await page.locator(noRadio).click()
    await page.locator(submitButton).click()
    await page.locator(answerFromDay).fill('5')
    await page.locator(answerFromMonth).fill('12')
    await page.locator(answerFromYear).fill('2016')
    await page.locator(answerToDay).fill('20')
    await page.locator(answerToMonth).fill('12')
    await page.locator(answerToYear).fill('2016')
    await page.locator(submitButton).click()
    await expect(page.locator('h1')).toHaveText('Are you sure you are able to report for the calendar month 5 December 2016 to 20 December 2016?')
    await page.goto('questionnaire/introduction/')
    await introductionPageLinear.previewQuestions().click()
    await expect(page).toHaveURL(/questionnaire\/preview/)
    await expect(page.locator(previewSectionTitle)).toHaveText('Main section')
    await expect(page.locator(previewQuestion).nth(2).locator('h3')).toHaveText(
      'Are you sure you are able to report for the calendar month {calendar_start_date} to {calendar_end_date}?'
    )
  })

  test(
    'Given I start a survey, When I view the preview page of hub flow schema, ' +
      "Then the twisty button should read 'Show all' and answers should be invisible",
    async ({ page, openQuestionnaire }) => {
      const introductionPageHub = new IntroductionPageHub(page)
      await openQuestionnaire(introductionSchemaHub)
      await introductionPageHub.previewQuestions().click()
      await expect(page).toHaveURL(/questionnaire\/preview/)
      await expect(page.locator(printButton)).toBeEnabled()
      await expect(page.locator(pdfButton)).toBeEnabled()
      await expect(page.locator(showAllButton)).toHaveCount(1)
      await expect(page.locator(previewSummaryContent)).toHaveAttribute('aria-hidden', 'true')

      await page.locator(showAllButton).click()
      await expect(page.locator(hideAllButton)).toHaveCount(1)
      await expect(page.locator(previewSummaryContent)).toHaveAttribute('aria-hidden', 'false')
    }
  )
})
