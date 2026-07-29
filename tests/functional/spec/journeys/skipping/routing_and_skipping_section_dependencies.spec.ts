import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { BrowserContext, Page } from '../../../fixtures/test'
import AgePage from '../../../generated_pages/routing_and_skipping_section_dependencies/age.page'
import HouseHoldPersonalDetailsSectionSummaryPage from '../../../generated_pages/routing_and_skipping_section_dependencies/household-personal-details-section-summary.page'
import HouseholdSectionSummaryPage from '../../../generated_pages/routing_and_skipping_section_dependencies/household-section-summary.page'
import ListCollectorAddPage from '../../../generated_pages/routing_and_skipping_section_dependencies/list-collector-add.page'
import ListCollectorPage from '../../../generated_pages/routing_and_skipping_section_dependencies/list-collector.page'
import NamePage from '../../../generated_pages/routing_and_skipping_section_dependencies/name-block.page'
import PrimaryPersonSummaryPage from '../../../generated_pages/routing_and_skipping_section_dependencies/primary-person-summary.page'
import ReasonNoConfirmationPage from '../../../generated_pages/routing_and_skipping_section_dependencies/reason-no-confirmation.page'
import RepeatingAgePage from '../../../generated_pages/routing_and_skipping_section_dependencies/repeating-age.page'
import RepeatingSexPage from '../../../generated_pages/routing_and_skipping_section_dependencies/repeating-sex.page'
import SecurityPage from '../../../generated_pages/routing_and_skipping_section_dependencies/security.page'
import SkipAgePage from '../../../generated_pages/routing_and_skipping_section_dependencies/skip-age.page'
import SkipEnableSectionPage from '../../../generated_pages/routing_and_skipping_section_dependencies/skip-household-section.page'
import EnableSectionPage from '../../../generated_pages/routing_and_skipping_section_dependencies/enable-section.page'
import SkipConfirmationPage from '../../../generated_pages/routing_and_skipping_section_dependencies/skip-confirmation.page'
import SkipConfirmationSectionSummaryPage from '../../../generated_pages/routing_and_skipping_section_dependencies/skip-confirmation-section-summary.page'
import SkipSectionSummaryPage from '../../../generated_pages/routing_and_skipping_section_dependencies/skip-section-summary.page'
import RepeatingIsDependentPage from '../../../generated_pages/routing_and_skipping_section_dependencies/repeating-is-dependent.page'
import RepeatingIsSmokerPage from '../../../generated_pages/routing_and_skipping_section_dependencies/repeating-is-smoker.page'
import HubPage from '../../../base_pages/hub.page'

