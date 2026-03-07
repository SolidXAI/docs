---
sidebar_position: 1
title: Built-in Selection Providers
description: Learn about the built-in selection providers available in SolidX — ListOfValuesSelectionProvider and PseudoForeignKeySelectionProvider.
summary: Documents the two built-in dynamic selection providers shipped with SolidX. ListOfValuesSelectionProvider populates dropdowns from List of Values (LOV) metadata entries filtered by type, while PseudoForeignKeySelectionProvider fetches options from any existing model to create lightweight foreign-key-style relationships without a formal database relation. Covers context configuration, field metadata examples, and search/query behaviour for both providers.
keywords: [backend, dynamic selection, providers, built-in, list of values, pseudo foreign key]
solidx_concerns: [dynamic_selection_provider]
---

import { IoIosArrowForward } from "react-icons/io";
import { FaLightbulb } from "react-icons/fa";
import { InfoBox } from '@site/src/common/InfoBox';
import { NoteBoxs } from '@site/src/common/NoteBoxs';


# Built-in Selection Providers

SolidX ships with two built-in dynamic selection providers so you can wire up common dropdown patterns without writing any code.
If you need something more advanced, see [Dynamic Selection Providers](../backend-customization/dynamic-selection-providers) for creating your own.

| Provider | Use case |
|---|---|
| `ListOfValuesSelectionProvider` | Populate a dropdown from [List of Values](../../metadata_schema/list-of-values.md) metadata entries |
| `PseudoForeignKeySelectionProvider` | Populate a dropdown from records in **any existing model**, creating a lightweight foreign-key-style relationship without a formal database relation |

---

## ListOfValuesSelectionProvider

Use this provider when the options for a field come from your **List of Values** metadata.
It filters LOV entries by `type` and maps each entry's `display` to the label and `value` to the stored value.

### Context

The context object passed via `selectionDynamicProviderCtxt` accepts:

| Key | Type | Required | Description |
|---|---|---|---|
| `type` | `string` | Yes | The LOV type to filter by (e.g. `"REGULATED_BY"`, `"INDUSTRY"`) |

### Field Metadata Example

<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Example: Dynamic selection field using <code>ListOfValuesSelectionProvider</code>
</summary>

```json
{
  "name": "regulatedBy",
  "displayName": "Regulated By",
  "description": "Regulated By",
  "type": "selectionDynamic",
  "ormType": "varchar",
  "isSystem": false,
  // highlight-start
  "selectionDynamicProvider": "ListOfValuesSelectionProvider",
  "selectionDynamicProviderCtxt": "{\"type\": \"REGULATED_BY\"}",
  // highlight-end
  "selectionValueType": "string",
  "required": false,
  "unique": false,
  "index": false,
  "private": false,
  "encrypt": false,
  "isUserKey": false,
  "enableAuditTracking": true,
  "isMultiSelect": true
}
```

</details>

### How It Works

1. SolidX reads the `selectionDynamicProviderCtxt` and extracts the `type` value.
2. The provider queries the internal `ListOfValuesService` with a filter of `type = <your type>`.
3. If the user types a search query in the dropdown, the provider additionally filters by `display` (case-insensitive contains).
4. Each matching LOV record is mapped to `{ label: record.display, value: record.value }` and returned to the UI.

<InfoBox>
  The LOV entries themselves are defined in your module's metadata file under the key <code>listOfValues</code> key. See the <a href="../../metadata_schema/list-of-values.md">List of Values metadata schema</a> for details on how to define them.
  <br/>
  You can also refer to <a href="../../../admin-docs/settings#list-of-values">Configuring List of Values</a> for instructions on how to manage LOV entries via the admin UI.
</InfoBox>

---

## PseudoForeignKeySelectionProvider

Use this provider when you want a dropdown whose options come from **records in another model** — without creating a formal database foreign key relationship.
This is useful for loosely-coupled references where a full relation is overkill or the models live in different modules.

<InfoBox>
  Use <code>PseudoForeignKeySelectionProvider</code> when you need to link data from a <strong>co-model</strong> (or any other model) to your current model but you <strong>cannot or don't want to create an actual database relation</strong> between them.
  <br/>
  <strong>Example scenario:</strong> Suppose you have a <code>customer</code> model in one module and a <code>country</code> model in another. You want the user to pick a country when creating a customer, but you don't want a formal foreign key — perhaps because the models are managed by different teams, the <code>country</code> data is reference-only, or you simply want to store the country code as a plain string rather than enforce referential integrity. With this provider you can populate a dynamic dropdown from the <code>country</code> model's records while keeping the two models completely decoupled at the database level.
</InfoBox>

### Context

The context object passed via `selectionDynamicProviderCtxt` accepts:

| Key | Type | Required | Description |
|---|---|---|---|
| `modelName` | `string` | Yes | The name of the model to query (e.g. `"country"`) |
| `labelFieldName` | `string` | Yes | The field on the target model to use as the **display label** |
| `valueFieldName` | `string` | Yes | The field on the target model to use as the **stored value** |
| `whereClauseFields` | `string[]` | Yes | Fields on the target model to search against when the user types a query |

<NoteBoxs>
  The provider also respects the standard <code>limit</code> and <code>offset</code> context properties for pagination.
</NoteBoxs>

### Field Metadata Example

<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Example: Dynamic selection field using <code>PseudoForeignKeySelectionProvider</code>
</summary>

```json
{
  "name": "countryOfIncorporation",
  "displayName": "Country of Incorporation",
  "description": "Select the country of incorporation",
  "type": "selectionDynamic",
  "ormType": "varchar",
  "isSystem": false,
  // highlight-start
  "selectionDynamicProvider": "PseudoForeignKeySelectionProvider",
  "selectionDynamicProviderCtxt": "{\"modelName\": \"country\", \"labelFieldName\": \"countryName\", \"valueFieldName\": \"countryCode\", \"whereClauseFields\": [\"countryName\", \"countryCode\"]}",
  // highlight-end
  "selectionValueType": "string",
  "required": true,
  "unique": false,
  "index": false,
  "private": false,
  "encrypt": false,
  "isUserKey": false,
  "enableAuditTracking": true,
  "isMultiSelect": false
}
```

</details>

### How It Works

1. SolidX reads the `selectionDynamicProviderCtxt` and extracts `modelName`, `labelFieldName`, `valueFieldName`, and `whereClauseFields`.
2. The provider uses `SolidIntrospectService` to look up the CRUD service for the specified model at runtime.
3. If the user types a search query, the provider builds an `$or` filter across all `whereClauseFields` using case-insensitive contains (`$containsi`).
4. The matching records are mapped to `{ label: record[labelFieldName], value: record[valueFieldName] }` and returned to the UI.

<div className="tips-box">
  <h4 className="card-headear-wrapper">
    <FaLightbulb className="feature-icon" />
    When to use which?
  </h4>

- Use **`ListOfValuesSelectionProvider`** when your options are a fixed, admin-managed set defined in metadata (e.g. statuses, categories, industries).
- Use **`PseudoForeignKeySelectionProvider`** when your options come from **live records** in another model (e.g. countries, clients, products).
- If neither fits, [create a custom dynamic selection provider](../backend-customization/dynamic-selection-providers).
</div>
