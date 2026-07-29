import { createOpenQuestionnaire, test, expect } from '../../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../../fixtures/test'
import TotalTurnoverPage from '../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/total-turnover-block.page'
import TotalEmployeesPage from '../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/total-employees-block.page'
import CompanySectionSummary from '../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/company-overview-section-summary.page'
import TurnoverBreakdownPage from '../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/turnover-breakdown-block.page'
import EmployeesBreakdownPage from '../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/employees-breakdown-block.page'
import BreakdownSectionSummary from '../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/breakdown-section-summary.page'
import HubPage from '../../../../base_pages/hub.page'
import ThankYouPage from '../../../../base_pages/thank-you.page'
import { verifyUrlContains } from '../../../../helpers'

const companyOverviewSectionID = 'company-overview-section'
const breakdownSectionId = 'breakdown-section'

const answerAndSubmitTurnoverBreakdownQuestion = async (page: Page, breakdown1: string, breakdown2: string, breakdown3: string): Promise<void> => {
  const turnoverBreakdownPage = new TurnoverBreakdownPage(page)
  await turnoverBreakdownPage.turnoverBreakdown1().fill(breakdown1)
  await turnoverBreakdownPage.turnoverBreakdown2().fill(breakdown2)
  await turnoverBreakdownPage.turnoverBreakdown3().fill(breakdown3)
  await turnoverBreakdownPage.submit().click()
}

const answerAndSubmitEmployeeBreakdownQuestion = async (page: Page, breakdown1: string, breakdown2: string): Promise<void> => {
  const employeesBreakdownPage = new EmployeesBreakdownPage(page)
  await employeesBreakdownPage.employeesBreakdown1().fill(breakdown1)
  await employeesBreakdownPage.employeesBreakdown2().fill(breakdown2)
  await employeesBreakdownPage.submit().click()
}

const answerAndSubmitTotalTurnoverQuestion = async (page: Page, total: string): Promise<void> => {
  const totalTurnoverPage = new TotalTurnoverPage(page)
  await totalTurnoverPage.totalTurnover().fill(total)
  await totalTurnoverPage.submit().click()
}

const answerAndSubmitTotalEmployeesQuestion = async (page: Page, total: string): Promise<void> => {
  const totalEmployeesPage = new TotalEmployeesPage(page)
  await totalEmployeesPage.totalEmployees().fill(total)
  await totalEmployeesPage.submit().click()
}

