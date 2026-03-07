---
sidebar_position: 1
title: Users
---

import { NoteBoxs } from '@site/src/common/NoteBoxs';
import { FaUserShield, FaEnvelopeOpenText, FaUserPlus,FaKey, FaListAlt, FaIdBadge } from "react-icons/fa";
import { IoIosArrowForward } from "react-icons/io";

# Users

User management in SOLID provides comprehensive tools for managing user accounts, profiles, and access control.

## User Management

### Creating Users

There are several ways to create users:

<div className="feature-grid">

  <div className="feature-card">
      <h4 className="card-title card-headear-wrapper">
      <FaUserShield size={15} style={{ marginRight: "10px" }} />
      Admin Creation:
    </h4>
    <ul className="card-desc">
      <li>Navigate to Users section</li>
      <li>Click "Create User"</li>
      <li>Fill required information</li>
      <li>Assign roles</li>
      <li>Send invitation</li>
    </ul>
  </div>

  <div className="feature-card">
     <h4 className="card-title card-headear-wrapper">
      <FaEnvelopeOpenText size={15} style={{ marginRight: "10px" }} />
      User Invitation:
    </h4>
    <ul className="card-desc">
      <li>Send email invitation</li>
      <li>User completes registration</li>
      <li>Automatic role assignment</li>
      <li>Email verification</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaUserPlus size={15} style={{ marginRight: "10px" }} />
      Self Registration:
    </h4>
    <ul className="card-desc">
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

<div className="feature-grid">
  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaKey size={16} style={{ marginRight: "10px" }} />
      Password Management
    </h4>
    <ul className="card-desc">
      <li>Password complexity rules</li>
      <li>Password expiration</li>
      <li>Password history</li>
      <li>Failed login lockout</li>
      <li>Password reset</li>
    </ul>
  </div>
</div>

## User Interface

<div className="feature-grid">
  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaListAlt size={16} style={{ marginRight: "10px" }} />
      User List View
    </h4>
    <ul className="card-desc">
      <li>Search users</li>
      <li>Filter users</li>
      <li>Export users</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaIdBadge size={16} style={{ marginRight: "10px" }} />
      User Detail View
    </h4>
    <ul className="card-desc">
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

<NoteBoxs>
  Internal user is a pre-defined technical role with limited permissions. All users need to be assigned this role, for application to work properly on user login.
</NoteBoxs>

## Best Practices

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    User Creation
  </summary>
  <ul className="card-desc">
    <li>Validate email addresses</li>
    <li>Enforce strong passwords</li>
    <li>Set appropriate roles</li>
    <li>Document user purpose</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Profile Management
  </summary>
  <ul className="card-desc">
    <li>Collect necessary information</li>
    <li>Respect privacy</li>
    <li>Regular information updates</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Security
  </summary>
  <ul className="card-desc">
    <li>Regular password changes</li>
    <li>Monitor login attempts</li>
    <li>Review access regularly</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Maintenance
  </summary>
  <ul className="card-desc">
    <li>Update user information</li>
    <li>Review role assignments</li>
    <li>Clean up permissions</li>
  </ul>
</details>
