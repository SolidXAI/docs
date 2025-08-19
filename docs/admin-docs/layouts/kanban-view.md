---
sidebar_position: 2
---

# Kanban View

![Kanban View](/img/admin-docs/layouts/kanban-view.png)

The Kanban View in SolidX is a powerful, metadata-driven interface that presents model records grouped by a specific fields in a Kanban format. It is auto-generated based on the model and field definitions and is fully configurable through a structured JSON layout.

Just like the List View, this is also a collection view hence this view supports robust features such as searching, filtering, sorting, pagination, data import/export, and custom actions—making it ideal for managing large collections of data with ease and flexibility. Over and above everything the list view provides, the Kanban view allows one to group the data on a field. The SolidX backend automatically manages grouping creating one swimlane for each distinct group value, the Kanban view is scalable in that it allows you to do pagination within each swimlane, and also if the unique number of groups is very large then pagination against the actual groups also.

## JSON Layout

The Kanban view is defined using a JSON layout that is automatically generated when a new model is created. This layout describes how fields should be displayed and interacted with on the Kanban view interface.

Here's an example layout for a model named Book:

```
{
  "type": "kanban",
  "attrs": {
    "swimlanesCount": 5,
    "recordsInSwimlane": 10,
    "enableGlobalSearch": true,
    "create": true,
    "edit": true,
    "delete": true,
    "groupBy": "status",
    "draggable": true,
    "allowedViews": [
      "list",
      "kanban"
    ]
  },
  "children": [
    {
      "type": "card",
      "attrs": {
        "name": "Card"
      },
      "children": [
        {
          "type": "row",
          "attrs": {
            "name": "row-1",
            "label": "",
            "className": "row"
          },
          "children": [
            {
              "type": "column",
              "attrs": {
                "name": "col-1",
                "label": "",
                "className": "col-12"
              },
              "children": [
                {
                  "type": "field",
                  "attrs": {
                    "name": "bannerImage",
                    "kanbanImagePreviewClassname": "book-kanban-image-preview"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "title",
                    "className": "text-xl",
                    "isSearchable": true
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "isbn",
                    "label": "ISBN",
                    "className": "text-sm"
                  }
                }
              ]
            }
          ]
        },
        {
          "type": "row",
          "attrs": {
            "name": "row-2",
            "label": "",
            "className": "row"
          },
          "children": [
            {
              "type": "column",
              "attrs": {
                "name": "col-1",
                "label": "",
                "className": "col-12"
              },
              "children": [
                {
                  "type": "field",
                  "attrs": {
                    "name": "pageCount",
                    "label": "Page Count"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "totalCopies",
                    "label": "totalCopies"
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
```

###  Kanban View Attributes
| Attribute              | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| swimlanesCount         | Number of swimlanes (columns) to display in the Kanban board.               |
| recordsInSwimlane      | Number of cards shown per swimlane before scrolling.                        |
| enableGlobalSearch     | Enables global search across all fields in the Kanban view.                 |
| create                 | Displays a button to add new cards (records).                               |
| edit                   | Enables card editing functionality.                                         |
| delete                 | Enables deleting cards from the Kanban board.                               |
| groupBy                | Field name by which the records will be grouped into swimlanes (e.g., `status`). |
| draggable              | Enables drag-and-drop of cards between swimlanes.                           |
| allowedViews           | View modes the user can toggle between (e.g., `kanban`, `list`).            |

###  Layout Elements
These are the layout elements one can use as children of the Kanban view.

| Element Type | Attribute                  | Description                                                                 |
|--------------|----------------------------|-----------------------------------------------------------------------------|
| card         | name                       | Optional name/identifier of the card.                                       |
| row          | name                       | Identifier for the row within the card.                                     |
| row          | className                  | CSS class applied to the row container.                                     |
| column       | name                       | Identifier for the column inside a row.                                     |
| column       | className                  | CSS class (e.g., `col-12` for full width).                                  |
| field        | name                       | Name of the data field to display (e.g., `title`, `isbn`, `pageCount`).     |
| field        | label                      | Label displayed for the field. Optional; defaults to field name.            |
| field        | className                  | CSS class to control field appearance (e.g., `text-xl`, `text-sm`).         |
| field        | kanbanImagePreviewClassname | Optional CSS class to style image preview in the Kanban card.              |
| field        | isSearchable               | If true, includes the field in global search.                               |

