import { test, expect } from '../../../fixtures/test'
import RoutingCheckboxContains from '../../../generated_pages/routing_checkbox_contains/country-checkbox.page'
import ContainsAllPage from '../../../generated_pages/routing_checkbox_contains/country-interstitial-all.page'
import ContainsAnyPage from '../../../generated_pages/routing_checkbox_contains/country-interstitial-any.page'
import SubmitPage from '../../../generated_pages/routing_checkbox_contains/submit.page'

test.describe('Routing Checkbox Contains Condition.', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_routing_checkbox_contains.json')
  })

  test(
    'Given a list of checkbox options, When I have don\'t select "Liechtenstein" and select the option "India" ' +
      'or the option "Azerbaijan" or both then I should be routed to the "contains any" condition page',
    async ({ page }) => {
      const containsAnyPage = new ContainsAnyPage(page)
      const routingCheckboxContains = new RoutingCheckboxContains(page)
      await expect(routingCheckboxContains.liechtenstein()).not.toBeChecked()

      await routingCheckboxContains.india().click()
      await routingCheckboxContains.submit().click()
      await expect(page).toHaveURL(new RegExp(containsAnyPage.pageName))

      // Or
      await containsAnyPage.previous().click()

      await routingCheckboxContains.india().click()
      await routingCheckboxContains.azerbaijan().click()
      await routingCheckboxContains.submit().click()

      await expect(page).toHaveURL(new RegExp(containsAnyPage.pageName))

      // Or
      await containsAnyPage.previous().click()

      await routingCheckboxContains.india().click()
      await routingCheckboxContains.submit().click()

      await expect(page).toHaveURL(new RegExp(containsAnyPage.pageName))
    }
  )

  test('Given a list of checkbox options, When I select the option "Malta" or the option "Liechtenstein" or both then I should be routed to the summary condition page', async ({
    page
  }) => {
    const containsAnyPage = new ContainsAnyPage(page)
    const routingCheckboxContains = new RoutingCheckboxContains(page)
    const submitPage = new SubmitPage(page)
    await routingCheckboxContains.liechtenstein().click()
    await routingCheckboxContains.submit().click()
    await expect(page).toHaveURL(new RegExp(submitPage.pageName))

    // Or
    await containsAnyPage.previous().click()

    await routingCheckboxContains.liechtenstein().click()
    await routingCheckboxContains.malta().click()
    await routingCheckboxContains.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))

    // Or
    await containsAnyPage.previous().click()

    await routingCheckboxContains.liechtenstein().click()
    await routingCheckboxContains.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
  })

  test('Given a list of checkbox options, When I select the options "India", "Azerbaijan" and "Liechtenstein" Then I should be routed to the "contains all" condition page', async ({
    page
  }) => {
    const containsAllPage = new ContainsAllPage(page)
    const routingCheckboxContains = new RoutingCheckboxContains(page)
    await routingCheckboxContains.india().click()
    await routingCheckboxContains.azerbaijan().click()
    await routingCheckboxContains.liechtenstein().click()
    await routingCheckboxContains.submit().click()
    await expect(page).toHaveURL(new RegExp(containsAllPage.pageName))
  })
})
