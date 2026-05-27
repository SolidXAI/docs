---
title: Fee Type Model
---

**Business Purpose:** Defines the different types of fees an institute can charge (e.g., "Tuition", "Bus Fee", "Library Fee"). This allows for categorization and flexible management of fees.

**Fields:**

| Field Name | Type | Description |
|---|---|---|
| `feeType` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | The name of the fee type. |
| `institute` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | A many-to-one relationship to the `institute` model. |
| `partPaymentAllowed` | [`boolean`](../../../admin-docs/module-builder/field-management#boolean) | Whether partial payments are allowed for this fee type. |
| `latePaymentFeesType` | [`selectionStatic`](../../../admin-docs/module-builder/field-management#static-selection) | The type of late fee to apply (None, Percent, Absolute). |
| `latePaymentFees` | [`decimal`](../../../admin-docs/module-builder/field-management#decimal) | The amount or percentage for the late fee. |
| `feeTypeUserKey` | [`computed`](../../../admin-docs/module-builder/field-management#computed) | A unique key for the fee type, computed from the fee type and institute name. |

### Key Fields Explained

-   **`institute` (Relation):** This is a crucial field that links each fee type to a specific institute. This `many-to-one` relationship ensures that "Tuition Fee" for "Institute A" is distinct from "Tuition Fee" for "Institute B".
-   **`latePaymentFeesType` & `latePaymentFees`:** This pair of fields allows for flexible late fee policies. An admin can choose to apply no late fee, a fixed amount (`Absolute`), or a percentage of the due amount (`Percent`).
-   **`feeTypeUserKey` (Computed):** This is a powerful SolidX feature. It automatically generates a unique, human-readable ID for the record before it's saved. In this case, it combines the `feeType` and the related `institute.instituteName` (e.g., "tuition-fee-institute-a") to guarantee that a fee type name is unique *within* a single institute.

### Creation Steps

If you are following the manual "Guided Tour", follow these steps to create the `Fee Type` model in the App Builder.

1.  Navigate to **Fees Portal > App Builder > Model** and click **Add**.
2.  Fill in the primary details for the model:
    -   **Singular Name:** `feeType`
    -   **Plural Name:** `feeTypes`
    -   **Display Name:** `Fee Type`
3.  Go to the **Fields** tab.
4.  Click **Add Field** and create each field exactly as defined in the table above.
5.  Click **Save**.

> **For the Fast Track: Model Metadata**
> The JSON block below contains the complete metadata definition for the **Fee Type** model.
> 
> This definition is structured with top-level properties for the model itself (like `singularName`, `pluralName`, `tableName`) and a `fields` array that defines every attribute you see in the table above.
> 
> You can use this metadata as part of the "Fast Track" approach by including it in the main `fees-portal-metadata.json` file.
<details>
<summary>&emsp; View Metadata JSON</summary>

```json
{
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
  "fields": [
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
      "enableAuditTracking": true
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
      "enableAuditTracking": true
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
      "enableAuditTracking": true
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
      "enableAuditTracking": true,
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
      "enableAuditTracking": true
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
      "computedFieldValueProviderCtxt": "{\n  \"fields\": [\n    \"feeType\",\n    \"institute.instituteName\"  
  ],\n  \"separator\": \"-\",\n  \"slugify\": true\n}",
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
}
```
</details>