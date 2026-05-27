---
title: Model Metadata Schema
description: Overview of the model metadata schema used in SolidX.
summary: This document details the model metadata schema in SolidX, where models represent data structures (entities/tables) within modules. Each model is a semantic, configurable structure that defines specific data types, their attributes, and relationships with other models. Key properties include singular/plural names, display name, data source configuration, table name, soft delete settings, audit logging, internationalization support, exportability, and user key field designation. The metadata also specifies which fields serve as unique identifiers for records and controls various behavioral aspects like draft-publish workflows.
json_pointer: "/moduleMetadata/models"
jsonpath: "$.moduleMetadata.models"
parent_component: moduleMetadata
type: array,
items_type: "object"
items_attributes_doc: "#model-metadata-attributes"
solidx_concerns: [create_model_with_fields, add_field_to_a_model, remove_field_from_a_model]
---

> **Where it lives**  
> **JSON Pointer:** `/moduleMetadata/models`  
> **JSONPath:** `$.moduleMetadata.models`  
> **Parent:** `moduleMetadata` in the root of the metadata file

## Overview

SolidX Models represent the structure of your data within a module. Each model defines a specific type of data, all attributes / fields that a model is made of & its relationships with other models.

Each model is a semantic, configurable data structure that forms the basis of adding custom business logic.

👉 For a conceptual overview of what a model is, see [Model Management Documentation](/docs/admin-docs/module-builder/model-management).

### Example: Institute Model
<details>
  <summary>Model Schema</summary>

```json
{
  "moduleMetadata": {
    ..., // Module metadata 
    "models": [
      {
        "singularName": "institute",
        "pluralName": "institutes",
        "displayName": "Institute",
        "description": "Institute records",
        "dataSource": "default",
        "dataSourceType": "postgres",
        "tableName": "fees_portal_institute",
        "userKeyFieldUserKey": "instituteName",
        "isChild": false,
        "enableAuditTracking": true,
        "enableSoftDelete": false,
        "draftPublishWorkflow": false,
        "internationalisation": false,
        "isLegacyTable":false,
        "isLegacyTableWithId":false
      },
      { // Child Model Example
        "singularName": "instituteUser",
        "pluralName": "instituteUsers",
        "displayName": "Institute User",
        "description": "Institute User records",
        "dataSource": "default",
        "dataSourceType": "postgres",
        "tableName": "fees_portal_institute_user",
        "isChild": true,
        "parentModelUserKey": "user",
        "enableAuditTracking": true,
        "enableSoftDelete": false,
        "draftPublishWorkflow": false,
        "internationalisation": false,
        "isLegacyTable":false,
        "isLegacyTableWithId":false

      },
      ... // Other models
    ]
  },
  ... // Other metadata
}
``` 
</details>

  ##  Model Metadata Attributes

### `singularName` *(string, required, unique)*
Unique identifier for the model (lowercase, underscores/dashes).  
Used internally by the system and in the API (e.g., `"institute"`).  
**Default:** N/A 

### `pluralName` *(string, required, unique)*
Plural form of the model name (lowercase, underscores/dashes).  
Used internally by the system and in the API (e.g., `"institutes"`).  
**Default:** N/A

### `displayName` *(string, required)*
Human-readable name shown in the admin panel’s navigation and UI  
(e.g., `"Institute"`).  
**Default:** N/A

### `description` *(string, optional)*
Short summary of what the model represents or its purpose.
**Default:** N/A

### `dataSource` *(string, required)*
Data source (from a predefined list) used to read/write data. If the application has multiple data sources configured, you can choose which one to use for this model.
**Default:** N/A

### `dataSourceType` *(string, required)*
Type of data source, either relational database (e.g., `"postgres"`, `"mysql"`) or NoSQL (e.g., `"mongodb"`). Currently supported types are:
- `"postgres"`
- `"mysql"`

### `tableName` *(string, optional, unique)*
Name of the database table/collection where the model's data is stored.  
By default, table names are generated automatically based on the singular name of the model, but you can specify a different name if required.  
**Default:** Auto-generated from `singularName` (e.g., `"feeType"` → `"fee_type"`).

### `userKeyFieldUserKey` *(string, optional)* i.e the user key field name
The field in the model that serves as a unique identifier for records, often used for display purposes.  
For example, in an "Institute" model, this could be the `"instituteName"` field.
Users keys are used in the UI to reference a model record. Examples include:
 - While displaying relation records in a dropdown, the model's user key field is shown as the label for each option e.g `"Institute A"`.
 - While displaying relation records in a list view, the model's user key field is shown as the label by default.
 - In the details view of a record, the model's user key field is shown in the breadcrumb navigation.

**Default:** N/A

> **Info**
> User keys should be unique and stable (i.e., should not change over time) for a model. If a model is used in relations, it is mandatory to have a unique user key field defined for it for the functionality to work correctly.

### `isChild` *(boolean, required)*
Indicates if the model is a child model (i.e., an extension of another model).  
Child models inherit fields and relationships from their parent model.  
**Default:** `false`

### `parentModelUserKey` *(string, optional)*
The `singularName` of the parent model if this model is a child model.  
**Default:** N/A

### `isSystem` *(boolean, required)*
If set to `true`, the model is considered a system model and is not included in code generation.  
System models typically have manually written code.  
**Default:** `false`

### `enableAuditTracking` *(boolean, required)*
If set to `true`, all data mutations (create, update, delete) on this model will be tracked and logged for auditing purposes.  
**Default:** `false`

### `enableSoftDelete` *(boolean, required)*
If set to `true`, records in this model will be "soft deleted" (marked as deleted without being permanently removed from the database).  
**Default:** `false`

### `draftPublishWorkflow` *(boolean, required)*
If set to `true`, the model will support a draft and publish workflow, allowing records to be saved as drafts before being published. This is useful for content that requires review before going live. For such models, additional fields like `status`, `publishedAt`, and `publishedBy` will be automatically managed.  
**Default:** `false`

### `internationalisation` *(boolean, required)*
If set to `true`, the model will support internationalization, allowing records to have translations in multiple languages. This is useful for applications that need to cater to a global audience.  
**Default:** `false`

### `isLegacyTable` *(boolean, optional)*
Indicates whether the table uses the legacy internationalization pattern and contains an IDENTITY (auto-increment) primary key.Set this to true only when the SQL DDL in the prompt defines a table with an IDENTITY column.When this is true, isLegacyTableWithId must be false. 
**Default:** `false`

### `isLegacyTableWithId` *(boolean, optional)*
Indicates whether the table uses the legacy internationalization pattern but does not contain any IDENTITY (auto-increment) column.Set this to true only when the SQL DDL in the prompt defines a table without an IDENTITY column.When this is true, isLegacyTable must be false. 
**Default:** `false`

<div>
  

##  Related Recipes (TODO)

</div>

👉 [Model Type Recipes](../../admin-docs/module-builder/model-management#related-recipes)  
**Default:** `false`
