---
sidebar_position: 8
---

# Institute User Model

**Business Purpose:** An extension of the base `User` model, specific to an institute. It links a core system user to an institute and defines their role within that institute (e.g., "Institute Admin").

**Fields:**

| Field Name | Type | Description |
|---|---|---|
| `userType` | [`selectionStatic`](../../../admin-docs/module-builder/field-management#static-selection) | The type of user (e.g., Institute Admin). |
| `institute` | [`relation`](../../../admin-docs/module-builder/field-management#relation) | A many-to-one relationship to the `institute` model. |

---

### Key Fields Explained

-   **Child Model (`isChild: true`):** This is a special type of model in SolidX. Notice the `isChild: true` and `parentModelUserKey: "user"` properties in the JSON. This tells SolidX that `InstituteUser` is not a standalone entity; instead, it **extends** the built-in `User` model from the Solid Core module.
-   **How it Works:** When you create a new `User` in the system, you can now also create an associated `InstituteUser` record for them. This allows you to add institute-specific properties (like `userType` and the `institute` they belong to) to a core user, which is a powerful pattern for multi-tenancy. A single user could potentially have roles in multiple institutes by having multiple `InstituteUser` records.

---

### Creation Steps

If you are following the manual "Guided Tour", follow these steps to create the `Institute User` model in the App Builder.

1.  Navigate to **Fees Portal > App Builder > Model** and click **Add**.
2.  Fill in the primary details for the model:
    -   **Singular Name:** `instituteUser`
    -   **Plural Name:** `instituteUsers`
    -   **Display Name:** `Institute User`
    -   **Is Child Model:** Check this box.
    -   **Parent Model:** Select `user` from the dropdown.
3.  Go to the **Fields** tab.
4.  Click **Add Field** and create each field exactly as defined in the table above.
5.  Click **Save**.

:::info You're Done with Data Modeling!
Once you have created this final model, you have finished the data modeling stage. The last step is to generate the code for all the new models you've created. In your `solid-api` terminal, run:

`solid refresh-module -n fees-portal`

This command will create all the necessary backend files for your new models. After it completes and the server restarts, you will see all your new models appear in the sidebar under the "Fees Portal" menu.
:::

---

:::tip For the Fast Track: Model Metadata
The JSON block below contains the complete metadata definition for the **Institute User** model.

This definition is structured with top-level properties for the model itself (like `singularName`, `pluralName`, `tableName`) and a `fields` array that defines every attribute you see in the table above.

You can use this metadata as part of the "Fast Track" approach by including it in the main `fees-portal-metadata.json` file.
:::

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
      "relationCoModelFieldName": "instituteUsers",
      "relationCreateInverse": true,
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
