import { test, expect } from '../../../fixtures/test'
import FirstQuestionPage from '../../../generated_pages/progress_value_source_blocks/s1-b1.page'
import SecondQuestionPage from '../../../generated_pages/progress_value_source_blocks/s1-b2.page'
import ThirdQuestionPage from '../../../generated_pages/progress_value_source_blocks/s1-b3.page'
import ThirdQuestionSectionTwoPage from '../../../generated_pages/progress_value_source_section_enabled_no_hub/s2-b1.page'
import FourthQuestionPage from '../../../generated_pages/progress_value_source_blocks/s1-b4.page'
import FifthQuestionPage from '../../../generated_pages/progress_value_source_blocks/s1-b5.page'
import SixthQuestionPage from '../../../generated_pages/progress_value_source_blocks/s1-b6.page'
import SeventhQuestionPage from '../../../generated_pages/progress_value_source_blocks/s1-b7.page'
import SubmitPage from '../../../generated_pages/progress_value_source_blocks/submit.page'
import HubPage from '../../../base_pages/hub.page'

test.describe('Feature: Routing based on progress value sources using block identifiers', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_progress_value_source_blocks.json')
  })

  test('When the block being evaluated is incomplete (Q2), Then dependent questions should not be on the path or summary', async ({ page }) => {
    const firstQuestionPage = new FirstQuestionPage(page)
    const thirdQuestionPage = new ThirdQuestionPage(page)
    const fifthQuestionPage = new FifthQuestionPage(page)
    const seventhQuestionPage = new SeventhQuestionPage(page)
    const submitPage = new SubmitPage(page)

    await firstQuestionPage.q1A1().fill('0')
    await firstQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(thirdQuestionPage.pageName))
    await thirdQuestionPage.q1A1().fill('1')
    await thirdQuestionPage.submit().click()

    await fifthQuestionPage.q1A1().fill('2')
    await fifthQuestionPage.submit().click()

    await seventhQuestionPage.q1A1().fill('3')
    await seventhQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    await expect(page.locator('#main-content')).not.toContainText('Section 1 Question 2')
    await expect(page.locator('#main-content')).not.toContainText('Section 1 Question 4')
  })

  test('When the blocks being evaluated are complete (Q2 + Q5), Then dependent questions should be on path and summary', async ({ page }) => {
    const firstQuestionPage = new FirstQuestionPage(page)
    const secondQuestionPage = new SecondQuestionPage(page)
    const thirdQuestionPage = new ThirdQuestionPage(page)
    const fourthQuestionPage = new FourthQuestionPage(page)
    const fifthQuestionPage = new FifthQuestionPage(page)
    const sixthQuestionPage = new SixthQuestionPage(page)
    const seventhQuestionPage = new SeventhQuestionPage(page)
    const submitPage = new SubmitPage(page)

    await firstQuestionPage.q1A1().fill('1')
    await firstQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(secondQuestionPage.pageName))
    await secondQuestionPage.q1A1().fill('1')
    await secondQuestionPage.submit().click()

    await thirdQuestionPage.q1A1().fill('2')
    await thirdQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(fourthQuestionPage.pageName))
    await fourthQuestionPage.q1A1().fill('3')
    await fourthQuestionPage.submit().click()

    await fifthQuestionPage.q1A1().fill('4')
    await fifthQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(sixthQuestionPage.pageName))
    await sixthQuestionPage.q1A1().fill('5')
    await sixthQuestionPage.submit().click()

    await seventhQuestionPage.q1A1().fill('6')
    await seventhQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    await expect(page.locator('#main-content')).toContainText('Section 1 Question 4')
    await expect(page.locator('#main-content')).toContainText('Section 1 Question 6')
  })

  test('When an answer change completes the evaluated block, Then dependent questions should appear on path and summary', async ({ page }) => {
    const firstQuestionPage = new FirstQuestionPage(page)
    const secondQuestionPage = new SecondQuestionPage(page)
    const thirdQuestionPage = new ThirdQuestionPage(page)
    const fourthQuestionPage = new FourthQuestionPage(page)
    const fifthQuestionPage = new FifthQuestionPage(page)
    const sixthQuestionPage = new SixthQuestionPage(page)
    const seventhQuestionPage = new SeventhQuestionPage(page)
    const submitPage = new SubmitPage(page)

    await firstQuestionPage.q1A1().fill('0')
    await firstQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(thirdQuestionPage.pageName))
    await thirdQuestionPage.q1A1().fill('1')
    await thirdQuestionPage.submit().click()

    await fifthQuestionPage.q1A1().fill('2')
    await fifthQuestionPage.submit().click()

    await seventhQuestionPage.q1A1().fill('3')
    await seventhQuestionPage.submit().click()

    await submitPage.s1B1Q1A1Edit().click()
    await expect(page).toHaveURL(new RegExp(firstQuestionPage.pageName))
    await firstQuestionPage.q1A1().fill('1')
    await firstQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(secondQuestionPage.pageName))
    await secondQuestionPage.q1A1().fill('1')
    await secondQuestionPage.submit().click()

    await thirdQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(fourthQuestionPage.pageName))
    await fourthQuestionPage.q1A1().fill('3')
    await fourthQuestionPage.submit().click()

    await fifthQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(sixthQuestionPage.pageName))
    await sixthQuestionPage.q1A1().fill('3')
    await sixthQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    await expect(page.locator('#main-content')).toContainText('Section 1 Question 4')
    await expect(page.locator('#main-content')).toContainText('Section 1 Question 6')
  })

  test('When an edited answer makes the evaluated block incomplete, Then dependent questions should be removed from path and summary', async ({ page }) => {
    const firstQuestionPage = new FirstQuestionPage(page)
    const secondQuestionPage = new SecondQuestionPage(page)
    const thirdQuestionPage = new ThirdQuestionPage(page)
    const fourthQuestionPage = new FourthQuestionPage(page)
    const fifthQuestionPage = new FifthQuestionPage(page)
    const sixthQuestionPage = new SixthQuestionPage(page)
    const seventhQuestionPage = new SeventhQuestionPage(page)
    const submitPage = new SubmitPage(page)

    await firstQuestionPage.q1A1().fill('1')
    await firstQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(secondQuestionPage.pageName))
    await secondQuestionPage.q1A1().fill('1')
    await secondQuestionPage.submit().click()

    await thirdQuestionPage.q1A1().fill('2')
    await thirdQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(fourthQuestionPage.pageName))
    await fourthQuestionPage.q1A1().fill('3')
    await fourthQuestionPage.submit().click()

    await fifthQuestionPage.q1A1().fill('4')
    await fifthQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(sixthQuestionPage.pageName))
    await sixthQuestionPage.q1A1().fill('5')
    await sixthQuestionPage.submit().click()

    await seventhQuestionPage.q1A1().fill('6')
    await seventhQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    await submitPage.s1B1Q1A1Edit().click()
    await expect(page).toHaveURL(new RegExp(firstQuestionPage.pageName))

    await firstQuestionPage.q1A1().fill('0')
    await firstQuestionPage.submit().click()

    await expect(page.locator('#main-content')).not.toContainText('Section 1 Question 4')
    await expect(page.locator('#main-content')).not.toContainText('Section 1 Question 6')
  })
})

