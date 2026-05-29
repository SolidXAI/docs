---
title: Testing
icon: "test-tube"
description: Comprehensive guide to SolidX testing architecture, workflow, vocabulary, and execution.
summary: This section explains how testing works in SolidX across metadata-driven API testing, Playwright-based UI end-to-end testing, shared testing primitives, test data management, and the operational workflow for bringing the system into SUT mode and running automated tests safely.
sidebar_position: 2.5
---

# Testing

SolidX provides a **metadata-driven testing system** that supports:

- automated API testing,
- automated frontend end-to-end testing using Playwright,
- shared assertions and utility steps,
- managed test data setup and teardown,
- and CLI-driven workflows for bringing the application into **system under test (SUT)** mode.

The important idea is that API and UI tests are not treated as two unrelated systems. They run through a shared testing engine and a shared scenario model, while using different adapters underneath.

<Callout type="info" title="Mental Model">

  SolidX testing is best understood as a <strong>single metadata-driven test system</strong> with multiple execution modes.
  - <strong>Metadata</strong> defines fixtures, scenarios, and custom specs.
    - <strong>The workflow</strong> prepares the system under test through setup, seed, load, run, and teardown.
    - <strong>The engine</strong> executes API, UI, or mixed scenarios through shared primitives.
  So the intuition is: API testing, UI testing, and test data management are all parts of the same testing architecture, not separate disconnected tools.

</Callout>

## What This Section Covers

This Testing section is split into a few focused pages:

- [Architecture](./architecture.md): how the testing engine, adapters, steps, registries, and reporters fit together
- [Workflow](./workflow.md): the end-to-end SOP for setup, seed, load, run, and teardown
- [Vocabulary](./vocabulary.md): the key terms used in SolidX testing
- [Authoring Scenarios](./authoring-scenarios.md): how to write `testing` metadata
- [API Testing](./api-testing.md): API automation patterns and supported primitives
- [UI Testing](./ui-testing.md): Playwright-based E2E testing patterns and supported primitives

## Read This In Order

If you are new to SolidX testing, the best reading order is:

1. [Workflow](./workflow.md)
2. [Vocabulary](./vocabulary.md)
3. [Architecture](./architecture.md)
4. [Authoring Scenarios](./authoring-scenarios.md)
5. [API Testing](./api-testing.md)
6. [UI Testing](./ui-testing.md)

## What SolidX Testing Looks Like In Practice

A typical test run looks like this:

1. Create isolated test datasources with `test data --setup`
2. Seed metadata into the fresh databases
3. Load test fixtures from module metadata
4. Run API and/or UI scenarios
5. Tear everything down and restore the original environment

At runtime, the testing engine:

- loads `testing.scenarios` from module metadata,
- filters scenarios by id or tag,
- registers built-in API, UI, assert, util, and custom spec steps,
- interpolates environment variables, params, test data, and saved resources,
- and executes each scenario through the shared engine.

## Where Testing Configuration Lives

Testing support is declared in module metadata under the `testing` key. That metadata can contain:

- `specs` for custom test spec registration,
- `roles` and `users` for testing-oriented identity setup,
- `data` for test fixtures,
- `scenarios` for executable test flows.

## Operational Entry Point

The operational entry point for testing is `solidctl`.

The main commands you will use are:

```bash
npx @solidxai/solidctl@latest test data --setup
npx @solidxai/solidctl@latest seed
npx @solidxai/solidctl@latest test data --load
npx @solidxai/solidctl@latest test run --module <module-name>
npx @solidxai/solidctl@latest test data --teardown
```

For the command reference itself, see [solidctl Reference](../solidctl-commands.md).
