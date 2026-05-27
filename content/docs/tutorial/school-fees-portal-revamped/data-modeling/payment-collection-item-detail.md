---
title: Payment Collection Item Detail Model
---

**Business Purpose:** Stores the breakdown of a payment, linking a payment transaction to one or more fee items. This model is the key to enabling partial payments.

**Fields:**

| Field Name | Type | Description |
|---|---|---|
| `institute` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | Many-to-one relationship to the `institute` model. |
| `student` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | Many-to-one relationship to the `student` model. |
| `paymentCollectionItem` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | Many-to-one relationship to the `paymentCollectionItem` model. |
| `paymentDate` | [`datetime`](../../../admin-docs/module-builder/field-management#datetime) | The date and time of the payment. |
| `amountPaid` | [`decimal`](../../../admin-docs/module-builder/field-management#decimal) | The amount paid in this transaction. |
| `isRefunded` | [`boolean`](../../../admin-docs/module-builder/field-management#boolean) | A flag indicating if this portion of the payment was refunded. |
| `paymentStatus` | [`selectionStatic`](../../../admin-docs/module-builder/field-management#static-selection) | The status of this payment detail (e.g., Succeeded, Failed). |
| `payment` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | Many-to-one relationship to the `payment` model. |

### Key Fields Explained

-   **The "Glue" Model:** This model's primary purpose is to connect a `Payment` with a `PaymentCollectionItem`. It acts as a "line item" for a payment.
-   **Enabling Partial Payments:** Imagine a student owes $500 for "Tuition Fee" and $100 for "Library Fee". They make a single payment of $600. This would create:
    -   One `Payment` record for $600.
    -   Two `PaymentCollectionItemDetail` records:
        1.  One linking the $600 `Payment` to the "Tuition Fee" `PaymentCollectionItem`, with an `amountPaid` of $500.
        2.  Another linking the same $600 `Payment` to the "Library Fee" `PaymentCollectionItem`, with an `amountPaid` of $100.
-   **Trigger for Computed Fields:** The creation of records in this model is what triggers the `computed` fields (like `amountPaid`) on the `PaymentCollectionItem` to automatically update.

### Creation Steps

If you are following the manual "Guided Tour", follow these steps to create the `Payment Collection Item Detail` model in the App Builder.

1.  Navigate to **Fees Portal > App Builder > Model** and click **Add**.
2.  Fill in the primary details for the model:
    -   **Singular Name:** `paymentCollectionItemDetail`
    -   **Plural Name:** `paymentCollectionItemDetails`
    -   **Display Name:** `Payment Collection Item Detail`
3.  Go to the **Fields** tab.
4.  Click **Add Field** and create each field exactly as defined in the table above.
5.  Click **Save**.

> **For the Fast Track: Model Metadata**
> The JSON block below contains the complete metadata definition for the **Payment Collection Item Detail** model.
> 
> This definition is structured with top-level properties for the model itself (like `singularName`, `pluralName`, `tableName`) and a `fields` array that defines every attribute you see in the table above.
> 
> You can use this metadata as part of the "Fast Track" approach outlined in the [Data Modeling Overview](./index.md) by including it in the main `fees-portal-metadata.json` file.
<details>
<summary>&emsp; View Metadata JSON</summary>

```json
{
  "singularName": "paymentCollectionItemDetail",
  "pluralName": "paymentCollectionItemDetails",
  "displayName": "Payment Collection Item Detail",
  "description": "This table allows us to store payment collection detail of user",
  "dataSource": "default",
  "dataSourceType": "postgres",
  "tableName": "fees_portal_payment_collection_item_detail",
  "isChild": false,
  "enableAuditTracking": true,
  "enableSoftDelete": false,
  "draftPublishWorkflow": false,
  "internationalisation": false,
  "fields": [
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
      "name": "student",
      "displayName": "Student",
      "description": null,
      "type": "relation",
      "ormType": "integer",
      "isSystem": false,
      "relationType": "many-to-one",
      "relationCoModelFieldName": null,
      "relationCreateInverse": false,
      "relationCoModelSingularName": "student",
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
      "name": "paymentCollectionItem",
      "displayName": "Payment Collection Item",
      "description": null,
      "type": "relation",
      "ormType": "integer",
      "isSystem": false,
      "relationType": "many-to-one",
      "relationCoModelFieldName": "paymentCollectionItemDetails",
      "relationCreateInverse": true,
      "relationCoModelSingularName": "paymentCollectionItem",
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
      "name": "paymentDate",
      "displayName": "Payment Date",
      "description": null,
      "type": "datetime",
      "ormType": "timestamp",
      "isSystem": false,
      "defaultValue": null,
      "required": true,
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
      "name": "isRefunded",
      "displayName": "Is Refunded",
      "description": null,
      "type": "boolean",
      "ormType": "boolean",
      "isSystem": false,
      "defaultValue": null,
      "required": false,
      "index": false,
      "private": false,
      "encrypt": false,
      "encryptionType": null,
      "decryptWhen": null,
      "columnName": null,
      "enableAuditTracking": true
    },
    {
      "name": "paymentStatus",
      "displayName": "Payment Status",
      "description": null,
      "type": "selectionStatic",
      "ormType": "varchar",
      "isSystem": false,
      "defaultValue": "Pending",
      "selectionStaticValues": [
        "Pending:Pending",
        "Succeeded:Succeeded",
        "Failed:Failed"
      ],
      "selectionValueType": "string",
      "required": true,
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
      "name": "payment",
      "displayName": "Payment",
      "description": null,
      "type": "relation",
      "ormType": "integer",
      "isSystem": false,
      "relationType": "many-to-one",
      "relationCoModelFieldName": "paymentCollectionItemDetails",
      "relationCreateInverse": true,
      "relationCoModelSingularName": "payment",
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
      "name": "amountPaid",
      "displayName": "Amount Paid",
      "description": null,
      "type": "decimal",
      "ormType": "decimal",
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
      "enableAuditTracking": true
    }
  ]
}
```
</details>
