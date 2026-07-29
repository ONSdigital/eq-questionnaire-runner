import { expect, type Locator, type Page } from '@playwright/test'

export const checkItemsInList = async (itemsExpected: string[], listLabel: (index: number) => Locator): Promise<void> => {
  for (let i = 1; i <= itemsExpected.length; i += 1) {
    await expect(listLabel(i)).toContainText(itemsExpected[i - 1])
  }
}

export const summaryItemComplete = async (summaryItemLabel: Locator, status: boolean): Promise<void> => {
  const icon = summaryItemLabel.locator('.ons-summary__item-title-icon.ons-summary__item-title-icon--check')
  await expect(icon).toHaveCount(status ? 1 : 0)
}

export const listItemComplete = async (listItemLocator: Locator, status: boolean): Promise<void> => {
  const icon = listItemLocator.locator('.ons-list__prefix.ons-list__prefix--icon-check')
  await expect(icon).toHaveCount(status ? 1 : 0)
}

const assertSummaryFunction = (selector: string): ((page: Page, entities: string[]) => Promise<void>) => {
  return async (page: Page, entities: string[]): Promise<void> => {
    const locators = page.locator(selector)
    await expect(locators).toHaveCount(entities.length)

    for (let index = 0; index < entities.length; index += 1) {
      await expect(locators.nth(index)).toHaveText(entities[index])
    }
  }
}

export const assertSummaryValues = assertSummaryFunction('.ons-summary__values')
export const assertSummaryTitles = assertSummaryFunction('.ons-summary__title')
export const assertSummaryItems = assertSummaryFunction('.ons-summary__item--text')

export const repeatingAnswerChangeLink = (page: Page, answerIndex: number): Locator => {
  return page.locator('dd[class="ons-summary__actions"]').nth(answerIndex).locator('a')
}

export const listItemIds = async (page: Page): Promise<string[]> => {
  const values = await page.locator('[data-list-item-id]').evaluateAll((nodes) => nodes.map((node) => node.getAttribute('data-list-item-id') ?? ''))
  return values
}

export const verifyUrlContains = async (page: Page, expectedUrlString: string): Promise<void> => {
  await expect(page).toHaveURL((url) => url.href.includes(expectedUrlString))
}
