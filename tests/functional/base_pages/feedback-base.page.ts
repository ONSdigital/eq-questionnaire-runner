import { type Locator } from '@playwright/test'
import BasePage from './base.page'

export default class FeedbackBasePage extends BasePage {
  url (): string {
    return `/submitted/feedback/${this.pageName}`
  }

  errorHeader (): Locator {
    return this.locator('[data-qa="error-header"]')
  }

  errorNumber (number = 1): Locator {
    return this.locator(`[data-qa="error-link-${String(number)}"] > a`)
  }
}
