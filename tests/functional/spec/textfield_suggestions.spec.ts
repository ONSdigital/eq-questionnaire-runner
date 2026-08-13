import { test, expect } from '../fixtures/test'
import SuggestionsPage from '../generated_pages/textfield_suggestions/country-block.page'
import MultipleSuggestionsPage from '../generated_pages/textfield_suggestions/multiple-country-block.page'
import SubmitPage from '../generated_pages/textfield_suggestions/submit.page'

test.describe('Suggestions', () => {
  test('Given I open a textfield with a suggestions url, When I have entered text, Then it will show suggestions', async ({ page, openQuestionnaire }) => {
    const suggestionsPage = new SuggestionsPage(page)
    await openQuestionnaire('test_textfield_suggestions.json')
    await suggestionsPage.country().fill('Uni')
    await expect(page.locator('#country-answer-listbox li').first()).toBeVisible()
  })
})

test.describe('Suggestions', () => {
  test('Given I open a textfield with a suggestions url that allows multiple suggestions, when I have entered text and picked suggestion from a list, then after typing more text it will show new suggestions', async ({
    page,
    openQuestionnaire
  }) => {
    const multipleSuggestionsPage = new MultipleSuggestionsPage(page)
    const submitPage = new SubmitPage(page)
    const suggestionsPage = new SuggestionsPage(page)
    await openQuestionnaire('test_textfield_suggestions.json')
    const suggestionsOption = page.locator('#multiple-country-answer-listbox__option--0')

    await suggestionsPage.country().fill('United States of America')
    await suggestionsPage.submit().click()
    await multipleSuggestionsPage.multipleCountry().click()
    // Browser needs to pause before typing starts to allow for the autosuggest Javascript to initialise
    await page.waitForTimeout(500)
    await page.keyboard.type('Ita')
    await suggestionsOption.click()
    await multipleSuggestionsPage.multipleCountry().click()
    // Browser needs to pause before typing starts to allow for the autosuggest Javascript to initialise
    await page.waitForTimeout(500)
    await page.keyboard.type(' United')
    await expect(page.locator('.ons-js-autosuggest-listbox li')).not.toHaveCount(0)
    await suggestionsOption.click()
    await multipleSuggestionsPage.submit().click()
    await expect(page).toHaveURL(new RegExp(submitPage.url()))
  })
})
