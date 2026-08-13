import { type Locator, type Page } from '@playwright/test'
import BasePage from './base.page'

export default class ConfirmEmailBasePage extends BasePage {
  constructor (page: Page, pageName: string = 'confirm-email') {
    super(page, pageName)
  }

  questionTitle (): Locator {
    return this.locator('[data-qa="confirm-email-title"]')
  }

  yes (): Locator {
    return this.locator('#confirm-email-0')
  }

  no (): Locator {
    return this.locator('#confirm-email-1')
  }

  errorPanel (): Locator {
    return this.locator('[data-qa="error-body"] div.ons-panel__body > [data-qa="error-list"]')
  }
}
