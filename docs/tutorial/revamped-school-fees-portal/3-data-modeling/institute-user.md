---
sidebar_position: 8
---

# Institute User Model

**Business Purpose:** An extension of the base `User` model, specific to an institute. It links a user to an institute and defines their role within that institute.

**Fields:**

| Field Name | Type | Description |
|---|---|---|
| `userType` | [`selectionStatic`](../../../admin-docs/module-builder/field-management#static-selection) | The type of user (e.g., Mswipe Admin, Institute Admin). |
| `institute` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | A many-to-one relationship to the `institute` model. |


**Metadata JSON:**

<details>
<summary>&emsp; View Metadata JSON</summary>

```json
{
  "singularName": "instituteUser",
  "pluralName": "instituteUsers",
  "displayName": "Institute User",
  "description": "This table allows us to store institute user records",
  "dataSource": "default",
  "dataSourceType": "postgres",
  "tableName": "fees_portal_institute_user",
  "isChild": true,
  "parentModelUserKey": "user",
  "enableAuditTracking": true,
  "enableSoftDelete": false,
  "draftPublishWorkflow": false,
  "internationalisation": false,
  "fields": [
    {
      "name": "userType",
      "displayName": "User Type",
      "description": null,
      "type": "selectionStatic",
      "ormType": "varchar",
      "isSystem": false,
      "defaultValue": "Institute Admin",
      "selectionStaticValues": [
        "Mswipe Admin:Mswipe Admin",
        "Institute Admin:Institute Admin"
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