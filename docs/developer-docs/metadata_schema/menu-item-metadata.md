---
title: Menu Item Metadata
description: Metadata schema for defining menus in SolidX applications.
sidebar_position: 6
json_pointer: "/menus"
jsonpath: "$.menus"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#menu-item-metadata-attributes"
solidx_concerns: [add_custom_menu_action_combo, add_new_role_with_permission, modify_role]
---

import { MdMenuBook } from "react-icons/md"; 

# Menu Item Metadata
> **Where it lives**  
> **JSON Pointer:** `/menus`  
> **JSONPath:** `$.menus`  
> **Parent:** Root of the metadata file

## Overview
SOLID automatically generates and manages the admin panel's menu structure based on your modules and resources. The menu system provides an intuitive way to navigate through your application's features

For a conceptual overview of menus in SolidX, refer to the [Menu System Overview](../../admin-docs/modules/menu-structure.md).


### Example: Fee Portal Module Menu Metadata
<summary> Menu Schema </summary>

``` json
{
  ..., // Other metadata  
  "menus": [ // Array of menu item metadata
    {
      "displayName": "Home",
      "name": "fees-portal-home-menu",
      "sequenceNumber": 1,
      "actionUserKey": "fees-portal-home-action",
      "moduleUserKey": "fees-portal",
      "parentMenuItemUserKey": "",
      "roles": [],
      "iconName": "home"
    },
    {
      "displayName": "Institute",
      "name": "institute-menu-item",
      "sequenceNumber": 2,
      "actionUserKey": "institute-list-view",
      "moduleUserKey": "fees-portal",
      "parentMenuItemUserKey": "",
      "roles": [
        "Institute Admin",
        "Mswipe Admin"
      ],
      "iconName": "school"
    },
    {
      "displayName": "Initiate Payments",
      "name": "paymentCollection-menu-item",
      "sequenceNumber": 3,
      "actionUserKey": "paymentCollection-list-view",
      "moduleUserKey": "fees-portal",
      "parentMenuItemUserKey": "",
      "roles": [
        "Institute Admin",
        "Mswipe Admin"
      ],
      "iconName": "payments"
    },
    {
      "displayName": "Created Payments",
      "name": "paymentCollectionItem-menu-item",
      "sequenceNumber": 1,
      "actionUserKey": "paymentCollectionItem-list-view",
      "moduleUserKey": "fees-portal",
      "parentMenuItemUserKey": "paymentCollection-menu-item",
      "roles": [
        "Institute Admin",
        "Mswipe Admin"
      ],
      "iconName": "receipt"
    },
  ],
}
```


<h2 className=" card-headear-wrapper">
    <MdMenuBook size={22} style={{ marginRight: "10px" }} />

## Menu Item Metadata Attributes
</h2>



### `name` *(string, required, unique)*
Name of the menu item (column/property).  
**Default:** N/A

--- 

### `displayName` *(string, required)*
Display name of the menu item (shown in the UI).  
**Default:** N/A



### `moduleUserKey` *(string, required)*
User key of the module this menu item belongs to.  
**Default:** N/A



### `parentMenuItemUserKey` *(string, optional)*
User key of the parent menu item (for nested menus).  
If empty or not provided, the menu item is a top-level item.  
**Default:** `""` (empty string)




### `actionUserKey` *(string, optional)*
User key of the action this menu item links to.  
If empty or not provided, the menu item will not link to any action.  
**Default:** `""` (empty string)




### `roles` *(array of Role Metadata, optional)*
Array of roles that can access this menu item.  
If empty or not provided, the menu item is accessible only to the `Admin` role.  
Refer to [Role Metadata](../../admin-docs/iam/roles.md) for details.




### `sequenceNumber` *(number, optional)*
Sequence number for ordering menu items.  
Lower numbers appear first. If empty or not provided, menu items are shown in the order in which they are inserted.
**Default:** N/A




### `iconName` *(string, optional)*
Name of the icon to display alongside the menu item.
Refer to the [Material Icons](https://fonts.google.com/icons?icon.set=Material+Icons) for available icons.  
**Default:** N/A