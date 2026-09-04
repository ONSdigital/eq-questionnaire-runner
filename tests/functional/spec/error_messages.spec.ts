import { test, expect } from '../fixtures/test'
import AboutYou from '../generated_pages/multiple_answers/about-you-block.page'
import BlockPage from '../generated_pages/percentage/block.page'

async function answerAllButOne (aboutYou: AboutYou): Promise<void> {
  await aboutYou.textfield().fill('John Doe')
  await aboutYou.dateDay().fill('1')
  await aboutYou.dateMonth().fill('1')
  await aboutYou.dateYear().fill('1995')
  await aboutYou.checkboxBmw().click()
  await aboutYou.radioYes().click()
  await aboutYou.currency().fill('50000')
  await aboutYou.monthYearDateMonth().fill('10')
  await aboutYou.monthYearDateYear().fill('2021')
  await aboutYou.dropdown().selectOption('Silver')
  await aboutYou.unit().fill('10000')
  await aboutYou.durationMonths().fill('3')
  await aboutYou.durationYears().fill('3')
  await aboutYou.yearDateYear().fill('2019')
  await aboutYou.number().fill('5')
  await aboutYou.percentage().fill('3')
  await aboutYou.mobileNumber().fill('07700900111')
}

test.describe('Error Messages', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_multiple_answers.json')
  })

  test('Given a question has errors, When errors are displayed, Then the error messages are correct', async ({ page }) => {
    const aboutYou = new AboutYou(page)
    const errorMessageMap = new Map<number, string>([
      [1, 'Enter an answer'],
      [2, 'Enter a date'],
      [3, 'Select at least one answer'],
      [4, 'Select an answer'],
      [5, 'Enter an answer'],
      [6, 'Enter a date'],
      [7, 'Select an answer'],
      [8, 'Enter an answer'],
      [9, 'Enter a duration'],
      [10, 'Enter a date'],
      [11, 'Enter an answer'],
      [12, 'Enter an answer'],
      [13, 'Enter a UK mobile number'],
      [14, 'Enter an answer']
    ])

    await aboutYou.submit().click()
    await expect(aboutYou.errorHeader()).toHaveText('There are 14 problems with your answer')

    for (const [index, errorMessage] of errorMessageMap) {
      await expect(aboutYou.errorNumber(index)).toContainText(errorMessage)
    }
  })

  test('Given a question has errors, When errors are displayed, Then the error message for each answer is correct', async ({ page }) => {
    const aboutYou = new AboutYou(page)
    await aboutYou.submit().click()

    await expect(aboutYou.textfieldErrorItem()).toHaveText('Enter an answer')
    await expect(aboutYou.dateErrorItem()).toHaveText('Enter a date')
    await expect(aboutYou.checkboxErrorItem()).toContainText('Select at least one answer')
    await expect(aboutYou.radioErrorItem()).toContainText('Select an answer')
    await expect(aboutYou.currencyErrorItem()).toHaveText('Enter an answer')
    await expect(aboutYou.monthYearDateErrorItem()).toHaveText('Enter a date')
    await expect(aboutYou.dropdownErrorItem()).toHaveText('Select an answer')
    await expect(aboutYou.unitErrorItem()).toHaveText('Enter an answer')
    await expect(aboutYou.durationErrorItem()).toHaveText('Enter a duration')
    await expect(aboutYou.yearDateErrorItem()).toHaveText('Enter a date')
    await expect(aboutYou.numberErrorItem()).toHaveText('Enter an answer')
    await expect(aboutYou.percentageErrorItem()).toHaveText('Enter an answer')
    await expect(aboutYou.mobileNumberErrorItem()).toHaveText('Enter a UK mobile number')
    await expect(aboutYou.textareaErrorItem()).toHaveText('Enter an answer')
  })

  test('Given a question has multiple errors, When the errors are displayed, Then the error messages are in a numbered list', async ({ page }) => {
    const aboutYou = new AboutYou(page)
    await aboutYou.submit().click()
    await expect(aboutYou.errorList()).toBeVisible()
  })

  test("Given a question has 1 error, When the error is displayed, Then error message isn't in a numbered list", async ({ page }) => {
    const aboutYou = new AboutYou(page)
    await answerAllButOne(aboutYou)

    await aboutYou.submit().click()
    await expect(aboutYou.singleErrorLink()).toBeVisible()
  })

  test('Given a question has 1 error, When the error is displayed, Then error header is correct', async ({ page }) => {
    const aboutYou = new AboutYou(page)
    await answerAllButOne(aboutYou)

    await aboutYou.submit().click()
    await expect(aboutYou.errorHeader()).toHaveText('There is a problem with your answer')
  })

  test('Given a question has errors, When an error message is clicked, Then the correct answer is focused', async ({ page }) => {
    const aboutYou = new AboutYou(page)
    await aboutYou.submit().click()

    await aboutYou.errorNumber(1).click()
    await expect(aboutYou.textfield()).toBeFocused()

    await aboutYou.errorNumber(2).click()
    await expect(aboutYou.dateDay()).toBeFocused()

    await aboutYou.errorNumber(3).click()
    await expect(aboutYou.checkboxBmw()).toBeFocused()

    await aboutYou.errorNumber(4).click()
    await expect(aboutYou.radioYes()).toBeFocused()

    await aboutYou.errorNumber(5).click()
    await expect(aboutYou.currency()).toBeFocused()

    await aboutYou.errorNumber(6).click()
    await expect(aboutYou.monthYearDateMonth()).toBeFocused()

    await aboutYou.errorNumber(7).click()
    await expect(aboutYou.dropdown()).toBeFocused()

    await aboutYou.errorNumber(8).click()
    await expect(aboutYou.unit()).toBeFocused()

    await aboutYou.errorNumber(9).click()
    await expect(aboutYou.durationYears()).toBeFocused()

    await aboutYou.errorNumber(10).click()
    await expect(aboutYou.yearDateYear()).toBeFocused()

    await aboutYou.errorNumber(11).click()
    await expect(aboutYou.number()).toBeFocused()

    await aboutYou.errorNumber(12).click()
    await expect(aboutYou.percentage()).toBeFocused()

    await aboutYou.errorNumber(13).click()
    await expect(aboutYou.mobileNumber()).toBeFocused()

    await aboutYou.errorNumber(14).click()
    await expect(aboutYou.textarea()).toBeFocused()
  })
})

test.describe('Error Message NaN value', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_percentage.json')
  })

  test('Given a NaN value was entered on percentage question, When the error is displayed, Then the error message is correct', async ({ page }) => {
    const blockPage = new BlockPage(page)
    await blockPage.answer().fill('NaN')
    await blockPage.submit().click()
    await expect(blockPage.errorHeader()).toHaveText('There is a problem with your answer')
    await expect(blockPage.answerErrorItem()).toHaveText('Enter a number')
  })

  test('Given a NaN value with separators was entered on percentage question, When the error is displayed, Then the error message is correct', async ({
    page
  }) => {
    const blockPage = new BlockPage(page)
    await blockPage.answer().fill(',NaN_')
    await blockPage.submit().click()
    await expect(blockPage.errorHeader()).toHaveText('There is a problem with your answer')
    await expect(blockPage.answerErrorItem()).toHaveText('Enter a number')
  })
})
