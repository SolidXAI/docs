---
title: Roles
---

# Roles

Roles in SolidX provide a way to group permissions and manage access control at a high level. Each role represents a set of permissions that can be assigned to users.

## Role Management

## Role Types

Below are some typical roles you can find in SOLID:

### System Roles

<div>

  <div>
    Administrator
    <ul>
      <li>Full system access</li>
      <li>User management</li>
    </ul>
  </div>

  <div>
    User
    <ul>
      <li>Basic system access</li>
      <li>Profile management</li>
      <li>Limited model permission</li>
    </ul>
  </div>

</div>

### Custom Roles

Examples of common custom roles:

<div>

  <div>
    Content Manager
    <ul>
      <li>Content creation</li>
      <li>Content editing</li>
    </ul>
  </div>

  <div>
    Viewer
    <ul>
      <li>Read-only access</li>
      <li>Report viewing</li>
      <li>Basic dashboards</li>
    </ul>
  </div>

</div>

### Permission Categories

<div>

  <div>
    Model Resource Permissions
    <ul>
      <li>CRUD operations</li>
      <li>Import/Export</li>
    </ul>
  </div>

  <div>
    Administrative Permissions
    <ul>
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

<details>
  <summary>
    
    Role Assignment
  </summary>
  <ul>
    <li>Assign minimum necessary roles</li>
    <li>Regular access reviews</li>
    <li>Document role assignments</li>
  </ul>
</details>

<details>
  <summary>
    
    Maintenance
  </summary>
  <ul>
    <li>Archive unused roles</li>
    <li>Monitor role changes</li>
  </ul>
</details>
