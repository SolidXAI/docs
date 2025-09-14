# SolidX Field Types Reference Guide

This guide provides comprehensive documentation for all field types supported in SolidX platform metadata, with real examples from the fees-portal module.

## 1. TEXT FIELD TYPES

### shortText
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

### longText
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

### richText
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
  "private": false
}
```

**Key Properties**:
- Supports HTML formatting
- No length restrictions
- Rich editing capabilities in UI

## 2. NUMERIC FIELD TYPES

### int
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

### decimal
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
  "precision": 10,
  "scale": 2
}
```

**Key Properties**:
- `precision`: Total number of digits
- `scale`: Number of decimal places
- Supports financial calculations

## 3. BOOLEAN FIELD TYPES

### boolean
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

## 4. DATE/TIME FIELD TYPES

### date
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

### datetime
**Purpose**: For date and time values  
**Database**: `timestamp` column  
**UI Component**: DateTime picker  
**Use Cases**: Created/updated timestamps, scheduled events, appointments

```json
{
  "name": "createdAt",
  "displayName": "Created At",
  "type": "datetime",
  "ormType": "timestamp",
  "defaultValue": "CURRENT_TIMESTAMP",
  "required": true,
  "enableAuditTracking": true
}
```

## 5. SELECTION FIELD TYPES

### selectionStatic
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

### selectionDynamic
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
- `selectionDynamicProvider`: Service class for data retrieval
- `selectionDynamicProviderCtxt`: JSON configuration for provider

## 6. RELATION FIELD TYPES

### relation (one-to-one, one-to-many, many-to-one, many-to-many)
**Purpose**: Establish relationships between models  
**Database**: Foreign key columns or junction tables  
**UI Component**: Related record selector  
**Use Cases**: Parent-child relationships, data linking

#### Many-to-One Relation (Child → Parent)
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

#### One-to-Many Relation (Parent → Children)
```json
{
  "name": "feeTypes",
  "displayName": "Fee Types",
  "type": "relation",
  "relationType": "one-to-many",
  "relationCoModelSingularName": "feeType",
  "relationCoModelColumnName": "instituteId",
  "relationModelModuleName": "fees-portal",
  "relationCreateInverse": true
}
```

#### Many-to-Many Relation
```json
{
  "name": "categories",
  "displayName": "Categories",
  "type": "relation",
  "relationType": "many-to-many",
  "relationCoModelSingularName": "category",
  "relationModelModuleName": "fees-portal",
  "relationJoinTableName": "fee_category_junction",
  "isRelationManyToManyOwner": true
}
```

**Key Properties**:
- `relationType`: "one-to-one", "one-to-many", "many-to-one", "many-to-many"
- `relationCoModelSingularName`: Target model name
- `relationCoModelColumnName`: Foreign key column name
- `relationJoinTableName`: Junction table for many-to-many
- `relationCascade`: Cascade behavior for deletes
- `relationCreateInverse`: Auto-create inverse relationship

## 7. MEDIA FIELD TYPES

### mediaSingle
**Purpose**: Single file/image upload  
**Database**: `varchar` (file path/URL)  
**UI Component**: File upload with preview  
**Use Cases**: Profile pictures, logos, single documents

```json
{
  "name": "logo",
  "displayName": "Logo",
  "type": "mediaSingle",
  "ormType": "varchar",
  "mediaTypes": ["image"],
  "mediaMaxSizeKb": 5120,
  "mediaStorageProviderUserKey": "default-aws-s3",
  "required": true
}
```

### mediaMultiple
**Purpose**: Multiple file uploads  
**Database**: `text` (JSON array of file paths)  
**UI Component**: Multi-file upload with gallery  
**Use Cases**: Photo galleries, document collections, attachments

```json
{
  "name": "documents",
  "displayName": "Documents",
  "type": "mediaMultiple",
  "ormType": "text",
  "mediaTypes": ["image", "document", "pdf"],
  "mediaMaxSizeKb": 10240,
  "mediaStorageProviderUserKey": "default-aws-s3",
  "required": false
}
```

**Key Properties**:
- `mediaTypes`: Array of allowed file types
- `mediaMaxSizeKb`: Maximum file size per file
- `mediaStorageProviderUserKey`: Storage configuration reference

## 8. COMPUTED FIELD TYPES

### computed
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
  "computedFieldValueProviderCtxt": "{\n  \"fields\": [\n    \"firstName\",\n    \"lastName\"\n  ],\n  \"separator\": \" \"\n}",
  "required": true
}
```

**Key Properties**:
- `computedFieldValueType`: Result data type
- `computedFieldTriggerConfig`: When to recalculate
- `computedFieldValueProvider`: Computation service class
- `computedFieldValueProviderCtxt`: JSON configuration for provider

## 9. SPECIALIZED FIELD TYPES

### password
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
  "encrypt": true,
  "encryptionType": "bcrypt"
}
```

### email
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

### phone
**Purpose**: Phone numbers with formatting  
**Database**: `varchar`  
**UI Component**: Phone input field  
**Use Cases**: Contact information, SMS notifications

```json
{
  "name": "phoneNumber",
  "displayName": "Phone Number",
  "type": "phone",
  "ormType": "varchar",
  "required": false,
  "min": 10,
  "max": 15
}
```

### json
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

## 10. SYSTEM FIELD PROPERTIES

All field types support these common properties:

### Core Properties
- `name`: Internal field reference (camelCase)
- `displayName`: User-friendly UI label
- `description`: Optional documentation
- `type`: Field type identifier
- `ormType`: Database column type
- `isSystem`: System-managed field flag
- `required`: Mandatory field flag
- `unique`: Uniqueness constraint
- `index`: Database index creation
- `private`: Hidden from UI flag
- `defaultValue`: Default field value

### Security Properties
- `encrypt`: Enable field encryption
- `encryptionType`: Encryption method (AES, bcrypt, etc.)
- `decryptWhen`: When to decrypt ("always", "admin_only", "never")

### Database Properties
- `columnName`: Custom database column name
- `enableAuditTracking`: Include in audit logs

### Validation Properties
- `min`/`max`: Value/length constraints
- `regexPattern`: Custom validation pattern
- `regexPatternNotMatchingErrorMsg`: Custom error message

## Field Type Decision Tree

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

This comprehensive guide covers all field types available in SolidX with real examples from your fees-portal metadata. Each field type is designed for specific use cases and automatically generates appropriate database columns, UI components, and API endpoints.
