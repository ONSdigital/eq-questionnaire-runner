import { test, expect } from '../../../fixtures/test'
import ConditionalCombinedRoutingPage from '../../../generated_pages/conditional_combined_routing/conditional-routing-block.page'
import ResponseAny from '../../../generated_pages/conditional_combined_routing/response-any.page'
import ResponseNotAny from '../../../generated_pages/conditional_combined_routing/response-not-any.page'
import SubmitPage from '../../../generated_pages/conditional_combined_routing/submit.page'

test.describe('Conditional combined routing.', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_conditional_combined_routing.json')
  })

  test('Given a list of radio options, When I choose the option "Yes" or the option "Sometimes", Then I should be routed to the relevant page', async ({
    page
  }) => {
    const conditionalCombinedRoutingPage = new ConditionalCombinedRoutingPage(page)
    const responseAny = new ResponseAny(page)
    await conditionalCombinedRoutingPage.yes().click()
    await conditionalCombinedRoutingPage.submit().click()
    await expect(page).toHaveURL(new RegExp(responseAny.pageName))

    // Or
    await responseAny.previous().click()

    await conditionalCombinedRoutingPage.sometimes().click()
    await conditionalCombinedRoutingPage.submit().click()

    await expect(page).toHaveURL(new RegExp(responseAny.pageName))
  })

  test('Given a list of radio options, When I choose the option "No, I prefer tea", Then I should be routed to the relevant page', async ({ page }) => {
    const conditionalCombinedRoutingPage = new ConditionalCombinedRoutingPage(page)
    const responseNotAny = new ResponseNotAny(page)
    await conditionalCombinedRoutingPage.noIPreferTea().click()
    await conditionalCombinedRoutingPage.submit().click()
    await expect(page).toHaveURL(new RegExp(responseNotAny.pageName))
  })

  test('Given a list of radio options, When I choose the option "No, I don\'t drink any hot drinks", Then I should be routed to the submit page', async ({
    page
  }) => {
    const conditionalCombinedRoutingPage = new ConditionalCombinedRoutingPage(page)
    const submitPage = new SubmitPage(page)
    await conditionalCombinedRoutingPage.noIDonTDrinkAnyHotDrinks().click()
    await conditionalCombinedRoutingPage.submit().click()
    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
  })
})
