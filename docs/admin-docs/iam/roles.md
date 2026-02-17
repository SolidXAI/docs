---
sidebar_position: 2
title: Roles
---

import { FaUserShield, FaUser, FaUsersCog, FaEye, FaDatabase, FaTools } from "react-icons/fa";
import { IoIosArrowForward } from "react-icons/io";

# Roles

Roles in SolidX provide a way to group permissions and manage access control at a high level. Each role represents a set of permissions that can be assigned to users.

## Role Management

## Role Types

Below are some typical roles you can find in SOLID:
import { FaUserShield, FaUser, FaUsersCog, FaEye, FaDatabase, FaTools } from "react-icons/fa";

### System Roles

<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaUserShield size={16} style={{ marginRight: "10px" }} />
      Administrator
    </h4>
    <ul className="card-desc">
      <li>Full system access</li>
      <li>User management</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaUser size={15} style={{ marginRight: "10px" }} />
      User
    </h4>
    <ul className="card-desc">
      <li>Basic system access</li>
      <li>Profile management</li>
      <li>Limited model permission</li>
    </ul>
  </div>

</div>

### Custom Roles

Examples of common custom roles:

<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaUsersCog size={18} style={{ marginRight: "10px" }} />
      Content Manager
    </h4>
    <ul className="card-desc">
      <li>Content creation</li>
      <li>Content editing</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaEye size={16} style={{ marginRight: "10px" }} />
      Viewer
    </h4>
    <ul className="card-desc">
      <li>Read-only access</li>
      <li>Report viewing</li>
      <li>Basic dashboards</li>
    </ul>
  </div>

</div>

### Permission Categories

<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaDatabase size={16} style={{ marginRight: "10px" }} />
      Model Resource Permissions
    </h4>
    <ul className="card-desc">
      <li>CRUD operations</li>
      <li>Import/Export</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaTools size={16} style={{ marginRight: "10px" }} />
      Administrative Permissions
    </h4>
    <ul className="card-desc">
      <li>User management</li>
      <li>Role management</li>
      <li>System settings</li>
    </ul>
  </div>

</div>

### Creating a New Role

_Figure 1: Creating a New Role_

![Creating a New Role](/img/admin-docs/iam/roles/role-name.png)

_Figure 2: Assigning Role Permissions_

![Assigning Role Permissions](/img/admin-docs/iam/roles/role-permissions.png)
<br/>

_Figure 3: Assigning Users to Role_

![Assigning Users to Role](/img/admin-docs/iam/roles/role-users.png)

_Figure 4: Assigning Menu Items to Role_

![Assigning Menu Items to Role](/img/admin-docs/iam/roles/role-menus.png)

_Figure 5: View Roles list_

![View Roles list](/img/admin-docs/iam/roles/role-list.png)

#### To create a new role:

1. Navigate to IAM > Roles
2. Click on "Add"
3. Provide details:
   - Name (unique identifier)
   - Permissions (list of permissions to assign)
   - Users (list of users assigned to the role)
   - Menu (list of menu items accessible by the role)
4. Click "Save" to create the role.
5. User can view the new role in the roles list.

## Best Practices

<details open>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Role Assignment
  </summary>
  <ul className="card-desc">
    <li>Assign minimum necessary roles</li>
    <li>Regular access reviews</li>
    <li>Document role assignments</li>
  </ul>
</details>

<details open>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Maintenance
  </summary>
  <ul className="card-desc">
    <li>Archive unused roles</li>
    <li>Monitor role changes</li>
  </ul>
</details>
