import { type Locator } from '@playwright/test'
import BasePage from './base.page'

export default class QuestionBasePage extends BasePage {
  url (): string {
    return `/questionnaire/${this.pageName}`
  }

  questionText (): Locator {
    return this.heading()
  }

  alert (): Locator {
    return this.locator('[data-qa="error-body"]')
  }

  error (): Locator {
    return this.locator('.ons-js-inpagelink')
  }

  legend (): Locator {
    return this.locator('legend')
  }

  errorHeader (): Locator {
    return this.locator('[data-qa="error-header"]')
  }

  errorNumber (number = 1): Locator {
    return this.locator(`[data-qa="error-link-${String(number)}"] > a`)
  }

  cancelAndReturn (): Locator {
    return this.locator('a[id="cancel-and-return"]')
  }

  individualResponseGuidance (): Locator {
    return this.locator('[data-qa="individual-response-url"]')
  }

  lastViewedQuestionGuidance (): Locator {
    return this.locator('#last-viewed-question-guidance')
  }

  lastViewedQuestionGuidanceLink (): Locator {
    return this.locator('#section-start-link')
  }
}
