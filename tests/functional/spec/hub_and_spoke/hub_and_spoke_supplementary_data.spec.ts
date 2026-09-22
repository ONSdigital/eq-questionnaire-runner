import { test, expect } from '../../fixtures/test'
import { getRandomString } from '../../jwt_helper'
import HubPage from '../../base_pages/hub.page'
import LengthOfEmploymentPage from '../../generated_pages/hub_section_required_with_repeat_supplementary/length-of-employment.page.js'
import Section3Page from '../../generated_pages/hub_section_required_with_repeat_supplementary/section-3-summary.page.js'
import LoadedSuccessfullyBlockPage from '../../generated_pages/hub_section_required_with_repeat_supplementary/loaded-successfully-block.page'
import IntroductionBlockPage from '../../generated_pages/hub_section_required_with_repeat_supplementary/introduction-block.page'
import ListCollectorEmployeesPage from '../../generated_pages/hub_section_required_with_repeat_supplementary/list-collector-employees.page'

test.describe('Feature: Hub and Spoke', () => {
  const hubAndSpokeSchema = 'test_hub_section_required_with_repeat_supplementary.json'
  const responseId = getRandomString(16)

  test.describe('Given a user opens a schema with hub required sections based on a repeating section using supplementary data,', () => {
    test.beforeEach('load the survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire(hubAndSpokeSchema, { responseId, sdsDatasetId: '203b2f9d-c500-8175-98db-86ffcfdccfa3' })
    })

    test('When all the repeating sections are complete, Then the hub should be displayed', async ({ page }) => {
      const loadedSuccessfullyBlockPage = new LoadedSuccessfullyBlockPage(page)
      const introductionBlockPage = new IntroductionBlockPage(page)
      const lengthOfEmploymentPage = new LengthOfEmploymentPage(page)
      const listCollectorEmployeesPage = new ListCollectorEmployeesPage(page)
      const section3Page = new Section3Page(page)
      const hubPage = new HubPage(page)

      await loadedSuccessfullyBlockPage.submit().click()
      await introductionBlockPage.submit().click()

      // Complete the repeating sections using supplementary data
      await listCollectorEmployeesPage.submit().click()
      await lengthOfEmploymentPage.day().fill('1')
      await lengthOfEmploymentPage.month().fill('1')
      await lengthOfEmploymentPage.year().fill('1930')
      await lengthOfEmploymentPage.submit().click()

      await section3Page.submit().click()

      await lengthOfEmploymentPage.day().fill('1')
      await lengthOfEmploymentPage.month().fill('1')
      await lengthOfEmploymentPage.year().fill('1930')
      await lengthOfEmploymentPage.submit().click()

      await section3Page.submit().click()

      await expect(page).toHaveURL(new RegExp(hubPage.pageName))
    })

    test('When the repeating sections are incomplete. Then the hub should not be displayed', async ({ page }) => {
      const loadedSuccessfullyBlockPage = new LoadedSuccessfullyBlockPage(page)
      const introductionBlockPage = new IntroductionBlockPage(page)
      const listCollectorEmployeesPage = new ListCollectorEmployeesPage(page)
      const lengthOfEmploymentPage = new LengthOfEmploymentPage(page)
      const section3Page = new Section3Page(page)
      const hubPage = new HubPage(page)

      await loadedSuccessfullyBlockPage.submit().click()
      await introductionBlockPage.submit().click()

      // Don't complete all repeating sections that use supplementary data
      await listCollectorEmployeesPage.submit().click()
      await lengthOfEmploymentPage.day().fill('1')
      await lengthOfEmploymentPage.month().fill('1')
      await lengthOfEmploymentPage.year().fill('1930')
      await lengthOfEmploymentPage.submit().click()
      await section3Page.submit().click()

      await page.goto(hubPage.pageName)
      await expect(page).toHaveURL(/length-of-employment/)
    })
  })
})
