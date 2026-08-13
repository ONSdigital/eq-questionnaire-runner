import { test, expect } from '../../fixtures/test'
import type { Page } from '../../fixtures/test'
import PrimaryPersonListCollectorPage from '../../generated_pages/relationships_primary/primary-person-list-collector.page'
import PrimaryPersonListCollectorAddPage from '../../generated_pages/relationships_primary/primary-person-list-collector-add.page'
import ListCollectorPage from '../../generated_pages/relationships_primary/list-collector.page'
import ListCollectorAddPage from '../../generated_pages/relationships_primary/list-collector-add.page'
import RelationshipsPage from '../../generated_pages/relationships_primary/relationships.page'

test.describe('Relationships - Primary Person', () => {
  const schema = 'test_relationships_primary.json'

  test.describe('Given I am completing the test_relationships_primary survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire(schema)
    })

    test('When I add household members, Then I will be asked my relationships as a primary person', async ({ page }) => {
      const listCollectorPage = new ListCollectorPage(page)
      const relationshipsPage = new RelationshipsPage(page)
      await addPrimaryAndTwoOthers(page)

      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await expect(relationshipsPage.questionText()).toContainText('is your')
    })

    test('When I add household members, Then non-primary relationships will be asked as a non primary person', async ({ page }) => {
      const listCollectorPage = new ListCollectorPage(page)
      const relationshipsPage = new RelationshipsPage(page)
      await addPrimaryAndTwoOthers(page)

      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await relationshipsPage.relationshipBrotherOrSister().click()
      await relationshipsPage.submit().click()
      await relationshipsPage.relationshipSonOrDaughter().click()
      await relationshipsPage.submit().click()
      await expect(relationshipsPage.questionText()).toContainText('is their')
    })

    test('When I add household members And add their relationships And remove the primary person And add a new primary person then I will be asked for the relationships again', async ({
      page
    }) => {
      const listCollectorPage = new ListCollectorPage(page)
      const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      const relationshipsPage = new RelationshipsPage(page)
      await addPrimaryAndTwoOthersAndCompleteRelationships(page)

      await page.goto('/questionnaire/primary-person-list-collector')

      await primaryPersonListCollectorPage.no().click()
      await primaryPersonListCollectorPage.submit().click()

      await page.goto('/questionnaire/primary-person-list-collector')

      await primaryPersonListCollectorPage.yes().click()
      await primaryPersonListCollectorPage.submit().click()
      await primaryPersonListCollectorAddPage.firstName().fill('Marcus')
      await primaryPersonListCollectorAddPage.lastName().fill('Twin')
      await primaryPersonListCollectorAddPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()

      await expect(relationshipsPage.questionText()).toContainText('Samuel Clemens is your')
    })

    async function addPrimaryAndTwoOthersAndCompleteRelationships (page: Page): Promise<void> {
      const listCollectorPage = new ListCollectorPage(page)
      const relationshipsPage = new RelationshipsPage(page)

      await addPrimaryAndTwoOthers(page)

      await listCollectorPage.no().click()
      await listCollectorPage.submit().scrollIntoViewIfNeeded()
      await listCollectorPage.submit().click()
      await relationshipsPage.relationshipBrotherOrSister().click()
      await relationshipsPage.submit().click()
      await relationshipsPage.relationshipSonOrDaughter().click()
      await relationshipsPage.submit().click()
      await relationshipsPage.relationshipBrotherOrSister().click()
    }

    async function addPrimaryAndTwoOthers (page: Page): Promise<void> {
      const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)

      await primaryPersonListCollectorPage.yes().click()
      await primaryPersonListCollectorPage.submit().scrollIntoViewIfNeeded()
      await primaryPersonListCollectorPage.submit().click()
      await primaryPersonListCollectorAddPage.firstName().fill('Marcus')
      await primaryPersonListCollectorAddPage.lastName().fill('Twin')
      await primaryPersonListCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Samuel')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Olivia')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
    }
  })
})
