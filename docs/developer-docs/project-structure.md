---
title: Project Structure
description: Overview of the folder structure for a SolidX fullstack application.
summary: This document provides a practical overview of the SolidX project structure, organized into backend (`solid-api`) and frontend (`solid-ui`) applications. The backend is a NestJS application that contains source code, module metadata, logs, uploaded media, and rebuild scripts. The frontend is a Vite + React application that boots the SolidX UI shell from `src/`, registers project-specific UI modules, and composes routes, reducers, middleware, and assets on top of `@solidxai/core-ui`. The document also highlights key SolidX dependencies, debugging configuration, and upgrade scripts.
sidebar_position: 3
solidx_concerns: []
---

import { FaFolder,FaBoxOpen,FaPuzzlePiece,FaLightbulb } from "react-icons/fa";


#  Project Structure

This project is organized into a backend API (`solid-api`) and a frontend UI (`solid-ui`) along with supporting scripts and configurations.

```bash
.
├── .vscode/                  # VS Code settings
├── solid-api/                # Backend API (NestJS)
├── solid-ui/                 # Frontend UI (Vite + React)
└── upgrade.sh                # SolidX upgrade script
```

##  solid-api/ - Backend (NestJS & TypeORM)

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


   <h4 className="card-title card-headear-wrapper">
      <FaFolder size={20} style={{ marginRight: "2px" }} />

  ###  Notable Subfolders
   </h4>


  - `src/`
    - Contains `main.ts` (entry point for the SolidX backend) and all SolidX modules like:
      - `fees-portal/`
    - `main-cli.ts` -> entry point for the SolidX cli commands.
    - `app.module.ts` ->  Contains the application module configuration.
    - `app-default-database.module.ts` -> Contains all the database configuration.

   <h4 className="card-title card-headear-wrapper">
      <FaBoxOpen size={22} style={{ marginRight: "2px" }} />

  ###  SolidX dependencies
   </h4>
  - `@solidxai/core`
    - Contains the core SolidX module which provides the core backend services for SolidX.
  - `@solidxai/code-builder`
    - Contains the functionality for generating the code in the SolidX backend.


  <h4 className="card-title card-headear-wrapper">
      <FaPuzzlePiece size={20} style={{ marginRight: "2px" }} />

  ###  SolidX modules
   </h4>

  
  - A SolidX module is a logical container that groups together related models and functionality under a unified domain or feature area e.g `fees-portal`.
  - You can find the structure for a SolidX module here [Generated Code](../developer-docs/extending/code-generation/index.md).  
  ---

##  solid-ui/ - Frontend (Vite & React)

The frontend is built as a Vite + React application. The generated app is intentionally thin: it bootstraps routing, theming, and Redux wiring, then layers project-specific UI modules on top of the shared `@solidxai/core-ui` package.

```bash
solid-ui/
├── .env, .gitignore          # Environment config and ignore files
├── dist/                     # Production build output
├── index.html                # Vite HTML entry
├── public/                   # Static assets copied as-is
├── src/                      # Application bootstrap and project-specific UI modules
├── local_packages/           # Optional locally linked SolidX packages
├── package.json              # Scripts and dependencies
├── tsconfig*.json            # TypeScript configuration
├── vite.config.ts            # Vite configuration
├── eslint.config.js          # Lint configuration
├── deploy.sh                 # Project deployment helper (if present)
```


   <h4 className="card-title card-headear-wrapper">
      <FaFolder size={20} style={{ marginRight: "2px" }} />

  ###  Notable Subfolders
   </h4>

  - `src/`
    - Contains the application bootstrap and all project-specific SolidX UI extensions.
    - Common entry files include:
      - `main.tsx` -> mounts the React app.
      - `App.tsx` -> wraps the app with the application router, store, layout, theme, and event-listener providers required by SolidX.
      - `AppRoutes.tsx` -> creates the route tree by calling `getSolidRoutes(...)` from `@solidxai/core-ui`.
      - `solid-ui-modules.ts` -> auto-discovers `*.ui-module.ts` files, registers their extensions, and builds the combined runtime for routes, reducers, and middleware.
    - App-specific features usually live under a module folder such as `src/venue/` or `src/fees-portal/`.
    - A typical module folder contains:
      - `*.ui-module.ts` -> the module registration file that contributes custom routes, extension components, extension functions, reducers, and middleware.
      - `admin-layout/` -> overrides or extends generated admin layouts with custom widgets, actions, and form/list behavior.
      - `custom-layout/` -> fully custom pages such as dashboards, login pages, and home screens.
      - `redux/` -> RTK Query APIs or other Redux slices owned by the module.
      - `utils/` -> module-specific helpers such as export utilities or formatting logic.
  - `public/`
    - Contains static files such as logos, icons, uploaded brand assets, and theme resources.
    - Theme files from `@solidxai/core-ui` are often copied here during `postinstall`.
  - `local_packages/`
    - Used when developing against local builds of shared SolidX packages instead of published npm versions.




<!-- ###  -->
   <h4 className="card-title card-headear-wrapper">
      <FaBoxOpen size={22} style={{ marginRight: "2px" }} />

  ###  SolidX dependencies
   </h4>

- `@solidxai/core-ui`
  - Contains the shared SolidX UI framework used by project apps.
  - Provides:
    - Route generation via `getSolidRoutes(...)`
    - Application providers such as `StoreProvider`, `LayoutProvider`, and `SolidThemeProvider`
    - Reusable admin pages, auth flows, layouts, widgets, and extension points
    - Shared Redux helpers, hooks, adapters, resources, and themes

### Key `@solidxai/core-ui` folders

```bash
solid-core-ui/src/
├── adapters/                 # Auth and integration adapters
├── components/               # Shared UI components
├── hooks/                    # Reusable React hooks
├── layouts/                  # Layout primitives and admin layout building blocks
├── modules/                  # Shared module-level UI behavior
├── redux/                    # Store helpers, APIs, hooks, and features
├── resources/                # Themes, fonts, images, and stylesheets
├── routes/                   # Shared route definitions and guards
├── types/                    # Shared TypeScript types
└── ui/                       # Higher-level UI exports and composition helpers
```
  
##  Debugging - VS Code
Contains editor-specific configurations like `launch.json` for debugging and IDE behavior.

##  Upgrade Scripts
`upgrade.sh`: Used for upgrading the core SolidX backend/frontend dependencies.

<div className="tips-box">
  <h4 className="card-headear-wrapper">
    <FaLightbulb className="feature-icon" />
    Tips 
  </h4>
  <ul>
    <li>All environment variables are stored in <span className="color-green"> .env </span> files within each app folder.</li>
  </ul>
</div>
