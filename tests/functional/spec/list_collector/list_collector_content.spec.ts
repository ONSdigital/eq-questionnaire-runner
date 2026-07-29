import { test, expect } from '../../fixtures/test'
import type { Page } from '../../fixtures/test'
import AnyOtherCompaniesOrBranchesPage from '../../generated_pages/list_collector_content_page/any-other-companies-or-branches.page'
import AnyCompaniesOrBranchesAddPage from '../../generated_pages/list_collector_content_page/any-other-companies-or-branches-add.page'
import AnyCompaniesOrBranchesRemovePage from '../../generated_pages/list_collector_content_page/any-other-companies-or-branches-remove.page'
import AnyCompaniesOrBranchesPage from '../../generated_pages/list_collector_content_page/any-companies-or-branches.page'
import CompaniesSummaryPage from '../../generated_pages/list_collector_content_page/section-companies-summary.page'
import HubPage from '../../base_pages/hub.page'
import ResponsiblePartyQuestionPage from '../../generated_pages/list_collector_content_page/responsible-party.page'
import ListCollectorFirstRepeatingBlockPage from '../../generated_pages/list_collector_content_page/companies-repeating-block-1-repeating-block.page'
import ListCollectorSecondRepeatingBlockPage from '../../generated_pages/list_collector_content_page/companies-repeating-block-2-repeating-block.page'
import ListCollectorContentPage from '../../generated_pages/list_collector_content_page/list-collector-content.page'
import ListCollectorContentSectionSummaryPage from '../../generated_pages/list_collector_content_page/section-list-collector-contents-summary.page'
import ConfirmationCheckboxPage from '../../generated_pages/list_collector_content_page/confirmation-checkbox.page'
import { listItemComplete, verifyUrlContains } from '../../helpers'