test.describe('Routing and skipping section dependencies', () => {
  test.describe.configure({ mode: 'serial' })

  test.describe('Given the routing and skipping section dependencies questionnaire', () => {
    test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_routing_and_skipping_section_dependencies.json')
    })

    test("When I answer 'No' to skipping the age question, Then in the Primary Person section I am asked my name, age and why I didn't confirm skipping", async ({
      page
    }) => {
      await answerNoToSkipAgeQuestion(page)

      await selectPrimaryPerson(page)
      await answerAndSubmitNameQuestion(page)
      await answerAndSubmitAgeQuestion(page)
      await answerAndSubmitReasonForNoConfirmationQuestion(page)

      await expectPersonalDetailsName(page)
      await expectPersonalDetailsAge(page)
      await expectReasonNoConfirmationAnswer(page)
    })

    test("When I answer 'Yes' to skipping the age question, Then in the Primary Person section I am only asked my name and why I didn't confirm skipping", async ({
      page
    }) => {
      await answerYesToSkipAgeQuestion(page)

      await selectPrimaryPerson(page)
      await answerAndSubmitNameQuestion(page)
      await answerAndSubmitReasonForNoConfirmationQuestion(page)

      await expectPersonalDetailsName(page)
      await expectReasonNoConfirmationAnswer(page)
      await expectPersonalDetailsAgeExistingFalse(page)
    })

    test(
      "When I answer 'Yes' to skipping the age question and 'Yes' to are you sure in skip question confirmation section, " +
        'Then in the Primary Person section I am just asked my name',
      async ({ page }) => {
        await answerYesToSkipAgeQuestion(page)

        await selectConfirmationSectionAndAnswerSecurityQuestion(page)
        await answerYesToSkipConfirmationQuestion(page)

        await selectPrimaryPerson(page)
        await answerAndSubmitNameQuestion(page)

        await expectPersonalDetailsName(page)
        await expectPersonalDetailsAgeExistingFalse(page)
        await expectReasonNoConfirmationExistingFalse(page)
      }
    )

    test(
      "When I answer 'Yes' to skipping the age question but 'No' to are you sure in skip question confirmation section, " +
        'Then in the Primary Person section I am only asked my name and age',
      async ({ page }) => {
        await answerYesToSkipAgeQuestion(page)

        await selectConfirmationSectionAndAnswerSecurityQuestion(page)
        await answerNoToSkipConfirmationQuestion(page)

        await selectPrimaryPerson(page)
        await answerAndSubmitNameQuestion(page)
        await answerAndSubmitAgeQuestion(page)

        await expectPersonalDetailsName(page)
        await expectPersonalDetailsAge(page)
        await expectReasonNoConfirmationExistingFalse(page)
      }
    )

    test("When I answer 'No' to skipping the age question and populate the household, Then in each repeating section I am not asked their age", async ({
      page
    }) => {
      const houseHoldPersonalDetailsSectionSummaryPage = new HouseHoldPersonalDetailsSectionSummaryPage(page)
      const hubPage = new HubPage(page)
      const repeatingAgePage = new RepeatingAgePage(page)
      const repeatingIsDependentPage = new RepeatingIsDependentPage(page)
      const repeatingIsSmokerPage = new RepeatingIsSmokerPage(page)
      const repeatingSexPage = new RepeatingSexPage(page)
      await answerNoToSkipAgeQuestion(page)

      await addHouseholdMembers(page)

      await hubPage.summaryRowLink('household-personal-details-section-1').click()
      await repeatingSexPage.female().click()
      await repeatingSexPage.submit().click()
      await repeatingAgePage.answer().fill('45')
      await repeatingAgePage.submit().click()
      await repeatingIsDependentPage.no().click()
      await repeatingIsDependentPage.submit().click()
      await repeatingIsSmokerPage.no().click()
      await repeatingIsSmokerPage.submit().click()

      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).toHaveText('Female')
      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).toHaveText('45')

      await houseHoldPersonalDetailsSectionSummaryPage.submit().click()
      await hubPage.summaryRowLink('household-personal-details-section-2').click()
      await repeatingSexPage.male().click()
      await repeatingSexPage.submit().click()
      await repeatingAgePage.answer().fill('10')
      await repeatingAgePage.submit().click()
      await repeatingIsDependentPage.yes().click()
      await repeatingIsDependentPage.submit().click()

      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).toHaveText('Male')
      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).toHaveText('10')
    })

    test("When I answer 'Yes' to skipping the age question and populate the household, Then in each repeating section I am not asked their age", async ({
      page
    }) => {
      const houseHoldPersonalDetailsSectionSummaryPage = new HouseHoldPersonalDetailsSectionSummaryPage(page)
      const hubPage = new HubPage(page)
      const repeatingIsDependentPage = new RepeatingIsDependentPage(page)
      const repeatingSexPage = new RepeatingSexPage(page)
      await answerYesToSkipAgeQuestion(page)

      await addHouseholdMembers(page)

      await hubPage.summaryRowLink('household-personal-details-section-1').click()
      await repeatingSexPage.female().click()
      await repeatingSexPage.submit().click()
      await repeatingIsDependentPage.no().click()
      await repeatingIsDependentPage.submit().click()
      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).toHaveText('Female')
      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).not.toBeVisible()

      await houseHoldPersonalDetailsSectionSummaryPage.submit().click()
      await hubPage.summaryRowLink('household-personal-details-section-2').click()
      await repeatingSexPage.male().click()
      await repeatingSexPage.submit().click()
      await repeatingIsDependentPage.yes().click()
      await repeatingIsDependentPage.submit().click()

      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).toHaveText('Male')
      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).not.toBeVisible()
    })
  })

  test.describe('Given the routing and skipping section dependencies questionnaire', () => {
    test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_routing_and_skipping_section_dependencies.json')
    })

    test(
      "When I answer 'No' to skipping the section question and 'Yes' to enable the section question, " +
        'Then the household summary will be visible on the hub',
      async ({ page }) => {
        const hubPage = new HubPage(page)
        await answerNoToSkipEnableQuestionAndYesToEnableSection(page)

        await expect(hubPage.summaryRowLink('household-section')).toBeVisible()
      }
    )

    test(
      "When I answer 'No' to skipping the section question and 'No' to enable the section question, " +
        'Then the household summary will not be visible on the hub',
      async ({ page }) => {
        const hubPage = new HubPage(page)
        await answerNoToSkipEnableQuestionAndNoToEnableSection(page)

        await expect(hubPage.summaryRowLink('household-section')).not.toBeVisible()
      }
    )
  })

  test.describe(
    "Given the routing and skipping section dependencies questionnaire and I answered 'No' to skipping the section question " +
      "and 'Yes' to enable the section question",
    () => {
      test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
        await openQuestionnaire('test_routing_and_skipping_section_dependencies.json')
      })

      test("When I change my answer to skipping the section question to 'No', Then the household summary will not be visible on the hub", async ({ page }) => {
        const hubPage = new HubPage(page)
        await answerNoToSkipEnableQuestionAndYesToEnableSection(page)
        await changeSkipEnableQuestionToYes(page)

        await expect(hubPage.summaryRowLink('household-section')).not.toBeVisible()
      })
    }
  )

  test.describe(
    "Given the routing and skipping section dependencies questionnaire and I answered 'Yes' to skipping the age question " +
      "but 'No' to are you sure in skip question confirmation section",
    () => {
      test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
        await openQuestionnaire('test_routing_and_skipping_section_dependencies.json')
      })

      test(
        "When I change my answer to skipping age to 'No', removing the 'are you sure' question from the path, " +
          "Then in the Primary Person section I am asked my name, age and why I didn't confirm skipping",
        async ({ page }) => {
          const primaryPersonSummaryPage = new PrimaryPersonSummaryPage(page)
          const reasonNoConfirmationPage = new ReasonNoConfirmationPage(page)
          await answerYesToSkipAgeQuestion(page)

          await selectConfirmationSectionAndAnswerSecurityQuestion(page)
          await answerNoToSkipConfirmationQuestion(page)

          await editNoToSkipAgeQuestion(page)

          await selectPrimaryPerson(page)
          await answerAndSubmitNameQuestion(page)
          await answerAndSubmitAgeQuestion(page)

          await reasonNoConfirmationPage.iDidButItWasRemovedFromThePathAsIChangedMyAnswerToNoOnTheSkipQuestion().click()
          await reasonNoConfirmationPage.submit().click()

          await expectPersonalDetailsName(page)
          await expectPersonalDetailsAge(page)
          await expect(primaryPersonSummaryPage.reasonNoConfirmationAnswer()).toHaveText(
            'I did, but it was removed from the path as I changed my answer to No on the skip question'
          )
        }
      )
    }
  )

  test.describe(
    "Given the routing and skipping section dependencies questionnaire and I answered 'Yes' to skipping the age question " +
      'and complete the Primary Person section',
    () => {
      let context: BrowserContext
      let page: Page
      let openQuestionnaire: ReturnType<typeof createOpenQuestionnaire>

      test.beforeAll('Load the survey', async ({ browser }) => {
        context = await browser.newContext()
        page = await context.newPage()
        openQuestionnaire = createOpenQuestionnaire(page)
        await openQuestionnaire('test_routing_and_skipping_section_dependencies.json')
      })

      test.afterAll(async () => {
        await context.close()
      })

      test("When I change my answer to skipping age to 'No', Then the Primary Person section status is changed to Partially completed", async () => {
        const hubPage = new HubPage(page)
        const primaryPersonSummaryPage = new PrimaryPersonSummaryPage(page)
        await answerYesToSkipAgeQuestion(page)
        await selectPrimaryPerson(page)
        await answerAndSubmitNameQuestion(page)
        await answerAndSubmitReasonForNoConfirmationQuestion(page)
        await primaryPersonSummaryPage.submit().click()

        await expect(hubPage.summaryRowState('primary-person')).toHaveText('Completed')

        await editNoToSkipAgeQuestion(page)

        await expect(hubPage.summaryRowState('primary-person')).toHaveText('Partially completed')
      })

      test("When I change my answer back to skipping age to 'Yes', Then the Primary Person section status is changed back to Completed", async () => {
        const hubPage = new HubPage(page)
        await editYesToSkipAgeQuestion(page)

        await expect(hubPage.summaryRowState('primary-person')).toHaveText('Completed')
      })
    }
  )

  test.describe(
    "Given the routing and skipping section dependencies questionnaire and I answered 'Yes' to skipping the age question " +
      'and add 2 household members but complete only one',
    () => {
      let context: BrowserContext
      let page: Page
      let openQuestionnaire: ReturnType<typeof createOpenQuestionnaire>

      test.beforeAll('Load the survey', async ({ browser }) => {
        context = await browser.newContext()
        page = await context.newPage()
        openQuestionnaire = createOpenQuestionnaire(page)
        await openQuestionnaire('test_routing_and_skipping_section_dependencies.json')
      })

      test.afterAll(async () => {
        await context.close()
      })

      test(
        "When I change my answer to skipping age to 'No', " +
          'Then the completed household member status is changed to Partially completed and the other stays as not started',
        async () => {
          const houseHoldPersonalDetailsSectionSummaryPage = new HouseHoldPersonalDetailsSectionSummaryPage(page)
          const hubPage = new HubPage(page)
          const repeatingIsDependentPage = new RepeatingIsDependentPage(page)
          const repeatingSexPage = new RepeatingSexPage(page)
          await answerYesToSkipAgeQuestion(page)
          await addHouseholdMembers(page)
          await hubPage.summaryRowLink('household-personal-details-section-1').click()
          await repeatingSexPage.female().click()
          await repeatingSexPage.submit().click()
          await repeatingIsDependentPage.no().click()
          await repeatingIsDependentPage.submit().click()
          await houseHoldPersonalDetailsSectionSummaryPage.submit().click()

          await editNoToSkipAgeQuestion(page)

          await expect(hubPage.summaryRowState('household-personal-details-section-1')).toHaveText('Partially completed')
          await expect(hubPage.summaryRowState('household-personal-details-section-2')).toHaveText('Not started')
        }
      )

      test(
        "When I change my answer back to skipping age to 'Yes', " +
          'Then the Partially completed household member status is changed back to Completed and the other stays as not started',
        async () => {
          const hubPage = new HubPage(page)
          await editYesToSkipAgeQuestion(page)

          await expect(hubPage.summaryRowState('household-personal-details-section-1')).toHaveText('Completed')
          await expect(hubPage.summaryRowState('household-personal-details-section-2')).toHaveText('Not started')
        }
      )
    }
  )

  test.describe('Given the routing and skipping section dependencies questionnaire', () => {
    test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_routing_and_skipping_section_dependencies.json')
    })

    test(
      "When I answer 'No' to skipping the age question and populate the household with Repeating Age > 18, " +
        'Then in each repeating section I am asked if they are smoker',
      async ({ page }) => {
        const houseHoldPersonalDetailsSectionSummaryPage = new HouseHoldPersonalDetailsSectionSummaryPage(page)
        const hubPage = new HubPage(page)
        const repeatingAgePage = new RepeatingAgePage(page)
        const repeatingIsDependentPage = new RepeatingIsDependentPage(page)
        const repeatingIsSmokerPage = new RepeatingIsSmokerPage(page)
        const repeatingSexPage = new RepeatingSexPage(page)
        await answerNoToSkipAgeQuestion(page)

        await addHouseholdMembers(page)

        await hubPage.summaryRowLink('household-personal-details-section-1').click()
        await repeatingSexPage.female().click()
        await repeatingSexPage.submit().click()
        await repeatingAgePage.answer().fill('45')
        await repeatingAgePage.submit().click()
        await repeatingIsDependentPage.no().click()
        await repeatingIsDependentPage.submit().click()
        await repeatingIsSmokerPage.no().click()
        await repeatingIsSmokerPage.submit().click()

        await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).toHaveText('Female')
        await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).toHaveText('45')
        await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).toHaveText('No')

        await houseHoldPersonalDetailsSectionSummaryPage.submit().click()
        await hubPage.summaryRowLink('household-personal-details-section-2').click()
        await repeatingSexPage.male().click()
        await repeatingSexPage.submit().click()
        await repeatingAgePage.answer().fill('19')
        await repeatingAgePage.submit().click()
        await repeatingIsDependentPage.yes().click()
        await repeatingIsDependentPage.submit().click()
        await repeatingIsSmokerPage.no().click()
        await repeatingIsSmokerPage.submit().click()

        await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).toHaveText('Male')
        await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).toHaveText('19')
        await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).toHaveText('No')
      }
    )

    test(
      "When I answer 'No' to skipping the age question and populate the household with Repeating Age < 18, " +
        'Then in each repeating section I am not asked if they are smoker',
      async ({ page }) => {
        const houseHoldPersonalDetailsSectionSummaryPage = new HouseHoldPersonalDetailsSectionSummaryPage(page)
        const hubPage = new HubPage(page)
        const repeatingAgePage = new RepeatingAgePage(page)
        const repeatingIsDependentPage = new RepeatingIsDependentPage(page)
        const repeatingSexPage = new RepeatingSexPage(page)
        await answerNoToSkipAgeQuestion(page)

        await addHouseholdMembers(page)

        await hubPage.summaryRowLink('household-personal-details-section-1').click()
        await repeatingSexPage.female().click()
        await repeatingSexPage.submit().click()
        await repeatingAgePage.answer().fill('15')
        await repeatingAgePage.submit().click()
        await repeatingIsDependentPage.yes().click()
        await repeatingIsDependentPage.submit().click()

        await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).toHaveText('Female')
        await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).toHaveText('15')
        await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).not.toBeVisible()

        await houseHoldPersonalDetailsSectionSummaryPage.submit().click()
        await hubPage.summaryRowLink('household-personal-details-section-2').click()
        await repeatingSexPage.male().click()
        await repeatingSexPage.submit().click()
        await repeatingAgePage.answer().fill('10')
        await repeatingAgePage.submit().click()
        await repeatingIsDependentPage.yes().click()
        await repeatingIsDependentPage.submit().click()

        await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).toHaveText('Male')
        await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).toHaveText('10')
        await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).not.toBeVisible()
      }
    )

    test("When I answer 'Yes' to skipping the age question and populate the household, Then in each repeating section I am not asked if they are smoker", async ({
      page
    }) => {
      const houseHoldPersonalDetailsSectionSummaryPage = new HouseHoldPersonalDetailsSectionSummaryPage(page)
      const hubPage = new HubPage(page)
      const repeatingIsDependentPage = new RepeatingIsDependentPage(page)
      const repeatingSexPage = new RepeatingSexPage(page)
      await answerYesToSkipAgeQuestion(page)

      await addHouseholdMembers(page)

      await hubPage.summaryRowLink('household-personal-details-section-1').click()
      await repeatingSexPage.female().click()
      await repeatingSexPage.submit().click()
      await repeatingIsDependentPage.no().click()
      await repeatingIsDependentPage.submit().click()
      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).toHaveText('Female')
      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).not.toBeVisible()
      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).not.toBeVisible()

      await houseHoldPersonalDetailsSectionSummaryPage.submit().click()
      await hubPage.summaryRowLink('household-personal-details-section-2').click()
      await repeatingSexPage.male().click()
      await repeatingSexPage.submit().click()
      await repeatingIsDependentPage.yes().click()
      await repeatingIsDependentPage.submit().click()

      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).toHaveText('Male')
      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).not.toBeVisible()
      await expect(houseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).not.toBeVisible()
    })
  })
})

