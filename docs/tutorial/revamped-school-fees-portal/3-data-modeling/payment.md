---
sidebar_position: 6
---

# Payment Model

**Business Purpose:** Records the details of a payment transaction, including gateway-specific IDs and the payment status.

**Fields:**

| Field Name | Type | Description |
|---|---|---|
| `institute` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | Many-to-one relationship to the `institute` model. |
| `student` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | Many-to-one relationship to the `student` model. |
| `stripeOrderId` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | Order ID from the Stripe payment gateway. |
| `stripePaymentId` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | Payment ID from the Stripe payment gateway. |
| `stripeTransId` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | Transaction ID from the Stripe payment gateway. |
| `stripeInvoiceId` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | Invoice ID from the Stripe payment gateway. |
| `stripeEncodedId` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | Encoded ID from the Stripe payment gateway. |
| `stripeStatus` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | Status from the Stripe payment gateway. |
| `amount` | [`decimal`](../../../admin-docs/module-builder/field-management#decimal) | The amount of the payment. |
| `isRefunded` | [`boolean`](../../../admin-docs/module-builder/field-management#boolean) | A flag indicating if the payment has been refunded. |
| `paymentStatus` | [`selectionStatic`](../../../admin-docs/module-builder/field-management#static-selection) | The status of the payment (e.g., Pending, Succeeded, Failed). |
| `paymentCollectionItemDetails` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | One-to-many relationship to `paymentCollectionItemDetail`. |


**Metadata JSON:**

<details>
<summary>&emsp; View Metadata JSON</summary>

```json
{
  "singularName": "payment",
  "pluralName": "payments",
  "displayName": "Payment",
  "description": "This table allows us to store payment records of a user",
  "dataSource": "default",
  "dataSourceType": "postgres",
  "tableName": "fees_portal_payment",
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
      "relationCoModelFieldName": "payments",
      "relationCreateInverse": true,
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
      "name": "stripeOrderId",
      "displayName": "Stripe Order Id",
      "description": null,
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
      "isUserKey": false,
      "enableAuditTracking": true
    },
    {
      "name": "stripePaymentId",
      "displayName": "Stripe Payment Id",
      "description": null,
      "type": "shortText",
      "ormType": "varchar",
      "isSystem": false,
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
      "columnName": null,
      "isUserKey": false,
      "enableAuditTracking": true
    },
    {
      "name": "stripeTransId",
      "displayName": "Stripe Trans Id",
      "description": null,
      "type": "shortText",
      "ormType": "varchar",
      "isSystem": false,
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
      "columnName": null,
      "isUserKey": false,
      "enableAuditTracking": true
    },
    {
      "name": "stripeInvoiceId",
      "displayName": "Stripe Invoice Id",
      "description": null,
      "type": "shortText",
      "ormType": "varchar",
      "isSystem": false,
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
      "columnName": null,
      "isUserKey": false,
      "enableAuditTracking": true
    },
    {
      "name": "stripeEncodedId",
      "displayName": "Stripe Encoded Id",
      "description": null,
      "type": "shortText",
      "ormType": "varchar",
      "isSystem": false,
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
      "columnName": null,
      "isUserKey": false,
      "enableAuditTracking": true
    },
    {
      "name": "stripeStatus",
      "displayName": "Stripe Status",
      "description": null,
      "type": "shortText",
      "ormType": "varchar",
      "isSystem": false,
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
      "columnName": null,
      "isUserKey": false,
      "enableAuditTracking": true
    },
    {
      "name": "amount",
      "displayName": "Amount",
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
    },
    {
      "name": "isRefunded",
      "displayName": "Is Refunded",
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
      "name": "paymentCollectionItemDetails",
      "displayName": "PaymentCollectionItemDetails",
      "description": null,
      "type": "relation",
      "ormType": "integer",
      "isSystem": false,
      "relationType": "one-to-many",
      "relationCoModelFieldName": "payment",
      "relationCreateInverse": true,
      "relationCoModelSingularName": "paymentCollectionItemDetail",
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
    }
  ]
}
```

</details>

**Apply Changes:** Apply model changes as guided in Data Modeling page.