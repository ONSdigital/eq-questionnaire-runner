import { type Locator, type Page } from '@playwright/test'
import BasePage from './base.page'

export default class ThankYouBasePage extends BasePage {
  constructor (page: Page, pageName = 'thank-you') {
    super(page, pageName)
  }

  url (): string {
    return `/submitted/${this.pageName}`
  }

  title (): Locator {
    return this.locator('[data-qa="title"]')
  }

  viewAnswersTitle (): Locator {
    return this.locator('[data-qa="view-submitted-response-title"]')
  }

  viewAnswersLink (): Locator {
    return this.locator('a[id="view-submitted-response-link"]')
  }

  viewSubmittedWarning (): Locator {
    return this.locator('[id="view-submitted-response-warning"]')
  }

  viewSubmittedGuidance (): Locator {
    return this.locator('[id="view-submitted-response-guidance"]')
  }

  viewSubmittedCountdown (): Locator {
    return this.locator('[id="view-submitted-response-countdown"]')
  }

  metadata (): Locator {
    return this.locator('.ons-description-list')
  }

  exitButton (): Locator {
    return this.locator('[data-qa="btn-exit"]')
  }

  savePrintAnswersLink (): Locator {
    return this.locator('[id="view-submitted-response-link"]')
  }

  email (): Locator {
    return this.locator('#email')
  }

  errorPanel (): Locator {
    return this.locator('[data-qa="error-body"]')
  }

  feedback (): Locator {
    return this.locator('.ons-feedback')
  }

  feedbackLink (): Locator {
    return this.locator('.ons-feedback__link')
  }
}
