import { test, expect } from '../../../fixtures/test'
import CheckboxVisibleTruePage from '../../../generated_pages/checkbox_detail_answer_textfield/checkbox-visible-true.page'
import CheckboxVisibleFalsePage from '../../../generated_pages/checkbox_detail_answer_textfield/checkbox-visible-false.page'
import CheckboxVisibleNonePage from '../../../generated_pages/checkbox_detail_answer_textfield/checkbox-visible-none.page'
import MutuallyExclusivePage from '../../../generated_pages/checkbox_detail_answer_textfield/mutually-exclusive.page'

test.describe('Given the checkbox detail_answer questionnaire,', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_checkbox_detail_answer_textfield.json')
  })

  test('When a checkbox has a detail_answer with visible set to true, Then the detail answer write-in field should be shown', async ({ page }) => {
    const checkboxVisibleTruePage = new CheckboxVisibleTruePage(page)
    await expect(checkboxVisibleTruePage.otherDetail()).toBeVisible({ timeout: 5000 })
  })

  test('When a checkbox has a detail_answer with visible set to true and another answer is checked, then the detail answer write-in field should still be shown', async ({
    page
  }) => {
    const checkboxVisibleTruePage = new CheckboxVisibleTruePage(page)
    await checkboxVisibleTruePage.coffee().click()
    await expect(checkboxVisibleTruePage.otherDetail()).toBeVisible({ timeout: 5000 })
  })

  test('When a checkbox has a detail_answer with visible set to false, Then the detail answer write-in field should not be shown', async ({ page }) => {
    const checkboxVisibleFalsePage = new CheckboxVisibleFalsePage(page)
    const checkboxVisibleTruePage = new CheckboxVisibleTruePage(page)
    await checkboxVisibleTruePage.coffee().click()
    await checkboxVisibleTruePage.submit().click()
    await expect(checkboxVisibleFalsePage.otherDetail()).toBeHidden({ timeout: 5000 })
  })

  test('When a checkbox has a detail_answer with visible not set, Then the detail answer write-in field should not be shown', async ({ page }) => {
    const checkboxVisibleFalsePage = new CheckboxVisibleFalsePage(page)
    const checkboxVisibleNonePage = new CheckboxVisibleNonePage(page)
    const checkboxVisibleTruePage = new CheckboxVisibleTruePage(page)
    await checkboxVisibleTruePage.coffee().click()
    await checkboxVisibleTruePage.submit().click()
    await checkboxVisibleFalsePage.iceCream().click()
    await checkboxVisibleFalsePage.submit().click()
    await expect(checkboxVisibleNonePage.otherDetail()).toBeHidden({ timeout: 5000 })
  })

  test('When a mutually exclusive checkbox has a detail_answer with visible set to true, Then the detail answer write-in field should be shown', async ({
    page
  }) => {
    const checkboxVisibleFalsePage = new CheckboxVisibleFalsePage(page)
    const checkboxVisibleNonePage = new CheckboxVisibleNonePage(page)
    const checkboxVisibleTruePage = new CheckboxVisibleTruePage(page)
    const mutuallyExclusivePage = new MutuallyExclusivePage(page)
    await checkboxVisibleTruePage.coffee().click()
    await checkboxVisibleTruePage.submit().click()
    await checkboxVisibleFalsePage.iceCream().click()
    await checkboxVisibleFalsePage.submit().click()
    await checkboxVisibleNonePage.blue().click()
    await checkboxVisibleNonePage.submit().click()
    await expect(mutuallyExclusivePage.otherDetail()).toBeVisible({ timeout: 5000 })
  })
})
