---
title: Module Metadata Schema
description: Overview of the module metadata schema used in SolidX.
sidebar_position: 1
---

## Module Metadata

When creating a new module in SolidX, you're defining a **core building block** of your application.  
A module groups together related models and functionality under a **unified domain**.

👉 For a conceptual overview of what a module is, see [Module Management Documentation](../admin-docs/module-builder/module-management.md).

---

### ▶️ Example: Fees Portal Module

<summary>📑 Module Schema</summary>

```json
{
  "moduleMetadata": {
    "name": "fees-portal",
    "displayName": "Fees Portal",
    "description": "Used to keep a track of all fees collections requests",
    "defaultDataSource": "default",
    "menuIconUrl": null,
    "menuSequenceNumber": 2,
    "isSystem": false,
    ... // Model and Field metadata goes here
  },
  ... // Other metadata components go here
}
```


---

## 🔍 Module Metadata Attributes

### `name` *(string, required, unique)*
Unique identifier for the module (lowercase, underscores/dashes).  
Used internally by the system and in the API (e.g., `"sales"`).  
**Default:** N/A

---

### `displayName` *(string, required)*
Human-readable name shown in the admin panel’s navigation and UI  
(e.g., `"Sales Management"`).  
**Default:** N/A

---

### `description` *(string, optional)*
Short summary of what the module represents or its purpose.  
**Default:** N/A

---

### `defaultDataSource` *(string, optional)*
Default data source (from a predefined list) used to read/write data.  
**Default:** N/A

---

### `menuSequenceNumber` *(number, optional)*
Order in which the module appears in the sidebar/navigation menu  
(lower numbers appear earlier).  
**Default:** N/A

---

### `isSystem` *(boolean, required)*
Marks this as a **system module** (cannot be deleted).  
**Default:** `false`

---

### `menuIconUrl` *(string, optional)*
Path/URL of an icon to represent the module in the navigation pane.  
**Default:** N/A