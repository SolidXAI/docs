---
title: UI Testing
description: Playwright-based frontend E2E testing support in SolidX, including navigation, actions, assertions, and runtime expectations.
sidebar_position: 6
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
  "steps": [
    {
      "given": {
        "op": "ui.goto",
        "with": {
          "url": "/login"
        }
      }
    },
    {
      "when": {
        "op": "ui.fill",
        "with": {
          "selector": "#user",
          "value": "alice"
        }
      }
    },
    {
      "and": {
        "op": "ui.fill",
        "with": {
          "selector": "#pass",
          "value": "secret"
        }
      }
    },
    {
      "and": {
        "op": "ui.click",
        "with": {
          "selector": "button[type=submit]"
        }
      }
    },
    {
      "then": {
        "op": "ui.expectUrl",
        "with": {
          "contains": "/dashboard"
        }
      }
    }
  ]
}
```

The `venue` module uses this exact kind of flow for password login:

- open `/auth/login`
- assert that the identifier field is visible
- fill identifier and password
- click the submit button
- wait for the transition to settle
- assert the landing URL
- assert expected text on the destination page

## UI Testing Patterns

Common patterns include:

- login and authentication verification
- create/edit flows through forms
- route guards and redirect behaviour
- visibility of important dashboard content
- smoke checks for critical pages

Practical patterns from the `venue` module:

- use `ui.expectVisible` before interacting with critical controls
- use concrete selectors such as `#identifier` or `button.auth-submit-button`
- assert both routing outcome and visible body text after login

The same example also includes `util.sleep` after submit. That can be useful while stabilising a new flow, but over time it is usually better to rely on stronger URL or visibility-based assertions wherever possible.

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

## Relationship To Playwright

Playwright is the execution adapter for UI automation in SolidX, but the testing model itself remains SolidX-native:

- scenarios are still metadata-driven
- step execution still goes through the shared engine
- reporting and interpolation still work the same way
- only the browser interaction layer is Playwright-specific

That gives teams the power of Playwright without forcing them to abandon the shared SolidX testing architecture.