###  Nested Displays
Kanban views allow deep nesting of UI components to structure the card layout visually.

1. **card**: Top-level container for a single record in the Kanban.
2. **row**: Used to define horizontal sections inside the card.
3. **column**: Placed inside a row to divide horizontal space.
4. **field**: Placed inside a column to render individual data points.

 Example nesting structure:
card → row → column → field(s)

This allows building responsive card layouts using grid-style divisions (e.g., Bootstrap-style `col-12`, `col-6`, etc.).

TODO: More details on all the different layout elements one can use in the Kanban View to be added here...

## Key Features 

### Search 

Enabled via enableGlobalSearch: true, this allows users to search across multiple searchable fields quickly. Fields marked with isSearchable: true participate in this feature.

More details can be found on the [Kanban View](../modules/kanban-view.md) page.

<!-- ![Global Search](/img/admin-docs/layouts/list-view-global-search.png) -->

### Filtering

Each field type supports type-specific filters:

Eg. 
- Numeric: greater than, less than, between
- Date/Time: before, after, between, today, last X days
- Selection: is one of, is not one of
- Boolean: is true, is false
- Text: contains, does not contain

More details can be found on the [Kanban View](../modules/kanban-view.md) page.

### Sorting

Enable sorting per field using sortable: true. Clicking column headers toggles ascending/descending order.

More details can be found on the [Kanban View](../modules/kanban-view.md) page.

### Pagination

Paginate large datasets efficiently with options to set default and allowed pageSizeOptions. Server-side pagination is supported for performance on large datasets.

More details can be found on the [Kanban View](../modules/kanban-view.md) page.

### Export

Data can be exported in standard formats such as CSV or Excel. This allows external analysis or record-keeping.

More details can be found on the [Kanban View](../modules/kanban-view.md) page.

### Import

Users can import records in bulk via structured files. Field mapping, validations, and error handling are supported out of the box.

More details can be found on the [Kanban View](../modules/kanban-view.md) page.

### Action Buttons 

Standard CRUD actions (create, edit, delete) can be enabled per model via layout attributes. You can also add custom action buttons tied to server-side logic, workflows, or external integrations.

These custom buttons can be added to the list view header or against each row. 

TODO: More details can be found on the [Kanban Action Buttons Recipe](../../recipes/) page.

### Impact of Roles

Roles can be used to control the display of columns and action buttons on the list view. 

The default buttons viz. create, edit & delete aswell as custom header or row actions can be controlled such that they are rendered only if the currently logged in user has that role.

For example in the below layout, the column "publisher" will be visible only to users who have the role admin or super-admin.

```
{
  "type": "list",
  "attrs": {
    "pagination": true,
    "pageSizeOptions": [10, 25, 50],
    "enableGlobalSearch": true,
    "create": true,
    "edit": true,
    "delete": true,
    "allowedViews": ["list", "kanban"]
  },
  "children": [
    ...
    ...
    ...
    {
      "type": "field",
      "attrs": {
        "name": "title",
        "sortable": true,
        "isSearchable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "publisher",
        "sortable": true,
        "isSearchable": true,
        "roles": ["admin", "super-admin"]
      }
    },
    ...
    ...
    ...
  ]
}

```

TODO: More details can be found on the [Controlling List View With Roles](../../recipes/) page.


## Field Rendering

TODO: Point to developer documentation, each element of type: "field" in the List View layout can be extensively customized through its attrs object. Please refer the developer documentation to view details about each attribute.

### Custom Cell Templates

One of the most powerful customization points is the ability to control how a field's cell is rendered using a custom view widget.

```
{
  "type": "field",
  "attrs": {
    "name": "title",
    "label": "Title",
    "sortable": true,
    "isSearchable": true,
    "viewWidget": "CustomTitleRenderer"
  }
}
```

- viewWidget refers to a React component.
- This component must conform to a predefined interface (props, value, rowData, etc.).
- You can use this to render:
  - Images
  - Icons
  - Tags
  - Links
  - Badges
  - Custom logic or formatting

SolidX provides a default widget for each field type (e.g., Boolean → toggle icon, Media → image preview). Developers can override these defaults globally or per field.

