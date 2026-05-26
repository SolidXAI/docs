---
title: Data Modeling
---

--- 
sidebar_position: 3
---

# Data Modeling
In this step, we will design the data model for our school fees portal. This is the most critical part of building the application, where we define the structure of our data. We'll use SolidX's **App Builder**, a powerful visual tool within the admin panel, to do this.

## Core Concepts of the App Builder

Before we start, let's understand a few key terms:

-   **Module:** A top-level container for a major feature of your application. It groups related data models, UI configurations, and business logic. We will create a `fees-portal` module.
-   **Model:** Represents a single data entity, which translates to a database table. For example, `Student` or `Institute`.
-   **Fields:** The attributes of a model, which translate to columns in a database table. For example, the `Student` model will have fields like `studentName` and `studentEmailAddress`.
-   **Data Source:** A connection to a database. SolidX can connect to multiple databases, but for this tutorial, we'll use the `default` PostgreSQL connection you configured during setup.

## Create a Module

In SolidX, a **Module** is a top-level container that groups related data models, UI configurations, and business logic. The first step in building our application is to create a new module (e.g. School Fees Portal) to house everything related to the school fees portal.

> By default SolidX has `Solid Core` module to allow setup and configure the SolidX application.

To do this, navigate to **Solid Core > App Builder > Module** from the sidebar menu, and then click the **Add** button.

This will open the new module form. Fill in the details as shown in the screenshot below. We will name our module `fees-portal`.

![Create Module](/img/tutorial/school-fees-portal/2-data-model/create-new-module.png)

> **A Note on Data Sources:** When you created the project, SolidX automatically configured a default data source connected to the PostgreSQL database you specified during setup. SolidX supports multiple data sources, allowing you to connect to different databases within the same application.

When creating a module, you can also assign a menu icon to it.

Example default menu icon:
<img src="/downloads/default-logo-icon.png" width="100" alt="Default Menu Icon" />
[Download default menu icon](/downloads/default-logo-icon.png)

### Generate Module Code

Creating the module in the UI simply adds a metadata record to the database. To make the module active in the application, you need to generate its corresponding boilerplate code. This can be done via the UI or the CLI.

**1. Via the UI**

From the module list view, find the `fees-portal` module you just created. Click the context menu (three dots) on that row and select the **"Generate Code"** action.

![Generate Module Code](/img/tutorial/school-fees-portal/2-data-model/module-generate-code.png)

Confirm the action in the dialog box that appears.

![Generate Module Code Confirmation](/img/tutorial/school-fees-portal/2-data-model/module-generate-code-confirmation.png)

Confirming this will generate all the necessary code for the newly bootstrapped project.

> **What does "Generate Code" do?**
> This powerful feature reads the metadata of your module and models and automatically writes the necessary boilerplate code in your `solid-api` project. This includes:
> - Database entity classes.
> - Service classes with CRUD (Create, Read, Update, Delete) methods.
> - Controller classes that expose REST API endpoints.
> - Basic UI views for the admin panel.

**2. Via the CLI**

Alternatively, you can generate the module code from your terminal.

```bash
# Navigate to your backend directory
cd school-fees-portal/solid-api

# Generate code for the module
solid refresh-module -n fees-portal
```

> refresh-module is the SolidX CLI command which takes the name of the module name in -n flag.

## Create Models

With the module in place, we can now define the data models for our application. For each model, you will:
1.  Navigate to **Solid Core > App Builder > Model** and click **Add**.
2.  Fill out the model's basic details (name, display name, etc.) and associate it with the `fees-portal` module.
3.  Add all the required fields to the model.
4.  Generate the code for the model.

![Create Model Sample](/img/tutorial/school-fees-portal/2-data-model/create-model-sample.png)

The following models need to be created. Each is detailed in its own section of this tutorial:
-   **Institute**: Represents an educational institution.
-   **Fee Type**: Defines the different types of fees an institute can charge.
-   **Student**: Represents a student in an institute.
-   **Payment Collection**: A batch of fee collection requests.
-   **Payment Collection Item**: An individual fee item within a collection.
-   **Payment**: Records a payment transaction.
-   **Payment Collection Item Detail**: The breakdown of a payment.
-   **Institute User**: Extends the base User model for institute-specific roles.

### ER Diagram

The following diagram illustrates the relationships between the models in our `fees-portal` module.

![ER-fees-portal](/img/tutorial/school-fees-portal/2-data-model/er-diagrams/fees-portal-er-diagram.png)

### Applying Model Changes

