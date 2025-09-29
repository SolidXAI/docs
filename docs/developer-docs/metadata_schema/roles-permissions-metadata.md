---
# title: Roles & Permissions
description: Metadata schema for defining roles and permissions in SolidX applications.
sidebar_position: 7
json_pointer: "/roles"
jsonpath: "$.roles"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#roles-permissions-metadata-attributes"
---

import { InfoBox } from '@site/src/common/InfoBox';

# Roles & Permissions
> **Where it lives**  
> **JSON Pointer:** `/roles`  
> **JSONPath:** `$.roles`  
> **Parent:** Root of the metadata file

## Overview

Roles in SolidX provide a way to group permissions and manage access control at a high level. Each role represents a set of permissions that can be assigned to users.
Permissions in SOLID are automatically discovered based on controller actions and provide fine-grained control over what users can do within the system.

By Default `Admin` role is created with all permissions.



### Example: Fee Portal Module Roles & Permissions Metadata

<summary> Roles & Permissions Schema </summary>

```json
{
  ..., // Other metadata
  "roles": [ // Array of role metadata
    {
      "name": "Institute Admin",
      "description": "Admin role for managing institute-related operations",
      "permissions": [ // Array of permissions
        "InstituteController.create",
        "InstituteController.insertMany",
        "InstituteController.update",
        "InstituteController.partialUpdate"
        "InstituteController.findOne",
        "InstituteController.findMany",
        "InstituteController.delete",
        "InstituteController.deleteMany",
        "InstituteController.recover",
        "InstituteController.recoverMany",
      ],
    }
  ]
}
```

## Roles & Permissions Metadata Attributes

### `name` _(string, required, unique)_

Name of the role.



### `description` _(string, optional)_

A brief description of the role's purpose.



### `permissions` _(array of strings, optional)_

An array of permission strings associated with the role. Each permission corresponds to a specific action that can be performed within the system, typically in the format `controller.method` (e.g., `InstituteController.update`).



<InfoBox>
Permissions are automatically discovered based on controller methods in the codebase. So for e.g., if you have a controller for managing institutes with methods like create, the permission `InstituteController.create` will be automatically created.
</InfoBox>


