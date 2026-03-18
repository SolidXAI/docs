---
sidebar_position: 3
title: End-to-End Implementation
description: Step-by-step guide to implementing the Fees Portal using SolidX.
summary: TODO
keywords: [TODO]
concerns: TODO
---

## Overview

This guide walks you through building a complete Fees Portal from scratch using SolidX. You'll learn how to configure data models, set up user roles, establish relationships between entities, for every key feature of the platform.

By following this implementation guide, you'll create a multi-tenant system where multiple educational institutes can independently manage their fee collection, each with their own payment gateway integration, custom branding, and administrative staff.

## Log In As Super Admin (Platform Admin)

The default setup of SolidX platform includes a `sa` (super admin) user with full access to all modules. This user acts as the Platform Admin for the Fees Portal.

:::info[Default Super Admin Credentials]
| Field    | Value         |
|----------|---------------|
| Username | `sa`          |
| Password | `Admin@3214$` |

These credentials are created during the seed step. See [Setting Up SolidX → Log In as Super Admin](../solidx_setup#log-in-as-super-admin) for details.
:::

## Creating the Fees Portal Module

Before creating individual data models, you need to first create a module that will contain all your models. A module is a logical grouping of related models and functionality. In this case, the "Fees Portal" module will contain all the models related to fee collection (Institute, Fee Type, Students, Payments, etc.).

### Module Configuration

Navigate to the module creation interface in SolidX and configure the following attributes:

| Attribute | Value | Description |
|-----------|-------|-------------|
| **Display Name** | Fees Portal | The human-readable name shown in menus and UI. Can include spaces and capitalization. |
| **Name** | fees-portal (Readonly) | . The technical identifier for the module. This is automatically generated based on the Display Name and cannot be changed. |
| **Menu Sequence Number** | 2 | Controls the order of this module in the navigation menu. Lower numbers appear first. |
| **Description** | Used to keep a track of all fees collections requests | A brief description explaining what this module does. Helps other developers understand its purpose. |
| **Default Data Source** | default | The database connection to use for this module's models. Use "default" for the primary database. |
| **Menu Icon** | None | Optional. Module Icon to display in the navigation menu. Leave this  empty if not needed. |

### Understanding Module Attributes

**Name vs Display Name:**
- **Display Name**: User-facing label shown everywhere in the UI (e.g., "Fees Portal", "Student Management")
- **Name**: Readonly and generated automatically. Must be unique, lowercase, and URL-friendly (e.g., `fees-portal`, `student-management`)

**Default Data Source:**
- Specifies which database connection all models in this module will use by default
- You can override this at the model level if needed
- Common value is "default" for the main application database

**Menu Sequence Number:**
- Determines where this module appears in the navigation
- Use numbers like 1, 2, 3, 10, 20, 30 to allow easy reordering later
- System modules typically use lower numbers (1-5)
- Custom modules can use higher numbers (6+)

### Module Creation Workflow

1. **Navigate to Module Management**: Access the module creation interface in SolidX admin panel
2. **Enter Module Details**: Fill in all the attributes listed in the table above
3. **Save Module**: The system will create the module structure
4. **Verify Creation**: Confirm the module appears in your module list
5. **Proceed to Model Creation**: Once the module is created, you can start adding models to it

### What Happens After Module Creation

Once you create the module:
- A new entry appears in your primary navigation menu (order set by Menu Sequence Number)
- API endpoints will be generated under `/api/fees-portal/...` whenever you create models
- A dedicated folder structure is created for module-specific code and metadata in the backend codebase

### Important Notes

- **Module Name Cannot Be Changed**: Once created, the module name is permanent. Choose carefully.
- **All Models Must Belong to a Module**: You cannot create standalone models; they must be part of a module.
- **Namespace Isolation**: Each module has its own namespace, preventing naming conflicts with other modules.

## Building the Fees Portal Feature by Feature

The Fees Portal is built incrementally — one feature at a time. Each feature is self-contained: it introduces the data models, roles, and configuration needed to unlock that capability. You don't need to build everything at once; each step leaves you with a working, testable slice of the platform.

Here's the sequence we'll follow:

1. **[Institute Onboarding](./institute_onboarding.md)** — Register an institute, configure fee types, invite admin users, and set up branding for the student portal.
2. **[Activate Institute Portal](./activate_institute.md)** — Provision DNS and web server configuration to make an institute's student portal live and accessible.
3. **[Initiate Payment Collection](./initiate_payment.md)** — Upload a bulk Excel file to generate payment requests for multiple students across multiple fee types in one go.
4. **[Student Payment Portal](./making_payment.md)** — Allow students and parents to view dues, make online payments via Stripe, and track payment history through a dedicated portal.

Let's begin with the foundation — **Institute Onboarding**.