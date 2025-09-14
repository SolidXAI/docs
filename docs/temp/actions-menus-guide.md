# SolidX Actions & Navigation Guide

This guide provides comprehensive documentation for actions and navigation configurations in SolidX platform metadata, with real examples from the fees-portal module.

## 1. ACTIONS OVERVIEW

Actions define what happens when users interact with UI elements like menu items, buttons, or links. They connect the frontend to backend functionality and determine how data is displayed or processed.

### Action Types
1. **Solid Actions**: Standard CRUD operations using SolidX's built-in views
2. **Custom Actions**: Custom components or pages with specific functionality
3. **Server Actions**: Direct API endpoint calls for backend operations

## 2. SOLID ACTIONS CONFIGURATION

Solid actions use predefined views and follow standard patterns for data management.

### Basic Solid Action Structure
```json
{
  "displayName": "Institute List View",        // User-friendly action name
  "name": "institute-list-view",              // Internal action reference (kebab-case)
  "type": "solid",                           // Action type: solid, custom
  "domain": "",                              // Domain context (optional)
  "context": "",                             // Additional configuration (optional)
  "customComponent": "/admin/address-master/institute/all",  // UI route path
  "customIsModal": true,                     // Display as modal dialog
  "serverEndpoint": "",                      // API endpoint (empty for views)
  "viewUserKey": "institute-list-view",      // Target view reference
  "moduleUserKey": "fees-portal",            // Module this action belongs to
  "modelUserKey": "institute"                // Model for standard actions
}
```

### Real Examples from Fees Portal

#### List View Action
```json
{
  "displayName": "Institute List View",
  "name": "institute-list-view",
  "type": "solid",
  "customComponent": "/admin/address-master/institute/all",
  "customIsModal": true,
  "viewUserKey": "institute-list-view",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "institute"
}
```

#### Form View Action
```json
{
  "displayName": "Create New Institute",
  "name": "institute-create-action",
  "type": "solid",
  "customComponent": "/admin/address-master/institute/create",
  "customIsModal": true,
  "viewUserKey": "institute-form-view",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "institute"
}
```

#### Edit Action
```json
{
  "displayName": "Edit Institute",
  "name": "institute-edit-action",
  "type": "solid",
  "customComponent": "/admin/address-master/institute/edit",
  "customIsModal": true,
  "viewUserKey": "institute-form-view",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "institute"
}
```

## 3. CUSTOM ACTIONS CONFIGURATION

Custom actions provide flexibility for specialized functionality that doesn't fit standard CRUD patterns.

### Basic Custom Action Structure
```json
{
  "displayName": "Custom Dashboard",          // User-friendly action name
  "name": "custom-dashboard-action",         // Internal action reference
  "type": "custom",                         // Action type: custom
  "domain": "",                             // Domain context
  "context": "{\"param1\": \"value1\"}",    // JSON configuration
  "customComponent": "/admin/custom/dashboard",  // Custom React component path
  "customIsModal": false,                   // Display as full page (not modal)
  "serverEndpoint": "",                     // API endpoint (if applicable)
  "viewUserKey": "",                        // Empty for custom actions
  "moduleUserKey": "fees-portal",           // Module context
  "modelUserKey": ""                        // Empty for custom actions
}
```

### Real Examples from Fees Portal

#### Home/Dashboard Action
```json
{
  "displayName": "fees-portal Home",
  "name": "fees-portal-home-action",
  "type": "custom",
  "customComponent": "/admin/core/fees-portal/home",
  "customIsModal": true,
  "viewUserKey": "",
  "moduleUserKey": "fees-portal",
  "modelUserKey": ""
}
```

#### Portal Preview Action
```json
{
  "displayName": "Preview Portal",
  "name": "preview-portal-action",
  "type": "custom",
  "customComponent": "/admin/core/fees-portal/preview",
  "customIsModal": true,
  "viewUserKey": "",
  "moduleUserKey": "fees-portal",
  "modelUserKey": ""
}
```

## 4. SERVER ACTIONS CONFIGURATION

Server actions handle backend operations that don't require UI components.

### Basic Server Action Structure
```json
{
  "displayName": "Export Data",              // User-friendly action name
  "name": "export-data-action",             // Internal action reference
  "type": "custom",                        // Still "custom" type
  "serverEndpoint": "/api/v1/export",       // Direct API endpoint
  "customComponent": "",                    // Empty for server-only actions
  "customIsModal": false,                  // Not applicable
  "viewUserKey": "",                       // Empty
  "moduleUserKey": "fees-portal",          // Module context
  "modelUserKey": ""                       // Empty
}
```

