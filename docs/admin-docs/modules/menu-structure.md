---
sidebar_position: 4
---

# Menu Structure

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

| Option | Description |
|--------|-------------|
| label | Display name in the menu |
| icon | Menu item icon |
| order | Custom ordering (lower numbers first) |
| visible | Show/hide menu item |
| roles | Role-based visibility |

## Features

<!-- ### Dynamic Updates
- Menu updates automatically when modules/resources change
- Real-time permission checks
- Responsive to user role changes
- Support for dynamic sub-menus

### Access Control
- Menu items respect user permissions
- Role-based visibility
- Resource-level access control
- Custom permission rules

### Customization
- Custom icons
- Custom ordering
- Custom labels
- Nested menu structures -->


<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">
    1  Dynamic Updates
    </h4>
    <ul className="card-desc">
      <li>Menu updates automatically when modules/resources change</li>
      <li>Real-time permission checks</li>
      <li>Responsive to user role changes</li>
      <li>Support for dynamic sub-menus</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">
    2  Access Control
    </h4>
    <ul className="card-desc">
      <li>Menu items respect user permissions</li>
      <li>Role-based visibility</li>
      <li>Resource-level access control</li>
      <li>Custom permission rules</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">
    3  Customization
    </h4>
    <ul className="card-desc">
      <li>Custom icons</li>
      <li>Custom ordering</li>
      <li>Custom labels</li>
      <li>Nested menu structures</li>
    </ul>
  </div>

</div>



## Best Practices

<!-- 1. **Organization**
   - Group related items together
   - Use clear, descriptive labels
   - Keep menu depth manageable
   - Consider user workflow

2. **Permissions**
   - Set appropriate access levels
   - Group similar permissions
   - Document permission requirements
   - Regular permission audits

3. **User Experience**
   - Use meaningful icons
   - Maintain consistent naming
   - Optimize menu depth
   - Consider mobile users

4. **Maintenance**
   - Regular menu audits
   - Update outdated labels
   - Remove unused items
   - Monitor access patterns -->

<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">
    1  Organization
    </h4>
    <ul className="card-desc">
      <li>Group related items together</li>
      <li>Use clear, descriptive labels</li>
      <li>Keep menu depth manageable</li>
      <li>Consider user workflow</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">
    2  Permissions
    </h4>
    <ul className="card-desc">
      <li>Set appropriate access levels</li>
      <li>Group similar permissions</li>
      <li>Document permission requirements</li>
      <li>Regular permission audits</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">
    3  User Experience
    </h4>
    <ul className="card-desc">
      <li>Use meaningful icons</li>
      <li>Maintain consistent naming</li>
      <li>Optimize menu depth</li>
      <li>Consider mobile users</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">
    4  Maintenance
    </h4>
    <ul className="card-desc">
      <li>Regular menu audits</li>
      <li>Update outdated labels</li>
      <li>Remove unused items</li>
      <li>Monitor access patterns</li>
    </ul>
  </div>

</div>
