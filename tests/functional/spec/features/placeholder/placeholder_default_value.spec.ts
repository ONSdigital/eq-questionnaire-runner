import { test, expect } from '../../../fixtures/test'
import EmployeesNumberBlockPage from '../../../generated_pages/placeholder_default_value/employees-number-block.page'
import EmployeesTrainingBlockPage from '../../../generated_pages/placeholder_default_value/employees-training-block.page'
import EmployeesNumberInterstitialPage from '../../../generated_pages/placeholder_default_value/employees-number-interstitial.page'

test.describe('Placeholder default value check', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_placeholder_default_value.json')
  })

  test('Given a question with default answer, When I do not enter any number and click submit, Then the interstitial page shows default employees number as ', async ({
    page
  }) => {
    const employeesNumberBlockPage = new EmployeesNumberBlockPage(page)
    await employeesNumberBlockPage.submit().click()
    await expect(page.locator('#main-content > p')).toContainText('The total number of employees confirmed are 0')
  })

  test('Given a question with default answer, When I enter a number of employee and click submit, Then the interstitial page shows me the employees number entered', async ({
    page
  }) => {
    const employeesNumberBlockPage = new EmployeesNumberBlockPage(page)
    await employeesNumberBlockPage.employeesNo().fill('54')
    await employeesNumberBlockPage.submit().click()
    await expect(page.locator('#main-content > p')).toContainText('The total number of employees confirmed are 54')
  })

  test('Given a training budget question with default answer, When I do not enter any amount and click submit, Then the interstitial page shows default amount as 250.', async ({
    page
  }) => {
    const employeesNumberBlockPage = new EmployeesNumberBlockPage(page)
    const employeesNumberInterstitialPage = new EmployeesNumberInterstitialPage(page)
    const employeesTrainingBlockPage = new EmployeesTrainingBlockPage(page)
    await employeesNumberBlockPage.submit().click()
    await employeesNumberInterstitialPage.submit().click()
    await employeesTrainingBlockPage.submit().click()
    await expect(page.locator('#main-content > p')).toHaveText('The average training budget per employee is £250.00')
  })

  test('Given a training budget question with default answer, When I enter an amount and click submit, Then the interstitial page shows amount entered', async ({
    page
  }) => {
    const employeesNumberBlockPage = new EmployeesNumberBlockPage(page)
    const employeesNumberInterstitialPage = new EmployeesNumberInterstitialPage(page)
    const employeesTrainingBlockPage = new EmployeesTrainingBlockPage(page)
    await employeesNumberBlockPage.submit().click()
    await employeesNumberInterstitialPage.submit().click()
    await employeesTrainingBlockPage.employeesAvgTraining().fill('100')
    await employeesTrainingBlockPage.submit().click()
    await expect(page.locator('#main-content > p')).toHaveText('The average training budget per employee is £100.00')
  })
})
