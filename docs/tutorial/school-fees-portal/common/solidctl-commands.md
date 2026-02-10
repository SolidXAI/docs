---
sidebar_position: 5
title: SolidX Control Plane CLI Reference
description: Comprehensive reference for using the SolidX Control Plane CLI (solidctl) to manage your SolidX application.
---

## SolidX Control Plane CLI Reference
The `solidctl` CLI provides commands for scaffolding, maintaining, and operating SolidX projects. Run `npx @solidxai/solidctl --help` to see all available commands.

| Command | Description |
|---|---|
| `create-app` | Scaffold a new SolidX project with backend (NestJS) and frontend (React). |
| `seed` | Bootstrap SolidX metadata, settings, and the system user. |
| `build` | Build the Solid API and frontend, and set up the Solid CLI. |
| `upgrade` | Upgrade Solid API and UI dependencies belonging to the `@solidxai` organization in the `solid-api` and `solid-ui` projects to their latest published versions. |
| `generate` | Generate code from model definitions. If `solid-api` and `solid-ui` are running using `solidx:dev`, the application is hot reloaded with the latest generated code. (**Not Implemented yet**) | 
| `info` | Print information about the current SolidX project. |
| `test-data` | Proxy to Solid test-data utilities. |

:::tip
Run `npx @solidxai/solidctl help <command>` to see detailed options for any command.
:::
