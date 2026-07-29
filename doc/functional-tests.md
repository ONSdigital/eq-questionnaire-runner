# Functional Tests

## Quick Reference

- The tests are written using the [Playwright](https://playwright.dev/) framework
- Playwright config: `playwright.config.ts`
- Playwright spec root: `tests/functional/spec`
- Configured Playwright projects:
  - `components`
  - `timeout_modal`
  - `features`
  - `journeys`

## VS Code Extension

The [Playwright VS Code extension](https://playwright.dev/docs/getting-started-vscode) is the easiest way to run and debug tests.
Once installed you can easily run individual tests directly from the UI with breakpoint debugging. Whilst debugging a test you can also access the browser the test is running in and access the DOM inspector.
It's well worth reading through the documentation and familiarising yourself with the features it provides.

## Advanced Running

The most flexible way to run Playwright tests is it's [CLI](https://playwright.dev/docs/test-cli) as this allows access to the full range of command line options.

Run all tests:

```shell
npx playwright test
```

By default it runs headless, to run headed:

```shell
npx playwright test --headed
```

Use the Playwright UI for interactive test selection and debugging:

```shell
npx playwright test --ui
```

Run a single configured project:

```shell
npx playwright test --project=components
npx playwright test --project=features
npx playwright test --project=journeys
npx playwright test --project=timeout_modal
```

Run all projects except timeout_modal:

```shell
npx playwright test --project=components --project=features --project=journeys
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

Or use a subset of a spec name and it will run all spec filenames containing that text (regardless of project/folder):

```shell
npx playwright test checkbox
```

Run a single test by title pattern:

```shell
npx playwright test -g "Given I am on the first question"
```

By default playwright will use an appropriate number of workers for your machine. You can override this with:

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
