import { createOpenQuestionnaire, test, expect } from '../../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../../fixtures/test'
import ListCollectorPage from '../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/list-collector.page'
import ListCollectorAddPage from '../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/list-collector-add.page'
import ListCollectorSummaryPage from '../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/householders-section-summary.page'
import TotalSpendingPage from '../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/total-spending-block.page'
import EntertainmentSpendingPage from '../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/entertainment-spending-block.page'
import HouseholdOverviewSectionSummary from '../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/household-overview-section-summary.page'
import BreakdownDrivingPage from '../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/breakdown-driving-block.page'
import SpendingBreakdownPage from '../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/spending-breakdown-block.page'
import EntertainmentBreakdownPage from '../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/second-spending-breakdown-block.page'
import BreakdownSectionSummary from '../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/breakdown-section-summary.page'
import HubPage from '../../../../base_pages/hub.page'
import ThankYouPage from '../../../../base_pages/thank-you.page'
import { verifyUrlContains } from '../../../../helpers'

const householderSectionId = 'householders-section'
const householdOverviewSectionId = 'household-overview-section'
const repeatingSectionId = (repeatIndex: number): string => {
  return `breakdown-section-${repeatIndex}`
}

const addPersonToHousehold = async (page: Page, firstName: string, lastName: string): Promise<void> => {
  const listCollectorPage = new ListCollectorPage(page)
  const listCollectorAddPage = new ListCollectorAddPage(page)
  await listCollectorPage.yes().click()
  await listCollectorPage.submit().click()
  await listCollectorAddPage.firstName().fill(firstName)
  await listCollectorAddPage.lastName().fill(lastName)
  await listCollectorAddPage.submit().click()
}

const answerAndSubmitTotalSpendingQuestion = async (page: Page, total: string): Promise<void> => {
  const totalSpendingPage = new TotalSpendingPage(page)
  await totalSpendingPage.totalSpending().fill(total)
  await totalSpendingPage.submit().click()
}

const answerAndSubmitEntertainmentSpendingQuestion = async (page: Page, total: string): Promise<void> => {
  const entertainmentSpendingPage = new EntertainmentSpendingPage(page)
  await entertainmentSpendingPage.entertainmentSpending().fill(total)
  await entertainmentSpendingPage.submit().click()
}

const answerAndSubmitSpendingBreakdownQuestion = async (page: Page, breakdown1: string, breakdown2: string, breakdown3: string): Promise<void> => {
  const spendingBreakdownPage = new SpendingBreakdownPage(page)
  await spendingBreakdownPage.spendingBreakdown1().fill(breakdown1)
  await spendingBreakdownPage.spendingBreakdown2().fill(breakdown2)
  await spendingBreakdownPage.spendingBreakdown3().fill(breakdown3)
  await spendingBreakdownPage.submit().click()
}

const assertSpendingBreakdownAnswer = async (page: Page, breakdown1: string, breakdown2: string, breakdown3: string): Promise<void> => {
  const spendingBreakdownPage = new SpendingBreakdownPage(page)
  await expect(spendingBreakdownPage.spendingBreakdown1()).toHaveValue(breakdown1)
  await expect(spendingBreakdownPage.spendingBreakdown2()).toHaveValue(breakdown2)
  await expect(spendingBreakdownPage.spendingBreakdown3()).toHaveValue(breakdown3)
}

const answerAndSubmitEntertainmentBreakdownQuestion = async (page: Page, breakdown1: string, breakdown2: string, breakdown3: string): Promise<void> => {
  const entertainmentBreakdownPage = new EntertainmentBreakdownPage(page)
  await entertainmentBreakdownPage.secondSpendingBreakdown1().fill(breakdown1)
  await entertainmentBreakdownPage.secondSpendingBreakdown2().fill(breakdown2)
  await entertainmentBreakdownPage.secondSpendingBreakdown3().fill(breakdown3)
  await entertainmentBreakdownPage.submit().click()
}

