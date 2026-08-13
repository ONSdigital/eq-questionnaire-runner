import { test, expect } from '../../../fixtures/test'
import QuestionPageOne from '../../../generated_pages/default/number-question-one.page'
import QuestionPageTwo from '../../../generated_pages/default/number-question-two.page'
import SubmitPage from '../../../generated_pages/default/submit.page'
import QuestionPageOneSkip from '../../../generated_pages/default_with_skip/number-question-one.page'
import QuestionPageThreeSkip from '../../../generated_pages/default_with_skip/number-question-three.page'

test.describe('Feature: Default Value', () => {
  test('Given I start default schema, When I do not answer a question, Then "no answer provided" is displayed on the Summary page', async ({
    page,
    openQuestionnaire
  }) => {
    const questionPageOne = new QuestionPageOne(page)
    const questionPageTwo = new QuestionPageTwo(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire('test_default.json')
    await questionPageOne.submit().click()
    await expect(page).toHaveURL(new RegExp(questionPageTwo.pageName))
    await questionPageTwo.two().fill('123')
    await questionPageTwo.submit().click()
    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    await expect(submitPage.answerOne()).toHaveText('0')
  })

  test('Given I have not answered a question containing a default value, When I return to the question, Then no value should be displayed', async ({
    page,
    openQuestionnaire
  }) => {
    const questionPageOne = new QuestionPageOne(page)
    const questionPageTwo = new QuestionPageTwo(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire('test_default.json')
    await questionPageOne.submit().click()
    await expect(page).toHaveURL(new RegExp(questionPageTwo.pageName))
    await questionPageTwo.two().fill('123')
    await questionPageTwo.submit().click()
    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    await submitPage.previous().click()
    await expect(page).toHaveURL(new RegExp(questionPageTwo.pageName))
    await questionPageTwo.previous().click()
    await expect(page).toHaveURL(new RegExp(questionPageOne.pageName))
    await expect(questionPageOne.one()).toHaveValue('')
  })

  test('Given I have not answered a question containing a default value, When a skip condition checks for the default value, Then I should skip the next question', async ({
    page,
    openQuestionnaire
  }) => {
    const questionPageOneSkip = new QuestionPageOneSkip(page)
    const questionPageThreeSkip = new QuestionPageThreeSkip(page)
    await openQuestionnaire('test_default_with_skip.json')
    await questionPageOneSkip.submit().click()
    await expect(page).toHaveURL(new RegExp(questionPageThreeSkip.pageName))
    await expect(questionPageThreeSkip.questionText()).toHaveText('Question Three')
  })
})
