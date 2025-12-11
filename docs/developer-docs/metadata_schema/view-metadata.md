---
title: View Metadata
description: Metadata schema for defining views in SolidX applications — with explanations before each code snippet.
summary: This document explains view metadata in SolidX, which defines UI presentations of models and automatically generates list views (tabular displays with search, filter, pagination), form views (input forms for create/edit operations), and kanban views (card-based displays with drag-and-drop). Each example below now starts with a short “What this shows” explanation.
sidebar_position: 4
json_pointer: "/views"
jsonpath: "$.views"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#view-metadata-attributes"
solidx_concerns: [update_layout, add_field_to_existing_layout, remove_field_from_existing_layout, modify_layout_field_attribute]
---

import { MdViewList,MdDescription,MdViewKanban,MdSecurity,MdWidgets,MdViewQuilt } from "react-icons/md";
import { RiLockLine } from "react-icons/ri";
import { FaBolt } from "react-icons/fa";            
import { IoIosArrowForward } from "react-icons/io";
import { InfoBox } from '@site/src/common/InfoBox';

# View Metadata
> **Where it lives**  
> **JSON Pointer:** `/views`  
> **JSONPath:** `$.views`  
> **Parent:** Root of the metadata file

## Overview
Views define UI presentation of models and automatically generate:
- **List Views:** Tabular display with search, filter, pagination
- **Form Views:** Input forms for create/edit operations
- **Kanban Views:** Card-based display with drag-and-drop

> **How to read this page**: Each code sample below is preceded by a short explanation of what the snippet configures and how it affects the generated UI.

---

## Example: Fee Portal List/Form Views
**What this shows:** A combined example of a **list** view and a **form** view for an *Institute* model inside a *Fees Portal* module. The list section demonstrates pagination, search and row actions. The form section demonstrates the hierarchical layout (sheet → notebook → page → row → column → field) and how to attach a form handler.

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    View Schema (List + Form)
  </summary>

```json
{ // List View for Institute Model
  "name": "institute-list-view",
  "displayName": "Institute",
  "type": "list",
  "context": "{}",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "institute",
  "layout": {
    "type": "list",
    "attrs": {
      "pagination": true,
      "pageSizeOptions": [10, 25, 50],
      "enableGlobalSearch": true,
      "create": true,
      "edit": true,
      "delete": true,
      "rowButtons": [
        {
          "attrs": {
            "className": "",
            "label": "Enable",
            "action": "ActivatePortal",
            "icon": "pi",
            "actionInContextMenu": false,
            "customComponentIsSystem": true,
            "openInPopup": true,
            "closable": true
          }
        }
      ],
      "configureViewActions": {
        "import": { "roles": ["Admin", "Mswipe Admin"] }
      },
      "children": [
        {
          "type": "field",
          "attrs": {
            "name": "id",
            "sortable": true,
            "filterable": true,
            "isSearchable": true
          }
        }
      ]
    }
  }
},
{ // Form View for Institute Model
  "name": "institute-form-view",
  "displayName": "Institute",
  "type": "form",
  "context": "{}",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "institute",
  "layout": {
    "type": "form",
    "attrs": {
      "name": "form-1",
      "label": "Institute",
      "className": "grid",
      "formButtons": [
        {
          "attrs": {
            "className": "",
            "label": "Preview",
            "action": "PreviewPortal",
            "icon": "pi",
            "actionInContextMenu": true,
            "openInPopup": true,
            "customComponentIsSystem": true,
            "closable": true
          }
        }
      ]
    },
    "onFormLayoutLoad": "instituteEditHandler",
    "children": [
      {
        "type": "sheet",
        "attrs": { "name": "sheet-1" },
        "children": [
          {
            "type": "notebook",
            "attrs": { "name": "notebook-1" },
            "children": [
              {
                "type": "page",
                "attrs": { "name": "page-1", "label": "Institutes" },
                "children": [
                  {
                    "type": "row",
                    "attrs": { "name": "sheet-1" },
                    "children": [
                      {
                        "type": "column",
                        "attrs": {
                          "name": "group-1",
                          "label": "Institutes Basic",
                          "className": "col-6"
                        },
                        "children": [
                          { "type": "field", "attrs": { "name": "instituteName" } }
                        ]
                      },
                      {
                        "type": "column",
                        "attrs": {
                          "name": "group-1",
                          "label": "Institutes Contact",
                          "className": "col-6"
                        },
                        "children": [
                          {
                            "type": "field",
                            "attrs": {
                              "name": "instituteAddress",
                              "disabled": false
                            }
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```
</details>

