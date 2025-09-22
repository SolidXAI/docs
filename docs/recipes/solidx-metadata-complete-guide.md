# SolidX Metadata Complete Documentation Guide

import { IoIosArrowForward } from "react-icons/io";


## Overview

This comprehensive guide documents the complete SolidX platform metadata structure using real examples from the fees-portal module. SolidX is a low-code platform that uses metadata-driven development to automatically generate backend APIs, frontend UIs, and database schemas.

## Table of Contents

1. [Platform Architecture](#platform-architecture)
2. [Module Metadata Structure](#module-metadata-structure)
3. [Field Types Reference](#field-types-reference)
4. [View Configurations](#view-configurations)
5. [Actions & Navigation](#actions--navigation)
6. [Security & Roles](#security--roles)
7. [Complete Metadata Example](#complete-metadata-example)
8. [Best Practices](#best-practices)

## Platform Architecture

### Core Components Hierarchy

```
SolidX Platform
├── Modules (Applications)
│   ├── Models (Database Tables/Entities)
│   │   ├── Fields (Table Columns/Properties)
│   │   ├── Views (UI Representations)
│   │   └── Actions (Operations)
│   ├── Menus (Navigation)
│   ├── Roles (Permissions)
│   ├── Security Rules (Access Control)
│   └── Media Storage Providers (File Handling)
```

### Key Concepts

- **Modules**: Complete applications (e.g., "Fees Portal", "Library Management")
- **Models**: Database entities with fields and relationships
- **Views**: UI representations (list, form, kanban) with layouts
- **Actions**: Operations triggered by user interactions
- **Security**: Role-based access control with data filtering

## Module Metadata Structure

### Top-Level Module Configuration

```json
{
  "moduleMetadata": {
    "name": "fees-portal",                    // Internal module identifier (kebab-case)
    "displayName": "Fees Portal",             // User-friendly name in UI
    "description": "Used to keep a track of all fees collections requests",
    "defaultDataSource": "default",           // Default database connection
    "menuIconUrl": null,                      // Navigation icon URL
    "menuSequenceNumber": 2,                  // Menu order position
    "isSystem": false,                        // System module flag
    "models": [...],                         // Model definitions
    "views": [...],                          // View configurations
    "actions": [...],                        // Action definitions
    "menus": [...],                          // Navigation menus
    "roles": [...],                          // User roles
    "securityRules": [...],                  // Access control rules
    "mediaStorageProviders": [...]           // File storage configs
  }
}
```

### Module Properties

| Property | Type | Description | Required | Example |
|----------|------|-------------|----------|---------|
| `name` | string | Internal identifier (kebab-case) | Yes | `"fees-portal"` |
| `displayName` | string | UI display name | Yes | `"Fees Portal"` |
| `description` | string | Module purpose description | No | `"Fees collection system"` |
| `defaultDataSource` | string | Database connection reference | Yes | `"default"` |
| `menuIconUrl` | string | Navigation icon URL | No | `"/icons/fees.png"` |
| `menuSequenceNumber` | integer | Menu order (1, 2, 3...) | No | `2` |
| `isSystem` | boolean | System module (read-only) | No | `false` |

## Model Structure

### Model Configuration

```json
{
  "singularName": "institute",                // Singular entity name
  "pluralName": "institutes",                 // Plural for UI/API
  "displayName": "Institute",                 // UI display name
  "description": "Educational institute entity",
  "dataSource": "default",                    // Database connection
  "dataSourceType": "postgres",               // Database type
  "tableName": "fees_portal_institute",       // Physical table name
  "userKeyFieldUserKey": "instituteName",     // Unique identifier field
  "isChild": false,                          // Child model flag
  "enableAuditTracking": true,               // Track changes
  "enableSoftDelete": false,                 // Soft delete records
  "draftPublishWorkflow": false,             // Content workflow
  "internationalisation": false,             // Multi-language support
  "fields": [...]                           // Field definitions
}
```

### Model Properties

| Property | Type | Description | Required | Example |
|----------|------|-------------|----------|---------|
| `singularName` | string | Entity singular name | Yes | `"institute"` |
| `pluralName` | string | Entity plural name | Yes | `"institutes"` |
| `displayName` | string | UI display name | Yes | `"Institute"` |
| `dataSource` | string | Database connection | Yes | `"default"` |
| `dataSourceType` | string | Database type | Yes | `"postgres"` |
| `tableName` | string | Physical table name | No | `"fees_portal_institute"` |
| `userKeyFieldUserKey` | string | Unique identifier field | No | `"instituteName"` |
| `isChild` | boolean | Child relationship flag | No | `false` |
| `enableAuditTracking` | boolean | Change tracking | No | `true` |
| `enableSoftDelete` | boolean | Soft delete support | No | `false` |

## Field Types Reference

### Text Field Types

#### shortText
```json
{
  "name": "instituteName",
  "displayName": "Institute Name",
  "type": "shortText",
  "ormType": "varchar",
  "min": null,
  "max": 256,
  "required": true,
  "unique": true,
  "index": true,
  "isUserKey": true
}
```

#### longText
```json
{
  "name": "description",
  "displayName": "Description",
  "type": "longText",
  "ormType": "text",
  "required": false,
  "max": 5000
}
```

#### richText
```json
{
  "name": "termsAndConditions",
  "displayName": "Terms & Conditions",
  "type": "richText",
  "ormType": "text",
  "required": true
}
```

### Numeric Field Types

#### int
```json
{
  "name": "studentCount",
  "displayName": "Student Count",
  "type": "int",
  "ormType": "integer",
  "min": 0,
  "max": 10000,
  "defaultValue": 0
}
```

#### decimal
```json
{
  "name": "feeAmount",
  "displayName": "Fee Amount",
  "type": "decimal",
  "ormType": "decimal",
  "min": 0,
  "max": 100000,
  "defaultValue": "0.00"
}
```

### Boolean Field Types

#### boolean
```json
{
  "name": "isActive",
  "displayName": "Is Active",
  "type": "boolean",
  "ormType": "boolean",
  "defaultValue": true
}
```

### Date/Time Field Types

#### date
```json
{
  "name": "dueDate",
  "displayName": "Due Date",
  "type": "date",
  "ormType": "date",
  "required": true
}
```

#### datetime
```json
{
  "name": "createdAt",
  "displayName": "Created At",
  "type": "datetime",
  "ormType": "timestamp",
  "required": true,
  "enableAuditTracking": true
}
```

### Selection Field Types

#### selectionStatic
```json
{
  "name": "status",
  "displayName": "Status",
  "type": "selectionStatic",
  "ormType": "varchar",
  "selectionStaticValues": [
    "Pending:Pending",
    "Active:Active",
    "Inactive:Inactive"
  ],
  "defaultValue": "Pending"
}
```

#### selectionDynamic
```json
{
  "name": "studentId",
  "displayName": "Student",
  "type": "selectionDynamic",
  "ormType": "varchar",
  "selectionDynamicProvider": "StudentListProvider",
  "required": true
}
```

### Relation Field Types

#### Many-to-One (Child → Parent)
```json
{
  "name": "institute",
  "displayName": "Institute",
  "type": "relation",
  "relationType": "many-to-one",
  "relationCoModelSingularName": "institute",
  "relationModelModuleName": "fees-portal",
  "required": true
}
```

#### One-to-Many (Parent → Children)
```json
{
  "name": "students",
  "displayName": "Students",
  "type": "relation",
  "relationType": "one-to-many",
  "relationCoModelSingularName": "student",
  "relationModelModuleName": "fees-portal"
}
```

#### Many-to-Many
```json
{
  "name": "categories",
  "displayName": "Categories",
  "type": "relation",
  "relationType": "many-to-many",
  "relationCoModelSingularName": "category",
  "relationJoinTableName": "student_category_junction",
  "isRelationManyToManyOwner": true
}
```

### Media Field Types

#### mediaSingle
```json
{
  "name": "logo",
  "displayName": "Logo",
  "type": "mediaSingle",
  "ormType": "varchar",
  "mediaTypes": ["image"],
  "mediaMaxSizeKb": 5120,
  "mediaStorageProviderUserKey": "default-aws-s3",
  "required": true
}
```

#### mediaMultiple
```json
{
  "name": "documents",
  "displayName": "Documents",
  "type": "mediaMultiple",
  "ormType": "text",
  "mediaTypes": ["image", "document", "pdf"],
  "mediaMaxSizeKb": 10240
}
```

### Computed Field Types

#### computed
```json
{
  "name": "fullName",
  "displayName": "Full Name",
  "type": "computed",
  "ormType": "varchar",
  "computedFieldValueType": "string",
  "computedFieldValueProvider": "ConcatEntityComputedFieldProvider",
  "computedFieldValueProviderCtxt": "{\"fields\": [\"firstName\", \"lastName\"], \"separator\": \" \"}",
  "required": true
}
```

### Specialized Field Types

#### email
```json
{
  "name": "email",
  "displayName": "Email Address",
  "type": "email",
  "ormType": "varchar",
  "required": true,
  "unique": true
}
```

#### password
```json
{
  "name": "password",
  "displayName": "Password",
  "type": "password",
  "ormType": "varchar",
  "encrypt": true,
  "encryptionType": "bcrypt"
}
```

## View Configurations

### List View Configuration

```json
{
  "name": "institute-list-view",
  "displayName": "Institute",
  "type": "list",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "institute",
  "layout": {
    "type": "list",
    "attrs": {
      "pagination": true,
      "pageSizeOptions": [10, 25, 50],
      "enableGlobalSearch": true,
      "create": true,
      "edit": true,
      "delete": true
    },
    "children": [
      {
        "type": "field",
        "attrs": {
          "name": "instituteName",
          "sortable": true,
          "filterable": true,
          "isSearchable": true
        }
      }
    ]
  }
}
```

### Form View Configuration

```json
{
  "name": "institute-form-view",
  "displayName": "Institute",
  "type": "form",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "institute",
  "layout": {
    "type": "form",
    "attrs": {
      "name": "form-1",
      "label": "Institute",
      "className": "grid"
    },
    "children": [
      {
        "type": "sheet",
        "attrs": { "name": "sheet-1" },
        "children": [
          {
            "type": "notebook",
            "attrs": { "name": "notebook-1" },
            "children": [
              {
                "type": "page",
                "attrs": {
                  "name": "page-1",
                  "label": "Basic Information"
                },
                "children": [
                  {
                    "type": "row",
                    "attrs": { "name": "row-1" },
                    "children": [
                      {
                        "type": "column",
                        "attrs": {
                          "name": "column-1",
                          "label": "Institute Details",
                          "className": "col-6"
                        },
                        "children": [
                          {
                            "type": "field",
                            "attrs": { "name": "instituteName" }
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```

## Actions & Navigation

### Solid Actions

```json
{
  "displayName": "Institute List View",
  "name": "institute-list-view",
  "type": "solid",
  "customComponent": "/admin/address-master/institute/all",
  "customIsModal": true,
  "viewUserKey": "institute-list-view",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "institute"
}
```

### Custom Actions

```json
{
  "displayName": "Fees Portal Home",
  "name": "fees-portal-home-action",
  "type": "custom",
  "customComponent": "/admin/core/fees-portal/home",
  "customIsModal": true,
  "moduleUserKey": "fees-portal"
}
```

### Menu Configuration

```json
{
  "displayName": "Institute",
  "name": "institute-menu-item",
  "sequenceNumber": 2,
  "actionUserKey": "institute-list-view",
  "moduleUserKey": "fees-portal",
  "parentMenuItemUserKey": "",
  "roles": ["Institute Admin", "Mswipe Admin"]
}
```

## Security & Roles

### Role Definition

```json
{
  "name": "Institute Admin",
  "displayName": "Institute Administrator",
  "permissions": {
    "models": {
      "create": ["student", "feeType"],
      "read": ["institute", "student", "feeType"],
      "update": ["student", "feeType"],
      "delete": ["student"]
    },
    "actions": [
      "institute-list-view",
      "student-list-view"
    ]
  }
}
```

### Security Rules

```json
{
  "name": "institute-access",
  "description": "Institute admins can only access their institute",
  "roleUserKey": "Institute Admin",
  "modelMetadataUserKey": "institute",
  "securityRuleConfig": {
    "filters": {
      "instituteUsers": {
        "id": { "$eq": "$activeUserId" }
      }
    }
  }
}
```

## Complete Metadata Example

```json
{
  "moduleMetadata": {
    "name": "fees-portal",
    "displayName": "Fees Portal",
    "description": "Complete fees collection management system",
    "defaultDataSource": "default",
    "menuSequenceNumber": 2,
    "isSystem": false,

    "models": [
      {
        "singularName": "institute",
        "pluralName": "institutes",
        "displayName": "Institute",
        "dataSource": "default",
        "dataSourceType": "postgres",
        "tableName": "fees_portal_institute",
        "userKeyFieldUserKey": "instituteName",
        "enableAuditTracking": true,
        "fields": [
          {
            "name": "instituteName",
            "displayName": "Institute Name",
            "type": "shortText",
            "ormType": "varchar",
            "required": true,
            "unique": true,
            "index": true,
            "isUserKey": true
          },
          {
            "name": "logo",
            "displayName": "Logo",
            "type": "mediaSingle",
            "mediaTypes": ["image"],
            "mediaMaxSizeKb": 5120,
            "mediaStorageProviderUserKey": "default-aws-s3",
            "required": true
          },
          {
            "name": "feeTypes",
            "displayName": "Fee Types",
            "type": "relation",
            "relationType": "one-to-many",
            "relationCoModelSingularName": "feeType",
            "relationModelModuleName": "fees-portal"
          }
        ]
      }
    ],

    "views": [
      {
        "name": "institute-list-view",
        "displayName": "Institute",
        "type": "list",
        "moduleUserKey": "fees-portal",
        "modelUserKey": "institute",
        "layout": {
          "type": "list",
          "attrs": {
            "pagination": true,
            "enableGlobalSearch": true,
            "create": true,
            "edit": true,
            "delete": true
          },
          "children": [
            {
              "type": "field",
              "attrs": {
                "name": "instituteName",
                "sortable": true,
                "filterable": true,
                "isSearchable": true
              }
            }
          ]
        }
      }
    ],

    "actions": [
      {
        "displayName": "Institute List View",
        "name": "institute-list-view",
        "type": "solid",
        "customComponent": "/admin/address-master/institute/all",
        "customIsModal": true,
        "viewUserKey": "institute-list-view",
        "moduleUserKey": "fees-portal",
        "modelUserKey": "institute"
      }
    ],

    "menus": [
      {
        "displayName": "Institute",
        "name": "institute-menu-item",
        "sequenceNumber": 2,
        "actionUserKey": "institute-list-view",
        "moduleUserKey": "fees-portal",
        "roles": ["Institute Admin", "Mswipe Admin"]
      }
    ],

    "roles": [
      {
        "name": "Institute Admin",
        "displayName": "Institute Administrator",
        "permissions": {
          "models": {
            "create": ["student", "feeType"],
            "read": ["institute", "student", "feeType"],
            "update": ["student", "feeType"],
            "delete": ["student"]
          }
        }
      }
    ],

    "securityRules": [
      {
        "name": "institute-access",
        "description": "Institute admins can only access their institute",
        "roleUserKey": "Institute Admin",
        "modelMetadataUserKey": "institute",
        "securityRuleConfig": {
          "filters": {
            "instituteUsers": {
              "id": { "$eq": "$activeUserId" }
            }
          }
        }
      }
    ]
  }
}
```

## Best Practices

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Naming Conventions
  </summary>
  <ul className="card-desc">
    <li>Use kebab-case for internal names (<code>fees-portal</code>, <code>institute-list-view</code>)</li>
    <li>Use PascalCase for display names (<code>Fees Portal</code>, <code>Institute List View</code>)</li>
    <li>Use camelCase for field names (<code>instituteName</code>, <code>feeAmount</code>)</li>
  </ul>
</details>

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Security First
  </summary>
  <ul className="card-desc">
    <li>Always configure roles and security rules</li>
    <li>Use principle of least privilege</li>
    <li>Implement proper data filtering</li>
    <li>Enable audit tracking for sensitive operations</li>
  </ul>
</details>

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Performance Optimization
  </summary>
  <ul className="card-desc">
    <li>Use database indexes for frequently queried fields</li>
    <li>Enable pagination for large datasets</li>
    <li>Implement proper caching strategies</li>
    <li>Use lazy loading for related data</li>
  </ul>
</details>

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    User Experience
  </summary>
  <ul className="card-desc">
    <li>Group related fields logically in forms</li>
    <li>Use appropriate field types for data validation</li>
    <li>Provide helpful field descriptions</li>
    <li>Implement responsive layouts</li>
  </ul>
</details>

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Maintainability
  </summary>
  <ul className="card-desc">
    <li>Use consistent field configurations</li>
    <li>Document complex business logic</li>
    <li>Version control metadata changes</li>
    <li>Test security rules thoroughly</li>
  </ul>
</details>

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Data Integrity
  </summary>
  <ul className="card-desc">
    <li>Configure proper field validations</li>
    <li>Set up referential integrity for relations</li>
    <li>Use appropriate data types</li>
    <li>Implement data constraints</li>
  </ul>
</details>

This comprehensive guide provides everything you need to understand and work with SolidX metadata configurations. The examples are based on real implementations from the fees-portal module and demonstrate best practices for building robust, secure, and user-friendly applications with the SolidX platform.
