import { createOpenQuestionnaire, test, expect } from '../../../fixtures/test'
import type { OpenQuestionnaire, BrowserContext, Page } from '../../../fixtures/test'
import ResponsiblePartyPage from '../../../generated_pages/list_collector_repeating_blocks_section_summary/responsible-party.page'
import AnyCompaniesOrBranchesPage from '../../../generated_pages/list_collector_repeating_blocks_section_summary/any-companies-or-branches.page'
import AddCompanyPage from '../../../generated_pages/list_collector_repeating_blocks_section_summary/any-other-companies-or-branches-add.page'
import EditCompanyPage from '../../../generated_pages/list_collector_repeating_blocks_section_summary/any-other-companies-or-branches-edit.page'
import RemoveCompanyPage from '../../../generated_pages/list_collector_repeating_blocks_section_summary/any-other-companies-or-branches-remove.page'
import CompaniesRepeatingBlock1Page from '../../../generated_pages/list_collector_repeating_blocks_section_summary/companies-repeating-block-1-repeating-block.page'
import CompaniesRepeatingBlock2Page from '../../../generated_pages/list_collector_repeating_blocks_section_summary/companies-repeating-block-2-repeating-block.page'
import AnyOtherCompaniesOrBranchesPage from '../../../generated_pages/list_collector_repeating_blocks_section_summary/any-other-companies-or-branches.page'
import SectionCompaniesPage from '../../../generated_pages/list_collector_repeating_blocks_section_summary/section-companies-summary.page'
import AnyOtherTradingDetailsPage from '../../../generated_pages/list_collector_repeating_blocks_section_summary/any-other-trading-details.page'
import SubmitPage from '../../../generated_pages/list_collector_repeating_blocks_section_summary/submit.page'
import { repeatingAnswerChangeLink, checkItemsInList, summaryItemComplete } from '../../../helpers'
import HubPage from '../../../base_pages/hub.page'
import ResponsiblePartyHubPage from '../../../generated_pages/list_collector_repeating_blocks_with_hub/responsible-party-business.page'
import ThankYouPage from '../../../base_pages/thank-you.page'

const summaryValues = 'dd[class="ons-summary__values"]'

const waitForThankYouAfterSubmit = async (page: Page, submitPage: SubmitPage, thankYouPage: ThankYouPage): Promise<void> => {
  const submitRedirectAttempts = 2
  const submitRedirectTimeoutMs = parseInt(process.env.EQ_SUBMIT_REDIRECT_TIMEOUT_MS ?? '10000', 10)
  let waitError

  for (let attempt = 1; attempt <= submitRedirectAttempts; attempt += 1) {
    try {
      await page.waitForURL((url: URL) => url.pathname.includes(thankYouPage.pageName), { timeout: submitRedirectTimeoutMs })

      return
    } catch (error) {
      waitError = error

      if (attempt < submitRedirectAttempts) {
        const currentUrl: string = page.url()
        if (currentUrl.includes(submitPage.pageName)) {
          await submitPage.submit().click()
        }
      }
    }
  }

  throw waitError
}

async function proceedToListCollector (page: Page): Promise<void> {
  const responsiblePartyPage = new ResponsiblePartyPage(page)
  const anyCompaniesOrBranchesPage = new AnyCompaniesOrBranchesPage(page)
  await responsiblePartyPage.yes().click()
  await anyCompaniesOrBranchesPage.submit().click()
  await anyCompaniesOrBranchesPage.yes().click()
  await anyCompaniesOrBranchesPage.submit().click()
}

async function addCompany (
  page: Page,
  companyOrBranchName: string,
  registrationNumber: string,
  registrationDateDay: string,
  registrationDateMonth: string,
  registrationDateYear: string,
  authorisedTraderUk: boolean,
  authorisedTraderEu?: boolean
): Promise<void> {
  const addCompanyPage = new AddCompanyPage(page)
  const companiesRepeatingBlock1Page = new CompaniesRepeatingBlock1Page(page)
  const companiesRepeatingBlock2Page = new CompaniesRepeatingBlock2Page(page)
  await addCompanyPage.companyOrBranchName().fill(companyOrBranchName)
  await addCompanyPage.submit().click()
  await companiesRepeatingBlock1Page.registrationNumber().fill(registrationNumber)
  await companiesRepeatingBlock1Page.registrationDateDay().fill(registrationDateDay)
  await companiesRepeatingBlock1Page.registrationDateMonth().fill(registrationDateMonth)
  await companiesRepeatingBlock1Page.registrationDateYear().fill(registrationDateYear)
  await companiesRepeatingBlock1Page.submit().click()
  if (authorisedTraderUk) {
    await companiesRepeatingBlock2Page.authorisedTraderUkRadioYes().click()
  } else {
    await companiesRepeatingBlock2Page.authorisedTraderUkRadioNo().click()
  }
  if (authorisedTraderEu === true) {
    await companiesRepeatingBlock2Page.authorisedTraderEuRadioYes().click()
  } else if (authorisedTraderEu === false) {
    await companiesRepeatingBlock2Page.authorisedTraderEuRadioNo().click()
  }
  await companiesRepeatingBlock2Page.submit().click()
}

