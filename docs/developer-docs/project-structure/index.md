---
title: Project Structure
description: Overview of the folder structure for the SolidX Fullstack Application.
sidebar_position: 3
---

# 📦 Project Structure

This project is organized into a backend API (`solid-api`) and frontend UI (`solid-ui`) along with supporting scripts and configurations.

```bash
.
├── .vscode/                  # VS Code settings (e.g. debug configuration)
├── solid-api/                # Backend API built with NestJS
├── solid-ui/                 # Frontend UI built with Next.js
└── upgrade.sh                # SolidX upgrade script
```

## 🛠️ `solid-api/` - Backend (NestJS & TypeORM)

This folder contains all backend services, business logic, and configurations.

```bash
solid-api/
├── .env, .gitignore, etc.       # Config and ignore files
├── logs/                        # Log files for application and errors
├── media-files-storage/         # Uploaded or generated media/data files
├── media-uploads/               # Temporary media uploads folder
├── module-metadata/             # Per-module metadata as json files
├── src/                         # Source code for the backend
├── test/                        # E2E tests
├── rebuild*.sh / refresh.bat    # Rebuild and refresh scripts
```

### 🔹 Notable Subfolders

- `src/`
  - Contains `main.ts` (entry point for the SolidX backend) and all functional modules like:
    - `fees-portal/`
  - `main-cli.ts` -> entry point for the SolidX cli commands.
  - `app.module.ts` ->  Contains the application module configuration.
  - `app-default-database.module.ts` -> Contains all the database configuration.

### 📦 SolidX dependencies
- `@solidstarters/solid-core`
  - Contains the core SolidX module which provides the core backend services for SolidX.
- `@solidstarters/solid-code-builder`
  - Contains the functionality for generating the code in the SolidX backend.

### 📝 TODO
 - Add more detailed documentation about the functional module project structure  
---

## 🎨 `solid-ui/` - Frontend (Next.js & Prime React)

The frontend is built using Next.js and Prime React components.

```bash
solid-ui/
├── .env, .gitignore, etc.       # Config and ignore files
├── .next/                       # Next.js build output (auto-generated)
├── app/                         # App Router pages (e.g., admin, auth)
├── public/                      # Static assets like icons and SVGs
├── redux/                       # Global Redux store config
├── types/                       # TypeScript type declarations
├── next.config.js, middleware.ts, etc. # App-wide config and middlewares
```

### 🔹 Notable Subfolders

- `app/`
  - Entry point for routes like `/admin`, `/auth`, etc.
  - layout and providers via `layout.tsx` and `GlobalProvider.tsx`.
- `public/`
  - Contains static files and theme assets.
- `redux/`
  - Global state configuration.

### 📦 SolidX dependencies
- `@solidstarters/solid-core-ui`
  - Contains the core ui components for the SolidX UI.
---

## 🔧 `Debugging` - VS Code

Contains editor-specific configurations like `launch.json` for debugging and IDE behavior.

---

## 🔁 Upgrade Scripts
- `upgrade.sh`: Used for upgrading the core SolidX backend/frontend dependencies.

---

## 🧭 Tips
- All environment variables are stored in `.env` files within each app folder.

---