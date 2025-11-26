---
sidebar_position: 6
---

# Payment Collection Item Model

**Business Purpose:** Represents a single, specific fee owed by a student. This is the most granular level of the fee structure, linking a student to a fee type for a specific amount and due date.

**Fields:**

| Field Name | Type | Description |
|---|---|---|
| `student` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | Many-to-one relationship to the `student` model. |
| `paymentCollection` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | Many-to-one relationship to the `paymentCollection` model. |
| `institute` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | Many-to-one relationship to the `institute` model. |
| `feeType` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | Many-to-one relationship to the `feeType` model. |
| `dueDate` | [`date`](../../../admin-docs/module-builder/field-management#date) | The due date for this specific fee item. |
| `amountToBePaid` | [`decimal`](../../../admin-docs/module-builder/field-management#decimal) | The amount to be paid for this fee item. |
| `partPaymentAllowed` | [`boolean`](../../../admin-docs/module-builder/field-management#boolean) | Whether partial payments are allowed for this fee type. |
| `status` | [`selectionStatic`](../../../admin-docs/module-builder/field-management#static-selection) | The payment status (e.g., Pending, Partially Paid, Fully Paid). |
| `amountPaid` | [`computed`](../../../admin-docs/module-builder/field-management#computed) | The total amount paid, computed from related payment details. |
| `amountPending` | [`computed`](../../../admin-docs/module-builder/field-management#computed) | The remaining amount to be paid. |
| `isOverdue` | [`boolean`](../../../admin-docs/module-builder/field-management#boolean) | A flag indicating if the payment is overdue. |
| `overdueByDays` | [`integer`](../../../admin-docs/module-builder/field-management#integer) | The number of days the payment is overdue. |
| `paymentCollectionItemDetails` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | One-to-many relationship to `paymentCollectionItemDetail`. |
| `lateAmountToBePaid` | [`decimal`](../../../admin-docs/module-builder/field-management#decimal) | The late fee amount to be paid. |
| `totalAmountToBePaid` | [`computed`](../../../admin-docs/module-builder/field-management#computed) | The total amount including late fees. |
| `mode` | [`shortText`](../../../admin-docs/module-builder/field-management#short-text) | The mode of payment. |

---

### Key Fields Explained

-   **Relations (`student`, `paymentCollection`, etc.):** This model is the hub of our application, connecting all the major entities for a single transaction.
-   **`status` (Static Selection):** This field acts as a state machine for the fee item. Its value will be updated automatically based on payments made, from `Pending` to `Partially Paid` and finally to `Fully Paid`.
-   **Computed Fields (`amountPaid`, `amountPending`, etc.):** These fields are where the magic happens. Instead of you writing code to calculate the paid or pending amount every time, SolidX does it for you.
    -   The `PaymentCollectionItemAmountProvider` is a piece of custom logic that listens for changes in the related `PaymentCollectionItemDetail` model.
    -   When a payment is made (i.e., a new "detail" record is created), this provider automatically runs, sums up the payments, and updates the `amountPaid` and `status` fields on this record. This keeps your data consistent without any effort.
-   **`paymentCollectionItemDetails` (Inverse Relation):** This field represents the "one-to-many" side of the relationship between a `PaymentCollectionItem` and its `PaymentCollectionItemDetails`. You do not create this field directly. When you define the `many-to-one` relationship from the `PaymentCollectionItemDetail` model back to `PaymentCollectionItem`, SolidX automatically adds this `paymentCollectionItemDetails` field, which holds a list of all payment breakdown records for this specific fee item.

---

### Creation Steps

If you are following the manual "Guided Tour", follow these steps to create the `Payment Collection Item` model in the App Builder.

1.  Navigate to **Fees Portal > App Builder > Model** and click **Add**.
2.  Fill in the primary details for the model:
    -   **Singular Name:** `paymentCollectionItem`
    -   **Plural Name:** `paymentCollectionItems`
    -   **Display Name:** `Payment Collection Item`
3.  Go to the **Fields** tab.
4.  Click **Add Field** and create each field exactly as defined in the table above.
5.  Click **Save**.

---

:::tip For the Fast Track: Model Metadata
The JSON block below contains the complete metadata definition for the **Payment Collection Item** model.

This definition is structured with top-level properties for the model itself (like `singularName`, `pluralName`, `tableName`) and a `fields` array that defines every attribute you see in the table above.

You can use this metadata as part of the "Fast Track" approach by including it in the main `fees-portal-metadata.json` file.
:::

<details>
<summary>&emsp; View Metadata JSON</summary>

```json
{
  "singularName": "paymentCollectionItem",
  "pluralName": "paymentCollectionItems",
  "displayName": "Payment Collection Item",
  "description": "This table allows us to store payment collections collected from user",
  "dataSource": "default",
  "dataSourceType": "postgres",
  "tableName": "fees_portal_payment_collection_item",
  "isChild": false,
  "enableAuditTracking": true,
  "enableSoftDelete": false,
  "draftPublishWorkflow": false,
  "internationalisation": false,
  "fields": [
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
      "name": "paymentCollection",
      "displayName": "Payment Collection",
      "description": null,
      "type": "relation",
      "ormType": "integer",
      "isSystem": false,
      "relationType": "many-to-one",
      "relationCoModelFieldName": "paymentCollectionItems",
      "relationCreateInverse": true,
      "relationCoModelSingularName": "paymentCollection",
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
      "name": "feeType",
      "displayName": "Fee Type",
      "description": null,
      "type": "relation",
      "ormType": "integer",
      "isSystem": false,
      "relationType": "many-to-one",
      "relationCoModelFieldName": null,
      "relationCreateInverse": false,
      "relationCoModelSingularName": "feeType",
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
      "name": "dueDate",
      "displayName": "Due date",
      "description": null,
      "type": "date",
      "ormType": "date",
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
      "name": "status",
      "displayName": "Status",
      "description": null,
      "type": "selectionStatic",
      "ormType": "varchar",
      "isSystem": false,
      "defaultValue": "Pending",
      "selectionStaticValues": [
        "Pending:Pending",
        "Partially Paid:Partially Paid",
        "Fully Paid:Fully Paid",
        "Cancelled:Cancelled"
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
      "name": "isOverdue",
      "displayName": "Is Overdue",
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
      "name": "overdueByDays",
      "displayName": "Overdue By Days",
      "description": null,
      "type": "int",
      "ormType": "integer",
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
      "name": "lateAmountToBePaid",
      "displayName": "Late Amount To Be Paid",
      "description": null,
      "type": "decimal",
      "ormType": "decimal",
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
      "enableAuditTracking": true
    },
    {
      "name": "amountPaid",
      "displayName": "Amount Paid",
      "description": null,
      "type": "computed",
      "ormType": "varchar",
      "isSystem": false,
      "computedFieldValueType": "decimal",
      "computedFieldTriggerConfig": [
        {
          "modelName": "paymentCollectionItemDetail",
          "moduleName": "fees-portal",
          "operations": [
            "after-update"
          ]
        }
      ],
      "computedFieldValueProvider": "PaymentCollectionItemAmountProvider",
      "computedFieldValueProviderCtxt": "{}",
      "required": true,
      "unique": false,
      "index": false,
      "private": false,
      "encrypt": false,
      "encryptionType": null,
      "decryptWhen": null,
      "columnName": null,
      "isUserKey": false
    },
    {
      "name": "amountToBePaid",
      "displayName": "Amount To Be Paid",
      "description": null,
      "type": "decimal",
      "ormType": "decimal",
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
      "enableAuditTracking": true
    },
    {
      "name": "amountPending",
      "displayName": "Amount Pending",
      "description": null,
      "type": "computed",
      "ormType": "varchar",
      "isSystem": false,
      "computedFieldValueType": "decimal",
      "computedFieldTriggerConfig": [
        {
          "modelName": "paymentCollectionItemDetail",
          "moduleName": "fees-portal",
          "operations": [
            "before-insert"
          ]
        }
      ],
      "computedFieldValueProvider": "NoopsEntityComputedFieldProviderService",
      "computedFieldValueProviderCtxt": "{}",
      "required": true,
      "unique": false,
      "index": false,
      "private": false,
      "encrypt": false,
      "encryptionType": null,
      "decryptWhen": null,
      "columnName": null,
      "isUserKey": false
    },
    {
      "name": "totalAmountToBePaid",
      "displayName": "Total Amount To Be Paid",
      "description": null,
      "type": "computed",
      "ormType": "varchar",
      "isSystem": false,
      "computedFieldValueType": "decimal",
      "computedFieldTriggerConfig": [
        {
          "modelName": "paymentCollectionItemDetail",
          "moduleName": "fees-portal",
          "operations": [
            "before-insert"
          ]
        }
      ],
      "computedFieldValueProvider": "NoopsEntityComputedFieldProviderService",
      "computedFieldValueProviderCtxt": "{}",
      "required": false,
      "unique": false,
      "index": false,
      "private": false,
      "encrypt": false,
      "encryptionType": null,
      "decryptWhen": null,
      "columnName": null,
      "isUserKey": false
    },
    {
      "name": "mode",
      "displayName": "Mode",
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
    }
  ]
}
```

</details>
