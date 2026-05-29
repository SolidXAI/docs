---
title: Project Structure
icon: "folder-tree"
description: Overview of the folder structure for a SolidX fullstack application.
summary: This document provides a practical overview of the SolidX project structure, organized into backend (`solid-api`) and frontend (`solid-ui`) applications. The backend is a NestJS application that contains source code, module metadata, logs, uploaded media, and rebuild scripts. The frontend is a Vite + React application that boots the SolidX UI shell from `src/`, registers project-specific UI modules, and composes routes, reducers, middleware, and assets on top of `@solidxai/core-ui`. The document also highlights key SolidX dependencies, debugging configuration, and upgrade scripts.
solidx_concerns: []
---



#  Project Structure

This project is organized into a backend API (`solid-api`) and a frontend UI (`solid-ui`) along with supporting scripts and configurations.

<Callout type="info" title="Mental Model">

  SolidX is designed to help you build <strong>full-stack applications</strong>, not just isolated backend services or isolated frontend sites.
  - <strong><code>solid-api</code>:</strong> owns metadata, persistence, APIs, business logic, and backend execution.
    - <strong><code>solid-ui</code>:</strong> owns the browser application, project-specific UI modules, routes, and user-facing workflows.
    - <strong>Shared SolidX packages:</strong> connect those two layers through metadata, generated structure, shared UI building blocks, and common conventions.
  So the intuition is: a SolidX project is a <strong>coordinated full-stack workspace</strong> where backend and frontend evolve together, rather than two unrelated folders living side by side.

</Callout>

```bash
.
├── .vscode/                  # VS Code settings
├── solid-api/                # Backend API (NestJS)
├── solid-ui/                 # Frontend UI (Vite + React)
└── upgrade.sh                # SolidX upgrade script
```

##  solid-api/ - Backend (NestJS & TypeORM)

This folder contains all backend services, business logic, and configurations.

<Callout type="info" title="Mental Model">

  <h4 className="">
    API Mental Model
  </h4>
  Think of <code>solid-api</code> as the <strong>system-of-record</strong> side of a SolidX application.
  - It owns your domain models and metadata.
    - It exposes the generated and custom API surface.
    - It contains the backend extension points for business logic, security, workflows, and integrations.
  So when you look at the backend folder structure, you should read it as: <strong>metadata + generated structure + custom backend logic</strong>.

</Callout>

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


   <h4>
      

  ###  Notable Subfolders
   </h4>


  - `src/`
    - Contains `main.ts` (entry point for the SolidX backend) and all SolidX modules like:
      - `fees-portal/`
    - `main-cli.ts` -> entry point for the SolidX cli commands.
    - `app.module.ts` ->  Contains the application module configuration.
    - `app-default-database.module.ts` -> Contains all the database configuration.

   <h4>
      

  ###  SolidX dependencies
   </h4>
  - `@solidxai/core`
    - Contains the core SolidX module which provides the core backend services for SolidX.
  - `@solidxai/code-builder`
    - Contains the functionality for generating the code in the SolidX backend.


  <h4>
      

  ###  SolidX modules
   </h4>

  
  - A SolidX module is a logical container that groups together related models and functionality under a unified domain or feature area e.g `fees-portal`.
  - You can find the structure for a SolidX module here [Generated Code](../developer-docs/extending/code-generation/index.md).  
  ---

##  solid-ui/ - Frontend (Vite & React)

The frontend is built as a Vite + React application. The generated app is intentionally thin: it bootstraps routing, theming, and Redux wiring, then layers project-specific UI modules on top of the shared `@solidxai/core-ui` package.

<Callout type="info" title="Mental Model">

  <h4 className="">
    UI Mental Model
  </h4>
  Think of <code>solid-ui</code> as the <strong>application shell and user-experience layer</strong> of your SolidX project.
  - The shared SolidX UI package provides the common runtime, layouts, and extension points.
    - Your project adds module-specific routes, dashboards, widgets, Redux integrations, and custom pages on top of that shell.
    - The frontend is convention-driven: it is intentionally lightweight at the root, and most project-specific behaviour is added through module folders and <code>*.ui-module.ts</code> registration.
  So when you read the frontend structure, the key idea is: <strong>small app shell, project-specific modules layered on top</strong>.

</Callout>

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


   <h4>
      

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





   <h4>
      

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

<Callout type="info" title="Tips">
  <ul>
    <li>All environment variables are stored in  .env  files within each app folder.</li>
  </ul>
</Callout>
