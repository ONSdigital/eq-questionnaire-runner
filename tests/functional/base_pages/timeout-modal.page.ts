import { type Locator, type Page } from '@playwright/test'

export default class TimeoutModalBasePage {
  private readonly page: Page

  constructor (page: Page) {
    this.page = page
  }

  timer (): Locator {
    return this.page.locator('.ons-js-timeout-timer')
  }

  submit (): Locator {
    return this.page.locator('.ons-js-modal-btn')
  }
}
