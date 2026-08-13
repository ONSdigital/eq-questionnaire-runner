import { test, expect } from '../fixtures/test'
import ListCollectorPage from '../generated_pages/variants_first_item_in_list/list-collector.page'
import ListCollectorAddPage from '../generated_pages/variants_first_item_in_list/list-collector-add.page'
import ListStatusQuestion from '../generated_pages/variants_first_item_in_list/list-status.page'
import HubPage from '../base_pages/hub.page'

test.describe('Question Variants First Item in List', () => {
  test('Given I am the first person on the list, When the when rule is set, Then I should the correct question variant', async ({
    page,
    openQuestionnaire
  }) => {
    const hubPage = new HubPage(page)
    const listCollectorAddPage = new ListCollectorAddPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const listStatusQuestion = new ListStatusQuestion(page)
    await openQuestionnaire('test_variants_first_item_in_list.json')
    await hubPage.submit().click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await listCollectorAddPage.firstName().fill('Marcus')
    await listCollectorAddPage.lastName().fill('Twin')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await hubPage.submit().click()
    await expect(listStatusQuestion.questionText()).toHaveText('You are the first person in the list')
  })

  test('Given I am the second person on the list, When the when rule is set, Then I should the correct question variant', async ({
    page,
    openQuestionnaire
  }) => {
    const hubPage = new HubPage(page)
    const listCollectorAddPage = new ListCollectorAddPage(page)
    const listCollectorPage = new ListCollectorPage(page)
    const listStatusQuestion = new ListStatusQuestion(page)
    await openQuestionnaire('test_variants_first_item_in_list.json')
    await hubPage.submit().click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await listCollectorAddPage.firstName().fill('Marcus')
    await listCollectorAddPage.lastName().fill('Twin')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.yes().click()
    await listCollectorPage.submit().click()
    await listCollectorAddPage.firstName().fill('John')
    await listCollectorAddPage.lastName().fill('Doe')
    await listCollectorAddPage.submit().click()
    await listCollectorPage.no().click()
    await listCollectorPage.submit().click()
    await hubPage.summaryRowLink('personal-details-section-2').click()
    await expect(listStatusQuestion.questionText()).toHaveText('You are not the first person in the list')
  })
})
