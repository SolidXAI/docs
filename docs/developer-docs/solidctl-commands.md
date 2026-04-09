---
sidebar_position: 2
title: solidctl Reference
description: Comprehensive reference for using the SolidX Control Plane CLI (solidctl) to manage your SolidX application.
---

The `solidctl` CLI is the primary tool for scaffolding, building, and maintaining SolidX projects. Run it from your project root using `npx @solidxai/solidctl@latest <command>`.

For help on any command:
```bash
# List all available commands
npx @solidxai/solidctl@latest --help

# Show detailed options for a specific command
npx @solidxai/solidctl@latest help <command>
```

:::info Under the hood
`solidctl` wraps the `solid` CLI that is built into your project, providing a consistent top-level interface regardless of your project setup.
:::


### Quick Reference

| Command | Description |
|---|---|
| [`create-app`](#create-app) | Scaffold a new SolidX project with backend (NestJS) and frontend (React). |
| [`build`](#build) | Compiles the latest code changes in `solid-api` and `solid-ui` into executable output — run this before other `solidctl` commands to ensure they pick up your latest changes. |
| [`seed`](#seed) | Bootstrap SolidX metadata, settings, and the system user. |
| [`generate`](#generate) | Generate code from model and module metadata definitions. |
| [`upgrade`](#upgrade) | Upgrade `@solidxai` dependencies to their latest published versions. |
| [`info`](#info) | Print information about the current SolidX project. |
| [`test`](#test) | Run the SolidX metadata-driven test suite. |
| [`mcp`](#mcp) | Start the SolidX MCP server for AI integrations. |

---

## Typical Workflow

**First-time setup:**
```bash
# Scaffold a new SolidX project
npx @solidxai/solidctl@latest create-app

# Compile the project
npx @solidxai/solidctl@latest build

# Bootstrap metadata, settings, and the system user
npx @solidxai/solidctl@latest seed
```

**Generating code from model metadata definitions:**
```bash
# Generate code for all models within a module
npx @solidxai/solidctl@latest generate module <module-name>

# Generate code for a single model
npx @solidxai/solidctl@latest generate model <model-name>
```

**Keeping dependencies up to date:**
```bash
# Upgrade to the latest beta release (default behaviour)
npx @solidxai/solidctl@latest upgrade

# Upgrade to the latest stable release
npx @solidxai/solidctl@latest upgrade --stable
```

---

## create-app

Scaffolds a new SolidX project, creating a `solid-api` (NestJS backend) and `solid-ui` (React frontend) in a new project directory.

By default, runs an interactive setup wizard that prompts you for configuration. Use `--no-interactive` to skip prompts and supply everything via flags.

```bash
npx @solidxai/solidctl@latest create-app [options]
```

### Options

| Flag | Default | Description |
|---|---|---|
| `--no-interactive` | — | Skip all prompts; use flags or defaults |
| `--name <name>` | `my-solid-app` | Project name (used as directory name in kebab-case) |
| `--api-port <port>` | `3000` | Port for the backend API server |
| `--ui-port <port>` | `3001` | Port for the frontend dev server |
| `--db-client <client>` | `PostgreSQL` | Database type: `PostgreSQL` or `MSSQL` |
| `--db-host <host>` | `localhost` | Database host |
| `--db-port <port>` | `5432` / `1433` | Database port (auto-set based on client) |
| `--db-name <name>` | `solidx_app_db` | Database name |
| `--db-username <username>` | `solidx_app_user` | Database username |
| `--db-password <password>` | `strongpassword` | Database password (change this for any non-local environment) |
| `--db-synchronize <yes\|no>` | `No` | Auto-sync DB schema on startup |
| `--verbose` | — | Show detailed logs during installation |

### What it does

1. Creates a new directory for your project (kebab-cased from `--name`)
2. Copies the `solid-api` and `solid-ui` boilerplate templates into the directory
3. Installs npm dependencies for both projects
4. Generates `.env` files for the backend and frontend from your configuration
5. Prints next steps including how to build, seed, and run the development servers

### After running

Your project will have the following structure:
```
<project-name>/
├── solid-api/   (NestJS backend)
└── solid-ui/    (React frontend)
```

The default system admin credentials are:
- **Username:** `sa`
- **Password:** `Admin@3214$`

:::tip
After `create-app`, your next steps are [`build`](#build) then [`seed`](#seed).
:::

---

## build

Builds both `solid-api` (backend) and `solid-ui` (frontend), so that your latest code changes are ready to be used when running other `solidctl` commands.

```bash
npx @solidxai/solidctl@latest build [options]
```

### Options

| Flag | Description |
|---|---|
| `--ui-only` | Build only `solid-ui` and skip the `solid-api` build |

Re-run `build` after making code changes or after running [`upgrade`](#upgrade) to ensure everything is up to date.

---

## seed

Bootstraps the SolidX platform in your database — populating core metadata, default settings, and creating the initial system user account.

```bash
npx @solidxai/solidctl@latest seed
```

:::note Prerequisites
[`build`](#build) must be run before `seed`.
:::

Run `seed`:
- Once when setting up a new project
- After manually editing module metadata JSON configuration files, to seed the changes to the database
- After certain version upgrades, if new platform metadata needs to be bootstrapped

---

## generate

Generates backend and frontend code from your model and module metadata definitions. This is the core command you use during feature development — after defining or updating metadata, you run `generate` to produce the corresponding TypeScript/React code.

`generate` has two subcommands:

### generate module

Generates code for all models within an entire module. This is the recommended approach.

```bash
npx @solidxai/solidctl@latest generate module <module-name>
```

**Example:**
```bash
npx @solidxai/solidctl@latest generate module Fees
```

### generate model

Generates code for a single model and its directly related models. Use this for a quicker, more targeted refresh when only one model has changed.

```bash
npx @solidxai/solidctl@latest generate model <model-name>
```

**Example:**
```bash
npx @solidxai/solidctl@latest generate model FeeStructure
```

:::note
Code generation uses AST-level file updates, meaning it intelligently merges generated code with any custom logic you have added to the generated files, rather than overwriting them entirely.

If you are running `solid-api` and `solid-ui` in development mode (`npm run solidx:dev`), the dev server will pick up the file changes and hot-reload automatically — but that is the dev server's behaviour, not part of this command itself.
:::

---

## upgrade

Upgrades the `@solidxai` packages (`@solidxai/core`, `@solidxai/code-builder`, `@solidxai/core-ui`) in your `solid-api` and `solid-ui` projects to the latest published versions.

By default, upgrades to the latest **beta** pre-release. Use `--stable` to upgrade to the latest stable release.

```bash
npx @solidxai/solidctl@latest upgrade [options]
```

### Options

| Flag | Description |
|---|---|
| `--stable` | Upgrade to the latest stable release instead of beta |
| `--tag <tag>` | Upgrade to a specific pre-release tag (e.g. `alpha`, `rc`) |
| `--dry-run` | Print the commands that would run without executing them |

### Examples

```bash
# Upgrade to latest beta (default)
npx @solidxai/solidctl@latest upgrade

# Upgrade to latest stable release
npx @solidxai/solidctl@latest upgrade --stable

# Upgrade to a specific pre-release tag
npx @solidxai/solidctl@latest upgrade --tag alpha

# Preview what would be upgraded without making changes
npx @solidxai/solidctl@latest upgrade --dry-run
```

After upgrading, run [`build`](#build) again to recompile `solid-api` with the updated packages.

---

## info

Prints information about the current SolidX project — versions, configuration, and environment details.

```bash
npx @solidxai/solidctl@latest info [args]
```

This is a pass-through to `solid info` inside `solid-api/`. Use it when diagnosing issues or when asked for project details by the SolidX support team.

---

## test

Runs testing scenarios and manages test data for your SolidX project. Tests are defined in the `testing` section of your module metadata configuration.

The `test` command has two subcommands:

### test run

Runs testing scenarios defined in a module's metadata.

```bash
npx @solidxai/solidctl@latest test run --module <module-name> [options]
```

#### Options

| Flag | Description |
|---|---|
| `-m, --module <name>` | **(Required)** Module name to load test scenarios from |
| `--scenario-ids <ids>` | Comma-separated list of scenario IDs to run (runs all if omitted) |
| `--include-tags <tags>` | Comma-separated list of tags — only scenarios matching all tags are run |
| `--skip-scenario-ids <ids>` | Comma-separated list of scenario IDs to skip |
| `--api-base-url <url>` | API base URL (defaults to `BASE_URL` env variable) |
| `--ui-base-url <url>` | Frontend base URL (defaults to `FRONTEND_BASE_URL` env variable) |
| `--headless <true\|false>` | Run browser in headless mode (default: `true`) |
| `--timeout-ms <number>` | Default scenario timeout in milliseconds |
| `--retries <number>` | Default number of retries per scenario |
| `--list-specs` | List all registered test specs and exit without running |
| `--print-api-logs` | Print full API request/response logs for each step |

#### Examples

```bash
# Run all test scenarios for a module
npx @solidxai/solidctl@latest test run --module Fees

# Run specific scenarios by ID
npx @solidxai/solidctl@latest test run --module Fees --scenario-ids sc-001,sc-002

# Run only scenarios matching a tag
npx @solidxai/solidctl@latest test run --module Fees --include-tags smoke

# Run with browser visible and verbose API logs
npx @solidxai/solidctl@latest test run --module Fees --headless false --print-api-logs

# List all registered test specs without running
npx @solidxai/solidctl@latest test run --module Fees --list-specs
```

### test data

Manages test data for your project — seeding, setting up, or tearing down test database environments.

```bash
npx @solidxai/solidctl@latest test data <--load|--setup|--teardown> [options]
```

Exactly one of `--load`, `--setup`, or `--teardown` must be specified.

#### Options

| Flag | Description |
|---|---|
| `--load` | Seed test data from the `testing.data` sections of module metadata |
| `--setup` | Create a new test datasource environment file and manifest |
| `--teardown` | Delete the test datasource environment/manifest and drop test databases |
| `--modules-to-test <names>` | Comma-separated list of module names to load test data for (used with `--load`; defaults to all modules) |

#### Examples

```bash
# Set up test database environment
npx @solidxai/solidctl@latest test data --setup

# Load test data for all modules
npx @solidxai/solidctl@latest test data --load

# Load test data for specific modules only
npx @solidxai/solidctl@latest test data --load --modules-to-test Fees,Onboarding

# Tear down test databases after testing
npx @solidxai/solidctl@latest test data --teardown
```

---

## mcp

Starts the SolidX MCP (Model Context Protocol) server, which exposes your project's metadata to AI tooling.

```bash
npx @solidxai/solidctl@latest mcp [args]
```

This is a pass-through to `solid mcp` inside `solid-api/`. Any additional arguments are forwarded to the underlying command.

---

:::tip Legacy Migration
If your project was previously using `@solidstarters` packages (the older package namespace), run `npx @solidxai/solidctl@latest legacy-migrate` to automatically update your dependencies and import paths to the current `@solidxai` namespace.
:::
