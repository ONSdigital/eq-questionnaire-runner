import { test, expect } from '../../../fixtures/test'
import Comparison1Page from '../../../generated_pages/skip_condition_answer_comparison/comparison-1.page'
import Comparison2Page from '../../../generated_pages/skip_condition_answer_comparison/comparison-2.page'

test.describe('Test skip condition answer comparisons', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_skip_condition_answer_comparison.json')
  })

  test('Given we start the skip condition survey, When we enter the same answers, Then the interstitial should show that the answers are the same', async ({
    page
  }) => {
    const comparison1Page = new Comparison1Page(page)
    const comparison2Page = new Comparison2Page(page)
    await comparison1Page.answer().fill('1')
    await comparison1Page.submit().click()
    await comparison2Page.answer().fill('1')
    await comparison2Page.submit().click()
    await expect(page.locator('#main-content > p')).toHaveText('Your second number was equal to your first number')
  })

  test('Given we start the skip condition survey, When we enter a high number then a low number, Then the interstitial should show that the answers are low then high', async ({
    page
  }) => {
    const comparison1Page = new Comparison1Page(page)
    const comparison2Page = new Comparison2Page(page)
    await comparison1Page.answer().fill('3')
    await comparison1Page.submit().click()
    await comparison2Page.answer().fill('2')
    await comparison2Page.submit().click()
    await expect(page.locator('#main-content > p')).toHaveText('Your first answer was greater than your second number')
  })

  test('Given we start the skip condition survey, When we enter a low number then a high number, Then the interstitial should show that the answers are high then low', async ({
    page
  }) => {
    const comparison1Page = new Comparison1Page(page)
    const comparison2Page = new Comparison2Page(page)
    await comparison1Page.answer().fill('1')
    await comparison1Page.submit().click()
    await comparison2Page.answer().fill('2')
    await comparison2Page.submit().click()
    await expect(page.locator('#main-content > p')).toHaveText('Your first answer was less than your second number')
  })
})