const addHouseholdMembers = async (page: Page): Promise<void> => {
  const hubPage = new HubPage(page)
  const householdSectionSummaryPage = new HouseholdSectionSummaryPage(page)
  const listCollectorPage = new ListCollectorPage(page)
  const listCollectorAddPage = new ListCollectorAddPage(page)
  await hubPage.summaryRowLink('household-section').click()
  await listCollectorPage.yes().click()
  await listCollectorPage.submit().click()
  await listCollectorAddPage.firstName().fill('Sarah')
  await listCollectorAddPage.lastName().fill('Smith')
  await listCollectorAddPage.submit().click()
  await listCollectorPage.yes().click()
  await listCollectorPage.submit().click()
  await listCollectorAddPage.firstName().fill('Marcus')
  await listCollectorAddPage.lastName().fill('Smith')
  await listCollectorAddPage.submit().click()
  await listCollectorPage.no().click()
  await listCollectorPage.submit().click()
  await householdSectionSummaryPage.submit().click()
}

const selectPrimaryPerson = async (page: Page): Promise<void> => {
  const hubPage = new HubPage(page)
  await hubPage.summaryRowLink('primary-person').click()
}

const selectConfirmationSectionAndAnswerSecurityQuestion = async (page: Page): Promise<void> => {
  const hubPage = new HubPage(page)
  const securityPage = new SecurityPage(page)
  await hubPage.summaryRowLink('skip-confirmation-section').click()
  await securityPage.yes().click()
  await securityPage.submit().click()
}

