---
title: Workflow
icon: "git-branch"
description: End-to-end workflow for setting up SolidX for automated testing, loading data, running tests, and tearing down safely.
---

# Testing Workflow

This page describes the end-to-end operational workflow for running automated tests in SolidX.

The goal of this workflow is to bring the application into **SUT mode**: a clean, isolated **system under test** with predictable metadata, predictable test data, and safe cleanup afterwards.

## Canonical Workflow

The standard flow is:

1. Create isolated test datasources
2. Seed metadata into those datasources
3. Load test fixtures
4. Run test scenarios
5. Tear everything down

These are the canonical commands:

```bash
solidctl test data --setup
solidctl seed
solidctl test data --load
solidctl test run --module <module-name>
solidctl test data --teardown
```

## Step 1: Test Datasource Setup

Command:

```bash
solidctl test data --setup
```

This step creates isolated test databases or schemas for the datasources configured in the project.

What happens here:

- a unique run name is generated,
- `.env` is backed up,
- datasource database names are rewritten to test-specific names,
- fresh databases or schemas are created,
- and a manifest is written so teardown can later reverse the process safely.

This is what moves the project into SUT mode.

## Step 2: Seed Metadata

Command:

```bash
solidctl seed
```

This seeds the fresh test databases with the metadata required for the platform to function.

That includes things like:

- models,
- fields,
- views,
- actions,
- roles,
- permissions,
- users,
- settings,
- and other platform metadata.

Why this step matters:

- test data loading depends on model metadata being present,
- security and identity setup depend on seeded metadata,
- and scenario execution assumes the metadata model already exists.

## Step 3: Load Test Data

Command:

```bash
solidctl test data --load
```

This step ingests testing identity and fixture data from module metadata.

In order, it:

- creates test roles from `testing.roles` and binds their permissions,
- creates test users from `testing.users`,
- and loads fixture records from `testing.data` into the test databases.

Key characteristics:

- data stays close to the module that owns it,
- loading is metadata-aware and idempotent - existing roles and users are not duplicated,
- record inserts behave like upserts,
- and relations can be resolved using user-key based conventions.

'> **Note**

''> `solid seed` must complete before running `--load`. Controller permissions are registered during seeding, and role binding will fail if they are not yet in the database.
'

You can also limit the load to certain modules:

```bash
solidctl test data --load --modules-to-test venue,reports
```

## Step 4: Run Test Cases

Command:

```bash
solidctl test run --module venue --api-base-url http://localhost:3000 --ui-base-url http://localhost:5173 --headless false
```

This step executes `testing.scenarios` from the selected module metadata.

The runner:

- filters scenarios by ids or tags if requested,
- registers built-in and custom step handlers,
- creates adapters,
- runs API, UI, or mixed scenarios,
- and reports results to the configured reporter.

Useful variants:

```bash
solidctl test run --module venue --list-specs true
solidctl test run --module venue --include-tags smoke
solidctl test run --module venue --scenario-ids api-authenticate-success,api-create-states
```

## Step 5: Teardown

Command:

```bash
solidctl test data --teardown
```

This reverses the SUT setup process.

It typically:

- restores `.env` from its backup,
- deletes test datasource backups and manifests,
- drops the test databases or schemas that were created,
- and returns the local environment to its normal state.

This step is important because it keeps local development environments clean and prevents test databases from accumulating over time.

## Why This Workflow Exists

SolidX testing is intentionally workflow-heavy because the platform is metadata-driven.

That means good automated testing is not only about running assertions. It also depends on:

- predictable metadata,
- clean test datasources,
- deterministic fixture loading,
- and safe cleanup.

The setup/load/run/teardown pattern ensures the system under test is isolated enough to be trustworthy.

## Local Development vs CI

The same workflow works in both local and automated environments.

Local development usually emphasises:

- running tests against local API and UI servers,
- inspecting UI behaviour in headed browser mode,
- iterating on a narrow set of scenarios.

CI usually emphasises:

- deterministic setup,
- full teardown,
- headless browser execution,
- module-scoped or tag-scoped runs.

## Recommended SOP

For most teams, the safest operating procedure is:

1. Run `test data --setup`
2. Run `seed`
3. Run `test data --load`
4. Start the application servers if needed
5. Run `test run`
6. Always finish with `test data --teardown`

## Common Failure Modes

Typical problems usually come from one of these:

- skipping `seed` before loading test data,
- pointing `--api-base-url` or `--ui-base-url` at the wrong server,
- forgetting that UI tests require a running frontend,
- stale `.env` values after interrupted runs,
- running scenarios that depend on data that was never loaded.

Next: [Vocabulary](./vocabulary.md)
