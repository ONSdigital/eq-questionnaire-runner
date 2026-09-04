import { test, expect } from '../../../fixtures/test'
import Block1Page from '../../../generated_pages/metadata_routing/block1.page'
import Block2Page from '../../../generated_pages/metadata_routing/block2.page'
import Block3Page from '../../../generated_pages/metadata_routing/block3.page'

test.describe('Feature: Routing - Boolean Flag', () => {
  test('Given I have a routing rule that uses a boolean flag and it is False, When I press continue, Then I should be routed to the correct page', async ({
    page,
    openQuestionnaire
  }) => {
    const block1Page = new Block1Page(page)
    const block2Page = new Block2Page(page)
    await openQuestionnaire('test_metadata_routing.json', {
      booleanFlag: false
    })
    await block1Page.submit().click()
    await expect(page).toHaveURL(new RegExp(block2Page.pageName))
  })

  test('Given I have a routing rule that uses a boolean flag and it is True, When I press continue, Then I should be routed to the correct page ', async ({
    page,
    openQuestionnaire
  }) => {
    const block1Page = new Block1Page(page)
    const block3Page = new Block3Page(page)
    await openQuestionnaire('test_metadata_routing.json', {
      booleanFlag: true
    })
    await block1Page.submit().click()
    await expect(page).toHaveURL(new RegExp(block3Page.pageName))
  })
})
