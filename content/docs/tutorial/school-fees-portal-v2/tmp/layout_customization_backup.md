---
title: Layout Customization Backup
---

#### Overview of Layout Customization Capabilities

SolidX provides a powerful JSON-based layout system that allows you to customize both list views and form views without writing code. The layout configuration is stored in the metadata JSON file and supports a hierarchical component structure.

##### Layout Component Hierarchy

The layout system uses a tree structure with the following component types:

**Form Layouts:**
- **form**: The root container for form views
  - **sheet**: Top-level container within a form
    - **notebook**: Tab container for organizing fields into multiple pages
      - **page**: Individual tab within a notebook
        - **row**: Horizontal container for organizing columns
          - **column**: Vertical container with label and CSS classes (e.g., `col-6`, `col-12`)
            - **field**: Individual form field

**List Layouts:**
- **list**: The root container for list/table views
  - **field**: Individual table column with sorting, filtering, and search capabilities

##### Available Configuration Options

**Form Layout Attributes:**

| Component | Attribute | Purpose | Example Values |
|-----------|-----------|---------|----------------|
| **form** | `name` | Unique identifier | `"form-1"` |
| | `label` | Form title | `"Institute"` |
| | `className` | CSS classes | `"grid"` |
| | `formButtons` | Custom action buttons | Array of button configurations |
| | `onFormLoad` | Handler function for form initialization | `"instituteEditHandler"` |
| **page** | `name` | Page identifier | `"page-1"` |
| | `label` | Tab label | `"Institutes"`, `"Payment Gateway Details"` |
| **column** | `name` | Column identifier | `"group-1"` |
| | `label` | Section heading | `"Institutes Basic"`, `"Institutes Contact"` |
| | `className` | Bootstrap grid classes | `"col-6"` (half width), `"col-12"` (full width) |
| | `visible` | Show/hide column | `true`, `false` |
| **field** | `name` | Field name from model | `"instituteName"`, `"logo"` |
| | `visible` | Show/hide field | `true`, `false` |
| | `disabled` | Enable/disable editing | `true`, `false` |
| | `showLabel` | Display field label | `true`, `false` |
| | `showFieldLabel` | Display field label in relations | `true`, `false` |
| | `inlineCreate` | Allow inline creation for relations | `"true"`, `"false"` |
| | `viewWidget` | Custom widget for view mode | `"maskedShortTextForm"` |
| | `editWidget` | Custom widget for edit mode | `"maskedShortTextEdit"` |

**List Layout Attributes:**

| Attribute | Purpose | Example Values |
|-----------|---------|----------------|
| **pagination** | Enable pagination | `true`, `false` |
| **pageSizeOptions** | Rows per page options | `[10, 25, 50]` |
| **enableGlobalSearch** | Enable search across all fields | `true`, `false` |
| **create** | Show create button | `true`, `false` |
| **edit** | Show edit button | `true`, `false` |
| **delete** | Show delete button | `true`, `false` |
| **configureViewActions** | Role-based action permissions | Object with action-role mappings |

**Field Attributes (List View):**

| Attribute | Purpose | Example |
|-----------|---------|---------|
| **name** | Field name from model | `"instituteName"` |
| **sortable** | Enable column sorting | `true`, `false` |
| **filterable** | Enable column filtering | `true`, `false` |
| **isSearchable** | Include in search | `true`, `false` |
| **label** | Custom column header | `"Institute Name"` |
| **coModelFieldToDisplay** | Field to display for relations | `"instituteName"` |