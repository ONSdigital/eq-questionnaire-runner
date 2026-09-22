import { test, expect } from '../../fixtures/test'
import type { Page } from '../../fixtures/test'
import ListCollectorPage from '../../generated_pages/relationships/list-collector.page'
import ListCollectorAddPage from '../../generated_pages/relationships/list-collector-add.page'
import ListCollectorRemovePage from '../../generated_pages/relationships/list-collector-remove.page'
import RelationshipsPage from '../../generated_pages/relationships/relationships.page'
import RelationshipsInterstitialPage from '../../generated_pages/relationships/relationship-interstitial.page'
import SectionSummaryPage from '../../generated_pages/relationships/section-summary.page'

test.describe('Relationships', () => {
  const schema = 'test_relationships.json'

  test.describe('Given I am completing the test_relationships survey,', () => {
    test.beforeEach('load the survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire(schema)
    })

    test('When I have one household member, Then I will be not be asked about relationships', async ({ page }) => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Marcus')
      await listCollectorAddPage.lastName().fill('Twin')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await expect(page).toHaveURL(/\/sections\/section\//)
    })

    test('When I add two household members, Then I will be asked about one relationship', async ({ page }) => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const relationshipsInterstitialPage = new RelationshipsInterstitialPage(page)
      const relationshipsPage = new RelationshipsPage(page)
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Marcus')
      await listCollectorAddPage.lastName().fill('Twin')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Samuel')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().scrollIntoViewIfNeeded()
      await listCollectorPage.submit().click()
      await expect(page).toHaveURL(new RegExp(relationshipsPage.pageName))
      await relationshipsPage.husbandOrWife().click()
      await relationshipsPage.submit().click()
      await relationshipsInterstitialPage.submit().click()
      await expect(page).toHaveURL(/\/sections\/section\//)
    })

    test.describe('When I add three household members,', () => {
      test.beforeEach('add three people', async ({ page }) => {
        await addThreePeople(page)
      })

      test('Then I will be asked about all relationships', async ({ page }) => {
        const listCollectorPage = new ListCollectorPage(page)
        const relationshipsInterstitialPage = new RelationshipsInterstitialPage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await listCollectorPage.no().click()
        await listCollectorPage.submit().click()
        await relationshipsPage.husbandOrWife().click()
        await relationshipsPage.submit().click()
        await relationshipsPage.legallyRegisteredCivilPartner().click()
        await relationshipsPage.submit().click()
        await relationshipsPage.husbandOrWife().click()
        await relationshipsPage.submit().click()
        await relationshipsInterstitialPage.submit().click()
        await expect(page).toHaveURL(/\/sections\/section\//)
      })

      test('And go to the first relationship, Then the previous link should return to the list collector', async ({ page }) => {
        const listCollectorPage = new ListCollectorPage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await listCollectorPage.no().click()
        await listCollectorPage.submit().click()
        await relationshipsPage.previous().click()
        await expect(page).toHaveURL(/\/questionnaire\/list-collector\//)
      })

      test("And go to the first relationship, Then the 'Brother or Sister' option should have the text 'Including half brother or half sister'", async ({
        page
      }) => {
        const listCollectorPage = new ListCollectorPage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await listCollectorPage.no().click()
        await listCollectorPage.submit().click()
        await expect(relationshipsPage.brotherOrSisterLabelDescription()).toHaveText('Including half brother or half sister')
      })

      test('And go to the second relationship, Then the previous link should return to the first relationship', async ({ page }) => {
        const listCollectorPage = new ListCollectorPage(page)
        const relationshipsInterstitialPage = new RelationshipsInterstitialPage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await listCollectorPage.no().click()
        await listCollectorPage.submit().click()
        await relationshipsPage.husbandOrWife().click()
        await relationshipsPage.submit().click()
        await relationshipsPage.previous().click()
        await relationshipsInterstitialPage.submit().click()
        await expect(page).toHaveURL(new RegExp(relationshipsPage.pageName))
        await expect(relationshipsPage.questionText()).toContainText('Marcus')
      })

      test('And go to the section summary, Then the previous link should return to the last relationship Interstitial', async ({ page }) => {
        const listCollectorPage = new ListCollectorPage(page)
        const relationshipsInterstitialPage = new RelationshipsInterstitialPage(page)
        const relationshipsPage = new RelationshipsPage(page)
        const sectionSummaryPage = new SectionSummaryPage(page)
        await listCollectorPage.no().click()
        await listCollectorPage.submit().click()
        await relationshipsPage.husbandOrWife().click()
        await relationshipsPage.submit().click()
        await relationshipsPage.legallyRegisteredCivilPartner().click()
        await relationshipsPage.submit().click()
        await relationshipsPage.husbandOrWife().click()
        await relationshipsPage.submit().click()
        await relationshipsInterstitialPage.submit().click()
        await expect(page).toHaveURL(/\/sections\/section\//)
        await sectionSummaryPage.previous().click()
        await relationshipsInterstitialPage.previous().click()
        await expect(page).toHaveURL(new RegExp(relationshipsPage.pageName))
        await expect(relationshipsPage.questionText()).toContainText('Olivia')
      })

      test('When I add all relationships and return to the relationships, Then the relationships should be populated', async ({ page }) => {
        const listCollectorPage = new ListCollectorPage(page)
        const relationshipsInterstitialPage = new RelationshipsInterstitialPage(page)
        const relationshipsPage = new RelationshipsPage(page)
        const sectionSummaryPage = new SectionSummaryPage(page)
        await listCollectorPage.no().click()
        await listCollectorPage.submit().click()
        await relationshipsPage.husbandOrWife().click()
        await relationshipsPage.submit().click()
        await relationshipsPage.legallyRegisteredCivilPartner().click()
        await relationshipsPage.submit().click()
        await relationshipsPage.husbandOrWife().click()
        await relationshipsPage.submit().click()
        await relationshipsInterstitialPage.submit().click()
        await expect(page).toHaveURL(/\/sections\/section\//)
        await sectionSummaryPage.previous().click()
        await relationshipsInterstitialPage.previous().click()
        await expect(relationshipsPage.husbandOrWife()).toBeChecked()
        await relationshipsPage.previous().click()
        await expect(relationshipsPage.legallyRegisteredCivilPartner()).toBeChecked()
      })

      test("And go to the first relationship, Then the person's name should be in the question title and playback text", async ({ page }) => {
        const listCollectorPage = new ListCollectorPage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await listCollectorPage.no().click()
        await listCollectorPage.submit().click()
        await expect(listCollectorPage.questionText()).toContainText('Marcus Twin')
        await expect(relationshipsPage.playback()).toContainText('Marcus Twin')
      })

      test('And go to the first relationship and submit without selecting an option, Then an error should be displayed', async ({ page }) => {
        const listCollectorPage = new ListCollectorPage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await listCollectorPage.no().click()
        await listCollectorPage.submit().click()
        await relationshipsPage.submit().click()
        await expect(relationshipsPage.error()).toBeVisible()
      })

      test("And go to the first relationship and click 'Save and sign out', Then I should be signed out", async ({ page }) => {
        const listCollectorPage = new ListCollectorPage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await listCollectorPage.no().click()
        await listCollectorPage.submit().click()
        await relationshipsPage.husbandOrWife().click()
        await relationshipsPage.saveSignOut().click()
        await expect(page).not.toHaveURL(/questionnaire/)
      })

      test("And go to the first relationship, select a relationship and click 'Save and sign out', Then I should be signed out", async ({ page }) => {
        const listCollectorPage = new ListCollectorPage(page)
        const relationshipsPage = new RelationshipsPage(page)
        await listCollectorPage.no().click()
        await listCollectorPage.submit().click()
        await relationshipsPage.saveSignOut().click()
        await expect(page).not.toHaveURL(/questionnaire/)
      })
    })

    test.describe('When I have added one or more household members after answering the relationships question,', () => {
      test.beforeEach('add three people and complete their relationships', async ({ page }) => {
        await addThreePeopleAndCompleteRelationships(page)
      })

      test('Then I delete one of the original household members I will not be asked for the original members relationships again', async ({ page }) => {
        const listCollectorRemovePage = new ListCollectorRemovePage(page)
        const sectionSummaryPage = new SectionSummaryPage(page)
        await sectionSummaryPage.peopleListRemoveLink(1).click()
        await listCollectorRemovePage.yes().click()
        await listCollectorRemovePage.submit().click()
        await expect(page).toHaveURL(/\/sections\/section\//)
      })

      test('Then I add another household member I will be redirected to parent list collector', async ({ page }) => {
        const listCollectorAddPage = new ListCollectorAddPage(page)
        const sectionSummaryPage = new SectionSummaryPage(page)
        await sectionSummaryPage.peopleListAddLink().click()
        await listCollectorAddPage.firstName().fill('Tom')
        await listCollectorAddPage.lastName().fill('Bowden')
        await listCollectorAddPage.submit().click()
        await expect(page).toHaveURL(/\/questionnaire\/list-collector\//)
      })
    })

    async function addThreePeopleAndCompleteRelationships (page: Page): Promise<void> {
      const listCollectorPage = new ListCollectorPage(page)
      const relationshipsInterstitialPage = new RelationshipsInterstitialPage(page)
      const relationshipsPage = new RelationshipsPage(page)

      await addThreePeople(page)

      await listCollectorPage.no().click()
      await listCollectorPage.submit().scrollIntoViewIfNeeded()
      await listCollectorPage.submit().click()
      await relationshipsPage.husbandOrWife().click()
      await relationshipsPage.submit().click()
      await relationshipsPage.legallyRegisteredCivilPartner().click()
      await relationshipsPage.submit().click()
      await relationshipsPage.husbandOrWife().click()
      await relationshipsPage.submit().click()
      await relationshipsInterstitialPage.submit().click()
    }

    async function addThreePeople (page: Page): Promise<void> {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)

      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Marcus')
      await listCollectorAddPage.lastName().fill('Twin')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Samuel')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().scrollIntoViewIfNeeded()
      await listCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Olivia')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
    }
  })
})
