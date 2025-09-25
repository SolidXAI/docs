---
title : Action Metadata
description : Metadata schema for defining actions in SolidX applications.
sidebar_position: 5
---

## Overview
Actions define what happens when users interact with UI elements like menu items, buttons, or links. They connect the frontend to backend functionality and determine how data is displayed or processed.

For a conceptual overview / guide/ recipes of how actions can be used in SolidX, refer to the [Action Guide](../../recipes/actions-menus-guide.md).



### Example: Fee Portal Module Action Metadata
<details>
<summary> Action Schema </summary>
``` json
{
    ..., // Other metadata
    "actions": [
        {
            "displayName": "fees-portal Home",
            "name": "fees-portal-home-action",
            "type": "custom", // Custom action
            "domain": "",
            "context": "",
            "customComponent": "/admin/core/fees-portal/home",
            "customIsModal": true,
            "serverEndpoint": "",
            "viewUserKey": "",
            "moduleUserKey": "fees-portal",
            "modelUserKey": ""
        },
        {
            "displayName": "Institute List Action",
            "name": "institute-list-action",
            "type": "solid", // Standard SolidX action
            "domain": "",
            "context": "",
            "customComponent": "",
            "customIsModal": true,
            "serverEndpoint": "",
            "viewUserKey": "institute-list-view",
            "moduleUserKey": "fees-portal",
            "modelUserKey": "institute"
        },
    ]
}
```
</details>

## Action Metadata Atributes

### `name` *(string, required, unique)*
Name of the action item (column/property).  
**Default:** N/A



### `displayName` *(string, required)*
Display name of the action item (shown in the UI).  
**Default:** N/A



### `type` *(string, required)*
Type of action. Supported types:
- `solid`: Standard SolidX action that interacts with SolidX backend services.
- `custom`: Custom action that uses a custom frontend component. You need to provide the `customComponent` attribute for this type.
**Default:** N/A



### `domain` *(JSON, optional)*
JSON object defining domain-specific parameters for the action.  
**Default:** N/A

--- 

### `context` *(JSON, optional)*
JSON object defining context-specific parameters for the action.  
**Default:** N/A



### `customComponent` *(string, optional)*
Path to the custom frontend component to be used for the action.
**Applies:** Only if `type` is `custom`.
**Default:** N/A



### `customIsModal` *(boolean, optional)*
Indicates if the custom component should be displayed as a modal dialog.
**Applies:** Only if `type` is `custom`.  
**Default:** `false`



### `serverEndpoint` *(string, optional)*
Backend server endpoint to be called for the action.
**Applies:** Only if `type` is `custom`.  
**Default:** N/A    



### `viewUserKey` *(string, optional)*
User key of the view associated with the action.  
**Default:** N/A


### `moduleUserKey` *(string, required)*
User key of the module this action belongs to.  
**Default:** N/A


### `modelUserKey` *(string, required)*
User key of the model this action operates on.  
**Default:** N/A




