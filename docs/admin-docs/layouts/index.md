---
sidebar_position: 3
---

# Layout Editor

## Intro

SolidX automatically generates powerful and intuitive UI layouts for each model based on the metadata defined at the module, model, and field levels. These layouts form the core of the user interface and make interacting with data seamless, efficient, and consistent across the platform.

Layouts are generated automatically once a model and its fields are configured. They adapt dynamically to the semantics of each field, ensuring each data type is handled appropriately in both display and interaction contexts.

## Layouts

SolidX supports three primary layout types:

### List View

Is usually used to render a collection of records. 

The List View provides a tabular, grid-like presentation of multiple records in a model. It is ideal for data-dense interfaces where sorting, filtering, and scanning rows quickly is a priority.

### Kanban View

Is usually used to render a collection of records. 

The Kanban View offers a board-style layout that groups records into columns based on a specific field (such as status or category). It’s perfect for workflows, pipelines, and status tracking.

### Form View

Is usually used to render a single of record. The form view serves a dual purpose of allowing users to view and edit the record.

The Form View is used to create or edit a single record. It renders each field with context-aware input controls based on the field type and its metadata (e.g., autocomplete for many-to-one, lists for one-to-many, rich editors for long text or HTML).


## Metadata-Aware Rendering

Each layout leverages the rich metadata attached to models and fields to deliver intelligent and dynamic behavior, below are a few examples (not an exhaustive list) of use-cases where the layouts use the rich metadata to bring type specific behavior.

 Type-Specific Filtering (List & Kanban Views)

Fields are rendered with filter options tailored to their semantic type:

- Numeric fields provide operators like equals, greater than, less than, between, etc.
- Date/Time fields support range filtering, relative dates (e.g., "last 7 days"), and precise date pickers.
- Boolean fields allow filtering by true/false values with toggleable options.
- Selection fields (static or dynamic) offer dropdowns with multiple select support.
- Relation fields support search and filter by linked records.
- And much more...

This allows users to slice, search, and interact with collections in a highly productive way.

 Intelligent Field Rendering (Form View)

In Form Views, each field type is rendered using components optimized for its data and usage context:

- Many-to-One fields use autocomplete dropdowns for efficient record selection.
- One-to-Many and Many-to-Many fields render embedded sub-lists or tabbed interfaces for managing related records.
- File and Media fields include upload interfaces with previews and validations.
- Rich text and long text fields offer contextual editors.
- Date/Time fields use user-friendly pickers with timezone handling.

SolidX ensures the layout is not only functional but also intuitive for users, adapting to both developer configuration and real-world usage needs.

## Extensible & Customizable

Each layout is customizable at the configuration or code level, allowing developers to:

- Customize visible columns or fields.
- Link display of columns or fields with roles assigned to a user.
- Override default sorting or grouping.
- Define custom actions, buttons, or view-specific logic.
- Provide different render modes for existing fields.
- Create completely custom user interfaces.



## Next Steps

Explore each layout in detail to understand its features, configuration options, and extensibility:

- [List View](./list-view.md):
- [Kanban View](./kanban-view.md):
- [Form View](./form-view.md):
