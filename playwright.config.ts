import { defineConfig } from '@playwright/test'

const ci = String(process.env.CI).toLowerCase() === 'true'

function parseSpecsEnv (
  raw: string
): string[] {
  // Support comma, whitespace, or newline separated pattern lists.
  return raw
    .split(/[,\n]/)
    .flatMap((chunk) => chunk.trim().split(/\s+/))
    .map((s) => s.trim())
    .filter(Boolean)
}

// @ts-expected-error
const specList = process.env.SPECS
  ? parseSpecsEnv(process.env.SPECS)
  : undefined

export default defineConfig({
  testDir: './tests/functional/',
  testMatch: specList, // if undefined, Playwright uses normal discovery
  timeout: ci ? 30000 : 20000,
  fullyParallel: true,
  /* Retry on CI only */
  retries: ci ? 2 : 0,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!ci,
  workers: 1,
  use: {
    baseURL: process.env.EQ_FUNCTIONAL_TEST_ENV ?? 'http://localhost:5000',
    viewport: { width: 1920, height: 1080 },
    trace: ci ? 'on-first-retry' : 'retain-on-failure'
  },
  projects: [
    {
      name: 'components',
      testMatch: ['tests/functional/spec/components/**/*.spec.ts', 'tests/functional/spec/summaries/**/*.spec.ts', 'tests/functional/spec/*.spec.ts']
    },
    {
      name: 'timeout_modal',
      testMatch: ['tests/functional/spec/timeout/**/*.spec.ts']
    },
    {
      name: 'features',
      testMatch: ['tests/functional/spec/features/**/*.spec.ts', 'tests/functional/spec/list_collector/**/*.spec.ts', 'tests/functional/spec/hub_and_spoke/**/*.spec.ts', 'tests/functional/spec/supplementary_data/**/*.spec.ts']
    },
    {
      name: 'journeys',
      testMatch: ['spec/journeys/**/*.spec.ts']
    }
  ]
})
