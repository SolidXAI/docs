---
title: Module Metadata Schema
description: Overview of the module metadata schema used in SolidX.
summary: This document explains the module metadata schema in SolidX, which represents the top-level building blocks for organizing applications. A module groups related models and functionality under a unified domain (like a Fees Portal module). The metadata includes properties such as module name, display name, description, default data source, menu icon, sequence number, and system flag. Examples demonstrate configuring module metadata for applications, and the document references the admin documentation for conceptual understanding of module management and the hierarchical relationship where modules contain models which contain fields.
json_pointer: "/moduleMetadata"
jsonpath: "$.moduleMetadata"
parent_component: root
items_type: object
items_attributes_doc: "#module-metadata-attributes"
solidx_concerns: [create_module]
---

#  Module Metadata

> **Where it lives**  
> **JSON Pointer:** `/moduleMetadata`  
> **JSONPath:** `$.moduleMetadata`  
> **Parent:** Root of the metadata file

##  Overview

When creating a new module in SolidX, you're defining a **core building block** of your application.  
A module groups together related models and functionality under a **unified domain**.

👉 For a conceptual overview of what a module is, see [Module Management Documentation](../../admin-docs/module-builder/module-management.md).

###  Example: Fees Portal Module
Below is a module metadata example for a "Fees Portal" module that tracks fee collection requests.
<details>
  <summary>
    
    Module Schema
  </summary>

```json
{
  "moduleMetadata": {
    "name": "fees-portal",
    "displayName": "Fees Portal",
    "description": "Keep track of fees collections requests",
    "defaultDataSource": "default",
    "menuIconUrl": null,
    "menuSequenceNumber": 2,
    "isSystem": false,
    ... // Model and Field metadata goes here
  },
  ... // Other metadata components go here
}
```
</details>

  The defaultDataSource is set to "default" here, which refers to the default data source configured in your SolidX instance. This is the TypeORM data source configured in your app-default.database.ts in your project `solid-api` src folder.

  ## Module Metadata Attributes

### `name` *(string, required, unique)*
Unique identifier for the module (lowercase, underscores/dashes).  
Used internally by the system and in the API (e.g., `"sales"`).  
**Default:** N/A

### `displayName` *(string, required)*
Human-readable name shown in the admin panel’s navigation and UI  
(e.g., `"Sales Management"`).  
**Default:** N/A

### `description` *(string, optional)*
Short summary of what the module represents or its purpose.  
**Default:** N/A

### `defaultDataSource` *(string, optional)*
Default data source (from a predefined list) used to read/write data.  
**Default:** N/A

### `menuSequenceNumber` *(number, optional)*
Order in which the module appears in the sidebar/navigation menu  
(lower numbers appear earlier).  
**Default:** N/A

### `isSystem` *(boolean, required)*
Marks this as a **system module** (cannot be deleted).  
**Default:** `false`

### `menuIconUrl` *(string, optional)*
Path/URL of an icon to represent the module in the navigation pane.  
**Default:** N/A