---
title: IAM
---

SOLID's IAM system provides comprehensive user, role, and permission management to secure your application.

## Overview

The IAM system consists of several key components:

- User management
- Role-based access control (RBAC)
- Permission management
- Record-level security
- Authentication providers

## Components

### Users

Manage user accounts and profiles:
- User creation and invitation
- Profile management
- Account settings
- Access control

→ [Users documentation](./users.md)

### Roles

Define and manage user roles:
- Role creation
- Permission assignment
- Role hierarchy
- Access levels

→ [Roles documentation](./roles.md)

### Permissions

Control access to system features:
- Automatic permission discovery
- Permission grouping
- Custom permissions
- Permission inheritance

→ [Permissions documentation](./permissions.md)

### Record Rules

Configure data-level security:
- Record-level access control
- Dynamic rules
- User-based filters
- Role-based filters

→ [Record Rules documentation](./record-rules.md)

### Authentication Providers

Multiple authentication methods:
- Password-based
- OTP (passwordless)
- OAuth providers: Google, Meta/Facebook, LinkedIn, Twitter/X
- Custom providers

→ [Authentication Providers](/docs/developer-docs/rest-apis/authentication/oauth-authentication/)

## Key Features

**User Management**
- User registration
- Profile management
- Password policies
- Account recovery
- Session management

**Access Control**
- Role-based access
- Permission management
- Record-level security
- API authentication
- Token management

**Authentication**
- Multiple auth methods
- Social login
- Two-factor auth
- Single sign-on
- JWT tokens

**Security Features**
- Password hashing
- Session management
- Token expiration
- Audit logging
- Security policies

## Best Practices

<details>
<summary>User Management</summary>

- Implement strong password policies
- Enable account recovery
- Monitor user activity
- Regular access reviews

</details>

<details>
<summary>Role Design</summary>

- Follow principle of least privilege
- Create role hierarchies
- Document role purposes
- Regular role audits

</details>

<details>
<summary>Permissions</summary>

- Group related permissions
- Regular permission reviews
- Document permission usage
- Monitor permission changes

</details>

<details>
<summary>Security</summary>

- Enable audit logging
- Monitor failed logins
- Regular security reviews
- Incident response plan

</details>
