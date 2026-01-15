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

The default setup of SolidX platform includes a `sa` i.e (super admin) user with full access to all modules. This user can act as the Platform Admin for the Fees Portal.

## Creating the Fees Portal Module

Before creating individual data models, you need to first create a module that will contain all your models. A module is a logical grouping of related models and functionality. In this case, the "Fees Portal" module will contain all the models related to fee collection (Institute, Fee Type, Students, Payments, etc.).

### Module Configuration

Navigate to the module creation interface in SolidX and configure the following attributes:

| Attribute | Value | Description |
|-----------|-------|-------------|
| **Name** | fees-portal | The technical identifier for the module. Use lowercase with hyphens. This will be used in URLs, code, and file paths. |
| **Display Name** | Fees Portal | The human-readable name shown in menus and UI. Can include spaces and capitalization. |
| **Description** | Used to keep a track of all fees collections requests | A brief description explaining what this module does. Helps other developers understand its purpose. |
| **Default Data Source** | default | The database connection to use for this module's models. Use "default" for the primary database. |
| **Menu Icon URL** | null | Optional. URL or path to an icon displayed in the navigation menu. Leave empty if not needed. |
| **Menu Sequence Number** | 2 | Controls the order of this module in the navigation menu. Lower numbers appear first. |
| **Is System Module** | ☐ No | Set to "Yes" only for core platform modules. For custom applications like fees portal, keep this as "No". |

### Understanding Module Attributes

**Name vs Display Name:**
- **Name**: Must be unique, lowercase, and URL-friendly (e.g., `fees-portal`, `student-management`)
- **Display Name**: User-facing label shown everywhere in the UI (e.g., "Fees Portal", "Student Management")

**Default Data Source:**
- Specifies which database connection all models in this module will use by default
- You can override this at the model level if needed
- Common value is "default" for the main application database

**Menu Sequence Number:**
- Determines where this module appears in the navigation
- Use numbers like 1, 2, 3, 10, 20, 30 to allow easy reordering later
- System modules typically use lower numbers (1-5)
- Custom modules can use higher numbers (6+)

**Is System Module:**
- System modules are protected and have special privileges
- Only mark as system if this is a core platform module (like user management, authentication)
- Regular business applications should always be marked as "No"

### Module Creation Workflow

1. **Navigate to Module Management**: Access the module creation interface in SolidX admin panel
2. **Enter Module Details**: Fill in all the attributes listed in the table above
3. **Save Module**: The system will create the module structure
4. **Verify Creation**: Confirm the module appears in your module list
5. **Proceed to Model Creation**: Once the module is created, you can start adding models to it

### What Happens After Module Creation

Once you create the module:
- A new entry appears in your navigation menu (if Menu Sequence Number is set)
- The module becomes available as a target when creating new models
- API endpoints will be generated under `/api/fees-portal/...`
- A dedicated folder structure is created for module-specific code and metadata

### Important Notes

- **Module Name Cannot Be Changed**: Once created, the module name is permanent. Choose carefully.
- **Display Name Can Be Updated**: You can change the display name anytime without breaking functionality.
- **All Models Must Belong to a Module**: You cannot create standalone models; they must be part of a module.
- **Namespace Isolation**: Each module has its own namespace, preventing naming conflicts with other modules.

## Building the Fees Portal Feature by Feature

We'll build the Fees Portal incrementally, implementing each feature one at a time. Each feature is self-contained with its own data models, workflows, and user interfaces.

The implementation follows this sequence:

1. **[Institute Onboarding](./institute_onboarding.md)** - Set up institutions, admin users, and fee types
2. **Payment Collections** - Create and manage fee collection requests (Coming soon)
3. **Student Management** - Handle student records and enrollment (Coming soon)
4. **Payment Processing** - Process online payments through integrated gateways (Coming soon)
5. **Reporting & Analytics** - Track collections and generate reports (Coming soon)

Each feature guide includes:
- The roles involved in that feature
- Data models required with detailed field descriptions and relationships
- Building the models in SolidX using the App Builder
- Customizing the user interface with the layout json configurations
- Step-by-step setup sequence for setting up the feature
- Best practices and decision guides

Let's begin with the foundation - **Institute Onboarding**.