---

## View Configurations

<h3 className=" card-headear-wrapper">
  <MdViewList size={22} />
  <span style={{marginLeft: 8}}>List View</span>
</h3>

List views display records in tabular format with advanced features like search, filtering, and pagination.

### 1) Basic List View Structure
**What this shows:** The minimal configuration for a list view. Connect to a module/model and define a `layout` with `attrs` (behavior) and `children` (columns).

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  List View Structure
</summary>

```json
{
  "name": "institute-list-view",
  "displayName": "Institute",
  "type": "list",
  "context": "{}",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "institute",
  "layout": {
    "type": "list",
    "attrs": {
      // List view attributes
    },
    "children": [
      // Field configurations
    ]
  }
}
```
</details>

### 2) List View Attributes
**What this shows:** How to toggle pagination and CRUD actions from the list, and how to restrict actions to specific roles.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  List View Attributes
</summary>

```json
"attrs": {
  "pagination": true,
  "pageSizeOptions": [10, 25, 50],
  "enableGlobalSearch": true,
  "create": true,
  "edit": true,
  "delete": true,
  "import": { "roles": ["Admin"] },
  "showArchived": { "roles": ["Admin"] },
  "export": { "roles": ["Admin", "Institute Admin"] },
  "customizeLayout": { "roles": ["Admin"] },
  "saveCustomFilter": { "roles": ["Admin"] }
}
```
</details>

### 3) List View Field Configuration
**What this shows:** Each item in `children` is a column. Control sort, filter and search participation; `viewWidget` customizes how the value renders.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  Field Configuration
</summary>

```json
"children": [
  {
    "type": "field",
    "attrs": {
      "name": "instituteName",
      "sortable": true,
      "filterable": true,
      "isSearchable": true
    }
  },
  {
    "type": "field",
    "attrs": {
      "name": "logo",
      "sortable": true,
      "filterable": true,
      "isSearchable": true
    }
  },
  {
    "type": "field",
    "attrs": {
      "name": "paymentGatewayAccessSecret",
      "viewWidget": "maskedShortTextList",
      "sortable": true,
      "filterable": true,
      "isSearchable": true
    }
  }
]
```
</details>

---

<h3 className=" card-headear-wrapper">
  <MdDescription size={22} />
  <span style={{marginLeft: 8}}>Form View</span>
</h3>

Form views handle data entry and editing with complex layout structures using sheets, notebooks, and pages.

### 1) Basic Form View Structure
**What this shows:** A `form` view with a base layout and optional `onFormLayoutLoad` handler. `children` will hold sheets/notebooks/pages/rows/columns/fields.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  Form View Structure
</summary>

```json
{
  "name": "institute-form-view",
  "displayName": "Institute",
  "type": "form",
  "context": "{}",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "institute",
  "layout": {
    "type": "form",
    "attrs": {
      // Form view attributes
    },
    "onFormLayoutLoad": "instituteEditHandler",
    "children": [
      // Layout components (sheets, notebooks, etc.)
    ]
  }
}
```
</details>

### 2) Form View Attributes
**What this shows:** Configure visual details and attach custom buttons that trigger actions or popups.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  Form View Attributes
</summary>

