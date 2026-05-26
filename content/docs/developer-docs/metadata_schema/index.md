---
title: Metadata Schema
description: Overview of the metadata schema used in SolidX.
summary: This document provides an overview of SolidX's metadata-driven architecture, which enables flexible configuration of both backend and frontend functionality without modifying core code. Metadata can be defined in JSON files or through the admin interface and is automatically synced to the database. Key components include Module, Model, Field, View, Action, Menu Item, Roles & Permissions, Users, Email/SMS Templates, Media Storage Providers, Scheduled Jobs, Security Rules, List of Values, and Dashboard metadata. The document covers seeding processes, best practices for naming conventions, security, performance optimization, user experience, maintainability, and data integrity.
solidx_concerns: [add_field_to_existing_layout, add_field_to_a_model, add/update_security_record_rule]
---

#  Metadata Schema
##  Overview

The metadata schema in `SolidX` is designed to provide a flexible and extensible way to define the structure and behavior of various application components. By using a metadata-driven approach, developers can easily customize and extend the functionality of the `SolidX`platform without modifying the core codebase.

`SolidX` allows configuring both backend and frontend functionality using metadata configuration. 

The metadata can either be defined in JSON files or through the admin interface. When any metadata is created or updated through the admin interface, it is stored in the database as well as in the JSON file for the corresponding module. This allows for easy version control and migration of metadata changes across different environments.

Every module needs to have its own metadata file which is then seeded into the database.

##  Seeding Metadata
To apply metadata changes made in the JSON file directly, you must sync the database with the updated metadata files.
1. **Seed metadata into the database**:

```bash
solid seed
```
This command reads all metadata files and updates the `SolidX` database.

2. (Only for code generation changes) **Refresh the generated code** :

```bash
# If your metadata changes involve code generation run:
solid refresh-model -n <model name>
```
This step ensures the generated code reflects the latest metadata.
Typical cases where this extra step is required:
-  Adding a new module  
-  Adding fields to a model  

<div>
  Tips
  <ul>
    <li> Just running the <span> solid seed </span>command is sufficient for most cases, except the ones mentioned above, since the platform reads the metadata directly from the database at runtime.</li>
  </ul>
</div>

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

<details>
  <summary>
    
    Naming Conventions
  </summary>
  <ul>
    <li>Use kebab-case for internal names (`fees-portal`, `institute-list-view`)</li>
    <li>Use PascalCase for display names (`Fees Portal`, `Institute List View`)</li>
    <li>Use camelCase for field names (`instituteName`, `feeAmount`)</li>
  </ul>
</details>

<details>
  <summary>
    
    Security First
  </summary>
  <ul>
    <li>Always configure roles and security rules</li>
    <li>Use principle of least privilege</li>
    <li>Implement proper data filtering</li>
    <li>Enable audit tracking for sensitive operations</li>
  </ul>
</details>

<details>
  <summary>
    
    Performance Optimization
  </summary>
  <ul>
    <li>Use database indexes for frequently queried fields</li>
    
  </ul>
</details>

<details>
  <summary>
    
    User Experience
  </summary>
  <ul>
    <li>Group related fields logically in forms</li>
    <li>Use appropriate field types for data validation</li>
    <li>Provide helpful field descriptions</li>
    
  </ul>
</details>

<details>
  <summary>
    
    Maintainability
  </summary>
  <ul>
    <li>Use consistent field configurations</li>
    
    <li>Version control metadata changes</li>
    <li>Test security rules thoroughly</li>
  </ul>
</details>

<details>
  <summary>
    
    Data Integrity
  </summary>
  <ul>
    <li>Configure proper field validations</li>
    
    <li>Use appropriate data types</li>
    <li>Ensure unique constraints where necessary</li>
    <li>Choose appropriate user keys for models. User keys should be unique and stable (i.e should not change over time) for a model</li>
    <li>Use appropriate relation cascading rules</li>
  </ul>
</details>

  ##  What’s Coming Up

In the upcoming sections, we’ll walk through practical examples that use the metadata schema and explain each attribute in detail.

These examples are based on the Fees Portal Module (a Fee Collection Module for Educational Institutions).

👉 If you’d like to learn more about the Fees Portal module itself, you can refer to the detailed guide here: [School Fees Portal Tutorial](../../tutorial/school-fees-portal/index.md)