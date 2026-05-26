---
title: Users
---

# Users

User management in SOLID provides comprehensive tools for managing user accounts, profiles, and access control.

## User Management

### Creating Users

There are several ways to create users:

<div>

  <div>
      Admin Creation:
    <ul>
      <li>Navigate to Users section</li>
      <li>Click "Create User"</li>
      <li>Fill required information</li>
      <li>Assign roles</li>
      <li>Send invitation</li>
    </ul>
  </div>

  <div>
     User Invitation:
    <ul>
      <li>Send email invitation</li>
      <li>User completes registration</li>
      <li>Automatic role assignment</li>
      <li>Email verification</li>
    </ul>
  </div>

  <div>
    Self Registration:
    <ul>
      <li>Enable public registration</li>
      <li>Configure registration fields</li>
      <li>Set default roles</li>
      <li>Enable email verification</li>
    </ul>
  </div>

</div>

### User Properties

| Property  | Description          |
| --------- | -------------------- |
| Full name | User's full name     |
| Username  | Unique identifier    |
| Email     | Primary contact      |
| Password  | Securely hashed      |
| Mobile    | User's mobile number |
| Roles     | Assigned roles       |
## Security Features

<div>
  <div>
    Password Management
    <ul>
      <li>Password complexity rules</li>
      <li>Password expiration</li>
      <li>Password history</li>
      <li>Failed login lockout</li>
      <li>Password reset</li>
    </ul>
  </div>
</div>

## User Interface

<div>
  <div>
    User List View
    <ul>
      <li>Search users</li>
      <li>Filter users</li>
      <li>Export users</li>
    </ul>
  </div>

  <div>
    User Detail View
    <ul>
      <li>Profile information</li>
      <li>Role management</li>
      <li>Activity history</li>
    </ul>
  </div>
</div>

### Creating a New User

![View existing users](/img/admin-docs/iam/users/user-list.png)  
_Figure 1: User list page showing existing users._

![Create a user](/img/admin-docs/iam/users/user-creation.png)  
_Figure 2: User creation form to add a new user._

To create a new user:

1. Navigate to IAM → Users section
2. Click the Add button
3. Fill in the required details in the form
4. Assign the user the required roles
5. Click Save
6. User is added to the list of users
7. User receives a mail with the login link and is prompted to change their password (if `forceChangePassword` is enabled)

  Internal user is a pre-defined technical role with limited permissions. All users need to be assigned this role, for application to work properly on user login.

## Best Practices

<details>
  <summary>
    
    User Creation
  </summary>
  <ul>
    <li>Validate email addresses</li>
    <li>Enforce strong passwords</li>
    <li>Set appropriate roles</li>
    <li>Document user purpose</li>
  </ul>
</details>

<details>
  <summary>
    
    Profile Management
  </summary>
  <ul>
    <li>Collect necessary information</li>
    <li>Respect privacy</li>
    <li>Regular information updates</li>
  </ul>
</details>

<details>
  <summary>
    
    Security
  </summary>
  <ul>
    <li>Regular password changes</li>
    <li>Monitor login attempts</li>
    <li>Review access regularly</li>
  </ul>
</details>

<details>
  <summary>
    
    Maintenance
  </summary>
  <ul>
    <li>Update user information</li>
    <li>Review role assignments</li>
    <li>Clean up permissions</li>
  </ul>
</details>
