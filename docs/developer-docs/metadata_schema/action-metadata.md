---
# title : Action Metadata
description : Metadata schema for defining actions in SolidX applications.
summary: This document defines action metadata in SolidX, which determines what happens when users interact with UI elements like menu items, buttons, or links. Actions connect the frontend to backend functionality and control how data is displayed or processed. The metadata supports two main action types: 'solid' (standard SolidX actions linked to views) and 'custom' (custom component actions with optional modal display). Key attributes include action name, display name, type, domain, context, custom component path, server endpoint, associated view, module, and model. Actions serve as the bridge between user interactions and application responses.
sidebar_position: 5
json_pointer: "/actions"
jsonpath: "$.actions"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#action-metadata-attributes"
solidx_concerns: [add_custom_menu_action_combo]
---

import { MdOutlineAssignment } from "react-icons/md";


# Action Metadata
> **Where it lives**  
> **JSON Pointer:** `/actions`  
> **JSONPath:** `$.actions`  
> **Parent:** Root of the metadata file

## Overview
Actions define what happens when users interact with UI elements like menu items, buttons, or links. They connect the frontend to backend functionality and determine how data is displayed or processed.

For a conceptual overview / guide/ recipes of how actions can be used in SolidX, refer to the [Action Guide](../../recipes/actions-menus-guide.md).



### Example: Fee Portal Module Action Metadata
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

<h2 className=" card-headear-wrapper">
    <MdOutlineAssignment size={24} style={{ marginRight: "10px" }} />

## Action Metadata Atributes
</h2>


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