test.describe('List Collector Repeating Blocks', () => {
  test.describe('Given a normal journey through the list collector with repeating blocks', () => {
    test.beforeEach('Load the survey', async ({ page, openQuestionnaire }) => {
      const responsiblePartyPage = new ResponsiblePartyPage(page)
      await openQuestionnaire('test_list_collector_repeating_blocks_section_summary.json')
      // These tests sometimes fail when a button is on the screen, but right on the very edge, accept cookies to increase screen space
      await responsiblePartyPage.acceptCookies().click()
    })

    test('When the user adds items and completes all of the repeating blocks, Then they are able to successfully submit the questionnaire.', async ({
      page
    }) => {
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const anyOtherTradingDetailsPage = new AnyOtherTradingDetailsPage(page)
      const sectionCompaniesPage = new SectionCompaniesPage(page)
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      await proceedToListCollector(page)
      await addCompany(page, 'ONS', '123', '1', '1', '2023', true, true)
      await anyOtherCompaniesOrBranchesPage.yes().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await addCompany(page, 'GOV', '456', '2', '2', '2023', false, false)

      await anyOtherCompaniesOrBranchesPage.no().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()

      await anyOtherTradingDetailsPage.submit().click()
      await sectionCompaniesPage.submit().click()
      await submitPage.submit().click()
      await waitForThankYouAfterSubmit(page, submitPage, thankYouPage)
      await expect(page).toHaveURL(new RegExp(thankYouPage.pageName))
    })
  })

  test.describe('Given a journey through the list collector with repeating blocks where items need to be updated', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Load the survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_list_collector_repeating_blocks_section_summary.json')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When the user adds items to the list and completes the repeating blocks, Then the completed items are displayed on the list collector page.', async () => {
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      await proceedToListCollector(page)
      await addCompany(page, 'ONS', '123', '1', '1', '2023', true, true)
      await anyOtherCompaniesOrBranchesPage.yes().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await addCompany(page, 'GOV', '456', '2', '2', '2023', false, false)
      await anyOtherCompaniesOrBranchesPage.yes().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await addCompany(page, 'MOD', '789', '3', '3', '2023', true)
      await checkItemsInList(['ONS', 'GOV', 'MOD'], (index) => anyOtherCompaniesOrBranchesPage.listLabel(index))
    })

    test('When the user edits an item, Then the name of the item is able to be changed', async () => {
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const editCompanyPage = new EditCompanyPage(page)
      await anyOtherCompaniesOrBranchesPage.listEditLink(2).click()
      await editCompanyPage.companyOrBranchName().fill('Government')
      await editCompanyPage.submit().click()
      await checkItemsInList(['ONS', 'Government', 'MOD'], (index) => anyOtherCompaniesOrBranchesPage.listLabel(index))
    })

    test('When the user clicks the remove link, Then the item selected is removed', async () => {
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const removeCompanyPage = new RemoveCompanyPage(page)
      await anyOtherCompaniesOrBranchesPage.listRemoveLink(2).click()
      await removeCompanyPage.yes().click()
      await removeCompanyPage.submit().click()
      await checkItemsInList(['ONS', 'MOD'], (index) => anyOtherCompaniesOrBranchesPage.listLabel(index))
      await expect(anyOtherCompaniesOrBranchesPage.listLabel(2)).not.toContainText('Government')
    })

    test('When a user has finished editing or removing from the list, Then they are still able to add additional companies', async () => {
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      await anyOtherCompaniesOrBranchesPage.yes().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await addCompany(page, 'Council', '101', '4', '4', '2023', false, true)
      await checkItemsInList(['ONS', 'MOD', 'Council'], (index) => anyOtherCompaniesOrBranchesPage.listLabel(index))
    })

    test('When a user has finished making changes to the list, Then section can be completed and the questionnaire submitted', async () => {
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const anyOtherTradingDetailsPage = new AnyOtherTradingDetailsPage(page)
      const sectionCompaniesPage = new SectionCompaniesPage(page)
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      await anyOtherCompaniesOrBranchesPage.no().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()

      await anyOtherTradingDetailsPage.submit().click()
      await sectionCompaniesPage.submit().click()
      await submitPage.submit().click()
      await waitForThankYouAfterSubmit(page, submitPage, thankYouPage)
      await expect(page).toHaveURL(new RegExp(thankYouPage.pageName))
    })
  })

  test.describe('Given a journey that test routes through the list collector with repeating blocks.', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Load the survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_list_collector_repeating_blocks_section_summary.json')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When the user only completes some of the repeating blocks and leaves others incomplete, Then on the list collector page only completed items should display the completed checkmark icon.', async () => {
      const addCompanyPage = new AddCompanyPage(page)
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const companiesRepeatingBlock1Page = new CompaniesRepeatingBlock1Page(page)
      const companiesRepeatingBlock2Page = new CompaniesRepeatingBlock2Page(page)
      const editCompanyPage = new EditCompanyPage(page)
      await proceedToListCollector(page)

      await addCompany(page, 'ONS', '123', '1', '1', '2023', true, true)
      await anyOtherCompaniesOrBranchesPage.yes().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await addCompanyPage.companyOrBranchName().fill('GOV')
      await addCompanyPage.submit().click()
      await companiesRepeatingBlock1Page.cancelAndReturn().click()
      await editCompanyPage.cancelAndReturn().click()

      await anyOtherCompaniesOrBranchesPage.yes().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await addCompanyPage.companyOrBranchName().fill('MOD')
      await addCompanyPage.submit().click()
      await companiesRepeatingBlock1Page.registrationNumber().fill('789')
      await companiesRepeatingBlock1Page.registrationDateDay().fill('3')
      await companiesRepeatingBlock1Page.registrationDateMonth().fill('3')
      await companiesRepeatingBlock1Page.registrationDateYear().fill('2023')
      await companiesRepeatingBlock1Page.submit().click()
      await companiesRepeatingBlock2Page.cancelAndReturn().click()
      await companiesRepeatingBlock1Page.cancelAndReturn().click()
      await editCompanyPage.cancelAndReturn().click()

      await anyOtherCompaniesOrBranchesPage.yes().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await addCompany(page, 'NAV', '101', '4', '4', '2023', true, true)

      // Only the ONS and NAV items should be complete
      await checkItemsInList(['ONS', 'GOV', 'MOD', 'NAV'], (index) => anyOtherCompaniesOrBranchesPage.listLabel(index))
      await summaryItemComplete(page.locator('dt[data-qa="list-item-1-label"]'), true)
      await summaryItemComplete(page.locator('dt[data-qa="list-item-2-label"]'), false)
      await summaryItemComplete(page.locator('dt[data-qa="list-item-3-label"]'), false)
      await summaryItemComplete(page.locator('dt[data-qa="list-item-1-label"]'), true)
    })

    test('When an item has incomplete repeating blocks, Then using submit on the list collector page will navigate the user to the first incomplete repeating block.', async () => {
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const companiesRepeatingBlock1Page = new CompaniesRepeatingBlock1Page(page)
      await anyOtherCompaniesOrBranchesPage.no().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await expect(page).toHaveURL(new RegExp(companiesRepeatingBlock1Page.pageName))
    })

    test('When there are multiple incomplete items and only the first incomplete item is completed, Then attempting using Submit on the list collector page will navigate the user to the next incomplete item.', async () => {
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const companiesRepeatingBlock1Page = new CompaniesRepeatingBlock1Page(page)
      const companiesRepeatingBlock2Page = new CompaniesRepeatingBlock2Page(page)
      // Complete the first incomplete list item
      await companiesRepeatingBlock1Page.registrationNumber().fill('456')
      await companiesRepeatingBlock1Page.registrationDateDay().fill('2')
      await companiesRepeatingBlock1Page.registrationDateMonth().fill('2')
      await companiesRepeatingBlock1Page.registrationDateYear().fill('2023')
      await companiesRepeatingBlock1Page.submit().click()
      await companiesRepeatingBlock2Page.authorisedTraderUkRadioNo().click()
      await companiesRepeatingBlock2Page.authorisedTraderEuRadioNo().click()
      await companiesRepeatingBlock2Page.submit().click()

      await anyOtherCompaniesOrBranchesPage.no().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()

      // The user is taken to the next incomplete repeating block
      await expect(page).toHaveURL(new RegExp(companiesRepeatingBlock2Page.pageName))
    })

    test('When the last remaining incomplete repeating block is completed, Then all items are marked as completed with the checkmark icon.', async () => {
      const companiesRepeatingBlock2Page = new CompaniesRepeatingBlock2Page(page)
      await companiesRepeatingBlock2Page.authorisedTraderUkRadioNo().click()
      await companiesRepeatingBlock2Page.submit().click()
      await summaryItemComplete(page.locator('dt[data-qa="list-item-1-label"]'), true)
      await summaryItemComplete(page.locator('dt[data-qa="list-item-2-label"]'), true)
      await summaryItemComplete(page.locator('dt[data-qa="list-item-3-label"]'), true)
      await summaryItemComplete(page.locator('dt[data-qa="list-item-4-label"]'), true)
    })

    test('When the user clicks a change link from the section summary and submits without changing an answer, Then the user is returned to the section summary anchored to the answer they clicked on', async () => {
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const anyOtherTradingDetailsPage = new AnyOtherTradingDetailsPage(page)
      const sectionCompaniesPage = new SectionCompaniesPage(page)
      await anyOtherCompaniesOrBranchesPage.no().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await anyOtherTradingDetailsPage.submit().click()

      await sectionCompaniesPage.anyOtherTradingDetailsAnswerEdit().click()
      await anyOtherTradingDetailsPage.submit().click()
      await expect(page).toHaveURL(/section-companies\/#any-other-trading-details-answer/)

      await sectionCompaniesPage.anyOtherTradingDetailsAnswerEdit().click()
      await anyOtherTradingDetailsPage.previous().click()
      await expect(page).toHaveURL(/section-companies\/#any-other-trading-details-answer/)
    })

    test('When an answer is edited from the section summary which does not affect progress, Then pressing continue returns the user to the section summary anchored to the answer they edited', async () => {
      const anyOtherTradingDetailsPage = new AnyOtherTradingDetailsPage(page)
      const sectionCompaniesPage = new SectionCompaniesPage(page)
      await sectionCompaniesPage.anyOtherTradingDetailsAnswerEdit().click()
      await anyOtherTradingDetailsPage.answer().fill('No')
      await anyOtherTradingDetailsPage.submit().click()
      await expect(page).toHaveURL(/section-companies\/#any-other-trading-details-answer/)
    })

    test('When a user clicks a change link from the final summary and submits without changing an answer, Then the user is returned to the final summary anchored to the answer they clicked on', async () => {
      const anyOtherTradingDetailsPage = new AnyOtherTradingDetailsPage(page)
      const sectionCompaniesPage = new SectionCompaniesPage(page)
      const submitPage = new SubmitPage(page)
      await sectionCompaniesPage.submit().click()

      await submitPage.anyOtherTradingDetailsAnswerEdit().click()
      await anyOtherTradingDetailsPage.submit().click()
      await expect(page).toHaveURL(/submit\/#any-other-trading-details-answer/)

      await submitPage.anyOtherTradingDetailsAnswerEdit().click()
      await anyOtherTradingDetailsPage.previous().click()
      await expect(page).toHaveURL(/submit\/#any-other-trading-details-answer/)
    })

    test('When an an answer is edited from the final summary which does not affect progress, Then pressing continue returns the user to the final summary anchored to the answer they edited', async () => {
      const anyOtherTradingDetailsPage = new AnyOtherTradingDetailsPage(page)
      const sectionCompaniesPage = new SectionCompaniesPage(page)
      await sectionCompaniesPage.anyOtherTradingDetailsAnswerEdit().click()
      await anyOtherTradingDetailsPage.answer().fill('Yes')
      await anyOtherTradingDetailsPage.submit().click()
      await expect(page).toHaveURL(/submit\/#any-other-trading-details-answer/)
    })

    test('When all items are completed by the user, Then the questionnaire is able to be submitted.', async () => {
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      await submitPage.submit().click()
      await expect(page).toHaveURL(new RegExp(thankYouPage.pageName))
    })
  })

  test.describe('Given a journey through the list collector with repeating blocks', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Load the survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_list_collector_repeating_blocks_section_summary.json')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When the user adds and completes items, Then they are able to see the items on the section summary page.', async () => {
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const anyOtherTradingDetailsPage = new AnyOtherTradingDetailsPage(page)
      const sectionCompaniesPage = new SectionCompaniesPage(page)
      await proceedToListCollector(page)
      await addCompany(page, 'ONS', '123', '1', '1', '2023', true, true)
      await anyOtherCompaniesOrBranchesPage.yes().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await addCompany(page, 'GOV', '456', '2', '2', '2023', false)
      await anyOtherCompaniesOrBranchesPage.no().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await anyOtherTradingDetailsPage.submit().click()
      await sectionCompaniesPage.submit().click()
      await expect(page.locator(summaryValues).nth(2)).toContainText('ONS')
      await expect(page.locator(summaryValues).nth(4)).toContainText('1 January 2023')
      await expect(page.locator(summaryValues).nth(5)).toContainText('Yes')
      await expect(page.locator(summaryValues).nth(7)).toContainText('GOV')
      await expect(page.locator(summaryValues).nth(8)).toContainText('456')
      await expect(page.locator(summaryValues).nth(11)).toContainText('No answer provided')
    })

    test('When an item is edited from the section summary page, Then the correct value is displayed when the user returns to the summary.', async () => {
      const companiesRepeatingBlock1Page = new CompaniesRepeatingBlock1Page(page)
      await expect(page.locator(summaryValues).nth(8)).toContainText('456')
      await repeatingAnswerChangeLink(page, 8).click()
      await companiesRepeatingBlock1Page.registrationNumber().fill('789')
      await companiesRepeatingBlock1Page.submit().click()
      await expect(page.locator(summaryValues).nth(8)).toContainText('789')
    })
  })

  test.describe('Given the user is completing a list collector with repeating blocks in a mandatory section of a hub based questionnaire.', () => {
    test.describe.configure({ mode: 'serial' })

    let context: BrowserContext
    let page: Page
    let openQuestionnaire: OpenQuestionnaire

    test.beforeAll('Load the survey', async ({ browser }) => {
      context = await browser.newContext()
      page = await context.newPage()
      openQuestionnaire = createOpenQuestionnaire(page)
      await openQuestionnaire('test_list_collector_repeating_blocks_with_hub.json')
    })

    test.afterAll(async () => {
      await context.close()
    })

    test('When the user adds complete and incomplete items and returns to the hub, Then the user should be taken to first incomplete repeating block when pressing Continue.', async () => {
      const addCompanyPage = new AddCompanyPage(page)
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const companiesRepeatingBlock1Page = new CompaniesRepeatingBlock1Page(page)
      const hubPage = new HubPage(page)
      await proceedToListCollector(page)

      await addCompany(page, 'ONS', '123', '1', '1', '2023', true, true)
      await anyOtherCompaniesOrBranchesPage.yes().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await addCompanyPage.companyOrBranchName().fill('GOV')
      await addCompanyPage.submit().click()
      await companiesRepeatingBlock1Page.cancelAndReturn().click()
      await page.goto('questionnaire/')
      await hubPage.submit().click()
      await anyOtherCompaniesOrBranchesPage.no().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await expect(page).toHaveURL(new RegExp(companiesRepeatingBlock1Page.pageName))
    })

    test('When the user completes the incomplete blocks and returns to the list collector Page, Then the completed items should display the checkmark icon', async () => {
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const companiesRepeatingBlock1Page = new CompaniesRepeatingBlock1Page(page)
      const companiesRepeatingBlock2Page = new CompaniesRepeatingBlock2Page(page)
      await companiesRepeatingBlock1Page.registrationNumber().fill('456')
      await companiesRepeatingBlock1Page.registrationDateDay().fill('2')
      await companiesRepeatingBlock1Page.registrationDateMonth().fill('2')
      await companiesRepeatingBlock1Page.registrationDateYear().fill('2023')
      await companiesRepeatingBlock1Page.submit().click()
      await companiesRepeatingBlock2Page.authorisedTraderUkRadioNo().click()
      await companiesRepeatingBlock2Page.submit().click()
      await expect(page).toHaveURL(new RegExp(anyOtherCompaniesOrBranchesPage.pageName))
      await summaryItemComplete(page.locator('dt[data-qa="list-item-1-label"]'), true)
      await summaryItemComplete(page.locator('dt[data-qa="list-item-2-label"]'), true)
    })

    test('When another incomplete item is added via the section summary, Then navigating to the submit page of the section will redirect to the list collector page.', async () => {
      const addCompanyPage = new AddCompanyPage(page)
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const anyOtherTradingDetailsPage = new AnyOtherTradingDetailsPage(page)
      const companiesRepeatingBlock1Page = new CompaniesRepeatingBlock1Page(page)
      const sectionCompaniesPage = new SectionCompaniesPage(page)
      // Add another item and partially complete
      await anyOtherCompaniesOrBranchesPage.no().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await anyOtherTradingDetailsPage.submit().click()
      await sectionCompaniesPage.companiesListAddLink().click()
      await addCompanyPage.companyOrBranchName().fill('MOD')
      await addCompanyPage.submit().click()
      await companiesRepeatingBlock1Page.cancelAndReturn().click()

      // Navigating to the section summary will redirect to the list collector page
      await page.goto('questionnaire/sections/section-companies/')
      await expect(page).toHaveURL(new RegExp(anyOtherCompaniesOrBranchesPage.pageName))
    })

    test('When the incomplete repeating blocks are completed, Then the user is able to complete the section and is taken to the hub page.', async () => {
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const companiesRepeatingBlock1Page = new CompaniesRepeatingBlock1Page(page)
      const companiesRepeatingBlock2Page = new CompaniesRepeatingBlock2Page(page)
      const hubPage = new HubPage(page)
      const sectionCompaniesPage = new SectionCompaniesPage(page)
      await anyOtherCompaniesOrBranchesPage.no().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await companiesRepeatingBlock1Page.registrationNumber().fill('789')
      await companiesRepeatingBlock1Page.registrationDateDay().fill('3')
      await companiesRepeatingBlock1Page.registrationDateMonth().fill('3')
      await companiesRepeatingBlock1Page.registrationDateYear().fill('2023')
      await companiesRepeatingBlock1Page.submit().click()
      await companiesRepeatingBlock2Page.authorisedTraderUkRadioYes().click()
      await companiesRepeatingBlock2Page.submit().click()
      await anyOtherCompaniesOrBranchesPage.no().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await sectionCompaniesPage.submit().click()
      await expect(page).toHaveURL(new RegExp(hubPage.pageName))
    })

    test('When the user is on the Hub page and has completed the section, Then they are able to add additional companies using the Add link', async () => {
      const addCompanyPage = new AddCompanyPage(page)
      const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
      const companiesRepeatingBlock1Page = new CompaniesRepeatingBlock1Page(page)
      const companiesRepeatingBlock2Page = new CompaniesRepeatingBlock2Page(page)
      const hubPage = new HubPage(page)
      const sectionCompaniesPage = new SectionCompaniesPage(page)
      await hubPage.summaryRowLink('section-companies').click()
      await sectionCompaniesPage.companiesListAddLink().click()
      await addCompanyPage.companyOrBranchName().fill('MOJ')
      await addCompanyPage.submit().click()
      await companiesRepeatingBlock1Page.registrationNumber().fill('789')
      await companiesRepeatingBlock1Page.registrationDateDay().fill('3')
      await companiesRepeatingBlock1Page.registrationDateMonth().fill('3')
      await companiesRepeatingBlock1Page.registrationDateYear().fill('2023')
      await companiesRepeatingBlock1Page.submit().click()
      await companiesRepeatingBlock2Page.authorisedTraderUkRadioYes().click()
      await companiesRepeatingBlock2Page.submit().click()
      await anyOtherCompaniesOrBranchesPage.no().click()
      await anyOtherCompaniesOrBranchesPage.submit().click()
      await sectionCompaniesPage.submit().click()
      await expect(page).toHaveURL(new RegExp(hubPage.pageName))
    })

    test('When the user has completed the list collector section and uses Submit on the hub page, Then the user will be redirected to the next section.', async () => {
      const hubPage = new HubPage(page)
      const responsiblePartyHubPage = new ResponsiblePartyHubPage(page)
      await hubPage.submit().click()
      await expect(page).toHaveURL(new RegExp(responsiblePartyHubPage.pageName))
    })
  })
})
