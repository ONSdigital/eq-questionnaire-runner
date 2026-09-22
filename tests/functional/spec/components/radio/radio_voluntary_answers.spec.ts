import { test, expect } from '../../../fixtures/test'
import RadioVoluntaryTruePage from '../../../generated_pages/radio_voluntary/radio-voluntary-true.page'
import RadioVoluntaryFalsePage from '../../../generated_pages/radio_voluntary/radio-voluntary-false.page'

test.describe('Component: Radio', () => {
  test.describe('Given I start a Voluntary Radio survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_radio_voluntary.json')
    })

    test('When I select a voluntary radio option, Then the clear button should be displayed', async ({ page }) => {
      const radioVoluntaryTruePage = new RadioVoluntaryTruePage(page)
      await radioVoluntaryTruePage.coffee().click()
      await expect(radioVoluntaryTruePage.clearSelectionButton()).toBeVisible()
    })

    test('When I select a voluntary radio option and click the clear button, Then the radio option should not be selected and the clear button should not be displayed', async ({
      page
    }) => {
      const radioVoluntaryTruePage = new RadioVoluntaryTruePage(page)
      await radioVoluntaryTruePage.coffee().click()
      await radioVoluntaryTruePage.clearSelectionButton().click()
      await expect(radioVoluntaryTruePage.coffee()).not.toBeChecked()
      await expect(radioVoluntaryTruePage.clearSelectionButton()).not.toBeVisible()
    })

    test('When I clear a previously saved voluntary radio option and submit, Then when returning to the page the radio option is no longer selected', async ({
      page
    }) => {
      const radioVoluntaryTruePage = new RadioVoluntaryTruePage(page)
      await radioVoluntaryTruePage.coffee().click()
      await radioVoluntaryTruePage.submit().click()
      await radioVoluntaryTruePage.previous().click()
      await radioVoluntaryTruePage.clearSelectionButton().click()
      await radioVoluntaryTruePage.submit().click()
      await radioVoluntaryTruePage.previous().click()
      await expect(radioVoluntaryTruePage.coffee()).not.toBeChecked()
      await expect(radioVoluntaryTruePage.clearSelectionButton()).not.toBeVisible()
    })

    test('When I select a non-voluntary radio option, Then the clear button should not be displayed on the page', async ({ page }) => {
      const radioVoluntaryFalsePage = new RadioVoluntaryFalsePage(page)
      const radioVoluntaryTruePage = new RadioVoluntaryTruePage(page)
      await radioVoluntaryTruePage.submit().click()
      await radioVoluntaryFalsePage.iceCream().click()
      await expect(radioVoluntaryFalsePage.clearSelectionButton()).not.toBeVisible()
    })
  })
})