const answerYesToSkipAgeQuestion = async (page: Page): Promise<void> => {
  const hubPage = new HubPage(page)
  const skipAgePage = new SkipAgePage(page)
  const skipEnableSectionPage = new SkipEnableSectionPage(page)
  const enableSectionPage = new EnableSectionPage(page)
  const skipSectionSummaryPage = new SkipSectionSummaryPage(page)
  await hubPage.summaryRowLink('skip-section').click()
  await skipAgePage.yes().click()
  await skipAgePage.submit().click()
  await skipEnableSectionPage.no().click()
  await skipEnableSectionPage.submit().click()
  await enableSectionPage.yes().click()
  await enableSectionPage.submit().click()
  await skipSectionSummaryPage.submit().click()
}

const editNoToSkipAgeQuestion = async (page: Page): Promise<void> => {
  const hubPage = new HubPage(page)
  const skipAgePage = new SkipAgePage(page)
  const skipSectionSummaryPage = new SkipSectionSummaryPage(page)
  await hubPage.summaryRowLink('skip-section').click()
  await skipSectionSummaryPage.skipAgeAnswerEdit().click()
  await skipAgePage.no().click()
  await skipAgePage.submit().click()
  await skipSectionSummaryPage.submit().click()
}

const editYesToSkipAgeQuestion = async (page: Page): Promise<void> => {
  const hubPage = new HubPage(page)
  const skipAgePage = new SkipAgePage(page)
  const skipSectionSummaryPage = new SkipSectionSummaryPage(page)
  await hubPage.summaryRowLink('skip-section').click()
  await skipSectionSummaryPage.skipAgeAnswerEdit().click()
  await skipAgePage.yes().click()
  await skipAgePage.submit().click()
  await skipSectionSummaryPage.submit().click()
}

