---
title: View Metadata
description: Metadata schema for defining views in SolidX applications.
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
    - List Views: Tabular display with search, filter, pagination
    - Form Views: Input forms for create/edit operations
    - Kanban Views: Card-based display with drag-and-drop

### Example: Fee Portal List/Form Views
<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    View Schema
  </summary>
  
``` json
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
        },
        ... // Other row button configuration objects
      ],
      "configureViewActions": {
        "import": { "roles": ["Admin", "Mswipe Admin"] },
        ... // Other view action configuration objects
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
        },
        ... // Other field layout configuration objects
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
                          { "type": "field", "attrs": { "name": "instituteName" } },
                          ... // Other field layout configuration objects
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
                      },
                      ... // Other column configuration objects
                    ]
                  }
                ]
              },
              ... // Other notebook page configuration objects
            ]
          }
        ]
      }
    ]
  }
}
  ```  
</details>

<!-- ### Example: Kanban View
You can refer to the [Kanban View Example](../../recipes/view-configurations-guide#4-kanban-view-configuration) for a detailed example of Kanban view metadata. -->

## View Configurations
<h3 className=" card-headear-wrapper">
    <MdViewList size={22}  />

### List View
</h3>
List views display records in tabular format with advanced features like search, filtering, and pagination.

#### 1. Basic List View Structure
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

#### 2. List View Attributes
```json
"attrs": {
    // Enable pagination
    "pagination": true,
    // Available page sizes                    
    "pageSizeOptions": [10, 25, 50],
    // Enable global search       
    "enableGlobalSearch": true,
    // Allow record creation from list            
    "create": true,
    // Allow inline/record editing                        
    "edit": true,
    // Allow record deletion                          
    "delete": true,
    // Role-based action permissions                        
    "import": {
      "roles": ["Admin"]
    },
    "showArchived": {
      "roles": ["Admin"]
    },
    "export": {
      "roles": ["Admin", "Institute Admin"]
    },
    "customizeLayout": {
      "roles": ["Admin"]
    },
    "saveCustomFilter": {
      "roles": ["Admin"]
    }
  }
}
```

#### 3. List View Field Configuration
```json
"children": [
  {
    "type": "field",
    "attrs": {
    "name": "instituteName",    // Field name from model
    "sortable": true,           // Enable column sorting
    "filterable": true,         // Enable column filtering
    "isSearchable": true        // Include in global search
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
      // Custom widget for display
      "viewWidget": "maskedShortTextList",  
      "sortable": true,
      "filterable": true,
      "isSearchable": true
    }
  }
]
```

<h3 className=" card-headear-wrapper">
    <MdDescription size={22}  />

### Form View
</h3>
Form views handle data entry and editing with complex layout structures using sheets, notebooks, and pages.

#### 1. Basic Form View Structure
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
    "onFormLayoutLoad": "instituteEditHandler",  // Event handler
    "children": [
      // Layout components (sheets, notebooks, etc.)
    ]
  }
}
```

#### 2. Form View Attributes
```json
"attrs": {
  "name": "form-1",                      // Form identifier
  "label": "Institute",                  // Form title
  "className": "grid",                   // CSS class for layout
  "formButtons": [                       // Custom form buttons
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

#### 3. Form Layout Components Hierarchy

Form layouts use a hierarchical structure:
```
Form
└── Sheet (top-level container)
    └── Notebook (tab container)
        └── Page (individual tab)
            └── Row (horizontal layout)
                └── Column (vertical container)
                    └── Field (input component)
```

##### Sheet Component
```json
{
  "type": "sheet",
  "attrs": {
    "name": "sheet-1"
  },
  "children": [
    // Notebook or Row components
  ]
}
```

##### Notebook Component (Tabs)
```json
{
  "type": "notebook",
  "attrs": {
    "name": "notebook-1"
  },
  "children": [
    // Page components (tabs)
  ]
}
```

##### Page Component (Individual Tab)
```json
{
  "type": "page",
  "attrs": {
    "name": "page-1",
    "label": "Institutes"
  },
  "children": [
    // Row components
  ]
}
```

##### Row Component (Horizontal Layout)
```json
{
  "type": "row",
  "attrs": {
    "name": "row-1"
  },
  "children": [
    // Column components
  ]
}
```

##### Column Component (Vertical Container)
```json
{
  "type": "column",
  "attrs": {
    "name": "column-1",
    "label": "Institutes Basic",        // Optional group label
    "className": "col-6"                // CSS grid class
  },
  "children": [
    // Field components
  ]
}
```

##### Field Component (Form Input)
```json
{
  "type": "field",
  "attrs": {
    "name": "instituteName",            // Field name from model
    "disabled": false,                  // Field enabled/disabled
    "showLabel": true,                  // Show field label
    "viewWidget": "default",            // Display widget override
    "editWidget": "default"             // Edit widget override
  }
}
```

##### Complete Form Layout Example
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
              "attrs": {
                "name": "page-1",
                "label": "Institutes"
              },
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
                        {
                          "type": "field",
                          "attrs": { "name": "instituteName" }
                        },
                        {
                          "type": "field",
                          "attrs": { "name": "description" }
                        }
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
            },
            {
              "type": "page",
              "attrs": {
                "name": "page-2",
                "label": "Payment Gateway Details"
              },
              "children": [
                // Additional form sections
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

<h3 className=" card-headear-wrapper">
    <MdViewKanban size={22}  />

### Kanban View
</h3>

Kanban views display records as cards with drag-and-drop functionality.


#### 1. Basic Kanban View Structure
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

#### 2. Kanban View Attributes
```json
"attrs": {
  "swimlanesCount": 10,                 // Number of swimlanes to show
  "recordsInSwimlane": 5,               // Records per swimlane
  "enableGlobalSearch": true,           // Enable search functionality
  "create": true,                       // Allow record creation
  "edit": true,                         // Allow record editing
  "delete": true,                       // Allow record deletion
  "groupBy": "status",                  // Field to group cards by
  "draggable": true,                    // Enable drag-and-drop
  "allowedViews": ["list", "kanban"]    // Alternative view types
}
```

#### 3. Kanban Card Template
```json
"children": [
  {
    "type": "cardTemplate",
    "attrs": {
      "name": "task-card"
    },
    "children": [
      {
        "type": "field",
        "attrs": {
          "name": "title",
          "displayType": "header"       // Display as card header
        }
      },
      {
        "type": "field",
        "attrs": {
          "name": "description",
          "displayType": "content"      // Display as card content
        }
      },
      {
        "type": "field",
        "attrs": {
          "name": "priority",
          "displayType": "badge"        // Display as colored badge
        }
      }
    ]
  }
]
```

## View RBAC

Views support role-based access control (RBAC) to restrict actions and field-level permissions based on user roles.

Below view actions will be visible/enabled only for users with the specified roles.
<h3 className=" card-headear-wrapper">
    <MdSecurity size={21}  />

### Role-Based View Actions
</h3>

```json
"configureViewActions": {
  "import": {
    "roles": ["Admin", "Manager"]
  },
  "export": {
    "roles": ["Admin", "Manager", "User"]
  },
  "customizeLayout": {
    "roles": ["Admin"]
  },
  "saveCustomFilter": {
    "roles": ["Admin", "Manager"]
  }
}
```

Below field will be visible only for users with the specified roles. This works in both list and form views.
<h3 className=" card-headear-wrapper">
    <RiLockLine size={21}  />

### Field-Level Permissions in Views
</h3>

```json
{
  "type": "field",
  "attrs": {
    "name": "salary",
    "roles": ["Admin", "HR"],       // Who can view this field
  }
}
```

<h3 className=" card-headear-wrapper">
    <MdWidgets size={21}  />

### View Widgets (TODO)
</h3>
Views support custom widgets to enhance field display and editing experiences. List view supports `viewWidget` and form views support `viewWidget` for view mode and `editWidget` for edit mode respectively.

#### Custom View Widgets
```json
{
  "type": "field",
  "attrs": {
    "name": "password",
    "viewWidget": "maskedShortTextList",    // List view widget
    "editWidget": "maskedShortTextEdit"     // Edit form widget
  }
}
```

#### Available Widget Types
- **Default widgets**: Auto-selected based on field type
- **Custom widgets**: Specific widget overrides for special display needs
- **Masked widgets**: For sensitive data (passwords, secrets)
- **Rich widgets**: For formatted content display

<h3 className=" card-headear-wrapper">
    <FaBolt size={21}  />

### View Event Handlers (TODO)
</h3>

Views support event handlers to execute custom logic at various stages of the view lifecycle. We can write custom handlers in our project which react to these events and modify view behavior dynamically.


#### Event Handler Types
- `onFormLayoutLoad`: Executed when form loads
- `onFormDataLoad`: Executed after form data is loaded
- `onFieldChange`: Triggered on field value changes
- `onFormSubmit`: Executed before form submission
- `onViewLoad`: Executed when view loads

<h3 className=" card-headear-wrapper">
    <MdViewQuilt size={24}  />

### View Layout Responsive Design
</h3>

#### CSS Grid Classes
```json
{
  "type": "column",
  "attrs": {
    "className": "col-12 col-md-6 col-lg-4"  // Responsive grid classes
  }
}
```

#### Layout Breakpoints
- `col-12`: Full width on all screens
- `col-md-6`: Half width on medium screens and up
- `col-lg-4`: Third width on large screens and up

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

Defines the **layout and structure** of the view.  
Controls how fields, widgets, buttons, and other UI elements are organized.

**Default:** N/A

####  Further Reference

For detailed attribute-level documentation of the `layout` schema per view type, see:

-  **List View:** [List View Layout Attributes](../../recipes/view-configurations-guide#list-view-attributes)  
-  **Form View:** [Form View Layout Attributes](../../recipes/view-configurations-guide#form-view-attributes)  
-  **Kanban View:** [Kanban View Layout Attributes](../../recipes/view-configurations-guide#kanban-view-attributes)




<InfoBox>
  Each view type has its own expected `layout` schema. Use the links above to understand required keys, optional properties, and usage examples.

</InfoBox>



### `moduleUserKey` *(string, optional)*
User key of the module this view belongs to.  
**Default:** N/A



### `modelUserKey` *(string, optional)*
User key of the model this view is associated with.  
**Default:** N/A    

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
