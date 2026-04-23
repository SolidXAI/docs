---
title: Modules
description: Overview of the module metadata schema used in SolidX.
summary: This document explains the module metadata schema in SolidX, which represents the top-level building blocks for organizing applications. A module groups related models and functionality under a unified domain (like a Fees Portal module). The metadata includes properties such as module name, display name, description, default data source, menu icon, sequence number, and system flag. Examples demonstrate configuring module metadata for applications, and the document references the admin documentation for conceptual understanding of module management and the hierarchical relationship where modules contain models which contain fields.
sidebar_position: 1
json_pointer: "/moduleMetadata"
jsonpath: "$.moduleMetadata"
parent_component: root
items_type: object
items_attributes_doc: "#module-metadata-attributes"
solidx_concerns: [create_module]
---
import { MdCategory } from "react-icons/md";
import { IoIosArrowForward } from "react-icons/io";
import { InfoBox } from '@site/src/common/InfoBox';



#  Module Metadata

> **Where it lives**  
> **JSON Pointer:** `/moduleMetadata`  
> **JSONPath:** `$.moduleMetadata`  
> **Parent:** Root of the metadata file

##  Overview

When creating a new module in SolidX, you're defining a **core building block** of your application.  
A module groups together related models and functionality under a **unified domain**.

<div className="tips-box information-box">
  <h4 className="card-headear-wrapper">
    Mental Model
  </h4>
  <p>
    A module is the top-level business boundary in SolidX. It is not just a folder or namespace. It is the container that tells the platform which models, views, menu entries, and behaviors belong to one domain.
  </p>
  <ul>
    <li>Start by asking: what business capability are we modelling?</li>
    <li>Put closely related models inside the same module.</li>
    <li>Use the module to define the identity of that domain inside the app.</li>
  </ul>
  <p>
    So the intuition is: <strong>a module is the platform's unit of business ownership</strong>.
  </p>
</div>

👉 For a conceptual overview of what a module is, see [Module Management Documentation](../../admin-docs/module-builder/module-management.md).

###  Example: Fees Portal Module
Below is a module metadata example for a "Fees Portal" module that tracks fee collection requests.
<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Module Schema
  </summary>

```json
{
  "moduleMetadata": {
    "name": "fees-portal",
    "displayName": "Fees Portal",
    "description": "Keep track of fees collections requests",
    "defaultDataSource": "default",
    "menuIconUrl": null,
    "menuSequenceNumber": 2,
    "isSystem": false,
    ... // Model and Field metadata goes here
  },
  ... // Other metadata components go here
}
```
</details>


<InfoBox>
  The defaultDataSource is set to "default" here, which refers to the default data source configured in your SolidX instance. This is the TypeORM data source configured in your app-default.database.ts in your project `solid-api` src folder.
</InfoBox>


  <h2 className=" card-headear-wrapper">
    <MdCategory size={24} style={{ marginRight: "10px" }} />

## Module Metadata Attributes
</h2>


### `name` *(string, required, unique)*
Unique identifier for the module (lowercase, underscores/dashes).  
Used internally by the system and in the API (e.g., `"sales"`).  
**Default:** N/A



### `displayName` *(string, required)*
Human-readable name shown in the admin panel’s navigation and UI  
(e.g., `"Sales Management"`).  
**Default:** N/A



### `description` *(string, optional)*
Short summary of what the module represents or its purpose.  
**Default:** N/A



### `defaultDataSource` *(string, optional)*
Default data source (from a predefined list) used to read/write data.  
**Default:** N/A



### `menuSequenceNumber` *(number, optional)*
Order in which the module appears in the sidebar/navigation menu  
(lower numbers appear earlier).  
**Default:** N/A



### `isSystem` *(boolean, required)*
Marks this as a **system module** (cannot be deleted).  
**Default:** `false`



### `menuIconUrl` *(string, optional)*
Path/URL of an icon to represent the module in the navigation pane.  
**Default:** N/A
