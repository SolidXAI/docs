---
title: Metadata Schema
description: Overview of the metadata schema used in SolidX.
summary: This document provides an overview of SolidX's metadata-driven architecture, which enables flexible configuration of both backend and frontend functionality without modifying core code. Metadata can be defined in JSON files or through the admin interface and is automatically synced to the database. Key components include Module, Model, Field, View, Action, Menu Item, Roles & Permissions, Users, Email/SMS Templates, Media Storage Providers, Scheduled Jobs, Security Rules, List of Values, and Dashboard metadata. The document covers seeding processes, best practices for naming conventions, security, performance optimization, user experience, maintainability, and data integrity.
solidx_concerns: [add_field_to_existing_layout, add_field_to_a_model, add/update_security_record_rule]
---

## Overview

The metadata schema in `SolidX` is designed to provide a flexible and extensible way to define the structure and behavior of various application components. By using a metadata-driven approach, developers can easily customize and extend the functionality of the `SolidX`platform without modifying the core codebase.

`SolidX` allows configuring both backend and frontend functionality using metadata configuration.

The metadata can either be defined in JSON files or through the admin interface. When any metadata is created or updated through the admin interface, it is stored in the database as well as in the JSON file for the corresponding module. This allows for easy version control and migration of metadata changes across different environments.

Every module needs to have its own metadata file which is then seeded into the database.

## Seeding Metadata

To apply metadata changes made in the JSON file directly, you must sync the database with the updated metadata files.

1. **Seed metadata into the database**:

```bash
solid seed
```

This command reads all metadata files and updates the `SolidX` database.

2. (Only for code generation changes) **Refresh the generated code**:

```bash
solid refresh-model -n <model name>
```

This step ensures the generated code reflects the latest metadata. Typical cases where this extra step is required:
- Adding a new module
- Adding fields to a model

> **Tip:** Just running the `solid seed` command is sufficient for most cases, except the ones mentioned above, since the platform reads the metadata directly from the database at runtime.

## Key Components

Below are the key components of the metadata schema. All the functionality concerning the below components is driven by the metadata schema.

- Module Metadata
- Model Metadata
- Field Metadata
- View Metadata
- Action Metadata
- Menu Item Metadata
- Roles & Permissions
- Users
- Email Templates
- SMS Templates
- Media Storage Providers
- Scheduled Jobs
- Security Rules
- List of Values
- Dashboard Metadata

## Best Practices

<details>
<summary>Naming Conventions</summary>

- Use kebab-case for internal names (`fees-portal`, `institute-list-view`)
- Use PascalCase for display names (`Fees Portal`, `Institute List View`)
- Use camelCase for field names (`instituteName`, `feeAmount`)

</details>

<details>
<summary>Security First</summary>

- Always configure roles and security rules
- Use principle of least privilege
- Implement proper data filtering
- Enable audit tracking for sensitive operations

</details>

<details>
<summary>Performance Optimization</summary>

- Use database indexes for frequently queried fields

</details>

<details>
<summary>User Experience</summary>

- Group related fields logically in forms
- Use appropriate field types for data validation
- Provide helpful field descriptions

</details>

<details>
<summary>Maintainability</summary>

- Use consistent field configurations
- Version control metadata changes
- Test security rules thoroughly

</details>

<details>
<summary>Data Integrity</summary>

- Configure proper field validations
- Use appropriate data types
- Ensure unique constraints where necessary
- Choose appropriate user keys for models. User keys should be unique and stable (i.e should not change over time) for a model
- Use appropriate relation cascading rules

</details>

## What's Coming Up

In the upcoming sections, we'll walk through practical examples that use the metadata schema and explain each attribute in detail.

These examples are based on the Fees Portal Module (a Fee Collection Module for Educational Institutions).

If you'd like to learn more about the Fees Portal module itself, you can refer to the detailed guide here: [School Fees Portal Tutorial](../../tutorial/school-fees-portal/index.md)
