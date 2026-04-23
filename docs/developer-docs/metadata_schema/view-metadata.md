---
title: Views
description: Metadata schema for defining generated UI views in SolidX.
summary: This document explains the current SolidX view model. SolidX UI supports many-record views (`list`, `tree`, `kanban`, and `card`) plus the single-record `form` view. The page explains how to think about view metadata, shows the common metadata shape, and documents the key layout patterns and attributes used by each view type.
sidebar_position: 4
json_pointer: "/views"
jsonpath: "$.views"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#view-metadata-attributes"
solidx_concerns: [update_layout, add_field_to_existing_layout, remove_field_from_existing_layout, modify_layout_field_attribute]
---

# View Metadata
> **Where it lives**  
> **JSON Pointer:** `/views`  
> **JSONPath:** `$.views`  
> **Parent:** Root of the metadata file

## Overview

View metadata is the layer where SolidX turns model metadata into an actual generated UI.

<div className="tips-box information-box">
  <h4 className="card-headear-wrapper">
    Mental Model
  </h4>
  <p>
    Models and fields define what the application knows about. Views define how users see and work with that data.
    You are not hand-building pages here. You are declaring the interaction pattern the generated UI should follow.
  </p>
  <ul>
    <li>Use many-record views when users are browsing, comparing, or moving through collections of records.</li>
    <li>Use single-record views when users are creating, inspecting, or editing one record at a time.</li>
    <li>Think of view metadata as the presentation contract between your domain model and the SolidX UI runtime.</li>
  </ul>
  <p>
    So the intuition is: <strong>view metadata decides how a model becomes a usable screen</strong>.
  </p>
</div>

## Supported View Families

SolidX currently supports the following view types:

### Many-Record Views
- `list`
- `tree`
- `kanban`
- `card`

### Single-Record Views
- `form`

This is the high-level split to keep in mind:

- many-record views are for collections
- single-record views are for one entity instance

## Common View Shape

Every view record follows the same overall structure:

```json
{
  "name": "application-list-view",
  "displayName": "Applications",
  "type": "list",
  "context": "{}",
  "moduleUserKey": "merchant-onboarding",
  "modelUserKey": "application",
  "layout": {
    "type": "list",
    "attrs": {},
    "children": []
  }
}
```

### Common Top-Level Attributes

#### `name`
Internal identifier for the view. This should be unique within the metadata set.

#### `displayName`
Human-friendly label for the view in the generated UI.

#### `type`
The view type. Must be one of:
- `list`
- `tree`
- `kanban`
- `card`
- `form`

#### `context`
JSON-stringified context configuration. In many examples this is simply `"{}"`.

#### `moduleUserKey`
The module the view belongs to.

#### `modelUserKey`
The model the view renders.

#### `layout`
The layout definition for the view. This contains:
- `type`: should match the view type
- `attrs`: view-level behavior and configuration
- `children`: layout nodes, field nodes, or card/form structure depending on the view type

#### Optional Top-Level Hooks
Some views also include additional behavior hooks at the top level.

Examples seen in real metadata:
- `onFieldChange`
- `onFormLayoutLoad`

These are typically used with form-driven workflows where the generated UI needs custom runtime behavior.

## How To Think About Layouts

The layout shape varies by view family:

- `list` and `tree` usually contain `field` children directly
- `card` and `kanban` contain a nested `card` node
- `form` contains a richer hierarchical structure such as `sheet -> notebook -> page -> row -> column -> field`

So while the outer wrapper is consistent, the inner layout tree depends on the interaction pattern you are choosing.

## Many-Record Views

Many-record views are for exploring and acting on collections of records.

### List View

Use `list` when users need a classic tabular experience with search, sorting, pagination, and row-level actions.

#### Typical Shape

```json
{
  "name": "mqMessage-list-view",
  "displayName": "Messages",
  "type": "list",
  "context": "{}",
  "moduleUserKey": "solid-core",
  "modelUserKey": "mqMessage",
  "layout": {
    "type": "list",
    "attrs": {
      "pagination": true,
      "pageSizeOptions": [10, 25, 50],
      "enableGlobalSearch": true,
      "create": false,
      "edit": false,
      "delete": false
    },
    "children": [
      {
        "type": "field",
        "attrs": {
          "name": "messageId",
          "isSearchable": true
        }
      }
    ]
  }
}
```

