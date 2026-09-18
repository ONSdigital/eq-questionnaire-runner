import { type Locator, type Page } from '@playwright/test'
import FeedbackBasePage from './feedback-base.page'

export default class FeedbackSentBasePage extends FeedbackBasePage {
  constructor (page: Page, pageName = 'sent') {
    super(page, pageName)
  }

  feedbackThankYouText (): Locator {
    return this.locator('[data-qa="feedback-thank-you-text"]')
  }

  doneButton (): Locator {
    return this.locator('[data-qa="btn-done"]')
  }
}