test.describe('List Collector Section Summary and Summary Items', () => {
  test.describe('Given I launch the test list collector section summary items survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_list_collector_content_page.json')
    })

    test('When I get to the Hub, Then from there the next block in list collector content section should be list collector content page.', async ({ page }) => {
      const hubPage = new HubPage(page)
      const listCollectorContentPage = new ListCollectorContentPage(page)
      const responsiblePartyQuestionPage = new ResponsiblePartyQuestionPage(page)
      await fillInListCollectorSection(page)
      await verifyUrlContains(page, hubPage.url())
      await expect(hubPage.summaryRowState('section-list-collector-contents')).toHaveText('Not started')
      await hubPage.submit().click()
      await responsiblePartyQuestionPage.yes().click()
      await responsiblePartyQuestionPage.submit().click()
      await verifyUrlContains(page, listCollectorContentPage.url())
    })

    test('When I get to the list collector content page, Then the relevant content and button is displayed.', async ({ page }) => {
      const hubPage = new HubPage(page)
      const listCollectorContentPage = new ListCollectorContentPage(page)
      const responsiblePartyQuestionPage = new ResponsiblePartyQuestionPage(page)
      await fillInListCollectorSection(page)
      await hubPage.submit().click()
      await responsiblePartyQuestionPage.yes().click()
      await responsiblePartyQuestionPage.submit().click()
      await expect(listCollectorContentPage.heading()).toContainText('Companies')
      await expect(page.locator('#main-content > p')).toHaveText(
        'You have previously reported the following companies. Press continue to updated registration and trading information.'
      )
      await expect(page.locator('#main-content > #guidance-1')).toContainText('Include all companies')
      await expect(page.locator('#main-content > #definition')).toContainText('Companies definition')
      await expect(listCollectorContentPage.submit()).toHaveText('Continue')
    })

    test('When I get to list collector content block section, Then I should be able to complete repeating blocks and get to the summary.', async ({ page }) => {
      const hubPage = new HubPage(page)
      const listCollectorContentPage = new ListCollectorContentPage(page)
      const listCollectorContentSectionSummaryPage = new ListCollectorContentSectionSummaryPage(page)
      const responsiblePartyQuestionPage = new ResponsiblePartyQuestionPage(page)
      await fillInListCollectorSection(page)
      await hubPage.submit().click()
      await responsiblePartyQuestionPage.yes().click()
      await responsiblePartyQuestionPage.submit().click()
      await listCollectorContentPage.submit().click()
      await completeRepeatingBlocks(page, 123, 1, 1, 1990, true, true)
      await listCollectorContentPage.submit().click()
      await completeRepeatingBlocks(page, 456, 1, 1, 1990, true, true)
      await listCollectorContentPage.submit().click()
      await verifyUrlContains(page, listCollectorContentSectionSummaryPage.url())
    })

    test('When I fill in first item repeating blocks, Then after going back to the hub the section should be in progress.', async ({ page }) => {
      const hubPage = new HubPage(page)
      const listCollectorContentPage = new ListCollectorContentPage(page)
      const responsiblePartyQuestionPage = new ResponsiblePartyQuestionPage(page)
      await fillInListCollectorSection(page)
      await hubPage.submit().click()
      await responsiblePartyQuestionPage.yes().click()
      await responsiblePartyQuestionPage.submit().click()
      await listCollectorContentPage.submit().click()
      await completeRepeatingBlocks(page, 123, 1, 1, 1990, true, true)
      await listCollectorContentPage.previous().click()
      await responsiblePartyQuestionPage.previous().click()
      await expect(hubPage.summaryRowState('section-list-collector-contents')).toHaveText('Partially completed')
    })

    test('When I fill in both items repeating blocks, Then after going back to the hub the section should be completed.', async ({ page }) => {
      const hubPage = new HubPage(page)
      const listCollectorContentPage = new ListCollectorContentPage(page)
      const listCollectorContentSectionSummaryPage = new ListCollectorContentSectionSummaryPage(page)
      const responsiblePartyQuestionPage = new ResponsiblePartyQuestionPage(page)
      await fillInListCollectorSection(page)
      await hubPage.submit().click()
      await responsiblePartyQuestionPage.yes().click()
      await responsiblePartyQuestionPage.submit().click()
      await listCollectorContentPage.submit().click()
      await completeRepeatingBlocks(page, 123, 1, 1, 1990, true, true)
      await listCollectorContentPage.submit().click()
      await completeRepeatingBlocks(page, 456, 1, 1, 1990, true, true)
      await listCollectorContentPage.submit().click()
      await listCollectorContentSectionSummaryPage.previous().click()
      await listCollectorContentPage.previous().click()
      await responsiblePartyQuestionPage.previous().click()
      await expect(hubPage.summaryRowState('section-list-collector-contents')).toHaveText('Completed')
    })

    test('When I complete both sections then add another item, The list collector content block reverts to in progress and the new repeating blocks need completing', async ({
      page
    }) => {
      const companiesSummaryPage = new CompaniesSummaryPage(page)
      const confirmationCheckboxPage = new ConfirmationCheckboxPage(page)
      const hubPage = new HubPage(page)
      const listCollectorContentPage = new ListCollectorContentPage(page)
      const listCollectorContentSectionSummaryPage = new ListCollectorContentSectionSummaryPage(page)
      const listCollectorFirstRepeatingBlockPage = new ListCollectorFirstRepeatingBlockPage(page)
      await completeBothSections(page)
      await expect(hubPage.summaryRowState('section-list-collector-contents')).toHaveText('Completed')
      await hubPage.summaryRowLink('section-companies').click()
      await verifyUrlContains(page, companiesSummaryPage.pageName)
      await companiesSummaryPage.companiesListAddLink().click()
      await addCompany(page, 'Company C', '789', false)
      await anyMoreCompaniesNo(page)
      await confirmationCheckboxPage.yes().click()
      await confirmationCheckboxPage.submit().click()
      await companiesSummaryPage.submit().click()
      await expect(hubPage.summaryRowState('section-list-collector-contents')).toHaveText('Partially completed')
      await hubPage.submit().click()
      await verifyUrlContains(page, listCollectorContentPage.pageName)
      await listItemComplete(listCollectorContentPage.listLabel(1), true)
      await listItemComplete(listCollectorContentPage.listLabel(2), true)
      await listItemComplete(listCollectorContentPage.listLabel(3), false)
      await listCollectorContentPage.submit().click()
      await verifyUrlContains(page, listCollectorFirstRepeatingBlockPage.pageName)
      await completeRepeatingBlocks(page, 666, 2, 5, 1995, true, true)
      await listItemComplete(listCollectorContentPage.listLabel(3), true)
      await listCollectorContentPage.submit().click()
      await listCollectorContentSectionSummaryPage.submit().click()
      await expect(hubPage.summaryRowState('section-list-collector-contents')).toHaveText('Completed')
    })

    // :TODO: Currently, this is expected behaviour, if list collector content blocks no longer need revisiting after removing items, this test needs updating.
    test('When I complete both sections then remove a list item item, Then the list collector content block reverts to in progress the list summary is revisited', async ({
      page
    }) => {
      const anyCompaniesOrBranchesRemovePage = new AnyCompaniesOrBranchesRemovePage(page)
      const companiesSummaryPage = new CompaniesSummaryPage(page)
      const hubPage = new HubPage(page)
      const listCollectorContentPage = new ListCollectorContentPage(page)
      const listCollectorContentSectionSummaryPage = new ListCollectorContentSectionSummaryPage(page)
      await completeBothSections(page)
      await expect(hubPage.summaryRowState('section-list-collector-contents')).toHaveText('Completed')
      await hubPage.summaryRowLink('section-companies').click()
      await companiesSummaryPage.companiesListRemoveLink(1).click()
      await anyCompaniesOrBranchesRemovePage.yes().click()
      await anyCompaniesOrBranchesRemovePage.submit().click()
      await companiesSummaryPage.submit().click()
      await expect(hubPage.summaryRowState('section-list-collector-contents')).toHaveText('Partially completed')
      await hubPage.submit().click()
      await listItemComplete(listCollectorContentPage.listLabel(1), true)
      await listCollectorContentPage.submit().click()
      await verifyUrlContains(page, listCollectorContentSectionSummaryPage.pageName)
      await listCollectorContentSectionSummaryPage.submit().click()
      await expect(hubPage.summaryRowState('section-list-collector-contents')).toHaveText('Completed')
    })
  })
})