After defining or updating your models, you need to sync these changes with your database and generate the corresponding backend code (entities, DTOs, services, etc.).

You can do this in two ways:

**1. Via the UI**

You can also generate code for each model individually directly from the admin panel. In the model list view, click the context menu on the model you want to generate code for and select **"Generate Code"**. This is the same process you followed for the module.

**2. Via the Command Line**

This is useful for applying changes to multiple models at once.

```bash
# Navigate to your backend directory
cd school-fees-portal/solid-api

# Apply all metadata changes to the database schema
solid seed

# Generate code for a specific model
solid refresh-model -n <model-name>
```

## Fast Track: Using the Module Metadata JSON

Instead of manually creating each model and its fields one-by-one through the App Builder UI, you can use a predefined JSON file to create the entire data structure for the `fees-portal` module in one go. This is a "fast track" method that saves significant time.

The JSON file below contains the complete definition for the module, including all its models (Institute, Fee Type, Student, etc.) and their respective fields and relationships.

**When to use this?**
*   Use this method if you want to quickly set up the application's data model without going through the step-by-step UI process.
*   If you prefer to understand the data modeling process in detail, you can skip this section and follow the manual model creation steps outlined previously.

**Next Steps: Seeding the Database**

1.  **Copy the JSON:** Copy the entire JSON content from the section below and paste it into the metadata file(`solid-api/module-metadata/fees-portal/fees-portal-metadata.json`).

### Module Metadata JSON

<details>
<summary>&emsp; View Module Metadata JSON</summary>

