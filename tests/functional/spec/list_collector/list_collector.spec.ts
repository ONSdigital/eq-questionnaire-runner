import { createOpenQuestionnaire, test, expect } from '../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../fixtures/test'
import { checkItemsInList } from '../../helpers'
import AnotherListCollectorPage from '../../generated_pages/list_collector/another-list-collector-block.page'
import AnotherListCollectorAddPage from '../../generated_pages/list_collector/another-list-collector-block-add.page'
import AnotherListCollectorEditPage from '../../generated_pages/list_collector/another-list-collector-block-edit.page'
import AnotherListCollectorRemovePage from '../../generated_pages/list_collector/another-list-collector-block-remove.page'
import ListCollectorPage from '../../generated_pages/list_collector/list-collector.page'
import ListCollectorAddPage from '../../generated_pages/list_collector/list-collector-add.page'
import ListCollectorEditPage from '../../generated_pages/list_collector/list-collector-edit.page'
import ListCollectorRemovePage from '../../generated_pages/list_collector/list-collector-remove.page'
import NextInterstitialPage from '../../generated_pages/list_collector/next-interstitial.page'
import SummaryPage from '../../generated_pages/list_collector/section-summary.page'
import PrimaryPersonListCollectorPage from '../../generated_pages/list_collector_list_summary/primary-person-list-collector.page'
import PrimaryPersonListCollectorAddPage from '../../generated_pages/list_collector_list_summary/primary-person-list-collector-add.page'
import SectionSummaryListCollectorPage from '../../generated_pages/list_collector_list_summary/list-collector.page'
import SectionSummaryListCollectorAddPage from '../../generated_pages/list_collector_list_summary/list-collector-add.page'
import SectionSummaryListCollectorEditPage from '../../generated_pages/list_collector_list_summary/list-collector-edit.page'
import SectionSummaryListCollectorRemovePage from '../../generated_pages/list_collector_list_summary/list-collector-remove.page'
import VisitorListCollectorPage from '../../generated_pages/list_collector_list_summary/visitor-list-collector.page'
import VisitorListCollectorAddPage from '../../generated_pages/list_collector_list_summary/visitor-list-collector-add.page'
import PeopleListSectionSummaryPage from '../../generated_pages/list_collector_list_summary/section-summary.page'
import SubmitPage from '../../base_pages/submit.page'
import IntroductionPage from '../../generated_pages/list_collector_list_summary/introduction.page'

