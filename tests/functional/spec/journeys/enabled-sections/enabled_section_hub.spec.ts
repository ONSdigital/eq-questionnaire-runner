import { test, expect } from '../../../fixtures/test'
import SectionOne from '../../../generated_pages/section_enabled_hub/section-1-block.page'
import HubPage from '../../../base_pages/hub.page'

test.describe('Feature: Section Enabled With Hub', () => {
  test.beforeEach('Open survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_section_enabled_hub.json')
  })

  test('When the user selects `Section 2` and submits, Then only section 2 should be displayed on the hub', async ({ page }) => {
    const hubPage = new HubPage(page)
    const sectionOne = new SectionOne(page)
    await sectionOne.section1Section2().click()
    await sectionOne.submit().click()

    await expect(hubPage.summaryRowState('section-2')).toBeVisible()
    await expect(hubPage.summaryRowTitle('section-2')).toContainText('Section 2')

    await expect(hubPage.summaryRowState('section-3')).not.toBeVisible()
  })

  test('When the user selects `Section 3` and submits, Then section 2 should not be displayed and section 3 should be displayed', async ({ page }) => {
    const hubPage = new HubPage(page)
    const sectionOne = new SectionOne(page)
    await sectionOne.section1Section3().click()
    await sectionOne.submit().click()

    await expect(hubPage.summaryRowState('section-3')).toBeVisible()
    await expect(hubPage.summaryRowTitle('section-3')).toContainText('Section 3')

    await expect(hubPage.summaryRowState('section-2')).not.toBeVisible()
  })

  test('When the user selects `Section 2` and `Section 3` and submits, Then section 2 and section 3 should be displayed', async ({ page }) => {
    const hubPage = new HubPage(page)
    const sectionOne = new SectionOne(page)
    await sectionOne.section1Section2().click()
    await sectionOne.section1Section3().click()
    await sectionOne.submit().click()

    await expect(hubPage.summaryRowState('section-2')).toBeVisible()
    await expect(hubPage.summaryRowTitle('section-2')).toContainText('Section 2')

    await expect(hubPage.summaryRowState('section-3')).toBeVisible()
    await expect(hubPage.summaryRowTitle('section-3')).toContainText('Section 3')
  })

  test('When the user selects `Neither` and submits,  Then hub should not display any other section and should be in the `Completed` state.', async ({
    page
  }) => {
    const hubPage = new HubPage(page)
    const sectionOne = new SectionOne(page)
    await sectionOne.section1ExclusiveNeither().click()
    await sectionOne.submit().click()

    await expect(hubPage.summaryRowState('section-2')).not.toBeVisible()
    await expect(hubPage.summaryRowState('section-3')).not.toBeVisible()

    await expect(hubPage.submit()).toHaveText('Submit survey')
    await expect(hubPage.heading()).toHaveText('Submit survey')
  })
})
