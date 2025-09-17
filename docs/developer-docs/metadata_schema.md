---
title: Metadata Schema
description: Overview of the metadata schema used in SolidX.
sidebar_position: 3.5
---

# Metadata Schema

The metadata configuration in SolidX allows configuring different **models** along with their **fields, relationships, permissions, roles, views**, and more.  
Every module can have its own metadata file which is then seeded into the database.

---

## 📦 Key Components

- Module Metadata  
- Model Metadata  
- Field Metadata  
- View Metadata  
- Action Metadata  
- Menu Item Metadata  
- Permissions  
- Roles  
- Users  
- Email Templates  
- SMS Templates  
- Media Storage Providers  
- Scheduled Jobs  
- Security Rules  
- List of Values  
- Dashboard Metadata  

---

## 🎯 Purpose

This section focuses on **working examples** using the metadata schema and explains each attribute in detail.  

All examples below are within the context of a **Fees Portal Module** (A Fee Collection Module for Educational Institutions).  
👉 For more details about the Fees Portal module, see [School Fees Portal Tutorial](../tutorial/school-fees-portal/index.md).

---

# 🧩 Metadata Components

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

---

✅ Next Steps:  
- Add **Model Metadata** docs here (with examples).  
- Create similar collapsible sections for **Fields, Relations, Computed Fields, Security Rules**, etc.  
- Keep examples concise, and push advanced details into collapsible blocks.  
