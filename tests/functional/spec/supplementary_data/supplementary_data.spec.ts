import { test, expect, type BrowserContext, type Page, type OpenQuestionnaire, createOpenQuestionnaire } from '../../fixtures/test'
import { getRandomString } from '../../jwt_helper'
import LoadedSuccessfullyBlockPage from '../../generated_pages/supplementary_data/loaded-successfully-block.page'
import IntroductionBlockPage from '../../generated_pages/supplementary_data/introduction-block.page'
import HubPage from '../../base_pages/hub.page'
import EmailBlockPage from '../../generated_pages/supplementary_data/email-block.page'
import TradingPage from '../../generated_pages/supplementary_data/trading.page'
import SalesBreakdownBlockPage from '../../generated_pages/supplementary_data/sales-breakdown-block.page'
import CalculatedSummarySalesPage from '../../generated_pages/supplementary_data/calculated-summary-sales.page'
import Section1InterstitialPage from '../../generated_pages/supplementary_data/section-1-interstitial.page'
import Section1Page from '../../generated_pages/supplementary_data/section-1-summary.page'
import AnyAdditionalEmployeesPage from '../../generated_pages/supplementary_data/any-additional-employees.page'
import ListCollectorAdditionalPage from '../../generated_pages/supplementary_data/list-collector-additional.page'
import AddAdditionalEmployeePage from '../../generated_pages/supplementary_data/list-collector-additional-add.page'
import Section3Page from '../../generated_pages/supplementary_data/section-3-summary.page'
import ListCollectorEmployeesPage from '../../generated_pages/supplementary_data/list-collector-employees.page'
import NewEmailPage from '../../generated_pages/supplementary_data/new-email.page'
import LengthOfEmploymentPage from '../../generated_pages/supplementary_data/length-of-employment.page'
import Section4Page from '../../generated_pages/supplementary_data/section-4-summary.page'
import AdditionalLengthOfEmploymentPage from '../../generated_pages/supplementary_data/additional-length-of-employment.page'
import Section5Page from '../../generated_pages/supplementary_data/section-5-summary.page'
import ListCollectorProductsPage from '../../generated_pages/supplementary_data/list-collector-products.page'
import ProductRepeatingBlock1Page from '../../generated_pages/supplementary_data/product-repeating-block-1-repeating-block.page'
import CalculatedSummaryVolumeSalesPage from '../../generated_pages/supplementary_data/calculated-summary-volume-sales.page'
import CalculatedSummaryVolumeTotalPage from '../../generated_pages/supplementary_data/calculated-summary-volume-total.page'
import DynamicProductsPage from '../../generated_pages/supplementary_data/dynamic-products.page'
import CalculatedSummaryValueSalesPage from '../../generated_pages/supplementary_data/calculated-summary-value-sales.page'
import Section6Page from '../../generated_pages/supplementary_data/section-6-summary.page'
import ProductVolumeInterstitialPage from '../../generated_pages/supplementary_data/product-volume-interstitial.page'
import ProductSalesInterstitialPage from '../../generated_pages/supplementary_data/product-sales-interstitial.page'
import ProductQuestion3EnabledPage from '../../generated_pages/supplementary_data/product-question-3-enabled.page'
import ThankYouPage from '../../base_pages/thank-you.page'
import ViewSubmittedResponsePage from '../../generated_pages/supplementary_data/view-submitted-response.page'
import { listItemComplete } from '../../helpers'

