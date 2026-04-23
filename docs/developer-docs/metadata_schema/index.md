---
title: Metadata Schema
description: Overview of the metadata schema used in SolidX.
summary: This document provides an overview of SolidX's metadata-driven architecture, which enables flexible configuration of both backend and frontend functionality without modifying core code. Metadata can be defined in JSON files or through the admin interface and is synced into the database through seeding. Key components include Module, Model, Field, View, Action, Menu Item, Roles & Permissions, Users, Email/SMS Templates, Media Storage Providers, Scheduled Jobs, Security Rules, List of Values, and Dashboard metadata. The document also explains how to think about seeding as the platform bootstrap step for a working SolidX environment.
sidebar_position: 3.5
solidx_concerns: [add_field_to_existing_layout, add_field_to_a_model, add/update_security_record_rule]
---

import { MdUpcoming } from "react-icons/md";
import {FaLightbulb } from "react-icons/fa";
import { IoIosArrowForward } from "react-icons/io";



#  Metadata Schema
##  Overview

<div className="tips-box information-box">
  <h4 className="card-headear-wrapper">
    Mental Model
  </h4>
  <p>
    In SolidX, metadata is not just configuration sitting on the side. It is the <strong>declarative layer that tells the platform what application to become</strong>.
  </p>
  <ul>
    <li>Models and fields define data structure.</li>
    <li>Views, actions, and menus define application behaviour and navigation.</li>
    <li>Roles, permissions, rules, templates, and settings define platform policy and runtime behaviour.</li>
  </ul>
  <p>
    So the intuition is: when you edit metadata, you are not merely tweaking settings. You are shaping the behaviour of the full stack platform.
  </p>
</div>

The metadata schema in `SolidX` is designed to provide a flexible and extensible way to define the structure and behavior of various application components. By using a metadata-driven approach, developers can easily customize and extend the functionality of the `SolidX`platform without modifying the core codebase.

`SolidX` allows configuring both backend and frontend functionality using metadata configuration. 

The metadata can either be defined in JSON files or through the admin interface. When any metadata is created or updated through the admin interface, it is stored in the database as well as in the JSON file for the corresponding module. This allows for easy version control and migration of metadata changes across different environments.

Every module needs to have its own metadata file which is then seeded into the database.

##  Seeding Metadata
Seeding is the process that initializes the database with the metadata and platform records required for SolidX to function correctly.

> The result of the seeding step is a working SolidX environment, not just a populated database.

<div className="tips-box information-box">
  <h4 className="card-headear-wrapper">
    Seeding Mental Model
  </h4>
  <p>
    In SolidX, metadata in JSON is only part of the story. The platform becomes usable when that metadata is seeded into the database so the runtime can discover modules, views, roles, menus, templates, and other platform records.
  </p>
  <ul>
    <li>A plain database is only persistence.</li>
    <li>A seeded database is a functioning SolidX environment.</li>
    <li>That is why seeding is a bootstrap step, not just sample-data insertion.</li>
  </ul>
  <p>
    So the intuition is: <strong>seeding is how declarative metadata becomes active platform state</strong>.
  </p>
</div>

### Why Seeding Matters
Seeding gives you a few immediate benefits:

- **Bootstraps the platform:** a new database becomes a usable SolidX instance rather than an empty persistence layer.
- **Keeps environments consistent:** local, test, and deployed environments can all be brought to the same metadata baseline.
- **Activates metadata changes:** when metadata changes in JSON or in the platform workflow, seeding is how those changes become active in the database.
- **Reduces manual setup:** key platform configuration does not need to be recreated by hand in every environment.

To apply metadata changes made in the JSON file directly, you must sync the database with the updated metadata files.
1. **Seed metadata into the database**:

```bash
npx @solidxai/solidctl@latest seed
```
This command reads all metadata files and updates the `SolidX` database.

