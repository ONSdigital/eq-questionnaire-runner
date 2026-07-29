import { test, expect } from '../../../fixtures/test'
import HouseholdRelationshipsBlockPage from '../../../generated_pages/hub_section_required_and_enabled/household-relationships-block.page'
import RelationshipsCountPage from '../../../generated_pages/hub_section_required_and_enabled/relationships-count.page'
import SubmitPage from '../../../base_pages/submit.page'

test.describe('Hub and spoke section required and enabled', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_hub_section_required_and_enabled.json')
  })

  test("Given a relationship question in household, When I answer 'Yes', meaning the second section is enabled, Then I am routed to second section", async ({
    page
  }) => {
    const householdRelationshipsBlockPage = new HouseholdRelationshipsBlockPage(page)
    const relationshipsCountPage = new RelationshipsCountPage(page)
    await householdRelationshipsBlockPage.yes().click()
    await householdRelationshipsBlockPage.submit().click()
    await expect(relationshipsCountPage.legend()).toHaveText('How many people are related?')
  })

  test(
    "Given a relationship question in household, When I answer 'No', " +
      'Then I am redirected to the hub and can submit my answers without completing the other section',
    async ({ page }) => {
      const householdRelationshipsBlockPage = new HouseholdRelationshipsBlockPage(page)
      const submitPage = new SubmitPage(page, 'questionnaire')
      await householdRelationshipsBlockPage.no().click()
      await householdRelationshipsBlockPage.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
      await expect(page.getByRole('heading', { name: 'Submit survey' })).toBeVisible()
      await submitPage.submit().click()
      await expect(page).toHaveURL(/thank-you/)
    }
  )
})
