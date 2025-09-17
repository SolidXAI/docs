---
title: Model Metadata Schema
description: Overview of the model metadata schema used in SolidX.
sidebar_position: 2
---

## Overview

SolidX Models represent the structure of your data within a module. Each model defines a specific type of data, all attributes / fields that a model is made of & its relationships with other models.

Each model is a semantic, configurable data structure that forms the basis of adding custom business logic.

👉 For a conceptual overview of what a model is, see [Model Management Documentation](../admin-docs/module-builder/model-management.md).

---
Example: Institute Model
<summary>📑 Model Schema</summary>

```json
{
  "moduleMetadata": {
    ..., // Module metadata 
    "models": [
      {
        "singularName": "institute",
        "pluralName": "institutes",
        "displayName": "Institute",
        "description": "The institute name...",
        "dataSource": "default",
        "dataSourceType": "postgres",
        "tableName": "fees_portal_institute",
        "userKeyFieldUserKey": "instituteName",
        "isChild": false,
        "enableAuditTracking": true,
        "enableSoftDelete": false,
        "draftPublishWorkflow": false,
        "internationalisation": false,
      },
      { // Child Model Example
        "singularName": "instituteUser",
        "pluralName": "instituteUsers",
        "displayName": "Institute User",
        "description": "This table allows us to store institute user records",
        "dataSource": "default",
        "dataSourceType": "postgres",
        "tableName": "fees_portal_institute_user",
        "isChild": true,
        "parentModelUserKey": "user",
        "enableAuditTracking": true,
        "enableSoftDelete": false,
        "draftPublishWorkflow": false,
        "internationalisation": false,
      },
      ... // Other models
    ]
  },
  ... // Other metadata
}
``` 

---

## 🔍 Model Metadata Attributes

### `singularName` *(string, required, unique)*
Unique identifier for the model (lowercase, underscores/dashes).  
Used internally by the system and in the API (e.g., `"institute"`).  
**Default:** N/A 

---
### `pluralName` *(string, required, unique)*
Plural form of the model name (lowercase, underscores/dashes).  
Used internally by the system and in the API (e.g., `"institutes"`).  
**Default:** N/A

---
### `displayName` *(string, required)*
Human-readable name shown in the admin panel’s navigation and UI  
(e.g., `"Institute"`).  
**Default:** N/A

---
### `description` *(string, optional)*
Short summary of what the model represents or its purpose.
**Default:** N/A

---
### `dataSource` *(string, required)*
Data source (from a predefined list) used to read/write data. If the application has multiple data sources configured, you can choose which one to use for this model.
**Default:** N/A

---
### `dataSourceType` *(string, required)*
Type of data source, either relational database (e.g., `"postgres"`, `"mysql"`) or NoSQL (e.g., `"mongodb"`). Currently supported types are:
- `"postgres"`
- `"mysql"`

---
### `tableName` *(string, optional, unique)*
Name of the database table/collection where the model's data is stored.  
By default, table names are generated automatically based on the singular name of the model, but you can specify a different name if required.  
**Default:** Auto-generated from `singularName` (e.g., `"feeType"` → `"fee_type"`).

---
### `userKeyFieldUserKey` *(string, optional)* i.e the user key field name
The field in the model that serves as a unique identifier for records, often used for display purposes.  
For example, in an "Institute" model, this could be the `"instituteName"` field.  
**Default:** N/A

---
### `isChild` *(boolean, required)*
Indicates if the model is a child model (i.e., an extension of another model).  
Child models inherit fields and relationships from their parent model.  
**Default:** `false`

---
### `parentModelUserKey` *(string, optional)*
The `singularName` of the parent model if this model is a child model.  
**Default:** N/A

---
### `isSystem` *(boolean, required)*
If set to `true`, the model is considered a system model and is not included in code generation.  
System models typically have manually written code.  
**Default:** `false`

---
### `enableAuditTracking` *(boolean, required)*
If set to `true`, all data mutations (create, update, delete) on this model will be tracked and logged for auditing purposes.  
**Default:** `false`

---
### `enableSoftDelete` *(boolean, required)*
If set to `true`, records in this model will be "soft deleted" (marked as deleted without being permanently removed from the database).  
**Default:** `false`

---
### `draftPublishWorkflow` *(boolean, required)*
If set to `true`, the model will support a draft and publish workflow, allowing records to be saved as drafts before being published. This is useful for content that requires review before going live. For such models, additional fields like `status`, `publishedAt`, and `publishedBy` will be automatically managed. 
**Default:** `false`

---
### `internationalisation` *(boolean, required)*
If set to `true`, the model will support internationalization, allowing records to have translations in multiple languages. This is useful for applications that need to cater to a global audience. 
**Default:** `false`

---

