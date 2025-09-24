---
title : List of Values
description : Metadata schema for defining list of values in SolidX applications.
sidebar_position: 14
---

## Overview
List of Values (LOV) are used to define a set of predefined values that can be used in various parts of the SolidX application, such as dropdowns or selection fields. This helps ensure data consistency and improve user experience.

### Example: List of Values Metadata
<details>
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
</details>

### Example of Dynamic Selection Field using List of Values
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
                        "selectionDynamicProviderCtxt": "{\n  \"type\": \"REGULATED_BY\"\n}",
                        "selectionValueType": "string",
                        "required": false,
                        "unique": false,
                        "index": false,
                        "private": false,
                        "encrypt": false,
                        "encryptionType": null,
                        "decryptWhen": null,
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
:::info
ListOfValuesSelectionProvider is a built-in selection provider that fetches values from the `listOfValues` metadata based on the specified `type`. The `selectionDynamicProviderCtxt` contains a JSON string with the `type` key to filter the LOV entries.
:::

#### 📖 Further Reference
 - 📋 Understanding Dynamic Selection Fields: See [Dynamic Selection Fields Documentation](../../admin-docs/module-builder/field-management#dynamic-selection)

### List of Values Metadata Attributes (TODO)