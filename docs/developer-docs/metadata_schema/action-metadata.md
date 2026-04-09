---
title: Actions
description: Metadata schema for defining actions in SolidX applications.
summary: This document defines action metadata in SolidX, which determines what happens when users interact with UI elements like menu items, buttons, or links. Actions connect the frontend to backend functionality and control how data is displayed or processed. The metadata supports two main action types - solid (standard SolidX actions linked to views) and custom (custom component actions with optional modal display). Key attributes include action name, display name, type, domain, context, custom component path, server endpoint, associated view, module, and model. Actions serve as the bridge between user interactions and application responses.
sidebar_position: 5
json_pointer: "/actions"
jsonpath: "$.actions"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#action-metadata-attributes"
solidx_concerns: [add_custom_menu_action_combo]
---
import { IoIosArrowForward } from "react-icons/io";
import { MdEmail } from "react-icons/md";
import { InfoBox } from '@site/src/common/InfoBox';
import { MdOutlineAssignment } from "react-icons/md";


# Action Metadata
> **Where it lives**  
> **JSON Pointer:** `/actions`  
> **JSONPath:** `$.actions`  
> **Parent:** Root of the metadata file

## Overview
Actions define what happens when users interact with UI elements like menu items, buttons, or links. They connect the frontend to backend functionality and determine how data is displayed or processed.

Menus, buttons, and links in SolidX applications are associated with actions.

When a user clicks on one of these UI elements, the corresponding action is triggered, executing the defined behavior.

Key Configuration Points:

1. **Module and View Association**: All actions need to be linked to a module and a view.

2. **Solid Actions**: In case of solid actions, the view user key and model user key is required. Since solid actions are generally linked to standard SolidX views, no custom component path is needed. In case of custom actions, a custom component path i.e (the linked view) is required. 

3. **Custom Actions**: Custom actions can optionally be displayed as modal dialogs. If the action is a custom action, the `customComponent` attribute must be provided to specify the path to the custom frontend component. The `customIsModal` attribute indicates if the component should be displayed as a modal dialog.

:::note
In case a custom action is not associated with a model, the model user key can be left blank.
:::

### Action Types
1. **Solid Actions**: Standard CRUD operations using SolidX's built-in views
2. **Custom Actions**: Custom components or pages with specific functionality

### Configuration Examples

### `Solid` Action Example
Below is an example of a `solid` action configuration, which links to a standard SolidX view for listing institutes.
<details open>
<summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
 Click to expand
</summary>
```json
{
    ..., // Other metadata
    "actions": [
        {
            "displayName": "Institute List View",      // User-friendly action name
            "name": "institute-list-view",             // Internal action reference (kebab-case)
            "type": "solid",                           // Action type: solid, custom
            "domain": "",                              // Domain context (optional)
            "context": "",                             // Additional configuration (optional)
            "customComponent": "",                     // UI route path
            "customIsModal": true,                     // Display as modal dialog
            "serverEndpoint": "",                      // Feature to be implemented
            "viewUserKey": "institute-list-view",      // Target view reference
            "moduleUserKey": "fees-portal",            // Module this action belongs to
            "modelUserKey": "institute"                // Model for standard actions
        },
        ... // Other actions
    ]
}
```
</details>

### `Custom` Action Example
Below is an example of a `custom` action configuration, which links to a custom frontend component for the fees portal home page.
<details open>
<summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
 Click to expand
  </summary>
```json
{
    ..., // Other metadata
    "actions": [
        {
            "displayName": "Fees Portal Home",
            "name": "fees-portal-home-action",
            "type": "custom", // Custom action
            "domain": "",
            "context": "",
            "customComponent": "/admin/core/fees-portal/home", // Required for custom actions
            "customIsModal": true,
            "serverEndpoint": "", // Feature to be implemented
            "viewUserKey": "",
            "moduleUserKey": "fees-portal",
            "modelUserKey": ""
        },
        ... // Other actions
    ]
}
``` 
</details>

## Complete Navigation Structure Example

Here's a complete navigation structure example from the fees-portal, illustrating how menus and actions are defined together:
<details open>
<summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
 Click to expand
  </summary>

```json
{
  "menus": [
    {
      "displayName": "Home",
      "name": "fees-portal-home-menu",
      "sequenceNumber": 1,
      "actionUserKey": "fees-portal-home-action"
    },
    {
      "displayName": "Institute",
      "name": "institute-menu-item",
      "sequenceNumber": 2,
      "actionUserKey": "institute-list-action",
      "roles": ["Institute Admin", "App Admin"]
    },
    ... // Additional menus
  ],
  "actions": [
    {
      "displayName": "fees-portal Home",
      "name": "fees-portal-home-action",
      "type": "custom",
      "customComponent": "/admin/core/fees-portal/home",
      "customIsModal": true,
      "moduleUserKey": "fees-portal"
    },
    {
      "displayName": "Institute List Action",
      "name": "institute-list-action",
      "type": "solid",
      "customComponent": "",
      "customIsModal": true,
      "viewUserKey": "institute-list-view",
      "modelUserKey": "institute",
      "moduleUserKey": "fees-portal",
    }
    // ... Additional actions
  ]
}
```
</details>

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