test.describe('Feature: Validation - Sum of grouped answers to equal total (Total in separate section)', () => {
  test.describe.configure({ mode: 'serial' })

  test.describe('Given I start a grouped answer validation with dependent sections and complete the total turnover and total employees questions', () => {
    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll(async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      const companySectionSummary = new CompanySectionSummary(page)
      const hubPage = new HubPage(page)
      await openQuestionnaire('test_validation_sum_against_total_hub_with_dependent_section.json')
      await answerAndSubmitTotalTurnoverQuestion(page, '1000')
      await answerAndSubmitTotalEmployeesQuestion(page, '10')
      await companySectionSummary.submit().click()

      await expect(hubPage.summaryRowState(companyOverviewSectionID)).toHaveText('Completed')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test("When I am on the hub, Then the breakdown section should be marked as 'Not Started'", async () => {
      const hubPage = new HubPage(page)
      await expect(hubPage.summaryRowState(breakdownSectionId)).toHaveText('Not started')
    })

    test('When I start the breakdown section and enter an answer that is not equal to the total for the turnover question, Then I should see a validation error', async () => {
      const hubPage = new HubPage(page)
      const turnoverBreakdownPage = new TurnoverBreakdownPage(page)
      await hubPage.submit().click()
      await answerAndSubmitTurnoverBreakdownQuestion(page, '1000', '250', '250')

      await expect(turnoverBreakdownPage.errorNumber(1)).toHaveText('Enter answers that add up to £1,000.00')
    })

    test(
      'When I start the breakdown section and enter answers that are equal the total, ' +
        "Then I should be able to get to the section summary and the breakdown section should be marked as 'Completed'",
      async () => {
        const breakdownSectionSummary = new BreakdownSectionSummary(page)
        const hubPage = new HubPage(page)
        await answerAndSubmitTurnoverBreakdownQuestion(page, '500', '250', '250')
        await answerAndSubmitEmployeeBreakdownQuestion(page, '5', '5')

        await verifyUrlContains(page, breakdownSectionSummary.pageName)
        await breakdownSectionSummary.submit().click()

        await expect(hubPage.summaryRowState(breakdownSectionId)).toHaveText('Completed')
      }
    )
  })

  test.describe('Given I start a grouped answer validation with dependent sections and complete the overview and breakdown sections', () => {
    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll(async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      const breakdownSectionSummary = new BreakdownSectionSummary(page)
      const companySectionSummary = new CompanySectionSummary(page)
      const hubPage = new HubPage(page)
      await openQuestionnaire('test_validation_sum_against_total_hub_with_dependent_section.json')

      // Complete overview section
      await answerAndSubmitTotalTurnoverQuestion(page, '1000')
      await answerAndSubmitTotalEmployeesQuestion(page, '10')
      await companySectionSummary.submit().click()

      // Complete breakdown section
      await hubPage.submit().click()
      await answerAndSubmitTurnoverBreakdownQuestion(page, '500', '250', '250')
      await answerAndSubmitEmployeeBreakdownQuestion(page, '5', '5')
      await breakdownSectionSummary.submit().click()

      await expect(hubPage.summaryRowState(breakdownSectionId)).toHaveText('Completed')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test("When I change my answer for the total turnover question, Then the breakdown section should be marked as 'Partially completed'", async () => {
      const companySectionSummary = new CompanySectionSummary(page)
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink(companyOverviewSectionID).click()
      await companySectionSummary.totalTurnoverAnswerEdit().click()

      await answerAndSubmitTotalTurnoverQuestion(page, '1500')
      await companySectionSummary.submit().click()
      await expect(hubPage.summaryRowState(breakdownSectionId)).toHaveText('Partially completed')
    })

    test(
      "When I click 'Continue with section' on the breakdown section, " +
        'Then I should be taken to the turnover breakdown question and my previous answers should be prefilled',
      async () => {
        const hubPage = new HubPage(page)
        const turnoverBreakdownPage = new TurnoverBreakdownPage(page)
        await hubPage.summaryRowLink(breakdownSectionId).click()

        await expect(turnoverBreakdownPage.turnoverBreakdown1()).toHaveValue('500.00')
        await expect(turnoverBreakdownPage.turnoverBreakdown2()).toHaveValue('250.00')
        await expect(turnoverBreakdownPage.turnoverBreakdown3()).toHaveValue('250.00')
      }
    )

    test('When I submit the turnover breakdown question with no changes, Then I should see a validation error', async () => {
      const turnoverBreakdownPage = new TurnoverBreakdownPage(page)
      await turnoverBreakdownPage.submit().click()

      await expect(turnoverBreakdownPage.errorNumber(1)).toHaveText('Enter answers that add up to £1,500.00')
    })

    test(
      'When I update my answers to equal the new total turnover, ' +
        "Then I should be able to get to the section summary and the breakdown section should be marked as 'Completed'",
      async () => {
        const breakdownSectionSummary = new BreakdownSectionSummary(page)
        const hubPage = new HubPage(page)
        await answerAndSubmitTurnoverBreakdownQuestion(page, '500', '500', '500')

        await verifyUrlContains(page, breakdownSectionSummary.pageName)
        await breakdownSectionSummary.submit().click()
        await expect(hubPage.summaryRowState(breakdownSectionId)).toHaveText('Completed')
      }
    )

    test('When I submit the questionnaire, Then I should see the thank you page', async () => {
      const hubPage = new HubPage(page)
      const thankYouPage = new ThankYouPage(page)
      await hubPage.submit().scrollIntoViewIfNeeded()
      await hubPage.submit().click()
      await verifyUrlContains(page, thankYouPage.pageName)
    })
  })
})
