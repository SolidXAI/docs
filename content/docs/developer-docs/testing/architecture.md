---
title: Architecture
icon: "blocks"
description: Testing architecture in SolidX, including the engine, adapters, registries, steps, and reporters.
---

# Testing Architecture

SolidX testing is implemented as a **shared execution engine** with pluggable adapters and step registries.

The architecture is designed so that API and UI tests can use the same scenario format, the same interpolation rules, the same reporting flow, and the same runtime context.

## High-Level Structure

The main testing implementation lives under `solid-core-module/src/testing/`.

At a high level, it is organised like this:

```bash
src/testing/
├── contracts/    # metadata and runtime context types
├── core/         # engine, interpolation, resource store, registries
├── adapters/     # API adapter and Playwright UI adapter
├── steps/        # built-in operations grouped by domain
├── reporter/     # reporting types and console reporter
└── runner/       # metadata execution and lifecycle helpers
```

## Main Building Blocks

### Testing Metadata

Testing starts from module metadata under the `testing` key.

That metadata describes:

- test fixtures,
- scenarios,
- optional testing roles and users,
- and optional custom test spec registrars.

This makes testing part of the application's metadata model rather than something completely external to it.

### Runner

The runner is responsible for turning metadata into an executable test session.

Its main job is to:

- build the step registry,
- register built-in step families,
- load and filter scenarios,
- build the test data index,
- create the runtime context,
- initialise adapters,
- and invoke the engine for each scenario.

This logic is coordinated through the metadata runner in `runner/run-from-metadata.ts`.

### Testing Engine

The `TestingEngine` is the core executor.

It:

- receives a scenario and a runtime context,
- applies retries and scenario timeouts,
- normalises Given/When/Then blocks into executable steps,
- interpolates step values before execution,
- invokes the correct step handler,
- stores results into the resource store when `saveAs` is used,
- and emits scenario and step lifecycle events to the reporter.

In other words, the engine is the shared orchestration layer for all scenario types.

### Step Registry

The step registry maps operation names such as:

- `api.request`
- `ui.goto`
- `assert.httpStatus`
- `util.sleep`
- `test.spec`

to their corresponding handlers.

Built-in registrations are grouped by domain:

- API steps
- UI steps
- assert steps
- util steps
- test-spec steps

### Adapters

Adapters are the bridge between generic scenario steps and concrete execution tools.

#### API Adapter

The API adapter uses Axios-style HTTP execution and powers operations such as:

- `api.request`
- `api.auth.bearerFromLogin`

#### UI Adapter

The UI adapter is Playwright-based and powers operations such as:

- navigation,
- form filling,
- clicks,
- assertions on visibility, text, and URL.

This is how SolidX supports frontend E2E testing in the same scenario engine without embedding browser logic directly into the engine itself.

### Reporter

Reporters consume lifecycle events such as:

- scenario start,
- step start,
- step end,
- scenario end.

The built-in reporter is a console reporter, but the architecture is already split so additional reporters can be introduced later.

### Resource Store

The resource store is a shared runtime object used to persist values between steps.

For example:

- an auth token returned by one step,
- a created record id,
- a custom test spec result,
- or any intermediate response you want to reference later.

Steps write to the store using `saveAs`, and later steps read those values through interpolation with `${res:...}`.

## Shared Runtime Context

Every scenario executes with a runtime context that contains:

- scenario id and scenario type,
- resolved params,
- the shared resource store,
- API and UI adapters,
- the last API response,
- the reporter,
- the spec registry,
- indexed test data,
- and runtime options such as API log printing.

This shared context is what allows API steps, UI steps, assertions, and custom specs to cooperate cleanly.

## Scenario Types

SolidX currently supports these scenario types:

- `api`
- `ui`
- `mixed`

`mixed` is especially useful when a workflow crosses both layers, for example:

- authenticate through an API step,
- create data through an API step,
- then verify the result through a UI step.

## Built-In Step Families

Built-in steps are registered from these domains:

- `api`
- `ui`
- `assert`
- `util`
- `test`

This gives SolidX a good balance between:

- standardisation for common testing needs,
- and extensibility when a project needs custom logic.

## Custom Specs

When built-in steps are not enough, SolidX provides `test.spec` as an escape hatch.

Custom specs:

- are registered through `testing.specs`,
- are resolved through the spec registry,
- receive the shared runtime context plus free-form input,
- and return structured results that can be saved and reused.

This lets teams keep the main testing workflow metadata-driven while still supporting highly custom assertions or setup logic.

The `venue` module shows a concrete version of this pattern:

- `testing.specs` points to `testing/register-test-specs.js`
- that registrar maps a stable id such as `venue.customHealth`
- a scenario invokes `test.spec`
- the spec receives `ctx` and `input`
- and it can read previously saved resources from `ctx.resources`

That is a strong pattern when built-in steps are almost enough, but you still need a project-specific verification step.

## UI Lifecycle

The runner starts the Playwright adapter only when a scenario requires UI execution.

That means:

- pure API runs do not pay the browser startup cost,
- UI scenarios can still run within the same framework,
- and browser lifecycle is handled centrally by the runner.

## Mental Model

The cleanest way to think about the testing architecture is:

- metadata defines what to test,
- the runner prepares the runtime,
- the engine executes the scenario,
- adapters talk to the outside world,
- the resource store carries state between steps,
- and reporters make the run visible.

In real projects, a common execution pattern looks like this:

- one scenario saves a reusable bootstrap resource such as `loginSuccess`
- later scenarios assert that dependency with `util.require`
- those scenarios interpolate the saved result via `${res:...}`
- and custom specs can read the same saved resource through the runtime context

That is how SolidX supports lightweight scenario chaining without needing a separate dependency graph.

Next: [Workflow](./workflow.md)
