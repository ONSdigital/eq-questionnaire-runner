import { test, expect } from '../fixtures/test'
import DateEntryBlockPage from '../generated_pages/placeholder_first_non_empty_item/date-entry-block.page'
import DateQuestionBlockPage from '../generated_pages/placeholder_first_non_empty_item/date-question-block.page'
import TotalTurnoverBlockPage from '../generated_pages/placeholder_first_non_empty_item/total-turnover-block.page'
import FoodQuestionBlockPage from '../generated_pages/placeholder_first_non_empty_item_cross_section_dependencies/food-question-block.page'
import AddPersonPage from '../generated_pages/placeholder_first_non_empty_item_repeating_sections/list-collector-add.page'
import ListCollectorPage from '../generated_pages/placeholder_first_non_empty_item_repeating_sections/list-collector.page'
import PersonalDetailsBlockPage from '../generated_pages/placeholder_first_non_empty_item_repeating_sections/personal-details-block.page'
import HubPage from '../base_pages/hub.page.js'
import { verifyUrlContains } from '../helpers'

test.describe('First Non Empty Item Transform', () => {
  test.beforeEach('Launch survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_placeholder_first_non_empty_item.json')
  })

  test('When the custom date range is entered and the answer is changed back to metadata date range, Then metadata date should be displayed', async ({
    page
  }) => {
    const dateEntryBlockPage = new DateEntryBlockPage(page)
    const dateQuestionBlockPage = new DateQuestionBlockPage(page)
    const totalTurnoverBlockPage = new TotalTurnoverBlockPage(page)
    // Set the date
    await dateQuestionBlockPage.noINeedToReportForADifferentPeriod().click()
    await dateQuestionBlockPage.submit().click()
    await dateEntryBlockPage.dateEntryFromDay().fill('5')
    await dateEntryBlockPage.dateEntryFromMonth().fill('01')
    await dateEntryBlockPage.dateEntryFromYear().fill('2017')
    await dateEntryBlockPage.dateEntryToDay().fill('25')
    await dateEntryBlockPage.dateEntryToMonth().fill('01')
    await dateEntryBlockPage.dateEntryToYear().fill('2017')
    await dateEntryBlockPage.submit().click()
    // Change to original dates
    await totalTurnoverBlockPage.previous().click()
    await dateEntryBlockPage.previous().click()
    await dateQuestionBlockPage.yesICanReportForThisPeriod().click()
    await dateQuestionBlockPage.submit().click()
    await verifyUrlContains(page, totalTurnoverBlockPage.pageName)
    await expect(totalTurnoverBlockPage.questionTitle()).toContainText('1 January 2017 to 1 February 2017')
  })
})

test.describe('First Non Empty Item Transform Cross Section', () => {
  test.beforeEach('Launch survey', async ({ page, openQuestionnaire }) => {
    const hubPage = new HubPage(page)
    await openQuestionnaire('test_placeholder_first_non_empty_item_cross_section_dependencies.json')
    await hubPage.submit().click()
  })

  test('Given a custom date range is entered, When the answer is changed back to metadata range, Then the metadata date should be displayed for both sections', async ({
    page
  }) => {
    const dateEntryBlockPage = new DateEntryBlockPage(page)
    const dateQuestionBlockPage = new DateQuestionBlockPage(page)
    const foodQuestionBlockPage = new FoodQuestionBlockPage(page)
    const hubPage = new HubPage(page)
    // Set the date
    await dateQuestionBlockPage.noINeedToReportForADifferentPeriod().click()
    await dateQuestionBlockPage.submit().click()
    await dateEntryBlockPage.dateEntryFromDay().fill('5')
    await dateEntryBlockPage.dateEntryFromMonth().fill('01')
    await dateEntryBlockPage.dateEntryFromYear().fill('2017')
    await dateEntryBlockPage.dateEntryToDay().fill('25')
    await dateEntryBlockPage.dateEntryToMonth().fill('01')
    await dateEntryBlockPage.dateEntryToYear().fill('2017')
    await dateEntryBlockPage.submit().click()

    // Check date changed and then change to original dates
    await hubPage.submit().click()
    await expect(foodQuestionBlockPage.questionTitle()).toContainText('5 January 2017 to 25 January 2017')
    await foodQuestionBlockPage.previous().click()
    await hubPage.summaryRowLink('default-section').click()
    await dateQuestionBlockPage.yesICanReportForThisPeriod().click()
    await dateQuestionBlockPage.submit().click()
    // Check the next section if the metadata date is shown
    await hubPage.submit().click()
    await verifyUrlContains(page, foodQuestionBlockPage.pageName)
    await expect(foodQuestionBlockPage.questionTitle()).toContainText('1 January 2017 to 1 February 2017')
  })
})

test.describe('First Non Empty Item Transform Repeating Sections', () => {
  test.beforeEach('Launch survey', async ({ page, openQuestionnaire }) => {
    const hubPage = new HubPage(page)
    await openQuestionnaire('test_placeholder_first_non_empty_item_repeating_sections.json')
    await hubPage.submit().click()
  })

  test('Given a custom date range is entered, When the answer is changed back to metadata range, Then the metadata date should be displayed for the repeating section title', async ({
    page
  }) => {
    const addPersonPage = new AddPersonPage(page)
    const dateEntryBlockPage = new DateEntryBlockPage(page)
    const dateQuestionBlockPage = new DateQuestionBlockPage(page)
    const hubPage = new HubPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const personalDetailsBlockPage = new PersonalDetailsBlockPage(page)
    // Set the date
    await dateQuestionBlockPage.noINeedToReportForADifferentPeriod().click()
    await dateQuestionBlockPage.submit().click()
    await dateEntryBlockPage.dateEntryFromDay().fill('5')
    await dateEntryBlockPage.dateEntryFromMonth().fill('01')
    await dateEntryBlockPage.dateEntryFromYear().fill('2017')
    await dateEntryBlockPage.dateEntryToDay().fill('25')
    await dateEntryBlockPage.dateEntryToMonth().fill('01')
    await dateEntryBlockPage.dateEntryToYear().fill('2017')
    await dateEntryBlockPage.submit().click()
    await hubPage.submit().click()

    // Add a person to the list collector
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await addPersonPage.firstName().fill('Paul')
    await addPersonPage.lastName().fill('Pogba')
    await addPersonPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await listCollectorPage.submit().click()
    // Check Repeating Section has the set dates
    await hubPage.submit().click()
    await verifyUrlContains(page, personalDetailsBlockPage.pageName)
    await expect(personalDetailsBlockPage.questionTitle()).toContainText('5 January 2017 to 25 January 2017')
    await personalDetailsBlockPage.previous().click()
    // Change to original dates
    await hubPage.summaryRowLink('date-section').click()
    await dateQuestionBlockPage.yesICanReportForThisPeriod().click()
    await dateQuestionBlockPage.submit().click()
    await hubPage.submit().click()
    // Check the list collector has metadata dates in the title
    await verifyUrlContains(page, personalDetailsBlockPage.pageName)
    await expect(personalDetailsBlockPage.questionTitle()).toContainText('1 January 2017 to 1 February 2017')
  })
})
