---
title: Roles
---

Roles in SolidX provide a way to group permissions and manage access control at a high level. Each role represents a set of permissions that can be assigned to users.

## Role Management

## Role Types

Below are some typical roles you can find in SOLID:

### System Roles

**Administrator**
- Full system access
- User management

**User**
- Basic system access
- Profile management
- Limited model permission

### Custom Roles

Examples of common custom roles:

**Content Manager**
- Content creation
- Content editing

**Viewer**
- Read-only access
- Report viewing
- Basic dashboards

### Permission Categories

**Model Resource Permissions**
- CRUD operations
- Import/Export

**Administrative Permissions**
- User management
- Role management
- System settings

### Creating a New Role

*Figure 1: Creating a New Role*

![Creating a New Role](/img/admin-docs/iam/roles/role-name.png)

*Figure 2: Assigning Role Permissions*

![Assigning Role Permissions](/img/admin-docs/iam/roles/role-permissions.png)

*Figure 3: Assigning Users to Role*

![Assigning Users to Role](/img/admin-docs/iam/roles/role-users.png)

*Figure 4: Assigning Menu Items to Role*

![Assigning Menu Items to Role](/img/admin-docs/iam/roles/role-menus.png)

*Figure 5: View Roles list*

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
<summary>Role Assignment</summary>

- Assign minimum necessary roles
- Regular access reviews
- Document role assignments

</details>

<details>
<summary>Maintenance</summary>

- Archive unused roles
- Monitor role changes

</details>