test.describe('List Collector', () => {
  test.describe('Given a normal journey through the list collector without variants', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Load the survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_list_collector.json')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('The user is able to add members of the household', async () => {
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
      await listCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Olivia')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Suzy')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
    })

    test('The collector shows all of the household members in the summary', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const peopleExpected = ['Marcus Twin', 'Samuel Clemens', 'Olivia Clemens', 'Suzy Clemens']
      await checkItemsInList(peopleExpected, (index) => listCollectorPage.listLabel(index))
    })

    test('The questionnaire allows the name of a person to be changed', async () => {
      const listCollectorEditPage = new ListCollectorEditPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.listEditLink(1).click()
      await listCollectorEditPage.firstName().fill('Mark')
      await listCollectorEditPage.lastName().fill('Twain')
      await listCollectorEditPage.submit().click()
      await expect(listCollectorPage.listLabel(1)).toHaveText('Mark Twain')
    })

    test('The questionnaire allows me to remove the first person (Mark Twain) from the summary', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const listCollectorRemovePage = new ListCollectorRemovePage(page)
      await listCollectorPage.listRemoveLink(1).click()
      await listCollectorRemovePage.yes().click()
      await listCollectorRemovePage.submit().click()
    })

    test('The collector summary does not show Mark Twain anymore.', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      await expect(listCollectorPage.listLabel(1)).not.toContainText('Mark Twain')
      await expect(listCollectorPage.listLabel(3)).toHaveText('Suzy Clemens')
    })

    test('The questionnaire allows more people to be added', async () => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await expect(listCollectorAddPage.questionText()).toHaveText('What is the name of the person?')
      await listCollectorAddPage.firstName().fill('Clara')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Jean')
      await listCollectorAddPage.lastName().fill('Clemens')
      await listCollectorAddPage.submit().click()
    })

    test('The user is returned to the list collector when the cancel link is clicked on the add page.', async () => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Someone')
      await listCollectorAddPage.lastName().fill('Else')
      await listCollectorAddPage.cancelAndReturn().click()
      await expect(page).toHaveURL(new RegExp(listCollectorPage.pageName))
    })

    test('The user is returned to the list collector when the cancel link is clicked on the edit page.', async () => {
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorEditPage = new ListCollectorEditPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      await listCollectorPage.yes().click()
      await listCollectorPage.submit().click()
      await listCollectorAddPage.firstName().fill('Someone')
      await listCollectorAddPage.lastName().fill('Else')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.listEditLink(1).click()
      await listCollectorEditPage.cancelAndReturn().click()
      await expect(page).toHaveURL(new RegExp(listCollectorPage.pageName))
    })

    test('The collector shows everyone on the summary', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const peopleExpected = ['Samuel Clemens', 'Olivia Clemens', 'Suzy Clemens', 'Clara Clemens', 'Jean Clemens']
      await checkItemsInList(peopleExpected, (index) => listCollectorPage.listLabel(index))
    })

    test('When No is answered on the list collector the user sees an interstitial', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const nextInterstitialPage = new NextInterstitialPage(page)
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await expect(page).toHaveURL(new RegExp(nextInterstitialPage.pageName))
      await nextInterstitialPage.submit().click()
    })

    test('After the interstitial, the user should be on the second list collector page', async () => {
      const anotherListCollectorPage = new AnotherListCollectorPage(page)
      await expect(page).toHaveURL(new RegExp(anotherListCollectorPage.pageName))
    })

    test('The collector still shows the same list of people on the summary', async () => {
      const listCollectorPage = new ListCollectorPage(page)
      const peopleExpected = ['Samuel Clemens', 'Olivia Clemens', 'Suzy Clemens', 'Clara Clemens', 'Jean Clemens']
      await checkItemsInList(peopleExpected, (index) => listCollectorPage.listLabel(index))
    })

    test('The collector allows the user to add another person to the same list', async () => {
      const anotherListCollectorAddPage = new AnotherListCollectorAddPage(page)
      const anotherListCollectorPage = new AnotherListCollectorPage(page)
      await anotherListCollectorPage.yes().click()
      await anotherListCollectorPage.submit().click()
      await anotherListCollectorAddPage.firstName().fill('Someone')
      await anotherListCollectorAddPage.lastName().fill('Else')
      await anotherListCollectorAddPage.submit().click()
      await expect(anotherListCollectorPage.listLabel(6)).toHaveText('Someone Else')
    })

    test('The collector allows the user to remove a person again', async () => {
      const anotherListCollectorPage = new AnotherListCollectorPage(page)
      const anotherListCollectorRemovePage = new AnotherListCollectorRemovePage(page)
      await anotherListCollectorPage.listRemoveLink(5).click()
      await anotherListCollectorRemovePage.yes().click()
      await anotherListCollectorRemovePage.submit().click()
    })

    test('The user is returned to the list collector when the previous link is clicked.', async () => {
      const anotherListCollectorEditPage = new AnotherListCollectorEditPage(page)
      const anotherListCollectorPage = new AnotherListCollectorPage(page)
      const anotherListCollectorRemovePage = new AnotherListCollectorRemovePage(page)
      await anotherListCollectorPage.listRemoveLink(1).click()
      await anotherListCollectorRemovePage.previous().click()
      await expect(page).toHaveURL(new RegExp(anotherListCollectorPage.pageName))
      await anotherListCollectorPage.listEditLink(1).click()
      await anotherListCollectorEditPage.previous().click()
      await expect(page).toHaveURL(new RegExp(anotherListCollectorPage.pageName))
      await anotherListCollectorPage.yes().click()
      await anotherListCollectorPage.submit().click()
      await anotherListCollectorEditPage.previous().click()
      await expect(page).toHaveURL(new RegExp(anotherListCollectorPage.pageName))
    })

    test('The questionnaire shows the confirmation page when no more people to add', async () => {
      const anotherListCollectorPage = new AnotherListCollectorPage(page)
      await anotherListCollectorPage.no().click()
      await anotherListCollectorPage.submit().click()
      await expect(page).toHaveURL(/\/sections\/section\//)
    })

    test('The questionnaire allows submission', async () => {
      const submitPage = new SubmitPage(page)
      const summaryPage = new SummaryPage(page)
      await summaryPage.submit().click()
      await submitPage.submit().click()
      await expect(page).toHaveURL(/thank-you/)
    })
  })

  test.describe('Given I start a list collector survey and complete to Section Summary', () => {
    test.beforeEach(async ({ page, openQuestionnaire }) => {
      const introductionPage = new IntroductionPage(page)
      const primaryPersonListCollectorAddPage = new PrimaryPersonListCollectorAddPage(page)
      const primaryPersonListCollectorPage = new PrimaryPersonListCollectorPage(page)
      const sectionSummaryListCollectorAddPage = new SectionSummaryListCollectorAddPage(page)
      const sectionSummaryListCollectorPage = new SectionSummaryListCollectorPage(page)
      const visitorListCollectorAddPage = new VisitorListCollectorAddPage(page)
      const visitorListCollectorPage = new VisitorListCollectorPage(page)
      await openQuestionnaire('test_list_collector_list_summary.json')
      await introductionPage.submit().click()
      await primaryPersonListCollectorPage.yes().click()
      await primaryPersonListCollectorPage.submit().click()
      await primaryPersonListCollectorAddPage.firstName().fill('Marcus')
      await primaryPersonListCollectorAddPage.lastName().fill('Twin')
      await primaryPersonListCollectorAddPage.submit().click()
      await sectionSummaryListCollectorPage.yes().click()
      await sectionSummaryListCollectorPage.submit().click()
      await sectionSummaryListCollectorAddPage.firstName().fill('Samuel')
      await sectionSummaryListCollectorAddPage.lastName().fill('Clemens')
      await sectionSummaryListCollectorAddPage.submit().click()
      await sectionSummaryListCollectorPage.no().click()
      await sectionSummaryListCollectorPage.submit().click()
      await visitorListCollectorPage.yes().click()
      await visitorListCollectorPage.submit().click()
      await visitorListCollectorAddPage.firstNameVisitor().fill('Olivia')
      await visitorListCollectorAddPage.lastNameVisitor().fill('Clemens')
      await visitorListCollectorAddPage.submit().click()
      await visitorListCollectorPage.no().click()
      await visitorListCollectorPage.submit().click()
    })

    test('The section summary should display contents of the list collector', async ({ page }) => {
      const peopleListSectionSummaryPage = new PeopleListSectionSummaryPage(page)
      await expect(peopleListSectionSummaryPage.peopleListLabel(1)).toHaveText('Marcus Twin (You)')
      await expect(peopleListSectionSummaryPage.peopleListLabel(2)).toHaveText('Samuel Clemens')
      await expect(peopleListSectionSummaryPage.visitorsListLabel(1)).toHaveText('Olivia Clemens')
    })

    test('When the user adds an item to the list, They should return to the section summary and it should display the updated list', async ({ page }) => {
      const peopleListSectionSummaryPage = new PeopleListSectionSummaryPage(page)
      const visitorListCollectorAddPage = new VisitorListCollectorAddPage(page)
      const visitorListCollectorPage = new VisitorListCollectorPage(page)
      await peopleListSectionSummaryPage.visitorsListAddLink().click()
      await visitorListCollectorAddPage.firstNameVisitor().fill('Joe')
      await visitorListCollectorAddPage.lastNameVisitor().fill('Bloggs')
      await visitorListCollectorAddPage.submit().click()
      await visitorListCollectorPage.no().click()
      await visitorListCollectorPage.submit().click()
      await expect(peopleListSectionSummaryPage.visitorsListLabel(2)).toHaveText('Joe Bloggs')
    })

    test('When the user removes an item from the list, They should return to the section summary and it should display the updated list', async ({ page }) => {
      const peopleListSectionSummaryPage = new PeopleListSectionSummaryPage(page)
      const sectionSummaryListCollectorRemovePage = new SectionSummaryListCollectorRemovePage(page)
      await peopleListSectionSummaryPage.peopleListRemoveLink(2).click()
      await sectionSummaryListCollectorRemovePage.yes().click()
      await sectionSummaryListCollectorRemovePage.submit().click()
      await expect(peopleListSectionSummaryPage.visitorsListLabel(2)).not.toBeVisible()
    })

    test('When the user updates the list, They should return to the section summary and it should display the updated list', async ({ page }) => {
      const peopleListSectionSummaryPage = new PeopleListSectionSummaryPage(page)
      const sectionSummaryListCollectorEditPage = new SectionSummaryListCollectorEditPage(page)
      await peopleListSectionSummaryPage.peopleListEditLink(1).click()
      await sectionSummaryListCollectorEditPage.firstName().fill('Mark')
      await sectionSummaryListCollectorEditPage.lastName().fill('Twain')
      await sectionSummaryListCollectorEditPage.submit().click()
      await expect(peopleListSectionSummaryPage.peopleListLabel(1)).toHaveText('Mark Twain (You)')
    })

    test('When the user removes an item from the list, They should see the individual response guidance', async ({ page }) => {
      const peopleListSectionSummaryPage = new PeopleListSectionSummaryPage(page)
      await peopleListSectionSummaryPage.peopleListRemoveLink(2).click()
      await expect(page.getByRole('link', { name: /If you can.t answer questions for this person/ })).toBeVisible()
    })

    test('When the user reaches the submit page and navigates back, They should see the Section Summary', async ({ page }) => {
      const peopleListSectionSummaryPage = new PeopleListSectionSummaryPage(page)
      const submitPage = new SubmitPage(page)
      await peopleListSectionSummaryPage.submit().click()
      await submitPage.previous().click()
      await expect(page).toHaveURL(new RegExp(peopleListSectionSummaryPage.pageName))
    })
  })
})
