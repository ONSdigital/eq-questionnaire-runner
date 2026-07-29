import { test, expect } from '../../../fixtures/test'
import RouteComparison1Page from '../../../generated_pages/routing_answer_comparison/route-comparison-1.page'
import RouteComparison2Page from '../../../generated_pages/routing_answer_comparison/route-comparison-2.page'

test.describe('Test routing skip', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_routing_answer_comparison.json')
  })

  test('Given we start the routing test survey, When we enter a low number then a high number, Then, we should be routed to the fourth page', async ({
    page
  }) => {
    const routeComparison1Page = new RouteComparison1Page(page)
    const routeComparison2Page = new RouteComparison2Page(page)
    await routeComparison1Page.answer().fill('1')
    await routeComparison1Page.submit().click()
    await routeComparison2Page.answer().fill('2')
    await routeComparison2Page.submit().click()
    await expect(page.locator('#main-content > p')).toHaveText('This page should never be skipped')
  })

  test('Given we start the routing test survey, When we enter a high number then a low number, Then, we should be routed to the third page', async ({
    page
  }) => {
    const routeComparison1Page = new RouteComparison1Page(page)
    const routeComparison2Page = new RouteComparison2Page(page)
    await routeComparison1Page.answer().fill('1')
    await routeComparison1Page.submit().click()
    await routeComparison2Page.answer().fill('0')
    await routeComparison2Page.submit().click()
    await expect(page.locator('#main-content > p')).toHaveText('This page should be skipped if your second answer was higher than your first')
  })

  test('Given we start the routing test survey, When we enter an equal number on both questions, Then, we should be routed to the third page', async ({
    page
  }) => {
    const routeComparison1Page = new RouteComparison1Page(page)
    const routeComparison2Page = new RouteComparison2Page(page)
    await routeComparison1Page.answer().fill('1')
    await routeComparison1Page.submit().click()
    await routeComparison2Page.answer().fill('1')
    await routeComparison2Page.submit().click()
    await expect(page.locator('#main-content > p')).toHaveText('This page should be skipped if your second answer was higher than your first')
  })
})
