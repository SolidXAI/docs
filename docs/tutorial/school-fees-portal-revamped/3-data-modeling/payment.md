---
sidebar_position: 7
---

# Payment Model

**Business Purpose:** Records the details of a single, complete payment transaction made by a student. This model acts as a log, capturing the total amount paid and all the identifiers returned by the external payment gateway.

**Fields:**

| Field Name | Type | Description |
|---|---|---|
| `institute` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | Many-to-one relationship to the `institute` model. |
| `student` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | Many-to-one relationship to the `student` model. |
| `paymentGatewayOrderId` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | Order ID from the Payment Gateway. |
| `paymentGatewayPaymentId` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | Payment ID from the Payment Gateway. |
| `paymentGatewayTransId` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | Transaction ID from the Payment Gateway. |
| `paymentGatewayInvoiceId` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | Invoice ID from the Payment Gateway. |
| `paymentGatewayEncodedId` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | Encoded ID from the Payment Gateway. |
| `paymentGatewayStatus` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | Status from the Payment Gateway. |
| `amount` | [`decimal`](../../../admin-docs/module-builder/field-management#decimal) | The amount of the payment. |
| `isRefunded` | [`boolean`](../../../admin-docs/module-builder/field-management#boolean) | A flag indicating if the payment has been refunded. |
| `paymentStatus` | [`selectionStatic`](../../../admin-docs/module-builder/field-management#static-selection) | The status of the payment (e.g., Pending, Succeeded, Failed). |
| `paymentCollectionItemDetails` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | One-to-many relationship to `paymentCollectionItemDetail`. |

---

### Key Fields Explained

-   **`paymentGateway...` Fields:** This group of fields is essential for traceability. They store all the unique IDs and status codes returned by the payment gateway (e.g., Stripe, PayPal) after a transaction attempt. This is critical for reconciling payments, handling disputes, and debugging transaction issues.
-   **`paymentStatus` (Static Selection):** This is our internal status for the payment, which is updated based on the callback we receive from the payment gateway. It can be `Pending` (while the user is on the payment page), `Succeeded`, or `Failed`.
-   **`paymentCollectionItemDetails` (Relation):** This one-to-many relationship is key for partial payments. A single `Payment` of $100 could be linked to two `PaymentCollectionItemDetail` records: one for $70 towards "Tuition" and one for $30 towards "Bus Fee".

---

### Creation Steps

If you are following the manual "Guided Tour", follow these steps to create the `Payment` model in the App Builder.

1.  Navigate to **Fees Portal > App Builder > Model** and click **Add**.
2.  Fill in the primary details for the model:
    -   **Singular Name:** `payment`
    -   **Plural Name:** `payments`
    -   **Display Name:** `Payment`
3.  Go to the **Fields** tab.
4.  Click **Add Field** and create each field exactly as defined in the table above.
5.  Click **Save**.

---

:::tip For the Fast Track: Model Metadata
The JSON block below contains the complete metadata definition for the **Payment** model.

This definition is structured with top-level properties for the model itself (like `singularName`, `pluralName`, `tableName`) and a `fields` array that defines every attribute you see in the table above.

You can use this metadata as part of the "Fast Track" approach by including it in the main `fees-portal-metadata.json` file.
:::

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
      "name": "paymentGatewayOrderId",
      "displayName": "Payment Gateway Order Id",
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
      "name": "paymentGatewayPaymentId",
      "displayName": "Payment Gateway Payment Id",
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
      "name": "paymentGatewayTransId",
      "displayName": "Payment Gateway Trans Id",
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
      "name": "paymentGatewayInvoiceId",
      "displayName": "Payment Gateway Invoice Id",
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
      "name": "paymentGatewayEncodedId",
      "displayName": "Payment Gateway Encoded Id",
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
      "name": "paymentGatewayStatus",
      "displayName": "Payment Gateway Status",
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
