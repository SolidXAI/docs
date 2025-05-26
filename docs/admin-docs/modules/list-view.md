---
sidebar_position: 3
---

# List View

The List View in SolidX is a powerful, metadata-driven interface that presents model records in a tabular format. It is auto-generated based on the model and field definitions and is fully configurable through a structured JSON layout.

This view supports robust features such as searching, filtering, sorting, pagination, data import/export, and custom actions—making it ideal for managing large collections of data with ease and flexibility.

## Key Features 

### Search 

Enabled via enableGlobalSearch: true, this allows users to search across multiple searchable fields quickly. Fields marked with isSearchable: true participate in this feature.

![Global Search](/img/admin-docs/layouts/list-view-global-search.png)

After applying the search it is visible in the search box, if search is applied on multiple fields then this results in an automatic AND clause being applied between the fields on which the search was applied.

![Search Applied](/img/admin-docs/layouts/list-view-global-search-applied.png)

### Filtering

Each field type supports type-specific filters:

Eg. 
- Numeric: greater than, less than, between
- Date/Time: before, after, between, today, last X days
- Selection: is one of, is not one of
- Boolean: is true, is false
- Text: contains, does not contain

To open the filter dialog you need to click on "Custom Filter" in the drop down that opens after clicking the "lens" icon or when applying Search. 

You can form an arbitrarily complex filter using the available fields.

![Filter Applied](/img/admin-docs/layouts/list-view-filters.png)


TODO: Below table summarises the different operators available against each field type.

| Field Type | Available Operators |
|---------|-------------|
| Integer | <ul><li>Equals</li><li>Not Equals</li><li>Less Than</li><li>Less Than Or Equal</li><li>Greater Than</li><li>Greater Than Or Equal</li><li>In</li><li>Not In</li><li>Between</li></ul> |
| Big Integer | Same as Integer |
| Decimal | Same as Integer |
| Short Text | <ul><li>Starts With</li><li>Contains</li><li>Not Contains</li><li>Ends With</li><li>Equals</li><li>Not Equals</li><li>In</li><li>Not In</li></ul> |
| ... | ... |
| ... | ... |
| ... | ... |


### Sorting

Enable sorting per field using sortable: true. Clicking column headers toggles ascending/descending order.

More details can be found on the [Modules List View](../modules/list-view.md) page.

### Pagination

Paginate large datasets efficiently with options to set default and allowed pageSizeOptions. Server-side pagination is supported for performance on large datasets.

More details can be found on the [Modules List View](../modules/list-view.md) page.

### Export

Data can be exported in standard formats such as CSV or Excel. This allows external analysis or record-keeping.

More details can be found on the [Modules List View](../modules/list-view.md) page.

### Import

Users can import records in bulk via structured files. Field mapping, validations, and error handling are supported out of the box.

More details can be found on the [Modules List View](../modules/list-view.md) page.

### Action Buttons 

Standard CRUD actions (create, edit, delete) can be enabled per model via layout attributes. You can also add custom action buttons tied to server-side logic, workflows, or external integrations.

These custom buttons can be added to the list view header or against each row. 

More details can be found on the [Action Buttons Recipe](../../recipes/) page.

### Saved Filters

### Change Layout 

### Switch Layout 

### Custom View Widget