By default, this triggers the `ModuleMetadataSeederService`, provided by the [`@solidxai/core`](https://www.npmjs.com/package/@solidxai/core) package.
It is responsible for populating the platform metadata needed by SolidX.

2. (Only for code generation changes) **Refresh the generated code** :

```bash
# If your metadata changes involve code generation, prefer regenerating the module:
npx @solidxai/solidctl@latest generate module

# If you want a smaller, targeted refresh, generate a single model:
npx @solidxai/solidctl@latest generate model
```
This step ensures the generated code reflects the latest metadata.
Typical cases where this extra step is required:
-  Adding a new module  
-  Adding fields to a model  

<div className="tips-box">
  <h4 className="card-headear-wrapper">
    <FaLightbulb className="feature-icon" />
    Tips 
  </h4>
  <ul>
    <li> Just running the <span className="color-green">npx @solidxai/solidctl@latest seed</span> command is sufficient for most cases, except the ones mentioned above, since the platform reads the metadata directly from the database at runtime.</li>
  </ul>
</div>

### What Gets Seeded
Seeding does not only load modules and models. It also initializes several platform concerns that SolidX expects to exist at runtime.

- **Permissions:** permission names are derived from controller and controller method names, for example `UserController.findMany`.
- **Media storage providers:** storage backends such as `default-filesystem` are initialized.
- **System fields metadata:** core system models and fields from the platform metadata are seeded.
- **Functional module metadata:** module JSON files are read and stored in the database.
- **Roles:** default roles such as `Admin` and `Internal User` are created, alongside any custom roles defined in metadata.
- **Users:** default users defined in metadata are seeded.
- **Views:** generated UI definitions are created from metadata.
- **Actions:** view-level actions are linked into the generated experience.
- **Menus:** navigation structure is initialized.
- **Email templates:** default email notification templates are seeded.
- **SMS templates:** SMS notification templates are seeded.
- **Settings:** application-level configuration records are initialized.
- **Security rules:** record-level access policies are seeded.
- **List of values:** reusable enumerations and dropdown value sets are seeded.
- **Dashboards:** dashboard configuration and summaries are initialized.

### Operational Notes
- If you change metadata only, `seed` is usually enough.
- If your metadata change affects generated backend code, run `generate module` or `generate model` after seeding.
- After seeding, verify seeded users and review permissions for any custom roles so the environment behaves as expected.


##  Key Components

Below are the key components of the metadata schema. All the functionality concerning the below components is driven by the metadata schema.

-  Module Metadata  
-  Model Metadata  
-  Field Metadata  
-  View Metadata  
-  Action Metadata  
-  Menu Item Metadata  
-  Roles & Permissions  
-  Users  
-  Email Templates  
-  SMS Templates  
-  Media Storage Providers  
-  Scheduled Jobs  
-  Security Rules  
-  List of Values  
-  Dashboard Metadata  

##  Best Practices

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Naming Conventions
  </summary>
  <ul className="card-desc">
    <li>Use kebab-case for internal names (<code>fees-portal</code>, <code>institute-list-view</code>)</li>
    <li>Use PascalCase for display names (<code>Fees Portal</code>, <code>Institute List View</code>)</li>
    <li>Use camelCase for field names (<code>instituteName</code>, <code>feeAmount</code>)</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Security First
  </summary>
  <ul className="card-desc">
    <li>Always configure roles and security rules</li>
    <li>Use principle of least privilege</li>
    <li>Implement proper data filtering</li>
    <li>Enable audit tracking for sensitive operations</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Performance Optimization
  </summary>
  <ul className="card-desc">
    <li>Use database indexes for frequently queried fields</li>
    <!-- <li>Enable pagination for large datasets</li>
    <li>Implement proper caching strategies</li>
    <li>Use lazy loading for related data</li> -->
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    User Experience
  </summary>
  <ul className="card-desc">
    <li>Group related fields logically in forms</li>
    <li>Use appropriate field types for data validation</li>
    <li>Provide helpful field descriptions</li>
    <!-- <li>Implement responsive layouts</li> -->
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Maintainability
  </summary>
  <ul className="card-desc">
    <li>Use consistent field configurations</li>
    <!-- <li>Document complex business logic</li> -->
    <li>Version control metadata changes</li>
    <li>Test security rules thoroughly</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Data Integrity
  </summary>
  <ul className="card-desc">
    <li>Configure proper field validations</li>
    <!-- <li>Set up referential integrity for relations</li> -->
    <li>Use appropriate data types</li>
    <li>Ensure unique constraints where necessary</li>
    <li>Choose appropriate user keys for models. User keys should be unique and stable (i.e should not change over time) for a model</li>
    <li>Use appropriate relation cascading rules</li>
  </ul>
</details>

  <h2 className=" card-headear-wrapper">
  <MdUpcoming size={28} style={{ marginRight: "12px" }} />

##  What’s Coming Up
</h2>

In the upcoming sections, we’ll walk through practical examples that use the metadata schema and explain each attribute in detail.

These examples are based on the Fees Portal Module (a Fee Collection Module for Educational Institutions).

👉 If you’d like to learn more about the Fees Portal module itself, you can refer to the detailed guide here: [School Fees Portal Tutorial](../../tutorial/school-fees-portal/index.md)
