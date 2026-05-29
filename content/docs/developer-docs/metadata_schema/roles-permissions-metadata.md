---
title: Roles & Permissions
icon: "shield"
description: Metadata schema for defining roles and permissions in SolidX applications.
summary: This document explains roles and permissions metadata in SolidX, which provides role-based access control at a high level. Roles group permissions and can be assigned to users, while permissions are automatically discovered based on controller actions for fine-grained control. Each role has a name and description, with permissions specified as an array of controller method names (e.g., "InstituteController.create", "InstituteController.findMany"). The system includes a default Admin role with all permissions. Examples demonstrate creating custom roles like Institute Admin with specific permission sets for managing institute-related operations.
json_pointer: "/roles"
jsonpath: "$.roles"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#roles-permissions-metadata-attributes"
solidx_concerns: [add_new_role_with_permission, modify_role]
---


# Roles & Permissions
> **Where it lives**  
> **JSON Pointer:** `/roles`  
> **JSONPath:** `$.roles`  
> **Parent:** Root of the metadata file

## Overview

Roles in SolidX provide a way to group permissions and manage access control at a high level. Each role represents a set of permissions that can be assigned to users.
Permissions in SOLID are automatically discovered based on controller actions and provide fine-grained control over what users can do within the system.

By Default `Admin` role is created with all permissions.

<Callout type="info" title="Mental Model">

  Roles and permissions in SolidX work as a two-layer access model. Permissions represent the fine-grained actions the platform knows about, while roles are the business-facing bundles you assign to users.
  - Think of permissions as capabilities discovered from the backend.
    - Think of roles as the practical packaging of those capabilities for real users.
    - Use roles to express job function, not just technical access flags.
  So the intuition is: <strong>permissions describe what the system can do, and roles describe who should be allowed to do it</strong>.

</Callout>



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


<h2 className=" ">
    

## Roles & Permissions Metadata Attributes
</h2>


### `name` _(string, required, unique)_

Name of the role.



### `description` _(string, optional)_

A brief description of the role's purpose.



### `permissions` _(array of strings, optional)_

An array of permission strings associated with the role. Each permission corresponds to a specific action that can be performed within the system, typically in the format `controller.method` (e.g., `InstituteController.update`).




Permissions are automatically discovered based on controller methods in the codebase. So for e.g., if you have a controller for managing institutes with methods like create, the permission `InstituteController.create` will be automatically created.