const fillInListCollectorSection = async (page: Page): Promise<void> => {
  const anyCompaniesOrBranchesPage = new AnyCompaniesOrBranchesPage(page)
  const companiesSummaryPage = new CompaniesSummaryPage(page)
  await anyCompaniesOrBranchesPage.yes().click()
  await anyCompaniesOrBranchesPage.submit().click()
  await addCompany(page, 'Company A', '123', true)
  await anyMoreCompaniesYes(page)
  await addCompany(page, 'Company B', '456', true)
  await anyMoreCompaniesNo(page)
  await companiesSummaryPage.submit().click()
}

const completeBothSections = async (page: Page): Promise<void> => {
  const hubPage = new HubPage(page)
  const listCollectorContentPage = new ListCollectorContentPage(page)
  const listCollectorContentSectionSummaryPage = new ListCollectorContentSectionSummaryPage(page)
  const responsiblePartyQuestionPage = new ResponsiblePartyQuestionPage(page)
  await fillInListCollectorSection(page)
  await hubPage.submit().click()
  await responsiblePartyQuestionPage.yes().click()
  await responsiblePartyQuestionPage.submit().click()
  await listCollectorContentPage.submit().click()
  await completeRepeatingBlocks(page, 654, 2, 6, 1999, true, true)
  await listCollectorContentPage.submit().click()
  await completeRepeatingBlocks(page, 655, 12, 1, 1989, true, false)
  await listCollectorContentPage.submit().click()
  await listCollectorContentSectionSummaryPage.submit().click()
}

const completeRepeatingBlocks = async (
  page: Page,
  registrationNumber: number,
  day: number,
  month: number,
  year: number,
  authorisedUk: boolean,
  authorisedEu: boolean
): Promise<void> => {
  const listCollectorFirstRepeatingBlockPage = new ListCollectorFirstRepeatingBlockPage(page)
  const listCollectorSecondRepeatingBlockPage = new ListCollectorSecondRepeatingBlockPage(page)
  await listCollectorFirstRepeatingBlockPage.registrationNumberRepeatingBlock().fill(String(registrationNumber))
  await listCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockDay().fill(String(day))
  await listCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockMonth().fill(String(month))
  await listCollectorFirstRepeatingBlockPage.registrationDateRepeatingBlockYear().fill(String(year))
  await listCollectorFirstRepeatingBlockPage.submit().click()
  if (authorisedUk) {
    await listCollectorSecondRepeatingBlockPage.authorisedTraderUkRadioRepeatingBlockYes().click()
  } else {
    await listCollectorSecondRepeatingBlockPage.authorisedTraderUkRadioRepeatingBlockNo().click()
  }
  if (authorisedEu) {
    await listCollectorSecondRepeatingBlockPage.authorisedTraderEuRadioRepeatingBlockYes().click()
  } else {
    await listCollectorSecondRepeatingBlockPage.authorisedTraderEuRadioRepeatingBlockNo().click()
  }
  await listCollectorSecondRepeatingBlockPage.submit().click()
}
const addCompany = async (page: Page, name: string, number: string, authorised: boolean): Promise<void> => {
  const anyCompaniesOrBranchesAddPage = new AnyCompaniesOrBranchesAddPage(page)
  await anyCompaniesOrBranchesAddPage.companyOrBranchName().fill(name)
  await anyCompaniesOrBranchesAddPage.registrationNumber().fill(number)
  if (authorised) {
    await anyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes().click()
  } else {
    await anyCompaniesOrBranchesAddPage.authorisedInsurerRadioNo().click()
  }
  await anyCompaniesOrBranchesAddPage.submit().click()
}

const anyMoreCompaniesYes = async (page: Page): Promise<void> => {
  const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
  await anyOtherCompaniesOrBranchesPage.yes().click()
  await anyOtherCompaniesOrBranchesPage.submit().click()
}

const anyMoreCompaniesNo = async (page: Page): Promise<void> => {
  const anyOtherCompaniesOrBranchesPage = new AnyOtherCompaniesOrBranchesPage(page)
  await anyOtherCompaniesOrBranchesPage.no().click()
  await anyOtherCompaniesOrBranchesPage.submit().click()
}