```json
"attrs": {
  "name": "form-1",
  "label": "Institute",
  "className": "grid",
  "formButtons": [
    {
      "attrs": {
        "className": "",
        "label": "Preview",
        "action": "PreviewPortal",
        "icon": "pi",
        "actionInContextMenu": true,
        "openInPopup": true,
        "customComponentIsSystem": true,
        "closable": true
      }
    }
  ]
}
```
</details>

### 3) Form Layout Components Hierarchy
**What this shows:** How layout blocks nest to build rich, organized forms.

```
Form
└── Sheet (top-level container)
    └── Notebook (tab container)
        └── Page (individual tab)
            └── Row (horizontal layout)
                └── Column (vertical container)
                    └── Field (input component)
```

#### Sheet Component
**What this shows:** A top-level container for your form sections.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  Sheet Component
</summary>

```json
{
  "type": "sheet",
  "attrs": { "name": "sheet-1" },
  "children": [
    // Notebook or Row components
  ]
}
```
</details>

#### Notebook Component (Tabs)
**What this shows:** A tab container that groups multiple pages.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  Notebook Component
</summary>

```json
{
  "type": "notebook",
  "attrs": { "name": "notebook-1" },
  "children": [
    // Page components (tabs)
  ]
}
```
</details>

#### Page Component (Individual Tab)
**What this shows:** A single tab with its own content.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  Page Component
</summary>

```json
{
  "type": "page",
  "attrs": { "name": "page-1", "label": "Institutes" },
  "children": [
    // Row components
  ]
}
```
</details>

#### Row Component (Horizontal Layout)
**What this shows:** A horizontal group of columns.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  Row Component
</summary>

```json
{
  "type": "row",
  "attrs": { "name": "row-1" },
  "children": [
    // Column components
  ]
}
```
</details>

#### Column Component (Vertical Container)
**What this shows:** A vertical container with optional label and grid classes.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  Column Component
</summary>

```json
{
  "type": "column",
  "attrs": {
    "name": "column-1",
    "label": "Institutes Basic",
    "className": "col-6"
  },
  "children": [
    // Field components
  ]
}
```
</details>

#### Field Component (Form Input)
**What this shows:** A single form input with view/edit widget overrides.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  Field Component
</summary>

```json
{
  "type": "field",
  "attrs": {
    "name": "instituteName",
    "disabled": false,
    "showLabel": true,
    "viewWidget": "default",
    "editWidget": "default"
  }
}
```
</details>

#### Complete Form Layout Example
**What this shows:** A full, multi-tab form bringing together all components.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  Complete Form Layout Example
</summary>

```json
{
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "Institute",
    "className": "grid"
  },
  "onFormLayoutLoad": "instituteEditHandler",
  "children": [
    {
      "type": "sheet",
      "attrs": { "name": "sheet-1" },
      "children": [
        {
          "type": "notebook",
          "attrs": { "name": "notebook-1" },
          "children": [
            {
              "type": "page",
              "attrs": { "name": "page-1", "label": "Institutes" },
              "children": [
                {
                  "type": "row",
                  "attrs": { "name": "row-1" },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "column-1",
                        "label": "Institutes Basic",
                        "className": "col-6"
                      },
                      "children": [
                        { "type": "field", "attrs": { "name": "instituteName" } },
                        { "type": "field", "attrs": { "name": "description" } }
                      ]
                    },
                    {
                      "type": "column",
                      "attrs": {
                        "name": "column-2",
                        "label": "Institutes Contact",
                        "className": "col-6"
                      },
                      "children": [
                        { "type": "field", "attrs": { "name": "instituteAddress", "disabled": false } }
                      ]
                    }
                  ]
                }
              ]
            },
            {
              "type": "page",
              "attrs": { "name": "page-2", "label": "Payment Gateway Details" },
              "children": []
            }
          ]
        }
      ]
    }
  ]
}
```
</details>

---

<h3 className=" card-headear-wrapper">
  <MdViewKanban size={22} />
  <span style={{marginLeft: 8}}>Kanban View</span>
