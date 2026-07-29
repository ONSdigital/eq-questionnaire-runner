import { test, expect } from '../../../../fixtures/test'
import type { Page } from '../../../../fixtures/test'
import ListCollectorPage from '../../../../generated_pages/validation_sum_against_total_dynamic_answers/list-collector.page'
import ListCollectorAddPage from '../../../../generated_pages/validation_sum_against_total_dynamic_answers/list-collector-add.page'
import DynamicAnswerPage from '../../../../generated_pages/validation_sum_against_total_dynamic_answers/dynamic-answer.page'
import DynamicAnswerOnlyPage from '../../../../generated_pages/validation_sum_against_total_dynamic_answers/dynamic-answer-only.page'
import TotalBlockPage from '../../../../generated_pages/validation_sum_against_total_dynamic_answers/total-block.page'
import DriverPage from '../../../../generated_pages/validation_sum_against_total_dynamic_answers/any-supermarket.page'
import SectionSummaryPage from '../../../../generated_pages/validation_sum_against_total_dynamic_answers/dynamic-answers-section-summary.page'
import ListCollectorRemovePage from '../../../../generated_pages/validation_sum_against_total_dynamic_answers/list-collector-remove.page'
import ListCollectorEditPage from '../../../../generated_pages/validation_sum_against_total_dynamic_answers/list-collector-edit.page'
import HubPage from '../../../../base_pages/hub.page'
import TotalBlockOtherPage from '../../../../generated_pages/validation_sum_against_total_dynamic_answers/total-block-other.page'

test.describe('Feature: Sum of dynamic answers based on list and optional static answers equal to validation against total ', () => {
  const summaryTitles = 'dt[class="ons-summary__item-title"]'

  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_validation_sum_against_total_dynamic_answers.json')
  })

  test.describe('Given I add list items with hardcoded total used for validation of dynamic answers', () => {
    test(
      "When I continue and enter numbers on dynamic and static answers page that don't add up to that total, " +
        'Then validation error should be displayed with appropriate message',
      async ({ page }) => {
        const dynamicAnswerPage = new DynamicAnswerPage(page)
        const totalBlockPage = new TotalBlockPage(page)
        await totalBlockPage.acceptCookies().click()
        await addTwoSupermarkets(page)
        await expect(page).toHaveURL(new RegExp(dynamicAnswerPage.pageName))
        await expect(dynamicAnswerPage.labels()).toHaveCount(3)
        await dynamicAnswerPage.inputs().nth(0).fill('33')
        await dynamicAnswerPage.inputs().nth(1).fill('33')
        await dynamicAnswerPage.percentageOfShoppingElsewhere().fill('33')
        await dynamicAnswerPage.submit().click()
        await expect(dynamicAnswerPage.errorNumber(1)).toHaveText('Enter answers that add up to 100')
      }
    )
  })

  test.describe('Given I add list items with hardcoded total used for validation of dynamic answers', () => {
    test('When I continue and enter numbers on dynamic and static answers page that add up to that total, Then I should be able to get to the subsequent question', async ({
      page
    }) => {
      const dynamicAnswerPage = new DynamicAnswerPage(page)
      const totalBlockOtherPage = new TotalBlockOtherPage(page)
      await addTwoSupermarkets(page)
      await expect(page).toHaveURL(new RegExp(dynamicAnswerPage.pageName))
      await expect(dynamicAnswerPage.labels()).toHaveCount(3)
      await dynamicAnswerPage.inputs().nth(0).fill('34')
      await dynamicAnswerPage.inputs().nth(1).fill('33')
      await dynamicAnswerPage.percentageOfShoppingElsewhere().fill('33')
      await dynamicAnswerPage.submit().click()
      await expect(page).toHaveURL(new RegExp(totalBlockOtherPage.pageName))
    })
  })

  test.describe('Given I add list items with custom total used for validation of dynamic answers', () => {
    test(
      "When I continue and enter numbers on dynamic answers only page that don't add up to that total, " +
        'Then validation error should be displayed with appropriate message',
      async ({ page }) => {
        const dynamicAnswerOnlyPage = new DynamicAnswerOnlyPage(page)
        const dynamicAnswerPage = new DynamicAnswerPage(page)
        const totalBlockOtherPage = new TotalBlockOtherPage(page)
        await addTwoSupermarkets(page)
        await expect(page).toHaveURL(new RegExp(dynamicAnswerPage.pageName))
        await expect(dynamicAnswerPage.labels()).toHaveCount(3)
        await dynamicAnswerPage.inputs().nth(0).fill('34')
        await dynamicAnswerPage.inputs().nth(1).fill('33')
        await dynamicAnswerPage.percentageOfShoppingElsewhere().fill('33')
        await dynamicAnswerPage.submit().click()
        await totalBlockOtherPage.totalOther().fill('100')
        await totalBlockOtherPage.submit().click()
        await expect(page).toHaveURL(new RegExp(dynamicAnswerOnlyPage.pageName))
        await dynamicAnswerOnlyPage.inputs().nth(0).fill('50')
        await dynamicAnswerOnlyPage.inputs().nth(1).fill('0')
        await dynamicAnswerOnlyPage.submit().click()
        await expect(dynamicAnswerOnlyPage.errorNumber(1)).toHaveText('Enter answers that add up to £100.00')
      }
    )
  })

  test.describe('Given I add list items with custom total used for validation of dynamic answers', () => {
    test('When I continue and enter numbers on dynamic answers only page that add up to that total, Then I should be able to get to the summary', async ({
      page
    }) => {
      const dynamicAnswerPage = new DynamicAnswerPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      await addTwoSupermarkets(page)
      await expect(page).toHaveURL(new RegExp(dynamicAnswerPage.pageName))
      await fillDynamicAnswers(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.pageName))
    })
  })

  test.describe('Given I add list items and fill all the dynamic answers', () => {
    test('When I continue and add another list item, Then I should be revisiting dynamic answers which should be updated to reflect the changes', async ({
      page
    }) => {
      const dynamicAnswerPage = new DynamicAnswerPage(page)
      const listCollectorAddPage = new ListCollectorAddPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      await addTwoSupermarkets(page)
      await expect(dynamicAnswerPage.labels()).toHaveCount(3)
      await fillDynamicAnswers(page)
      await sectionSummaryPage.supermarketsListAddLink().click()
      await listCollectorAddPage.supermarketName().fill('Morrisons')
      await listCollectorAddPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await expect(page).toHaveURL(new RegExp(dynamicAnswerPage.pageName))
      await expect(dynamicAnswerPage.labels()).toHaveCount(4)
    })
  })

  test.describe('Given I add list items and fill all the dynamic answers', () => {
    test('When I continue and remove existing list item, Then I should be revisiting dynamic answers which should be updated to reflect the changes', async ({
      page
    }) => {
      const dynamicAnswerPage = new DynamicAnswerPage(page)
      const listCollectorRemovePage = new ListCollectorRemovePage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      await addTwoSupermarkets(page)
      await fillDynamicAnswers(page)
      await sectionSummaryPage.supermarketsListRemoveLink(1).click()
      await listCollectorRemovePage.yes().click()
      await listCollectorRemovePage.submit().click()
      await expect(page).toHaveURL(new RegExp(dynamicAnswerPage.pageName))
      await expect(dynamicAnswerPage.labels()).toHaveCount(2)
    })
  })

  test.describe('Given I add list items and fill all the dynamic answers', () => {
    test('When I continue and edit existing list item, Then I should return straight to the summary because the dynamic answers do not depend on the supermarket name', async ({
      page
    }) => {
      const listCollectorEditPage = new ListCollectorEditPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      await addTwoSupermarkets(page)
      await fillDynamicAnswers(page)
      await sectionSummaryPage.supermarketsListEditLink(1).click()
      await listCollectorEditPage.supermarketName().fill('Aldi')
      await listCollectorEditPage.submit().click()
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.pageName))
      await expect(sectionSummaryPage.groupContent(2).locator(summaryTitles).nth(0)).toHaveText('Percentage of shopping at Aldi')
    })
  })

  test.describe('Given I add list items and fill all the dynamic answers', () => {
    test('When I journey backwards, Then I should be revisiting all the previous blocks', async ({ page }) => {
      const driverPage = new DriverPage(page)
      const dynamicAnswerOnlyPage = new DynamicAnswerOnlyPage(page)
      const dynamicAnswerPage = new DynamicAnswerPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      const totalBlockOtherPage = new TotalBlockOtherPage(page)
      await addTwoSupermarkets(page)
      await fillDynamicAnswers(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.pageName))
      await sectionSummaryPage.previous().click()
      await dynamicAnswerOnlyPage.previous().click()
      await totalBlockOtherPage.previous().click()
      await dynamicAnswerPage.previous().click()
      await listCollectorPage.previous().click()
      await expect(page).toHaveURL(new RegExp(driverPage.pageName))
    })
  })
})

