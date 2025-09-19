---
title: Populating Users
description: Metadata schema for defining users in SolidX applications.
sidebar_position: 8
---

## Overview
We can populate some initial users in the system using the `users` metadata. These users will created with the default role that is specified in the environment variable `IAM_DEFAULT_ROLE` or `Public` role if the environment variable is not set.

For a conceptual overview of users, refer to the [Users Management](../../admin-docs/iam/users.md) documentation.

---

### Example: Fee Portal Module Users Metadata
<summary> Users Schema </summary>
``` json
{
  ..., // Other metadata
  "users": [ // Array of user metadata
    {
      "fullName": "John Doe",
      "username": "johndoe",
      "email": "john.doe@example.com",
      "password": "securePassword123",
      "mobile": "919999999999",
    },
    {
      "fullName": "Jane Smith",
      "username": "janesmith",
      "email": "jane.smith@example.com",
      "password": "securePassword456",
      "mobile": "918888888888",
    }  
  ]
}
```

## Users Metadata Attributes
### `fullName` *(string, required)*
Full name of the user.

---
### `username` *(string, required, unique)*
Unique username for the user.

---
### `email` *(string, required, unique)*
Unique email address of the user.

---
### `password` *(string, required)*
Password for the user account. It is recommended to use a strong password.

---
### `mobile` *(string, optional)*
Mobile number of the user.

---