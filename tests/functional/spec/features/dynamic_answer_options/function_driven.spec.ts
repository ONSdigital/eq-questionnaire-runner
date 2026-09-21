import { test, expect } from '../../../fixtures/test'
import type { Page } from '../../../fixtures/test'
import ReferenceDatePage from '../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/reference-date.page'
import DynamicCheckboxPage from '../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/dynamic-checkbox.page'
import DynamicRadioPage from '../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/dynamic-radio.page'
import DynamicDropdownPage from '../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/dynamic-dropdown.page'
import DynamicMutuallyExclusivePage from '../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/dynamic-mutually-exclusive.page'
import SubmitPage from '../../../generated_pages/dynamic_answer_options_function_driven_with_static_options/submit.page'

const dropdownOptionValues = ['2020-12-28', '2020-12-29', '2020-12-30', '2020-12-31', '2021-01-01', '2021-01-02', '2021-01-03']
const dropdownOptionValuesWithStaticOption = [...dropdownOptionValues, 'I did not work']

const testCases = [
  {
    schemaName: 'test_dynamic_answer_options_function_driven_with_static_options.json',
    answerOptionCount: 8,
    optionValues: dropdownOptionValuesWithStaticOption
  },
  {
    schemaName: 'test_dynamic_answer_options_function_driven.json',
    answerOptionCount: 7,
    optionValues: dropdownOptionValues
  }
]

