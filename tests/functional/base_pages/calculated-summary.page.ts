import { type Locator } from '@playwright/test'
import BasePage from './base.page'

export default class CalculatedSummaryBasePage extends BasePage {
  calculatedSummaryTitle (): Locator {
    return this.locator('[data-qa="calculated-summary-title"]')
  }

  calculatedSummaryQuestion (): Locator {
    return this.locator('[data-qa=calculated-summary-question]')
  }

  calculatedSummaryAnswer (): Locator {
    return this.locator('[data-qa=calculated-summary-answer]')
  }

  summaryItems (): Locator {
    return this.locator('dl.ons-summary__items')
  }
}
