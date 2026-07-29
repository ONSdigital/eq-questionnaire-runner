import { test, expect } from '../../fixtures/test'
import DoesAnyoneLiveHerePage from '../../generated_pages/confirmation_question_within_repeating_section/list-collector.page'
import AddPersonPage from '../../generated_pages/confirmation_question_within_repeating_section/list-collector-add.page'
import CarerPage from '../../generated_pages/confirmation_question_within_repeating_section/carer-block.page'
import DateOfBirthPage from '../../generated_pages/confirmation_question_within_repeating_section/dob-block.page'
import ConfirmDateOfBirthPage from '../../generated_pages/confirmation_question_within_repeating_section/confirm-dob-block.page'
import DefaultSectionSummary from '../../generated_pages/confirmation_question_within_repeating_section/default-section-summary.page'
import ConfirmCarerPage from '../../generated_pages/confirmation_question_within_repeating_section/confirm-carer-block.page'
import StudentPage from '../../generated_pages/confirmation_question_within_repeating_section/student-block.page'

test.describe('Feature: Confirmation Question Within A Repeating Section', () => {
  test.describe('Given I am in a repeating section', () => {
    test.beforeEach('Add a person', async ({ page, openQuestionnaire }) => {
      const addPersonPage = new AddPersonPage(page)
      const dateOfBirthPage = new DateOfBirthPage(page)
      const doesAnyoneLiveHerePage = new DoesAnyoneLiveHerePage(page)
      await openQuestionnaire('test_confirmation_question_within_repeating_section.json')
      await doesAnyoneLiveHerePage.yes().click()
      await doesAnyoneLiveHerePage.submit().click()
      await addPersonPage.firstName().fill('John')
      await addPersonPage.lastName().fill('Doe')
      await addPersonPage.submit().click()
      await doesAnyoneLiveHerePage.no().click()
      await doesAnyoneLiveHerePage.submit().click()
      await expect(page).toHaveURL(new RegExp(dateOfBirthPage.pageName))
    })

    test.describe('Given a confirmation question', () => {
      test("When I answer 'No' to the confirmation question, Then I should be routed back to the source question", async ({ page }) => {
        const confirmDateOfBirthPage = new ConfirmDateOfBirthPage(page)
        const dateOfBirthPage = new DateOfBirthPage(page)
        // Answer question preceding confirmation question
        await dateOfBirthPage.day().fill('01')
        await dateOfBirthPage.month().fill('01')
        await dateOfBirthPage.year().fill('2015')
        await dateOfBirthPage.submit().click()

        // Answer 'No' to confirmation question
        await confirmDateOfBirthPage.noINeedToChangeTheirDateOfBirth().click()
        await confirmDateOfBirthPage.submit().click()
        await expect(page).toHaveURL(new RegExp(dateOfBirthPage.pageName))
      })
    })

    test.describe('Given I have answered a confirmation question', () => {
      test('When I view the summary, Then the confirmation question should not be displayed', async ({ page }) => {
        const confirmDateOfBirthPage = new ConfirmDateOfBirthPage(page)
        const dateOfBirthPage = new DateOfBirthPage(page)
        const defaultSectionSummary = new DefaultSectionSummary(page)
        await dateOfBirthPage.day().fill('01')
        await dateOfBirthPage.month().fill('01')
        await dateOfBirthPage.year().fill('2015')
        await dateOfBirthPage.submit().click()

        await confirmDateOfBirthPage.yesPersonNameIsAgeOld().click()
        await confirmDateOfBirthPage.submit().click()

        await expect(page).toHaveURL(/sections\/default-section\//)
        await expect(defaultSectionSummary.confirmDateOfBirth()).not.toBeVisible()
      })
    })

    test.describe('Given a confirmation question with a skip condition', () => {
      test(
        "When I submit an a date of birth where the age is at least '16', " +
          'Then I should be skipped past the confirmation question and directed to the carer question',
        async ({ page }) => {
          const carerPage = new CarerPage(page)
          const dateOfBirthPage = new DateOfBirthPage(page)
          await dateOfBirthPage.day().fill('01')
          await dateOfBirthPage.month().fill('01')
          await dateOfBirthPage.year().fill('2000')
          await dateOfBirthPage.submit().click()

          await expect(page).toHaveURL(new RegExp(carerPage.pageName))
          await expect(carerPage.questionText()).toContainText('Does John Doe look')
        }
      )
    })

    test.describe('Given a confirmation question', () => {
      test('When I go back to change my answer and return to the confirmation question, then the confirmation answer is cleared and I am routed to the next question', async ({
        page
      }) => {
        const carerPage = new CarerPage(page)
        const confirmCarerPage = new ConfirmCarerPage(page)
        const dateOfBirthPage = new DateOfBirthPage(page)
        const studentPage = new StudentPage(page)
        await dateOfBirthPage.day().fill('01')
        await dateOfBirthPage.month().fill('01')
        await dateOfBirthPage.year().fill('1990')
        await dateOfBirthPage.submit().click()
        await carerPage.no().click()
        await carerPage.submit().click()
        await confirmCarerPage.noINeedToChangeTheCarerAnswer().click()
        await confirmCarerPage.submit().click()
        await carerPage.yes().click()
        await carerPage.submit().click()
        // Assert that neither confirmation radio is selected
        await expect(confirmCarerPage.yesTheCarerAnswerIsCorrect()).not.toBeChecked()
        await expect(confirmCarerPage.noINeedToChangeTheCarerAnswer()).not.toBeChecked()
        // Assert routed to next question
        await confirmCarerPage.yesTheCarerAnswerIsCorrect().click()
        await confirmCarerPage.submit().click()
        await expect(page).toHaveURL(new RegExp(studentPage.pageName))
      })
    })
  })
})
