---
# title: Field Metadata Schema
description: Overview of the field metadata schema used in SolidX.
summary: This comprehensive document details field metadata in SolidX, which treats fields as semantic attributes that define how users interact with data in the admin interface. It covers extensive field types including numeric (integer, bigInteger, decimal), text (shortText, longText, richText), temporal (date, dateTime, time), boolean, JSON, media (singleMedia, multipleMedia), specialized types (email, GUID, computed fields), selection fields (static and dynamic), and relation fields (manyToOne, oneToMany, manyToMany). Each field type includes configuration options for validation, default values, encryption, indexing, uniqueness, privacy, and audit tracking, with detailed examples and attribute documentation.
sidebar_position: 3
json_pointer: "/moduleMetadata/models/fields"
jsonpath: "$.moduleMetadata.models[*].fields[*]"
parent_component: models
type: array,
items_type: "object"
items_attributes_doc: "#field-metadata-attributes"
solidx_concerns: [add_field_to_a_model, remove_field_from_a_model]
---

import { IoIosArrowForward } from "react-icons/io";
import { FaCheckCircle } from "react-icons/fa";
import { MdNumbers, MdTextFields, MdCalendarMonth, MdMerge, MdPhotoLibrary,MdSecurity, MdCheckBox, MdFunctions,MdCheckCircle,MdCancel,MdRule } from "react-icons/md";
import { RiSettings3Line,RiShieldKeyholeLine } from "react-icons/ri";     
import { BiData,BiBookContent} from "react-icons/bi";             
import { InfoBox } from '@site/src/common/InfoBox';
import { WarningBox } from '@site/src/common/WarningBox';



# Field Metadata
> **Where it lives**  
> **JSON Pointer:** `/moduleMetadata/models/fields`  
> **JSONPath:** `$.moduleMetadata.models[*].fields[*]`  
> **Parent:** `models` in the `moduleMetadata` of the root of the metadata file

## Overview

Every SolidX model is composed of fields. Fields in SolidX go over and above the standard fields one expects, instead we treat fields as semantic attributes with relevance to how the users interact with that data in our admin interface. 

👉 For a conceptual overview of fields supported in a model, see [Field Management Documentation](../../admin-docs/module-builder/field-management.md).


### Example: Institute + Fee Type Model fields
<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Field Schema
  </summary>

```json
{
  "moduleMetadata": {
    ..., // Module metadata 
    "models": [ // Model metadata array
      { // Institute model metadata
        "singularName": "institute",
        "pluralName": "institutes",
        "displayName": "Institute",
        "description": "Institute records",
        "dataSource": "default",
        "dataSourceType": "postgres",
        "tableName": "fees_portal_institute",
        "userKeyFieldUserKey": "instituteName",
        "isChild": false,
        "enableAuditTracking": true,
        "enableSoftDelete": false,
        "draftPublishWorkflow": false,
        "internationalisation": false,
        "fields": [ // Institute model fields metadata
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
            "enableAuditTracking": false
          },
          ..., // Other fields
        ]
      },
      { // Fee Type model metadata
        "singularName": "feeType",
        "pluralName": "feeTypes",
        "displayName": "Fee Type",
        "description": "Fee Type records",
        "dataSource": "default",
        "dataSourceType": "postgres",
        "tableName": "fees_portal_fee_type",
        "userKeyFieldUserKey": "feeTypeUserKey",
        "isChild": false,
        "enableAuditTracking": true,
        "enableSoftDelete": false,
        "draftPublishWorkflow": false,
        "internationalisation": false,
        "fields": [ // Fee Type model fields metadata
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
            "enableAuditTracking": false
          },
          ... // Other fields
        ]
      },
      ..., // Other models
    ]
  },
  ... // Other metadata
}
```
</details>


##  Field Type (`type`)  

> **This is the most important attribute of a field.**  
> It determines the **behavior, validation, storage, and UI options** for the field.  



  <h3 className=" card-headear-wrapper">
    <MdNumbers size={24}  />

###  Numeric Types
</h3>

