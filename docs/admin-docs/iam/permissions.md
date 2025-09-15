---
sidebar_position: 3
---

# Permissions

Permissions in SOLID are automatically discovered based on controller actions and provide fine-grained control over what users can do within the system.

## Permission System

### Automatic Discovery
- Permissions are automatically generated from controller actions
- Each controller method becomes a permission
- Permissions follow a consistent naming pattern
- Custom permissions can be added manually

### Permission Structure

```bash
module:resource:action

Examples:
- users:profile:read
- content:articles:create
- media:files:upload
```

## Permission Types

### Resource Permissions

<!-- 1. **CRUD Operations**
   - Create: `resource:create`
   - Read: `resource:read`
   - Update: `resource:update`
   - Delete: `resource:delete`

2. **Special Operations**
   - Import: `resource:import`
   - Export: `resource:export`
   - Archive: `resource:archive`
   - Restore: `resource:restore` -->


<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 CRUD Operations</h4>
    - Create: `resource:create`
   - Read: `resource:read`
   - Update: `resource:update`
   - Delete: `resource:delete`
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 Special Operations</h4>
    - Import: `resource:import`
   - Export: `resource:export`
   - Archive: `resource:archive`
   - Restore: `resource:restore`

  </div>

</div>




### Administrative Permissions

<!-- 1. **User Management**
   - Create users: `users:create`
   - Manage roles: `roles:manage`
   - Assign permissions: `permissions:assign`

2. **System Settings**
   - Configure system: `settings:manage`
   - Manage modules: `modules:manage`
   - View logs: `logs:read` -->



<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 User Management</h4>
    - Create users: `users:create`
   - Manage roles: `roles:manage`
   - Assign permissions: `permissions:assign`
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 System Settings</h4>
      - Configure system: `settings:manage`
   - Manage modules: `modules:manage`
   - View logs: `logs:read`


  </div>

</div>


### Feature Permissions

<!-- 1. **Module Access**
   - Access module: `module:access`
   - Configure module: `module:configure`
   - Manage module data: `module:manage`

2. **Tool Access**
   - Use import tool: `tools:import:use`
   - Use export tool: `tools:export:use`
   - Use admin tools: `tools:admin:use` -->


<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 Module Access</h4>
  - Access module: `module:access`
   - Configure module: `module:configure`
   - Manage module data: `module:manage`
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 Tool Access</h4>
     - Use import tool: `tools:import:use`
   - Use export tool: `tools:export:use`
   - Use admin tools: `tools:admin:use`


  </div>

</div>


## Permission Management

### Viewing Permissions

```json
{
  "module": "content",
  "permissions": [
    {
      "name": "content:articles:create",
      "description": "Create new articles",
      "category": "resource",
      "dependencies": ["content:access"]
    },
    {
      "name": "content:articles:publish",
      "description": "Publish articles",
      "category": "special",
      "dependencies": ["content:articles:create"]
    }
  ]
}
```

### Grouping Permissions

Permissions can be grouped for easier management:

```json
{
  "group": "content_management",
  "description": "Content Management Permissions",
  "permissions": [
    "content:articles:*",
    "content:categories:*",
    "media:images:upload"
  ]
}
```

## Permission Assignment

### Direct Assignment
```json
{
  "roleId": "editor",
  "permissions": [
    "content:articles:create",
    "content:articles:edit",
    "content:articles:publish"
  ]
}
```

### Pattern-based Assignment
```json
{
  "roleId": "content_admin",
  "patterns": [
    "content:*:*",      // All content permissions
    "media:images:*",    // All image permissions
    "!*.delete"         // Exclude delete permissions
  ]
}
```

## Best Practices

<!-- 1. **Permission Design**
   - Use clear, descriptive names
   - Follow naming conventions
   - Document permission purposes
   - Consider dependencies

2. **Permission Assignment**
   - Follow least privilege principle
   - Group related permissions
   - Regular permission audits
   - Document assignments

3. **Security**
   - Validate permission checks
   - Log permission changes
   - Monitor usage patterns
   - Regular security reviews

4. **Maintenance**
   - Clean up unused permissions
   - Update documentation
   - Review dependencies
   - Monitor performance -->

<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 Permission Design</h4>
    <ul className="card-desc">
      <li>Use clear, descriptive names</li>
      <li>Follow naming conventions</li>
      <li>Document permission purposes</li>
      <li>Consider dependencies</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 Permission Assignment</h4>
    <ul className="card-desc">
      <li>Follow least privilege principle</li>
      <li>Group related permissions</li>
      <li>Regular permission audits</li>
      <li>Document assignments</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">3 Security</h4>
    <ul className="card-desc">
      <li>Validate permission checks</li>
      <li>Log permission changes</li>
      <li>Monitor usage patterns</li>
      <li>Regular security reviews</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">4 Maintenance</h4>
    <ul className="card-desc">
      <li>Clean up unused permissions</li>
      <li>Update documentation</li>
      <li>Review dependencies</li>
      <li>Monitor performance</li>
    </ul>
  </div>

</div>





## Common Operations

### Creating Custom Permissions

```json
{
  "name": "reports:dashboard:export",
  "description": "Export dashboard reports",
  "category": "feature",
  "dependencies": [
    "reports:dashboard:view"
  ],
  "metadata": {
    "scope": "global",
    "auditLevel": "high"
  }
}
```

### Permission Dependency Check

```json
{
  "permission": "content:articles:publish",
  "dependencies": [
    {
      "requires": ["content:articles:create", "content:articles:edit"],
      "message": "User must have create and edit permissions to publish"
    }
  ]
}
```

### Permission Audit Log

```json
{
  "action": "permission_change",
  "timestamp": "2024-01-01T12:00:00Z",
  "details": {
    "role": "editor",
    "added": ["content:articles:publish"],
    "removed": ["content:articles:delete"],
    "reason": "Role responsibility adjustment",
    "performedBy": "admin@example.com"
  }
}
```