testCases.forEach(({ schemaName, answerOptionCount, optionValues }) => {
  test.describe(`Feature: Dynamically generated answer options driven by a function (${schemaName})`, () => {
    test.beforeEach('Open questionnaire', async ({ page, openQuestionnaire }) => {
      await openQuestionnaireAndSetReferenceDate(page, openQuestionnaire, schemaName)
    })

    test('When I click a checkbox option, then the checkbox should be selected', async ({ page }) => {
      const dynamicCheckboxPage = new DynamicCheckboxPage(page)
      for (let i = 0; i < answerOptionCount; i++) {
        await dynamicCheckboxPage.answerByIndex(i).click()
        await expect(dynamicCheckboxPage.answerByIndex(i)).toBeChecked()
      }
    })

    test('When I click a selected checkbox option, then it should be deselected', async ({ page }) => {
      const dynamicCheckboxPage = new DynamicCheckboxPage(page)
      for (let i = 0; i < answerOptionCount; i++) {
        await dynamicCheckboxPage.answerByIndex(i).click()
      }

      for (let i = 0; i < answerOptionCount; i++) {
        await dynamicCheckboxPage.answerByIndex(i).click()
        await expect(dynamicCheckboxPage.answerByIndex(i)).not.toBeChecked()
      }
    })

    test('When I submit the checkbox page, then I should be taken to the radio page', async ({ page }) => {
      const dynamicCheckboxPage = new DynamicCheckboxPage(page)
      const dynamicRadioPage = new DynamicRadioPage(page)
      await dynamicCheckboxPage.submit().click()
      await expect(page).toHaveURL(new RegExp(dynamicRadioPage.pageName))
    })

    test('When I click a radio option, then the radio should be selected', async ({ page }) => {
      const dynamicCheckboxPage = new DynamicCheckboxPage(page)
      const dynamicRadioPage = new DynamicRadioPage(page)
      await dynamicCheckboxPage.submit().click()

      for (let i = 0; i < answerOptionCount; i++) {
        await dynamicRadioPage.answerByIndex(i).click()
        await expect(dynamicRadioPage.answerByIndex(i)).toBeChecked()
      }
    })

    test('When I submit the radio page, then I should be taken to the dropdown page', async ({ page }) => {
      const dynamicCheckboxPage = new DynamicCheckboxPage(page)
      const dynamicRadioPage = new DynamicRadioPage(page)
      const dynamicDropdownPage = new DynamicDropdownPage(page)
      await dynamicCheckboxPage.submit().click()
      await dynamicRadioPage.submit().click()
      await expect(page).toHaveURL(new RegExp(dynamicDropdownPage.pageName))
    })

    test('When I select a dropdown option, then the option should be selected', async ({ page }) => {
      const dynamicCheckboxPage = new DynamicCheckboxPage(page)
      const dynamicRadioPage = new DynamicRadioPage(page)
      const dynamicDropdownPage = new DynamicDropdownPage(page)
      await dynamicCheckboxPage.submit().click()
      await dynamicRadioPage.submit().click()

      for (const value of optionValues) {
        await dynamicDropdownPage.answer().selectOption(value)
        await expect(dynamicDropdownPage.answer()).toHaveValue(value)
      }
    })

    test('When I submit the dropdown page, then I should be taken to the mutually exclusive page', async ({ page }) => {
      const dynamicCheckboxPage = new DynamicCheckboxPage(page)
      const dynamicRadioPage = new DynamicRadioPage(page)
      const dynamicDropdownPage = new DynamicDropdownPage(page)
      const dynamicMutuallyExclusivePage = new DynamicMutuallyExclusivePage(page)
      await dynamicCheckboxPage.submit().click()
      await dynamicRadioPage.submit().click()
      await dynamicDropdownPage.submit().click()
      await expect(page).toHaveURL(new RegExp(dynamicMutuallyExclusivePage.pageName))
    })

    test('When I click a dynamic mutually exclusive checkbox option, then it should be selected', async ({ page }) => {
      const dynamicCheckboxPage = new DynamicCheckboxPage(page)
      const dynamicRadioPage = new DynamicRadioPage(page)
      const dynamicDropdownPage = new DynamicDropdownPage(page)
      const dynamicMutuallyExclusivePage = new DynamicMutuallyExclusivePage(page)
      await dynamicCheckboxPage.submit().click()
      await dynamicRadioPage.submit().click()
      await dynamicDropdownPage.submit().click()

      for (let i = 0; i < answerOptionCount; i++) {
        await dynamicMutuallyExclusivePage.answerByIndex(i).click()
        await expect(dynamicMutuallyExclusivePage.answerByIndex(i)).toBeChecked()
      }
    })

    test('When I click a selected dynamic mutually exclusive option, then it should be deselected', async ({ page }) => {
      const dynamicCheckboxPage = new DynamicCheckboxPage(page)
      const dynamicRadioPage = new DynamicRadioPage(page)
      const dynamicDropdownPage = new DynamicDropdownPage(page)
      const dynamicMutuallyExclusivePage = new DynamicMutuallyExclusivePage(page)
      await dynamicCheckboxPage.submit().click()
      await dynamicRadioPage.submit().click()
      await dynamicDropdownPage.submit().click()

      for (let i = 0; i < answerOptionCount; i++) {
        await dynamicMutuallyExclusivePage.answerByIndex(i).click()
      }

      for (let i = 0; i < answerOptionCount; i++) {
        await dynamicMutuallyExclusivePage.answerByIndex(i).click()
        await expect(dynamicMutuallyExclusivePage.answerByIndex(i)).not.toBeChecked()
      }
    })

    test('When I click the static mutually exclusive option, then it should be selected', async ({ page }) => {
      const dynamicCheckboxPage = new DynamicCheckboxPage(page)
      const dynamicRadioPage = new DynamicRadioPage(page)
      const dynamicDropdownPage = new DynamicDropdownPage(page)
      const dynamicMutuallyExclusivePage = new DynamicMutuallyExclusivePage(page)
      await dynamicCheckboxPage.submit().click()
      await dynamicRadioPage.submit().click()
      await dynamicDropdownPage.submit().click()

      await dynamicMutuallyExclusivePage.staticIDidNotWork().click()
      await expect(dynamicMutuallyExclusivePage.staticIDidNotWork()).toBeChecked()
    })

    test('When I click the selected static mutually exclusive option, then it should be deselected', async ({ page }) => {
      const dynamicCheckboxPage = new DynamicCheckboxPage(page)
      const dynamicRadioPage = new DynamicRadioPage(page)
      const dynamicDropdownPage = new DynamicDropdownPage(page)
      const dynamicMutuallyExclusivePage = new DynamicMutuallyExclusivePage(page)
      await dynamicCheckboxPage.submit().click()
      await dynamicRadioPage.submit().click()
      await dynamicDropdownPage.submit().click()

      await dynamicMutuallyExclusivePage.staticIDidNotWork().click()
      await dynamicMutuallyExclusivePage.staticIDidNotWork().click()
      await expect(dynamicMutuallyExclusivePage.staticIDidNotWork()).not.toBeChecked()
    })

    test('Given no answers are provided, Then summary shows no answer provided for each dynamic question', async ({ page }) => {
      const dynamicCheckboxPage = new DynamicCheckboxPage(page)
      const dynamicRadioPage = new DynamicRadioPage(page)
      const dynamicDropdownPage = new DynamicDropdownPage(page)
      const dynamicMutuallyExclusivePage = new DynamicMutuallyExclusivePage(page)
      const submitPage = new SubmitPage(page)

      await dynamicCheckboxPage.submit().click()
      await dynamicRadioPage.submit().click()
      await dynamicDropdownPage.submit().click()
      await dynamicMutuallyExclusivePage.submit().click()

      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
      await expect(submitPage.dynamicCheckboxAnswer()).toHaveText('No answer provided')
      await expect(submitPage.dynamicRadioAnswer()).toHaveText('No answer provided')
      await expect(submitPage.dynamicDropdownAnswer()).toHaveText('No answer provided')
      await expect(submitPage.dynamicMutuallyExclusiveDynamicAnswer()).toHaveText('No answer provided')
    })

    test('Given dynamic options are selected, Then selected answers are shown on summary', async ({ page }) => {
      const dynamicCheckboxPage = new DynamicCheckboxPage(page)
      const dynamicRadioPage = new DynamicRadioPage(page)
      const dynamicDropdownPage = new DynamicDropdownPage(page)
      const dynamicMutuallyExclusivePage = new DynamicMutuallyExclusivePage(page)
      const submitPage = new SubmitPage(page)

      await dynamicCheckboxPage.answerByIndex(2).click()
      await dynamicCheckboxPage.answerByIndex(3).click()
      await dynamicCheckboxPage.submit().click()

      await dynamicRadioPage.answerByIndex(1).click()
      await dynamicRadioPage.submit().click()

      await dynamicDropdownPage.answer().selectOption('2021-01-02')
      await dynamicDropdownPage.submit().click()

      await dynamicMutuallyExclusivePage.answerByIndex(0).click()
      await dynamicMutuallyExclusivePage.answerByIndex(6).click()
      await dynamicMutuallyExclusivePage.submit().click()

      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
      await expect(submitPage.dynamicCheckboxAnswer().locator('li')).toHaveText(['Wednesday 30 December 2020', 'Thursday 31 December 2020'])
      await expect(submitPage.dynamicRadioAnswer()).toHaveText('Tuesday 29 December 2020')
      await expect(submitPage.dynamicDropdownAnswer()).toHaveText('Saturday 2 January 2021')
      await expect(submitPage.dynamicMutuallyExclusiveDynamicAnswer().locator('li')).toHaveText(['Monday 28 December 2020', 'Sunday 3 January 2021'])
    })
  })
})

