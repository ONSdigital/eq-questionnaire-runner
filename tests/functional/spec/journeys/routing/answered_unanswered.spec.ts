import { test, expect } from '../../../fixtures/test'
import QuestionOne from '../../../generated_pages/routing_answered_unanswered/block-1.page'
import QuestionOneAnswered from '../../../generated_pages/routing_answered_unanswered/answered-question-1.page'
import QuestionOneUnanswered from '../../../generated_pages/routing_answered_unanswered/unanswered-question-1.page'
import QuestionTwo from '../../../generated_pages/routing_answered_unanswered/block-2.page'
import QuestionTwoAnswered from '../../../generated_pages/routing_answered_unanswered/answered-question-2.page'
import QuestionTwoUnanswered from '../../../generated_pages/routing_answered_unanswered/unanswered-question-2.page'
import QuestionThree from '../../../generated_pages/routing_answered_unanswered/block-3.page'
import QuestionThreeAnsweredOrNotZero from '../../../generated_pages/routing_answered_unanswered/answered-question-3.page'
import QuestionThreeUnansweredOrAnswerZero from '../../../generated_pages/routing_answered_unanswered/unanswered-or-zero-question-3.page'
import { verifyUrlContains } from '../../../helpers'

test.describe('Test routing question answered/unanswered', () => {
  test.describe('Given I am on the first question', () => {
    test.beforeEach('Load the questionnaire', async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_routing_answered_unanswered.json')
    })

    test('When I select any answer and submit, Then I should see a page saying I have answered the first question', async ({ page }) => {
      const questionOne = new QuestionOne(page)
      const questionOneAnswered = new QuestionOneAnswered(page)
      await questionOne.ham().click()
      await questionOne.submit().click()
      await expect(questionOneAnswered.heading()).toHaveText('You answered the first question!')
      await verifyUrlContains(page, questionOneAnswered.pageName)

      await questionOneAnswered.previous().click()
      await questionOne.cheese().click()
      await questionOne.submit().click()
      await expect(questionOneAnswered.heading()).toHaveText('You answered the first question!')
      await verifyUrlContains(page, questionOneAnswered.pageName)
    })

    test("When I don't select an answer and submit, Then I should see a page saying I have not answered the first question", async ({ page }) => {
      const questionOne = new QuestionOne(page)
      const questionOneAnswered = new QuestionOneAnswered(page)
      await questionOne.submit().click()
      await expect(questionOneAnswered.heading()).toHaveText('You did not answer the first question!')
      await verifyUrlContains(page, questionOneAnswered.pageName)
    })
  })

  test.describe('Given I am on the second question', () => {
    test.beforeEach('Load the questionnaire and get to the second question', async ({ page, openQuestionnaire }) => {
      const questionOne = new QuestionOne(page)
      const questionOneUnanswered = new QuestionOneUnanswered(page)
      await openQuestionnaire('test_routing_answered_unanswered.json')
      await questionOne.submit().click()
      await questionOneUnanswered.submit().click()
    })

    test('When I select any answer and submit, Then I should see a page saying I have answered the second question', async ({ page }) => {
      const questionOneAnswered = new QuestionOneAnswered(page)
      const questionTwo = new QuestionTwo(page)
      const questionTwoAnswered = new QuestionTwoAnswered(page)
      await questionTwo.pizzaHut().click()
      await questionTwo.submit().click()
      await expect(questionTwoAnswered.heading()).toHaveText('You answered the second question!')
      await verifyUrlContains(page, questionTwoAnswered.pageName)

      await questionOneAnswered.previous().click()
      await questionTwo.dominoS().click()
      await questionTwo.submit().click()
      await expect(questionTwoAnswered.heading()).toHaveText('You answered the second question!')
      await verifyUrlContains(page, questionTwoAnswered.pageName)
    })

    test("When I don't select an answer and submit, Then I should see a page saying I have not answered the second question", async ({ page }) => {
      const questionTwo = new QuestionTwo(page)
      const questionTwoAnswered = new QuestionTwoAnswered(page)
      const questionTwoUnanswered = new QuestionTwoUnanswered(page)
      await questionTwo.submit().click()
      await expect(questionTwoUnanswered.heading()).toHaveText('You did not answer the second question!')
      await verifyUrlContains(page, questionTwoAnswered.pageName)
    })
  })

  test.describe('Given I am on the third question', () => {
    test.beforeEach('Load the questionnaire and get to the third question', async ({ page, openQuestionnaire }) => {
      const questionOne = new QuestionOne(page)
      const questionOneUnanswered = new QuestionOneUnanswered(page)
      const questionTwo = new QuestionTwo(page)
      const questionTwoUnanswered = new QuestionTwoUnanswered(page)
      await openQuestionnaire('test_routing_answered_unanswered.json')
      await questionOne.submit().click()
      await questionOneUnanswered.submit().click()
      await questionTwo.submit().click()
      await questionTwoUnanswered.submit().click()
    })

    test('When I do not answer the question or answer `0` and submit, Then I should see a page saying I did not answer the question or that I chose `0`', async ({
      page
    }) => {
      const questionThree = new QuestionThree(page)
      const questionThreeUnansweredOrAnswerZero = new QuestionThreeUnansweredOrAnswerZero(page)
      await questionThree.submit().click()
      await expect(questionThreeUnansweredOrAnswerZero.heading()).toHaveText('You did not answer the question or chose 0 slices')
      await verifyUrlContains(page, questionThreeUnansweredOrAnswerZero.pageName)

      await questionThreeUnansweredOrAnswerZero.previous().click()
      await questionThree.answer3().fill('0')
      await questionThree.submit().click()
      await expect(questionThreeUnansweredOrAnswerZero.heading()).toHaveText('You did not answer the question or chose 0 slices')
      await verifyUrlContains(page, questionThreeUnansweredOrAnswerZero.pageName)
    })

    test('When I enter an answer greater than 0 and submit, Then I should see a page saying I chose at least one', async ({ page }) => {
      const questionThree = new QuestionThree(page)
      const questionThreeAnsweredOrNotZero = new QuestionThreeAnsweredOrNotZero(page)
      const questionTwoAnswered = new QuestionTwoAnswered(page)
      await questionThree.answer3().fill('2')
      await questionThree.submit().click()
      await expect(questionTwoAnswered.heading()).toHaveText('You chose at least 1 slice')
      await verifyUrlContains(page, questionThreeAnsweredOrNotZero.pageName)
    })
  })
})
