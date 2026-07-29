import { test, expect } from '../../../fixtures/test'
import SectionOne from '../../../generated_pages/section_enabled_checkbox/section-1-block.page'
import SectionTwo from '../../../generated_pages/section_enabled_checkbox/section-2-block.page'
import SubmitPage from '../../../generated_pages/section_enabled_checkbox/submit.page'

test.describe('Feature: Section Enabled Based On Checkbox Answers', () => {
  test.beforeEach('Open survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_section_enabled_checkbox.json')
  })

  test('When the user selects `Section 2` and submits, Then section 2 should be displayed', async ({ page }) => {
    const sectionOne = new SectionOne(page)
    await sectionOne.section1Section2().click()
    await sectionOne.submit().click()

    await expect(page).toHaveURL(/section-2-block/)
  })

  test('When the user selects `Section 3` and submits, Then section 2 should not be displayed and section 3 should be displayed', async ({ page }) => {
    const sectionOne = new SectionOne(page)
    await sectionOne.section1Section3().click()
    await sectionOne.submit().click()

    await expect(page).toHaveURL(/section-3-block/)
  })

  test('When the user selects `Section 2` and `Section 3` and submits, Then section 2 and section 3 should be displayed', async ({ page }) => {
    const sectionOne = new SectionOne(page)
    const sectionTwo = new SectionTwo(page)
    await sectionOne.section1Section2().click()
    await sectionOne.section1Section3().click()
    await sectionOne.submit().click()

    await expect(page).toHaveURL(/section-2-block/)
    await sectionTwo.submit().click()
    await expect(page).toHaveURL(/section-3-block/)
  })

  test('When the user selects `Neither` and submits, Then they should be taken straight to the summary', async ({ page }) => {
    const sectionOne = new SectionOne(page)
    const submitPage = new SubmitPage(page)
    await sectionOne.section1ExclusiveNeither().click()
    await sectionOne.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.url()))
    await expect(submitPage.section2Question()).not.toBeVisible()
    await expect(submitPage.section3Question()).not.toBeVisible()
  })
})
