---
sidebar_position: 2
---

import { FiSearch, FiFilter, FiArrowUp, FiList,FiUserCheck, FiSettings} from "react-icons/fi";
import { CiImport,CiExport } from "react-icons/ci";
import { MdAttractions,MdViewModule,MdFilterList } from "react-icons/md";

# Kanban View

The Kanban View in SolidX is a powerful, metadata-driven interface that presents model records in a kanban format. It is auto-generated based on the model and field definitions and is fully configurable through a structured JSON layout.

This view supports robust features such as searching, filtering, sorting, pagination, data import/export, and custom actions—making it ideal for managing large collections of data with ease and flexibility.

## Key Features

 <div className="card-headear-wrapper">
<FiSearch size={25}  style={{ marginRight: "2px"}} />
    
###  Search
</div>

Enabled via enableGlobalSearch: true, this allows users to search across multiple searchable fields quickly. Fields marked with isSearchable: true participate in this feature.

<!-- ![Global Search](/img/admin-docs/modules/kanban-view-global-search.png) -->

After applying the search it is visible in the search box, if search is applied on multiple fields then this results in an automatic AND clause being applied between the fields on which the search was applied.

<!-- ![Search Applied](/img/admin-docs/modules/list-view-global-search-applied.png) -->
<div className="card-headear-wrapper">
<FiFilter size={26}  style={{ marginRight: "2px"}} />
    
###  Filtering
</div>

Each field type supports type-specific filters:

Eg.
- <span className="white-color"><strong>Numeric : </strong></span> greater than, less than, between
- <span className="white-color"><strong>Date/Time : </strong></span> before, after, between, today, last X days
- <span className="white-color"><strong>Selection : </strong></span> is one of, is not one of
- <span className="white-color"><strong>Boolean : </strong></span> true, false
- <span className="white-color"><strong>Text : </strong></span> contains, does not contain


To open the filter dialog you need to click on "Custom Filter" in the drop down that opens after clicking the "lens" icon or when applying Search.

You can form an arbitrarily complex filter using the available fields.

![Filter Applied](/img/admin-docs/modules/kanban-view-filter-applied.png)

TODO: Below table summarises the different operators available against each field type.

| Field Type  | Available Operators                                                                                                                                                                   |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Integer     | <ul><li>Equals</li><li>Not Equals</li><li>Less Than</li><li>Less Than Or Equal</li><li>Greater Than</li><li>Greater Than Or Equal</li><li>In</li><li>Not In</li><li>Between</li></ul> |
| Big Integer | Same as Integer                                                                                                                                                                       |
| Decimal     | Same as Integer                                                                                                                                                                       |
| Short Text  | <ul><li>Starts With</li><li>Contains</li><li>Not Contains</li><li>Ends With</li><li>Equals</li><li>Not Equals</li><li>In</li><li>Not In</li></ul>                                     |
| ...         | ...                                                                                                                                                                                   |
| ...         | ...                                                                                                                                                                                   |
| ...         | ...                                                                                                                                                                                   |

<div className="card-headear-wrapper">
  <FiArrowUp size={28} style={{ marginRight: "2px"}} />
    
### Sorting
</div>

Enable sorting per field using sortable: true. Clicking column headers toggles ascending/descending order.

<div className="card-headear-wrapper">
  <FiList size={28} style={{ marginRight: "2px"}} />
    
### Pagination
</div>

Paginate large datasets efficiently with options to set default and allowed pageSizeOptions. Server-side pagination is supported for performance on large datasets.

<div className="card-headear-wrapper">
  <CiExport size={28} style={{ marginRight: "2px"}} />
    
### Export
</div>

Data can be exported in standard formats such as CSV or Excel. This allows external analysis or record-keeping. The export functionality is completely dynamic and metadata driven based on how you have configured your model & fields.

The export functionality works exactly as explained on the [List View](./list-view.md#export) section

<div className="card-headear-wrapper">
  <CiImport size={28} style={{ marginRight: "2px"}} />
    
### Import
</div>

Users can import records in bulk via structured files. Field mapping, validations, and error handling are supported out of the box. The import functionality is completely dynamic and metadata driven based on how you have configured your model & fields.

The import functionality works exactly as explained on the [List View](./list-view.md#import) section

<div className="card-headear-wrapper">
  <MdAttractions size={28} style={{ marginRight: "2px"}} />
    
### Action Buttons
</div>

Standard CRUD actions (create, edit, delete) can be enabled per model via layout attributes. You can also add custom action buttons tied to server-side logic, workflows, or external integrations.

These custom buttons can be added to the list view header or against each row.

TODO: More details can be found on the [Action Buttons Recipe](../../recipes/) page.

TODO: Screenshots pending from Sapphire or anywhere we have action buttons on the list view.

<div className="card-headear-wrapper">
  <MdFilterList size={30} style={{ marginRight: "6px" }} />

### Saved Filters

</div>

The SolidX list view lets you apply custom filters and then save them using saved filters.

The saved filters functionality works exactly as explained on the [List View](./list-view.md#saved-filters) section

<div className="card-headear-wrapper">
  <FiSettings size={26} style={{ marginRight: "2px" }} />

### Change Layout

</div>

You can use the cog wheel in the upper right corner to change which all columns are currently displayed in the list view.

![Saved Filter Step 4](/img/admin-docs/modules/switch-views.png)

<div className="card-headear-wrapper">
  <MdViewModule size={28} style={{ marginRight: "2px" }} />

### Switch Layout

</div>

When configured you can switch between the 2 collection views currently supported by SolidX viz. List & Kanban.

If enabled you will see this option enabled in the "Customize Layout" option that opens after clicking on the cog wheel in the upper right corner.

![Saved Filter Step 4](/img/admin-docs/modules/switch-views.png)

## Related Recipes

1. [Configure Redis Based Exports](../../recipes/):
   All exports in SolidX run in the background, we also have the provision to run large exports as a background job on a queue using our queues abstraction. This recipe talks about how to do this with Redis as the message broker.
2. [Configure Custom Import Instructions](../../recipes/):
3. [Configure A Custom Widget](../../recipes/):
   In this recipe we will see how we can customize the display and behavior of a column in the list view.
4. [Configure Switch Layout](../../recipes/):
   In this recipe we will see how we can enable the list view to enable view switching.
