import { test, expect } from '../../../../fixtures/test'
import type { Page } from '../../../../fixtures/test'
import TotalAnswerPage from '../../../../generated_pages/validation_sum_against_value_source/total-block.page'
import BreakdownAnswerPage from '../../../../generated_pages/validation_sum_against_value_source/breakdown-block.page'
import TotalPlaybackPage from '../../../../generated_pages/validation_sum_against_value_source/number-total-playback.page'
import SecondBreakdownAnswerPage from '../../../../generated_pages/validation_sum_against_value_source/second-breakdown-block.page'
import SubmitPage from '../../../../generated_pages/validation_sum_against_total_equal/submit.page'
import AnotherTotalPlaybackPage from '../../../../generated_pages/validation_sum_against_value_source/another-number-total-playback.page'

const answerAndSubmitBreakdownQuestion = async (page: Page, breakdown1: string, breakdown2: string, breakdown3: string, breakdown4: string): Promise<void> => {
  const breakdownAnswerPage = new BreakdownAnswerPage(page)
  await breakdownAnswerPage.breakdown1().fill(breakdown1)
  await breakdownAnswerPage.breakdown2().fill(breakdown2)
  await breakdownAnswerPage.breakdown3().fill(breakdown3)
  await breakdownAnswerPage.breakdown4().fill(breakdown4)
  await breakdownAnswerPage.submit().click()
}

const answerAndSubmitSecondBreakdownQuestion = async (
  page: Page,
  breakdown1: string,
  breakdown2: string,
  breakdown3: string,
  breakdown4: string
): Promise<void> => {
  const secondBreakdownAnswerPage = new SecondBreakdownAnswerPage(page)
  await secondBreakdownAnswerPage.secondBreakdown1().fill(breakdown1)
  await secondBreakdownAnswerPage.secondBreakdown2().fill(breakdown2)
  await secondBreakdownAnswerPage.secondBreakdown3().fill(breakdown3)
  await secondBreakdownAnswerPage.secondBreakdown4().fill(breakdown4)
  await secondBreakdownAnswerPage.submit().click()
}

const answerBothBreakdownQuestions = async (page: Page, array1: string[], array2: string[]): Promise<void> => {
  const totalPlaybackPage = new TotalPlaybackPage(page)
  await answerAndSubmitBreakdownQuestion(page, array1[0], array1[1], array1[2], array1[3])

  await totalPlaybackPage.submit().click()

  await answerAndSubmitSecondBreakdownQuestion(page, array2[0], array2[1], array2[2], array2[3])
}

