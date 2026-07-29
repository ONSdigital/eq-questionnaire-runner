import { type Locator, type Page } from '@playwright/test'
import FeedbackBasePage from './feedback-base.page'

export default class FeedbackPage extends FeedbackBasePage {
  constructor (page: Page, pageName = 'send') {
    super(page, pageName)
  }

  feedbackTitle (): Locator {
    return this.locator('[data-qa="feedback-title"]')
  }

  feedbackType (): Locator {
    return this.locator('#feedback-type')
  }

  feedbackTypePageDesignAndStructure (): Locator {
    return this.locator('#feedback-type-1')
  }

  feedbackTypeGeneralFeedback (): Locator {
    return this.locator('#feedback-type-2')
  }

  feedbackText (): Locator {
    return this.locator('#feedback-text')
  }

  errorPanel (): Locator {
    return this.locator('[data-qa="error-body"]')
  }
}
