import { test, expect } from '../../../fixtures/test'
import type { Page } from '../../../fixtures/test'
import ReferenceDatePage from '../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/reference-date.page'
import DynamicCheckboxPage from '../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-checkbox.page'
import DynamicRadioPage from '../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-radio.page'
import DynamicDropdownPage from '../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-dropdown.page'
import DynamicMutuallyExclusivePage from '../../../generated_pages/dynamic_answer_options_function_driven_with_static_options_mandatory/dynamic-mutually-exclusive.page'

test.describe('Feature: Dynamically generated mandatory answer options driven by a function with static options', () => {
  test.beforeEach('Open questionnaire and set reference date', async ({ page, openQuestionnaire }) => {
    await openQuestionnaireAndSetReferenceDate(page, openQuestionnaire)
  })

  test('When Checkbox is not answered and submitted, Then error header and question error panel are shown', async ({ page }) => {
    const dynamicCheckboxPage = new DynamicCheckboxPage(page)
    await dynamicCheckboxPage.submit().click()
    await expect(dynamicCheckboxPage.errorHeader()).toHaveText('There is a problem with your answer')
    await expect(dynamicCheckboxPage.answerErrorItem()).toContainText('Select at least one answer')
    await expect(dynamicCheckboxPage.questionErrorPanel()).toBeVisible()
  })

  test('When Radio is not answered and submitted, Then error header and question error panel are shown', async ({ page }) => {
    const dynamicCheckboxPage = new DynamicCheckboxPage(page)
    const dynamicRadioPage = new DynamicRadioPage(page)
    await dynamicCheckboxPage.answerByIndex(0).click()
    await dynamicCheckboxPage.submit().click()

    await dynamicRadioPage.submit().click()
    await expect(dynamicRadioPage.errorHeader()).toHaveText('There is a problem with your answer')
    await expect(dynamicRadioPage.answerErrorItem()).toContainText('Select an answer')
    await expect(dynamicRadioPage.questionErrorPanel()).toBeVisible()
  })

  test('When Dropdown is not answered and submitted, Then error header and question error panel are shown', async ({ page }) => {
    const dynamicCheckboxPage = new DynamicCheckboxPage(page)
    const dynamicRadioPage = new DynamicRadioPage(page)
    const dynamicDropdownPage = new DynamicDropdownPage(page)
    await dynamicCheckboxPage.answerByIndex(0).click()
    await dynamicCheckboxPage.submit().click()
    await dynamicRadioPage.answerByIndex(0).click()
    await dynamicRadioPage.submit().click()

    await dynamicDropdownPage.submit().click()
    await expect(dynamicDropdownPage.errorHeader()).toHaveText('There is a problem with your answer')
    await expect(dynamicDropdownPage.answerErrorItem()).toHaveText('Select an answer')
    await expect(dynamicDropdownPage.questionErrorPanel()).toBeVisible()
  })

  test('When Mutually Exclusive checkbox is not answered and submitted, Then error header and question error panel are shown', async ({ page }) => {
    const dynamicCheckboxPage = new DynamicCheckboxPage(page)
    const dynamicRadioPage = new DynamicRadioPage(page)
    const dynamicDropdownPage = new DynamicDropdownPage(page)
    const dynamicMutuallyExclusivePage = new DynamicMutuallyExclusivePage(page)
    await dynamicCheckboxPage.answerByIndex(0).click()
    await dynamicCheckboxPage.submit().click()
    await dynamicRadioPage.answerByIndex(0).click()
    await dynamicRadioPage.submit().click()
    await dynamicDropdownPage.answer().selectOption('2021-01-02')
    await dynamicDropdownPage.submit().click()

    await dynamicMutuallyExclusivePage.submit().click()
    await expect(dynamicMutuallyExclusivePage.errorHeader()).toHaveText('There is a problem with your answer')
    await expect(dynamicMutuallyExclusivePage.errorNumber(1)).toContainText('Select at least one answer')
    await expect(dynamicMutuallyExclusivePage.questionErrorPanel()).toBeVisible()
  })
})

async function openQuestionnaireAndSetReferenceDate (page: Page, openQuestionnaire: (schema: string) => Promise<void>): Promise<void> {
  const referenceDatePage = new ReferenceDatePage(page)
  await openQuestionnaire('test_dynamic_answer_options_function_driven_with_static_options_mandatory.json')
  await referenceDatePage.day().fill('1')
  await referenceDatePage.month().fill('1')
  await referenceDatePage.year().fill('2021')
  await referenceDatePage.submit().click()
}