test.describe('Feature: Sum of grouped answers equal to validation against value source ', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_validation_sum_against_value_source.json')
  })

  test.describe('Given I start a grouped answer validation survey and enter 12 into the total', () => {
    test('When I continue and enter 3 in each breakdown field, Then I should be able to get to the total playback page', async ({ page }) => {
      const totalAnswerPage = new TotalAnswerPage(page)
      const totalPlaybackPage = new TotalPlaybackPage(page)
      await totalAnswerPage.total().fill('12')
      await totalAnswerPage.submit().click()

      await answerAndSubmitBreakdownQuestion(page, '3', '3', '3', '3')

      await expect(page).toHaveURL(new RegExp(totalPlaybackPage.pageName))
    })
  })

  test.describe('Given I have a calculated summary value of 12', () => {
    test('When I continue to second breakdown and enter values equal to calculated summary total, Then I should be able to get to the next calculated summary', async ({
      page
    }) => {
      const anotherTotalPlaybackPage = new AnotherTotalPlaybackPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('12')
      await totalAnswerPage.submit().click()

      await answerBothBreakdownQuestions(page, ['3', '3', '3', '3'], ['2', '2', '1', '1'])

      await expect(page).toHaveURL(new RegExp(anotherTotalPlaybackPage.pageName))
    })
  })

  test.describe('Given I completed both grouped answer validation questions and I am on the summary', () => {
    test('When I go back from the summary and change the total, Then I must reconfirm both breakdown questions with valid answers before I can get to the next calculated summary', async ({
      page
    }) => {
      const anotherTotalPlaybackPage = new AnotherTotalPlaybackPage(page)
      const breakdownAnswerPage = new BreakdownAnswerPage(page)
      const submitPage = new SubmitPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('12')
      await totalAnswerPage.submit().click()

      await answerBothBreakdownQuestions(page, ['3', '3', '3', '3'], ['2', '2', '1', '1'])

      await anotherTotalPlaybackPage.submit().click()

      await submitPage.totalAnswerEdit().click()
      await totalAnswerPage.total().fill('15')
      await totalAnswerPage.submit().click()

      await breakdownAnswerPage.submit().click()

      await expect(breakdownAnswerPage.errorNumber(1)).toBeVisible()

      await expect(breakdownAnswerPage.errorNumber(1)).toHaveText('Enter answers that add up to 15')

      await answerBothBreakdownQuestions(page, ['6', '3', '3', '3'], ['3', '3', '2', '1'])

      await expect(page).toHaveURL(new RegExp(anotherTotalPlaybackPage.pageName))
    })
  })

  test.describe('Given I completed both grouped answer validation questions and I am on the summary', () => {
    test('When I go back from the summary and change the total, Then I must reconfirm the breakdown question based on answer value source with valid answers before I can continue', async ({
      page
    }) => {
      const anotherTotalPlaybackPage = new AnotherTotalPlaybackPage(page)
      const breakdownAnswerPage = new BreakdownAnswerPage(page)
      const submitPage = new SubmitPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('12')
      await totalAnswerPage.submit().click()

      await answerBothBreakdownQuestions(page, ['3', '3', '3', '3'], ['2', '2', '1', '1'])

      await anotherTotalPlaybackPage.submit().click()

      await submitPage.totalAnswerEdit().click()
      await totalAnswerPage.total().fill('15')
      await totalAnswerPage.submit().click()

      await answerAndSubmitBreakdownQuestion(page, '0', '3', '3', '3')

      await expect(breakdownAnswerPage.errorNumber(1)).toBeVisible()

      await expect(breakdownAnswerPage.errorNumber(1)).toHaveText('Enter answers that add up to 15')

      await answerBothBreakdownQuestions(page, ['5', '4', '4', '2'], ['3', '3', '2', '1'])

      await expect(page).toHaveURL(new RegExp(anotherTotalPlaybackPage.pageName))
    })
  })

  test.describe('Given I completed both grouped answer validation questions and I am on the summary', () => {
    test('When I go back from the summary and change the first breakdown question answers so its total changes, Then I must reconfirm the second breakdown question based on calculated summary value source with valid answers before I can continue', async ({
      page
    }) => {
      const anotherTotalPlaybackPage = new AnotherTotalPlaybackPage(page)
      const secondBreakdownAnswerPage = new SecondBreakdownAnswerPage(page)
      const submitPage = new SubmitPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      const totalPlaybackPage = new TotalPlaybackPage(page)
      await totalAnswerPage.total().fill('12')
      await totalAnswerPage.submit().click()

      await answerBothBreakdownQuestions(page, ['3', '3', '3', '3'], ['2', '2', '1', '1'])

      await anotherTotalPlaybackPage.submit().click()

      await submitPage.breakdown1Edit().click()

      await answerAndSubmitBreakdownQuestion(page, '6', '3', '2', '1')

      await totalPlaybackPage.submit().click()

      await secondBreakdownAnswerPage.submit().click()

      await expect(secondBreakdownAnswerPage.errorNumber(1)).toBeVisible()

      await expect(secondBreakdownAnswerPage.errorNumber(1)).toHaveText('Enter answers that add up to 9')

      await answerAndSubmitSecondBreakdownQuestion(page, '5', '4', '0', '0')

      await expect(secondBreakdownAnswerPage.errorNumber(1)).not.toBeVisible()

      await expect(page).toHaveURL(new RegExp(anotherTotalPlaybackPage.pageName))
    })
  })

  test.describe('Given I start a grouped answer validation survey and enter 5 into the total', () => {
    test('When I continue and enter 3 in each breakdown field, Then I should see a validation error', async ({ page }) => {
      const breakdownAnswerPage = new BreakdownAnswerPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('5')
      await totalAnswerPage.submit().click()

      await answerAndSubmitBreakdownQuestion(page, '3', '3', '3', '3')

      await expect(breakdownAnswerPage.errorNumber(1)).toHaveText('Enter answers that add up to 5')
    })
  })

  test.describe('Given I start a grouped answer validation survey and enter 5 into the total', () => {
    test('When I enter 3 in each breakdown field and continue to second breakdown and enter 3 in each field, Then I should see a validation error', async ({
      page
    }) => {
      const secondBreakdownAnswerPage = new SecondBreakdownAnswerPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      await totalAnswerPage.total().fill('5')
      await totalAnswerPage.submit().click()

      await answerBothBreakdownQuestions(page, ['2', '1', '1', '1'], ['3', '3', '3', '3'])

      await expect(secondBreakdownAnswerPage.errorNumber(1)).toHaveText('Enter answers that add up to 3')
    })
  })

  test.describe('Given I edit a question from a Calculated Summary page', () => {
    test('When I change the answer and there is a question that needs to be revisited before I can return to the Calculated Summary Page, Then I revisit the relevant page before I route back to the Calculated Summary page', async ({
      page
    }) => {
      const anotherTotalPlaybackPage = new AnotherTotalPlaybackPage(page)
      const breakdownAnswerPage = new BreakdownAnswerPage(page)
      const secondBreakdownAnswerPage = new SecondBreakdownAnswerPage(page)
      const submitPage = new SubmitPage(page)
      const totalAnswerPage = new TotalAnswerPage(page)
      const totalPlaybackPage = new TotalPlaybackPage(page)
      await totalAnswerPage.total().fill('5')
      await totalAnswerPage.submit().click()

      await answerBothBreakdownQuestions(page, ['2', '1', '1', '1'], ['1', '2', '0', '0'])

      await anotherTotalPlaybackPage.breakdown1Edit().click()

      await breakdownAnswerPage.breakdown1().fill('1')
      await breakdownAnswerPage.breakdown2().fill('2')

      await breakdownAnswerPage.submit().click()

      await totalPlaybackPage.previous().click()

      await breakdownAnswerPage.submit().click()

      await totalPlaybackPage.submit().click()

      await secondBreakdownAnswerPage.submit().click()

      await anotherTotalPlaybackPage.submit().click()

      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    })
  })
})
