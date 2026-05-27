---
title: Database Seeding
icon: "database"
description: Overview of how the database is initialized with metadata in SolidX.
summary: This document explains the database seeding process in SolidX, which initializes the database with essential metadata and data required for the application to function. The seeding is triggered via the 'solid seed' command and populates permissions, media storage providers, system fields, functional modules metadata, roles (Admin and Internal User), default users, views, actions, menus, email/SMS templates, settings, security rules, list of values, and dashboard configurations. The ModuleMetadataSeederService from the @solidstarters/solid-core package handles all the seeding operations automatically.
---

Seeding is the process of initializing the database with the **essential metadata and data** required for the application to function correctly.

> The result of the seeding step is a **fully functional database** with all necessary metadata populated.

## Running the seed Command

To run the seeding process, execute the following command in the `solid-api` directory:

```bash
solid seed
```

This command triggers the `ModuleMetadataSeederService`, provided by the [`@solidstarters/solid-core`](https://www.npmjs.com/package/@solidstarters/solid-core) package. It is responsible for populating all the necessary metadata into the database.

## What Gets Seeded?

The following metadata is populated during the seeding process:

### Permissions

- Permission names are derived from the controller and controller method names.
- Example: `UserController.findMany`, `MenuItemMetadataController.findMany`

### Media Storage Providers

- Sets up providers used for storing media files.
- Default providers include:
  - `default-filesystem`: For local file storage.

### System Fields Metadata

- All the system models and fields are defined in the solid-core-metadata.json file provided by the `@solidstarters/solid-core` package.
- The above configuration gets seeded as part of this step

### Functional Modules Metadata

- Reads from JSON files to seed metadata per functional module (e.g. fees portal, temple portal).

### Roles

- Creates default roles like:
  - `Admin`: With all permissions.
  - `Internal User`: With the necessary technical permissions. All users created in SolidX are assigned this role.
- Other custom roles are created but require manual permission assignment post-login.

### Users

- Seeds default users as specified in metadata.
- Users are prompted to **change their passwords** on first login.

### Views

- User interface components are created based on metadata.

### Actions

- Links views to functionalities using action definitions.

### Menus

- Sets up navigation menus for the app.

### Email Templates

- Initializes default email templates for notifications.

### SMS Templates

- Populates SMS templates for messaging services.

### Settings

- Seeds default application-level configurations.

### Security Rules

- Establishes access rules for different models and roles.

### List of Values

- Predefined value lists used across the app (e.g., dropdowns).

### Dashboards

- Dashboard configuration providing visual summaries and KPIs

## Summary

The seeding process is **essential for bootstrapping** a SolidX instance with all necessary metadata. Make sure to verify seeded users and assign proper permissions for any additional roles.
