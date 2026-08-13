import { type Locator } from '@playwright/test'
import BasePage from './base.page'

export default class QuestionPreviewBasePage extends BasePage {
  url (): string {
    return `/submitted/feedback/${this.pageName}`
  }

  showButton (): Locator {
    return this.locator('[data-ga-category="Preview Survey"]')
  }
}
