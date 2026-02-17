---
sidebar_position: 1
title: List View
---

import { FiSearch, FiFilter, FiArrowUp, FiList,FiUserCheck,FiSettings } from "react-icons/fi";
import { CiImport,CiExport } from "react-icons/ci";
import { MdAttractions,MdFilterList,MdViewModule } from "react-icons/md";
import { IoIosArrowForward } from "react-icons/io";

# List View

The List View in SolidX is a powerful, metadata-driven interface that presents model records in a tabular format. It is auto-generated based on the model and field definitions and is fully configurable through a structured JSON layout.

This view supports robust features such as searching, filtering, sorting, pagination, data import/export, and custom actions—making it ideal for managing large collections of data with ease and flexibility.

## Key Features

  <div className="card-headear-wrapper">
<FiSearch size={25}  style={{ marginRight: "2px"}} />
    
###  Search
</div>

Enabled via enableGlobalSearch: true, this allows users to search across multiple searchable fields quickly. Fields marked with isSearchable: true participate in this feature.

![Global Search](/img/admin-docs/modules/list-view-global-search.png)

After applying the search it is visible in the search box, if search is applied on multiple fields then this results in an automatic AND clause being applied between the fields on which the search was applied.

![Search Applied](/img/admin-docs/modules/list-view-global-search-applied.png)

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

![Filter Applied](/img/admin-docs/modules/list-view-filters.png)

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
  <FiArrowUp size={28}  style={{ marginRight: "2px"}} />
    
###  Sorting
</div>

Enable sorting per field using sortable: true. Clicking column headers toggles ascending/descending order.

<div className="card-headear-wrapper">
  <FiList size={28}  style={{ marginRight: "2px"}} />
    
###  Pagination
</div>

Paginate large datasets efficiently with options to set default and allowed pageSizeOptions. Server-side pagination is supported for performance on large datasets.

<div className="card-headear-wrapper">
  <CiExport size={28}  style={{ marginRight: "2px"}} />
    
###  Export
</div>

Data can be exported in standard formats such as CSV or Excel. This allows external analysis or record-keeping. The export functionality is completely dynamic and metadata driven based on how you have configured your model & fields.

<details open>
  <summary className="card-title card-headear-wrapper ">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Step 1
  </summary>
One can access the export functionality from the cog wheel on the list view

![Export Step 1](/img/admin-docs/modules/export-0.png)

DEV TODO: Make export button access controlled by roles & permissions. We should have a custom permission called export in all models I believe?

</details>

<details open>
  <summary className="card-title card-headear-wrapper ">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Step 2
  </summary>

Based on the models metadata the user can select the fields that they would like to include in the export. This screen has 2 sections Available and Selected. The Selected fields are based on the currently configured list view, so the columns displayed in the list view are by default included in the export.

Also note that all fields are exportable except for media fields. Media fields are skipped as part of the export.

![Export Step 2](/img/admin-docs/modules/export-1.png)

</details>

<details open>
  <summary className="card-title card-headear-wrapper ">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Step 3
  </summary>

One can choose to save this export configuration as a named template to be re-used later.

![Export Step 3](/img/admin-docs/modules/export-2.png)

![Export Step 4](/img/admin-docs/modules/export-3.png)

</details>

<details open>
  <summary className="card-title card-headear-wrapper ">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Step 4
  </summary>

All exports in SolidX run in the background (either as a NodeJS async process) or as a message on a Queue, more on this in the recipes section. After the export is completed the export is available on the export transactions screen.

![Export Step 5](/img/admin-docs/modules/export-4.png)

TODO: Show a screenshot of the export transactions screen and how the user can download it.

</details>

<br/>

<div className="card-headear-wrapper">
  <CiImport size={28}  style={{ marginRight: "2px"}} />
    
###  Import
</div>

Users can import records in bulk via structured files. Field mapping, validations, and error handling are supported out of the box. The import functionality is completely dynamic and metadata driven based on how you have configured your model & fields.

<details open>
  <summary className="card-title card-headear-wrapper ">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Step 1
  </summary>

One can access the import functionality from the cog wheel on the list view.

![Import Step 1](/img/admin-docs/modules/import-0.png)

DEV TODO: Make import button access controlled by roles & permissions. We should have a custom permission called export in all models I believe?

</details>

<details open>
  <summary className="card-title card-headear-wrapper ">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Step 2
  </summary>

As the first step of the import process SolidX provides a pre-built excel template that can be used to import the data. This template is automatically generated based on the model & field metadata.
This screen also displays other instructions around validations etc that will be applied when the excel is imported.

![Import Step 2](/img/admin-docs/modules/import-1.png)
<br/>

![Import Step 3](/img/admin-docs/modules/import-2.png)

</details>

<details open>
  <summary className="card-title card-headear-wrapper ">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Step 3
  </summary>

Here we upload the actual file which is to be imported.

![Import Step 4](/img/admin-docs/modules/import-3.png)

</details>

<details open>
  <summary className="card-title card-headear-wrapper ">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Step 4
  </summary>
Here we provide the mapping for the import, basically fields from the excel header are mapped against fields from SolidX field metadata for this model. 
<br/>
TODO: Mapping screen screenshot is pending.

</details>

<details open>
  <summary className="card-title card-headear-wrapper ">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Step 5
  </summary>

All imports in SolidX run in the background (either as a NodeJS async process) or as a message on a Queue, more on this in the recipes section. After the import is completed the export is available on the import transactions screen.
![Import Step 5](/img/admin-docs/modules/import-4.png)

TODO: Show a screenshot of the import transactions screen and how the user can download it.

</details>

   <br/>

<div className="card-headear-wrapper">
  <MdAttractions size={28}   />
    
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

<details open>
  <summary className="card-title card-headear-wrapper ">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Step 1
  </summary>
Start with choosing a custom filter (or search based filter)

![Saved Filter Step 1](/img/admin-docs/modules/saved-filter-custom-filter.png)

</details>

<details open>
  <summary className="card-title card-headear-wrapper ">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Step 2
  </summary>
Next we click on the cogwheel on the upper right corner, choose "Save Custom Filter", and in the popup that opens give it a name and decide if this is going to be private or not. If marked as private this saved filter is visible only to the user who is creating it.

![Saved Filter Step 2](/img/admin-docs/modules/saved-filter-cog-wheel.png)
<br/>
![Saved Filter Step 3](/img/admin-docs/modules/saved-filter-create.png)

</details>

<details open>
  <summary className="card-title card-headear-wrapper ">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Step 2
  </summary>
After you save the filter it is now available to be applied in the list of saved filters in the dropdown that opens under the search area.

![Saved Filter Step 4](/img/admin-docs/modules/saved-filter-apply-and-view.png)

</details>

<br/>

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
2. [Configure Custom Import Instructions](../../recipes/)
3. [Configure A Custom Widget](../../recipes/): 
   In this recipe we will see how we can customize the display and behavior of a column in the list view.
4. [Configure Switch Layout](../../recipes/):
   In this recipe we will see how we can enable the list view to enable view switching.