## 5. MENUS CONFIGURATION

Menus define the navigation structure and connect actions to UI elements.

### Basic Menu Item Structure
```json
{
  "displayName": "Institute Management",     // Menu item text
  "name": "institute-menu-item",            // Internal menu reference (kebab-case)
  "sequenceNumber": 2,                      // Order in menu (1, 2, 3, etc.)
  "actionUserKey": "institute-list-view",   // Action triggered on click
  "moduleUserKey": "fees-portal",           // Module this menu belongs to
  "parentMenuItemUserKey": "",              // Parent menu for nested items
  "roles": ["Institute Admin", "Mswipe Admin"]  // User roles that can see this menu
}
```

### Real Examples from Fees Portal

#### Top-Level Menu Items
```json
{
  "displayName": "Home",
  "name": "fees-portal-home-menu",
  "sequenceNumber": 1,
  "actionUserKey": "fees-portal-home-action",
  "moduleUserKey": "fees-portal",
  "parentMenuItemUserKey": "",
  "roles": []
},
{
  "displayName": "Institute",
  "name": "institute-menu-item",
  "sequenceNumber": 2,
  "actionUserKey": "institute-list-view",
  "moduleUserKey": "fees-portal",
  "parentMenuItemUserKey": "",
  "roles": ["Institute Admin", "Mswipe Admin"]
}
```

#### Nested Menu Items
```json
{
  "displayName": "Settings",
  "name": "settings-submenu",
  "sequenceNumber": 1,
  "actionUserKey": "",
  "moduleUserKey": "fees-portal",
  "parentMenuItemUserKey": "",
  "roles": ["Admin"]
},
{
  "displayName": "General Settings",
  "name": "general-settings-menu",
  "sequenceNumber": 1,
  "actionUserKey": "general-settings-action",
  "moduleUserKey": "fees-portal",
  "parentMenuItemUserKey": "settings-submenu",
  "roles": ["Admin"]
},
{
  "displayName": "Payment Settings",
  "name": "payment-settings-menu",
  "sequenceNumber": 2,
  "actionUserKey": "payment-settings-action",
  "moduleUserKey": "fees-portal",
  "parentMenuItemUserKey": "settings-submenu",
  "roles": ["Admin"]
}
```

## 6. ACTION SECURITY AND ROLES

### Role-Based Action Access
```json
{
  "displayName": "Admin Dashboard",
  "name": "admin-dashboard-action",
  "type": "custom",
  "roles": ["Admin", "SuperAdmin"],        // Only these roles can access
  "customComponent": "/admin/dashboard",
  "customIsModal": false
}
```

### Menu-Level Security
```json
{
  "displayName": "User Management",
  "name": "user-management-menu",
  "sequenceNumber": 10,
  "actionUserKey": "user-list-action",
  "roles": ["Admin"],                       // Menu hidden from non-admin users
  "moduleUserKey": "fees-portal"
}
```

## 7. ACTION CONTEXT AND PARAMETERS

### Context Configuration
```json
{
  "displayName": "Filtered Student List",
  "name": "filtered-student-action",
  "type": "solid",
  "context": "{\"filter\": {\"status\": \"active\"}, \"sort\": \"name\"}",
  "viewUserKey": "student-list-view",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "student"
}
```

### Dynamic Context with Placeholders
```json
{
  "displayName": "Student Details",
  "name": "student-detail-action",
  "type": "solid",
  "context": "{\"studentId\": \"{{recordId}}\", \"mode\": \"view\"}",
  "viewUserKey": "student-detail-view",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "student"
}
```

## 8. ACTION ROUTING PATTERNS

### Standard SolidX Routing
SolidX uses consistent URL patterns for actions:

```
# List Views
/admin/{module}/{model}/all
/admin/address-master/institute/all

# Create Forms
/admin/{module}/{model}/create
/admin/address-master/institute/create

# Edit Forms
/admin/{module}/{model}/edit
/admin/address-master/institute/edit

# Custom Components
/admin/{module}/{custom-path}
/admin/core/fees-portal/home
```

### Route Parameters
```json
{
  "customComponent": "/admin/address-master/institute/all?status=active&page=1",
  "customIsModal": true
}
```

## 9. BULK ACTIONS CONFIGURATION