test.describe('Using supplementary data', () => {
  test.describe.configure({ mode: 'serial' })
  const supplementaryDataSchema = 'test_supplementary_data.json'
  const responseId = getRandomString(16)
  const summaryItems = '.ons-summary__item--text'
  const summaryValues = '.ons-summary__values'
  const summaryRowTitles = '.ons-summary__row-title'

  let context: BrowserContext
  let page: Page
  let openQuestionnaire: OpenQuestionnaire

  test.beforeAll(async ({ browser }) => {
    context = await browser.newContext()
    page = await context.newPage()
    openQuestionnaire = createOpenQuestionnaire(page)
    await openQuestionnaire(supplementaryDataSchema, { sdsDatasetId: '203b2f9d-c500-8175-98db-86ffcfdccfa3', responseId })
  })

  test.afterAll(async () => {
    await context.close()
  })

  test('Given I launch a survey using supplementary data, When I am outside a repeating section, Then I am able to see the list of items relating to a given supplementary data list item on the page', async () => {
    await expect(page.locator('#main-content #guidance-1')).toContainText('The surnames of the employees are: Potter, Kent.')
    await expect(page.locator('#main-content li').nth(0)).toHaveText('Articles and equipment for sports or outdoor games')
    await expect(page.locator('#main-content li').nth(1)).toHaveText('Kitchen Equipment')
  })

  test('Given I progress through the interstitial block, When I begin the introduction block, Then I see the supplementary data piped in', async () => {
    const loadedSuccessfullyBlockPage = new LoadedSuccessfullyBlockPage(page)
    const hubPage = new HubPage(page)
    const introductionBlockPage = new IntroductionBlockPage(page)
    const emailBlockPage = new EmailBlockPage(page)
    await loadedSuccessfullyBlockPage.submit().click()
    await introductionBlockPage.acceptCookies().click()
    await expect(introductionBlockPage.businessDetailsContent()).toContainText('You are completing this survey for Tesco')
    await expect(introductionBlockPage.businessDetailsContent()).toContainText(
      'If the company details or structure have changed contact us on 01171231231'
    )
    await expect(introductionBlockPage.guidancePanel(1)).toContainText('Some supplementary guidance about the survey')
    await introductionBlockPage.submit().click()
    await hubPage.submit().click()
    await emailBlockPage.yes().click()
    await emailBlockPage.submit().click()
  })

  test('Given I have dynamic answer options based off a supplementary date value, When I reach the block using them, Then I see a correct list of options to choose from', async () => {
    const tradingPage = new TradingPage(page)

    await expect(page).toHaveURL(new RegExp(tradingPage.pageName))
    await expect(tradingPage.answerLabelByIndex(0)).toHaveText('Thursday 27 November 1947')
    await expect(tradingPage.answerLabelByIndex(1)).toContainText('Friday 28 November 1947')
    await expect(tradingPage.answerLabelByIndex(2)).toContainText('Saturday 29 November 1947')
    await expect(tradingPage.answerLabelByIndex(3)).toContainText('Sunday 30 November 1947')
    await expect(tradingPage.answerLabelByIndex(4)).toContainText('Monday 1 December 1947')
    await expect(tradingPage.answerLabelByIndex(5)).toContainText('Tuesday 2 December 1947')
    await expect(tradingPage.answerLabelByIndex(6)).toContainText('Wednesday 3 December 1947')

    await tradingPage.answerByIndex(3).click()
    await tradingPage.submit().click()
  })

  test('Given I have a calculated question validated against a supplementary data value, When I enter a breakdown that exceeds the total, Then I see an error message', async () => {
    const salesBreakdownBlockPage = new SalesBreakdownBlockPage(page)

    await salesBreakdownBlockPage.salesBristol().fill('333000')
    await salesBreakdownBlockPage.salesLondon().fill('444000')
    await salesBreakdownBlockPage.submit().click()

    await expect(salesBreakdownBlockPage.errorNumber(1)).toContainText('Enter answers that add up to or are less than 555,000')
  })

  test('Given I have a calculated question validated against a supplementary data value, When I enter a breakdown less than the total, Then I see a calculated summary page with the sum of my previous answers', async () => {
    const salesBreakdownBlockPage = new SalesBreakdownBlockPage(page)
    const calculatedSummarySalesPage = new CalculatedSummarySalesPage(page)

    await salesBreakdownBlockPage.salesLondon().fill('111000')
    await salesBreakdownBlockPage.submit().click()

    await expect(calculatedSummarySalesPage.calculatedSummaryTitle()).toHaveText(
      'Total value of sales from Bristol and London is calculated to be £444,000.00. Is this correct?'
    )
  })

  test('Given I have an interstitial block with all answers and supplementary data, When I reach this block, Then I see the placeholders rendered correctly', async () => {
    const section1InterstitialPage = new Section1InterstitialPage(page)
    const calculatedSummarySalesPage = new CalculatedSummarySalesPage(page)

    await calculatedSummarySalesPage.submit().click()

    await expect(section1InterstitialPage.questionText()).toContainText('Summary of information provided for Tesco')

    const body = page.locator('body')
    await expect(body).toContainText('Telephone Number: 01171231231')
    await expect(body).toContainText('Email: contact@tesco.org')
    await expect(body).toContainText('Note Title: Value of total sales')
    await expect(body).toContainText('Note Description: Total value of goods sold during the period of the return')
    await expect(body).toContainText('Note Example Title: Including')
    await expect(body).toContainText('Note Example Description: Sales across all UK stores')
    await expect(body).toContainText('Incorporation Date: 27 November 1947')
    await expect(body).toContainText('Trading start date: 30 November 1947')
    await expect(body).toContainText('Guidance: Some supplementary guidance about the survey')
    await expect(body).toContainText('Total Uk Sales: £555,000.00')
    await expect(body).toContainText('Bristol sales: £333,000.00')
    await expect(body).toContainText('London sales: £111,000.00')
    await expect(body).toContainText('Sum of Bristol and London sales: £444,000.00')
  })

  test('Given I have a section summary enabled, When I reach the section summary, Then I see it rendered correctly with supplementary data', async () => {
    const section1InterstitialPage = new Section1InterstitialPage(page)
    const section1Page = new Section1Page(page)

    await section1InterstitialPage.submit().click()

    await expect(section1Page.emailQuestion()).toHaveText('Is contact@tesco.org still the correct contact email for Tesco?')
    await expect(section1Page.sameEmailAnswer()).toHaveText('Yes')
    await expect(section1Page.tradingQuestion()).toHaveText('When did Tesco begin trading?')
    await expect(section1Page.tradingAnswer()).toHaveText('Sunday 30 November 1947')
    await expect(page.locator('.ons-summary__row-title').nth(0)).toHaveText('How much of the £555,000.00 total UK sales was from Bristol and London?')
    await expect(section1Page.salesBristolAnswer()).toHaveText('£333,000.00')
    await expect(section1Page.salesLondonAnswer()).toHaveText('£111,000.00')
  })

  test('Given I add an answer used in a first non empty item transform with supplementary data, When I return to the interstitial block, Then I see the transform value has updated', async () => {
    const section1Page = new Section1Page(page)
    const emailBlockPage = new EmailBlockPage(page)
    const newEmailPage = new NewEmailPage(page)
    const section1InterstitialPage = new Section1InterstitialPage(page)

    await section1Page.sameEmailAnswerEdit().click()
    await emailBlockPage.no().click()
    await emailBlockPage.submit().click()
    await newEmailPage.answer().fill('new.contact@gmail.com')
    await newEmailPage.submit().click()
    await section1Page.previous().click()

    await expect(page.locator('body')).toContainText('Email: new.contact@gmail.com')

    await section1InterstitialPage.submit().click()
    await section1Page.submit().click()
  })

  test('Given I have a list collector content block using a supplementary list, When I start the section, I see the supplementary list items in the list', async () => {
    const hubPage = new HubPage(page)
    const listCollectorEmployeesPage = new ListCollectorEmployeesPage(page)

    await hubPage.submit().click()
    await expect(listCollectorEmployeesPage.listLabel(1)).toHaveText('Harry Potter')
    await expect(listCollectorEmployeesPage.listLabel(2)).toHaveText('Clark Kent')
    await listCollectorEmployeesPage.submit().click()
  })

  test('Given I add some additional employees via another list collector, When I return to the Hub, Then I see new enabled sections for the supplementary list items and my added ones', async () => {
    const hubPage = new HubPage(page)
    const anyAdditionalEmployeesPage = new AnyAdditionalEmployeesPage(page)
    const addAdditionalEmployeePage = new AddAdditionalEmployeePage(page)
    const listCollectorAdditionalPage = new ListCollectorAdditionalPage(page)
    const section3Page = new Section3Page(page)

    await hubPage.submit().click()
    await anyAdditionalEmployeesPage.yes().click()
    await anyAdditionalEmployeesPage.submit().click()

    await addAdditionalEmployeePage.employeeFirstName().fill('Jane')
    await addAdditionalEmployeePage.employeeLastName().fill('Doe')
    await addAdditionalEmployeePage.submit().click()

    await listCollectorAdditionalPage.yes().click()
    await listCollectorAdditionalPage.submit().click()

    await addAdditionalEmployeePage.employeeFirstName().fill('John')
    await addAdditionalEmployeePage.employeeLastName().fill('Smith')
    await addAdditionalEmployeePage.submit().click()

    await listCollectorAdditionalPage.no().click()
    await listCollectorAdditionalPage.submit().click()

    await section3Page.submit().click()

    await expect(hubPage.summaryRowTitle('section-4-1')).toContainText('Harry Potter')
    await expect(hubPage.summaryRowTitle('section-4-2')).toContainText('Clark Kent')
    await expect(hubPage.summaryRowTitle('section-5-1')).toContainText('Jane Doe')
    await expect(hubPage.summaryRowTitle('section-5-2')).toContainText('John Smith')

    await hubPage.submit().click()
  })

  test('Given I have repeating sections for both supplementary and dynamic list items, When I start a repeating section for a supplementary list item, Then I see static supplementary data correctly piped in', async () => {
    const lengthOfEmploymentPage = new LengthOfEmploymentPage(page)

    await expect(lengthOfEmploymentPage.questionTitle()).toContainText('When did Harry Potter start working for Tesco?')
    await expect(lengthOfEmploymentPage.employmentStartLegend()).toContainText('Start date at Tesco')
  })

  test('Given I have validation on the start date in the repeating section, When I enter a date before the incorporation date, Then I see an error message', async () => {
    const lengthOfEmploymentPage = new LengthOfEmploymentPage(page)

    await lengthOfEmploymentPage.day().fill('1')
    await lengthOfEmploymentPage.month().fill('1')
    await lengthOfEmploymentPage.year().fill('1930')
    await lengthOfEmploymentPage.submit().click()

    await expect(lengthOfEmploymentPage.singleErrorLink()).toHaveText('Enter a date after 26 November 1947')
  })

  test('Given I have validation on the start date in the repeating section, When I enter a date after the incorporation date, Then I see that date on the summary page for the section', async () => {
    const lengthOfEmploymentPage = new LengthOfEmploymentPage(page)
    const section4Page = new Section4Page(page)

    await lengthOfEmploymentPage.year().fill('1990')
    await lengthOfEmploymentPage.submit().click()

    await expect(section4Page.lengthEmploymentQuestion()).toHaveText('When did Harry Potter start working for Tesco?')
    await expect(section4Page.employmentStart()).toHaveText('1 January 1990')
  })

  test('Given I complete the repeating section for another supplementary item, When I reach the summary page, Then I see the correct supplementary data with my answers', async () => {
    const section4Page = new Section4Page(page)
    const hubPage = new HubPage(page)
    const lengthOfEmploymentPage = new LengthOfEmploymentPage(page)

    await section4Page.submit().click()
    await hubPage.submit().click()

    await expect(lengthOfEmploymentPage.questionTitle()).toContainText('When did Clark Kent start working for Tesco?')
    await lengthOfEmploymentPage.day().fill('5')
    await lengthOfEmploymentPage.month().fill('6')
    await lengthOfEmploymentPage.year().fill('2011')
    await lengthOfEmploymentPage.submit().click()

    await expect(section4Page.lengthEmploymentQuestion()).toHaveText('When did Clark Kent start working for Tesco?')
    await expect(section4Page.employmentStart()).toHaveText('5 June 2011')
  })

  test('Given I move onto the dynamic list items, When I start a repeating section for a dynamic list item, Then I see static supplementary data correctly piped in and the same validation and summary', async () => {
    const section4Page = new Section4Page(page)
    const hubPage = new HubPage(page)
    const additionalLengthOfEmploymentPage = new AdditionalLengthOfEmploymentPage(page)
    const section5Page = new Section5Page(page)

    await section4Page.submit().click()
    await hubPage.submit().click()

    await expect(additionalLengthOfEmploymentPage.questionTitle()).toContainText('When did Jane Doe start working for Tesco?')
    await expect(additionalLengthOfEmploymentPage.additionalEmploymentStartLegend()).toHaveText('Start date at Tesco')

    await additionalLengthOfEmploymentPage.day().fill('1')
    await additionalLengthOfEmploymentPage.month().fill('1')
    await additionalLengthOfEmploymentPage.year().fill('1930')
    await additionalLengthOfEmploymentPage.submit().click()

    await expect(additionalLengthOfEmploymentPage.singleErrorLink()).toHaveText('Enter a date after 26 November 1947')

    await additionalLengthOfEmploymentPage.year().fill('2000')
    await additionalLengthOfEmploymentPage.submit().click()

    await expect(section5Page.additionalLengthEmploymentQuestion()).toHaveText('When did Jane Doe start working for Tesco?')
    await expect(section5Page.additionalEmploymentStart()).toHaveText('1 January 2000')

    await section5Page.submit().click()
    await hubPage.submit().click()

    await additionalLengthOfEmploymentPage.day().fill('3')
    await additionalLengthOfEmploymentPage.month().fill('3')
    await additionalLengthOfEmploymentPage.year().fill('2010')
    await additionalLengthOfEmploymentPage.submit().click()

    await expect(section5Page.additionalLengthEmploymentQuestion()).toHaveText('When did John Smith start working for Tesco?')
    await expect(section5Page.additionalEmploymentStart()).toHaveText('3 March 2010')

    await section5Page.submit().click()
  })

  test('Given I have some repeating blocks with supplementary data, When I begin the section, Then I see the supplementary names rendered correctly', async () => {
    const hubPage = new HubPage(page)
    const listCollectorProductsPage = new ListCollectorProductsPage(page)

    await hubPage.submit().click()
    await expect(listCollectorProductsPage.listLabel(1)).toHaveText('Articles and equipment for sports or outdoor games')
    await expect(listCollectorProductsPage.listLabel(2)).toHaveText('Kitchen Equipment')
    await listCollectorProductsPage.submit().click()
  })

  test('Given I have repeating blocks with supplementary data, When I start the first repeating block, Then I see the supplementary data for the first list item', async () => {
    const productRepeatingBlock1Page = new ProductRepeatingBlock1Page(page)
    const body = page.locator('body')

    await expect(body).toContainText('Include')
    await expect(body).toContainText("for children's playgrounds")
    await expect(body).toContainText('swimming pools and paddling pools')
    await expect(body).toContainText('Exclude')
    await expect(body).toContainText('sports holdalls, gloves, clothing of textile materials, footwear, protective eyewear, rackets, balls, skates')
    await expect(body).toContainText(
      "for skiing, water sports, golf, fishing', for skiing, water sports, golf, fishing, table tennis, PE, gymnastics, athletics"
    )

    await expect(productRepeatingBlock1Page.productVolumeSalesLabel()).toHaveText('Volume of sales for Articles and equipment for sports or outdoor games')
    await expect(productRepeatingBlock1Page.productVolumeTotalLabel()).toHaveText(
      'Total volume produced for Articles and equipment for sports or outdoor games'
    )

    await productRepeatingBlock1Page.productVolumeSales().fill('100')
    await productRepeatingBlock1Page.productVolumeTotal().fill('200')
  })

  test('Given I have repeating blocks with supplementary data, When I start the second repeating block, Then I see the supplementary data for the second list item', async () => {
    const productRepeatingBlock1Page = new ProductRepeatingBlock1Page(page)
    const listCollectorProductsPage = new ListCollectorProductsPage(page)
    const body = page.locator('body')

    await productRepeatingBlock1Page.submit().click()
    await listCollectorProductsPage.submit().click()

    await expect(body).toContainText('Include')
    await expect(body).toContainText('pots and pans')
    await expect(body).not.toContainText('Exclude')
    await expect(productRepeatingBlock1Page.productVolumeSalesLabel()).toHaveText('Volume of sales for Kitchen Equipment')
    await expect(productRepeatingBlock1Page.productVolumeTotalLabel()).toHaveText('Total volume produced for Kitchen Equipment')

    await productRepeatingBlock1Page.productVolumeSales().fill('50')
    await productRepeatingBlock1Page.productVolumeTotal().fill('300')
    await productRepeatingBlock1Page.submit().click()
  })

  test('Given I have a calculated summary using the repeating blocks, When I reach the Calculated Summary, Then I see the correct total and supplementary data labels', async () => {
    const listCollectorProductsPage = new ListCollectorProductsPage(page)
    const calculatedSummaryVolumeSalesPage = new CalculatedSummaryVolumeSalesPage(page)

    await listCollectorProductsPage.submit().click()
    await expect(page).toHaveURL(new RegExp(calculatedSummaryVolumeSalesPage.pageName))
    await expect(calculatedSummaryVolumeSalesPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the total volume of sales over the previous quarter to be 150 kg. Is this correct?'
    )

    const items = page.locator(summaryItems)
    await expect(items.nth(0)).toHaveText('Volume of sales for Articles and equipment for sports or outdoor games')
    await expect(items.nth(1)).toHaveText('Volume of sales for Kitchen Equipment')
    await expect(items.nth(2)).toHaveText('Total sales volume')

    const values = page.locator(summaryValues)
    await expect(values.nth(0)).toHaveText('100 kg')
    await expect(values.nth(1)).toHaveText('50 kg')
    await expect(values.nth(2)).toHaveText('150 kg')

    await calculatedSummaryVolumeSalesPage.submit().click()
  })

  test('Given I have another calculated summary using the repeating blocks, When I reach the Calculated Summary, Then I see the correct total and supplementary data labels', async () => {
    const calculatedSummaryVolumeTotalPage = new CalculatedSummaryVolumeTotalPage(page)

    await expect(calculatedSummaryVolumeTotalPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the total volume produced over the previous quarter to be 500 kg. Is this correct?'
    )

    const items = page.locator(summaryItems)
    await expect(items.nth(0)).toHaveText('Total volume produced for Articles and equipment for sports or outdoor games')
    await expect(items.nth(1)).toHaveText('Total volume produced for Kitchen Equipment')
    await expect(items.nth(2)).toHaveText('Total volume produced')

    const values = page.locator(summaryValues)
    await expect(values.nth(0)).toHaveText('200 kg')
    await expect(values.nth(1)).toHaveText('300 kg')
    await expect(values.nth(2)).toHaveText('500 kg')

    await calculatedSummaryVolumeTotalPage.submit().click()
  })

  test('Given I have dynamic answers using a supplementary list, When I reach the dynamic answer page, Then I see the correct supplementary data in the answer labels', async () => {
    const dynamicProductsPage = new DynamicProductsPage(page)

    await expect(dynamicProductsPage.labels().nth(0)).toHaveText('Value of sales for Articles and equipment for sports or outdoor games')
    await expect(dynamicProductsPage.labels().nth(1)).toHaveText('Value of sales for Kitchen Equipment')
    await expect(dynamicProductsPage.labels().nth(2)).toHaveText('Value of sales from other categories')

    await dynamicProductsPage.inputs().nth(0).fill('110')
    await dynamicProductsPage.inputs().nth(1).fill('220')
    await dynamicProductsPage.inputs().nth(2).fill('330')
    await dynamicProductsPage.submit().click()
  })

  test('Given I have a calculated summary of dynamic answers for a supplementary list, When I reach the calculated summary, Then I see the correct supplementary data in the title and labels', async () => {
    const calculatedSummaryValueSalesPage = new CalculatedSummaryValueSalesPage(page)

    await expect(calculatedSummaryValueSalesPage.calculatedSummaryTitle()).toHaveText(
      'We calculate the total value of sales over the previous quarter to be £660.00. Is this correct?'
    )

    const items = page.locator(summaryItems)
    await expect(items.nth(0)).toHaveText('Value of sales for Articles and equipment for sports or outdoor games')
    await expect(items.nth(1)).toHaveText('Value of sales for Kitchen Equipment')
    await expect(items.nth(2)).toHaveText('Value of sales from other categories')
    await expect(items.nth(3)).toHaveText('Total sales value')

    const values = page.locator(summaryValues)
    await expect(values.nth(0)).toHaveText('£110.00')
    await expect(values.nth(1)).toHaveText('£220.00')
    await expect(values.nth(2)).toHaveText('£330.00')
    await expect(values.nth(3)).toHaveText('£660.00')

    await calculatedSummaryValueSalesPage.submit().click()
  })

  test('Given I have a section with repeating answers for a supplementary list, When I reach the section summary page, Then I see the supplementary data and my answers rendered correctly', async () => {
    const section6Page = new Section6Page(page)
    const hubPage = new HubPage(page)

    await expect(page.locator(summaryRowTitles).first()).toBeVisible({ timeout: 60_000 })
    await expect(page.locator(summaryRowTitles).nth(0)).toHaveText('Articles and equipment for sports or outdoor games')

    const items = page.locator(summaryItems)
    await expect(items.nth(0)).toHaveText('Volume of sales for Articles and equipment for sports or outdoor games')
    await expect(items.nth(1)).toHaveText('Total volume produced for Articles and equipment for sports or outdoor games')
    await expect(items.nth(2)).toHaveText('Volume of sales for Kitchen Equipment')
    await expect(items.nth(3)).toHaveText('Total volume produced for Kitchen Equipment')
    await expect(items.nth(4)).toHaveText('Value of sales for Articles and equipment for sports or outdoor games')
    await expect(items.nth(5)).toHaveText('Value of sales for Kitchen Equipment')
    await expect(items.nth(6)).toHaveText('Value of sales from other categories')

    const values = page.locator(summaryValues)
    await expect(values.nth(0)).toHaveText('100 kg')
    await expect(values.nth(1)).toHaveText('200 kg')
    await expect(values.nth(2)).toHaveText('50 kg')
    await expect(values.nth(3)).toHaveText('300 kg')
    await expect(values.nth(4)).toHaveText('£110.00')
    await expect(values.nth(5)).toHaveText('£220.00')
    await expect(values.nth(6)).toHaveText('£330.00')

    await section6Page.submit().click()
    await expect(hubPage.summaryRowState('section-6')).toHaveText('Completed')
  })

  test('Given I am using a supplementary dataset where the size of one of the lists skips a question in a section, When I enter the section, Then I only see an interstitial block as the other block is skipped', async () => {
    const hubPage = new HubPage(page)
    const productVolumeInterstitialPage = new ProductVolumeInterstitialPage(page)

    await hubPage.summaryRowLink('section-8').click()
    await expect(page).toHaveURL(new RegExp(productVolumeInterstitialPage.pageName))
    await productVolumeInterstitialPage.submit().click()
    await expect(hubPage.summaryRowState('section-8')).toHaveText('Completed')
  })

  test('Given I relaunch the survey with new supplementary data and new list items for the repeating section, When I open the Hub page, Then I see the new supplementary list items as new incomplete sections and not any old ones', async () => {
    const hubPage = new HubPage(page)

    await openQuestionnaire(supplementaryDataSchema, {
      sdsDatasetId: '3bb41d29-4daa-9520-82f0-cae365f390c6',
      responseId
    })

    await expect(hubPage.summaryRowTitle('section-4-1')).toContainText('Harry Potter')
    await expect(hubPage.summaryRowTitle('section-4-2')).toContainText('Bruce Wayne')
    await expect(hubPage.summaryRowTitle('section-5-1')).toContainText('Jane Doe')
    await expect(hubPage.summaryRowTitle('section-5-2')).toContainText('John Smith')

    await expect(hubPage.summaryRowState('section-4-1')).toHaveText('Completed')
    await expect(hubPage.summaryRowState('section-4-2')).toHaveText('Not started')
    await expect(hubPage.summaryRowState('section-5-1')).toHaveText('Completed')
    await expect(hubPage.summaryRowState('section-5-2')).toHaveText('Completed')

    await expect(page.locator('body')).not.toContainText('Clark Kent')
  })

  test('Given the survey has been relaunched with new data and more items in the products list, When I am on the Hub, Then I see the products section and section with a new block due to the product list size are both in progress', async () => {
    const hubPage = new HubPage(page)

    await expect(hubPage.summaryRowState('section-6')).toHaveText('Partially completed')
    await expect(hubPage.summaryRowState('section-8')).toHaveText('Partially completed')
  })

  test('Given I am using a supplementary dataset with a product list size that skips a question in the sales target section, When I enter the section, Then I only see an interstitial block', async () => {
    const hubPage = new HubPage(page)
    const productSalesInterstitialPage = new ProductSalesInterstitialPage(page)

    await hubPage.summaryRowLink('section-7').click()
    await expect(page).toHaveURL(new RegExp(productSalesInterstitialPage.pageName))
    await productSalesInterstitialPage.submit().click()
    await expect(hubPage.summaryRowState('section-7')).toHaveText('Completed')
  })

  test('Given there is now an additional product, When I resume the Product Details Section, Then I start from the list collector content block and see the new product is incomplete', async () => {
    const hubPage = new HubPage(page)
    const listCollectorProductsPage = new ListCollectorProductsPage(page)
    const productRepeatingBlock1Page = new ProductRepeatingBlock1Page(page)

    await hubPage.summaryRowLink('section-6').click()
    await expect(page).toHaveURL(new RegExp(listCollectorProductsPage.pageName))

    await listItemComplete(listCollectorProductsPage.listLabel(1), true)
    await listItemComplete(listCollectorProductsPage.listLabel(2), true)
    await listItemComplete(listCollectorProductsPage.listLabel(3), false)

    await listCollectorProductsPage.submit().click()
    await expect(page).toHaveURL(new RegExp(productRepeatingBlock1Page.pageName))
  })

  test('Given I complete the section and relaunch with the old data that has fewer items in the products list, When I am on the Hub, Then I see the products section and sales targets sections are now in progress', async () => {
    const hubPage = new HubPage(page)
    const productRepeatingBlock1Page = new ProductRepeatingBlock1Page(page)
    const listCollectorProductsPage = new ListCollectorProductsPage(page)
    const calculatedSummaryVolumeSalesPage = new CalculatedSummaryVolumeSalesPage(page)
    const calculatedSummaryVolumeTotalPage = new CalculatedSummaryVolumeTotalPage(page)
    const dynamicProductsPage = new DynamicProductsPage(page)
    const calculatedSummaryValueSalesPage = new CalculatedSummaryValueSalesPage(page)
    const section6Page = new Section6Page(page)

    await productRepeatingBlock1Page.productVolumeSales().fill('40')
    await productRepeatingBlock1Page.productVolumeTotal().fill('50')
    await productRepeatingBlock1Page.submit().click()

    await listCollectorProductsPage.submit().click()
    await calculatedSummaryVolumeSalesPage.submit().click()
    await calculatedSummaryVolumeTotalPage.submit().click()

    await dynamicProductsPage.inputs().nth(2).fill('115')
    await dynamicProductsPage.submit().click()

    await calculatedSummaryValueSalesPage.submit().click()
    await section6Page.submit().click()

    await expect(hubPage.summaryRowState('section-6')).toHaveText('Completed')

    await openQuestionnaire(supplementaryDataSchema, {
      sdsDatasetId: '203b2f9d-c500-8175-98db-86ffcfdccfa3',
      responseId
    })

    await expect(hubPage.summaryRowState('section-6')).toHaveText('Partially completed')
    await expect(hubPage.summaryRowState('section-7')).toHaveText('Partially completed')
  })

  test('Given I return to the new data resulting in a new incomplete section, When I start the section, Then I see the new supplementary data piped in accordingly', async () => {
    const hubPage = new HubPage(page)
    const lengthOfEmploymentPage = new LengthOfEmploymentPage(page)
    const section4Page = new Section4Page(page)

    await openQuestionnaire(supplementaryDataSchema, {
      sdsDatasetId: '3bb41d29-4daa-9520-82f0-cae365f390c6',
      responseId
    })

    await hubPage.submit().click()

    await lengthOfEmploymentPage.day().fill('10')
    await lengthOfEmploymentPage.month().fill('10')
    await lengthOfEmploymentPage.year().fill('1999')
    await lengthOfEmploymentPage.submit().click()

    await expect(section4Page.lengthEmploymentQuestion()).toHaveText('When did Bruce Wayne start working for Lidl?')
    await expect(section4Page.employmentStart()).toHaveText('10 October 1999')

    await section4Page.submit().click()
  })

  test("Given I can view my response after submission, When I submit the survey, Then I see the values I've entered and correct rendering with supplementary data", async () => {
    const hubPage = new HubPage(page)
    const listCollectorProductsPage = new ListCollectorProductsPage(page)
    const productRepeatingBlock1Page = new ProductRepeatingBlock1Page(page)
    const calculatedSummaryVolumeSalesPage = new CalculatedSummaryVolumeSalesPage(page)
    const calculatedSummaryVolumeTotalPage = new CalculatedSummaryVolumeTotalPage(page)
    const dynamicProductsPage = new DynamicProductsPage(page)
    const calculatedSummaryValueSalesPage = new CalculatedSummaryValueSalesPage(page)
    const section6Page = new Section6Page(page)
    const productQuestion3EnabledPage = new ProductQuestion3EnabledPage(page)
    const thankYouPage = new ThankYouPage(page)
    const viewSubmittedResponsePage = new ViewSubmittedResponsePage(page)

    await hubPage.submit().click()
    await listCollectorProductsPage.submit().click()
    await productRepeatingBlock1Page.productVolumeSales().fill('40')
    await productRepeatingBlock1Page.productVolumeTotal().fill('50')
    await productRepeatingBlock1Page.submit().click()
    await listCollectorProductsPage.submit().click()
    await calculatedSummaryVolumeSalesPage.submit().click()
    await calculatedSummaryVolumeTotalPage.submit().click()
    await dynamicProductsPage.inputs().nth(2).fill('115')
    await dynamicProductsPage.submit().click()
    await calculatedSummaryValueSalesPage.submit().click()
    await section6Page.submit().click()
    await hubPage.submit().click()
    await productQuestion3EnabledPage.yes().click()
    await productQuestion3EnabledPage.submit().click()
    await hubPage.submit().click()
    await thankYouPage.savePrintAnswersLink().click()

    await expect(page.getByRole('heading', { name: 'Company Details' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Additional Employees' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Harry Potter' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Bruce Wayne' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Jane Doe' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'John Smith' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Product details' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Production Targets' })).toBeVisible()

    // Company details
    await expect(viewSubmittedResponsePage.emailQuestion()).toHaveText('Is contact@lidl.org still the correct contact email for Lidl?')
    await expect(viewSubmittedResponsePage.sameEmailAnswer()).toHaveText('No')
    await expect(viewSubmittedResponsePage.newEmailQuestion()).toHaveText('What is the new contact email for Lidl?')
    await expect(viewSubmittedResponsePage.newEmailAnswer()).toHaveText('new.contact@gmail.com')
    await expect(viewSubmittedResponsePage.tradingQuestion()).toHaveText('When did Lidl begin trading?')
    await expect(viewSubmittedResponsePage.tradingAnswer()).toHaveText('Sunday 30 November 1947')
    await expect(page.locator(summaryRowTitles).nth(0)).toHaveText('How much of the £555,000.00 total UK sales was from Bristol and London?')
    await expect(viewSubmittedResponsePage.salesBristolAnswer()).toHaveText('£333,000.00')
    await expect(viewSubmittedResponsePage.salesLondonAnswer()).toHaveText('£111,000.00')

    // Additional Employees
    await expect(viewSubmittedResponsePage.anyAdditionalEmployeeQuestion()).toHaveText('Do you have any additional employees to report on?')
    await expect(viewSubmittedResponsePage.anyAdditionalEmployeeAnswer()).toHaveText('Yes')
    await expect(viewSubmittedResponsePage.additionalEmployeeReportingContent(1).locator(summaryItems).nth(0)).toHaveText('Jane Doe')
    await expect(viewSubmittedResponsePage.additionalEmployeeReportingContent(1).locator(summaryItems).nth(1)).toHaveText('John Smith')

    // Harry Potter
    await expect(viewSubmittedResponsePage.employeeDetailQuestionsContent(0).locator(summaryItems).nth(0)).toHaveText(
      'When did Harry Potter start working for Lidl?'
    )
    await expect(viewSubmittedResponsePage.employeeDetailQuestionsContent(0).locator(summaryValues).nth(0)).toHaveText('1 January 1990')

    // Bruce Wayne
    await expect(viewSubmittedResponsePage.employeeDetailQuestionsContent('0-1').locator(summaryItems).nth(0)).toHaveText(
      'When did Bruce Wayne start working for Lidl?'
    )
    await expect(viewSubmittedResponsePage.employeeDetailQuestionsContent('0-1').locator(summaryValues).nth(0)).toHaveText('10 October 1999')

    // Jane Doe
    await expect(viewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent(0).locator(summaryItems).nth(0)).toHaveText(
      'When did Jane Doe start working for Lidl?'
    )
    await expect(viewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent(0).locator(summaryValues).nth(0)).toHaveText('1 January 2000')

    // John Smith
    await expect(viewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent('0-2').locator(summaryItems).nth(0)).toHaveText(
      'When did John Smith start working for Lidl?'
    )
    await expect(viewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent('0-2').locator(summaryValues).nth(0)).toHaveText('3 March 2010')

    // Product details
    await expect(viewSubmittedResponsePage.productReportingContent(0).locator(summaryItems).nth(0)).toHaveText(
      'Volume of sales for Articles and equipment for sports or outdoor games'
    )
    await expect(viewSubmittedResponsePage.productReportingContent(0).locator(summaryItems).nth(1)).toHaveText(
      'Total volume produced for Articles and equipment for sports or outdoor games'
    )
    await expect(viewSubmittedResponsePage.productReportingContent(0).locator(summaryItems).nth(2)).toHaveText('Volume of sales for Kitchen Equipment')
    await expect(viewSubmittedResponsePage.productReportingContent(0).locator(summaryValues).nth(0)).toHaveText('100 kg')
    await expect(viewSubmittedResponsePage.productReportingContent(0).locator(summaryValues).nth(1)).toHaveText('200 kg')
    await expect(viewSubmittedResponsePage.productReportingContent(0).locator(summaryItems).nth(3)).toHaveText(
      'Total volume produced for Kitchen Equipment'
    )
    await expect(viewSubmittedResponsePage.productReportingContent(0).locator(summaryItems).nth(4)).toHaveText('Volume of sales for Groceries')
    await expect(viewSubmittedResponsePage.productReportingContent(0).locator(summaryItems).nth(5)).toHaveText('Total volume produced for Groceries')
    await expect(viewSubmittedResponsePage.productReportingContent(0).locator(summaryValues).nth(2)).toHaveText('50 kg')
    await expect(viewSubmittedResponsePage.productReportingContent(0).locator(summaryValues).nth(3)).toHaveText('300 kg')
    await expect(viewSubmittedResponsePage.productReportingContent(0).locator(summaryValues).nth(4)).toHaveText('40 kg')
    await expect(viewSubmittedResponsePage.productReportingContent(0).locator(summaryValues).nth(5)).toHaveText('50 kg')
    await expect(viewSubmittedResponsePage.productReportingContent(1).locator(summaryItems).nth(0)).toHaveText(
      'Value of sales for Articles and equipment for sports or outdoor games'
    )
    await expect(viewSubmittedResponsePage.productReportingContent(1).locator(summaryItems).nth(1)).toHaveText('Value of sales for Kitchen Equipment')
    await expect(viewSubmittedResponsePage.productReportingContent(1).locator(summaryItems).nth(2)).toHaveText('Value of sales for Groceries')
    await expect(viewSubmittedResponsePage.productReportingContent(1).locator(summaryItems).nth(3)).toHaveText('Value of sales from other categories')
    await expect(viewSubmittedResponsePage.productReportingContent(1).locator(summaryValues).nth(0)).toHaveText('£110.00')
    await expect(viewSubmittedResponsePage.productReportingContent(1).locator(summaryValues).nth(1)).toHaveText('£220.00')
    await expect(viewSubmittedResponsePage.productReportingContent(1).locator(summaryValues).nth(2)).toHaveText('£115.00')
    await expect(viewSubmittedResponsePage.productReportingContent(1).locator(summaryValues).nth(3)).toHaveText('£330.00')
  })
})
