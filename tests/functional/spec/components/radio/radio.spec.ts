import { test, expect } from '../../../fixtures/test'

import RadioMandatoryPage from '../../../generated_pages/radio_mandatory/radio-mandatory.page'
import RadioMandatorySummary from '../../../generated_pages/radio_mandatory/submit.page'

import RadioMandatoryOptionalDetailAnswerPage from '../../../generated_pages/radio_mandatory_with_detail_answer_optional/radio-mandatory.page'
import RadioMandatoryOptionDetailAnswerSummary from '../../../generated_pages/radio_mandatory_with_detail_answer_optional/submit.page'

import RadioMandatoryDetailAnswerOverriddenPage from '../../../generated_pages/radio_mandatory_with_detail_answer_mandatory_with_overridden_error/radio-mandatory.page'

import RadioMandatoryOverriddenPage from '../../../generated_pages/radio_mandatory_with_overridden_error/radio-mandatory.page'

import RadioNonMandatoryPage from '../../../generated_pages/radio_optional/radio-non-mandatory.page'
import RadioNonMandatorySummary from '../../../generated_pages/radio_optional/submit.page'

import RadioNonMandatoryDetailAnswerOverriddenPage from '../../../generated_pages/radio_optional_with_detail_answer_mandatory_with_overridden_error/radio-non-mandatory.page'

import RadioNonMandatoryDetailAnswerPage from '../../../generated_pages/radio_optional_with_detail_answer_mandatory/radio-non-mandatory.page'
import RadioNonMandatoryDetailAnswerSummary from '../../../generated_pages/radio_optional_with_detail_answer_mandatory/submit.page'

