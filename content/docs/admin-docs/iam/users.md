---
title: Users
---

User management in SOLID provides comprehensive tools for managing user accounts, profiles, and access control.

## User Management

### Creating Users

There are several ways to create users:

**Admin Creation**
- Navigate to Users section
- Click "Create User"
- Fill required information
- Assign roles
- Send invitation

**User Invitation**
- Send email invitation
- User completes registration
- Automatic role assignment
- Email verification

**Self Registration**
- Enable public registration
- Configure registration fields
- Set default roles
- Enable email verification

### User Properties

| Property | Description |
|----------|-------------|
| Full name | User's full name |
| Username | Unique identifier |
| Email | Primary contact |
| Password | Securely hashed |
| Mobile | User's mobile number |
| Roles | Assigned roles |

## Security Features

**Password Management**
- Password complexity rules
- Password expiration
- Password history
- Failed login lockout
- Password reset

## User Interface

**User List View**
- Search users
- Filter users
- Export users

**User Detail View**
- Profile information
- Role management
- Activity history

### Creating a New User

![View existing users](/img/admin-docs/iam/users/user-list.png)
*Figure 1: User list page showing existing users.*

![Create a user](/img/admin-docs/iam/users/user-creation.png)
*Figure 2: User creation form to add a new user.*

To create a new user:

1. Navigate to IAM → Users section
2. Click the Add button
3. Fill in the required details in the form
4. Assign the user the required roles
5. Click Save
6. User is added to the list of users
7. User receives a mail with the login link and is prompted to change their password (if `forceChangePassword` is enabled)

> **Note:** Internal user is a pre-defined technical role with limited permissions. All users need to be assigned this role, for application to work properly on user login.

## Best Practices

<details>
<summary>User Creation</summary>

- Validate email addresses
- Enforce strong passwords
- Set appropriate roles
- Document user purpose

</details>

<details>
<summary>Profile Management</summary>

- Collect necessary information
- Respect privacy
- Regular information updates

</details>

<details>
<summary>Security</summary>

- Regular password changes
- Monitor login attempts
- Review access regularly

</details>

<details>
<summary>Maintenance</summary>

- Update user information
- Review role assignments
- Clean up permissions

</details>