const answerNoToSkipAgeQuestion = async (page: Page): Promise<void> => {
  const hubPage = new HubPage(page)
  const skipAgePage = new SkipAgePage(page)
  const skipEnableSectionPage = new SkipEnableSectionPage(page)
  const enableSectionPage = new EnableSectionPage(page)
  const skipSectionSummaryPage = new SkipSectionSummaryPage(page)
  await hubPage.summaryRowLink('skip-section').click()
  await skipAgePage.no().click()
  await skipAgePage.submit().click()
  await skipEnableSectionPage.no().click()
  await skipEnableSectionPage.submit().click()
  await enableSectionPage.yes().click()
  await enableSectionPage.submit().click()
  await skipSectionSummaryPage.submit().click()
}

const answerNoToSkipConfirmationQuestion = async (page: Page): Promise<void> => {
  const skipConfirmationPage = new SkipConfirmationPage(page)
  const skipConfirmationSectionSummaryPage = new SkipConfirmationSectionSummaryPage(page)
  await skipConfirmationPage.no().click()
  await skipConfirmationPage.submit().click()
  await skipConfirmationSectionSummaryPage.submit().click()
}

const answerYesToSkipConfirmationQuestion = async (page: Page): Promise<void> => {
  const skipConfirmationPage = new SkipConfirmationPage(page)
  const skipConfirmationSectionSummaryPage = new SkipConfirmationSectionSummaryPage(page)
  await skipConfirmationPage.yes().click()
  await skipConfirmationPage.submit().click()
  await skipConfirmationSectionSummaryPage.submit().click()
}

