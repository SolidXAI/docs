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

```
module:resource:action

Examples:
- users:profile:read
- content:articles:create
- media:files:upload
```

## Permission Types

### Resource Permissions

1. **CRUD Operations**
   - Create: `resource:create`
   - Read: `resource:read`
   - Update: `resource:update`
   - Delete: `resource:delete`

2. **Special Operations**
   - Import: `resource:import`
   - Export: `resource:export`
   - Archive: `resource:archive`
   - Restore: `resource:restore`

### Administrative Permissions

1. **User Management**
   - Create users: `users:create`
   - Manage roles: `roles:manage`
   - Assign permissions: `permissions:assign`

2. **System Settings**
   - Configure system: `settings:manage`
   - Manage modules: `modules:manage`
   - View logs: `logs:read`

### Feature Permissions

1. **Module Access**
   - Access module: `module:access`
   - Configure module: `module:configure`
   - Manage module data: `module:manage`

2. **Tool Access**
   - Use import tool: `tools:import:use`
   - Use export tool: `tools:export:use`
   - Use admin tools: `tools:admin:use`

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

1. **Permission Design**
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
   - Monitor performance

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
