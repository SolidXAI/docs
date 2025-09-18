---
title: Field Metadata Schema
description: Overview of the field metadata schema used in SolidX.
sidebar_position: 3
---

## Overview

Every SolidX model is composed of fields. Fields in SolidX go over and above the standard fields one expects, instead we treat fields as semantic attributes with relevance to how the users interact with that data in our admin interface. 

👉 For a conceptual overview of fields supported in a model, see [Field Management Documentation](../../admin-docs/module-builder/field-management.md).

---
### Example: Institute + Fee Type Model fields
<details>
<summary>📑 Field Schema</summary>

```json
{
    "moduleMetadata": {
        ..., // Module metadata 
        "models": [ // Model metadata array
            { // Institute model metadata
                "singularName": "institute",
                "pluralName": "institutes",
                "displayName": "Institute",
                "description": "The institute name...",
                "dataSource": "default",
                "dataSourceType": "postgres",
                "tableName": "fees_portal_institute",
                "userKeyFieldUserKey": "instituteName",
                "isChild": false,
                "enableAuditTracking": true,
                "enableSoftDelete": false,
                "draftPublishWorkflow": false,
                "internationalisation": false,
                "fields": [ // Institute model fields metadata
                    {
                        "name": "instituteName",
                        "displayName": "Institute Name",
                        "description": null,
                        "type": "shortText",
                        "ormType": "varchar",
                        "isSystem": false,
                        "defaultValue": null,
                        "min": null,
                        "max": null,
                        "required": true,
                        "unique": true,
                        "index": true,
                        "private": false,
                        "encrypt": false,
                        "encryptionType": null,
                        "decryptWhen": null,
                        "columnName": null,
                        "isUserKey": true,
                        "enableAuditTracking": false
                    },
                    {
                        "name": "logo",
                        "displayName": "Logo",
                        "description": null,
                        "type": "mediaSingle",
                        "ormType": "varchar",
                        "isSystem": false,
                        "mediaTypes": [
                            "image"
                        ],
                        "mediaMaxSizeKb": 5120,
                        "required": true,
                        "unique": false,
                        "index": false,
                        "private": false,
                        "encrypt": false,
                        "encryptionType": null,
                        "decryptWhen": null,
                        "columnName": null,
                        "mediaStorageProviderUserKey": "default-aws-s3"
                    },
                    {
                        "name": "description",
                        "displayName": "Description",
                        "description": null,
                        "type": "longText",
                        "ormType": "text",
                        "isSystem": false,
                        "regexPattern": "",
                        "regexPatternNotMatchingErrorMsg": "",
                        "defaultValue": null,
                        "min": null,
                        "max": null,
                        "required": false,
                        "unique": false,
                        "index": false,
                        "private": false,
                        "encrypt": false,
                        "encryptionType": null,
                        "decryptWhen": null,
                        "columnName": null
                    },
                    ..., // Other fields
                    {
                        "name": "feeTypes",
                        "displayName": "FeeTypes",
                        "description": "FeeTypes",
                        "type": "relation",
                        "ormType": "integer",
                        "isSystem": false,
                        "relationType": "one-to-many",
                        "relationCoModelFieldName": "institute",
                        "relationCreateInverse": true,
                        "relationCoModelSingularName": "feeType",
                        "relationCoModelColumnName": null,
                        "relationModelModuleName": "fees-portal",
                        "relationCascade": "cascade",
                        "required": false,
                        "unique": false,
                        "index": false,
                        "private": false,
                        "encrypt": false,
                        "encryptionType": null,
                        "decryptWhen": null,
                        "columnName": null,
                        "relationJoinTableName": null,
                        "isRelationManyToManyOwner": null,
                        "relationFieldFixedFilter": "",
                        "enableAuditTracking": false
                    },
                    ..., // Other fields
                ]
            },
            { // Fee Type model metadata
                "singularName": "feeType",
                "pluralName": "feeTypes",
                "displayName": "Fee Type",
                "description": "Model used to capture different fee types that a school, institute might use.",
                "dataSource": "default",
                "dataSourceType": "postgres",
                "tableName": "fees_portal_fee_type",
                "userKeyFieldUserKey": "feeTypeUserKey",
                "isChild": false,
                "enableAuditTracking": true,
                "enableSoftDelete": false,
                "draftPublishWorkflow": false,
                "internationalisation": false,
                "fields": [ // Fee Type model fields metadata
                    {
                        "name": "feeType",
                        "displayName": "Fee Type",
                        "description": "The actual fee type. Eg. Tuition Fees, Bus Fees",
                        "type": "shortText",
                        "ormType": "varchar",
                        "isSystem": false,
                        "defaultValue": null,
                        "min": null,
                        "max": null,
                        "required": true,
                        "unique": false,
                        "index": false,
                        "private": false,
                        "encrypt": false,
                        "encryptionType": null,
                        "decryptWhen": null,
                        "columnName": null,
                        "isUserKey": true,
                        "enableAuditTracking": false
                    },
                    {
                        "name": "institute",
                        "displayName": "Institute",
                        "description": null,
                        "type": "relation",
                        "ormType": "integer",
                        "isSystem": false,
                        "relationType": "many-to-one",
                        "relationCoModelFieldName": "feeTypes",
                        "relationCreateInverse": true,
                        "relationCoModelSingularName": "institute",
                        "relationCoModelColumnName": null,
                        "relationModelModuleName": "fees-portal",
                        "relationCascade": "cascade",
                        "required": true,
                        "unique": false,
                        "index": false,
                        "private": false,
                        "encrypt": false,
                        "encryptionType": null,
                        "decryptWhen": null,
                        "columnName": null,
                        "relationJoinTableName": null,
                        "isRelationManyToManyOwner": null,
                        "relationFieldFixedFilter": "",
                        "enableAuditTracking": false
                    },
                    {
                        "name": "partPaymentAllowed",
                        "displayName": "Part Payment Allowed",
                        "description": null,
                        "type": "boolean",
                        "ormType": "boolean",
                        "isSystem": false,
                        "defaultValue": null,
                        "required": true,
                        "index": false,
                        "private": false,
                        "encrypt": false,
                        "encryptionType": null,
                        "decryptWhen": null,
                        "columnName": null,
                        "enableAuditTracking": false
                    },
                    {
                        "name": "latePaymentFeesType",
                        "displayName": "Late Payment Fees Type",
                        "description": null,
                        "type": "selectionStatic",
                        "ormType": "varchar",
                        "isSystem": false,
                        "defaultValue": "None",
                        "selectionStaticValues": [
                            "None:None",
                            "Percent:Percent",
                            "Absolute:Absolute"
                        ],
                        "selectionValueType": "string",
                        "required": false,
                        "unique": false,
                        "index": false,
                        "private": false,
                        "encrypt": false,
                        "encryptionType": null,
                        "decryptWhen": null,
                        "columnName": null,
                        "enableAuditTracking": false,
                        "isMultiSelect": false
                    },
                    {
                        "name": "latePaymentFees",
                        "displayName": "Late Payment Fees",
                        "description": null,
                        "type": "decimal",
                        "ormType": "decimal",
                        "isSystem": false,
                        "defaultValue": "0",
                        "min": null,
                        "max": null,
                        "required": false,
                        "unique": false,
                        "index": false,
                        "private": false,
                        "encrypt": false,
                        "encryptionType": null,
                        "decryptWhen": null,
                        "columnName": null,
                        "enableAuditTracking": false
                    },
                    {
                        "name": "feeTypeUserKey",
                        "displayName": "Fee Type User Key",
                        "description": "Concatenation of fee type and institute name",
                        "type": "computed",
                        "ormType": "varchar",
                        "isSystem": false,
                        "computedFieldValueType": "string",
                        "computedFieldTriggerConfig": [
                            {
                                "modelName": "feeType",
                                "moduleName": "fees-portal",
                                "operations": [
                                    "before-insert"
                                ]
                            }
                        ],
                        "computedFieldValueProvider": "ConcatEntityComputedFieldProvider",
                        "computedFieldValueProviderCtxt": "{\n  \"fields\": [\n    \"feeType\",\n    \"institute.instituteName\"\n  ],\n  \"separator\": \"-\",\n  \"slugify\": true\n}",
                        "required": true,
                        "unique": true,
                        "index": false,
                        "private": false,
                        "encrypt": false,
                        "encryptionType": null,
                        "decryptWhen": null,
                        "columnName": null,
                        "isUserKey": true
                    }
                ]
            },
            ..., // Other models
        ]
    },
    ... // Other metadata
}
```
</details>
---

