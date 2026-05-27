---
title: Menu Structure
---

SOLID automatically generates and manages the admin panel's menu structure based on your modules and resources. The menu system provides an intuitive way to navigate through your application's features.

## Menu Organization

### Automatic Generation

- Each module gets its own menu section
- Resources within modules appear as sub-items
- Menu items are automatically ordered alphabetically
- Access control is integrated with permissions

### Menu Hierarchy

```
├── Module 1
│   ├── Resource 1
│   ├── Resource 2
│   └── Resource 3
├── Module 2
│   ├── Resource 4
│   └── Resource 5
└── System
    ├── Users
    ├── Roles
    └── Settings
```

## Menu Configuration

You can customize the menu structure through configuration:

```json
{
  "menu": {
    "items": [
      {
        "module": "sales",
        "label": "Sales Management",
        "icon": "shopping-cart",
        "order": 1,
        "items": [
          {
            "resource": "customers",
            "label": "Customers",
            "icon": "users",
            "order": 1
          },
          {
            "resource": "orders",
            "label": "Orders",
            "icon": "file-text",
            "order": 2
          }
        ]
      }
    ]
  }
}
```

### Configuration Options

| Option  | Description                           |
| ------- | ------------------------------------- |
| label   | Display name in the menu              |
| icon    | Menu item icon                        |
| order   | Custom ordering (lower numbers first) |
| visible | Show/hide menu item                   |
| roles   | Role-based visibility                 |

## Features

<div>

<div>
  Dynamic Updates
  <ul>
    <li>Menu updates automatically when modules/resources change</li>
    <li>Real-time permission checks</li>
    <li>Responsive to user role changes</li>
    <li>Support for dynamic sub-menus</li>
  </ul>
</div>

<div>
  Access Control
  <ul>
    <li>Menu items respect user permissions</li>
    <li>Role-based visibility</li>
    <li>Resource-level access control</li>
    <li>Custom permission rules</li>
  </ul>
</div>

<div>
  Customization
  <ul>
    <li>Custom icons</li>
    <li>Custom ordering</li>
    <li>Custom labels</li>
    <li>Nested menu structures</li>
  </ul>
</div>

</div>

## Best Practices
<details>
    <summary>Organization</summary>
    <ul>
      <li>Group related items together</li>
      <li>Use clear, descriptive labels</li>
      <li>Keep menu depth manageable</li>
      <li>Consider user workflow</li>
    </ul>
</details>
<details>
    <summary>Permissions</summary>
    <ul>
      <li>Set appropriate access levels</li>
      <li>Group similar permissions</li>
      <li>Document permission requirements</li>
      <li>Regular permission audits</li>
    </ul>
</details>
<details>
    <summary>User Experience</summary>
   <ul>
      <li>Use meaningful icons</li>
      <li>Maintain consistent naming</li>
      <li>Optimize menu depth</li>
      <li>Consider mobile users</li>
    </ul>
</details>
<details>
    <summary>Maintenance</summary>
      <ul>
      <li>Regular menu audits</li>
      <li>Update outdated labels</li>
      <li>Remove unused items</li>
      <li>Monitor access patterns</li>
    </ul>
</details>

