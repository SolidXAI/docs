---
sidebar_position: 2
---

# Roles

Roles in SOLID provide a way to group permissions and manage access control at a high level. Each role represents a set of permissions that can be assigned to users.

## Role Management

### Creating Roles

1. Navigate to IAM > Roles
2. Click "Create Role"
3. Configure role settings:
   - Name
   - Description
   - Base role (optional)
   - Permissions

### Role Properties

| Property | Description |
|----------|-------------|
| Name | Unique identifier for the role |
| Description | Purpose and scope of the role |
| Base Role | Inherit permissions from another role |
| Permissions | List of assigned permissions |
| Status | Active/Inactive state |

## Role Types

### System Roles
<!-- 
1. **Administrator**
   - Full system access
   - User management
   - System configuration
   - Security settings

2. **User**
   - Basic system access
   - Profile management
   - Limited resource access -->


   <div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 Administrator</h4>
    <ul className="card-desc">
      <li>Full system access</li>
      <li>User management</li>
      <li>System configuration</li>
      <li>Security settings</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 User</h4>
    <ul className="card-desc">
      <li>Basic system access</li>
      <li>Profile management</li>
      <li>Limited resource access</li>
    </ul>
  </div>

</div>


### Custom Roles

Examples of common custom roles:

<!-- 1. **Content Manager**
   - Content creation
   - Content editing
   - Media management
   - Publishing control

2. **Viewer**
   - Read-only access
   - Report viewing
   - Basic dashboards -->


<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 Content Manager</h4>
    <ul className="card-desc">
      <li>Content creation</li>
      <li>Content editing</li>
      <li>Media management</li>
      <li>Publishing control</li>
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



## Role Hierarchy

### Inheritance Structure

```
Administrator
├── Manager
│   ├── Team Lead
│   │   └── Team Member
│   └── Content Manager
└── Viewer
```

### Inheritance Rules
- Child roles inherit parent permissions
- Additional permissions can be added
- Inherited permissions cannot be removed
- Multiple inheritance is supported

## Permission Assignment

### Managing Permissions

1. Select role to modify
2. Navigate to Permissions tab
3. Choose permissions:
```json
{
  "role": "content_manager",
  "permissions": {
    "content": [
      "create",
      "read",
      "update",
      "delete"
    ],
    "media": [
      "upload",
      "download",
      "manage"
    ]
  }
}
```

### Permission Categories
<!-- 
1. **Resource Permissions**
   - CRUD operations
   - Import/Export
   - Special actions

2. **Feature Permissions**
   - Module access
   - Feature usage
   - Tool access

3. **Administrative Permissions**
   - User management
   - Role management
   - System settings -->


<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 Resource Permissions</h4>
    <ul className="card-desc">
      <li>CRUD operations</li>
      <li>Import/Export</li>
      <li>Special actions</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 Feature Permissions</h4>
    <ul className="card-desc">
      <li>Module access</li>
      <li>Feature usage</li>
      <li>Tool access</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">3 Administrative Permissions</h4>
    <ul className="card-desc">
      <li>User management</li>
      <li>Role management</li>
      <li>System settings</li>
    </ul>
  </div>

</div>



## Best Practices

<!-- 1. **Role Design**
   - Follow principle of least privilege
   - Create roles based on job functions
   - Document role purposes
   - Regular role reviews

2. **Permission Management**
   - Group related permissions
   - Regular permission audits
   - Document permission assignments
   - Monitor role usage

3. **Role Assignment**
   - Assign minimum necessary roles
   - Regular access reviews
   - Document role assignments
   - Monitor role changes

4. **Maintenance**
   - Archive unused roles
   - Update role definitions
   - Clean up permissions
   - Review inheritance -->


   <div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 Role Design</h4>
    <ul className="card-desc">
      <li>Follow principle of least privilege</li>
      <li>Create roles based on job functions</li>
      <li>Document role purposes</li>
      <li>Regular role reviews</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 Permission Management</h4>
    <ul className="card-desc">
      <li>Group related permissions</li>
      <li>Regular permission audits</li>
      <li>Document permission assignments</li>
      <li>Monitor role usage</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">3 Role Assignment</h4>
    <ul className="card-desc">
      <li>Assign minimum necessary roles</li>
      <li>Regular access reviews</li>
      <li>Document role assignments</li>
      <li>Monitor role changes</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">4 Maintenance</h4>
    <ul className="card-desc">
      <li>Archive unused roles</li>
      <li>Update role definitions</li>
      <li>Clean up permissions</li>
      <li>Review inheritance</li>
    </ul>
  </div>

</div>




## Common Operations

### Creating a New Role

```json
{
  "name": "project_manager",
  "description": "Manages project resources and team members",
  "baseRole": "team_lead",
  "permissions": {
    "projects": ["create", "read", "update", "delete"],
    "teams": ["manage", "assign"],
    "reports": ["view", "export"]
  }
}
```

### Modifying Role Permissions

```json
{
  "role": "project_manager",
  "addPermissions": {
    "budget": ["view", "manage"],
    "resources": ["allocate"]
  },
  "removePermissions": {
    "reports": ["export"]
  }
}
```

### Role Assignment to Users

```json
{
  "userId": "user123",
  "roles": {
    "add": ["project_manager"],
    "remove": ["team_member"]
  },
  "reason": "Promotion to Project Manager",
  "effectiveDate": "2024-01-01"
}
```
