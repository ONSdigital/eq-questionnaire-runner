import { test, expect } from '../../fixtures/test'
import type { Locator, Page } from '../../fixtures/test'
import AnyCompaniesOrBranchesDrivingQuestionPage from '../../generated_pages/list_collector_section_summary/any-companies-or-branches.page'
import AnyCompaniesOrBranchesPage from '../../generated_pages/list_collector_section_summary/any-other-companies-or-branches.page'
import AnyCompaniesOrBranchesAddPage from '../../generated_pages/list_collector_section_summary/any-other-companies-or-branches-add.page'
import AnyCompaniesOrBranchesRemovePage from '../../generated_pages/list_collector_section_summary/any-other-companies-or-branches-remove.page'
import SectionSummaryPage from '../../generated_pages/list_collector_section_summary/section-companies-summary.page'
import SectionSummaryTwoPage from '../../generated_pages/list_collector_section_summary/section-household-summary.page'
import UkBasedPage from '../../generated_pages/list_collector_section_summary/confirmation-checkbox.page'
import ListCollectorPage from '../../generated_pages/list_collector_section_summary/list-collector.page'
import HouseholderCheckboxPage from '../../generated_pages/list_collector_section_summary/householder-checkbox.page'
import SubmitPage from '../../generated_pages/list_collector_section_summary/submit.page'
import ThankYouPage from '../../base_pages/thank-you.page'
import ViewSubmittedResponsePage from '../../generated_pages/list_collector_section_summary/view-submitted-response.page'
import { listItemIds } from '../../helpers'

