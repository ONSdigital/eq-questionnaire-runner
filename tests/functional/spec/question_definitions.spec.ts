import { test, expect } from '../fixtures/test'
import DefinitionPage from '../generated_pages/question_definition/definition-block.page'

test.describe('Component: Definition', () => {
  test.describe('Given I start a survey which contains question definition', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_question_definition.json')
    })

    test('When I click the title link, then the description should be visible', async ({ page }) => {
      const definitionPage = new DefinitionPage(page)
      await expect(definitionPage.definitionContent()).toHaveAttribute('aria-hidden', 'true')

      await definitionPage.definitionTitle().click()

      await expect(definitionPage.definitionContent()).toHaveAttribute('aria-hidden', 'false')
      await expect(definitionPage.definitionContent()).toContainText(
        'A typical photovoltaic system employs solar panels, each comprising a number of solar cells, which generate electrical power.'
      )
    })

    test('When I click the title link twice, then the description should not be visible', async ({ page }) => {
      const definitionPage = new DefinitionPage(page)
      await expect(definitionPage.definitionContent()).toHaveAttribute('aria-hidden', 'true')

      await definitionPage.definitionTitle().click()
      await definitionPage.definitionTitle().click()

      await expect(definitionPage.definitionContent()).toHaveAttribute('aria-hidden', 'true')
    })
  })
})
