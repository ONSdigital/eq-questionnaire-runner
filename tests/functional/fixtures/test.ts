import { test as base, expect, type Page } from '@playwright/test'
import * as JwtHelper from '../jwt_helper'

const sessionRedirectTimeoutMs = parseInt(process.env.EQ_SESSION_REDIRECT_TIMEOUT_MS ?? '15000', 10)

interface OpenQuestionnaireOptions {
  launchVersion?: string
  theme?: string
  userId?: string
  collectionId?: string
  responseId?: string
  surveyId?: string
  periodId?: string
  periodStr?: string
  ruRef?: string
  sdsDatasetId?: string | null
  region?: string
  language?: string
  includeLogoutUrl?: boolean
  booleanFlag?: boolean
}

type OpenQuestionnaire = (schema: string, options?: OpenQuestionnaireOptions) => Promise<void>

interface Fixtures {
  openQuestionnaire: OpenQuestionnaire
}

function createOpenQuestionnaire (page: Page): OpenQuestionnaire {
  return async (schema, options) => await gotoSession(page, schema, options)
}

async function gotoSession (page: Page, schema: string, options: OpenQuestionnaireOptions = {}): Promise<void> {
  const {
    launchVersion = 'v2',
    theme = 'default',
    userId = JwtHelper.getRandomString(10),
    collectionId = JwtHelper.getRandomString(10),
    responseId = JwtHelper.getRandomString(16),
    surveyId = '123',
    periodId = '201605',
    periodStr = 'May 2016',
    ruRef = '12345678901A',
    sdsDatasetId = null,
    region = 'GB-ENG',
    language = 'en',
    includeLogoutUrl = false,
    booleanFlag = false
  } = options

  const token = await JwtHelper.generateToken(schema, {
    launchVersion,
    theme,
    userId,
    collectionId,
    responseId,
    surveyId,
    periodId,
    periodStr,
    ruRef,
    sdsDatasetId,
    regionCode: region,
    languageCode: language,
    includeLogoutUrl,
    booleanFlag
  })

  await page.goto(`/session?token=${token}`)
  await page.waitForURL((url: URL): boolean => !url.toString().includes('/session?token='), { timeout: sessionRedirectTimeoutMs })
}

export const test = base.extend<Fixtures>({
  openQuestionnaire: async ({ page }, use) => {
    const openQuestionnaire: OpenQuestionnaire = createOpenQuestionnaire(page)
    await use(openQuestionnaire)
  }
})

export { expect }
export { createOpenQuestionnaire }
export type { Page, Locator, BrowserContext } from '@playwright/test'
export type { OpenQuestionnaireOptions, OpenQuestionnaire }
