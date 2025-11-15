---
sidebar_position: 4
---

# Payment Collection Model

**Business Purpose:** Represents a batch of fee collection requests, often initiated by uploading a file. It groups multiple fee items for an institute.

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


**Metadata JSON:**

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
      "computedFieldValueProviderCtxt": "{\n  \"dynamicFieldPrefix\": \"name\",
  \"length\": 5
}",
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

**Apply Changes:** Apply model changes as guided in Data Modeling page.