const answerNoToSkipEnableQuestionAndYesToEnableSection = async (page: Page): Promise<void> => {
  const hubPage = new HubPage(page)
  const skipAgePage = new SkipAgePage(page)
  const skipEnableSectionPage = new SkipEnableSectionPage(page)
  const enableSectionPage = new EnableSectionPage(page)
  const skipSectionSummaryPage = new SkipSectionSummaryPage(page)
  await hubPage.summaryRowLink('skip-section').click()
  await skipAgePage.no().click()
  await skipAgePage.submit().click()
  await skipEnableSectionPage.no().click()
  await skipEnableSectionPage.submit().click()
  await enableSectionPage.yes().click()
  await enableSectionPage.submit().click()
  await skipSectionSummaryPage.submit().click()
}

const answerNoToSkipEnableQuestionAndNoToEnableSection = async (page: Page): Promise<void> => {
  const hubPage = new HubPage(page)
  const skipAgePage = new SkipAgePage(page)
  const skipEnableSectionPage = new SkipEnableSectionPage(page)
  const enableSectionPage = new EnableSectionPage(page)
  const skipSectionSummaryPage = new SkipSectionSummaryPage(page)
  await hubPage.summaryRowLink('skip-section').click()
  await skipAgePage.no().click()
  await skipAgePage.submit().click()
  await skipEnableSectionPage.no().click()
  await skipEnableSectionPage.submit().click()
  await enableSectionPage.no().click()
  await enableSectionPage.submit().click()
  await skipSectionSummaryPage.submit().click()
}

