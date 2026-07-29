import { type Locator } from '@playwright/test'
import BasePage from './base.page'

export default class GrandCalculatedSummaryBasePage extends BasePage {
  grandCalculatedSummaryTitle (): Locator {
    return this.locator('[data-qa="grand-calculated-summary-title"]')
  }

  grandCalculatedSummaryQuestion (): Locator {
    return this.locator('[data-qa=grand-calculated-summary-question]')
  }

  grandCalculatedSummaryAnswer (): Locator {
    return this.locator('[data-qa=grand-calculated-summary-answer]')
  }
}
