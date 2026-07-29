import { test, expect } from '../../../fixtures/test'
import SectionOne from '../../../generated_pages/section_enabled_radio/section-1-block.page'
import SubmitPage from '../../../generated_pages/section_enabled_radio/submit.page'

test.describe('Feature: Section Enabled Based On Radio Answers', () => {
  test.beforeEach('Open survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_section_enabled_radio.json')
  })

  test('When section 2 is enabled and the user changes the answers and disables section 2, Then they should be taken straight to the summary', async ({
    page
  }) => {
    const sectionOne = new SectionOne(page)
    const submitPage = new SubmitPage(page)
    await sectionOne.yesEnableSection2().click()
    await sectionOne.submit().click()

    await expect(page).toHaveURL(/section-2-block/)
    await page.goBack()
    await expect(page).toHaveURL(/section-1-block/)

    await sectionOne.noDisableSection2().click()
    await sectionOne.submit().click()
    await expect(page).toHaveURL(new RegExp(submitPage.url()))
  })

  test('When the user answers `Yes, enable section 2` and submits, Then section 2 should be displayed', async ({ page }) => {
    const sectionOne = new SectionOne(page)
    await sectionOne.yesEnableSection2().click()
    await sectionOne.submit().click()

    await expect(page).toHaveURL(/section-2-block/)
  })

  test('When the user answers `No, disable section 2` and submits, Then they should be taking straight to the summary', async ({ page }) => {
    const sectionOne = new SectionOne(page)
    const submitPage = new SubmitPage(page)
    await sectionOne.noDisableSection2().click()
    await sectionOne.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.url()))
    await expect(submitPage.section2Question()).not.toBeVisible()
  })
})
