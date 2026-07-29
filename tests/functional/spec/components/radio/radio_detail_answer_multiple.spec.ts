import { test, expect } from '../../../fixtures/test'
import MandatoryRadioPage from '../../../generated_pages/radio_detail_answer_multiple/radio-mandatory.page'
import SubmitPage from '../../../generated_pages/radio_detail_answer_multiple/submit.page'

test.describe('Radio with multiple "detail_answer" options', () => {
  const radioSchema = 'test_radio_detail_answer_multiple.json'

  test('Given detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', async ({
    page,
    openQuestionnaire
  }) => {
    const mandatoryRadioPage = new MandatoryRadioPage(page)
    await openQuestionnaire(radioSchema)
    await mandatoryRadioPage.eggs().click()
    await expect(mandatoryRadioPage.eggsDetail()).toBeVisible()
    await mandatoryRadioPage.favouriteNotListed().click()
    await expect(mandatoryRadioPage.favouriteNotListedDetail()).toBeVisible()
  })

  test('Given a mandatory detail answer, When I select the option but leave the input field empty and submit, Then an error should be displayed.', async ({
    page,
    openQuestionnaire
  }) => {
    const mandatoryRadioPage = new MandatoryRadioPage(page)
    await openQuestionnaire(radioSchema)
    await mandatoryRadioPage.favouriteNotListed().click()
    await mandatoryRadioPage.submit().click()
    await expect(mandatoryRadioPage.error()).toBeVisible()
    await expect(mandatoryRadioPage.errorNumber(1)).toHaveText('Enter your favourite to continue')
  })

  test('Given a selected radio answer with an error for a mandatory detail answer, When I enter valid value and submit the page, Then the error is cleared and I navigate to next page.', async ({
    page,
    openQuestionnaire
  }) => {
    const mandatoryRadioPage = new MandatoryRadioPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire(radioSchema)
    await mandatoryRadioPage.favouriteNotListed().click()
    await mandatoryRadioPage.submit().click()
    await expect(mandatoryRadioPage.error()).toBeVisible()

    await mandatoryRadioPage.favouriteNotListedDetail().fill('Bacon')
    await mandatoryRadioPage.submit().click()
    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
  })

  test('Given a non-mandatory detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', async ({
    page,
    openQuestionnaire
  }) => {
    const mandatoryRadioPage = new MandatoryRadioPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire(radioSchema)
    await mandatoryRadioPage.eggs().click()
    await expect(mandatoryRadioPage.eggsDetail()).toBeVisible()
    await mandatoryRadioPage.submit().click()
    await expect(submitPage.radioMandatoryAnswer()).toHaveText('Eggs')
  })

  test('Given a detail answer, When the user provides text, Then that text should be displayed on the summary screen', async ({ page, openQuestionnaire }) => {
    const mandatoryRadioPage = new MandatoryRadioPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire(radioSchema)
    await mandatoryRadioPage.eggs().click()
    await mandatoryRadioPage.eggsDetail().fill('Scrambled')
    await mandatoryRadioPage.submit().click()
    await expect(submitPage.radioMandatoryAnswer().locator('span')).toHaveText('Eggs')
    await expect(submitPage.radioMandatoryAnswer().locator('li')).toHaveText('Scrambled')
  })

  test('Given I have previously added text in a detail answer and saved, When I select a different radio and save, Then the text entered in the detail answer field should be empty.', async ({
    page,
    openQuestionnaire
  }) => {
    const mandatoryRadioPage = new MandatoryRadioPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire(radioSchema)
    await mandatoryRadioPage.favouriteNotListed().click()
    await mandatoryRadioPage.favouriteNotListedDetail().fill('Bacon')
    await mandatoryRadioPage.submit().click()
    await submitPage.previous().click()
    await mandatoryRadioPage.eggs().click()
    await mandatoryRadioPage.submit().click()
    await submitPage.previous().click()
    await mandatoryRadioPage.favouriteNotListed().click()
    await expect(mandatoryRadioPage.favouriteNotListedDetail()).toHaveValue('')
  })
})
