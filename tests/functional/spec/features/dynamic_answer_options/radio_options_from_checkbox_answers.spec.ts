import { test, expect } from '../../../fixtures/test'
import InjurySustainedPage from '../../../generated_pages/dynamic_radio_options_from_checkbox/injury-sustained.page'
import MostSeriousInjuryPage from '../../../generated_pages/dynamic_radio_options_from_checkbox/most-serious-injury.page'
import HealedTheQuickestPage from '../../../generated_pages/dynamic_radio_options_from_checkbox/healed-the-quickest.page'
import SubmitPage from '../../../generated_pages/dynamic_radio_options_from_checkbox/submit.page'

test.describe('Dynamic radio options from checkbox answers', () => {
  test('When checkbox answers are submitted, Then next radio question includes those answers plus static option', async ({ page, openQuestionnaire }) => {
    const injurySustainedPage = new InjurySustainedPage(page)
    const mostSeriousInjuryPage = new MostSeriousInjuryPage(page)
    await openQuestionnaire('test_dynamic_radio_options_from_checkbox.json')

    await injurySustainedPage.head().click()
    await injurySustainedPage.body().click()
    await injurySustainedPage.submit().click()

    await expect(page).toHaveURL(new RegExp(mostSeriousInjuryPage.pageName))
    await expect(mostSeriousInjuryPage.answerLabelByIndex(0)).toHaveText('Head')
    await expect(mostSeriousInjuryPage.answerLabelByIndex(1)).toHaveText('Body')
    await expect(mostSeriousInjuryPage.answerLabelByIndex(2)).toHaveText('They were of equal severity (static option)')
    await expect(mostSeriousInjuryPage.answerLabelByIndex(3)).toHaveCount(0)
  })

  test('When first dynamic radio is answered, Then second dynamic radio only includes checkbox-derived options', async ({ page, openQuestionnaire }) => {
    const injurySustainedPage = new InjurySustainedPage(page)
    const mostSeriousInjuryPage = new MostSeriousInjuryPage(page)
    const healedTheQuickestPage = new HealedTheQuickestPage(page)
    await openQuestionnaire('test_dynamic_radio_options_from_checkbox.json')

    await injurySustainedPage.head().click()
    await injurySustainedPage.body().click()
    await injurySustainedPage.submit().click()

    await mostSeriousInjuryPage.answerByIndex(0).click()
    await mostSeriousInjuryPage.submit().click()

    await expect(page).toHaveURL(new RegExp(healedTheQuickestPage.pageName))
    await expect(healedTheQuickestPage.answerLabelByIndex(0)).toHaveText('Head')
    await expect(healedTheQuickestPage.answerLabelByIndex(1)).toHaveText('Body')
    await expect(healedTheQuickestPage.answerLabelByIndex(2)).toHaveCount(0)
  })

  test('When dynamic radios are answered and submitted, Then summary displays all answers correctly', async ({ page, openQuestionnaire }) => {
    const injurySustainedPage = new InjurySustainedPage(page)
    const mostSeriousInjuryPage = new MostSeriousInjuryPage(page)
    const healedTheQuickestPage = new HealedTheQuickestPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire('test_dynamic_radio_options_from_checkbox.json')

    await injurySustainedPage.head().click()
    await injurySustainedPage.body().click()
    await injurySustainedPage.submit().click()

    await mostSeriousInjuryPage.answerByIndex(0).click()
    await mostSeriousInjuryPage.submit().click()

    await healedTheQuickestPage.answerByIndex(1).click()
    await healedTheQuickestPage.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    await expect(submitPage.injurySustainedAnswer().locator('li')).toHaveText(['Head', 'Body'])
    await expect(submitPage.mostSeriousInjuryAnswer()).toHaveText('Head')
    await expect(submitPage.healedTheQuickestAnswer()).toHaveText('Body')
  })

  test('When the checkbox dependency answer is edited, Then selected dependent dynamic radio answers are removed', async ({ page, openQuestionnaire }) => {
    const injurySustainedPage = new InjurySustainedPage(page)
    const mostSeriousInjuryPage = new MostSeriousInjuryPage(page)
    const healedTheQuickestPage = new HealedTheQuickestPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire('test_dynamic_radio_options_from_checkbox.json')

    await injurySustainedPage.head().click()
    await injurySustainedPage.body().click()
    await injurySustainedPage.submit().click()

    await mostSeriousInjuryPage.answerByIndex(0).click()
    await mostSeriousInjuryPage.submit().click()

    await healedTheQuickestPage.answerByIndex(1).click()
    await healedTheQuickestPage.submit().click()

    await submitPage.injurySustainedAnswerEdit().click()
    await injurySustainedPage.arms().click()
    await injurySustainedPage.submit().click()

    await expect(mostSeriousInjuryPage.answerByIndex(0)).not.toBeChecked()
    await expect(mostSeriousInjuryPage.answerByIndex(1)).not.toBeChecked()
  })
})
