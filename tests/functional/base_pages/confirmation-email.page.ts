import { type Locator, type Page } from '@playwright/test'
import BasePage from './base.page'

export default class ConfirmationEmailBasePage extends BasePage {
  constructor (page: Page, pageName = 'email-confirmation') {
    super(page, pageName)
  }

  title (): Locator {
    return this.locator('[data-qa="title"]')
  }

  email (): Locator {
    return this.locator('#email')
  }

  errorPanel (): Locator {
    return this.locator('[data-qa="error-body"] div.ons-panel__body > [data-qa="error-list"]')
  }

  feedback (): Locator {
    return this.locator('.ons-feedback')
  }
}