const changeSkipEnableQuestionToYes = async (page: Page): Promise<void> => {
  const hubPage = new HubPage(page)
  const skipEnableSectionPage = new SkipEnableSectionPage(page)
  const skipSectionSummaryPage = new SkipSectionSummaryPage(page)
  await hubPage.summaryRowLink('skip-section').click()
  await skipSectionSummaryPage.skipHouseholdSectionAnswerEdit().click()
  await skipEnableSectionPage.yes().click()
  await skipEnableSectionPage.submit().click()
  await skipSectionSummaryPage.submit().click()
}

const answerAndSubmitNameQuestion = async (page: Page): Promise<void> => {
  const namePage = new NamePage(page)
  await namePage.name().fill('John Smith')
  await namePage.submit().click()
}

const answerAndSubmitAgeQuestion = async (page: Page): Promise<void> => {
  const agePage = new AgePage(page)
  await agePage.answer().fill('50')
  await agePage.submit().click()
}

const answerAndSubmitReasonForNoConfirmationQuestion = async (page: Page): Promise<void> => {
  const reasonNoConfirmationPage = new ReasonNoConfirmationPage(page)
  await reasonNoConfirmationPage.iDidNotVisitSection2SoConfirmationWasNotNeeded().click()
  await reasonNoConfirmationPage.submit().click()
}

const expectPersonalDetailsName = async (page: Page): Promise<void> => {
  const primaryPersonSummaryPage = new PrimaryPersonSummaryPage(page)
  await expect(primaryPersonSummaryPage.nameAnswer()).toHaveText('John Smith')
}

const expectPersonalDetailsAge = async (page: Page): Promise<void> => {
  const primaryPersonSummaryPage = new PrimaryPersonSummaryPage(page)
  await expect(primaryPersonSummaryPage.ageAnswer()).toHaveText('50')
}

const expectReasonNoConfirmationAnswer = async (page: Page): Promise<void> => {
  const primaryPersonSummaryPage = new PrimaryPersonSummaryPage(page)
  await expect(primaryPersonSummaryPage.reasonNoConfirmationAnswer()).toHaveText('I did not visit section 2, so confirmation was not needed')
}

const expectPersonalDetailsAgeExistingFalse = async (page: Page): Promise<void> => {
  const primaryPersonSummaryPage = new PrimaryPersonSummaryPage(page)
  await expect(primaryPersonSummaryPage.ageAnswer()).not.toBeVisible()
}

const expectReasonNoConfirmationExistingFalse = async (page: Page): Promise<void> => {
  const primaryPersonSummaryPage = new PrimaryPersonSummaryPage(page)
  await expect(primaryPersonSummaryPage.reasonNoConfirmationAnswer()).not.toBeVisible()
}
