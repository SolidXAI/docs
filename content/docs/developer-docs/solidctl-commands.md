---
title: solidctl Reference
icon: "terminal"
description: Reference for the SolidX CLI (`solidctl`) used to scaffold, build, upgrade, inspect, seed, test, generate, and run agent tasks in a SolidX project.
---

# solidctl Reference

The `solidctl` CLI is the main command-line entry point for working with SolidX projects.

<Callout type="info" title="Mental Model">

  Think of <code>solidctl</code> as the <strong>operational control surface</strong> for a SolidX project.
  - <strong>Bootstrap commands</strong> create and build the project.
    - <strong>Platform commands</strong> seed metadata and inspect project state.
    - <strong>Development commands</strong> regenerate code and update package versions.
    - <strong>Testing commands</strong> prepare isolated test environments and run scenarios.
    - <strong>Agent commands</strong> run the SolidX AI agent.
  So the intuition is: <strong><code>solidctl</code> is not just a scaffolding command</strong>. It is the main CLI you use across the entire lifecycle of a SolidX app, from project creation to testing and maintenance.

</Callout>

Run it from your project root:

```bash
npx @solidxai/solidctl@latest <command>
```

For help:

```bash
# Top-level help
npx @solidxai/solidctl@latest --help

# Command-specific help
npx @solidxai/solidctl@latest <command> --help
```

> **Info**

> This page intentionally documents the most commonly used commands and skips a few internal or less commonly needed ones. In particular, it does **not** document `mcp`, `legacy-migrate`, `local-upgrade`, or `release`.

## Quick Reference