const assertRepeatingSectionOnChange = (
  getPage: () => Page,
  repeatIndex: number,
  currentBreakdown1: string,
  currentBreakdown2: string,
  currentBreakdown3: string,
  newTotal: string
): void => {
  test(
    `When I click 'Continue with section' on repeating section ${repeatIndex} with total ${newTotal}, ` +
      'Then I should be taken to the spending breakdown question and my previous answers should be prefilled',
    async () => {
      const page = getPage()
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink(repeatingSectionId(repeatIndex)).click()

      await assertSpendingBreakdownAnswer(page, currentBreakdown1, currentBreakdown2, currentBreakdown3)
    }
  )

  test(`When I submit the spending breakdown question with no changes on repeating section ${repeatIndex} with total ${newTotal}, Then I should see a validation error`, async () => {
    const page = getPage()
    const spendingBreakdownPage = new SpendingBreakdownPage(page)
    await spendingBreakdownPage.submit().click()

    await expect(spendingBreakdownPage.errorNumber(1)).toHaveText(`Enter answers that add up to £${newTotal}`)
  })

  test(
    `When I update my answers to equal the new total spending on repeating section ${repeatIndex} with total ${newTotal}, Then I should be able to get to the section summary ` +
      "and the breakdown section should be marked as 'Completed'",
    async () => {
      const page = getPage()
      const breakdownSectionSummary = new BreakdownSectionSummary(page)
      const hubPage = new HubPage(page)
      await answerAndSubmitSpendingBreakdownQuestion(page, newTotal, '0', '0')

      await verifyUrlContains(page, breakdownSectionSummary.pageName)
      await breakdownSectionSummary.submit().click()
      await expect(hubPage.summaryRowState(repeatingSectionId(repeatIndex))).toHaveText('Completed')
    }
  )
}

