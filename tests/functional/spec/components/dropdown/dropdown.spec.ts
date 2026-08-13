import { test, expect } from '../../../fixtures/test'
import DropdownMandatoryPage from '../../../generated_pages/dropdown_mandatory/dropdown-mandatory.page'
import DropdownMandatorySummary from '../../../generated_pages/dropdown_mandatory/submit.page'
import DropdownMandatoryOverriddenPage from '../../../generated_pages/dropdown_mandatory_with_overridden_error/dropdown-mandatory-with-overridden-error.page'
import DropdownOptionalPage from '../../../generated_pages/dropdown_optional/dropdown-optional.page'
import DropdownOptionalSummary from '../../../generated_pages/dropdown_optional/submit.page'

test.describe('Component: Dropdown', () => {
  // Mandatory
  test.describe('Given I start a Mandatory Dropdown survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_dropdown_mandatory.json')
    })

    test('When I have selected a dropdown option, Then the selected option should be displayed in the summary', async ({ page }) => {
      const dropdownMandatoryPage = new DropdownMandatoryPage(page)
      const dropdownMandatorySummary = new DropdownMandatorySummary(page)
      await dropdownMandatoryPage.answer().selectOption('Rugby is better!')
      await dropdownMandatoryPage.submit().click()
      await expect(dropdownMandatorySummary.dropdownMandatoryAnswer()).toHaveText('Rugby is better!')
    })

    test('When I have not selected a dropdown option and click Continue, Then the default error message should be displayed', async ({ page }) => {
      const dropdownMandatoryPage = new DropdownMandatoryPage(page)
      await dropdownMandatoryPage.submit().click()
      await expect(dropdownMandatoryPage.errorNumber(1)).toHaveText('Select an answer')
    })

    test('When I have selected a dropdown option and I try to select a default (disabled) dropdown option, Then the already selected option should be displayed in summary', async ({
      page
    }) => {
      const dropdownMandatoryPage = new DropdownMandatoryPage(page)
      const dropdownMandatorySummary = new DropdownMandatorySummary(page)
      await dropdownMandatoryPage.answer().selectOption('Liverpool')
      await expect(dropdownMandatoryPage.answer().locator('option[value=""]')).toBeDisabled()
      await dropdownMandatoryPage.submit().click()
      await expect(dropdownMandatorySummary.dropdownMandatoryAnswer()).toHaveText('Liverpool')
    })

    test('When I click the dropdown label, Then the dropdown should be focused', async ({ page }) => {
      const dropdownMandatoryPage = new DropdownMandatoryPage(page)
      await dropdownMandatoryPage.answerLabel().click()
      await expect(dropdownMandatoryPage.answer()).toBeFocused()
    })

    test("When I'm on the summary page and I click Edit then Continue, Then the answer on the summary page should be unchanged", async ({ page }) => {
      const dropdownMandatoryPage = new DropdownMandatoryPage(page)
      const dropdownMandatorySummary = new DropdownMandatorySummary(page)
      await dropdownMandatoryPage.answer().selectOption('Rugby is better!')
      await dropdownMandatoryPage.submit().click()
      await expect(dropdownMandatorySummary.dropdownMandatoryAnswer()).toHaveText('Rugby is better!')
      await dropdownMandatorySummary.dropdownMandatoryAnswerEdit().click()
      await dropdownMandatoryPage.submit().click()
      await expect(dropdownMandatorySummary.dropdownMandatoryAnswer()).toHaveText('Rugby is better!')
    })

    test("When I'm on the summary page and I click Edit and change the answer, Then the newly selected answer should be displayed in the summary", async ({
      page
    }) => {
      const dropdownMandatoryPage = new DropdownMandatoryPage(page)
      const dropdownMandatorySummary = new DropdownMandatorySummary(page)
      await dropdownMandatoryPage.answer().selectOption('Rugby is better!')
      await dropdownMandatoryPage.submit().click()
      await expect(dropdownMandatorySummary.dropdownMandatoryAnswer()).toHaveText('Rugby is better!')
      await dropdownMandatorySummary.dropdownMandatoryAnswerEdit().click()
      await dropdownMandatoryPage.submit().click()
      await expect(dropdownMandatorySummary.dropdownMandatoryAnswer()).toHaveText('Rugby is better!')
      await dropdownMandatorySummary.dropdownMandatoryAnswerEdit().click()
      await dropdownMandatoryPage.answer().selectOption('Liverpool')
      await dropdownMandatoryPage.submit().click()
      await expect(dropdownMandatorySummary.dropdownMandatoryAnswer()).toHaveText('Liverpool')
    })
  })

  test.describe('Given I start a Mandatory With Overridden Error Dropdown survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_dropdown_mandatory_with_overridden_error.json')
    })

    test('When I have not selected a dropdown option and click Continue, Then the overridden error message should be displayed', async ({ page }) => {
      const dropdownMandatoryOverriddenPage = new DropdownMandatoryOverriddenPage(page)
      await dropdownMandatoryOverriddenPage.submit().click()
      await expect(dropdownMandatoryOverriddenPage.errorNumber(1)).toHaveText('Overridden test error message.')
    })
  })

  // Optional
  test.describe('Given I start a Optional Dropdown survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_dropdown_optional.json')
    })

    test('When I have not selected a dropdown option, Then the summary should display "No answer provided"', async ({ page }) => {
      const dropdownOptionalPage = new DropdownOptionalPage(page)
      const dropdownOptionalSummary = new DropdownOptionalSummary(page)
      await dropdownOptionalPage.submit().click()
      await expect(dropdownOptionalSummary.dropdownOptionalAnswer()).toHaveText('No answer provided')
    })

    test('When I have selected a dropdown option, Then the selected option should be displayed in the summary', async ({ page }) => {
      const dropdownOptionalPage = new DropdownOptionalPage(page)
      const dropdownOptionalSummary = new DropdownOptionalSummary(page)
      await dropdownOptionalPage.answer().selectOption('Rugby is better!')
      await dropdownOptionalPage.submit().click()
      await expect(dropdownOptionalSummary.dropdownOptionalAnswer()).toHaveText('Rugby is better!')
    })

    test('When I have selected a dropdown option and I reselect the default option (Select an answer), Then the summary should display "No answer provided"', async ({
      page
    }) => {
      const dropdownOptionalPage = new DropdownOptionalPage(page)
      const dropdownOptionalSummary = new DropdownOptionalSummary(page)
      await dropdownOptionalPage.answer().selectOption('Chelsea')
      await dropdownOptionalPage.submit().click()
      await expect(dropdownOptionalSummary.dropdownOptionalAnswer()).toHaveText('Chelsea')
      await dropdownOptionalSummary.dropdownOptionalAnswerEdit().click()
      await dropdownOptionalPage.answer().selectOption('')
      await dropdownOptionalPage.submit().click()
      await expect(dropdownOptionalSummary.dropdownOptionalAnswer()).toHaveText('No answer provided')
    })
  })
})
