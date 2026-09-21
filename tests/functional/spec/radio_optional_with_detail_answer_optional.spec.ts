import { test, expect } from '../fixtures/test'
import RadioNonMandatoryPage from '../generated_pages/radio_optional_with_detail_answer_optional/radio-non-mandatory.page'
import SubmitPage from '../generated_pages/radio_optional_with_detail_answer_optional/submit.page'

test.describe('Checkbox and Radio item descriptions', () => {
  test.beforeEach('load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_radio_optional_with_detail_answer_optional.json')
  })

  test.describe('Given the user is presented with an optional radio answer with optional detail answer', () => {
    test('When no answer is provided, Then the expected answer is displayed', async ({ page }) => {
      const radioNonMandatoryPage = new RadioNonMandatoryPage(page)
      const submitPage = new SubmitPage(page)
      await radioNonMandatoryPage.submit().click()
      await expect(submitPage.radioNonMandatoryAnswer()).toHaveText('No answer provided')
    })

    test('When Toast is selected and no detail answer is provided, Then the expected answer is displayed', async ({ page }) => {
      const radioNonMandatoryPage = new RadioNonMandatoryPage(page)
      const submitPage = new SubmitPage(page)
      await radioNonMandatoryPage.toast().click()
      await radioNonMandatoryPage.submit().click()
      await expect(submitPage.radioNonMandatoryAnswer()).toHaveText('Toast')
    })

    test('When Other is selected and no detail answer is provided, Then the expected answer is displayed', async ({ page }) => {
      const radioNonMandatoryPage = new RadioNonMandatoryPage(page)
      const submitPage = new SubmitPage(page)
      await radioNonMandatoryPage.other().click()
      await radioNonMandatoryPage.submit().click()
      await expect(submitPage.radioNonMandatoryAnswer()).toHaveText('Other')
    })

    test('When Other is selected and detail answer is provided, Then the expected answer is displayed', async ({ page }) => {
      const radioNonMandatoryPage = new RadioNonMandatoryPage(page)
      const submitPage = new SubmitPage(page)
      await radioNonMandatoryPage.other().click()
      await radioNonMandatoryPage.otherDetail().fill('Eggs')
      await radioNonMandatoryPage.submit().click()
      await expect(submitPage.radioNonMandatoryAnswer()).toContainText('Eggs')
    })

    test('When Other is selected and detail answer is provided and the answer is changed, Then the expected answer is displayed', async ({ page }) => {
      const radioNonMandatoryPage = new RadioNonMandatoryPage(page)
      const submitPage = new SubmitPage(page)
      await radioNonMandatoryPage.other().click()
      await radioNonMandatoryPage.otherDetail().fill('Eggs')
      await radioNonMandatoryPage.toast().click()
      await radioNonMandatoryPage.submit().click()
      await expect(submitPage.radioNonMandatoryAnswer()).toHaveText('Toast')
    })
  })
})