#### Common `list` Layout Attributes
- `pagination`
- `pageSizeOptions`
- `enableGlobalSearch`
- `create`
- `edit`
- `delete`
- `rowButtons`
- `headerButtons`
- `allowedViews`
- `truncateAfter`

#### Common `list` Child Pattern
`list` layouts typically contain direct `field` children:

```json
{
  "type": "field",
  "attrs": {
    "name": "createdAt",
    "isSearchable": true,
    "sortable": true
  }
}
```

#### Real Patterns Seen In Metadata
- row-level custom actions using `rowButtons`
- top-level actions using `headerButtons`
- view switching using `allowedViews`, for example `["list", "kanban"]` or `["list", "card"]`

### Tree View

Use `tree` when the records are better understood in a hierarchical browsing experience rather than a flat table.

#### Typical Shape

```json
{
  "name": "nbfTransaction-tree-view",
  "displayName": "NBF Transaction",
  "type": "tree",
  "context": "{}",
  "moduleUserKey": "tranaction",
  "modelUserKey": "nbfTransaction",
  "layout": {
    "type": "tree",
    "attrs": {
      "pagination": true,
      "pageSizeOptions": [10, 25, 50],
      "enableGlobalSearch": true,
      "create": true,
      "edit": true,
      "delete": true
    },
    "children": [
      {
        "type": "field",
        "attrs": {
          "name": "status"
        }
      }
    ]
  }
}
```

#### Common `tree` Layout Attributes
- `pagination`
- `pageSizeOptions`
- `enableGlobalSearch`
- `create`
- `edit`
- `delete`

#### Common `tree` Child Pattern
Like `list`, `tree` layouts usually contain direct `field` children.

The difference is not the metadata wrapper so much as the UI presentation mode and the way the records are visualized.

### Card View

Use `card` when a collection should be shown as tiles or cards rather than rows.

This is especially useful for media-heavy or visually-oriented records.

#### Typical Shape

```json
{
  "name": "media-card-view",
  "displayName": "Media Card",
  "type": "card",
  "context": "{}",
  "moduleUserKey": "solid-core",
  "modelUserKey": "media",
  "layout": {
    "type": "card",
    "attrs": {
      "pagination": true,
      "pageSize": 24,
      "pageSizeOptions": [12, 24, 48],
      "enableGlobalSearch": true,
      "create": true,
      "edit": true,
      "delete": true,
      "allowedViews": ["list", "card"]
    },
    "children": [
      {
        "type": "card",
        "attrs": {
          "name": "Card",
          "cardWidget": "MediaCardWidget"
        },
        "children": [
          {
            "type": "field",
            "attrs": {
              "name": "relativeUri",
              "widget": "image",
              "isSearchable": true
            }
          }
        ]
      }
    ]
  }
}
```

#### Common `card` Layout Attributes
- `pagination`
- `pageSize`
- `pageSizeOptions`
- `enableGlobalSearch`
- `create`
- `edit`
- `delete`
- `allowedViews`

#### Common `card` Child Pattern
Unlike `list` and `tree`, a `card` view contains a nested `card` node:

```json
{
  "type": "card",
  "attrs": {
    "name": "Card",
    "cardWidget": "MediaCardWidget"
  },
  "children": [
    {
      "type": "field",
      "attrs": {
        "name": "originalFileName"
      }
    }
  ]
}
```

The nested `card` node is where you define the fields and widget used to render each record tile.

### Kanban View

Use `kanban` when records move through stages, statuses, or workflows and users benefit from a board-style experience.

#### Typical Shape

```json
{
  "name": "application-kanban-view",
  "displayName": "Applications Kanban",
  "type": "kanban",
  "context": "{}",
  "moduleUserKey": "merchant-onboarding",
  "modelUserKey": "application",
  "layout": {
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
      "allowedViews": ["list", "kanban"]
    },
    "children": [
      {
        "type": "card",
        "attrs": {
          "name": "Card",
          "cardWidget": "ApplicationKanbanCardWidget"
        },
        "children": [
          {
            "type": "field",
            "attrs": {
              "name": "displayName",
              "isSearchable": true
            }
          }
        ]
      }
    ]
  }
}
```