test.describe('Feature: Section enabled based on progress value sources using block identifiers (no hub)', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_progress_value_source_section_enabled_no_hub.json')
  })

  test('When the block being evaluated is complete, Then the dependent section should be enabled', async ({ page }) => {
    const firstQuestionPage = new FirstQuestionPage(page)
    const secondQuestionPage = new SecondQuestionPage(page)
    const thirdQuestionSectionTwoPage = new ThirdQuestionSectionTwoPage(page)

    await firstQuestionPage.q1A1().fill('0')
    await firstQuestionPage.submit().click()
    await secondQuestionPage.q1A1().fill('1')
    await secondQuestionPage.submit().click()

    await expect(page).toHaveURL(new RegExp(thirdQuestionSectionTwoPage.pageName))
  })
})

test.describe('Feature: Section enabled based on progress value sources using section identifiers', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_progress_value_source_section_enabled_hub.json')
  })

  test('When the evaluated section is complete, Then the dependent section should be enabled', async ({ page }) => {
    const firstQuestionPage = new FirstQuestionPage(page)
    const secondQuestionPage = new SecondQuestionPage(page)
    const hubPage = new HubPage(page)

    await hubPage.submit().click()
    await firstQuestionPage.q1A1().fill('0')
    await firstQuestionPage.submit().click()
    await secondQuestionPage.q1A1().fill('1')
    await secondQuestionPage.submit().click()

    await expect(hubPage.summaryRowState('section-2')).toHaveText('Not started')
  })

  test('When the evaluated section is incomplete, Then the dependent section should not be enabled', async ({ page }) => {
    const firstQuestionPage = new FirstQuestionPage(page)
    const hubPage = new HubPage(page)

    await hubPage.submit().click()
    await firstQuestionPage.q1A1().fill('0')
    await firstQuestionPage.submit().click()
    await page.goto(hubPage.url())

    await expect(hubPage.summaryRowState('section-1')).toHaveText('Partially completed')
    await expect(page.locator('#main-content')).not.toContainText('Section 2')
  })
})
