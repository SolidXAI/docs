---
title: Authoring Scenarios
description: How to define testing metadata, scenarios, steps, interpolation, and custom specs in SolidX.
sidebar_position: 4
---

# Authoring Scenarios

This page explains how to write testing metadata for SolidX.

## Where Scenarios Live

Testing definitions live inside a module metadata JSON file under the `testing` key.

At a high level, the shape looks like this:

```json
{
  "testing": {
    "specs": ["path/to/register-test-specs.js"],
    "roles": [],
    "users": [],
    "data": [],
    "scenarios": []
  }
}
```

## Top-Level Testing Keys

### `specs`

Paths to custom spec registration modules.

These are used when you want to invoke `test.spec` from a scenario.

### `roles`

Optional testing role definitions used for automation-oriented identity setup.

### `users`

Optional testing user definitions used for automation-oriented identity setup.

### `data`

Test fixture records to load before execution.

Each record contains:

- `modelUserKey`
- `recUserKeyValue`
- `data`

Real project pattern:

- use `testing.data` as a reusable fixture library
- express relations through `...UserKey` fields such as `stateUserKey`, `cityUserKey`, or `templateMasterUserKey`
- keep `recUserKeyValue` stable so scenarios can reference the fixture by name

### `scenarios`

The executable scenarios for the module.

This is the core of the testing system.

## Scenario Shape

Each scenario has this structure:

```json
{
  "id": "api-authenticate-success",
  "name": "Authenticate succeeds",
  "type": "api",
  "params": {
    "username": "alice"
  },
  "tags": ["smoke"],
  "timeoutMs": 30000,
  "retries": 1,
  "steps": []
}
```

### Important Fields

- `id`: stable scenario identifier
- `name`: optional human-readable label
- `type`: `api`, `ui`, or `mixed`
- `params`: free-form scenario parameters
- `tags`: labels for filtering
- `timeoutMs`: scenario timeout override
- `retries`: scenario retry count
- `steps`: the actual executable flow

## Step Styles

Steps can be written in two ways.

### Phase Style

```json
{
  "given": { "op": "ui.goto", "with": { "url": "/login" } }
}
```

### Flat Style

```json
{
  "op": "util.log",
  "with": { "message": "Starting scenario" }
}
```

The engine normalises both forms before execution.

## Step Fields

Each executable step can include:

- `op`: required operation name
- `with`: op-specific input
- `saveAs`: save step result into the resource store
- `name`: optional reporting label
- `spec`: custom spec id for `test.spec`
- `timeoutMs`: per-step timeout override

## Interpolation

Before each step runs, the engine resolves interpolation tokens.

Supported token families include:

- `${env:NAME}` for environment variables
- `${params.foo}` for scenario params
- `${res:path.to.value}` for saved runtime resources
- `${data:modelUserKey["recUserKeyValue"].field}` for test data lookups

Examples:

```json
{
  "params": {
    "state": "${data:stateMaster[\"Maharashtra\"].name}"
  }
}
```

```json
{
  "when": {
    "op": "api.request",
    "with": {
      "method": "POST",
      "url": "${env:API_BASE_URL}/api/example",
      "json": {
        "stateName": "${params.state}",
        "city": "${data:cityMaster[\"New Delhi\"].name}"
      }
    }
  }
}
```

## Referencing Test Data

Test data is indexed as:

```text
data:<modelUserKey>["<recUserKeyValue>"]
```

Useful patterns:

- `.fieldName` to access a single field
- `._rec` to access the whole underlying object

Example:

```json
"${data:cityMaster[\"New Delhi\"]._rec}"
```

The `venue` module uses this pattern heavily:

- master fixtures such as `stateMaster["Maharashtra"]`
- relation-aware fixtures such as `cityMaster["Mumbai"]`
- file-upload fixtures such as `lead["LeadWithFile"]._rec`

That keeps scenarios short and readable, because large request bodies stay in `testing.data` instead of being repeated inline.

## Using saveAs

When a step returns a value you want later, use `saveAs`.

Example:

```json
{
  "when": {
    "op": "api.auth.bearerFromLogin",
    "with": {
      "url": "${env:API_BASE_URL}/auth/login",
      "username": "alice",
      "password": "secret"
    },
    "saveAs": "auth.token"
  }
}
```

Later steps can then use:

```json
"Authorization": "Bearer ${res:auth.token}"
```

In practice, many teams save the full login response rather than only the token. The `venue` module saves the response as `loginSuccess` and then reads the token later via:

```json
"Bearer ${res:loginSuccess.bodyJson.data.accessToken}"
```

That is a useful pattern because it preserves the entire auth response for later steps.

## Scenario Chaining With `util.require`

A common SolidX pattern is:

1. create a reusable bootstrap scenario, usually authentication
2. save its result with `saveAs`
3. start later scenarios with `util.require`
4. fail early with a helpful message if the prerequisite resource is missing

Example:

```json
{
  "given": {
    "op": "util.require",
    "with": {
      "resource": "loginSuccess",
      "message": "Run scenario api-authenticate-success first to create loginSuccess."
    }
  }
}
```

The `venue` module uses this pattern throughout its authenticated API scenarios.

## Custom Specs

When built-in operations are not enough, use `test.spec`.

Example step:

```json
{
  "when": {
    "op": "test.spec",
    "spec": "example.customHealth",
    "with": {
      "input": {
        "url": "${env:API_BASE_URL}/health"
      }
    },
    "saveAs": "custom.health"
  }
}
```

Custom specs are registered through the spec registry and made available via `testing.specs`.

Real project pattern:

```json
{
  "specs": ["testing/register-test-specs.js"]
}
```

That registrar then maps ids such as `venue.customHealth` to concrete spec implementations.

The `venue` example also shows a helpful convention where `with.input` includes both:

- direct input values, such as a health URL
- and a resource path, such as `authResourcePath`

This lets a custom spec combine metadata input with previously saved runtime state.

## Authoring Recommendations

Recommended practices:

- keep scenario ids stable and descriptive
- use tags such as `smoke`, `regression`, or `auth`
- keep API and UI scenarios small and composable
- use `generate module` or `seed` workflows consistently before execution
- prefer `saveAs` plus interpolation over hard-coded chained values
- reserve `test.spec` for genuine escape-hatch cases
- prefer reusable fixture libraries in `testing.data` over repeating large payloads inline
- make scenario prerequisites explicit with `util.require`
- keep one small authentication bootstrap scenario per module when many scenarios need auth

## When To Use API vs UI vs Mixed

- Use `api` when you want fast, direct, backend-facing verification.
- Use `ui` when you want browser-level user-flow verification.
- Use `mixed` when your flow crosses both layers and it would be artificial to separate them.

Next: [API Testing](./api-testing.md)
