import { type Locator, type Page } from '@playwright/test'
import BasePage from './base.page'

export default class ConfirmationEmailSentBasePage extends BasePage {
  constructor (page: Page, pageName = 'email-confirmation') {
    super(page, pageName)
  }

  confirmationText (): Locator {
    return this.locator('[data-qa="confirmation-text"]')
  }

  sendAnotherEmail (): Locator {
    return this.locator('a[id="send-another-email"]')
  }

  feedback (): Locator {
    return this.locator('.ons-feedback')
  }

  feedbackLink (): Locator {
    return this.locator('.ons-feedback__link')
  }
}
