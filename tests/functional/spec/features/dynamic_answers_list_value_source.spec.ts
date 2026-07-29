import { test, expect } from '../../fixtures/test'
import type { Page } from '../../fixtures/test'
import DriverPage from '../../generated_pages/dynamic_answers_list_source/any-supermarket.page'
import DynamicAnswerPage from '../../generated_pages/dynamic_answers_list_source/dynamic-answer.page'
import DynamicAnswerOnlyPage from '../../generated_pages/dynamic_answers_list_source/dynamic-answer-only.page'
import ListCollectorPage from '../../generated_pages/dynamic_answers_list_source/list-collector.page'
import ListCollectorAddPage from '../../generated_pages/dynamic_answers_list_source/list-collector-add.page'
import ListCollectorRemovePage from '../../generated_pages/dynamic_answers_list_source/list-collector-remove.page'
import SetMinimumPage from '../../generated_pages/dynamic_answers_list_source/minimum-spending.page'
import SectionSummaryPage from '../../generated_pages/dynamic_answers_list_source/list-collector-section-summary.page'
import HubPage from '../../base_pages/hub.page'
import OnlineShoppingPage from '../../generated_pages/dynamic_answers_list_source/dynamic-answer-separate-section.page'

test.describe('Dynamic answers list value source', () => {
  const summaryTitles = '.ons-summary__item-title'
  const summaryValues = '.ons-summary__values'
  const summaryActions = '.ons-summary__actions'

  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_dynamic_answers_list_source.json')
  })

  test('Given list items have been added, When the dynamic answers are displayed, Then the correct answers should be visible', async ({ page }) => {
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    await addTwoSupermarkets(page)
    await expect(dynamicAnswerPage.labels().nth(0)).toHaveText('Percentage of shopping at Tesco')
    await expect(dynamicAnswerPage.labels().nth(1)).toHaveText('Percentage of shopping at Aldi')
    await expect(dynamicAnswerPage.labels()).toHaveCount(4)
  })

  test('Given list items have been added, When additional items are added using add link, Then the correct dynamic answers are displayed', async ({ page }) => {
    const driverPage = new DriverPage(page)
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    const listCollectorAddPage = new ListCollectorAddPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const sectionSummaryPage = new SectionSummaryPage(page)
    await driverPage.yes().click()
    await driverPage.submit().click()
    await listCollectorAddPage.supermarketName().fill('Tesco')
    await listCollectorAddPage.setMaximum().fill('10000')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await expect(dynamicAnswerPage.labels().nth(0)).toHaveText('Percentage of shopping at Tesco')
    await expect(dynamicAnswerPage.labels()).toHaveCount(2)
    await setMinimumAndGetSectionSummary(page)
    await sectionSummaryPage.supermarketsListAddLink().click()
    await listCollectorAddPage.supermarketName().fill('Aldi')
    await listCollectorAddPage.setMaximum().fill('10000')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await expect(dynamicAnswerPage.labels().nth(0)).toHaveText('Percentage of shopping at Tesco')
    await expect(dynamicAnswerPage.labels().nth(1)).toHaveText('Percentage of shopping at Aldi')
    await expect(dynamicAnswerPage.labels()).toHaveCount(4)
  })

  test('Given list items have been added and the dynamic answers are submitted, When the summary is displayed, Then the correct answers should be visible and have correct values', async ({
    page
  }) => {
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    const sectionSummaryPage = new SectionSummaryPage(page)
    await addTwoSupermarkets(page)
    await dynamicAnswerPage.inputs().nth(0).fill('12')
    await dynamicAnswerPage.inputs().nth(1).fill('21')
    await dynamicAnswerPage.inputs().nth(2).fill('3')
    await dynamicAnswerPage.inputs().nth(3).fill('7')
    await setMinimumAndGetSectionSummary(page)
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryTitles).nth(0)).toHaveText('Percentage of shopping at Tesco')
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues).nth(0)).toHaveText('12%')
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryTitles).nth(1)).toHaveText('Percentage of shopping at Aldi')
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues).nth(1)).toHaveText('21%')
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues).nth(2)).toHaveText('3')
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues).nth(3)).toHaveText('7')
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryTitles)).toHaveCount(8)
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues)).toHaveCount(8)
  })

  test('Given list items have been added and the dynamic answers are submitted, When the dynamic answers are revisited, Then they should be visible and have correct values', async ({
    page
  }) => {
    const dynamicAnswerOnlyPage = new DynamicAnswerOnlyPage(page)
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    const sectionSummaryPage = new SectionSummaryPage(page)
    const setMinimumPage = new SetMinimumPage(page)
    await addTwoSupermarkets(page)
    await dynamicAnswerPage.inputs().nth(0).fill('12')
    await dynamicAnswerPage.inputs().nth(1).fill('21')
    await setMinimumAndGetSectionSummary(page)
    await sectionSummaryPage.previous().click()
    await dynamicAnswerOnlyPage.previous().click()
    await setMinimumPage.previous().click()
    await expect(page).toHaveURL(new RegExp(dynamicAnswerPage.pageName))
    await expect(dynamicAnswerPage.inputs().nth(0)).toHaveValue('12')
    await expect(dynamicAnswerPage.inputs().nth(1)).toHaveValue('21')
    await expect(dynamicAnswerPage.labels().nth(0)).toHaveText('Percentage of shopping at Tesco')
    await expect(dynamicAnswerPage.labels().nth(1)).toHaveText('Percentage of shopping at Aldi')
  })

  test('Given list items have been added and the dynamic answers are submitted, When the dynamic answers are resubmitted with different values, Then they should be displayed correctly on summary', async ({
    page
  }) => {
    const dynamicAnswerOnlyPage = new DynamicAnswerOnlyPage(page)
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    const sectionSummaryPage = new SectionSummaryPage(page)
    const setMinimumPage = new SetMinimumPage(page)
    await addTwoSupermarkets(page)
    await dynamicAnswerPage.inputs().nth(0).fill('12')
    await dynamicAnswerPage.inputs().nth(1).fill('21')
    await setMinimumAndGetSectionSummary(page)
    await sectionSummaryPage.previous().click()
    await dynamicAnswerOnlyPage.previous().click()
    await setMinimumPage.previous().click()
    await dynamicAnswerPage.inputs().nth(0).fill('21')
    await dynamicAnswerPage.inputs().nth(1).fill('12')
    await dynamicAnswerPage.submit().click()
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues).nth(0)).toHaveText('21%')
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues).nth(1)).toHaveText('12%')
  })

  test('Given list items have been added and the dynamic answers are submitted, When the summary edit answer link is used for dynamic answer, Then the focus is on correct answer option', async ({
    page
  }) => {
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    const sectionSummaryPage = new SectionSummaryPage(page)
    await addTwoSupermarkets(page)
    await dynamicAnswerPage.inputs().nth(0).fill('12')
    await dynamicAnswerPage.inputs().nth(1).fill('21')
    await setMinimumAndGetSectionSummary(page)
    await sectionSummaryPage.listCollectorGroupContent(2).locator(summaryActions).nth(0).locator('a').click()
    await expect(page).toHaveURL(new RegExp(dynamicAnswerPage.pageName))
    await expect(dynamicAnswerPage.inputs().nth(0)).toBeFocused()
    await dynamicAnswerPage.submit().click()
    await sectionSummaryPage.listCollectorGroupContent(2).locator(summaryActions).nth(1).locator('a').click()
    await expect(page).toHaveURL(new RegExp(dynamicAnswerPage.pageName))
    await expect(dynamicAnswerPage.inputs().nth(1)).toBeFocused()
  })

  test('Given list items have been added and the dynamic answers are submitted, When the dynamic answers are resubmitted with answers updated, Then they should be displayed correctly on summary', async ({
    page
  }) => {
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    const sectionSummaryPage = new SectionSummaryPage(page)
    await addTwoSupermarkets(page)
    await dynamicAnswerPage.inputs().nth(0).fill('12')
    await dynamicAnswerPage.inputs().nth(1).fill('21')
    await setMinimumAndGetSectionSummary(page)
    await sectionSummaryPage.listCollectorGroupContent(2).locator(summaryActions).nth(0).locator('a').click()
    await dynamicAnswerPage.inputs().nth(0).fill('21')
    await dynamicAnswerPage.submit().click()
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues).nth(0)).toHaveText('21%')
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues).nth(1)).toHaveText('21%')
  })

  test('Given list items have been added and the dynamic answers are submitted, When the list items are removed and answers updated, Then they should be displayed correctly on summary', async ({
    page
  }) => {
    const dynamicAnswerOnlyPage = new DynamicAnswerOnlyPage(page)
    const dynamicAnswerPage = new DynamicAnswerPage(page)
    const listCollectorRemovePage = new ListCollectorRemovePage(page)
    const sectionSummaryPage = new SectionSummaryPage(page)
    await addTwoSupermarkets(page)
    await dynamicAnswerPage.inputs().nth(0).fill('12')
    await dynamicAnswerPage.inputs().nth(1).fill('21')
    await setMinimumAndGetSectionSummary(page)
    await sectionSummaryPage.supermarketsListRemoveLink(1).click()
    await listCollectorRemovePage.yes().click()
    await listCollectorRemovePage.submit().click()
    await dynamicAnswerPage.submit().click()
    await dynamicAnswerOnlyPage.submit().click()
    await expect(page).toHaveURL(new RegExp(sectionSummaryPage.pageName))
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryTitles).nth(0)).toHaveText('Percentage of shopping at Aldi')
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues).nth(0)).toHaveText('21%')
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryTitles)).toHaveCount(5)
    await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues)).toHaveCount(5)
  })

  test(
    'Given list items have been added and the dynamic answers are submitted, ' +
      "When the driving question is changed to 'No' and subsequently changed back to 'Yes', Then all answers should re-appear on summary",
    async ({ page }) => {
      const driverPage = new DriverPage(page)
      const dynamicAnswerPage = new DynamicAnswerPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      await addTwoSupermarkets(page)
      await dynamicAnswerPage.inputs().nth(0).fill('12')
      await dynamicAnswerPage.inputs().nth(1).fill('21')
      await dynamicAnswerPage.inputs().nth(2).fill('3')
      await dynamicAnswerPage.inputs().nth(3).fill('7')
      await setMinimumAndGetSectionSummary(page)
      await sectionSummaryPage.anySupermarketAnswerEdit().click()
      await driverPage.no().click()
      await driverPage.submit().click()
      await expect(page.locator('#main-content')).not.toContainText('Percentage of shopping at Tesco')
      await expect(page.locator('#main-content')).not.toContainText('Percentage of shopping at Aldi')
      await sectionSummaryPage.anySupermarketAnswerEdit().click()
      await driverPage.yes().click()
      await driverPage.submit().click()

      await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryTitles).nth(0)).toHaveText('Percentage of shopping at Tesco')
      await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues).nth(0)).toHaveText('12%')
      await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryTitles).nth(1)).toHaveText('Percentage of shopping at Aldi')
      await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues).nth(1)).toHaveText('21%')
      await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues).nth(2)).toHaveText('3')
      await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues).nth(3)).toHaveText('7')
      await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryTitles)).toHaveCount(8)
      await expect(sectionSummaryPage.listCollectorGroupContent(2).locator(summaryValues)).toHaveCount(8)
    }
  )

  test('Given list items have been added, When the dynamic answers are displayed in a separate section, Then the correct answers should be visible', async ({
    page
  }) => {
    const onlineShoppingPage = new OnlineShoppingPage(page)
    await addTwoSupermarketsAndGetToNextSection(page)
    await expect(onlineShoppingPage.labels().nth(0)).toHaveText('Percentage of online shopping at Tesco')
    await expect(onlineShoppingPage.labels().nth(1)).toHaveText('Percentage of online shopping at Aldi')
    await expect(onlineShoppingPage.labels()).toHaveCount(4)
  })
})

