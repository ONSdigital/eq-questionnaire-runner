import { type Locator } from '@playwright/test'
import BasePage from './base.page'

export default class ViewSubmittedResponseBasePage extends BasePage {
  metadata (): Locator {
    return this.locator('.ons-description-list')
  }

  metadataTerm (number = 1): Locator {
    return this.locator(`.ons-description-list > .ons-description-list__item:nth-of-type(${number}) > dt`)
  }

  metadataValue (number = 1): Locator {
    return this.locator(`.ons-description-list > .ons-description-list__item:nth-of-type(${number}) > dd`)
  }

  informationPanel (): Locator {
    return this.locator('[id="view-submitted-guidance"]')
  }

  printButton (): Locator {
    return this.locator('[data-qa="btn-print"]')
  }

  downloadButton (): Locator {
    return this.locator('[data-qa="btn-pdf"]')
  }
}
