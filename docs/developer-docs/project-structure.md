---
# title: Project Structure
description: Overview of the folder structure for the SolidX Fullstack Application.
summary: This document provides a comprehensive overview of the SolidX project folder structure, organized into backend (solid-api) and frontend (solid-ui) components. The solid-api folder contains NestJS-based backend services with source code, module metadata, logs, and media storage. The solid-ui folder houses the Next.js frontend with PrimeReact components, including app routes, Redux state management, and static assets. The document also covers key dependencies including @solidstarters/solid-core for backend services, solid-code-builder for code generation, and solid-core-ui for frontend components. It includes debugging configurations and upgrade scripts.
sidebar_position: 3
solidx_concerns: []
---

import { FaFolder,FaBoxOpen,FaPuzzlePiece,FaLightbulb } from "react-icons/fa";


#  Project Structure

This project is organized into a backend API (`solid-api`) and frontend UI (`solid-ui`) along with supporting scripts and configurations.

```bash
.
├── .vscode/                  # VS Code settings
├── solid-api/                # Backend API (NestJS)
├── solid-ui/                 # Frontend UI (Next.js)
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
  - `@solidstarters/solid-core`
    - Contains the core SolidX module which provides the core backend services for SolidX.
  - `@solidstarters/solid-code-builder`
    - Contains the functionality for generating the code in the SolidX backend.


  <h4 className="card-title card-headear-wrapper">
      <FaPuzzlePiece size={20} style={{ marginRight: "2px" }} />

  ###  SolidX modules
   </h4>

  
  - A SolidX module is a logical container that groups together related models and functionality under a unified domain or feature area e.g `fees-portal`.
  - You can find the structure for a SolidX module here [Generated Code](../developer-docs/extending/code-generation/index.md).  
  ---

##  solid-ui/ - Frontend (Next.js & Prime React)

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


   <h4 className="card-title card-headear-wrapper">
      <FaFolder size={20} style={{ marginRight: "2px" }} />

  ###  Notable Subfolders
   </h4>

  - `app/`
    - Entry point for routes like `/admin`, `/auth`, etc.
    - layout and providers via `layout.tsx` and `GlobalProvider.tsx`.
  - `public/`
    - Contains static files and theme assets.
  - `redux/`
    - Global state configuration.




<!-- ###  -->
   <h4 className="card-title card-headear-wrapper">
      <FaBoxOpen size={22} style={{ marginRight: "2px" }} />

  ###  SolidX dependencies
   </h4>

- `@solidstarters/solid-core-ui`
  - Contains the core ui components for the SolidX UI.
  
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