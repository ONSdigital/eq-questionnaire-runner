import { test, expect } from '../../../fixtures/test'
import RadioVisibleTruePage from '../../../generated_pages/radio_detail_answer_visible/radio-visible-true.page'
import RadioVisibleFalsePage from '../../../generated_pages/radio_detail_answer_visible/radio-visible-false.page'
import RadioVisibleNonePage from '../../../generated_pages/radio_detail_answer_visible/radio-visible-none.page'

test.describe('Given I start a Radio survey with a write-in option', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_radio_detail_answer_visible.json')
  })

  test('When I view a write-in radio and the visible option is set to true, Then the detail answer label should be displayed', async ({ page }) => {
    const radioVisibleTruePage = new RadioVisibleTruePage(page)
    await expect(radioVisibleTruePage.otherDetail()).toBeVisible({ timeout: 5000 })
  })

  test('When I view a write-in radio and the visible option is set to true, Then after choosing non write-in option the detail answer label should be displayed', async ({
    page
  }) => {
    const radioVisibleTruePage = new RadioVisibleTruePage(page)
    await radioVisibleTruePage.coffee().click()
    await expect(radioVisibleTruePage.otherDetail()).toBeVisible({ timeout: 5000 })
  })

  test('When I view a write-in radio and the visible option is set to false, Then the detail answer label should not be displayed', async ({ page }) => {
    const radioVisibleFalsePage = new RadioVisibleFalsePage(page)
    const radioVisibleTruePage = new RadioVisibleTruePage(page)
    await radioVisibleTruePage.coffee().click()
    await radioVisibleTruePage.submit().click()
    await expect(radioVisibleFalsePage.otherDetail()).toBeHidden({ timeout: 5000 })
  })

  test('When I view a write-in radio and the visible option is not set, Then the detail answer label should not be displayed', async ({ page }) => {
    const radioVisibleFalsePage = new RadioVisibleFalsePage(page)
    const radioVisibleNonePage = new RadioVisibleNonePage(page)
    const radioVisibleTruePage = new RadioVisibleTruePage(page)
    await radioVisibleTruePage.coffee().click()
    await radioVisibleFalsePage.submit().click()
    await radioVisibleFalsePage.iceCream().click()
    await radioVisibleFalsePage.submit().click()
    await expect(radioVisibleNonePage.otherDetail()).toBeHidden({ timeout: 5000 })
  })
})
