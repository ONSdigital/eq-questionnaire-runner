import { test, expect } from '../fixtures/test'
import CheckboxBlockPage from '../generated_pages/radio_checkbox_descriptions/checkbox-block.page'
import RadioBlockPage from '../generated_pages/radio_checkbox_descriptions/radio-block.page'

test.describe('Checkbox and Radio item descriptions', () => {
  test.describe('Given the user is presented with radio or checkbox options', () => {
    test.beforeEach('Launch survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_radio_checkbox_descriptions.json')
    })

    test('When the schema defines a description for a checkbox option, then that description is displayed', async ({ page }) => {
      const checkboxBlockPage = new CheckboxBlockPage(page)
      await expect(checkboxBlockPage.newMethodsOfOrganisingExternalRelationshipsWithOtherFirmsOrPublicInstitutionsLabelDescription()).toHaveText(
        'For example first use of alliances, partnerships, outsourcing or sub-contracting'
      )
    })

    test('When the schema defines a description for a radio option, then that description is displayed', async ({ page }) => {
      const checkboxBlockPage = new CheckboxBlockPage(page)
      const radioBlockPage = new RadioBlockPage(page)
      await checkboxBlockPage.newBusinessPracticesForOrganisingProcedures().click()
      await checkboxBlockPage.submit().click()
      await expect(radioBlockPage.newMethodsOfOrganisingExternalRelationshipsWithOtherFirmsOrPublicInstitutionsLabelDescription()).toHaveText(
        'For example first use of alliances, partnerships, outsourcing or sub-contracting'
      )
    })
  })
})
