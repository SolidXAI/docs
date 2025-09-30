---
title: Users
description: Metadata schema for populating users in SolidX applications.
sidebar_position: 8
json_pointer: "/users"
jsonpath: "$.users"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#users-metadata-attributes"
---

# Users 
> **Where it lives**  
> **JSON Pointer:** `/users`  
> **JSONPath:** `$.users`  
> **Parent:** Root of the metadata file


## Overview
We can populate some initial users in the system using the `users` metadata. These users will be created with the default role that is specified in the environment variable `IAM_DEFAULT_ROLE` or `Public` role if the environment variable is not set.


### Example: Fee Portal Module Users Metadata
Below is an example of how to initialize users using the metadata configuration. The below example creates two users, "John Doe" and "Jane Smith", with their respective details. Since no passwords are provided, the system will auto-generate secure passwords for these users and mail them to the specified email addresses.

<summary> Users Schema </summary>
``` json
{
  ..., // Other metadata
  "users": [ // Array of user metadata
    {
      "fullName": "John Doe",
      "username": "johndoe",
      "email": "john.doe@example.com",
      "mobile": "919999999999",
    },
    {
      "fullName": "Jane Smith",
      "username": "janesmith",
      "email": "jane.smith@example.com",
      "mobile": "918888888888",
    }  
  ]
}
```

## Users Metadata Attributes
### `fullName` *(string, required)*
Full name of the user.


### `username` *(string, required, unique)*
Unique username for the user.

### `email` *(string, required, unique)*
Unique email address of the user.

### `mobile` *(string, optional)*
**Includes** country code (e.g. 919876543210 for India)

Mobile number of the user.

## Further Reference
- [Users Management](../../admin-docs/iam/users.md)
