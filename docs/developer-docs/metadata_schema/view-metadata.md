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
---

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
### List View
List views display records in tabular format with advanced features like search, filtering, and pagination.

#### Basic List View Structure
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

#### List View Attributes
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

#### List View Field Configuration
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

### Form View
Form views handle data entry and editing with complex layout structures using sheets, notebooks, and pages.

#### Basic Form View Structure
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

#### Form View Attributes
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

#### Form Layout Components Hierarchy

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

### Kanban View

Kanban views display records as cards with drag-and-drop functionality.

#### Basic Kanban View Structure
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

#### Kanban View Attributes
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

#### Kanban Card Template
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
### Role-Based View Actions
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
### Field-Level Permissions in Views
```json
{
  "type": "field",
  "attrs": {
    "name": "salary",
    "roles": ["Admin", "HR"],       // Who can view this field
  }
}
```

### View Widgets (TODO)
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

### View Event Handlers (TODO)
Views support event handlers to execute custom logic at various stages of the view lifecycle. We can write custom handlers in our project which react to these events and modify view behavior dynamically.

#### Event Handler Types
- `onFormLayoutLoad`: Executed when form loads
- `onFormDataLoad`: Executed after form data is loaded
- `onFieldChange`: Triggered on field value changes
- `onFormSubmit`: Executed before form submission
- `onViewLoad`: Executed when view loads

### View Layout Responsive Design

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

#### 📖 Further Reference

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

### Layout Organization
1. **Use logical grouping**: Group related fields in columns with descriptive labels
2. **Progressive disclosure**: Use tabs (notebooks) for complex forms
3. **Responsive design**: Use appropriate grid classes for different screen sizes
4. **Field ordering**: Place important fields first, follow logical workflow

### Security Considerations
1. **Role-based access**: Configure view actions based on user roles
2. **Field-level security**: Hide sensitive fields from unauthorized users
3. **Audit trails**: Enable audit tracking for sensitive operations

### Performance Optimization
1. **Pagination**: Always enable pagination for large datasets
2. **Field selection**: Only display necessary fields in list views