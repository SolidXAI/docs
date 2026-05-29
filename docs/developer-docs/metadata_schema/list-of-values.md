---
title : List of Values
description : Metadata schema for defining list of values in SolidX applications.
summary: This document describes list of values (LOV) metadata in SolidX, which defines predefined value sets for use in dropdowns and selection fields throughout the application. Each LOV entry includes type (category), value (internal identifier), display text (shown to users), description, default flag, sequence number for ordering, and associated module reference. Examples demonstrate configuring industry types (Healthcare, Information Technology) and regulatory bodies (FCA, SEC, PRA, CBI) with proper sequencing. The metadata ensures data consistency, improves user experience, and provides centralized management of commonly used value lists across the application.
sidebar_position: 14
json_pointer: "/listOfValues"
jsonpath: "$.listOfValues"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#list-of-values-metadata-attributes"
solidx_concerns: [add_lov_record]
---

import { InfoBox } from '@site/src/common/InfoBox';


# List of Values
> **Where it lives**  
> **JSON Pointer:** `/listOfValues`  
> **JSONPath:** `$.listOfValues`  
> **Parent:** Root of the metadata file

## Overview
List of Values (LOV) are used to define a set of predefined values that can be used in various parts of the SolidX application, such as dropdowns or selection fields. This helps ensure data consistency and improve user experience.

### Example: List of Values Metadata
Below is an example wherein we define several list of values for different types such as INDUSTRY and REGULATED_BY.

<summary> List of Values Schema </summary>

``` json
{
    ..., // Other metadata sections
    "listOfValues": [
    {
      "type": "INDUSTRY",
      "value": "Healthcare",
      "display": "Healthcare",
      "description": "Industry Healthcare list of value",
      "default": false,
      "sequence": 4,
      "moduleUserKey": "<MODULE_USER_KEY>"
    },
    {
      "type": "INDUSTRY",
      "value": "Information Technology",
      "display": "Information Technology",
      "description": "Industry Information Technology list of value",
      "default": false,
      "sequence": 3,
      "moduleUserKey": "<MODULE_USER_KEY>"
    },
    {
      "type": "REGULATED_BY",
      "value": "FCA",
      "display": "FCA",
      "description": "Regulated by FCA list of value",
      "default": false,
      "sequence": 6,
      "moduleUserKey": "<MODULE_USER_KEY>"
    }
    ]
}
```

### Using the List of Values in Dynamic Selection Fields
To use the defined list of values in your application, you need to reference them by creating a dynamic selection field in your model.

To utilize the defined list of values in a dynamic selection field, you can configure a field in your model to reference the LOV using the `ListOfValuesSelectionProvider`. Below is an example of how to set up a dynamic selection field that pulls values from the `REGULATED_BY` type in the LOV.

``` json
{
    "moduleMetadata": {
        ..., // Module metadata 
        "models": [ // Model metadata array
            { // Institute model metadata
                "singularName": "institute",
                ..., // Other model attributes
                "fields": [ // Institute model fields metadata
                    ..., // Other fields
                    { // Regulated By field metadata
                        "name": "regulatedBy",
                        "displayName": "Regulated By",
                        "description": "Regulated By",
                        "type": "selectionDynamic",
                        "ormType": "varchar",
                        "isSystem": false,
                        "selectionDynamicProvider": "ListOfValuesSelectionProvider",
                        "selectionDynamicProviderCtxt": "{\"type\": \"REGULATED_BY\"}",
                        "selectionValueType": "string",
                        "required": false,
                        "unique": false,
                        "index": false,
                        "private": false,
                        "columnName": null,
                        "isUserKey": false,
                        "enableAuditTracking": true,
                        "isMultiSelect": true
                    }
                ]
            }
        ]
    }
}
```


<InfoBox>
    ListOfValuesSelectionProvider is a built-in selection provider that fetches values from the `listOfValues` metadata based on the specified `type`. The `selectionDynamicProviderCtxt` contains a JSON string with the `type` key to filter the LOV entries.
</InfoBox>

####  Further Reference
 -  Understanding Dynamic Selection Fields: See [Dynamic Selection Fields Documentation](../../admin-docs/module-builder/field-management#dynamic-selection)
 -  Built-in Selection Providers: See [Built-in Selection Providers](../extending/reference/built-in-selection-providers) for full documentation on `ListOfValuesSelectionProvider` and `PseudoForeignKeySelectionProvider`

### List of Values Metadata Attributes


### `type` *(string, required)*
Type/category of the list of values (e.g., INDUSTRY, COUNTRY, STATUS).

### `value` *(string, required)*
The actual value stored in the database.

### `display` *(string, required)*
The display name shown to users in the UI.

### `description` *(string, required)*
A brief description of the list of value.

### `default` *(boolean, optional, default: false)*
Indicates if this value is the default selection.

### `sequence` *(number, optional)*
Defines the order in which the values are displayed.

### `moduleUserKey` *(string, optional)*
The user key of the module to which this list of values is associated. This helps in scoping the LOV to a specific module.