</h3>

Kanban views display records as cards with drag-and-drop functionality.

### 1) Basic Kanban View Structure
**What this shows:** Declares a `kanban` view and the places where swimlane and card configuration live.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  Kanban View Structure
</summary>

```json
{
  "name": "task-kanban-view",
  "displayName": "Task Board",
  "type": "kanban",
  "context": "{}",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "task",
  "layout": {
    "type": "kanban",
    "attrs": {
      // Kanban view attributes
    },
    "children": [
      // Card template configuration
    ]
  }
}
```
</details>

### 2) Kanban View Attributes
**What this shows:** Controls lane count, records per lane, the grouping field, and drag-and-drop.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  Kanban View Attributes
</summary>

```json
"attrs": {
  "swimlanesCount": 10,
  "recordsInSwimlane": 5,
  "enableGlobalSearch": true,
  "create": true,
  "edit": true,
  "delete": true,
  "groupBy": "status",
  "draggable": true,
  "allowedViews": ["list", "kanban"]
}
```
</details>

### 3) Kanban Card Template
**What this shows:** Maps model fields to parts of the card: header, content, badges.

<details>
<summary className="card-title card-header-wrapper">
  <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
  Kanban Card Template
</summary>

```json
"children": [
  {
    "type": "cardTemplate",
    "attrs": { "name": "task-card" },
    "children": [
      { "type": "field", "attrs": { "name": "title", "displayType": "header" } },
      { "type": "field", "attrs": { "name": "description", "displayType": "content" } },
      { "type": "field", "attrs": { "name": "priority", "displayType": "badge" } }
    ]
  }
]
```
</details>

---

## View RBAC

Views support role-based access control (RBAC) to restrict actions and field-level permissions based on user roles.

<h3 className=" card-headear-wrapper">
  <MdSecurity size={21} />
  <span style={{marginLeft: 8}}>Role-Based View Actions</span>
</h3>

**What this shows:** Limit visibility of list-level actions (import/export/layout customization) to specific roles.

<details>
  <summary className="card-title card-header-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    View Actions
  </summary>

```json
"configureViewActions": {
  "import": { "roles": ["Admin", "Manager"] },
  "export": { "roles": ["Admin", "Manager", "User"] },
  "customizeLayout": { "roles": ["Admin"] },
  "saveCustomFilter": { "roles": ["Admin", "Manager"] }
}
```
</details>

<h3 className=" card-headear-wrapper">
  <RiLockLine size={21} />
  <span style={{marginLeft: 8}}>Field-Level Permissions in Views</span>
</h3>

**What this shows:** Hide or show sensitive fields per role.

<details>
  <summary className="card-title card-header-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Field-Level Permissions
  </summary>

```json
{
  "type": "field",
  "attrs": {
    "name": "salary",
    "roles": ["Admin", "HR"]
  }
}
```
</details>

---

<h3 className=" card-headear-wrapper">
  <MdWidgets size={21} />
  <span style={{marginLeft: 8}}>View Widgets</span>
</h3>

Views support custom widgets to enhance field display and editing experiences. List view supports `viewWidget` and form views support `viewWidget` (view mode) and `editWidget` (edit mode).

**What this shows:** Override default rendering/editing of a field using specific named widgets.

<details>
  <summary className="card-title card-header-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Custom View Widgets
  </summary>

```json
{
  "type": "field",
  "attrs": {
    "name": "password",
    "viewWidget": "maskedShortTextList",
    "editWidget": "maskedShortTextEdit"
  }
}
```
</details>

#### Further Reference
- List View Widgets: [List View Widgets](/docs/developer-docs/extending/frontend-customization/list-view-field-widgets)
- Form View / Edit Widgets: [Form View Widgets](/docs/developer-docs/extending/frontend-customization/form-view-field-widgets)

---

<h3 className=" card-headear-wrapper">
  <FaBolt size={21} />
  <span style={{marginLeft: 8}}>View Event Handlers (TODO)</span>