test.describe('Component: Radio', () => {
  test.describe('Given I start a Mandatory Radio survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_radio_mandatory.json')
    })

    test('When I have selected a radio option that contains an escaped character, Then the selected option should be displayed in the summary', async ({
      page
    }) => {
      const radioMandatoryPage = new RadioMandatoryPage(page)
      const radioMandatorySummary = new RadioMandatorySummary(page)

      await radioMandatoryPage.teaCoffee().click()
      await radioMandatoryPage.submit().click()
      await expect(page).toHaveURL(new RegExp(radioMandatorySummary.pageName))
      await expect(radioMandatorySummary.radioMandatoryAnswer()).toHaveText('Tea & Coffee')
    })
  })

  test.describe('Given I start a Mandatory Radio survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_radio_mandatory.json')
    })

    test('When I have selected a radio option, Then the selected option should be displayed in the summary', async ({ page }) => {
      const radioMandatoryPage = new RadioMandatoryPage(page)
      const radioMandatorySummary = new RadioMandatorySummary(page)

      await radioMandatoryPage.coffee().click()
      await radioMandatoryPage.submit().click()
      await expect(page).toHaveURL(new RegExp(radioMandatorySummary.pageName))
      await expect(radioMandatorySummary.radioMandatoryAnswer()).toHaveText('Coffee')
    })
  })

  test.describe('Given I start a Mandatory Radio survey  ', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_radio_mandatory.json')
    })

    test('When I have submitted the page without any option, Then the question text is hidden in the error message using a span element', async ({ page }) => {
      const radioMandatoryOverriddenPage = new RadioMandatoryOverriddenPage(page)

      await radioMandatoryOverriddenPage.submit().click()

      await expect(radioMandatoryOverriddenPage.errorNumber(1).locator('span')).toHaveClass(/ons-u-vh/)
      await expect(radioMandatoryOverriddenPage.errorNumber(1).locator('span')).toContainText('What do you prefer for breakfast?')
    })
  })

  test.describe('Given I start a Mandatory Radio DetailAnswer survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_radio_mandatory_with_detail_answer_mandatory.json')
    })

    test('When I have selected a other text field, Then the selected option should be displayed in the summary', async ({ page }) => {
      const radioMandatoryOptionalDetailAnswerPage = new RadioMandatoryOptionalDetailAnswerPage(page)
      const radioMandatoryOptionDetailAnswerSummary = new RadioMandatoryOptionDetailAnswerSummary(page)

      await radioMandatoryOptionalDetailAnswerPage.other().click()
      await radioMandatoryOptionalDetailAnswerPage.otherDetail().fill('Hello World')
      await radioMandatoryOptionalDetailAnswerPage.submit().click()
      await expect(page).toHaveURL(new RegExp(radioMandatoryOptionDetailAnswerSummary.pageName))
      await expect(radioMandatoryOptionDetailAnswerSummary.radioMandatoryAnswer()).toContainText('Hello World')
    })
  })

  test.describe('Given I start a Mandatory Radio DetailAnswer Overridden Error survey ', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_radio_mandatory_with_detail_answer_mandatory_with_overridden_error.json')
    })

    test('When I submit without any data in the other text field it should Then throw an overridden error', async ({ page }) => {
      const radioMandatoryDetailAnswerOverriddenPage = new RadioMandatoryDetailAnswerOverriddenPage(page)

      await radioMandatoryDetailAnswerOverriddenPage.other().click()
      await radioMandatoryDetailAnswerOverriddenPage.submit().click()
      await expect(radioMandatoryDetailAnswerOverriddenPage.errorNumber(1)).toHaveText('Test error message is overridden')
    })
  })

  test.describe('Given I start a Mandatory Radio DetailAnswer survey ', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_radio_mandatory_with_detail_answer_optional.json')
    })

    test('When I submit without any data in the other text field is selected, Then the selected option should be displayed in the summary', async ({
      page
    }) => {
      const radioMandatoryOptionalDetailAnswerPage = new RadioMandatoryOptionalDetailAnswerPage(page)
      const radioMandatoryOptionDetailAnswerSummary = new RadioMandatoryOptionDetailAnswerSummary(page)

      await radioMandatoryOptionalDetailAnswerPage.submit().click()
      await expect(page).toHaveURL(new RegExp(radioMandatoryOptionDetailAnswerSummary.pageName))
      await expect(radioMandatoryOptionDetailAnswerSummary.radioMandatoryAnswer()).toContainText('No answer provided')
    })
  })

  test.describe('Given I start a Mandatory Radio DetailAnswer Overridden error survey  ', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_radio_mandatory_with_overridden_error.json')
    })

    test('When I have submitted the page without any option, Then an overridden error is displayed', async ({ page }) => {
      const radioMandatoryOverriddenPage = new RadioMandatoryOverriddenPage(page)

      await radioMandatoryOverriddenPage.submit().click()
      await expect(radioMandatoryOverriddenPage.errorNumber(1)).toHaveText('Test error message is overridden')
    })
  })

  test.describe('Given I start a Optional survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_radio_optional.json')
    })

    test('When I have selected no option, Then the selected option should be displayed in the summary', async ({ page }) => {
      const radioNonMandatoryPage = new RadioNonMandatoryPage(page)
      const radioNonMandatorySummary = new RadioNonMandatorySummary(page)

      await radioNonMandatoryPage.submit().click()
      await expect(page).toHaveURL(new RegExp(radioNonMandatorySummary.pageName))
      await expect(radioNonMandatorySummary.radioNonMandatoryAnswer()).toHaveText('No answer provided')
    })
  })

  test.describe('Given I start a Optional DetailAnswer Overridden error survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_radio_optional_with_detail_answer_mandatory_with_overridden_error.json')
    })

    test('When I have submitted an other option with an empty text field, Then an overridden error is displayed', async ({ page }) => {
      const radioNonMandatoryDetailAnswerOverriddenPage = new RadioNonMandatoryDetailAnswerOverriddenPage(page)

      await radioNonMandatoryDetailAnswerOverriddenPage.other().click()
      await radioNonMandatoryDetailAnswerOverriddenPage.submit().click()
      await expect(radioNonMandatoryDetailAnswerOverriddenPage.errorNumber(1)).toHaveText('Test error message is overridden')
    })
  })

  test.describe('Given I Start a Optional Mandatory DetailAnswer survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_radio_optional_with_detail_answer_mandatory.json')
    })

    test('When I submit data in the other text field it should be persisted and Then displayed on the summary', async ({ page }) => {
      const radioNonMandatoryDetailAnswerPage = new RadioNonMandatoryDetailAnswerPage(page)
      const radioNonMandatoryDetailAnswerSummary = new RadioNonMandatoryDetailAnswerSummary(page)

      await radioNonMandatoryDetailAnswerPage.other().click()
      await radioNonMandatoryDetailAnswerPage.otherDetail().fill('Hello World')
      await radioNonMandatoryDetailAnswerPage.submit().click()
      await expect(page).toHaveURL(new RegExp(radioNonMandatoryDetailAnswerSummary.pageName))
      await expect(radioNonMandatoryDetailAnswerSummary.radioNonMandatoryAnswer()).toContainText('Hello World')
    })
  })
})
