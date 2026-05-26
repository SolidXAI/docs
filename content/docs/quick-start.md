---
title: Quick Start
description: "Get a SolidX project running in under 10 minutes, manually or let your AI agent do it."
summary: "Two paths to a working SolidX project. Manual mode walks you through every step. Agentic mode gives you a copy-paste prompt for Claude Code, Cursor, Codex, or any AI coding assistant."
icon: "rocket"
---

# Quick Start

Get a SolidX project running in under 10 minutes.

Two modes are available:

- **Manual mode**: you run each `solidctl` command yourself, step by step.
- **Agentic mode**: you paste a prompt into your AI coding assistant (Claude Code, Cursor, Codex CLI, etc.) and it handles the entire setup automatically.

Both paths produce the same result: a working SolidX project with backend and frontend.

---

## Prerequisites

| Requirement | Version | Required for | Check |
|---|---|---|---|
| **Node.js** | 22+ (LTS recommended) | All modes | `node -v` |
| **Docker** | Latest stable | Database setup (if you don't have PostgreSQL) | `docker --version` |
| **PostgreSQL** | 14+ | All modes, via Docker or existing instance | `psql --version` |
| **Python** | 3.11+ | Agent & MCP only | `python3 --version` |

Node.js and a PostgreSQL database are the only hard requirements. Docker is the easiest way to get PostgreSQL running if you don't already have one. Python is only needed if you plan to use the SolidX AI Agent or MCP server.

---

## Mode 1: Manual

### Step 1: Set up the database

If you already have PostgreSQL running, skip to Step 2 and use your existing credentials.

Otherwise, spin up a PostgreSQL container with Docker:

```bash
docker run -d \
  --name SolidX_DB \
  -e POSTGRES_USER=solidx_app_user \
  -e POSTGRES_PASSWORD=strongpassword \
  -e POSTGRES_DB=solidx_app_db \
  -p 5432:5432 \
  -v solidx_pgdata:/var/lib/postgresql/data \
  postgres:17
```

Remember these credentials. The scaffolding prompts will ask for them.

### Step 2: Scaffold the project

Choose the path that matches your database setup:

#### Path A: You used the Docker command above

Since your database uses the default credentials from Step 1, you can scaffold with a single one-shot command (replace `my-project` with your project name):

```bash
npx @solidxai/solidctl@latest create-app \
  --name my-project \
  --no-interactive \
  --db-client PostgreSQL \
  --db-host localhost \
  --db-port 5432 \
  --db-name solidx_app_db \
  --db-username solidx_app_user \
  --db-password strongpassword
```

#### Path B: You have an existing PostgreSQL database

Run the interactive scaffolding and enter your credentials when prompted:

```bash
npx @solidxai/solidctl@latest create-app
```

> **Scaffolding takes 5-10 minutes**
>
> The `create-app` command installs all npm dependencies for both backend and frontend. This is a one-time cost; subsequent commands like `build` and `seed` are much faster.

### Step 3: Build and seed

```bash
cd <your-project-name>

npx @solidxai/solidctl@latest build
npx @solidxai/solidctl@latest seed
```

- `build` compiles both backend and frontend.
- `seed` loads platform metadata, default settings, and the super admin user.

### Step 4: Start the services

From the project root, run a single `solidctl` command to start both the backend API and frontend admin panel in one supervisor:

```bash
npx @solidxai/solidctl@latest start:dev
```

Open the admin panel at `http://localhost:3001` and log in:

| Field | Value |
|---|---|
| Username | `sa` |
| Password | `Admin@3214$` |

That's it. Your SolidX project is running. Start building modules via the admin panel, or extend the generated code directly.

---

## Mode 2: Agentic

Paste the prompt below into your AI coding assistant (Claude Code, Cursor Agent, Codex CLI, Windsurf, etc.) from the directory where you want the project created.

> **How this works**
>
> The prompt is self-contained. Your AI agent will check prerequisites, set up the database if needed, and run all the commands. You only need to provide your PostgreSQL credentials if you already have an instance running on port 5432. Otherwise the agent spins one up via Docker with default credentials.

```
Set up a new SolidX project for me. Follow these steps in order. Do not skip any step. Report status after each step.

First, ask me for the project name I want to use.

Prerequisite checks:
- Verify Node.js 22+ is installed. If missing, install it via nvm (curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && source ~/.nvm/nvm.sh && nvm install 22). If nvm is also missing and cannot be installed, stop and tell me to install Node.js 22+ manually.
- Verify Docker is installed and running (docker info). If Docker is missing, stop and tell me to install Docker Desktop.

Database setup:
- Check if something is already listening on port 5432 (e.g. lsof -i :5432 or netstat).
- If port 5432 is FREE:
  - Run: docker run -d --name SolidX_DB -e POSTGRES_USER=solidx_app_user -e POSTGRES_PASSWORD=strongpassword -e POSTGRES_DB=solidx_app_db -p 5432:5432 -v solidx_pgdata:/var/lib/postgresql/data postgres:17
  - Use these DB credentials in the next step: host=localhost, port=5432, user=solidx_app_user, password=strongpassword, database=solidx_app_db
- If port 5432 is OCCUPIED (existing PostgreSQL):
  - Ask me for the database host, port, username, password, and database name.
  - Use the credentials I provide in the next step.

Project scaffold (this step takes 5-10 minutes; npm installs all dependencies for both backend and frontend):
- Run: npx @solidxai/solidctl@latest create-app --name <PROJECT_NAME> --no-interactive --db-client PostgreSQL --db-host <DB_HOST> --db-port <DB_PORT> --db-name <DB_NAME> --db-username <DB_USER> --db-password <DB_PASSWORD>
  (Use the project name I provided, and the DB credentials determined in the database setup step above.)
- Inform me that scaffolding is in progress and will take several minutes. Do not treat the long-running npm install as a failure. Wait for it to complete.

Build and seed:
- cd <PROJECT_NAME>
- npx @solidxai/solidctl@latest build
- npx @solidxai/solidctl@latest seed

Start the services (single supervisor that runs both backend and frontend):
- From the project root (<PROJECT_NAME>), run: npx @solidxai/solidctl@latest start:dev
- This starts both solid-api and solid-ui dev processes together. Run it as a background process so you can continue with the verification step.

Final verification:
- Confirm the backend API is reachable at http://localhost:3000
- Confirm the frontend admin panel is reachable at http://localhost:3001
- Report the project directory path, the URLs, and the super admin login (username: sa, password: Admin@3214$)
```

Your AI agent will execute all the steps and report back when the project is ready to use.

---

## Optional: SolidX AI Agent

Once your project is running, you can start the SolidX AI agent to build modules, models, and features through natural language.

### Start the agent server

```bash
npx @solidxai/solidctl@latest agent start
```

The agent auto-installs its Python package into `~/.solidx/venv` on first run if `solidx-agent` is not already in PATH. Open the Chat UI at `http://localhost:8765`.

### Run a single task (CLI)

```bash
npx @solidxai/solidctl@latest agent run "Build a CRM with Lead and Contact models, add name/email/phone fields"
```

Options:

| Flag | Default | Description |
|---|---|---|
| `-m, --mode` | `native` | Tool mode: `native` or `mcp` |
| `-l, --log-level` | `INFO` | Logging level |

---

## Optional: MCP Server

The MCP server exposes SolidX tools to external AI clients (Claude Desktop, Cursor, Codex CLI, etc.) over HTTP with API-key authentication.

### Start the MCP server

```bash
npx @solidxai/solidctl@latest mcp start
```

Options:

| Flag | Default | Description |
|---|---|---|
| `-p, --port` | `9000` | Listen port |
| `-H, --host` | `0.0.0.0` | Bind address |
| `--mount-path` | `/mcp` | URL path for the MCP endpoint |
| `-l, --log-level` | `INFO` | Logging level |

### Connect from Claude Desktop

1. Generate an API key in your SolidX admin panel (under IAM → API Keys).

2. Add the server to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "solidx": {
      "url": "http://localhost:9000/mcp",
      "headers": {
        "solidx-api-key": "sldx_..."
      }
    }
  }
}
```

3. Restart Claude Desktop. The SolidX tools will appear automatically.

### Connect from Cursor / Codex CLI

Point your MCP client at:

```
http://localhost:9000/mcp
```

Include the header `solidx-api-key: sldx_...` on every request.

---

## Common solidctl Commands

| Command | What it does |
|---|---|
| `create-app` | Scaffold a new project |
| `build` | Build backend + frontend |
| `seed` | Load metadata and system user |
| `agent start` | Start the AI agent server |
| `agent run "<task>"` | Run a single agent task |
| `mcp start` | Start the MCP server (HTTP) |
| `generate module` | Regenerate code from metadata |
| `upgrade` | Upgrade SolidX dependencies |
| `info --detailed` | Show project info |

Full reference: [solidctl Commands](/docs/developer-docs/solidctl-commands)

---

## Next Steps

- **Build modules** using the admin panel's Module Builder.
- **Customize layouts**: list views, form views, kanban boards.
- **Extend the backend**: controllers, services, providers.
- **Set up IAM**: roles, permissions, record-level security rules.
- **Go deeper**: read the [Tutorial](/docs/tutorial/), [Reference](/docs/developer-docs/), and [Recipes](/docs/recipes/).