```json 
{
  "moduleMetadata": {
    "name": "fees-portal",
    "displayName": "Fees Portal",
    "description": "Used to keep a track of all fees collections requests",
    "defaultDataSource": "default",
    "menuIconUrl": null,
    "menuSequenceNumber": 2,
    "isSystem": false,
    "models": [
      {
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
        "fields": [
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
            "enableAuditTracking": true
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
          {
            "name": "paymentGatewayMerchantId",
            "displayName": "Cust Code",
            "description": null,
            "type": "shortText",
            "ormType": "varchar",
            "isSystem": false,
            "defaultValue": null,
            "min": null,
            "max": null,
            "required": true,
            "unique": true,
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
            "name": "paymentGatewayAccessKey",
            "displayName": "Access Key",
            "description": null,
            "type": "shortText",
            "ormType": "varchar",
            "isSystem": false,
            "defaultValue": null,
            "min": null,
            "max": null,
            "required": true,
            "unique": true,
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
            "name": "paymentGatewayAccessSecret",
            "displayName": "Access Secret",
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
            "name": "instituteAddress",
            "displayName": "Institute Address",
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
            "enableAuditTracking": true
          },
          {
            "name": "instituteUsers",
            "displayName": "InstituteUsers",
            "description": "InstituteUsers",
            "type": "relation",
            "ormType": "integer",
            "isSystem": false,
            "relationType": "one-to-many",
            "relationCoModelFieldName": "institute",
            "relationCreateInverse": true,
            "relationCoModelSingularName": "instituteUser",
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
            "name": "instituteBrochure",
            "displayName": "Institute Brochure",
            "description": null,
            "type": "mediaSingle",
            "ormType": "varchar",
            "isSystem": false,
            "mediaTypes": [
              "file"
            ],
            "mediaMaxSizeKb": 5120,
            "required": false,
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
            "name": "instituteIntroVideo",
            "displayName": "Institute Intro Video",
            "description": null,
            "type": "mediaSingle",
            "ormType": "varchar",
            "isSystem": false,
            "mediaTypes": [
              "video"
            ],
            "mediaMaxSizeKb": 5120,
            "required": false,
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
            "name": "supportEmail",
            "displayName": "Support Email",
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
            "name": "supportMobile",
            "displayName": "Support Mobile",
            "description": null,
            "type": "shortText",
            "ormType": "varchar",
            "isSystem": false,
            "defaultValue": null,
            "min": 10,
            "max": 10,
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
            "name": "gst",
            "displayName": "GST",
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
            "name": "tnC",
            "displayName": "Terms and Conditions",
            "description": null,
            "type": "richText",
            "ormType": "text",
            "isSystem": false,
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
            "name": "faqs",
            "displayName": "FAQS",
            "description": null,
            "type": "richText",
            "ormType": "text",
            "isSystem": false,
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
            "name": "privacyPolicy",
            "displayName": "Privacy Policy",
            "description": null,
            "type": "richText",
            "ormType": "text",
            "isSystem": false,
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
            "name": "emailDomain",
            "displayName": "Email Domain",
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
            "name": "custUserId",
            "displayName": "Cust UserID",
            "description": "Customer UserID",
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
            "enableAuditTracking": false
          }
        ]
      },
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
            "computedFieldValueProviderCtxt": "{\n  \"fields\": [\n    \"feeType\",\n    \"institute.instituteName\" ],  \"separator\": \"-\", \"slugify\": true}",
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
      {
        "singularName": "student",
        "pluralName": "students",
        "displayName": "Student",
        "description": "This table allows us to store student records institute wise",
        "dataSource": "default",
        "dataSourceType": "postgres",
        "tableName": "fees_portal_student",
        "userKeyFieldUserKey": "studentLoginId",
        "isChild": false,
        "enableAuditTracking": true,
        "enableSoftDelete": false,
        "draftPublishWorkflow": false,
        "internationalisation": false,
        "fields": [
          {
            "name": "studentName",
            "displayName": "Student Name",
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
            "name": "studentEmailAddress",
            "displayName": "Student Email Address",
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
            "name": "studentMobileNumber",
            "displayName": "Student Mobile Number",
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
            "name": "parentName",
            "displayName": "Parent Name",
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
            "name": "parentMobileNumber",
            "displayName": "Parent Mobile Number",
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
            "name": "parentEmailAddress",
            "displayName": "Parent Email Address",
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
            "name": "studentId",
            "displayName": "Student Id",
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
            "name": "payments",
            "displayName": "Payments",
            "description": "Payments",
            "type": "relation",
            "ormType": "integer",
            "isSystem": false,
            "relationType": "one-to-many",
            "relationCoModelFieldName": "student",
            "relationCreateInverse": true,
            "relationCoModelSingularName": "payment",
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
            "name": "otp",
            "displayName": "Otp",
            "description": "This is used to store student otp",
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
            "name": "otpExpiresAt",
            "displayName": "Otp Expires At",
            "description": "This is the time when otp get expired",
            "type": "datetime",
            "ormType": "timestamp",
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
            "name": "token",
            "displayName": "Token",
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
            "name": "studentLoginId",
            "displayName": "Student Login ID",
            "description": "Student Login ID",
            "type": "computed",
            "ormType": "varchar",
            "isSystem": false,
            "computedFieldValueType": "string",
            "computedFieldTriggerConfig": [
              {
                "modelName": "student",
                "moduleName": "fees-portal",
                "operations": [
                  "before-insert"
                ]
              }
            ],
            "computedFieldValueProvider": "AlphaNumExternalIdComputationProvider",
            "computedFieldValueProviderCtxt": "{\n  \"dynamicFieldPrefix\": \"studentName\", \"length\": 5}",
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
            "description": "PaymentCollectionItems",
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
            "description": "Payment Collection Id",
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
            "computedFieldValueProviderCtxt": "{\n  \"dynamicFieldPrefix\": \"name\", \"length\": 5}",
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
            "name": "paymentCollectionItemDetails",
            "displayName": "PaymentCollectionItemDetails",
            "description": "PaymentCollectionItemDetails",
            "type": "relation",
            "ormType": "integer",
            "isSystem": false,
            "relationType": "one-to-many",
            "relationCoModelFieldName": "paymentCollectionItem",
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
            "description": "Mode",
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
      },
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
            "description": "PaymentCollectionItemDetails",
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
      },
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
      },
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
    ]
  }
}
```

</details>

2.  **Run the seed command:** Navigate to your backend directory in your terminal and run the `solid seed` command.

    ```bash
    # Navigate to your backend directory
    cd school-fees-portal/solid-api

    # Run the seed command
    solid seed
    ```

**What does `solid seed` do?**

The `solid seed` command reads the `fees-portal-metadata.json` file and automatically inserts all the module and model definitions into the SolidX database. This is the equivalent of creating each module and model manually via the App Builder UI.

After the seed command completes successfully, the final step is to generate the application code based on this new metadata, just as you would have done if you created the module manually.

```bash

# Generate code for the module

solid refresh-module -n fees-portal

```

This will create all the necessary entity, service, and controller files in your `solid-api` project.

After the code is generated, the SolidX backend will have the necessary files for your new module. You should now see the "Fees Portal" module appear in the main sidebar menu with a default home page.

> **Info**
> 
> If you have started backend using `npm run solidx:dev` it automatically watches for code changes and restarts the backend. Currently SolidX only requires making code changes in backend.
> 

![Module Home Page](/img/tutorial/school-fees-portal/2-data-model/fees-portal-homepage.png)
