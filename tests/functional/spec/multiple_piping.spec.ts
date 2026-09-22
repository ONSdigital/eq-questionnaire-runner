import { test, expect } from '../fixtures/test'
import AddressPage from '../generated_pages/multiple_piping/what-is-your-address.page'
import TextfieldPage from '../generated_pages/multiple_piping/textfield.page'
import MultiplePipingPage from '../generated_pages/multiple_piping/piping-question.page'

test.describe('Piping', () => {
  const pipingSchema = 'test_multiple_piping.json'

  test.describe('Multiple piping into question and answer', () => {
    test.beforeEach('load the survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire(pipingSchema)
    })

    test('Given I enter multiple fields in one question, When I navigate to the multiple piping answer, Then I should see all values piped into an answer', async ({
      page
    }) => {
      const addressPage = new AddressPage(page)
      const multiplePipingPage = new MultiplePipingPage(page)
      const textfieldPage = new TextfieldPage(page)
      await addressPage.addressLine1().fill('1 The ONS')
      await addressPage.townCity().fill('Newport')
      await addressPage.postcode().fill('NP10 8XG')
      await addressPage.country().fill('Wales')
      await addressPage.submit().click()
      await textfieldPage.firstText().fill('Fireman')
      await textfieldPage.secondText().fill('Sam')
      await textfieldPage.submit().click()
      await expect(multiplePipingPage.answerAddressLabel()).toHaveText('1 The ONS, Newport, NP10 8XG, Wales')
    })

    test('Given I enter values in multiple questions, When I navigate to the multiple piping question, Then I should see both values piped into the question', async ({
      page
    }) => {
      const addressPage = new AddressPage(page)
      const multiplePipingPage = new MultiplePipingPage(page)
      const textfieldPage = new TextfieldPage(page)
      await addressPage.addressLine1().fill('1 The ONS')
      await addressPage.submit().click()
      await textfieldPage.firstText().fill('Fireman')
      await textfieldPage.secondText().fill('Sam')
      await textfieldPage.submit().click()
      await expect(multiplePipingPage.questionText()).toHaveText('Does Fireman Sam live at 1 The ONS')
    })
  })
})
