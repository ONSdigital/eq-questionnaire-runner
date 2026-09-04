import { type Locator, type Page } from '@playwright/test'
import BasePage from './base.page'

export default class IntroductionPageBase extends BasePage {
  constructor (page: Page, pageName = 'introduction') {
    super(page, pageName)
  }

  myAccountLink (): Locator {
    return this.locator('#my-account')
  }

  exitButton (): Locator {
    return this.locator('[data-qa="btn-exit"]').first()
  }

  getStarted (): Locator {
    return this.locator('.qa-btn-get-started')
  }

  useOfInformation (): Locator {
    return this.locator('#use-of-information')
  }

  useOfData (): Locator {
    return this.locator('#how-we-use-your-data')
  }

  legalResponse (): Locator {
    return this.locator('[data-qa="legal-response"]')
  }

  legalBasis (): Locator {
    return this.locator('[data-qa="legal-basis"]')
  }

  introDescription (): Locator {
    return this.locator('#use-of-information p')
  }

  previewQuestions (): Locator {
    return this.locator('a[href="/questionnaire/preview"]')
  }

  introQuestion (number = 1): Locator {
    return this.locator(`#intro-questions-${number}`)
  }
}
