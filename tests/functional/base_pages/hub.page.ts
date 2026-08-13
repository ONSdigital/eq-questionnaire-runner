import { type Locator, type Page } from '@playwright/test'
import BasePage from './base.page'

export default class HubBasePage extends BasePage {
  constructor (page: Page, pageName = 'questionnaire') {
    super(page, pageName)
  }

  url (): string {
    return `/${this.pageName}/`
  }

  summaryItems (): Locator {
    return this.locator('dl.ons-summary__items')
  }

  summaryRowState (sectionId: string): Locator {
    return this.locator(`[data-qa="hub-row-${sectionId}-state"]`)
  }

  summaryRowLink (sectionId: string): Locator {
    return this.locator(`[data-qa="hub-row-${sectionId}-link"]`)
  }

  summaryRowTitle (sectionId: string): Locator {
    return this.locator(`[data-qa="hub-row-${sectionId}-title"]`)
  }
}