## 🎛 Field Type (`type`)  

> **This is the most important attribute of a field.**  
> It determines the **behavior, validation, storage, and UI options** for the field.  

---

### 📊 Numeric Types
| Value    | Reference |
|----------|------------|
| `int`    | [Integer Field](../../admin-docs/module-builder/field-management#integer) |
| `bigint` | [BigInt Field](../../admin-docs/module-builder/field-management#bigint) |
| `decimal`| [Decimal Field](../../admin-docs/module-builder/field-management#decimal) |

---

### ✍️ Text Types
| Value       | Reference |
|-------------|-----------|
| `shortText` | [Short Text Field](../../admin-docs/module-builder/field-management#shorttext) |
| `longText`  | [Long Text Field](../../admin-docs/module-builder/field-management#longtext) |
| `richText`  | [Rich Text Field](../../admin-docs/module-builder/field-management#richtext) |
| `json`      | [JSON Field](../../admin-docs/module-builder/field-management#json) |

---

### 🔘 Boolean
- [`boolean`](../../admin-docs/module-builder/field-management#boolean)

---

### 🗓 Date & Time Types
| Value     | Reference |
|-----------|-----------|
| `date`    | [Date Field](../../admin-docs/module-builder/field-management#date) |
| `datetime`| [Datetime Field](../../admin-docs/module-builder/field-management#datetime) |
| `time`    | [Time Field](../../admin-docs/module-builder/field-management#time) |

---

### 🔗 Relations
- [`relation`](../../admin-docs/module-builder/field-management#relation)

---

### 🖼 Media Types
| Value         | Reference |
|---------------|-----------|
| `mediaSingle`   | [Single Media Field](../../admin-docs/module-builder/field-management#single-media) |
| `mediaMultiple` | [Multiple Media Field](../../admin-docs/module-builder/field-management#multiple-media) |

---

### 📧 Auth & Identity
| Value     | Reference |
|-----------|-----------|
| `email`   | [Email Field](../../admin-docs/module-builder/field-management#email) |
| `password`| [Password Field](../../admin-docs/module-builder/field-management#password) |

---

### ✅ Selection
| Value            | Reference |
|------------------|-----------|
| `selectionStatic`  | [Static Selection Field](../../admin-docs/module-builder/field-management#static-selection) |
| `selectionDynamic` | [Dynamic Selection Field](../../admin-docs/module-builder/field-management#dynamic-selection) |

---

### ⚙️ Computed
- [`computed`](../../admin-docs/module-builder/field-management#computed)


---

## 🔍 Field Metadata Attributes

### `name` *(string, required)*
Name of the field (column/property).  
**Default:** N/A

---

### `displayName` *(string, required)*
Human-readable label for UI and docs.  
**Default:** N/A

---

### `description` *(string, optional)*
Short help/purpose text shown in UI or docs.  
**Default:** N/A

---

### `type` *(SolidFieldType, required)*
Refer to [Field Type](#-field-type-type) section above.

**Default:** N/A

---

### `modelId` *(number, optional)*
Numeric id of the owning model (internal linkage).  
**Default:** N/A

---

### `ormType` *(PSQLType, optional)*
Override database column type. Use only when the default mapping from `type` is insufficient.  
**Values:** 
- integer
- decimal
- bigint
- varchar
- text
- boolean
- timestamp
- timestamptz
- time
- date
- json
- jsonb  
**Default:** Derived from `type`

<!-- --- -->

<!-- ### `length` *(number, optional)*
Max length/size where relevant.  
**Applies to:** shortText, longText, richText, json  
**Default:** N/A -->

---

### `defaultValue` *(string, optional)*
Literal default value applied on create.  
**Default:** N/A

---

### `regexPattern` *(string, optional)*
Validation pattern for textual inputs.  
**Applies to:** shortText, longText, email, password  
**Default:** N/A

---

### `regexPatternNotMatchingErrorMsg` *(string, optional)*
Custom error message when `regexPattern` fails.  
**Default:** N/A

---

### `required` *(boolean, optional)*
Marks field as mandatory.  
**Default:** false

---

### `unique` *(boolean, optional)*
Enforces uniqueness.  
**Default:** false

---

### `encrypt` *(boolean, optional)*
Enable symmetric encryption-at-rest for this field.  
**Default:** false
:::note
 Feature coming soon!
:::

---

### `encryptionType` *(enum, optional)*
Only if `encrypt = true`.  
**Values:** 
- aes-128
- aes-256  
**Default:** aes-256 (recommended)
:::note
Feature coming soon!
:::

---

### `decryptWhen` *(enum, optional)*
Only if `encrypt = true`. Controls when plaintext is produced.  
**Values:** 
- before-transit
- after-transit  
**Default:** after-transit
:::note
Feature coming soon!
:::
---

### `index` *(boolean, optional)*
Add an index for search/sort (where supported).  
**Not applicable to:** richText, longText  
**Default:** false

---

### `max` *(number, optional)*
Upper bound (number/date) or maximum length (text/json).  
**Applies to:** shortText, longText, richText, json, int, decimal, date, datetime, time  
**Default:** N/A

---

### `min` *(number, optional)*
Lower bound (number/date) or minimum length (text/json).  
**Applies to:** shortText, longText, richText, json, int, decimal, date, datetime, time  
**Default:** N/A

---

### `private` *(boolean, optional)*
Exclude from default listings/exports; require elevated access.  
**Default:** false
:::note
Feature coming soon!
:::
---

### `mediaTypes` *(MediaType[], optional)*
Allowlist of media categories.  
**Applies to:** mediaSingle, mediaMultiple  
**Values:** 
- image
- audio
- video
- file  
**Default:** All sensible for the field type

---

### `mediaMaxSizeKb` *(number, optional)*
Max upload size per item in kilobytes.  
**Applies to:** mediaSingle, mediaMultiple  
**Default:** N/A

---

### `mediaStorageProviderId` *(number, optional)*
Numeric id of configured media storage provider.  
**Applies to:** mediaSingle, mediaMultiple  
**Default:** Module/provider default

---

### `mediaStorageProviderUserKey` *(string, optional)*
Name/userKey of configured media storage provider.  
**Applies to:** mediaSingle, mediaMultiple  
**Default:** default-filesystem

:::note
By default, SolidX applications gets seeded with 2 media storage providers i.e default-filesystem and default-aws-s3. You can create more providers as per your requirements. You can refer to the [Storage Provider Documentation](../../admin-docs/media-library/storage-providers.md) for more details.
:::
---

### `relationType` *(RelationType, optional)*
Kind of relation.  
**Applies to:** relation  
**Values:** 
- many-to-one
- many-to-many
- one-to-many  
**Default:** N/A

---

### `relationCoModelSingularName` *(string, optional)*
`singularName` of the related co-model.  
**Applies to:** relation  
**Default:** N/A

---

### `relationCreateInverse` *(boolean, optional)*
Generate inverse side on co-model.  
**Applies to:** relation  
**Default:** false

:::warning
Currently we auto-create the inverse side of the field metadata on the co-model. In future releases, we will get rid of the inverse field auto-creation and instead have the user explicitly create the inverse field on the co-model. This is to ensure that the user has full control on how the inverse field is created on the co-model and keep things explicit and simple
:::
---

### `relationCascade` *(CascadeType, optional)*
Only if `type = relation` and `relationCreateInverse = true`.
Cascade behavior for persistence i.e (create/update) and deletion.  
**Applies to:** relation  
**Values:** 
- set null
- restrict
- cascade  
**Default:** restrict (recommended explicitness)

---

### `relationModelModuleName` *(string, optional)*
Only if `type = relation` and `relationCreateInverse = true` and the related co-model lives in a **different module**.
Module name if the related co-model lives in a **different module**.  
**Applies to:** relation  
**Default:** Current module

---

### `relationCoModelFieldName` *(string, mandatory for many-to-many)*
Only if `type = relation` and `relationCreateInverse = true`.
For m2m or cross-model relations, the other side's field name.  
Auto-inferred for many-to-one but required for many-to-many.
**Applies to:** relation  
**Default:** Auto-inferred for many-to-one

---

### `isRelationManyToManyOwner` *(boolean, mandatory for many-to-many)*
Only if `type = relation` and `relationType = many-to-many`.
Marks this side as the **owner** of the many-to-many.
At least one side must be the owner, otherwise the many-to-many relation will not work.  
**Applies to:** relation (many-to-many)  
**Default:** false
:::info
TODO: change default to true in future releases
:::

---

### `relationFieldFixedFilter` *(string, optional)*
Fixed filter (JSON) applied when fetching related records from the admin ui. This can be used to apply static as well as dynamic filters when we want to conditionally filter the values shown for the related records

The filter is a JSON object of schema type BasicFilterDto:
<details>
<summary>📑 Filter schema</summary>
```ts
export enum SoftDeleteFilter {
    INCLUSIVE = "inclusive",
    EXCLUSIVE = "exclusive",
}

export class BasicFilterDto extends PaginationQueryDto {

    @IsOptional()
    @ApiProperty({ description: "Fields" })
    readonly fields?: string[];

    @IsOptional()
    @ApiProperty({ description: "sort" })
    readonly sort?: string[];

    @IsOptional()
    @ApiProperty({ description: "groupBy" })
    readonly groupBy?: string[];


    @IsOptional()
    @ApiProperty({ description: "populate" })
    readonly populate?: string[];


    @IsOptional()
    @ApiProperty({ description: "populateMedia" })
    readonly populateMedia?: string[];

    @IsOptional()
    @IsEnum(SoftDeleteFilter)
    @ApiProperty({
        description: "showSoftDeleted",
        enum: SoftDeleteFilter,
    })
    readonly showSoftDeleted?: SoftDeleteFilter;

    @IsOptional()
    @ApiProperty({ description: "populateGroup" })
    readonly populateGroup?: boolean;

    @IsOptional()
    @ApiProperty({ description: "groupFilter" })
    groupFilter?: BasicFilterDto

    @IsOptional()
    @ApiProperty({ description: "locale" })
    readonly locale?: string;

    @IsOptional()
    @ApiProperty({ description: "status publish draft" })
    readonly status?: string;
}

export class PaginationQueryDto {
    constructor(limit: number, offset: number) {
        this.limit = limit;
        this.offset = offset;
    }

    @IsOptional()
    @Type(() => Number)
    @IsPositive()
    limit?: number = 10;

    @IsOptional()
    @Type(() => Number)
    @IsInt()
    @Min(0)
    offset?: number = 0;

    @IsOptional()
    filters?: Record<string, any>;
}
```
</details>

**Applies to:** relation  
**Default:** N/A

---

### `selectionDynamicProvider` *(string, optional)*
Provider identifier for loading dynamic options.
**Applies to:** selectionDynamic  
**Default:** N/A

---

### `selectionDynamicProviderCtxt` *(string, optional)*
Context/config passed to the dynamic provider.
**Applies to:** selectionDynamic  
**Default:** N/A

---

### `selectionStaticValues` *(string[], optional)*
List of static options in `key:Label` format.  
**Applies to:** selectionStatic  
**Default:** N/A

---

### `selectionValueType` *(enum, optional)*
Primitive type of selection values.  
**Applies to:** selectionStatic, selectionDynamic  
**Values:** 
- string
- int  
**Default:** string

---

### `computedFieldValueProvider` *(string, optional)*
Provider/class that computes the field value.  
**Applies to:** computed  
**Default:** N/A

---

### `computedFieldValueProviderCtxt` *(string, optional)*
Context/config passed to the computed value provider.  
**Applies to:** computed  
**Default:** N/A

---

### `computedFieldValueType` *(enum, optional)*
Declared output type of the computed field.  
**Applies to:** computed  
**Values:** 
- string
- int
- decimal
- boolean
- date
- datetime  
**Default:** string

---

### `computedFieldTriggerConfig` *(array of objects, optional)*
Operations that trigger compute and the trigger model/module to attach to. This is useful when the computed field depends on relations or other models and needs to be re-computed when those models change.
<summary>📑 Config schema</summary>
``` ts
export class ComputedFieldTriggerConfig {
  moduleName: string; // Name of the module which should trigger the computed field re-evaluation
  modelName: string; // Name of the model which should trigger the computed field re-evaluation
  operations: ComputedFieldTriggerOperation[]; // List of operations on the model, when computed field should be re-evaluated
}
```
**Operations values:** 
- before-insert
- after-insert
- before-update
- after-update
- before-delete
- after-delete  
**Applies to:** computed  
**Default:** N/A

---

<!-- ### `uuid` *(string, optional)*
Explicit UUID for this field definition (rarely needed).  
**Default:** Auto-generated -->

---

### `isSystem` *(boolean, optional)*
System fields are excluded from code generation (hand-written code assumed).  
**Default:** false

---

### `isMarkedForRemoval` *(boolean, optional)*
Soft-removal flag for the field definition. Fields marked for removal are excluded from code generation.
**Default:** false
:::info
 This flag enables the code builder to identify fields that need to be deleted from the codebase. They are deleted after code generation is complete.  
:::

---

### `columnName` *(string, optional)*
Override database column name.  
**Default:** Derived from `name`

---

### `relationCoModelColumnName` *(string, optional)*
Override co-model's column name for relation bindings.  
**Applies to:** relation  
**Default:** Auto-generated/inferred

---

### `isUserKey` *(boolean, optional)*
Marks this field as the **user key** (friendly identifier). This is mandatory if we need to use a relation field in the UI, since the user key is what gets displayed in the dropdowns and lookups.  
**Default:** false

---

### `relationJoinTableName` *(string, optional)*
Custom join table name for many-to-many.  
**Applies to:** relation (many-to-many)  
**Default:** Auto-generated

---

### `enableAuditTracking` *(boolean, optional)*
Track create/update/delete for this field in audit logs.  
**Default:** false

---

### `isMultiSelect` *(boolean, optional)*
Allow multiple selected values (UI + storage impact).  
**Applies to:** selection fields and some primitives depending on UI policy  
**Default:** false

---

## Implementation Notes & Gotchas

- **`ormType` vs `type`** — Prefer defaults derived from `type`. Override `ormType` only when you need a specific DB type (e.g., `jsonb` instead of `json`).  
- **`unique` + `index`** — `unique` usually implies an index; still set `index: true` for frequent filter columns that aren’t unique.  
<!-- - **Encryption** — Prefer `aes-256` unless you have legacy constraints. Keep `decryptWhen: after-transit` to minimize plaintext exposure between services.   -->
<!-- - **Privacy** — `private: true` hides in default listings/exports but does not bypass access control; combine with security rules where needed.   -->
- **User key** — Set `isUserKey: true` on the one field that identifies a record best for humans (e.g., `instituteName`).  
- **Selection fields** — Ensure storage matches UI: arrays for multi-select; validate that `selectionValueType` aligns with downstream consumers.  
- **Relations** — Always specify `relationCascade` explicitly; implicit defaults differ across ORMs/DBs. For many-to-many, define the **owner** side to control join-table updates.  
- **Computed** — Providers should be idempotent and side‑effect free. For pre-compute operations e.g (before-insert, before-update, before-remove), provider needs to set the value on the entity object directly i.e (since in pre-compute operations, the assumption is that the computed field entity and the triggering entity are the same). For post-compute operations e.g (after-insert, after-update, after-remove), provider needs to use the entity manager in the provider implementation to update the entity since in post-compute operations, the assumption is that the computed field entity and the triggering entity can be different.
- **Media** — Validate MIME and size server-side. `mediaTypes` is an allowlist, not a guarantee of safety. Consider thumbnailing and antivirus for file uploads.

---

## Quick Matrix (What applies where?)

| Aspect                | Text (short/long/rich) | Number (int/decimal/bigint) | Date/time | Relation | Media | Selection | Computed |
|-----------------------|------------------------|-----------------------------|-----------|---------|-------|-----------|----------|
| `length`              | ✅                     | ❌                          | ❌        | ❌      | ❌    | ❌        | ❌       |
| `min` / `max`         | ✅ (length)            | ✅ (range)                   | ✅ (bounds)| ❌     | ❌    | ❌        | ❌       |
| `regexPattern`        | ✅                     | ❌                          | ❌        | ❌      | ❌    | ❌        | ❌       |
| `media*`              | ❌                     | ❌                          | ❌        | ❌      | ✅    | ❌        | ❌       |
| `relation*`           | ❌                     | ❌                          | ❌        | ✅      | ❌    | ❌        | ❌       |
| `selection*`          | ❌                     | ❌                          | ❌        | ❌      | ❌    | ✅        | ❌       |
| `computed*`           | ❌                     | ❌                          | ❌        | ❌      | ❌    | ❌        | ✅       |
| `encrypt`/`private`   | ✅                     | ✅                           | ✅        | (id only)| file meta| values   | output   |
| `index`               | ✅ (except rich/long)  | ✅                           | ✅        | ✅      | ❌    | ✅        | ✅ (virtual) |



---

## Recipes & Patterns
You can refer to this [Field Metadata Recipes & Patterns](../../recipes/field-types-reference.md) documentation for some common field metadata recipes and patterns that you can use while defining your model fields.

