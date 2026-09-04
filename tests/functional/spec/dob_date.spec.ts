import { test, expect } from '../fixtures/test'
import DateOfBirthPage from '../generated_pages/dob_date/date-of-birth.page'
import UnderSixteenPage from '../generated_pages/dob_date/under-sixteen.page'

test.describe('Date of birth check', () => {
  test.beforeEach('Load the survey', async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_dob_date.json')
  })

  test('Given I am completing a date question, When I enter a value less than 16 years, Then I am routed to under 16 page', async ({ page }) => {
    const dateOfBirthPage = new DateOfBirthPage(page)
    const underSixteenPage = new UnderSixteenPage(page)
    await dateOfBirthPage.day().fill('12')
    await dateOfBirthPage.month().fill('4')
    await dateOfBirthPage.year().fill('2021')
    await dateOfBirthPage.submit().click()
    await expect(underSixteenPage.legend()).toHaveText('You are under 16!')
  })

  test('Given I am completing a date question, When I enter a value less than 16 years, Then I am routed to over 16 page', async ({ page }) => {
    const dateOfBirthPage = new DateOfBirthPage(page)
    const underSixteenPage = new UnderSixteenPage(page)
    await dateOfBirthPage.day().fill('12')
    await dateOfBirthPage.month().fill('4')
    await dateOfBirthPage.year().fill('1980')
    await dateOfBirthPage.submit().click()
    await expect(underSixteenPage.legend()).toHaveText('You are over 16!')
  })
})
