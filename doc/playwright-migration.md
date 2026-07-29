# Playwright Migration

The migration focuses on:

- Preserving existing questionnaire behavior
- Translating WDIO interaction and assertion patterns into Playwright-native equivalents
- Removing unnecessary waiting by moving to Playwright's auto-waiting locator assertions
- Stabilising historically flaky journeys

The directory structure of the tests and suites has been purposely kept to enable easier comparison of the Playwright tests with their WDIO equivalents.

It's worth reading through the Playwright [docs](https://playwright.dev/docs/writing-tests) and familiarising yourself with it's terminology before reading further.

## The migration

These are the broad mappings used throughout the migration:

- WDIO `$` / `$$` element access -> Playwright `locator(...)`
- WDIO `browser.url(...)` navigation -> Playwright `page.goto(...)`
- WDIO click/type calls -> Playwright locator actions (`click`, `fill`, `check`, etc.)
- WDIO page/text extraction assertions -> Playwright locator assertions:
  - Visibility/state checks are performed on locators (`toBeVisible`, `toBeChecked`, `toBeHidden`)
  - Input and content checks use locator assertions (`toHaveValue`, `toHaveText`, `toContainText`, `toHaveCount`)
  - URL and routing checks use `toHaveURL` instead of ad-hoc string checks

### Waits

WDIO waits (e.g. `waitForDisplayed`) have been mostly removed as Playwright auto-waits by default. Explicit time-based waits have been kept only where behaviour is intentionally time-dependent e.g. timeout tests. For these tests we also override the global timeout using `test.setTimeout(...)` as the waits exceed the default test timeout.

### Summary page answers

There were a number of summary page answer assertions that relied on checking for strings with escaped newlines (`\n`). These have been replaced with more explicit checks.

#### Single level lists

Individual `li` text values are asserted e.g.

```js
await expect(await $(SummaryPage.checkboxAnswer()).getText()).toBe("British\nIrish");
```

becomes:

```ts
await expect(summaryPage.checkboxAnswer().locator('li')).toHaveText(['British', 'Irish'])
```

#### Detail answers

Text text content of specific elements is asserted e.g.

```js
await expect(await $(SubmitPage.optionalRadioWithDropdownDetailAnswer()).getText()).toBe("Fruit\nMango");
```

becomes:

```ts
await expect(submitPage.optionalRadioWithDropdownDetailAnswer().locator('span')).toHaveText('Fruit')
await expect(submitPage.optionalRadioWithDropdownDetailAnswer().locator('li')).toHaveText('Mango')
```

And for multiple detail answers:

```js
await expect(await $(SubmitPage.mandatoryCheckboxAnswer()).getText()).toBe("Cheese\nMozzarella\nYour choice\nBacon");
```

becomes:

```ts
const topLevelAnswers = submitPage.mandatoryCheckboxAnswer().locator(':scope > ul > li')
await expect(topLevelAnswers.nth(0).locator('span')).toHaveText('Cheese')
await expect(topLevelAnswers.nth(0).locator('li')).toHaveText('Mozzarella')
await expect(topLevelAnswers.nth(1).locator('span')).toHaveText('Your choice')
await expect(topLevelAnswers.nth(1).locator('li')).toHaveText('Bacon')
```

#### Multi-line answers

For text that uses line breaks (`<br>`) we assert the text content and the number of `<br>` elements e.g.

```js
await expect(await $(SubmitPage.summaryRowState("address-question-concatenated-answer")).getText()).toBe("Cardiff Road\nNewport\nNP10 8XG");
await expect(await $(SubmitPage.summaryRowState("age-question-concatenated-answer")).getText()).toBe("7\nThis age is an estimate");
```

becomes:

```ts
await expect(addressSummary.locator('br')).toHaveCount(2)
await expect(addressSummary).toHaveText(/Cardiff Road\s*Newport\s*NP10 8XG/)
await expect(ageSummary.locator('br')).toHaveCount(1)
await expect(ageSummary).toHaveText(/7\s*This age is an estimate/)
```

### Hidden content

For hidden content, `aria-hidden` attributes and values are asserted rather than empty text e.g.

```js
await expect(await $(InterstitialDefinitionPage.definitionContent()).getText()).toBe("");
```

becomes:

```ts
await expect(interstitialDefinitionPage.definitionContent()).toHaveAttribute('aria-hidden', 'true')
```

### Stateful tests

Playwright expects individual tests within spec files to be able to run in any order. For tests that depend on them running in a sequential order the parent `describe` is configured with `test.describe.configure({ mode: 'serial' })`. If any shared state is required, this is defined after this statement and before the first `test` e.g.

in `save_sign_out.spec.ts` the response id is shared between tests using:

```ts
const responseId = getRandomString(16)
```

and in `numbers.spec.ts` the browser context is shared across all tests using:

```ts
let context: BrowserContext
let page: Page
let openQuestionnaire: OpenQuestionnaire

test.beforeAll(async ({ browser }) => {
  context = await browser.newContext()
  page = await context.newPage()
  openQuestionnaire = createOpenQuestionnaire(page)
  await openQuestionnaire('test_numbers.json')
})

test.afterAll(async () => {
  await context.close()
})
```
