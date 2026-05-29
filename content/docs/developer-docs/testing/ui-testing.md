---
title: UI Testing
icon: "monitor"
description: Playwright-based frontend E2E testing support in SolidX, including navigation, actions, assertions, and runtime expectations.
---

# UI Testing

SolidX supports frontend end-to-end testing through a Playwright-based UI adapter.

This lets browser-level automation run through the same metadata-driven testing engine used for API testing.

## How UI Testing Works

At runtime:

1. the runner loads `ui` or `mixed` scenarios from metadata
2. it determines whether a browser is needed
3. the Playwright adapter is started when required
4. UI steps are executed through the adapter
5. the browser is shut down cleanly at the end of the run

This means UI testing is integrated into the same engine rather than being maintained as a separate testing framework.

## What UI Testing Is Best For

Use UI testing when you need to validate:

- real user flows,
- form behaviour,
- page transitions,
- visible content,
- routing outcomes,
- browser-side interactions.

## Runtime Expectations

UI testing requires a running frontend application.

That usually means supplying:

- `--ui-base-url`
- optionally `--headless`

Example:

```bash
npx @solidxai/solidctl@latest test run --module venue --ui-base-url http://localhost:5173 --headless false
```

Within scenarios, the UI base URL is available as `${env:TEST_UI_BASE_URL}`.

If a scenario includes UI execution, the browser lifecycle is managed by the test runner.

## Core UI Operations

### Navigation

Common navigation primitives include:

- `ui.goto`
- `ui.expectUrl`

Use them to open pages and confirm that routing behaved as expected.

### Form Input

Common form primitives include:

- `ui.fill`
- `ui.select`
- `ui.press`

These are useful for login flows, search flows, forms, and interactive field-based scenarios.

### Form Fields

Form inputs in SolidX get their `id` from the field's `name` in model metadata.

That means the selector for any form field is `#fieldName` — where `fieldName` matches the field's `name` property in the module metadata.

For example, a model with a field named `title` will render an input with `id="title"`, so the selector is `#title`.

When writing form-level UI scenarios, look up the model's fields in the metadata to find the right names.

### Actions

The main action primitive is:

- `ui.click`

This is commonly used for:

- submit buttons,
- links,
- menu actions,
- modal interactions.

### Assertions

Common UI assertions include:

- `ui.expectVisible`
- `ui.expectText`
- `ui.expectUrl`

These let you verify that the browser is showing the expected outcome of a user flow.

## Example UI Flow

```json
{
  "id": "ui-login-happy-path",
  "type": "ui",
  "tags": ["smoke"],
  "steps": [
    {
      "given": {
        "op": "ui.goto",
        "with": { "url": "${env:TEST_UI_BASE_URL}/auth/login" }
      }
    },
    {
      "and": {
        "op": "ui.expectVisible",
        "with": { "selector": "#identifier" }
      }
    },
    {
      "when": {
        "op": "ui.fill",
        "with": { "selector": "#identifier", "value": "libTestEditor@test.local" }
      }
    },
    {
      "and": {
        "op": "ui.expectVisible",
        "with": { "selector": "input[type='password']" }
      }
    },
    {
      "and": {
        "op": "ui.fill",
        "with": { "selector": "input[type='password']", "value": "Test@1234" }
      }
    },
    {
      "and": {
        "op": "ui.click",
        "with": { "selector": "button:has-text('Sign In')" }
      }
    },
    {
      "then": {
        "op": "ui.expectVisible",
        "with": { "selector": ".solid-admin-header" }
      }
    },
    {
      "and": {
        "op": "ui.expectUrl",
        "with": { "contains": "/admin" }
      }
    }
  ]
}
```

The standard login flow:

- navigate to `/auth/login`
- assert `#identifier` is visible before filling it
- fill the identifier field with the test user's email
- assert the password input is visible, then fill it — use `input[type='password']` not `#password`
- click the submit button by its label with `button:has-text('Sign In')`
- assert `.solid-admin-header` is visible to confirm the app has loaded
- assert the URL contains `/admin`

## UI Testing Patterns

Common patterns include:

- login and authentication verification
- create/edit flows through forms
- route guards and redirect behaviour
- visibility of important dashboard content
- smoke checks for critical pages

Practical patterns from real scenarios:

- use `ui.expectVisible` before filling any input — confirms the element is ready
- use `#identifier` for the login identifier and `input[type='password']` for the password field
- use `button:has-text('Sign In')` for the login submit — more readable than a class selector
- assert `.solid-admin-header` visibility after login before asserting the URL
- use `.solid-sidebar-tree-link:has(.solid-sidebar-tree-label:text('ModelName'))` to click a sidebar model link
- assert `table tbody` visibility to confirm a list view has loaded

`util.sleep` can be useful while stabilising a new flow, but over time it is better to rely on stronger URL or visibility-based assertions wherever possible.

## Mixed Scenarios

One of the strengths of the SolidX testing model is that UI testing can be combined with API testing in `mixed` scenarios.

This is useful when:

- API setup is faster than doing the same setup through the browser
- UI verification is still required at the end
- a workflow naturally crosses backend and frontend layers

For example:

- create prerequisite data via API
- open a UI page
- assert that the created data is visible in the browser

## Headless vs Headed

Use headless mode when:

- running in CI
- you want fast non-visual execution

Use headed mode when:

- debugging a failing scenario
- developing a new UI scenario
- inspecting selectors and interaction timing

## Good UI Testing Practices

Recommended practices:

- keep UI scenarios focused on user-visible behaviour
- avoid using UI tests when API tests would cover the same risk more cheaply
- prefer stable selectors and predictable page states
- use test data and API setup steps to reduce unnecessary browser work
- use `mixed` scenarios when that better reflects the real workflow
- prefer visible-state assertions over arbitrary waits when you can
- keep login scenarios reusable, because they are often the first UI smoke test a module maintains

## Selector Conventions

SolidX UI components do not use `data-testid`. Selectors fall into three groups.

### ID selectors — form fields

Form inputs get their `id` from the field's `name` in model metadata.

```text
#title       → input for a field named "title"
#identifier  → login identifier input (always this value)
#email       → email input on dedicated email forms
```

When writing tests for a specific model's form, look up the model's `fields[*].name` values in the metadata to get the correct IDs.

### CSS class selectors — structural and interactive elements

The project uses stable `solid-*` BEM-style classes:

```text
.auth-container           login page container
.solid-admin-header       top app header after login
.solid-sidebar            navigation sidebar
.solid-data-table-row     table rows in list views
.solid-table-paginator    list view pagination bar
.solid-form-section       form content wrapper
```

### Playwright extended selectors — text and composition

Use Playwright's extended syntax for buttons, menu items, and toasts:

```text
button:has-text('Sign In')                    button by visible label
:text-is('Catalog')                           exact text match
:has-text('...')                              subtree text match
.solid-sidebar-tree-link:has(.solid-sidebar-tree-label:text('Book'))
div[role='status']:has-text('Invalid Credentials')
```

Prefer `button:has-text(...)` over class-based button selectors when the button label is stable — it reads clearly and survives class renames.

---

## Relationship To Playwright

Playwright is the execution adapter for UI automation in SolidX, but the testing model itself remains SolidX-native:

- scenarios are still metadata-driven
- step execution still goes through the shared engine
- reporting and interpolation still work the same way
- only the browser interaction layer is Playwright-specific

That gives teams the power of Playwright without forcing them to abandon the shared SolidX testing architecture.