test.describe('Feature: Dynamically generated answer options driven by a function with static options', () => {
  test('Given static options are selected throughout, Then summary shows those static answers', async ({ page, openQuestionnaire }) => {
    const dynamicCheckboxPage = new DynamicCheckboxPage(page)
    const dynamicRadioPage = new DynamicRadioPage(page)
    const dynamicDropdownPage = new DynamicDropdownPage(page)
    const dynamicMutuallyExclusivePage = new DynamicMutuallyExclusivePage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaireAndSetReferenceDate(page, openQuestionnaire, 'test_dynamic_answer_options_function_driven_with_static_options.json')

    await dynamicCheckboxPage.answerByIndex(7).click()
    await dynamicCheckboxPage.submit().click()

    await dynamicRadioPage.answerByIndex(7).click()
    await dynamicRadioPage.submit().click()

    await dynamicDropdownPage.answer().selectOption('I did not work')
    await dynamicDropdownPage.submit().click()

    await dynamicMutuallyExclusivePage.answerByIndex(7).click()
    await dynamicMutuallyExclusivePage.submit().click()
    await expect(submitPage.dynamicMutuallyExclusiveDynamicAnswer()).toHaveText('None of the above')

    await submitPage.previous().click()
    await dynamicMutuallyExclusivePage.staticIDidNotWork().click()
    await dynamicMutuallyExclusivePage.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    await expect(submitPage.dynamicCheckboxAnswer()).toHaveText('I did not work')
    await expect(submitPage.dynamicRadioAnswer()).toHaveText('I did not work')
    await expect(submitPage.dynamicDropdownAnswer()).toHaveText('I did not work')
    await expect(submitPage.dynamicMutuallyExclusiveStaticAnswer()).toHaveText('I did not work')
  })

  test('Given answers are selected, When the reference date is edited, Then dependent answers are cleared', async ({ page, openQuestionnaire }) => {
    const referenceDatePage = new ReferenceDatePage(page)
    const dynamicCheckboxPage = new DynamicCheckboxPage(page)
    const dynamicRadioPage = new DynamicRadioPage(page)
    const dynamicDropdownPage = new DynamicDropdownPage(page)
    const dynamicMutuallyExclusivePage = new DynamicMutuallyExclusivePage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaireAndSetReferenceDate(page, openQuestionnaire, 'test_dynamic_answer_options_function_driven_with_static_options.json')

    await dynamicCheckboxPage.answerByIndex(7).click()
    await dynamicCheckboxPage.submit().click()
    await dynamicRadioPage.answerByIndex(7).click()
    await dynamicRadioPage.submit().click()
    await dynamicDropdownPage.answer().selectOption('I did not work')
    await dynamicDropdownPage.submit().click()
    await dynamicMutuallyExclusivePage.staticIDidNotWork().click()
    await dynamicMutuallyExclusivePage.submit().click()

    await submitPage.referenceDateAnswerEdit().click()
    await referenceDatePage.day().fill('2')
    await referenceDatePage.submit().click()

    await expect(dynamicCheckboxPage.answerByIndex(7)).not.toBeChecked()

    await dynamicCheckboxPage.answerByIndex(7).click()
    await dynamicCheckboxPage.submit().click()

    await expect(dynamicRadioPage.answerByIndex(7)).not.toBeChecked()

    await dynamicRadioPage.answerByIndex(7).click()
    await dynamicRadioPage.submit().click()

    await expect(dynamicDropdownPage.answer()).toContainText('Select an answer')

    await dynamicDropdownPage.answer().selectOption('I did not work')
    await dynamicDropdownPage.submit().click()

    await expect(dynamicMutuallyExclusivePage.staticIDidNotWork()).toBeChecked()
    await dynamicMutuallyExclusivePage.submit().click()

    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
  })
})

async function openQuestionnaireAndSetReferenceDate (page: Page, openQuestionnaire: (schema: string) => Promise<void>, schemaName: string): Promise<void> {
  const referenceDatePage = new ReferenceDatePage(page)
  await openQuestionnaire(schemaName)
  await referenceDatePage.day().fill('1')
  await referenceDatePage.month().fill('1')
  await referenceDatePage.year().fill('2021')
  await referenceDatePage.submit().click()
}