</h3>

**What this shows:** Hook into lifecycle events to preprocess layout/data or react to user input.

- `onFormLayoutLoad`: Executed when form loads
- `onFormDataLoad`: Executed after form data is loaded
- `onFieldChange`: Triggered on field value changes
- `onFieldBlur`: Executed when a field loses focus
- `onCustomWidgetRender`: Called when a custom widget is rendered

Further reference: [Event Handlers Documentation](../extending/frontend-customization/form-view-events)

---

<h3 className=" card-headear-wrapper">
  <MdViewQuilt size={24} />
  <span style={{marginLeft: 8}}>View Layout Responsive Design</span>
</h3>

### CSS Grid Classes
**What this shows:** Use grid utility classes to control width across breakpoints.

<details>
  <summary className="card-title card-header-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    CSS Grid Classes
  </summary>

```json
{
  "type": "column",
  "attrs": { "className": "col-12 col-md-6 col-lg-4" }
}
```
</details>

#### Layout Breakpoints
- `col-12`: Full width on all screens
- `col-md-6`: Half width on medium screens and up
- `col-lg-4`: Third width on large screens and up

---

## View Metadata Attributes

### `name` *(string, required, unique)*
Name of the view (used for referencing).  
**Default:** N/A

### `displayName` *(string, required)*
Display name of the view (shown in the UI).  
**Default:** N/A

### `type` *(string, required)*
Type of view. Supported types:
- `list`: List view for displaying multiple records in a tabular format.
- `form`: Form view for creating/editing a single record.
- `kanban`: Kanban view for visualizing records as cards in columns.
**Default:** N/A

### `context` *(JSON, optional)*
JSON object defining context-specific parameters for the view.  
**Default:** N/A

### `layout` *(JSON, required)*
Defines the **layout and structure** of the view. Controls how fields, widgets, buttons, and other UI elements are organized.  
**Default:** N/A

#### Further Reference
- **List View:** [List View Layout Attributes](../../admin-docs/layouts/list-view#list-view-attributes-type-list)  
- **Form View:** [Form View Layout Attributes](../../admin-docs/layouts/form-view)  
- **Kanban View:** [Kanban View Layout Attributes](../../admin-docs/layouts/kanban-view#kanban-view-attributes) 

<InfoBox>
  Each view type has its own expected `layout` schema. Use the links above to understand required keys, optional properties, and usage examples.
</InfoBox>

### `moduleUserKey` *(string, optional)*
User key of the module this view belongs to.  
**Default:** N/A

### `modelUserKey` *(string, optional)*
User key of the model this view is associated with.  
**Default:** N/A    

---

## Best Practices

<details>
  <summary className="card-title card-header-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Layout Organization
  </summary>
  <ul className="card-desc">
    <li><strong>Use logical grouping</strong>: Group related fields in columns with descriptive labels</li>
    <li><strong>Progressive disclosure</strong>: Use tabs (notebooks) for complex forms</li>
    <li><strong>Responsive design</strong>: Use appropriate grid classes for different screen sizes</li>
    <li><strong>Field ordering</strong>: Place important fields first, follow logical workflow</li>
  </ul>
</details>

<details>
  <summary className="card-title card-header-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Security Considerations
  </summary>
  <ul className="card-desc">
    <li><strong>Role-based access</strong>: Configure view actions based on user roles</li>
    <li><strong>Field-level security</strong>: Hide sensitive fields from unauthorized users</li>
    <li><strong>Audit trails</strong>: Enable audit tracking for sensitive operations</li>
  </ul>
</details>

<details>
  <summary className="card-title card-header-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Performance Optimization
  </summary>
  <ul className="card-desc">
    <li><strong>Pagination</strong>: Always enable pagination for large datasets</li>
    <li><strong>Field selection</strong>: Only display necessary fields in list views</li>
  </ul>
</details>