test.describe('Feature: Validation - Sum of grouped answers to equal total (Repeating section) (Total in separate section)', () => {
  test.describe.configure({ mode: 'serial' })

  test.describe('Given I start a repeating grouped answer validation with dependent sections and add 2 householdersand complete the household overview section', () => {
    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll(async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      const householdOverviewSectionSummary = new HouseholdOverviewSectionSummary(page)
      const hubPage = new HubPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const listCollectorSummaryPage = new ListCollectorSummaryPage(page)
      await openQuestionnaire('test_validation_sum_against_total_repeating_with_dependent_section.json')

      // Add 2 householders
      await addPersonToHousehold(page, 'John', 'Doe')
      await addPersonToHousehold(page, 'Jane', 'Doe')
      await listCollectorPage.no().click()
      await listCollectorPage.submit().scrollIntoViewIfNeeded()
      await listCollectorPage.submit().click()
      await listCollectorSummaryPage.submit().click()

      // Complete household overview section
      await answerAndSubmitTotalSpendingQuestion(page, '1000')
      await answerAndSubmitEntertainmentSpendingQuestion(page, '500')
      await householdOverviewSectionSummary.submit().click()

      await expect(hubPage.summaryRowState(householderSectionId)).toHaveText('Completed')
      await expect(hubPage.summaryRowState(householdOverviewSectionId)).toHaveText('Completed')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test("When I am on the hub, Then the two repeating breakdown sections should be marked as 'Not Started'", async () => {
      const hubPage = new HubPage(page)
      await expect(hubPage.summaryRowState(repeatingSectionId(1))).toHaveText('Not started')
      await expect(hubPage.summaryRowState(repeatingSectionId(2))).toHaveText('Not started')
    })

    test(
      "When I start a repeating section and don't skip the calculated question, and enter an answer that is not equal " +
        'to the total for the spending question, Then I should see a validation error',
      async () => {
        const breakdownDrivingPage = new BreakdownDrivingPage(page)
        const hubPage = new HubPage(page)
        const spendingBreakdownPage = new SpendingBreakdownPage(page)
        await hubPage.summaryRowLink(repeatingSectionId(1)).click()
        await breakdownDrivingPage.yes().click()
        await breakdownDrivingPage.submit().click()

        await answerAndSubmitSpendingBreakdownQuestion(page, '500', '500', '500')

        await expect(spendingBreakdownPage.errorNumber(1)).toHaveText('Enter answers that add up to £1,000.00')
      }
    )

    test(
      'When I enter an answer that is equal to the total for the spending question, ' +
        "Then I should be able to get to the section summary and the repeating section should be marked as 'Completed'",
      async () => {
        const breakdownSectionSummary = new BreakdownSectionSummary(page)
        const hubPage = new HubPage(page)
        await answerAndSubmitSpendingBreakdownQuestion(page, '500', '250', '250')
        await answerAndSubmitEntertainmentBreakdownQuestion(page, '250', '150', '100')

        await verifyUrlContains(page, breakdownSectionSummary.pageName)
        await breakdownSectionSummary.submit().click()

        await expect(hubPage.summaryRowState(repeatingSectionId(1))).toHaveText('Completed')
      }
    )

    test(
      "When I start another repeating section and answer 'No' to the driving question, " +
        "Then I should not have to answer the breakdown question and the section is marked as 'Completed'",
      async () => {
        const breakdownDrivingPage = new BreakdownDrivingPage(page)
        const breakdownSectionSummary = new BreakdownSectionSummary(page)
        const hubPage = new HubPage(page)
        await hubPage.summaryRowLink(repeatingSectionId(2)).click()
        await breakdownDrivingPage.no().click()
        await breakdownDrivingPage.submit().click()

        await verifyUrlContains(page, breakdownSectionSummary.pageName)
        await breakdownSectionSummary.submit().click()

        await expect(hubPage.summaryRowState(repeatingSectionId(2))).toHaveText('Completed')
      }
    )

    test(
      'When I change my answer for the total spending question, Then the first repeating section should be marked as ' +
        "'Partially completed' and section repeating section should stay as 'Completed'",
      async () => {
        const householdOverviewSectionSummary = new HouseholdOverviewSectionSummary(page)
        const hubPage = new HubPage(page)
        await hubPage.summaryRowLink(householdOverviewSectionId).click()
        await householdOverviewSectionSummary.totalSpendingAnswerEdit().click()

        await answerAndSubmitTotalSpendingQuestion(page, '1500')
        await householdOverviewSectionSummary.submit().click()
        await expect(hubPage.summaryRowState(repeatingSectionId(1))).toHaveText('Partially completed')

        // The 2nd repeating section skipped the breakdown question, therefore progress should updated for sections that have
        // calculated questions on the path.
        await expect(hubPage.summaryRowState(repeatingSectionId(2))).toHaveText('Completed')
      }
    )

    assertRepeatingSectionOnChange(() => page, 1, '500.00', '250.00', '250.00', '1,500.00')

    test(
      "When I change my answer to the driving question to 'Yes' for the 2nd repeating section, " +
        'Then I am able to answer the breakdown question and complete the section',
      async () => {
        const breakdownDrivingPage = new BreakdownDrivingPage(page)
        const breakdownSectionSummary = new BreakdownSectionSummary(page)
        const hubPage = new HubPage(page)
        await hubPage.summaryRowLink(repeatingSectionId(2)).click()
        await breakdownSectionSummary.breakdownDrivingAnswerEdit().click()
        await breakdownDrivingPage.yes().click()
        await breakdownDrivingPage.submit().click()

        await answerAndSubmitSpendingBreakdownQuestion(page, '1000', '500', '0')
        await answerAndSubmitEntertainmentBreakdownQuestion(page, '250', '150', '100')
        await breakdownSectionSummary.submit().click()
        await expect(hubPage.summaryRowState(repeatingSectionId(2))).toHaveText('Completed')
      }
    )

    test("When I change my answer for the total spending question, Then both repeating section should be marked as 'Partially completed'", async () => {
      const householdOverviewSectionSummary = new HouseholdOverviewSectionSummary(page)
      const hubPage = new HubPage(page)
      await hubPage.summaryRowLink(householdOverviewSectionId).click()
      await householdOverviewSectionSummary.totalSpendingAnswerEdit().click()

      await answerAndSubmitTotalSpendingQuestion(page, '2500')
      await householdOverviewSectionSummary.submit().click()
      await expect(hubPage.summaryRowState(repeatingSectionId(1))).toHaveText('Partially completed')

      // The 2nd repeating section is now on the path, therefore, its status should have been updated.
      await expect(hubPage.summaryRowState(repeatingSectionId(2))).toHaveText('Partially completed')
    })

    assertRepeatingSectionOnChange(() => page, 1, '1500.00', '0.00', '0.00', '2,500.00')
    assertRepeatingSectionOnChange(() => page, 2, '1000.00', '500.00', '0.00', '2,500.00')

    test("When I edit and resubmit the total spending question without changing the value, Then the repeating section's status should stay as 'Completed'", async () => {
      const householdOverviewSectionSummary = new HouseholdOverviewSectionSummary(page)
      const hubPage = new HubPage(page)
      const totalSpendingPage = new TotalSpendingPage(page)
      await hubPage.summaryRowLink(householdOverviewSectionId).click()
      await householdOverviewSectionSummary.totalSpendingAnswerEdit().click()

      await expect(totalSpendingPage.totalSpending()).toHaveValue('2500.00')
      await totalSpendingPage.submit().click()
      await householdOverviewSectionSummary.submit().click()

      await expect(hubPage.summaryRowState(repeatingSectionId(1))).toHaveText('Completed')
      await expect(hubPage.summaryRowState(repeatingSectionId(2))).toHaveText('Completed')
    })

    test('When I submit the questionnaire, Then I should see the thank you page', async () => {
      const hubPage = new HubPage(page)
      const thankYouPage = new ThankYouPage(page)
      await hubPage.submit().click()

      await verifyUrlContains(page, thankYouPage.pageName)
    })
  })
})
