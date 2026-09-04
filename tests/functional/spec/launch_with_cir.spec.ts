import { test, expect } from '../fixtures/test'
import NameBlockPage from '../generated_pages/textfield/name-block.page'
import HubPage from '../base_pages/hub.page'
import ThankYouPage from '../base_pages/thank-you.page'

test.describe('Launch a survey from the collection instrument registry', () => {
  test.beforeEach('load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire(null, {
      cirInstrumentId: 'fd4a527f-c126-da2d-8ee6-51663a43e416'
    })
  })

  test('Given I retrieve a Collection Instrument, When I Launch, Then I am able to complete the survey as normal', async ({ page }) => {
    const nameBlockPage = new NameBlockPage(page)
    const hubPage = new HubPage(page)
    const thankYouPage = new ThankYouPage(page)

    await expect(page).toHaveURL(new RegExp(nameBlockPage.pageName))
    await nameBlockPage.name().fill('Joe')
    await nameBlockPage.submit().click()
    await hubPage.submit().click()
    await expect(page).toHaveURL(new RegExp(thankYouPage.pageName))
  })
})
