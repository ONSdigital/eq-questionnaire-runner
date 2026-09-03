**# Functional Tests

## Quick Reference

- The tests are written using the [Playwright](https://playwright.dev/) framework
- Playwright config: `playwright.config.ts`
- Playwright spec root: `tests/functional/spec`

## Advanced Running

The most flexible way to run Playwright tests is it's [CLI](https://playwright.dev/docs/test-cli) as this allows access to the full range of command line options.

Run all tests:

```shell
npx playwright test
```

By default, it runs headless, to run headed:

```shell
npx playwright test --headed
```

Use the Playwright UI for interactive test selection and debugging:

```shell
npx playwright test --ui
```

Run all specs in a folder:

```shell
npx playwright test tests/functional/spec/list_collector
```

Run a single spec file:

```shell
npx playwright test tests/functional/spec/preview.spec.ts
```

Or omit the path and just use the spec filename:

```shell
npx playwright test preview.spec.ts
```

Or use a subset of a spec name, and it will run all spec filenames containing that text (regardless of folder):

```shell
npx playwright test checkbox
```

Run a single test by title pattern:

```shell
npx playwright test -g "Given I am on the first question"
```

By default, playwright will use an appropriate number of workers for your machine. You can override this with:

```shell
npx playwright test --workers 1
```

Re-run only failed tests:

```shell
npx playwright test --last-failed
```

Generate HTML report (and keep the list output):

```shell
npx playwright test --reporter html,list
```

Open Playwright HTML report:

```shell
npx playwright show-report
```

## Debugging

You can easily run individual tests directly from the UI with breakpoint debugging in PyCharm. For VSCode read about [the Playwright VSCode extension](https://playwright.dev/docs/getting-started-vscode). Whilst debugging a test you can also access the browser the test is running in and access the DOM inspector.
It's well worth reading through the documentation and familiarising yourself with the features it provides.

Run in debug mode (opens the Playwright inspector and runs headed with debug-friendly defaults):

```shell
npx playwright test --debug
```

Pause on every action:

```shell
PWDEBUG=1 npx playwright test
```

Reduce concurrency during investigation:

```shell
npx playwright test --workers 1 <spec file>
```
