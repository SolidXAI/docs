---
title: Project Structure
icon: "folder-tree"
description: Overview of the folder structure for the SolidX Fullstack Application.
summary: This document provides a comprehensive overview of the SolidX project folder structure, organized into backend (solid-api) and frontend (solid-ui) components. The solid-api folder contains NestJS-based backend services with source code, module metadata, logs, and media storage. The solid-ui folder houses the Next.js frontend with PrimeReact components, including app routes, Redux state management, and static assets. The document also covers key dependencies including @solidstarters/solid-core for backend services, solid-code-builder for code generation, and solid-core-ui for frontend components. It includes debugging configurations and upgrade scripts.
solidx_concerns: []
---

This project is organized into a backend API (`solid-api`) and frontend UI (`solid-ui`) along with supporting scripts and configurations.

```bash
.
├── .vscode/                  # VS Code settings
├── solid-api/                # Backend API (NestJS)
├── solid-ui/                 # Frontend UI (Next.js)
└── upgrade.sh                # SolidX upgrade script
```

## solid-api/ - Backend (NestJS & TypeORM)

This folder contains all backend services, business logic, and configurations.

```bash
solid-api/
├── .env, .gitignore, etc.       # Config and ignore files
├── logs/                        # Application / Error logs
├── media-files-storage/         # Uploaded or generated files
├── media-uploads/               # Temporary upload folder
├── module-metadata/             # Module metadata (JSON)
├── src/                         # Source code for the backend
├── test/                        # E2E tests
├── rebuild*.sh / refresh.bat    # Rebuild and refresh scripts
```

### Notable Subfolders

- `src/`
  - Contains `main.ts` (entry point for the SolidX backend) and all SolidX modules like `fees-portal/`
  - `main-cli.ts` — entry point for the SolidX CLI commands
  - `app.module.ts` — contains the application module configuration
  - `app-default-database.module.ts` — contains all the database configuration

### SolidX Dependencies

- `@solidstarters/solid-core` — contains the core SolidX module which provides the core backend services for SolidX
- `@solidstarters/solid-code-builder` — contains the functionality for generating the code in the SolidX backend

### SolidX Modules

A SolidX module is a logical container that groups together related models and functionality under a unified domain or feature area (e.g., `fees-portal`).

You can find the structure for a SolidX module here: [Generated Code](../developer-docs/extending/code-generation/index.md)

## solid-ui/ - Frontend (Next.js & Prime React)

The frontend is built using Next.js and Prime React components.

```bash
solid-ui/
├── .env, .gitignore       # Config / ignore files
├── .next/                 # Next.js build output
├── app/                   # App Router pages (e.g., admin, auth)
├── public/                # Static assets like icons and SVGs
├── redux/                 # Global Redux store config
├── types/                 # TypeScript type declarations
├── next.config.js         # Next.js configuration
├── middleware.ts          # App-wide config and middlewares
```

### Notable Subfolders

- `app/` — entry point for routes like `/admin`, `/auth`, etc. Layout and providers via `layout.tsx` and `GlobalProvider.tsx`
- `public/` — contains static files and theme assets
- `redux/` — global state configuration

### SolidX Dependencies

- `@solidstarters/solid-core-ui` — contains the core UI components for the SolidX UI

## Debugging - VS Code

Contains editor-specific configurations like `launch.json` for debugging and IDE behavior.

## Upgrade Scripts

`upgrade.sh`: Used for upgrading the core SolidX backend/frontend dependencies.

> **Tip:** All environment variables are stored in `.env` files within each app folder.
