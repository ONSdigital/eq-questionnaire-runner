import { createOpenQuestionnaire, test, expect } from '../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../fixtures/test'
import ListCollectorPage from '../../generated_pages/relationships_unrelated/list-collector.page'
import ListCollectorAddPage from '../../generated_pages/relationships_unrelated/list-collector-add.page'
import RelationshipsPage from '../../generated_pages/relationships_unrelated/relationships.page'
import RelatedToAnyoneElsePage from '../../generated_pages/relationships_unrelated/related-to-anyone-else.page'
import RelationshipsInterstitialPage from '../../generated_pages/relationships_unrelated/relationship-interstitial.page'
import { verifyUrlContains } from '../../helpers'

test.describe('Unrelated Relationships', () => {
  const schema = 'test_relationships_unrelated.json'

  test.describe('Given I am completing the test_relationships_unrelated survey,', () => {
    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('load the survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire(schema)
    })

    test.afterAll(async () => {
      await context.close()
    })

    test.describe('And I add six people', () => {
      test.describe.configure({ mode: 'serial' })

      test.beforeAll('add people', async () => {
        const listCollectorPage = new ListCollectorPage(page)
        await addPerson('Andrew', 'Austin')
        await addPerson('Betty', 'Burns')
        await addPerson('Carla', 'Clark')
        await addPerson('Daniel', 'Davis')
        await addPerson('Eve', 'Elliot')
        await listCollectorPage.no().click()
        await listCollectorPage.submit().click()
      })

      test("When I answer 'Unrelated' twice, Then I will be asked if anyone else is related with a list of the remaining people", async () => {
        const relatedToAnyoneElsePage = new RelatedToAnyoneElsePage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await relationshipsPage.unrelated().click()
        await relationshipsPage.submit().click()
        await relationshipsPage.unrelated().click()
        await relationshipsPage.submit().click()
        await expect(relatedToAnyoneElsePage.questionText()).toHaveText('Are any of these people related to you?')
        await expect(relatedToAnyoneElsePage.listLabel(1)).toHaveText('Daniel Davis')
        await expect(relatedToAnyoneElsePage.listLabel(2)).toHaveText('Eve Elliot')
      })

      test('When I click previous, Then I will go back to the previous relationship', async () => {
        const relatedToAnyoneElsePage = new RelatedToAnyoneElsePage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await relatedToAnyoneElsePage.previous().click()
        await verifyUrlContains(page, relationshipsPage.pageName)
        await expect(relationshipsPage.unrelated()).toBeChecked()
        await expect(relationshipsPage.questionText()).toContainText('Carla Clark is unrelated to Andrew Austin')
      })

      test("When I return to the 'related to anyone else' question and select 'Yes', Then I will be taken to the next relationship for the first person", async () => {
        const relatedToAnyoneElsePage = new RelatedToAnyoneElsePage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await relationshipsPage.submit().click()
        await relatedToAnyoneElsePage.yes().click()
        await relatedToAnyoneElsePage.submit().click()
        await expect(relationshipsPage.questionText()).toContainText('Thinking about Andrew Austin, Daniel Davis is their')
      })

      test("When I click previous, Then I will go back to the 'related to anyone else' question", async () => {
        const relatedToAnyoneElsePage = new RelatedToAnyoneElsePage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await relationshipsPage.previous().click()
        await expect(relatedToAnyoneElsePage.questionText()).toHaveText('Are any of these people related to you?')
        await expect(relatedToAnyoneElsePage.yes()).toBeChecked()
      })

      test("When I select 'No' to the 'related to anyone else' question, Then I will be taken to the first relationship for the second person", async () => {
        const relatedToAnyoneElsePage = new RelatedToAnyoneElsePage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await relatedToAnyoneElsePage.noNoneOfThesePeopleAreRelatedToMe().click()
        await relatedToAnyoneElsePage.submit().click()
        await expect(relationshipsPage.questionText()).toContainText('Thinking about Betty Burns, Carla Clark is their')
      })

      test("When I click previous, Then I will go back to the 'related to anyone else' question for the first person", async () => {
        const relatedToAnyoneElsePage = new RelatedToAnyoneElsePage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await relationshipsPage.previous().click()
        await expect(relatedToAnyoneElsePage.questionText()).toHaveText('Are any of these people related to you?')
        await expect(relatedToAnyoneElsePage.listLabel(1)).toHaveText('Daniel Davis')
        await expect(relatedToAnyoneElsePage.listLabel(2)).toHaveText('Eve Elliot')
        await expect(relatedToAnyoneElsePage.noNoneOfThesePeopleAreRelatedToMe()).toBeChecked()
      })

      test('When I click complete the remaining relationships, Then I will go to the relationships section complete page', async () => {
        const relatedToAnyoneElsePage = new RelatedToAnyoneElsePage(page)
        const relationshipsInterstitialPage = new RelationshipsInterstitialPage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await relatedToAnyoneElsePage.submit().click()
        await relationshipsPage.unrelated().click()
        await relationshipsPage.submit().click()
        await relationshipsPage.unrelated().click()
        await relationshipsPage.submit().click()
        await relationshipsPage.unrelated().click()
        await relationshipsPage.submit().click()
        await relationshipsPage.unrelated().click()
        await relationshipsPage.submit().click()
        await relationshipsPage.unrelated().click()
        await relationshipsPage.submit().click()
        await relationshipsPage.unrelated().click()
        await relationshipsPage.submit().click()
        await expect(page).toHaveURL(new RegExp(relationshipsInterstitialPage.pageName))
      })
    })

    async function addPerson (firstName: string, lastName: string): Promise<void> {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().scrollIntoViewIfNeeded()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill(firstName)
      await listCollectorAddPage.lastName().fill(lastName)
      await listCollectorAddPage.submit().click()
    }
  })
})