TODO: More on this in the developer documentation & recipes [Custom View Widget](../../recipes/).

## Metadata Driven

The Kanban View automatically adapts to each field's semantic metadata. 

For example:

- Password fields are masked
- Relation fields display the userkey field of the related record.
- Audit-tracked fields may have change indicators or badges.
- Private fields are excluded from the view entirely unless specifically enabled.
- image fields are rendered with a thumbnail of the image.

Changing the JSON layout changes the list view.

This means that without writing a single line of code, your Kanban View remains consistent, secure, and tailored to your data model.

- The JSON layout is editable via the Layout Designer or programmatically.
- Developers can extend core behavior via plugin hooks or lifecycle methods.
- Actions, filters, and UI components can be customized per project or reused across modules.


## Generated Code

When a new model is created, SolidX automatically creates a new layout JSON that is stored in the ss_view_metadata table. 

TODO: More details on this can be found in the developer documentation section.

## Related Recipes
- [Adding Custom Action Buttons](../../recipes/): <br />
   This recipe talks about how you can add custom action buttons to the list view header and rows.
- [Custom View Widget](../../recipes/): <br />
   This recipe talks about how you can create a custom view widget to control how a field is rendered in the list view.
- [Controlling Kanban View With Roles](../../recipes/): <br />
   This recipe talks about how you can control various visual aspects of the list view by using roles.


<!-- 
# Kanban View

The Kanban View provides a visual way to manage and track records through different stages or states, perfect for workflow and process management.

## Core Features

### Board Configuration
- **Columns**:
  - Dynamic column creation
  - Column reordering
  - Column limits
  - Column colors
- **Cards**:
  - Customizable card layout
  - Card colors and badges
  - Quick edit functionality
  - Drag and drop between columns

### Data Organization
- **Grouping**:
  - Group by any field
  - Collapsible groups
  - Group statistics
  - Custom group ordering
- **Filtering**:
  - Quick filters
  - Advanced filter builder
  - Saved filter presets
  - Dynamic filter updates

### Data Management
- **Import/Export**:
  - Bulk card creation
  - Data export to CSV/Excel
  - Board template export
  - Configuration backup
- **Actions**:
  - Custom card actions
  - Bulk operations
  - Automated workflows
  - Status transitions

## Card Configuration

Customize card appearance and behavior through JSON configuration:

```json
{
  "card": {
    "header": {
      "field": "title",
      "style": {
        "fontSize": "16px",
        "fontWeight": "bold"
      }
    },
    "content": [
      {
        "field": "description",
        "maxLines": 3
      },
      {
        "field": "assignee",
        "type": "avatar"
      },
      {
        "field": "due_date",
        "type": "date",
        "format": "MM/DD/YYYY",
        "color": {
          "overdue": "red",
          "upcoming": "orange",
          "future": "green"
        }
      }
    ],
    "footer": {
      "left": [
        {
          "field": "priority",
          "type": "badge"
        }
      ],
      "right": [
        {
          "field": "comments_count",
          "type": "icon",
          "icon": "comment"
        }
      ]
    }
  },
  "columns": {
    "field": "status",
    "values": [
      {
        "value": "new",
        "label": "New",
        "color": "blue"
      },
      {
        "value": "in_progress",
        "label": "In Progress",
        "color": "orange"
      },
      {
        "value": "completed",
        "label": "Completed",
        "color": "green"
      }
    ]
  }
}
```

## Common Use Cases

### Project Management
- Task tracking
- Sprint planning
- Bug tracking
- Release management

### Sales Pipeline
- Lead management
- Deal tracking
- Customer onboarding
- Account management

### Content Management
- Content workflow
- Review process
- Publishing pipeline
- Asset management

### HR Processes
- Recruitment pipeline
- Employee onboarding
- Performance reviews
- Training programs

## Best Practices

1. **Board Design**
   - Keep columns focused
   - Limit work in progress
   - Use clear column names
   - Consider workflow direction

2. **Card Design**
   - Show relevant information
   - Use visual indicators
   - Keep cards concise
   - Include key metrics

3. **Performance**
   - Limit cards per column
   - Use efficient filters
   - Implement pagination
   - Cache board state

4. **User Experience**
   - Provide clear actions
   - Use consistent colors
   - Enable quick edits
   - Support keyboard shortcuts
 -->