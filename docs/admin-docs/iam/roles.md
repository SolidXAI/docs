---
sidebar_position: 2
---

# Roles

Roles in SOLID provide a way to group permissions and manage access control at a high level. Each role represents a set of permissions that can be assigned to users.

## Role Management

## Role Types
Below are some typical roles you can find in SOLID:

### System Roles

  <div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 Administrator</h4>
    <ul className="card-desc">
      <li>Full system access</li>
      <li>User management</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 User</h4>
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
    <h4 className="card-title">1 Content Manager</h4>
    <ul className="card-desc">
      <li>Content creation</li>
      <li>Content editing</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 Viewer</h4>
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
    <h4 className="card-title">1 Model Resource Permissions</h4>
    <ul className="card-desc">
      <li>CRUD operations</li>
      <li>Import/Export</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 Administrative Permissions</h4>
    <ul className="card-desc">
      <li>User management</li>
      <li>Role management</li>
      <li>System settings</li>
    </ul>
  </div>

</div>



## Best Practices


   <div className="feature-grid">


  <div className="feature-card">
    <h4 className="card-title">1 Role Assignment</h4>
    <ul className="card-desc">
      <li>Assign minimum necessary roles</li>
      <li>Regular access reviews</li>
      <li>Document role assignments</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 Maintenance</h4>
    <ul className="card-desc">
      <li>Archive unused roles</li>
      <li>Monitor role changes</li>
    </ul>
  </div>

</div>


### Creating a New Role
![Creating a New Role](/img/admin-docs/iam/roles/role-name.png)
*Figure 1: Creating a New Role*
![Assigning Role Permissions](/img/admin-docs/iam/roles/role-permissions.png)
*Figure 2: Assigning Role Permissions*
![Assigning Users to Role](/img/admin-docs/iam/roles/role-users.png)
*Figure 3: Assigning Users to Role*
![Assigning Menu Items to Role](/img/admin-docs/iam/roles/role-menus.png)
*Figure 4: Assigning Menu Items to Role*
![View Roles list](/img/admin-docs/iam/roles/role-list.png)
*Figure 5: View Roles list*

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

