Set up a new SolidX project for me using a full PostgreSQL database. Follow these steps in order. Do not skip any step. Keep status updates brief - a short line per step is enough, no need for a detailed recap.

First, ask me for the project name I want to use. Default to "my-solid-app" if I don't specify one. Use this as `<PROJECT_NAME>` in every command below.

Prerequisite checks:

- Verify Node.js 22+ is installed. If missing, install it via nvm (curl -o- [https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.5/install.sh](https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.5/install.sh) | bash && source ~/.nvm/nvm.sh && nvm install 22). If nvm is also missing and cannot be installed, stop and tell me to install Node.js 22+ manually.
- Install the SolidX CLI globally: npm i -g @solidxai/solidctl@beta. Verify with `solidctl --version`. If this fails, stop and tell me to install it manually.
- Check whether Docker is installed and the daemon is running (`docker info`).
  - If Docker is running, continue to the database setup step below.
  - If Docker is not installed or not running, ask me whether I have an existing PostgreSQL 14+ instance you can connect to.
    - If yes, collect the host, port, database name, username, and password from me and skip the database setup step below.
    - If no, **stop here** and tell me to either start/install Docker, point you at an existing PostgreSQL instance, or explicitly ask you to fall back to the embedded PGlite database for a quick trial (note if I choose the embedded fallback: it needs no Docker or credentials, but the [SolidX AI Agent](/docs/quick-start/using-solidx-ai-agent) and [MCP server](/docs/quick-start/using-solidx-mcp-server) are early-alpha with it). Do not proceed until I respond.

Database setup (skip this step if I gave you an existing PostgreSQL instance, or if I explicitly chose the embedded fallback above):

- Use a project-scoped container and volume name so this doesn't collide with other SolidX projects on my machine: `<PROJECT_NAME>_db` and `<PROJECT_NAME>_pgdata`.
- If a container named `<PROJECT_NAME>_db` already exists (e.g. from a previous run of this prompt), start it if it's stopped and reuse it instead of creating a new one.
- Otherwise, start a fresh container:
  ```
  docker run -d \
    --name <PROJECT_NAME>_db \
    -e POSTGRES_USER=solidx_app_user \
    -e POSTGRES_PASSWORD=strongpassword \
    -e POSTGRES_DB=solidx_app_db \
    -p 5432:5432 \
    -v <PROJECT_NAME>_pgdata:/var/lib/postgresql/data \
    postgres:17
  ```
- If port 5432 is already in use by something else, pick the next free port (5433, 5434, ...), use `-p <PORT>:5432` instead, and use that same `<PORT>` in the scaffold step below.
- Wait for PostgreSQL to accept connections before continuing - poll with `docker exec <PROJECT_NAME>_db pg_isready` a few times if needed instead of proceeding immediately.

Project scaffold (this step takes 5-10 minutes; npm installs all dependencies for both backend and frontend):

- Full PostgreSQL (container you just started or an existing instance you connected to):
  ```
  solidctl create-app --no-interactive --name <PROJECT_NAME> \
    --db-client PostgreSQL \
    --db-host localhost \
    --db-port <PORT> \
    --db-name solidx_app_db \
    --db-username solidx_app_user \
    --db-password strongpassword
  ```
  Replace the `--db-*` values with whatever credentials I gave you if I pointed you at an existing instance.
- Embedded fallback only (if I explicitly asked for it): `solidctl create-app --no-interactive --embedded --name <PROJECT_NAME>`
- Let me know scaffolding is in progress and may take several minutes. Do not treat the long-running npm install as a failure. Wait for it to complete.

Connect MCP (wires up whichever supported AI clients are installed on my machine - Claude Code, Claude Desktop, Cursor, and Codex):

- Run: `cd <PROJECT_NAME> && solidctl mcp install`
- This reads the project's API key from `~/.solidx/<PROJECT_NAME>/mcp.json` and writes a `solidx-<PROJECT_NAME>-mcp` server entry into every detected client's config. Note which client(s) it configured, to mention in the final summary.

Start the services (a single supervisor runs the backend API, the frontend, and the MCP server together):

- Still inside `<PROJECT_NAME>`, run `solidctl start:dev` as a background process so you can continue with the verification step. This also starts the MCP server - no separate `mcp start` step is needed.
- Confirm the backend API comes up at http://localhost:3000 and the frontend admin panel at http://localhost:3001.
- Once you've confirmed both are up, **stop this background `start:dev` process** (and any child processes it spawned) before moving on. I will start it again myself per the restart instructions below - leaving your copy running would just fight over the same ports.

Final summary - give me a short summary here, not a step-by-step recap. Include only:

- The project directory path.
- The two URLs: API at http://localhost:3000, admin panel at http://localhost:3001.
- The super admin login: username `sa`, password `Admin@3214$`.
- Which AI client config(s) `mcp install` updated.

Restart required - read this carefully, the order matters:

- You already stopped the verification copy of `start:dev` in the previous step, so no services are running right now and there's no port conflict.
- Give me this exact single command to copy and run **myself in my own terminal window** (not something you run in the background), so the project runs independently of this session and survives a restart:
  ```
  cd <PROJECT_NAME> && solidctl start:dev
  ```
- Then tell me explicitly: "Run the command above in your own terminal to start the project, then restart me (this session/window) so I pick up the new SolidX MCP tools."
- Do not consider the setup incomplete because of this - scaffolding, MCP wiring, and service startup were all verified. The restart is only so the current AI session can see the new tools, and the command above is what keeps the servers running afterward.