#### Common `kanban` Layout Attributes
- `swimlanesCount`
- `recordsInSwimlane`
- `enableGlobalSearch`
- `create`
- `edit`
- `delete`
- `groupBy`
- `draggable`
- `allowedViews`

#### Common `kanban` Child Pattern
Like `card` views, `kanban` uses a nested `card` child.

The key difference is that the surrounding view organizes cards into grouped swimlanes based on `groupBy`.

## Single-Record Views

### Form View

Use `form` when a user is working with a single record at a time, whether creating, editing, reviewing, or progressing a workflow.

#### Typical Shape

```json
{
  "name": "application-form-view",
  "displayName": "Application",
  "type": "form",
  "context": "{}",
  "moduleUserKey": "merchant-onboarding",
  "modelUserKey": "application",
  "onFieldChange": "OnProductTypeChangeHandler",
  "layout": {
    "type": "form",
    "attrs": {
      "name": "form-1",
      "label": "Application",
      "className": "grid",
      "workflowField": "status",
      "workflowFieldUpdateEnabled": false,
      "showAddFormButton": false,
      "formButtons": [
        {
          "attrs": {
            "label": "Send to Checker",
            "action": "ValidateApplication",
            "openInPopup": true,
            "roles": ["Admin", "Maker"]
          }
        }
      ]
    },
    "children": [
      {
        "type": "sheet",
        "attrs": {
          "name": "sheet-1"
        },
        "children": [
          {
            "type": "notebook",
            "attrs": {
              "name": "notebook-1"
            },
            "children": [
              {
                "type": "page",
                "attrs": {
                  "name": "general-info",
                  "label": "General Info"
                },
                "children": [
                  {
                    "type": "row",
                    "attrs": {
                      "name": "row-1"
                    },
                    "children": [
                      {
                        "type": "column",
                        "attrs": {
                          "name": "col-1",
                          "className": "col-6"
                        },
                        "children": [
                          {
                            "type": "field",
                            "attrs": {
                              "name": "displayName"
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

#### Common `form` Layout Attributes
- `name`
- `label`
- `className`
- `workflowField`
- `workflowFieldUpdateEnabled`
- `disabled`
- `readonly`
- `showAddFormButton`
- `showEditFormButton`
- `showDeleteFormButton`
- `formButtons`

#### Common `form` Layout Structure
The most common hierarchy is:

```text
form
  sheet
    notebook
      page
        row
          column
            field
```

You may also see variants such as `group` in some real metadata, but the main idea stays the same: forms are composed as nested layout containers ending in `field` nodes.

#### Real Patterns Seen In Metadata
- workflow-aware forms using `workflowField`
- read-only review screens using `disabled` and `readonly`
- custom action buttons using `formButtons`
- dynamic runtime behavior using top-level hooks such as `onFieldChange` or `onFormLayoutLoad`

## Choosing The Right View Type

Use this rule of thumb:

- choose `list` when the primary need is table-like browsing
- choose `tree` when the same data is better understood hierarchically
- choose `card` when each record should be presented visually as a tile
- choose `kanban` when records move through workflow stages
- choose `form` when the user is working on one record in depth

## Recommended Mental Model

When designing views, think in this order:

1. What is the user's job on this screen: browse many records or work on one record?
2. If it is many records, which interaction pattern fits best: table, hierarchy, cards, or board?
3. Which actions should the generated UI expose directly?
4. Which fields should be visible and searchable in that view?

That sequence usually leads to cleaner metadata decisions than starting with low-level layout details.

## View Metadata Attributes

### Top-Level View Attributes

#### `name`
Unique internal name of the view.

#### `displayName`
Human-readable label shown in the UI.

#### `type`
The view type:
- `list`
- `tree`
- `kanban`
- `card`
- `form`

#### `context`
Serialized view context, commonly `"{}"`.

#### `moduleUserKey`
The owning module.

#### `modelUserKey`
The target model.

#### `layout`
The layout definition, including `type`, `attrs`, and `children`.

#### `onFieldChange` *(optional)*
Runtime handler hook used by some form views.

#### `onFormLayoutLoad` *(optional)*
Runtime handler hook used when the form layout needs custom initialization behavior.

#### Layout Notes By View Type

- `list` and `tree` expect `field` children
- `card` and `kanban` expect a nested `card` child
- `form` expects nested layout containers ending in `field` nodes
