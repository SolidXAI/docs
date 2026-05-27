---
title: Permissions
---

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

### Resource Permissions

<div>

  <div>
    CRUD Operations
    - Create: `resource:create`  
    - Read: `resource:read`  
    - Update: `resource:update`  
    - Delete: `resource:delete`
  </div>

  <div>
    Special Operations
    - Import: `resource:import`  
    - Export: `resource:export`  
    - Archive: `resource:archive`  
    - Restore: `resource:restore`
  </div>

</div>

### Administrative Permissions

<div>

  <div>
    User Management
    - Create users: `users:create`  
    - Manage roles: `roles:manage`  
    - Assign permissions: `permissions:assign`
  </div>

  <div>
    System Settings
    - Configure system: `settings:manage`  
    - Manage modules: `modules:manage`  
    - View logs: `logs:read`
  </div>

</div>

### Feature Permissions

<div>

  <div>
    Module Access
    - Access module: `module:access`  
    - Configure module: `module:configure`  
    - Manage module data: `module:manage`
  </div>

  <div>
    Tool Access
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

### Best Practices 
<details>
  <summary>Permission Design</summary>
  <ul>
    <li>Use clear, descriptive names</li>
    <li>Follow naming conventions</li>
    <li>Document permission purposes</li>
    <li>Consider dependencies between permissions</li>
  </ul>
</details>
<details>
  <summary>Permission Assignment</summary>
  <ul>
    <li>Follow the principle of least privilege</li>
    <li>Group related permissions logically</li>
    <li>Perform regular permission audits</li>
    <li>Document assignments and changes</li>
  </ul>
</details>
<details>
  <summary>Security</summary>
  <ul>
    <li>Validate permission checks programmatically</li>
    <li>Log permission changes</li>
    <li>Monitor usage patterns for anomalies</li>
    <li>Perform regular security reviews</li>
  </ul>
</details>
<details>
  <summary>Maintenance</summary>
  <ul>
    <li>Clean up unused permissions</li>
    <li>Update permission documentation</li>
    <li>Review dependencies when modifying permissions</li>
    <li>Monitor performance and access patterns</li>
  </ul>
</details>
