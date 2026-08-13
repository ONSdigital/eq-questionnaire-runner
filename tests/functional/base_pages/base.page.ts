import { type Locator, type Page } from '@playwright/test'

export default class BasePage {
  protected page: Page

  readonly pageName: string

  constructor (page: Page, pageName: string) {
    this.page = page
    this.pageName = pageName
  }

  protected locator (selector: string): Locator {
    return this.page.locator(selector)
  }

  previous (): Locator {
    return this.locator('a[id="top-previous"]')
  }

  heading (): Locator {
    return this.locator('h1')
  }

  warning (): Locator {
    return this.locator('[data-qa="warning"]')
  }

  guidance (): Locator {
    return this.locator('[data-qa="guidance"]')
  }

  acceptCookies (): Locator {
    return this.locator('[data-button="accept"]')
  }

  submit (): Locator {
    return this.locator('[data-qa="btn-submit"]')
  }

  saveSignOut (): Locator {
    return this.locator('[data-qa="btn-save-sign-out"]').first()
  }

  switchLanguage (languageCode: string): Locator {
    return this.locator(`a[href="?language_code=${languageCode}"]`)
  }
}
