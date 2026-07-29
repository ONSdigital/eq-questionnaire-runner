import { test, expect } from '../fixtures/test'
import IntroductionPage from '../generated_pages/introduction/introduction.page'

test.describe('Introduction page', () => {
  const introductionSchema = 'test_introduction.json'

  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire(introductionSchema)
  })

  test('Given I start a survey, When I view the introduction page, Then I should be able to see introduction information', async ({
    page,
    openQuestionnaire
  }) => {
    const introductionPage = new IntroductionPage(page)
    await openQuestionnaire(introductionSchema)
    await expect(introductionPage.useOfData()).toContainText('How we use your data')
    await expect(introductionPage.useOfInformation()).toContainText('Data should relate to all sites in England, Scotland and Wales unless otherwise stated.')
    await expect(introductionPage.legalResponse()).toHaveText('Your response is legally required')
    await expect(introductionPage.legalBasis()).toHaveText('Notice is given under section 999 of the Test Act 2000')
    await expect(introductionPage.introDescription()).toHaveText(
      'To take part, all you need to do is check that you have the information you need to answer the survey questions.'
    )
  })

  test('Given I start a survey, When preview content is set on the introduction page, Then the content headings should be displayed at the correct level', async ({
    page,
    openQuestionnaire
  }) => {
    const introductionPage = new IntroductionPage(page)
    await openQuestionnaire(introductionSchema)
    await expect(introductionPage.introQuestion(1).locator('h3')).toBeVisible()
  })

  test('Given I start a survey with introduction guidance set, When I view the introduction page, Then I should be able to see introduction guidance', async ({
    page,
    openQuestionnaire
  }) => {
    const introductionPage = new IntroductionPage(page)
    await openQuestionnaire(introductionSchema)
    await expect(introductionPage.guidancePanel(1)).toBeVisible()
    await expect(introductionPage.guidancePanel(1)).toContainText('Coronavirus (COVID-19) guidance')
    await expect(introductionPage.guidancePanel(1)).toContainText(
      'Explain your figures in the comment section to minimise us contacting you and to help us tell an industry story'
    )
  })
})
