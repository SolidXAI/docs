---
sidebar_position: 4
---

# Payment Collection Model

**Business Purpose:** Represents a batch of fee collection requests, often initiated by uploading a file (e.g., an Excel sheet). It acts as a container for multiple individual fee items for an institute.

**Fields:**

| Field Name | Type | Description |
|---|---|---|
| `name` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | A name for the payment collection batch. |
| `description` | [`longText`](../../../admin-docs/module-builder/field-management#long-text) | A description of the payment collection. |
| `institute` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | A many-to-one relationship to the `institute` model. |
| `paymentFile` | [`mediaSingle`](../../../admin-docs/module-builder/field-management#single-media) | The uploaded file (e.g., Excel, CSV) containing fee details. |
| `paymentCollectionItems` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | A one-to-many relationship to `paymentCollectionItem`. |
| `dueDate` | [`date`](../../../admin-docs/module-builder/field-management#date) | The due date for the payments in this collection. |
| `paymentCollectionId` | [`computed`](../../../admin-docs/module-builder/field-management#computed) | A unique ID for the payment collection, computed from its name. |

---

### Key Fields Explained

-   **`paymentFile` (Media - File):** This field is central to the bulk-upload use case. An institute admin will upload an Excel or CSV file here. We will later write a **Subscriber** that listens for the creation of this record, parses the file, and automatically creates all the individual `PaymentCollectionItem` records for each student listed in the file.
-   **`paymentCollectionItems` (Relation):** This defines the one-to-many link between a single collection batch and the many individual fee items it contains.
-   **`paymentCollectionId` (Computed):** This serves as the unique, human-readable User Key for the collection batch, automatically generated from the `name` field (e.g., `annual-fees-2023-a4f81`).

---

### Creation Steps

If you are following the manual "Guided Tour", follow these steps to create the `Payment Collection` model in the App Builder.

1.  Navigate to **Fees Portal > App Builder > Model** and click **Add**.
2.  Fill in the primary details for the model:
    -   **Singular Name:** `paymentCollection`
    -   **Plural Name:** `paymentCollections`
    -   **Display Name:** `Payment Collection`
3.  Go to the **Fields** tab.
4.  Click **Add Field** and create each field exactly as defined in the table above.
5.  Click **Save**.

---

:::tip For the Fast Track: Model Metadata
The JSON block below contains the complete metadata definition for the **Payment Collection** model.

This definition is structured with top-level properties for the model itself (like `singularName`, `pluralName`, `tableName`) and a `fields` array that defines every attribute you see in the table above.

You can use this metadata as part of the "Fast Track" approach outlined in the [Data Modeling Overview](./index.md) by including it in the main `fees-portal-metadata.json` file.
:::

<details>
<summary>&emsp; View Metadata JSON</summary>

```json
{
  "singularName": "paymentCollection",
  "pluralName": "paymentCollections",
  "displayName": "Payment Collection",
  "description": "This table allows us to store payment collection records institute wise",
  "dataSource": "default",
  "dataSourceType": "postgres",
  "tableName": "fees_portal_payment_collection",
  "userKeyFieldUserKey": "paymentCollectionId",
  "isChild": false,
  "enableAuditTracking": true,
  "enableSoftDelete": false,
  "draftPublishWorkflow": false,
  "internationalisation": false,
  "fields": [
    {
      "name": "name",
      "displayName": "Name",
      "description": null,
      "type": "shortText",
      "ormType": "varchar",
      "isSystem": false,
      "defaultValue": null,
      "min": null,
      "max": null,
      "required": true,
      "unique": false,
      "index": true,
      "private": false,
      "encrypt": false,
      "encryptionType": null,
      "decryptWhen": null,
      "columnName": null,
      "isUserKey": false,
      "enableAuditTracking": true
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
    {
      "name": "institute",
      "displayName": "Institute",
      "description": null,
      "type": "relation",
      "ormType": "integer",
      "isSystem": false,
      "relationType": "many-to-one",
      "relationCoModelFieldName": null,
      "relationCreateInverse": false,
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
      "name": "paymentFile",
      "displayName": "Payment File",
      "description": null,
      "type": "mediaSingle",
      "ormType": "varchar",
      "isSystem": false,
      "mediaTypes": [
        "file"
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
      "mediaStorageProviderUserKey": "default-filesystem"
    },
    {
      "name": "paymentCollectionItems",
      "displayName": "PaymentCollectionItems",
      "description": null,
      "type": "relation",
      "ormType": "integer",
      "isSystem": false,
      "relationType": "one-to-many",
      "relationCoModelFieldName": "paymentCollection",
      "relationCreateInverse": true,
      "relationCoModelSingularName": "paymentCollectionItem",
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
      "enableAuditTracking": true
    },
    {
      "name": "dueDate",
      "displayName": "Due date",
      "description": null,
      "type": "date",
      "ormType": "date",
      "isSystem": false,
      "defaultValue": null,
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
      "name": "paymentCollectionId",
      "displayName": "Payment Collection Id",
      "description": null,
      "type": "computed",
      "ormType": "varchar",
      "isSystem": false,
      "computedFieldValueType": "string",
      "computedFieldTriggerConfig": [
        {
          "modelName": "paymentCollection",
          "moduleName": "fees-portal",
          "operations": [
            "before-insert"
          ]
        }
      ],
      "computedFieldValueProvider": "AlphaNumExternalIdComputationProvider",
      "computedFieldValueProviderCtxt": "{\n  \"dynamicFieldPrefix\": \"name\",\n  \"length\": 5\n}",
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