### Bulk Action Structure
```json
{
  "displayName": "Bulk Update Status",
  "name": "bulk-status-update-action",
  "type": "custom",
  "context": "{\"operation\": \"bulk_update\", \"field\": \"status\"}",
  "serverEndpoint": "/api/v1/institute/bulk-update",
  "customComponent": "/admin/bulk-actions/status-update",
  "customIsModal": true,
  "roles": ["Admin", "Manager"]
}
```

## 10. ACTION EVENT HANDLERS

### Action Event Configuration
```json
{
  "displayName": "Submit Form",
  "name": "submit-form-action",
  "type": "custom",
  "context": "{\"onSuccess\": \"redirectToList\", \"onError\": \"showErrorMessage\"}",
  "serverEndpoint": "/api/v1/submit",
  "eventHandlers": {
    "onBeforeAction": "validateForm",
    "onSuccess": "handleSuccess",
    "onError": "handleError"
  }
}
```

## 11. ACTION WORKFLOW INTEGRATION

### Workflow-Triggered Actions
```json
{
  "displayName": "Approve Request",
  "name": "approve-request-action",
  "type": "custom",
  "context": "{\"workflowStage\": \"approval\", \"nextStage\": \"processing\"}",
  "serverEndpoint": "/api/v1/workflow/approve",
  "customComponent": "/admin/workflow/approve-modal",
  "customIsModal": true,
  "roles": ["Approver", "Manager"]
}
```

## 12. MENU CONFIGURATION BEST PRACTICES

### Menu Organization
1. **Logical Grouping**: Group related functionality under parent menus
2. **Sequence Numbers**: Use consistent numbering for menu order
3. **Role-Based Visibility**: Configure appropriate roles for each menu item
4. **User Experience**: Place frequently used items at the top

### Action Naming Conventions
```
# List Actions
{model}-list-view
institute-list-view

# Create Actions
{model}-create-action
student-create-action

# Edit Actions
{model}-edit-action
payment-edit-action

# Custom Actions
{feature}-{action}-action
fees-portal-home-action
bulk-export-action
```

### Security Best Practices
1. **Principle of Least Privilege**: Only assign necessary roles to actions
2. **Hierarchical Access**: Use role hierarchies for menu visibility
3. **Audit Trails**: Enable logging for sensitive actions
4. **Input Validation**: Validate all action parameters

## 13. COMPLETE NAVIGATION EXAMPLE

Here's a complete navigation structure example from the fees-portal:

```json
{
  "menus": [
    {
      "displayName": "Home",
      "name": "fees-portal-home-menu",
      "sequenceNumber": 1,
      "actionUserKey": "fees-portal-home-action"
    },
    {
      "displayName": "Institute",
      "name": "institute-menu-item",
      "sequenceNumber": 2,
      "actionUserKey": "institute-list-view",
      "roles": ["Institute Admin", "Mswipe Admin"]
    },
    {
      "displayName": "Initiate Payments",
      "name": "paymentCollection-menu-item",
      "sequenceNumber": 3,
      "actionUserKey": "paymentCollection-list-view",
      "roles": ["Institute Admin", "Mswipe Admin"]
    },
    {
      "displayName": "Created Payments",
      "name": "paymentCollectionItem-menu-item",
      "sequenceNumber": 4,
      "actionUserKey": "paymentCollectionItem-list-view",
      "roles": ["Institute Admin", "Mswipe Admin"]
    },
    {
      "displayName": "Payments Collected",
      "name": "payment-menu-item",
      "sequenceNumber": 5,
      "actionUserKey": "payment-list-view",
      "roles": ["Institute Admin", "Mswipe Admin"]
    },
    {
      "displayName": "Students",
      "name": "student-menu-item",
      "sequenceNumber": 6,
      "actionUserKey": "student-list-view",
      "roles": ["Institute Admin", "Mswipe Admin"]
    }
  ],
  "actions": [
    {
      "displayName": "fees-portal Home",
      "name": "fees-portal-home-action",
      "type": "custom",
      "customComponent": "/admin/core/fees-portal/home",
      "customIsModal": true
    },
    {
      "displayName": "Institute List View",
      "name": "institute-list-view",
      "type": "solid",
      "customComponent": "/admin/address-master/institute/all",
      "customIsModal": true,
      "viewUserKey": "institute-list-view",
      "modelUserKey": "institute"
    }
    // ... additional actions
  ]
}
```

This comprehensive guide covers all aspects of actions and navigation in SolidX, from basic CRUD operations to complex custom workflows, with real examples from your fees-portal module.