async function addTwoSupermarkets (page: Page): Promise<void> {
  const driverPage = new DriverPage(page)
  const listCollectorAddPage = new ListCollectorAddPage(page)
  const listCollectorPage = new ListCollectorPage(page)
  await driverPage.yes().click()
  await driverPage.submit().click()
  await listCollectorAddPage.supermarketName().fill('Tesco')
  await listCollectorAddPage.setMaximum().fill('10000')
  await listCollectorAddPage.submit().click()
  await listCollectorPage.yes().click()
  await listCollectorPage.submit().click()
  await listCollectorAddPage.supermarketName().fill('Aldi')
  await listCollectorAddPage.setMaximum().fill('10000')
  await listCollectorAddPage.submit().click()
  await listCollectorPage.no().click()
  await listCollectorPage.submit().click()
}

async function addTwoSupermarketsAndGetToNextSection (page: Page): Promise<void> {
  const driverPage = new DriverPage(page)
  const listCollectorAddPage = new ListCollectorAddPage(page)
  const listCollectorPage = new ListCollectorPage(page)
  const dynamicAnswerPage = new DynamicAnswerPage(page)
  const sectionSummaryPage = new SectionSummaryPage(page)
  const hubPage = new HubPage(page)
  await driverPage.yes().click()
  await driverPage.submit().click()
  await listCollectorAddPage.supermarketName().waitFor()
  await listCollectorAddPage.supermarketName().fill('Tesco')
  await listCollectorAddPage.setMaximum().fill('10000')
  await listCollectorAddPage.submit().click()
  await listCollectorPage.yes().click()
  await listCollectorPage.submit().click()
  await listCollectorAddPage.supermarketName().fill('Aldi')
  await listCollectorAddPage.setMaximum().fill('10000')
  await listCollectorAddPage.submit().click()
  await listCollectorPage.no().click()
  await listCollectorPage.submit().click()
  await dynamicAnswerPage.inputs().nth(0).fill('12')
  await dynamicAnswerPage.inputs().nth(1).fill('21')
  await dynamicAnswerPage.inputs().nth(2).fill('3')
  await dynamicAnswerPage.inputs().nth(3).fill('7')
  await setMinimumAndGetSectionSummary(page)
  await sectionSummaryPage.submit().click()
  await hubPage.submit().click()
}

async function setMinimumAndGetSectionSummary (page: Page): Promise<void> {
  const dynamicAnswerPage = new DynamicAnswerPage(page)
  const setMinimumPage = new SetMinimumPage(page)
  const dynamicAnswerOnlyPage = new DynamicAnswerOnlyPage(page)
  await dynamicAnswerPage.submit().click()
  await setMinimumPage.setMinimum().fill('2')
  await setMinimumPage.submit().click()
  await dynamicAnswerOnlyPage.submit().click()
}
