import { test, expect } from '../../../fixtures/test'
import MandatoryRadioPage from '../../../generated_pages/placeholder_option_label_from_value/mandatory-radio.page'
import ConfirmationQuestionRadioBlockPage from '../../../generated_pages/placeholder_option_label_from_value/confirmation-question-radio-block.page'

test.describe('Option label value check', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_placeholder_option_label_from_value.json')
  })

  test('Given radio options are provided, When I select first answer (piped from metadata) and go to the next page, Then the question title contains the label text of the answer I selected', async ({
    page
  }) => {
    const confirmationQuestionRadioBlockPage = new ConfirmationQuestionRadioBlockPage(page)
    const mandatoryRadioPage = new MandatoryRadioPage(page)
    await expect(mandatoryRadioPage.answerBusinessNamePipedLabel()).toContainText('Apple (piped)')
    await mandatoryRadioPage.answerBusinessNamePiped().click()
    await mandatoryRadioPage.submit().scrollIntoViewIfNeeded()
    await mandatoryRadioPage.submit().click()
    await expect(confirmationQuestionRadioBlockPage.questionText()).toContainText('Apple (piped)')
  })

  test('Given radio options are provided, When I select an answer (static) and go to the next page, Then the question title contains the label text of the answer I selected', async ({
    page
  }) => {
    const confirmationQuestionRadioBlockPage = new ConfirmationQuestionRadioBlockPage(page)
    const mandatoryRadioPage = new MandatoryRadioPage(page)
    await mandatoryRadioPage.googleLtd().click()
    await mandatoryRadioPage.submit().scrollIntoViewIfNeeded()
    await mandatoryRadioPage.submit().click()
    await expect(confirmationQuestionRadioBlockPage.questionText()).toContainText('Google LTD')
  })
})