| Command | Description |
|---|---|
| [`create-app`](#create-app) | Scaffold a new SolidX project. |
| [`build`](#build) | Build the project and set up the Solid CLI. |
| [`upgrade`](#upgrade) | Upgrade SolidX package dependencies. |
| [`seed`](#seed) | Install or refresh seeded metadata and platform settings. |
| [`info`](#info) | Print information about the current project. |
| [`test`](#test) | Seed test data or run metadata-driven testing scenarios. |
| [`generate`](#generate) | Generate backend code boilerplate from metadata. |
| [`agent`](#agent) | Start the SolidX AI agent server or run a single task. |

## Command Families

It can help to group the commands mentally before reading the detailed reference:

- **Bootstrap:** `create-app`, `build`
- **Platform lifecycle:** `seed`, `info`
- **Development workflow:** `generate`, `upgrade`
- **Testing workflow:** `test`
- **AI workflow:** `agent`

## Typical Workflow

### First-time setup

```bash
# Scaffold a new project
npx @solidxai/solidctl@latest create-app

# Build the project
npx @solidxai/solidctl@latest build

# Seed metadata, settings, and the system user
npx @solidxai/solidctl@latest seed
```

### Day-to-day development

```bash
# Regenerate code from metadata
npx @solidxai/solidctl@latest generate module

# Build after upgrades or major changes
npx @solidxai/solidctl@latest build

# Inspect project information
npx @solidxai/solidctl@latest info --detailed
```

### Testing workflow

```bash
# Set up test datasource files and databases
npx @solidxai/solidctl@latest test data --setup

# Seed test data
npx @solidxai/solidctl@latest test data --load

# Run module scenarios
npx @solidxai/solidctl@latest test run --module Fees
```

## create-app

Scaffolds a new SolidX project with:

- `solid-api` for the backend
- `solid-ui` for the frontend

By default, `create-app` runs interactively. Use `--no-interactive` to skip prompts and rely on flags/defaults instead.

```bash
npx @solidxai/solidctl@latest create-app [options]
```

### Options

| Flag | Default | Description |
|---|---|---|
| `--verbose` | — | Show detailed logs during installation |
| `--no-interactive` | — | Skip all prompts and use defaults or provided flags |
| `--name <name>` | `my-solid-app` | Project name |
| `--api-port <port>` | `3000` | Backend API port |
| `--db-client <client>` | `PostgreSQL` | Database type: `PostgreSQL` or `MSSQL` |
| `--db-host <host>` | `localhost` | Database host |
| `--db-port <port>` | `5432` / `1433` | Database port |
| `--db-name <name>` | `solidx_app_db` | Database name |
| `--db-username <username>` | `solidx_app_user` | Database username |
| `--db-password <password>` | `strongpassword` | Database password |
| `--db-synchronize <yes\|no>` | `Yes` | Auto-sync DB schema |
| `--ui-port <port>` | `3001` | Frontend port |

### What it does

1. Creates a new project directory.
2. Scaffolds `solid-api` and `solid-ui`.
3. Installs dependencies.
4. Writes environment configuration.
5. Prints the next commands to run.

### Recommended next steps

```bash
npx @solidxai/solidctl@latest build
npx @solidxai/solidctl@latest seed
```

## build

Builds SolidX and sets up the Solid CLI.

```bash
npx @solidxai/solidctl@latest build [options]
```

### Options

| Flag | Description |
|---|---|
| `--ui-only` | Build only `solid-ui` and skip the `solid-api` build |

### Notes

- Run this after scaffolding a new project.
- Run this again after upgrades.
- Run this if CLI-backed commands are not seeing your latest local code.

## upgrade

Upgrades SolidX dependencies. By default, this upgrades to the latest **beta** pre-release.

```bash
npx @solidxai/solidctl@latest upgrade [options]
```

### Options

| Flag | Description |
|---|---|
| `--core` | Upgrade `solid-core` only |
| `--ui` | Upgrade `solid-ui` only |
| `--code-builder` | Upgrade `solid-code-builder` only |
| `--dry-run` | Show commands without executing |
| `--stable` | Upgrade to the latest stable release instead of beta |
| `--tag <tag>` | Install a specific pre-release tag such as `alpha` or `rc` |

### Examples

```bash
# Upgrade everything to latest beta
npx @solidxai/solidctl@latest upgrade

# Upgrade only solid-core
npx @solidxai/solidctl@latest upgrade --core

# Upgrade only solid-ui
npx @solidxai/solidctl@latest upgrade --ui

# Upgrade only solid-code-builder
npx @solidxai/solidctl@latest upgrade --code-builder

# Upgrade to latest stable
npx @solidxai/solidctl@latest upgrade --stable

# Upgrade to a specific pre-release track
npx @solidxai/solidctl@latest upgrade --tag alpha

# Preview without changing anything
npx @solidxai/solidctl@latest upgrade --dry-run
```

### Recommended follow-up

After upgrading, run:

```bash
npx @solidxai/solidctl@latest build
```

## seed

Seeds metadata and platform-level data into the application.

```bash
npx @solidxai/solidctl@latest seed [options]
```

### Options

| Flag | Default | Description |
|---|---|---|
| `-m, --modules-to-seed [module names]` | all modules | Comma-separated list of module names to seed |
| `-s, --seeder [seeder name]` | `ModuleMetadataSeederService` | Seeder to run |
| `--prune` | — | Remove metadata that is no longer present in JSON |

### When to use it

- after initial project setup
- after changing metadata JSON files
- after upgrades that introduce new platform metadata

### Examples

```bash
# Seed everything
npx @solidxai/solidctl@latest seed

# Seed only selected modules
npx @solidxai/solidctl@latest seed --modules-to-seed Fees,Onboarding

# Seed and prune removed metadata
npx @solidxai/solidctl@latest seed --prune
```

## info

Prints information about the consuming project.

```bash
npx @solidxai/solidctl@latest info [options]
```

### Options

| Flag | Description |
|---|---|
| `-d, --detailed` | Print more details about the consuming project |

Use this when debugging project configuration, versions, or runtime setup.

## test

The `test` command has two main areas:

- `test data` for test data and datasource lifecycle tasks
- `test run` for scenario execution

For the broader testing architecture, vocabulary, and workflow, see [Testing](./testing/index.md).

```bash
npx @solidxai/solidctl@latest test [command]
```

### test data

Seeds test data from metadata or manages test datasource setup and teardown.

```bash
npx @solidxai/solidctl@latest test data [options]
```

#### Options

| Flag | Description |
|---|---|
| `--load` | Seed test data from `testing.data` sections |
| `--setup` | Create a new `.env.<dbRunName>` and test datasource manifest |
| `--teardown` | Delete the test datasource env/manifest and drop test databases |
| `--modules-to-test [module names]` | Comma-separated list of module names to test; defaults to all modules |

#### Examples

```bash
# Set up test environment
npx @solidxai/solidctl@latest test data --setup

# Load all test data
npx @solidxai/solidctl@latest test data --load

# Load only selected modules
npx @solidxai/solidctl@latest test data --load --modules-to-test Fees,Onboarding

# Tear down test environment
npx @solidxai/solidctl@latest test data --teardown
```

### test run

Runs testing scenarios from module metadata.

```bash
npx @solidxai/solidctl@latest test run [options]
```

#### Options

| Flag | Description |
|---|---|
| `-m, --module [module name]` | Module name to load metadata from |
| `--scenario-ids [ids]` | Comma-separated list of scenario ids to run |
| `--include-tags [tags]` | Comma-separated list of tags; scenario must include all |
| `--skip-scenario-ids [ids]` | Comma-separated list of scenario ids to skip |
| `--reporter [name]` | Reporter name; currently `console` |
| `--list-specs [true\|false]` | List registered test specs and exit |
| `--print-api-logs [true\|false]` | Print full API request/response logs for `api.request` steps |
| `--api-base-url [url]` | API base URL; defaults to `process.env.BASE_URL` |
| `--ui-base-url [url]` | UI base URL; defaults to `process.env.FRONTEND_BASE_URL` |
| `--headless [true\|false]` | Run UI browser in headless mode; default `true` |
| `--timeout-ms [number]` | Default scenario timeout in milliseconds |
| `--retries [number]` | Default scenario retries |

#### Examples

```bash
# Run all scenarios for a module
npx @solidxai/solidctl@latest test run --module Fees

# Run specific scenarios
npx @solidxai/solidctl@latest test run --module Fees --scenario-ids sc-001,sc-002

# Run tagged scenarios only
npx @solidxai/solidctl@latest test run --module Fees --include-tags smoke

# Run with visible browser and verbose API logs
npx @solidxai/solidctl@latest test run --module Fees --headless false --print-api-logs true

# List registered specs
npx @solidxai/solidctl@latest test run --module Fees --list-specs true
```

## generate

Generates code boilerplate from model metadata configurations.

```bash
npx @solidxai/solidctl@latest generate [command]
```

### Subcommands

| Subcommand | Description |
|---|---|
| `model` | Generate code for a single model and its related models |
| `module` | Generate code for an entire module; this is the recommended path |

### Guidance

- Prefer `generate module` for most workflows.
- Use `generate model` when you want a smaller, targeted refresh.
- This command is about metadata-driven code generation, primarily for generated backend structure.

For a deeper explanation of generated structure and the surrounding conventions, see [Code Generation](./extending/code-generation/index.md).

## agent

Runs the SolidX AI agent.

```bash
npx @solidxai/solidctl@latest agent [command]
```

### Subcommands

| Subcommand | Description |
|---|---|
| `start` | Start the AI agent server |
| `run <task>` | Run a single agent task |

### Examples

```bash
# Show help for the agent command
npx @solidxai/solidctl@latest agent --help

# Show help for starting the agent server
npx @solidxai/solidctl@latest agent start --help

# Run a single task
npx @solidxai/solidctl@latest agent run "summarise project metadata"
```
