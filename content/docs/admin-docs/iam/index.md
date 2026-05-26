---
title: IAM
---

# IAM

SOLID's IAM system provides comprehensive user, role, and permission management to secure your application.

## Overview

The IAM system consists of several key components:

- User management
- Role-based access control (RBAC)
- Permission management
- Record-level security
- Authentication providers

## Components

### [Users](./users.md)

<div>
  Manage user accounts and profiles:
   - User creation and invitation
   - Profile management
   - Account settings
   - Access control
</div>

### [Roles](./roles.md)

<div>
  Define and manage user roles:
    - Role creation
    - Permission assignment
    - Role hierarchy
    - Access levels
</div>

### [Permissions](./permissions.md)

<div>
    Control access to system features:
     - Automatic permission discovery
     - Permission grouping
     - Custom permissions
     - Permission inheritance
</div>

### [Record Rules](./record-rules.md)

<div>
    Configure data-level security:
     - Record-level access control
     - Dynamic rules
     - User-based filters
     - Role-based filters
</div>

### [Authentication Providers](/docs/developer-docs/rest-apis/authentication/oauth-authentication/)

<div>
    Multiple authentication methods:
      - Password-based
      - OTP (passwordless)
      - OAuth providers:
        - Google
        - Meta/Facebook
        - LinkedIn
        - Twitter/X
      - Custom providers 
</div>

## Key Features
<div>

  <div>
    User Management
    <ul>
      <li>User registration</li>
      <li>Profile management</li>
      <li>Password policies</li>
      <li>Account recovery</li>
      <li>Session management</li>
    </ul>
  </div>

  <div>
    Access Control
    <ul>
      <li>Role-based access</li>
      <li>Permission management</li>
      <li>Record-level security</li>
      <li>API authentication</li>
      <li>Token management</li>
    </ul>
  </div>

  <div>
    Authentication
    <ul>
      <li>Multiple auth methods</li>
      <li>Social login</li>
      <li>Two-factor auth</li>
      <li>Single sign-on</li>
      <li>JWT tokens</li>
    </ul>
  </div>

  <div>
    Security Features
    <ul>
      <li>Password hashing</li>
      <li>Session management</li>
      <li>Token expiration</li>
      <li>Audit logging</li>
      <li>Security policies</li>
    </ul>
  </div>

</div>

## Best Practices
<details>
  <summary>
    
    User Management
  </summary>
  <ul>
    <li>Implement strong password policies</li>
    <li>Enable account recovery</li>
    <li>Monitor user activity</li>
    <li>Regular access reviews</li>
  </ul>
</details>

<details>
  <summary>
    
    Role Design
  </summary>
  <ul>
    <li>Follow principle of least privilege</li>
    <li>Create role hierarchies</li>
    <li>Document role purposes</li>
    <li>Regular role audits</li>
  </ul>
</details>

<details>
  <summary>
    
    Permissions
  </summary>
  <ul>
    <li>Group related permissions</li>
    <li>Regular permission reviews</li>
    <li>Document permission usage</li>
    <li>Monitor permission changes</li>
  </ul>
</details>

<details>
  <summary>
    
    Security
  </summary>
  <ul>
    <li>Enable audit logging</li>
    <li>Monitor failed logins</li>
    <li>Regular security reviews</li>
    <li>Incident response plan</li>
  </ul>
</details>