test.describe('List Collector Section Summary and Summary Items', () => {
  test.describe('Given I launch the test list collector section summary items survey', () => {
    test.beforeEach(async ({ openQuestionnaire }) => {
      await openQuestionnaire('test_list_collector_section_summary.json')
    })

    test('When I get to the section summary, Then the driving question should be visible.', async ({ page }) => {
      const sectionSummaryPage = new SectionSummaryPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesNo(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      await expect(sectionSummaryPage.anyCompaniesOrBranchesQuestion()).toBeVisible()
      await expect(sectionSummaryPage.anyCompaniesOrBranchesAnswer()).toHaveText('Yes')
    })

    test('When I add my own item, Then the item should be visible on the section summary and have correct values', async ({ page }) => {
      const sectionSummaryPage = new SectionSummaryPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesNo(page)
      await expect(sectionSummaryPage.companiesListLabel(1)).toContainText('Name of UK company or branch')
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__values').nth(0)).toContainText('Company A')
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__values').nth(1)).toContainText('123')
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__values').nth(2)).toContainText('Yes')
      const listItemId = (await listItemIds(page))[0]
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__actions a').nth(0)).toHaveAttribute(
        'href',
        new RegExp(`return_to=section-summary(&|&amp;)return_to_answer_id=${listItemId}#company-or-branch-name`)
      )
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__actions a').nth(1)).toHaveAttribute(
        'href',
        new RegExp(`/questionnaire/companies/${listItemId}/remove-company/\\?return_to=section-summary`)
      )
    })

    test('When I add multiple items, Then all the items should be visible on the section summary and have correct values', async ({ page }) => {
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesYes(page)
      await addCompany(page, 'Company B', '456', false)
      await anyMoreCompaniesYes(page)
      await addCompany(page, 'Company C', '789', true)
      await anyMoreCompaniesNo(page)
      await answerUkBasedQuestion(page)
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__values').nth(0)).toContainText('Company A')
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__values').nth(1)).toContainText('123')
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__values').nth(2)).toContainText('Yes')
      await expect(companiesListRowItem(page, 2).locator('.ons-summary__values').nth(0)).toContainText('Company B')
      await expect(companiesListRowItem(page, 2).locator('.ons-summary__values').nth(1)).toContainText('456')
      await expect(companiesListRowItem(page, 2).locator('.ons-summary__values').nth(2)).toContainText('No')
      await expect(companiesListRowItem(page, 3).locator('.ons-summary__values').nth(0)).toContainText('Company C')
      await expect(companiesListRowItem(page, 3).locator('.ons-summary__values').nth(1)).toContainText('789')
      await expect(companiesListRowItem(page, 3).locator('.ons-summary__values').nth(2)).toContainText('Yes')
    })

    test('When I remove an item, Then the list of answers should no longer be visible on the section summary.', async ({ page }) => {
      const sectionSummaryPage = new SectionSummaryPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesNo(page)
      await removeFirstCompany(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      await expect(page.locator('#main-content')).not.toContainText('Company A')
      await expect(sectionSummaryPage.companiesListEditLink(1)).not.toBeVisible()
      await expect(sectionSummaryPage.companiesListRemoveLink(1)).not.toBeVisible()
    })

    test('When I remove an item but the list collector is still on the path, Then the placeholder text should be visible on the section summary.', async ({
      page
    }) => {
      const sectionSummaryPage = new SectionSummaryPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesNo(page)
      await removeFirstCompany(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      await expect(page.locator('#main-content')).toContainText('No UK company or branch added')
    })

    test('When I have multiple items in the list and I remove the first item, Then only the item that was not deleted should be visible on the section summary.', async ({
      page
    }) => {
      const sectionSummaryPage = new SectionSummaryPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesYes(page)
      await addCompany(page, 'Company B', '234', true)
      await anyMoreCompaniesNo(page)
      await removeFirstCompany(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      await expect(page.locator('#main-content')).not.toContainText('Company A')
      await expect(page.locator('#main-content')).toContainText('Company B')
    })

    test('When I add an item and relevant data and answer No on the additional items page, Then I should get to the section summary page.', async ({
      page
    }) => {
      const sectionSummaryPage = new SectionSummaryPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesNo(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      await expect(sectionSummaryPage.companiesListAddLink()).toBeVisible()
    })

    test('When I add an item and relevant data and answer Yes on the additional items page, Then I should be able to and add a new item and relevant data.', async ({
      page
    }) => {
      const anyCompaniesOrBranchesAddPage = new AnyCompaniesOrBranchesAddPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesYes(page)
      await expect(anyCompaniesOrBranchesAddPage.companyOrBranchName()).toBeVisible()
      await expect(anyCompaniesOrBranchesAddPage.registrationNumber()).toBeVisible()
      await expect(anyCompaniesOrBranchesAddPage.authorisedInsurerRadioYes()).toBeVisible()
      await expect(anyCompaniesOrBranchesAddPage.heading()).toHaveText('Give details about the company or branch that undertakes general insurance business')
    })

    test('When I add an item and relevant data, Then I should be able to edit that item from the section summary page.', async ({ page }) => {
      const anyCompaniesOrBranchesAddPage = new AnyCompaniesOrBranchesAddPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesNo(page)
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__values').nth(0)).toContainText('Company A')
      await sectionSummaryPage.companiesListEditLink(1).click()
      await expect(page).toHaveURL(/edit-company\/\?return_to=section-summary/)
      await expect(anyCompaniesOrBranchesAddPage.companyOrBranchName()).toHaveValue('Company A')
    })

    test('When I edit an item after adding it, Then I should be redirected to the summary page', async ({ page }) => {
      const anyCompaniesOrBranchesAddPage = new AnyCompaniesOrBranchesAddPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesNo(page)
      await expect(companiesListRowItem(page, 1)).toContainText('Company A')
      await sectionSummaryPage.companiesListEditLink(1).click()
      await anyCompaniesOrBranchesAddPage.companyOrBranchName().fill('Changed Company')
      await anyCompaniesOrBranchesAddPage.submit().click()
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      await expect(companiesListRowItem(page, 1)).toContainText('Changed Company')
    })

    test('When no item is added but I change my answer to the driving question to Yes, Then I should be able to add a new item.', async ({ page }) => {
      const sectionSummaryPage = new SectionSummaryPage(page)
      await drivingQuestionNo(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      await expect(sectionSummaryPage.companiesListEditLink(1)).not.toBeVisible()
      await expect(sectionSummaryPage.companiesListRemoveLink(1)).not.toBeVisible()
      await expect(sectionSummaryPage.companiesListAddLink()).not.toBeVisible()
      await sectionSummaryPage.anyCompaniesOrBranchesAnswerEdit().click()
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesNo(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      await expect(sectionSummaryPage.companiesListEditLink(1)).toBeVisible()
      await expect(sectionSummaryPage.companiesListRemoveLink(1)).toBeVisible()
      await expect(sectionSummaryPage.companiesListAddLink()).toBeVisible()
    })

    test('When I add an item and relevant data but change my answer to the driving question to No, Then I should see the original item on the summary if change the answer back to Yes.', async ({
      page
    }) => {
      const sectionSummaryPage = new SectionSummaryPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesNo(page)
      await expect(companiesListRowItem(page, 1)).toContainText('Company A')
      await sectionSummaryPage.anyCompaniesOrBranchesAnswerEdit().click()
      await drivingQuestionNo(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      await expect(sectionSummaryPage.companiesListEditLink(1)).not.toBeVisible()
      await expect(sectionSummaryPage.companiesListRemoveLink(1)).not.toBeVisible()
      await expect(page.locator('#main-content')).not.toContainText('No UK company or branch added')
      await expect(sectionSummaryPage.companiesListAddLink()).not.toBeVisible()
      await sectionSummaryPage.anyCompaniesOrBranchesAnswerEdit().click()
      await drivingQuestionYes(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      await expect(companiesListRowItem(page, 1)).toContainText('Company A')
      await expect(sectionSummaryPage.companiesListEditLink(1)).toBeVisible()
      await expect(sectionSummaryPage.companiesListRemoveLink(1)).toBeVisible()
      await expect(sectionSummaryPage.companiesListAddLink()).toBeVisible()
    })

    test('When I add another company from the summary page, Then I am asked if I want to add any more company before accessing the section summary', async ({
      page
    }) => {
      const anyCompaniesOrBranchesPage = new AnyCompaniesOrBranchesPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesNo(page)
      await sectionSummaryPage.companiesListAddLink().click()
      await expect(page).toHaveURL(/\/questionnaire\/companies\/add-company/)
      await expect(page).toHaveURL(/\?return_to=section-summary/)
      await addCompany(page, 'Company B', '456', true)
      await expect(page).toHaveURL(new RegExp(anyCompaniesOrBranchesPage.url()))
      await expect(page.locator('#main-content')).toContainText('Company A')
      await expect(page.locator('#main-content')).toContainText('Company B')
      await anyMoreCompaniesNo(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
    })

    test('When I add three companies, Then I am prompted with the confirmation question', async ({ page }) => {
      const ukBasedPage = new UkBasedPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesYes(page)
      await addCompany(page, 'Company B', '456', true)
      await anyMoreCompaniesYes(page)
      await addCompany(page, 'Company C', '789', true)
      await anyMoreCompaniesNo(page)
      await expect(page).toHaveURL(new RegExp(ukBasedPage.url()))
    })

    test('When I add less than 3 companies, Then I am not prompted with the confirmation question', async ({ page }) => {
      const sectionSummaryPage = new SectionSummaryPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesYes(page)
      await addCompany(page, 'Company B', '456', true)
      await anyMoreCompaniesNo(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
    })

    test('When I add more than 3 companies, Then I am not prompted with the confirmation question', async ({ page }) => {
      const sectionSummaryPage = new SectionSummaryPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesYes(page)
      await addCompany(page, 'Company B', '456', true)
      await anyMoreCompaniesYes(page)
      await addCompany(page, 'Company C', '789', true)
      await anyMoreCompaniesYes(page)
      await addCompany(page, 'Company D', '135', true)
      await anyMoreCompaniesNo(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
    })

    test(
      'When I add another company from the summary page, and the amount then totals to 3, ' +
        "and the confirmation question hasn't been previously answered, Then I am prompted with the confirmation question",
      async ({ page }) => {
        const sectionSummaryPage = new SectionSummaryPage(page)
        const ukBasedPage = new UkBasedPage(page)
        await drivingQuestionYes(page)
        await addCompany(page, 'Company A', '123', true)
        await anyMoreCompaniesYes(page)
        await addCompany(page, 'Company B', '456', true)
        await anyMoreCompaniesNo(page)
        await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
        await sectionSummaryPage.companiesListAddLink().click()
        await expect(page).toHaveURL(/\/questionnaire\/companies\/add-company/)
        await expect(page).toHaveURL(/\?return_to=section-summary/)
        await addCompany(page, 'Company C', '234', true)
        await anyMoreCompaniesNo(page)
        await expect(page).toHaveURL(new RegExp(ukBasedPage.url()))
        await answerUkBasedQuestion(page)
        await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      }
    )

    test(
      'When I remove a company from the summary page, and the amount then totals to 3, ' +
        "and the confirmation question hasn't been previously answered, Then I am prompted with the confirmation question",
      async ({ page }) => {
        const sectionSummaryPage = new SectionSummaryPage(page)
        const ukBasedPage = new UkBasedPage(page)
        await drivingQuestionYes(page)
        await addCompany(page, 'Company A', '123', true)
        await anyMoreCompaniesYes(page)
        await addCompany(page, 'Company B', '456', true)
        await anyMoreCompaniesYes(page)
        await addCompany(page, 'Company C', '234', true)
        await anyMoreCompaniesYes(page)
        await addCompany(page, 'Company D', '345', true)
        await anyMoreCompaniesNo(page)
        await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
        await removeFirstCompany(page)
        await expect(page).toHaveURL(new RegExp(ukBasedPage.url()))
        await answerUkBasedQuestion(page)
        await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      }
    )

    test('When I get to the summary page, Then the summary should be displayed as expected with change links', async ({ page }) => {
      const householderCheckboxPage = new HouseholderCheckboxPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      const sectionSummaryTwoPage = new SectionSummaryTwoPage(page)
      const submitPage = new SubmitPage(page)
      const ukBasedPage = new UkBasedPage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesYes(page)
      await addCompany(page, 'Company B', '456', true)
      await anyMoreCompaniesYes(page)
      await addCompany(page, 'Company C', '234', true)
      await anyMoreCompaniesNo(page)
      await expect(page).toHaveURL(new RegExp(ukBasedPage.url()))
      await answerUkBasedQuestion(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      await sectionSummaryPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await householderCheckboxPage.no().click()
      await householderCheckboxPage.submit().click()
      await sectionSummaryTwoPage.submit().click()

      await expect(page).toHaveURL(new RegExp(submitPage.url()))
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__values').nth(0)).toContainText('Company A')
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__values').nth(1)).toContainText('123')
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__actions').nth(0)).toContainText('Change')
      await expect(companiesListRowItem(page, 2).locator('.ons-summary__values').nth(0)).toContainText('Company B')
      await expect(companiesListRowItem(page, 2).locator('.ons-summary__values').nth(1)).toContainText('456')
      await expect(companiesListRowItem(page, 2).locator('.ons-summary__actions').nth(0)).toContainText('Change')
      await expect(companiesListRowItem(page, 3).locator('.ons-summary__values').nth(0)).toContainText('Company C')
      await expect(companiesListRowItem(page, 3).locator('.ons-summary__values').nth(1)).toContainText('234')
      await expect(companiesListRowItem(page, 3).locator('.ons-summary__actions').nth(0)).toContainText('Change')
      await expect(submitPage.householderCheckboxAnswer()).toContainText('No')
      await expect(page.locator('#main-content')).toContainText('Add another UK company or branch')
      await expect(page.locator('#main-content')).toContainText('Remove')
    })

    test('When I get to the view submitted response page, Then the summary should be displayed as expected without any change or remove links', async ({
      page
    }) => {
      const householderCheckboxPage = new HouseholderCheckboxPage(page)
      const listCollectorPage = new ListCollectorPage(page)
      const sectionSummaryPage = new SectionSummaryPage(page)
      const sectionSummaryTwoPage = new SectionSummaryTwoPage(page)
      const submitPage = new SubmitPage(page)
      const thankYouPage = new ThankYouPage(page)
      const ukBasedPage = new UkBasedPage(page)
      const viewSubmittedResponsePage = new ViewSubmittedResponsePage(page)
      await drivingQuestionYes(page)
      await addCompany(page, 'Company A', '123', true)
      await anyMoreCompaniesYes(page)
      await addCompany(page, 'Company B', '456', true)
      await anyMoreCompaniesYes(page)
      await addCompany(page, 'Company C', '234', true)
      await anyMoreCompaniesNo(page)
      await expect(page).toHaveURL(new RegExp(ukBasedPage.url()))
      await answerUkBasedQuestion(page)
      await expect(page).toHaveURL(new RegExp(sectionSummaryPage.url()))
      await sectionSummaryPage.submit().click()
      await listCollectorPage.no().click()
      await listCollectorPage.submit().click()
      await householderCheckboxPage.no().click()
      await householderCheckboxPage.submit().click()
      await sectionSummaryTwoPage.submit().click()
      await submitPage.submit().click()
      await expect(thankYouPage.title()).toContainText('Thank you for completing the Test List Collector Section Summary')
      await thankYouPage.savePrintAnswersLink().click()

      await expect(page).toHaveURL(new RegExp(viewSubmittedResponsePage.pageName))
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__values').nth(0)).toContainText('Company A')
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__values').nth(1)).toContainText('123')
      await expect(companiesListRowItem(page, 1).locator('.ons-summary__values').nth(2)).toContainText('Yes')
      await expect(companiesListRowItem(page, 2).locator('.ons-summary__values').nth(0)).toContainText('Company B')
      await expect(companiesListRowItem(page, 2).locator('.ons-summary__values').nth(1)).toContainText('456')
      await expect(companiesListRowItem(page, 2).locator('.ons-summary__values').nth(2)).toContainText('Yes')
      await expect(companiesListRowItem(page, 3).locator('.ons-summary__values').nth(0)).toContainText('Company C')
      await expect(companiesListRowItem(page, 3).locator('.ons-summary__values').nth(1)).toContainText('234')
      await expect(companiesListRowItem(page, 3).locator('.ons-summary__values').nth(2)).toContainText('Yes')
      await expect(page.locator('#main-content')).not.toContainText('Change')
      await expect(page.locator('#main-content')).not.toContainText('Remove')
      await expect(page.locator('#main-content')).not.toContainText('Add another UK company or branch')
    })
  })
})

const drivingQuestionYes = async (page: Page): Promise<void> => {
  const anyCompaniesOrBranchesDrivingQuestionPage = new AnyCompaniesOrBranchesDrivingQuestionPage(page)
  await anyCompaniesOrBranchesDrivingQuestionPage.yes().click()
  await anyCompaniesOrBranchesDrivingQuestionPage.submit().click()
}

const drivingQuestionNo = async (page: Page): Promise<void> => {
  const anyCompaniesOrBranchesDrivingQuestionPage = new AnyCompaniesOrBranchesDrivingQuestionPage(page)
  await anyCompaniesOrBranchesDrivingQuestionPage.no().click()
  await anyCompaniesOrBranchesDrivingQuestionPage.submit().click()
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
  const anyCompaniesOrBranchesPage = new AnyCompaniesOrBranchesPage(page)
  await anyCompaniesOrBranchesPage.yes().click()
  await anyCompaniesOrBranchesPage.submit().click()
}

const anyMoreCompaniesNo = async (page: Page): Promise<void> => {
  const anyCompaniesOrBranchesPage = new AnyCompaniesOrBranchesPage(page)
  await anyCompaniesOrBranchesPage.no().click()
  await anyCompaniesOrBranchesPage.submit().click()
}

const removeFirstCompany = async (page: Page): Promise<void> => {
  const sectionSummaryPage = new SectionSummaryPage(page)
  const anyCompaniesOrBranchesRemovePage = new AnyCompaniesOrBranchesRemovePage(page)
  await sectionSummaryPage.companiesListRemoveLink(1).click()
  await anyCompaniesOrBranchesRemovePage.yes().click()
  await anyCompaniesOrBranchesRemovePage.submit().click()
}

const answerUkBasedQuestion = async (page: Page): Promise<void> => {
  const ukBasedPage = new UkBasedPage(page)
  await ukBasedPage.yes().click()
  await ukBasedPage.submit().click()
}

const companiesListRowItem = (page: Page, row: number): Locator => {
  return page.locator(`#group-companies-1 .ons-summary__items .ons-summary__item:nth-of-type(${row})`)
}
