---
title: Vocabulary
description: Key terms and concepts used in SolidX testing.
sidebar_position: 3
---

# Testing Vocabulary

This page defines the core terms used throughout SolidX testing documentation.

## Start Here

The testing vocabulary in SolidX becomes much easier to follow if you read it as a hierarchy instead of a flat list.

At a high level, the structure looks like this:

1. A project is brought into **SUT mode**
2. A module provides **testing metadata**
3. That metadata defines **test data**, optional **custom specs**, and executable **scenarios**
4. A scenario is made of **steps**
5. Steps execute **ops**
6. Ops run through adapters, the runtime context, and the resource store

In simplified form:

```text
SUT
└── Module under test
    └── testing metadata
        ├── data
        ├── specs
        └── scenarios
            └── steps
                └── ops
                    ├── api
                    ├── ui
                    ├── assert
                    ├── util
                    └── test
```

That means the most useful reading order is usually:

- environment and execution terms,
- metadata structure terms,
- scenario and step terms,
- runtime and execution terms.

This is not redundant with the other testing pages, because this page is meant to help readers decode the words used across the rest of the section quickly.

## Level 1: Environment And Execution Scope

### System Under Test (SUT)

The specific SolidX application environment being prepared and exercised by the test workflow.

In practice, SUT mode usually means:

- isolated test datasources are active,
- metadata has been seeded,
- test fixtures have been loaded,
- and the app is ready for scenario execution.

### Module Under Test

The module whose `testing` metadata is being loaded and executed, typically passed through:

```bash
npx @solidxai/solidctl@latest test run --module venue
```

### Datasource

A configured database connection used by the application.

The test workflow creates isolated test databases or schemas per datasource.

### Run Name

A generated identifier used during `test data --setup` to distinguish one isolated testing run from another.

It helps name backups, manifests, and test datasources safely.

### Manifest

The file written during test setup that records what was created so teardown can reverse it safely and deterministically.

### Headless

A browser execution mode where UI tests run without showing a visible browser window.

This is common in CI runs.

## Level 2: Metadata Structure

### Testing Metadata

The `testing` section inside module metadata JSON files.

This metadata can define:

- `specs`
- `roles`
- `users`
- `data`
- `scenarios`

Read this as:

- `testing`
  the root testing block for a module
- `testing.roles`
  test role definitions with permissions
- `testing.users`
  test user definitions with credentials and role assignments
- `testing.data`
  reusable fixtures loaded before execution
- `testing.specs`
  custom spec registration entry points
- `testing.scenarios`
  executable scenario definitions

### Scenario

An executable testing flow defined in metadata.

A scenario has:

- an `id`,
- an optional `name`,
- a `type`,
- optional `params`,
- optional `tags`,
- optional timeout and retry settings,
- and a list of `steps`.

### Scenario Type

The execution mode of a scenario.

Supported values are:

- `api`
- `ui`
- `mixed`

### Test Data

Fixture records defined in `testing.data`.

These are loaded into the test database before scenario execution and can also be referenced inside scenarios through interpolation.

In practice, test data often acts as a reusable fixture library for:

- master data such as states, cities, regions, or products
- relation-driven records expressed through `...UserKey` fields
- upload fixtures where a field value points to `file:/absolute/path`

### Test Data Index

The in-memory indexed representation of `testing.data` built by the runner.

This is what powers `${data:...}` lookups during scenario execution.

### Spec

In the SolidX testing context, a spec usually means a **custom executable testing unit** registered for use through `test.spec`.

This is different from a scenario:

- a scenario is metadata-defined orchestration,
- a spec is custom code invoked from a scenario.

For example, the `venue` module registers `venue.customHealth` and then invokes it from a scenario through `test.spec`.

### Testing Roles

Role definitions declared in `testing.roles`.

Each entry names a role and lists the permissions to bind to it. Permissions can be exact (`ControllerName.methodName`) or wildcard (`ControllerName.*`).

Roles are created by `test data --load` and are skipped if they already exist.

### Testing Users

User definitions declared in `testing.users`.

Each entry provides credentials and an optional list of role names to assign.

Users are created by `test data --load` and are skipped if a user with the same username already exists.

### Tag

A label attached to a scenario for filtering and grouping.

Tags make it easy to run only subsets such as:

- `smoke`
- `regression`
- `auth`

## Level 3: Scenario Composition

### Step

A single executable unit inside a scenario.

Steps can be written in:

- phase style using `given`, `when`, `then`, `and`
- or flat op style

Each step ultimately resolves to an operation handler.

### Op

Short for operation.

This is the actual executable name of a step, for example:

- `api.request`
- `ui.goto`
- `assert.equals`
- `util.sleep`
- `test.spec`

Read the hierarchy like this:

- a scenario contains steps
- a step names an op
- an op belongs to a family such as `api`, `ui`, `assert`, `util`, or `test`

### Given / When / Then / And

BDD-style step phases used for readability.

These phases are normalised before execution — the engine treats all four identically.

Use `given` for preconditions, `when` for the action under test, `then` for assertions, and `and` to continue the previous phase without repeating it. The choice is a reading aid, not a rule.

### saveAs

A step field that stores the result of the step into the resource store.

Example:

```json
{
  "when": {
    "op": "api.auth.bearerFromLogin",
    "with": { "url": "...", "username": "alice", "password": "secret" },
    "saveAs": "auth.token"
  }
}
```

In real projects, this is often used to save the full authentication response, for example `loginSuccess`, and then later read the token from `${res:loginSuccess.bodyJson.data.accessToken}`.

### test.spec

A built-in step operation that executes a registered custom spec.

Use it when built-in operations are not expressive enough.

### util.require

A built-in utility step used to fail fast when a required resource is missing from the resource store.

This is commonly used to make scenario prerequisites explicit, such as requiring `loginSuccess` before attempting authenticated API calls.

## Level 4: Runtime And Execution

### Adapter

A runtime integration layer that connects generic test steps to concrete tooling.

Examples:

- the API adapter executes HTTP requests
- the UI adapter uses Playwright for browser automation

### Playwright Adapter

The UI testing adapter used by SolidX for browser-based E2E testing.

It powers navigation, actions, and assertions against the frontend.

### Resource Store

A shared runtime store used to persist values across steps and scenarios.

Values are written using `saveAs` and later read using `${res:...}` interpolation.

Typical stored values include:

- auth tokens,
- ids,
- response objects,
- custom spec results.

### Interpolation

The process of resolving dynamic placeholders inside testing metadata before a step executes.

Common token families are:

- `${env:NAME}`
- `${params.foo}`
- `${res:path.to.value}`
- `${data:model["recordKey"].field}`

### Reporter

A component that receives lifecycle events from scenario execution and turns them into visible output.

The default reporter is a console reporter.

### Runtime Context

The object shared across step execution.

It includes:

- scenario metadata,
- params,
- adapters,
- reporter,
- resource store,
- last API response,
- spec registry,
- indexed test data.

### Last API Response

The most recent API response stored in the runtime context.

This is especially useful for assertions like `assert.httpStatus`.

Next: [Authoring Scenarios](./authoring-scenarios.md)