async function addTwoSupermarkets (page: Page): Promise<void> {
  const totalBlockPage = new TotalBlockPage(page)
  const hubPage = new HubPage(page)
  const driverPage = new DriverPage(page)
  const listCollectorAddPage = new ListCollectorAddPage(page)
  const listCollectorPage = new ListCollectorPage(page)
  await totalBlockPage.total().fill('100')
  await totalBlockPage.submit().click()
  await hubPage.summaryRowLink('dynamic-answers-section').click()
  await driverPage.yes().click()
  await driverPage.submit().click()
  await listCollectorAddPage.supermarketName().fill('Tesco')
  await listCollectorAddPage.submit().click()
  await listCollectorPage.yes().click()
  await listCollectorPage.submit().click()
  await listCollectorAddPage.supermarketName().fill('Asda')
  await listCollectorAddPage.submit().click()
  await listCollectorPage.no().click()
  await listCollectorPage.submit().click()
}

async function fillDynamicAnswers (page: Page): Promise<void> {
  const dynamicAnswerPage = new DynamicAnswerPage(page)
  const totalBlockOtherPage = new TotalBlockOtherPage(page)
  const dynamicAnswerOnlyPage = new DynamicAnswerOnlyPage(page)
  await dynamicAnswerPage.inputs().nth(0).fill('34')
  await dynamicAnswerPage.inputs().nth(1).fill('33')
  await dynamicAnswerPage.percentageOfShoppingElsewhere().fill('33')
  await dynamicAnswerPage.submit().click()
  await totalBlockOtherPage.totalOther().fill('100')
  await totalBlockOtherPage.submit().click()
  await dynamicAnswerOnlyPage.inputs().nth(0).fill('50')
  await dynamicAnswerOnlyPage.inputs().nth(1).fill('50')
  await dynamicAnswerOnlyPage.submit().click()
}
