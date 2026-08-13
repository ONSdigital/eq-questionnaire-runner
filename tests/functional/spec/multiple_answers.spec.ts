import { test, expect } from '../fixtures/test'
import AboutYou from '../generated_pages/multiple_answers/about-you-block.page'
import AgeBlock from '../generated_pages/multiple_answers/age-block.page'
import SubmitPage from '../generated_pages/multiple_answers/submit.page'

async function answerAllQuestions (aboutYou: AboutYou, ageBlock: AgeBlock): Promise<void> {
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
  await aboutYou.textarea().fill('Fuel type petrol')
  await aboutYou.submit().click()

  await ageBlock.age().fill('10')
  await ageBlock.ageEstimateThisAgeIsAnEstimate().click()
  await ageBlock.submit().click()
}

test.describe('Multiple Answers', () => {
  test.describe('Given I have completed a questionnaire that has multiple answers per question', () => {
    test.beforeEach('Load the questionnaire and answer all questions', async ({ page, openQuestionnaire }) => {
      const aboutYou = new AboutYou(page)
      const ageBlock = new AgeBlock(page)
      await openQuestionnaire('test_multiple_answers.json')
      await answerAllQuestions(aboutYou, ageBlock)
    })

    test('When I am on the summary, Then all answers are displayed', async ({ page }) => {
      const submitPage = new SubmitPage(page)
      await expect(submitPage.textfieldAnswer()).toHaveText('John Doe')
      await expect(submitPage.dateAnswer()).toHaveText('1 January 1995')
      await expect(submitPage.checkboxAnswer()).toHaveText('BMW')
      await expect(submitPage.radioAnswer()).toHaveText('Yes')
      await expect(submitPage.currencyAnswer()).toHaveText('£50,000.00')
      await expect(submitPage.monthYearDateAnswer()).toHaveText('October 2021')
      await expect(submitPage.dropdownAnswer()).toHaveText('Silver')
      await expect(submitPage.unitAnswer()).toHaveText('10,000 mi')
      await expect(submitPage.durationAnswer()).toHaveText('3 years 3 months')
      await expect(submitPage.yearDateAnswer()).toHaveText('2019')
      await expect(submitPage.numberAnswer()).toHaveText('5')
      await expect(submitPage.percentageAnswer()).toHaveText('3%')
      await expect(submitPage.mobileNumberAnswer()).toHaveText('07700900111')
      await expect(submitPage.textareaAnswer()).toHaveText('Fuel type petrol')

      await expect(submitPage.ageAnswer()).toHaveText('10')
      await expect(submitPage.ageEstimateAnswer()).toHaveText('This age is an estimate')
    })

    test("When I click 'Change' an answer, Then I should be taken to the correct page and the answer input should be focused", async ({ page }) => {
      const aboutYou = new AboutYou(page)
      const submitPage = new SubmitPage(page)
      await submitPage.currencyAnswerEdit().click()
      await expect(page).toHaveURL(new RegExp(aboutYou.url()))
      await expect(page).toHaveURL(/\/questionnaire\/about-you-block\/\?.*#currency-answer/)
      await expect(aboutYou.currency()).toBeFocused()
    })
  })

  test.describe('Given I have launched a questionnaire that has multiple answers per question', () => {
    test.beforeEach('Load the questionnaire', async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_multiple_answers.json')
    })

    test('When I am on the question page, Then all answers should have a label/legend', async ({ page }) => {
      const aboutYou = new AboutYou(page)
      await expect(aboutYou.dateLegend()).toHaveText('What is your date of birth?')
      await expect(aboutYou.monthYearDateLegend()).toHaveText('When would you like the car by?')
      await expect(aboutYou.radioLegend()).toHaveText('Would you like the sports package?')
      await expect(aboutYou.durationLegend()).toHaveText('How long have you had your licence?')
      await expect(aboutYou.checkboxLegend()).toHaveText('What are your favourite car brands?')
      await expect(aboutYou.textfieldLabel()).toHaveText('Your name')
      await expect(aboutYou.currencyLabel()).toHaveText('What is your budget?')
      await expect(aboutYou.dropdownLabel()).toHaveText('Select a colour')
      await expect(aboutYou.unitLabel()).toHaveText('Max mileage')
      await expect(aboutYou.numberLabel()).toHaveText('How many seats?')
      await expect(aboutYou.percentageLabel()).toHaveText('Max CO2 emissions')
      await expect(aboutYou.mobileNumberLabel()).toHaveText('What is your mobile number?')
      await expect(aboutYou.textareaLabel()).toHaveText('Other comments')
    })
  })
})
