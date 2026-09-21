import { type Locator, type Page } from '@playwright/test'
import BasePage from './base.page'

export default class SubmitBasePage extends BasePage {
  constructor (page: Page, pageName = 'submit') {
    super(page, pageName)
  }

  url (): string {
    return `/questionnaire/${this.pageName}`
  }

  summary (): Locator {
    return this.locator('.summary')
  }

  summaryRowState (sectionId: string): Locator {
    return this.locator(`[data-qa="${sectionId}"]`)
  }

  summaryShowAllButton (): Locator {
    return this.locator('.ons-accordion__toggle-all')
  }
}