| Value    | Reference | Example |
|----------|------------|---------|
| `int`    | [Integer Field](../../admin-docs/module-builder/field-management#integer) | [See Example](#int) |
| `bigint` | [BigInt Field](../../admin-docs/module-builder/field-management#bigint) | [See Example](#bigint-todo) |
| `decimal`| [Decimal Field](../../admin-docs/module-builder/field-management#decimal) | [See Example](#decimal) |



  <h3 className=" card-headear-wrapper">
    <MdTextFields size={24}  />

###  Text Types
</h3>

| Value       | Reference | Example |
|-------------|-----------|---------|
| `shortText` | [Short Text Field](../../admin-docs/module-builder/field-management#shorttext) | [See Example](#shorttext) |
| `longText`  | [Long Text Field](../../admin-docs/module-builder/field-management#longtext) | [See Example](#longtext) |
| `richText`  | [Rich Text Field](../../admin-docs/module-builder/field-management#richtext) | [See Example](#richtext) |
| `json`      | [JSON Field](../../admin-docs/module-builder/field-management#json) | [See Example](#json) |



  <h3 className=" card-headear-wrapper">
    <FaCheckCircle size={20}  />

### Boolean
</h3>

| Value     | Reference | Example |
|-----------|-----------|---------|
| `boolean` | [Boolean Field](../../admin-docs/module-builder/field-management#boolean) | [See Example](#boolean) |



  <h3 className=" card-headear-wrapper">
    <MdCalendarMonth size={22}  />

### Date / Time Types
</h3>

| Value     | Reference | Example |
|-----------|-----------|---------|
| `date`    | [Date Field](../../admin-docs/module-builder/field-management#date) | [See Example](#date) |
| `datetime`| [Datetime Field](../../admin-docs/module-builder/field-management#datetime) | [See Example](#datetime) |
| `time`    | [Time Field](../../admin-docs/module-builder/field-management#time) | [See Example](#time-todo) |



  <h3 className=" card-headear-wrapper">
    <MdMerge size={24}  />

###  Relation Types
</h3>

| Value         | Reference | Example |
|---------------|-----------| --------|
| `many-to-one`   | [Many To One](../../admin-docs/module-builder/field-management#many-to-one) | [See Example](#many-to-one-relation-child--parent) |
| `one-to-many`   | [One To Many](../../admin-docs/module-builder/field-management#one-to-many) | [See Example](#one-to-many-relation-parent--children) |
| `many-to-many`  | [Many To Many](../../admin-docs/module-builder/field-management#many-to-many) | [See Example](#many-to-many-relation) |


  <h3 className=" card-headear-wrapper">
    <MdPhotoLibrary size={24}  />

###  Media Types
</h3>

| Value         | Reference | Example |
|---------------|-----------| --------|
| `mediaSingle`   | [Single Media Field](../../admin-docs/module-builder/field-management#single-media) | [See Example](#mediasingle) |
| `mediaMultiple` | [Multiple Media Field](../../admin-docs/module-builder/field-management#multiple-media) | [See Example](#mediamultiple) |



  <h3 className=" card-headear-wrapper">
    <MdSecurity size={22}  />

###  Specialized Types
</h3>

| Value     | Reference | Example |
|-----------|-----------|---------|
| `email`   | [Email Field](../../admin-docs/module-builder/field-management#email) | [See Example](#email) |
| `password`| [Password Field](../../admin-docs/module-builder/field-management#password) | [See Example](#password) |



  <h3 className=" card-headear-wrapper">
    <MdCheckBox size={20}  />

###  Selection Types
</h3>

| Value            | Reference | Example |
|------------------|-----------|---------|
| `selectionStatic`  | [Static Selection Field](../../admin-docs/module-builder/field-management#static-selection) | [See Example](#selectionstatic) |
| `selectionDynamic` | [Dynamic Selection Field](../../admin-docs/module-builder/field-management#dynamic-selection) | [See Example](#selectiondynamic) |



  <h3 className=" card-headear-wrapper">
    <MdFunctions size={24}  />

###  Computed
</h3>
| Value      | Reference | Example |
|------------|-----------|---------|
| `computed` | [Computed Field](../../admin-docs/module-builder/field-management#computed) | [See Example](#computed-1) |


## Field Metadata Examples
  <h3 className=" card-headear-wrapper">
    <MdNumbers size={24}  />

###  Numeric Types
</h3>

#### 1. int
**Purpose**: For whole numbers (positive/negative)  
**Database**: `integer` column  
**UI Component**: Number input field  
**Use Cases**: Counts, quantities, IDs, rankings

```json
{
  "name": "studentCount",
  "displayName": "Student Count",
  "type": "int",
  "ormType": "integer",
  "min": 0,
  "max": 10000,
  "defaultValue": 0,
  "required": true
}
```
**Key Properties**:
- `min`: Lower bound
- `max`: Upper bound
- `defaultValue`: Initial value on create


#### 2. decimal
**Purpose**: For decimal/floating point numbers  
**Database**: `decimal` column  
**UI Component**: Decimal input field  
**Use Cases**: Prices, percentages, measurements, financial amounts

```json
{
  "name": "feeAmount",
  "displayName": "Fee Amount",
  "type": "decimal",
  "ormType": "decimal",
  "min": 0,
  "max": 100000,
  "defaultValue": "0.00",
  "required": true,
}
```
**Key Properties**:
- `min`: Lower bound
- `max`: Upper bound
- `defaultValue`: Initial value on create

#### 3. bigint (TODO)

  <h3 className=" card-headear-wrapper">
    <MdTextFields size={24}  />

###  Text Types
</h3>


#### 1. shortText
**Purpose**: For shorter text content (typically up to 1000 characters)  
**Database**: `varchar` column  
**UI Component**: Text input field  
**Use Cases**: Names, titles, identifiers, short descriptions

```json
{
  "name": "instituteName",
  "displayName": "Institute Name",
  "type": "shortText",
  "ormType": "varchar",
  "min": null,
  "max": 256,
  "required": true,
  "unique": true,
  "index": true,
  "isUserKey": true
}
```

**Key Properties**:
- `min`/`max`: Character limits
- `unique`: Enforce uniqueness
- `index`: Database performance optimization
- `isUserKey`: Use as record identifier

#### 2. longText
**Purpose**: For multi-line text content of any length  
**Database**: `text` column  
**UI Component**: Textarea field  
**Use Cases**: Descriptions, comments, notes, multi-paragraph content

```json
{
  "name": "description",
  "displayName": "Description",
  "type": "longText",
  "ormType": "text",
  "regexPattern": "^[a-zA-Z0-9\\s]*$",
  "regexPatternNotMatchingErrorMsg": "Only alphanumeric characters and spaces allowed",
  "min": 10,
  "max": 5000,
  "required": false
}
```

**Key Properties**:
- `regexPattern`: Validation pattern
- `regexPatternNotMatchingErrorMsg`: Custom validation error message
- Supports longer content than `shortText`

#### 3. richText
**Purpose**: For formatted text with HTML support  
**Database**: `text` column  
**UI Component**: Rich text editor (HTML)  
**Use Cases**: Content with formatting, FAQs, policies, documentation

```json
{
  "name": "privacyPolicy",
  "displayName": "Privacy Policy",
  "type": "richText",
  "ormType": "text",
  "required": false,
}
```

**Key Properties**:
- Supports HTML formatting
- No length restrictions
- Rich editing capabilities in UI

<h3 className=" card-headear-wrapper">
    <FaCheckCircle size={20}  />

### Boolean
</h3>

#### 1. boolean
**Purpose**: For true/false values  
**Database**: `boolean` column  
**UI Component**: Checkbox or toggle switch  
**Use Cases**: Flags, settings, yes/no options, status indicators

```json
{
  "name": "isActive",
  "displayName": "Is Active",
  "type": "boolean",
  "ormType": "boolean",
  "defaultValue": true,
  "required": true
}
```

**Key Properties**:
- `defaultValue`: `true` or `false`
- Simple on/off state management

<h3 className=" card-headear-wrapper">
    <MdCalendarMonth size={22}  />

### Date / Time Types
</h3>

#### 1. date
**Purpose**: For date values only (no time)  
**Database**: `date` column  
**UI Component**: Date picker  
**Use Cases**: Birth dates, deadlines, event dates

```json
{
  "name": "dueDate",
  "displayName": "Due Date",
  "type": "date",
  "ormType": "date",
  "required": true,
  "defaultValue": null
}
```

#### 2. datetime
**Purpose**: For date and time values  
**Database**: `timestamp` column  
**UI Component**: DateTime picker  
**Use Cases**: Created/updated timestamps, scheduled events, appointments

```json
{
  "name": "registeredAt",
  "displayName": "Registered At",
  "type": "datetime",
  "ormType": "timestamp",
  "required": true,
  "enableAuditTracking": true
}
```

#### 3. time (TODO)

<h3 className=" card-headear-wrapper">
    <MdMerge size={24}  />

###  Relation Types
</h3>

**Purpose**: Establish relationships between models  
**Database**: Foreign key columns or junction tables  
**UI Component**: Related record selector  
**Use Cases**: Parent-child relationships, data linking

**Supported Types** i.e attribute (`relationType`):
 - `many-to-one`: Many records link to one parent (e.g., Orders → Customer)
 - `one-to-many`: One record has many children (e.g., Customer → Orders)
 - `many-to-many`: Many records link to many others via a junction table (e.g., Students ↔ Courses)

#### 1. Many-to-One Relation (Child → Parent)
```json
{
  "name": "institute",
  "displayName": "Institute",
  "type": "relation",
  "relationType": "many-to-one",
  "relationCoModelSingularName": "institute",
  "relationCoModelColumnName": null,
  "relationModelModuleName": "fees-portal",
  "relationCascade": "cascade",
  "required": true
}
```

#### 2. One-to-Many Relation (Parent → Children)
```json
{
  "name": "feeTypes",
  "displayName": "Fee Types",
  "type": "relation",
  "relationType": "one-to-many",
  "relationCoModelSingularName": "feeType",
  "relationCoModelFieldName": "institute",
  "relationCoModelColumnName": "instituteId",
  "relationModelModuleName": "fees-portal",
  "relationCreateInverse": true
}
```

#### 3. Many-to-Many Relation
```json
{
  "name": "categories",
  "displayName": "Categories",
  "type": "relation",
  "relationType": "many-to-many",
  "relationCoModelSingularName": "category",
  "relationModelModuleName": "fees-portal",
  "relationJoinTableName": "fee_category_junction",
  "isRelationManyToManyOwner": true,
  "relationCreateInverse": true
}
```

**Key Properties**:
- `relationType`:  "one-to-many", "many-to-one", "many-to-many"
- `relationCoModelSingularName`: Target model name
- `relationCoModelColumnName`: Foreign key column name
- `relationJoinTableName`: Junction table for many-to-many
- `relationCascade`: Cascade behavior for deletes
- `relationCreateInverse`: Auto-create inverse relationship

Give an example of inverse vs non-inverse relation creation (TODO)

<h3 className=" card-headear-wrapper">
    <MdPhotoLibrary size={24}  />

###  Media Types
</h3>


#### 1. mediaSingle
**Purpose**: Single file/image upload  
**UI Component**: File upload with preview  
**Use Cases**: Profile pictures, logos, single documents

```json
{
  "name": "logo",
  "displayName": "Logo",
  "type": "mediaSingle",
  "mediaTypes": ["image"],
  "mediaMaxSizeKb": 5120,
  "mediaStorageProviderUserKey": "default-aws-s3",
  "required": true
}
```

#### 2. mediaMultiple
**Purpose**: Multiple file uploads  
**UI Component**: Multi-file upload with gallery  
**Use Cases**: Photo galleries, document collections, attachments

```json
{
  "name": "documents",
  "displayName": "Documents",
  "type": "mediaMultiple",
  "mediaTypes": ["image", "document", "pdf"],
  "mediaMaxSizeKb": 10240,
  "mediaStorageProviderUserKey": "default-aws-s3",
  "required": false
}
```

**Key Properties**:
- `mediaTypes`: Array of allowed file types
- `mediaMaxSizeKb`: Maximum file size per file
- `mediaStorageProviderUserKey`: [Storage configuration reference](../../admin-docs/media-library/storage-providers.md)

<h3 className=" card-headear-wrapper">
    <MdSecurity size={22}  />

###  Specialized Types
</h3>

#### 1. email
**Purpose**: Email addresses with validation  
**Database**: `varchar`  
**UI Component**: Email input field  
**Use Cases**: User contact information, notifications

```json
{
  "name": "email",
  "displayName": "Email Address",
  "type": "email",
  "ormType": "varchar",
  "required": true,
  "unique": true,
  "index": true
}
```

#### 2. json
**Purpose**: Store complex JSON data structures  
**Database**: `text`/`jsonb`  
**UI Component**: JSON editor or code field  
**Use Cases**: Flexible data structures, API responses, configurations

```json
{
  "name": "metadata",
  "displayName": "Metadata",
  "type": "json",
  "ormType": "jsonb",
  "required": false,
  "defaultValue": "{}"
}
```

#### 3. password
**Purpose**: Secure password storage with hashing  
**Database**: `varchar` (hashed)  
**UI Component**: Password input field  
**Use Cases**: User authentication, secure credentials

```json
{
  "name": "password",
  "displayName": "Password",
  "type": "password",
  "ormType": "varchar",
  "min": 8,
  "max": 128,
  "required": true,
  "regexPattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$",
}
```

<h3 className=" card-headear-wrapper">
    <MdCheckBox size={20}  />

###  Selection Types
</h3>

#### 1. selectionStatic
**Purpose**: Dropdown with predefined options  
**Database**: `varchar` column  
**UI Component**: Dropdown/select field  
**Use Cases**: Status options, categories, fixed lists

```json
{
  "name": "latePaymentFeesType",
  "displayName": "Late Payment Fees Type",
  "type": "selectionStatic",
  "ormType": "varchar",
  "selectionStaticValues": [
    "None:None",
    "Percent:Percent",
    "Absolute:Absolute"
  ],
  "selectionValueType": "string",
  "defaultValue": "None",
  "required": true
}
```

**Format**: `"value:label"` where value is stored in DB, label is displayed in UI

#### 2. selectionDynamic
**Purpose**: Dropdown populated from API/database query  
**Database**: `varchar` column  
**UI Component**: Dynamic dropdown field  
**Use Cases**: Related data, user lists, dynamic categories

```json
{
  "name": "studentId",
  "displayName": "Student",
  "type": "selectionDynamic",
  "ormType": "varchar",
  "selectionDynamicProvider": "StudentListProvider",
  "selectionDynamicProviderCtxt": "{\"filters\": {\"isActive\": true}}",
  "required": true
}
```

**Key Properties**:
- `selectionDynamicProvider`: Provider class responsible for returning the dynamic dropdown options
- `selectionDynamicProviderCtxt`: JSON context/config passed to the provider

<h3 className=" card-headear-wrapper">
    <MdFunctions size={24}  />

###  Computed
</h3>

#### 1. computed
**Purpose**: Auto-calculated values from other fields  
**Database**: `varchar`/`decimal`/etc. (based on result type)  
**UI Component**: Read-only display field  
**Use Cases**: Calculated totals, formatted names, derived values

```json
{
  "name": "fullName",
  "displayName": "Full Name",
  "type": "computed",
  "ormType": "varchar",
  "computedFieldValueType": "string",
  "computedFieldTriggerConfig": [
    {
      "modelName": "student",
      "moduleName": "fees-portal",
      "operations": ["before-insert", "before-update"]
    }
  ],
  "computedFieldValueProvider": "ConcatEntityComputedFieldProvider",
  "computedFieldValueProviderCtxt": "{\"fields\":[\"firstName\",\"lastName\"],\"separator\":\" \"}",
  "required": true
}
```

**Key Properties**:
- `computedFieldValueType`: Result data type
- `computedFieldTriggerConfig`: When to recalculate
- `computedFieldValueProvider`: Computation service provider class
- `computedFieldValueProviderCtxt`: JSON configuration for provider


## Common Field Metadata Attributes
All field types support these common properties:

<h3 className=" card-headear-wrapper">
    <RiSettings3Line size={24}  />

### Core Properties
</h3>

- `name`: Internal field reference (camelCase)
- `displayName`: User-friendly UI label
- `description`: Optional documentation
- `type`: Field type identifier
- `ormType`: Database column type
- `isSystem`: System-managed field flag
- `required`: Mandatory field flag
- `unique`: Uniqueness constraint
- `index`: Database index creation
- `private`: Hidden from UI flag (Not yet implemented)
- `defaultValue`: Default field value

<h3 className=" card-headear-wrapper">
    <RiShieldKeyholeLine size={24}  />

### Security Properties
</h3>

- `encrypt`: Enable field encryption (Not yet implemented)
- `encryptionType`: Encryption method (AES, bcrypt, etc.) (Not yet implemented)
- `decryptWhen`: When to decrypt ("always", "admin_only", "never") (Not yet implemented)

<h3 className=" card-headear-wrapper">
    <BiData size={24}  />

### Database Properties
</h3>

- `columnName`: Custom database column name
- `enableAuditTracking`: Include in audit logs

<h3 className=" card-headear-wrapper">
    <MdRule size={24}  />

### Validation Properties
</h3>

- `min`/`max`: Value/length constraints
- `regexPattern`: Custom validation pattern
- `regexPatternNotMatchingErrorMsg`: Custom error message

##  Field Metadata Attributes

### `name` *(string, required)*
Name of the field (column/property).  
**Default:** N/A



### `displayName` *(string, required)*
Human-readable label for UI and docs.  
**Default:** N/A



### `description` *(string, optional)*
Short help/purpose text shown in UI or docs.  
**Default:** N/A



### `type` *(SolidFieldType, required)*
Refer to [Field Type](#-field-type-type) section above.

**Default:** N/A



### `modelId` *(number, optional)*
Numeric id of the owning model (internal linkage).  
**Default:** N/A



### `ormType` *(PSQLType, optional)*
Override database column type. Use only when the default mapping from `type` is insufficient.  
**Values:** 
- integer
- decimal
- bigint
- varchar
- text
- boolean
- timestamp
- timestamptz
- time
- date
- json
- jsonb  
**Default:** Derived from `type`

<!-- --- -->

<!-- ### `length` *(number, optional)*
Max length/size where relevant.  
**Applies to:** shortText, longText, richText, json  
**Default:** N/A -->



### `defaultValue` *(string, optional)*
Literal default value applied on create.  
**Default:** N/A



### `regexPattern` *(string, optional)*
Validation pattern for textual inputs.  
**Applies to:** shortText, longText, email, password  
**Default:** N/A



### `regexPatternNotMatchingErrorMsg` *(string, optional)*
Custom error message when `regexPattern` fails.  
**Default:** N/A



### `required` *(boolean, optional)*
Marks field as mandatory.  
**Default:** false



### `unique` *(boolean, optional)*
Enforces uniqueness.  
**Default:** false



### `encrypt` *(boolean, optional)*
Enable symmetric encryption-at-rest for this field.  
**Default:** false



<InfoBox>
 Feature coming soon!
</InfoBox>



### `encryptionType` *(enum, optional)*
Only if `encrypt = true`.  
**Values:** 
- aes-128
- aes-256  
**Default:** aes-256 (recommended)



<InfoBox>
 Feature coming soon!
</InfoBox>



### `decryptWhen` *(enum, optional)*
Only if `encrypt = true`. Controls when plaintext is produced.  
**Values:** 
- before-transit
- after-transit  
**Default:** after-transit


<InfoBox>
 Feature coming soon!
</InfoBox>



### `index` *(boolean, optional)*
Add an index for search/sort (where supported).  
**Not applicable to:** richText, longText  
**Default:** false



### `max` *(number, optional)*
Upper bound (number/date) or maximum length (text/json).  
**Applies to:** shortText, longText, richText, json, int, decimal, date, datetime, time  
**Default:** N/A



### `min` *(number, optional)*
Lower bound (number/date) or minimum length (text/json).  
**Applies to:** shortText, longText, richText, json, int, decimal, date, datetime, time  
**Default:** N/A



### `private` *(boolean, optional)*
Exclude from default listings/exports; require elevated access.  
**Default:** false


<InfoBox>
 Feature coming soon!
</InfoBox>



### `mediaTypes` *(MediaType[], optional)*
Allowlist of media categories.  
**Applies to:** mediaSingle, mediaMultiple  
**Values:** 
- image
- audio
- video
- file  
**Default:** All sensible for the field type



### `mediaMaxSizeKb` *(number, optional)*
Max upload size per item in kilobytes.  
**Applies to:** mediaSingle, mediaMultiple  
**Default:** N/A



### `mediaStorageProviderId` *(number, optional)*
Numeric id of configured media storage provider.  
**Applies to:** mediaSingle, mediaMultiple  
**Default:** Module/provider default



### `mediaStorageProviderUserKey` *(string, optional)*
Name/userKey of configured media storage provider.  
**Applies to:** mediaSingle, mediaMultiple  
**Default:** default-filesystem





<InfoBox>
  By default, SolidX applications gets seeded with 2 media storage providers i.e default-filesystem and default-aws-s3. You can create more providers as per your requirements. You can refer to the [Storage Provider Documentation](../../admin-docs/media-library/storage-providers.md) for more details.
</InfoBox>




### `relationType` *(RelationType, optional)*
Kind of relation.  
**Applies to:** relation  
**Values:** 
- many-to-one
- many-to-many
- one-to-many  
**Default:** N/A



### `relationCoModelSingularName` *(string, optional)*
`singularName` of the related co-model.  
**Applies to:** relation  
**Default:** N/A



### `relationCreateInverse` *(boolean, optional)*
Generate inverse side on co-model.  
**Applies to:** relation  
**Default:** false








<WarningBox>
  Currently we auto-create the inverse side of the field metadata on the co-model. In future releases, we will get rid of the inverse field auto-creation and instead have the user explicitly create the inverse field on the co-model. This is to ensure that the user has full control on how the inverse field is created on the co-model and keep things explicit and simple
</WarningBox>



### `relationCascade` *(CascadeType, optional)*
Only if `type = relation` and `relationCreateInverse = true`.
Cascade behavior for persistence i.e (create/update) and deletion.  
**Applies to:** relation  
**Values:** 
- set null
- restrict
- cascade  
**Default:** restrict (recommended explicitness)



### `relationModelModuleName` *(string, optional)*
Only if `type = relation` and `relationCreateInverse = true` and the related co-model lives in a **different module**.
Module name if the related co-model lives in a **different module**.  
**Applies to:** relation  
**Default:** Current module



### `relationCoModelFieldName` *(string, mandatory for many-to-many)*
Only if `type = relation` and `relationCreateInverse = true`.
For m2m or cross-model relations, the other side's field name.  
Auto-inferred for many-to-one but required for many-to-many.
**Applies to:** relation  
**Default:** Auto-inferred for many-to-one



### `isRelationManyToManyOwner` *(boolean, mandatory for many-to-many)*
Only if `type = relation` and `relationType = many-to-many`.
Marks this side as the **owner** of the many-to-many.
At least one side must be the owner, otherwise the many-to-many relation will not work.  
**Applies to:** relation (many-to-many)  
**Default:** false





<InfoBox>
  TODO: change default to true in future releases
</InfoBox>

### `relationFieldFixedFilter` *(string, optional)*
Fixed filter (JSON) applied when fetching related records from the admin ui. This can be used to apply static as well as dynamic filters when we want to conditionally filter the values shown for the related records

The filter is a JSON object of schema type BasicFilterDto:
<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Filter schema
  </summary>

```ts
export enum SoftDeleteFilter {
    INCLUSIVE = "inclusive",
    EXCLUSIVE = "exclusive",
}

export class BasicFilterDto extends PaginationQueryDto {

    @IsOptional()
    @ApiProperty({ description: "Fields" })
    readonly fields?: string[];

    @IsOptional()
    @ApiProperty({ description: "sort" })
    readonly sort?: string[];

    @IsOptional()
    @ApiProperty({ description: "groupBy" })
    readonly groupBy?: string[];


    @IsOptional()
    @ApiProperty({ description: "populate" })
    readonly populate?: string[];


    @IsOptional()
    @ApiProperty({ description: "populateMedia" })
    readonly populateMedia?: string[];

    @IsOptional()
    @IsEnum(SoftDeleteFilter)
    @ApiProperty({
        description: "showSoftDeleted",
        enum: SoftDeleteFilter,
    })
    readonly showSoftDeleted?: SoftDeleteFilter;

    @IsOptional()
    @ApiProperty({ description: "populateGroup" })
    readonly populateGroup?: boolean;

    @IsOptional()
    @ApiProperty({ description: "groupFilter" })
    groupFilter?: BasicFilterDto

    @IsOptional()
    @ApiProperty({ description: "locale" })
    readonly locale?: string;

    @IsOptional()
    @ApiProperty({ description: "status publish draft" })
    readonly status?: string;
}

export class PaginationQueryDto {
    constructor(limit: number, offset: number) {
        this.limit = limit;
        this.offset = offset;
    }

    @IsOptional()
    @Type(() => Number)
    @IsPositive()
    limit?: number = 10;

    @IsOptional()
    @Type(() => Number)
    @IsInt()
    @Min(0)
    offset?: number = 0;

    @IsOptional()
    filters?: Record<string, any>;
}
```
</details>

**Applies to:** relation  
**Default:** N/A



### `selectionDynamicProvider` *(string, optional)*
Provider identifier for loading dynamic options.
**Applies to:** selectionDynamic  
**Default:** N/A



### `selectionDynamicProviderCtxt` *(string, optional)*
Context/config passed to the dynamic provider.
**Applies to:** selectionDynamic  
**Default:** N/A



### `selectionStaticValues` *(string[], optional)*
List of static options in `key:Label` format.  
**Applies to:** selectionStatic  
**Default:** N/A



### `selectionValueType` *(enum, optional)*
Primitive type of selection values.  
**Applies to:** selectionStatic, selectionDynamic  
**Values:** 
- string
- int  
**Default:** string



### `computedFieldValueProvider` *(string, optional)*
Provider/class that computes the field value.  
**Applies to:** computed  
**Default:** N/A



### `computedFieldValueProviderCtxt` *(string, optional)*
Context/config passed to the computed value provider.  
**Applies to:** computed  
**Default:** N/A



### `computedFieldValueType` *(enum, optional)*
Declared output type of the computed field.  
**Applies to:** computed  
**Values:** 
- string
- int
- decimal
- boolean
- date
- datetime  
**Default:** string



### `computedFieldTriggerConfig` *(array of objects, optional)*
Operations that trigger compute and the trigger model/module to attach to. This is useful when the computed field depends on relations or other models and needs to be re-computed when those models change.
<!-- <summary> Config schema</summary> -->
**Config schema**

``` tsx
export class ComputedFieldTriggerConfig {
  moduleName: string; // Name of the module which should trigger the computed field re-evaluation
  modelName: string; // Name of the model which should trigger the computed field re-evaluation
  operations: ComputedFieldTriggerOperation[]; // List of operations on the model, when computed field should be re-evaluated
}
```
**Operations values:** 
- before-insert
- after-insert
- before-update
- after-update
- before-delete
- after-delete  
**Applies to:** computed  
**Default:** N/A



<!-- ### `uuid` *(string, optional)*
Explicit UUID for this field definition (rarely needed).  
**Default:** Auto-generated -->



### `isSystem` *(boolean, optional)*
System fields are excluded from code generation (hand-written code assumed).  
**Default:** false



### `isMarkedForRemoval` *(boolean, optional)*
Soft-removal flag for the field definition. Fields marked for removal are excluded from code generation.
**Default:** false


<InfoBox>
 This flag enables the code builder to identify fields that need to be deleted from the codebase. They are deleted after code generation is complete.  
</InfoBox>


### `columnName` *(string, optional)*
Override database column name.  
**Default:** Derived from `name`



### `relationCoModelColumnName` *(string, optional)*
Override co-model's column name for relation bindings.  
**Applies to:** relation  
**Default:** Auto-generated/inferred



### `isUserKey` *(boolean, optional)*
Marks this field as the **user key** (friendly identifier).

Further Reference:
- [Model User Keys Explained](./model-metadata.md#userkeyfielduserkey-string-optional-ie-the-user-key-field-name) 

**Default:** false



### `relationJoinTableName` *(string, optional)*
Custom join table name for many-to-many.  
**Applies to:** relation (many-to-many)  
**Default:** Auto-generated



### `enableAuditTracking` *(boolean, optional)*
Track create/update/delete for this field in audit logs.  
**Default:** false



### `isMultiSelect` *(boolean, optional)*
Allow multiple selected values (UI + storage impact).  
**Applies to:** selection fields and some primitives depending on UI policy  
**Default:** false



## Implementation Notes & Gotchas

- **`ormType` vs `type`** — Prefer defaults derived from `type`. Override `ormType` only when you need a specific DB type (e.g., `jsonb` instead of `json`).  
- **`unique` + `index`** — `unique` usually implies an index; still set `index: true` for frequent filter columns that aren’t unique.  
<!-- - **Encryption** — Prefer `aes-256` unless you have legacy constraints. Keep `decryptWhen: after-transit` to minimize plaintext exposure between services.   -->
<!-- - **Privacy** — `private: true` hides in default listings/exports but does not bypass access control; combine with security rules where needed.   -->
- **User key** — Set `isUserKey: true` on the one field that identifies a record best for humans (e.g., `instituteName`).  
- **Selection fields** — Ensure storage matches UI: arrays for multi-select; validate that `selectionValueType` aligns with downstream consumers.  
- **Relations** — Always specify `relationCascade` explicitly; implicit defaults differ across ORMs/DBs. For many-to-many, define the **owner** side to control join-table updates.  
- **Computed** — Providers should be idempotent and side‑effect free. For pre-compute operations e.g (before-insert, before-update, before-remove), provider needs to set the value on the entity object directly i.e (since in pre-compute operations, the assumption is that the computed field entity and the triggering entity are the same). For post-compute operations e.g (after-insert, after-update, after-remove), provider needs to use the entity manager in the provider implementation to update the entity since in post-compute operations, the assumption is that the computed field entity and the triggering entity can be different.
- **Media** — Validate MIME and size server-side. `mediaTypes` is an allowlist, not a guarantee of safety. Consider thumbnailing and antivirus for file uploads.

<h2 className=" card-headear-wrapper">
    <BiBookContent size={24} style={{ marginRight: "10px" }} />

## Cheat Sheet
</h2>


```
┌─────────────────────────────────────┐
│           DATA TYPE?                │
├─────────────────────────────────────┤
│ TEXT:                              │
│ ├── Short (< 1000 chars) → shortText │
│ ├── Long/Multi-line → longText      │
│ └── Formatted/HTML → richText       │
├─────────────────────────────────────┤
│ NUMBERS:                           │
│ ├── Whole numbers → int             │
│ └── Decimals → decimal              │
├─────────────────────────────────────┤
│ CHOICES:                           │
│ ├── Fixed options → selectionStatic │
│ └── Dynamic data → selectionDynamic │
├─────────────────────────────────────┤
│ RELATIONSHIPS:                     │
│ ├── One-to-One → relation           │
│ ├── One-to-Many → relation          │
│ ├── Many-to-One → relation          │
│ └── Many-to-Many → relation         │
├─────────────────────────────────────┤
│ FILES:                             │
│ ├── Single file → mediaSingle       │
│ └── Multiple files → mediaMultiple  │
├─────────────────────────────────────┤
│ CALCULATED:                        │
│ └── Auto-computed → computed        │
├─────────────────────────────────────┤
│ SPECIAL:                           │
│ ├── True/False → boolean           │
│ ├── Date only → date               │
│ ├── Date+Time → datetime           │
│ ├── Password → password            │
│ ├── Email → email                  │
│ ├── Phone → phone                  │
│ └── Complex data → json            │
└─────────────────────────────────────┘
```


<!-- ## Quick Matrix (What applies where?)

| Aspect                | Text(short/long/rich)                 | Number(int/decimal/bigint) | Date/time | Relation | Media | Selection | Computed |
|-----------------------|------------------------                |-----------------------------|-----------|---------|-------|-----------|----------|
| `length`              | <MdCheckCircle className="icon-yes" />                     | <MdCancel className="icon-no" />                           | <MdCancel className="icon-no" />         | <MdCancel className="icon-no" />       | <MdCancel className="icon-no" />     | <MdCancel className="icon-no" />         | <MdCancel className="icon-no" />        |
| `min` / `max`         | <MdCheckCircle className="icon-yes" />                           | <span className="table-icon-with-text"> <MdCheckCircle className="icon-yes" /> (range) </span>                    | <span className="table-icon-with-text"> <MdCheckCircle className="icon-yes" /> (bounds) </span>  | <MdCancel className="icon-no" />      | <MdCancel className="icon-no" />     | <MdCancel className="icon-no" />         | <MdCancel className="icon-no" />        |
| `regexPattern`        | <MdCheckCircle className="icon-yes" />                                   | <MdCancel className="icon-no" />                           | <MdCancel className="icon-no" />         | <MdCancel className="icon-no" />       | <MdCancel className="icon-no" />     | <MdCancel className="icon-no" />         | <MdCancel className="icon-no" />        |
| `media*`              | <MdCancel className="icon-no" />                                    | <MdCancel className="icon-no" />                           | <MdCancel className="icon-no" />         | <MdCancel className="icon-no" />       | <MdCheckCircle className="icon-yes" />     | <MdCancel className="icon-no" />         | <MdCancel className="icon-no" />        |
| `relation*`           | <MdCancel className="icon-no" />                                     | <MdCancel className="icon-no" />                           | <MdCancel className="icon-no" />         | <MdCheckCircle className="icon-yes" />       | <MdCancel className="icon-no" />     | <MdCancel className="icon-no" />         | <MdCancel className="icon-no" />        |
| `selection*`          | <MdCancel className="icon-no" />                                    | <MdCancel className="icon-no" />                           | <MdCancel className="icon-no" />         | <MdCancel className="icon-no" />       | <MdCancel className="icon-no" />     | <MdCheckCircle className="icon-yes" />         | <MdCancel className="icon-no" />        |
| `computed*`           | <MdCancel className="icon-no" />                                     | <MdCancel className="icon-no" />                           | <MdCancel className="icon-no" />         | <MdCancel className="icon-no" />       | <MdCancel className="icon-no" />     | <MdCancel className="icon-no" />         | <MdCheckCircle className="icon-yes" />        |
| `encrypt`/`private`   | <MdCheckCircle className="icon-yes" />                                    | <MdCheckCircle className="icon-yes" />                            | <MdCheckCircle className="icon-yes" />         | (id only)| file meta| values   | output   |
| `index`               | <span className="table-icon-with-text"> <MdCheckCircle className="icon-yes" /> (except rich/long) </span>                    | <MdCheckCircle className="icon-yes" />                            | <MdCheckCircle className="icon-yes" />         | <MdCheckCircle className="icon-yes" />       | <MdCancel className="icon-no" />     | <MdCheckCircle className="icon-yes" />         | <span className="table-icon-with-text"> <MdCheckCircle className="icon-yes" /> (virtual) </span>     | -->