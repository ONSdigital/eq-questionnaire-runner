import { test, expect } from '../../../fixtures/test'

import AddressConfirmation from '../../../generated_pages/address/address-confirmation.page'
import AddressMandatory from '../../../generated_pages/address/address-block-mandatory.page'
import AddressOptional from '../../../generated_pages/address/address-block-optional.page'
import SubmitPage from '../../../generated_pages/address/submit.page'

test.describe('Address Answer Type', () => {
  test.beforeEach(async ({ openQuestionnaire }) => {
    await openQuestionnaire('test_address.json')
  })

  test.describe('Given the user is on an address input question', () => {
    test('When the user enters all address fields, Then the summary displays the address fields', async ({ page }) => {
      const addressConfirmation = new AddressConfirmation(page)
      const addressMandatory = new AddressMandatory(page)
      const addressOptional = new AddressOptional(page)
      const submitPage = new SubmitPage(page)
      await addressMandatory.line1().fill('Evelyn Street')
      await addressMandatory.line2().fill('Apt 7')
      await addressMandatory.town().fill('Barry')
      await addressMandatory.postcode().fill('CF63 4JG')

      await addressMandatory.submit().click()
      await addressOptional.submit().click()
      await addressConfirmation.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))

      await expect(submitPage.addressMandatory().locator('br')).toHaveCount(3)
      await expect(submitPage.addressMandatory()).toHaveText(/Evelyn Street\s*Apt 7\s*Barry\s*CF63 4JG/)
    })
  })

  test.describe('Given the user is on an address input question', () => {
    test('When the user enters only address line 1, Then the summary only displays address line 1', async ({ page }) => {
      const addressConfirmation = new AddressConfirmation(page)
      const addressMandatory = new AddressMandatory(page)
      const addressOptional = new AddressOptional(page)
      const submitPage = new SubmitPage(page)
      await addressMandatory.line1().fill('Evelyn Street')

      await addressMandatory.submit().click()
      await addressOptional.submit().click()
      await addressConfirmation.submit().click()
      await expect(page).toHaveURL(new RegExp(submitPage.pageName))
      await expect(submitPage.addressMandatory()).toHaveText('Evelyn Street')
    })
  })

  test.describe('Given the user is on an mandatory address input question', () => {
    test('When the user submits the page without entering address line 1, Then an error is displayed', async ({ page }) => {
      const addressMandatory = new AddressMandatory(page)
      await addressMandatory.submit().click()
      await expect(addressMandatory.error()).toHaveText('Enter an address')
    })
  })

  test.describe('Given the user is on an optional address input question', () => {
    test('When the user submits the page without entering any fields, Then the summary should display `No answer provided`.', async ({ page }) => {
      const addressConfirmation = new AddressConfirmation(page)
      const addressMandatory = new AddressMandatory(page)
      const addressOptional = new AddressOptional(page)
      const submitPage = new SubmitPage(page)
      // Get to optional address question
      await addressMandatory.line1().fill('Evelyn Street')
      await addressMandatory.submit().click()

      await addressOptional.submit().click()
      await addressConfirmation.submit().click()
      await expect(submitPage.addressOptional()).toHaveText('No answer provided')
    })
  })

  test.describe('Given the user has submitted an address answer type question', () => {
    test('When the user revisits the address question page, Then all entered fields are filled in', async ({ page }) => {
      const addressMandatory = new AddressMandatory(page)
      const addressOptional = new AddressOptional(page)
      await addressMandatory.line1().fill('Evelyn Street')
      await addressMandatory.line2().fill('Apt 7')
      await addressMandatory.town().fill('Barry')
      await addressMandatory.postcode().fill('CF63 4JG')

      await addressMandatory.submit().click()
      await expect(page).toHaveURL(new RegExp(addressOptional.pageName))

      await page.goto(addressMandatory.url())

      await expect(addressMandatory.line1()).toHaveValue('Evelyn Street')
      await expect(addressMandatory.line2()).toHaveValue('Apt 7')
      await expect(addressMandatory.town()).toHaveValue('Barry')
      await expect(addressMandatory.postcode()).toHaveValue('CF63 4JG')
    })
  })

  test.describe('Given the user has submitted an address answer type question', () => {
    test('When the user visits the address confirmation question page, Then the first line of the address is displayed', async ({ page }) => {
      const addressConfirmation = new AddressConfirmation(page)
      const addressMandatory = new AddressMandatory(page)
      const addressOptional = new AddressOptional(page)
      await addressMandatory.line1().fill('Evelyn Street')
      await addressMandatory.line2().fill('Apt 7')
      await addressMandatory.town().fill('Barry')
      await addressMandatory.postcode().fill('CF63 4JG')
      await addressMandatory.submit().click()
      await addressOptional.submit().click()
      await expect(addressConfirmation.questionText()).toHaveText('Please confirm the first line of your address is Evelyn Street')
    })
  })
})
