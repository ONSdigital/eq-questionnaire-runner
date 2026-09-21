import { test, expect } from '../../../fixtures/test'
import DefaultInstructionPage from '../../../generated_pages/checkbox_instruction/default-instruction-checkbox.page'
import NoInstructionPage from '../../../generated_pages/checkbox_instruction/no-instruction-checkbox.page'
import CustomInstructionPage from '../../../generated_pages/checkbox_instruction/custom-instruction-checkbox.page'

test.describe('Given the checkbox label variants questionnaire,', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_checkbox_instruction.json')
  })

  test('Given an instruction has not been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then the default instruction should be visible', async ({
    page
  }) => {
    await expect(page.locator('#main-content')).toContainText('Select all that apply')
  })

  test('Given an instruction has been set to null in the schema for a checkbox answer, When the checkbox answer is displayed, Then the instruction should not be visible', async ({
    page
  }) => {
    const defaultInstructionPage = new DefaultInstructionPage(page)

    await defaultInstructionPage.red().click()
    await defaultInstructionPage.submit().click()
    await expect(page.locator('#main-content')).not.toContainText('Select all that apply')
  })

  test('Given a custom instruction has been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then the custom instruction should be visible', async ({
    page
  }) => {
    const defaultInstructionPage = new DefaultInstructionPage(page)
    const noInstructionPage = new NoInstructionPage(page)

    await defaultInstructionPage.red().click()
    await defaultInstructionPage.submit().click()
    await noInstructionPage.rugby().click()
    await noInstructionPage.submit().click()
    await expect(page.locator('#main-content')).toContainText('Select your answer')
  })

  test('Given a label and custom instruction have been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then both the custom instruction and label should be visible', async ({
    page
  }) => {
    const customInstructionPage = new CustomInstructionPage(page)
    const defaultInstructionPage = new DefaultInstructionPage(page)
    const noInstructionPage = new NoInstructionPage(page)

    await defaultInstructionPage.red().click()
    await defaultInstructionPage.submit().click()
    await noInstructionPage.rugby().click()
    await noInstructionPage.submit().click()
    await customInstructionPage.monday().click()
    await customInstructionPage.submit().click()
    await expect(page.locator('#main-content')).toContainText('Days of the Week')
    await expect(page.locator('#main-content')).toContainText('Select your answer')
  })
})
