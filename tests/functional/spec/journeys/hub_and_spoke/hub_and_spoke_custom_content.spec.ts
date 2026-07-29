import { test, expect } from '../../../fixtures/test'
import HouseholdSummary from '../../../generated_pages/hub_and_spoke_custom_content/household-section-summary.page'
import HowManyPeopleLiveHere from '../../../generated_pages/hub_and_spoke_custom_content/how-many-people-live-here.page'
import DoesAnyoneLiveHere from '../../../generated_pages/hub_and_spoke_custom_content/does-anyone-live-here.page'
import HubPage from '../../../base_pages/hub.page'

test.describe('Feature: Hub and Spoke with custom content', () => {
  const hubAndSpokeSchema = 'test_hub_and_spoke_custom_content.json'

  test('When the questionnaire is incomplete, then custom content should be displayed correctly', async ({ page, openQuestionnaire }) => {
    const hubPage = new HubPage(page)
    await openQuestionnaire(hubAndSpokeSchema)
    await expect(hubPage.heading()).toHaveText('Choose another section to complete')
    await expect(hubPage.guidance()).not.toBeVisible()
    await expect(hubPage.summaryRowLink('household-section')).toContainText('Start section: Household residents')
    await expect(hubPage.submit()).toHaveText('Continue')
    await expect(hubPage.warning()).not.toBeVisible()
  })

  test('When the questionnaire is complete, then custom content should be displayed correctly', async ({ page, openQuestionnaire }) => {
    const doesAnyoneLiveHere = new DoesAnyoneLiveHere(page)
    const householdSummary = new HouseholdSummary(page)
    const howManyPeopleLiveHere = new HowManyPeopleLiveHere(page)
    const hubPage = new HubPage(page)
    await openQuestionnaire(hubAndSpokeSchema)
    await hubPage.summaryRowLink('household-section').click()
    await doesAnyoneLiveHere.yes().click()
    await doesAnyoneLiveHere.submit().click()
    await howManyPeopleLiveHere.answer1().click()
    await howManyPeopleLiveHere.submit().click()
    await householdSummary.submit().click()
    await expect(hubPage.summaryRowLink('household-section')).toContainText('View answers: Household residents')
    await expect(hubPage.heading()).toHaveText('Submission title')
    await expect(hubPage.guidance()).toHaveText('Submission guidance')
    await expect(hubPage.submit()).toHaveText('Submission button')
    await expect(hubPage.warning()).toHaveText('Submission warning')
  })
})
