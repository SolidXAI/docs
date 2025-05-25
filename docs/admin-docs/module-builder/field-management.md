---
sidebar_position: 3
---

# Fields

Every SolidX model is composed of fields. Fields in SolidX go over and above the standard fields one expects, instead we treat fields as semantic attributes with relevance to how the users interact with that data in our admin interface. 

## Creating New Fields 

Fields are created from the model creation form.

To create a new field:

1. Navigate to the App Builder, then click on the "Model" menu item.
2. This will show a list of existing models in the system.
3. Find the model in which you would like to add a new field.
4. Click on the model to open it in the form view. 
5. Click on the "Fields" tab, and then click on the "Add" button inside the Fields tab.

This will open up the "Add New Field" popup. Adding a field involves first selecting the type of field you want to add, and then providing field specific metadata. 

![Choose Field Type](/img/admin-docs/module-builder/add-field-choose-field-type.png)

The metadata you provide is itself split into 2 parts Basic & Advanced. Basic metadata is common for all fields, while the Advanced metadata varies based on the field type.

![Choose Field Type](/img/admin-docs/module-builder/add-field-metadata.png)

Below you will find detailed documentation for each field type

### Basic Config

All fields need to at the minimum specify the following fields. 

- Display Name: This is used on all SolidX views as a label wherever the field is used. 
- Name: This is the internal name of this field.
- Description: Whatever you write here will be used as help text tooltip on all SolidX views. 
- Set Column Name: By default SolidX generates the column name for you, if you want to control the column name then enable this option and specify the column name.

### Advanced Config

This section allows you to add metadata specific to each field type. 

#### Integer

![Integer Field](/img/admin-docs/module-builder/integer-field.png)


#### Big Integer

![Big Integer](/img/admin-docs/module-builder/big-integer-field.png)


#### Decimal

![Decimal](/img/admin-docs/module-builder/decimal-field.png)


#### Short Text

![Short Text](/img/admin-docs/module-builder/short-text-field.png)


#### Long Text

![Long Text](/img/admin-docs/module-builder/long-text-field.png)


#### Rich Text

![Rich Text](/img/admin-docs/module-builder/rich-text-field.png)


#### JSON

![JSON](/img/admin-docs/module-builder/json-field.png)


#### Boolean

![Boolean](/img/admin-docs/module-builder/boolean-field.png)


#### Date

![Date](/img/admin-docs/module-builder/date-field.png)


#### Datetime

![Datetime](/img/admin-docs/module-builder/datetime-field.png)


#### Time

![Time](/img/admin-docs/module-builder/time-field.png)


#### Relation

##### Many to one

![Many to one](/img/admin-docs/module-builder/relation-field-many-to-one.png)

##### Many to many

![Many to many](/img/admin-docs/module-builder/relation-field-many-to-many.png)

##### One to many

![One to many](/img/admin-docs/module-builder/relation-field-one-to-many.png)

#### Single Media

![Single Media](/img/admin-docs/module-builder/single-media-field.png)

#### Multiple Media

![Multiple Media](/img/admin-docs/module-builder/multiple-media-field.png)


#### Email

![Email](/img/admin-docs/module-builder/email-field.png)


#### Password

![Password](/img/admin-docs/module-builder/password-field.png)


#### Static Selection

![Static Selection](/img/admin-docs/module-builder/static-selection-field.png)


#### Dynamic Selection

![Static Selection](/img/admin-docs/module-builder/dynamic-selection-field.png)


#### Computed 

![Static Selection](/img/admin-docs/module-builder/computed-field.png)


#### UUID

<!-- 

#### Basic Fields

| Type | Description | Use Case |
|------|-------------|----------|
| Text | Short text content | Names, titles, references |
| Long Text | Extended text content | Descriptions, notes |
| Number | Numeric values | Quantities, amounts |
| Boolean | True/false values | Status flags, toggles |
| Date | Date values | Event dates, deadlines |
| DateTime | Date and time values | Timestamps, schedules |
| Email | Email addresses | Contact information |
| Phone | Phone numbers | Contact information |
| URL | Web addresses | Links, websites |

### Advanced Fields

| Type | Description | Use Case |
|------|-------------|----------|
| Media | File and image uploads | Documents, images |
| JSON | Structured data | Complex data structures |
| Enumeration | Predefined list of values | Status types, categories |
| Password | Secure password storage | User credentials |
| Rich Text | Formatted text content | Documentation, articles |
| Color | Color values | Theme settings, styling |

### Relationship Fields

| Type | Description | Use Case |
|------|-------------|----------|
| One-to-One | Link to single record | User profiles |
| One-to-Many | Link to multiple records | Order items |
| Many-to-Many | Bidirectional multiple links | Product categories |

## Field Configuration

### Common Options

| Option | Description |
|--------|-------------|
| Name | Internal field identifier |
| Label | Display name in UI |
| Description | Help text for users |
| Required | Make field mandatory |
| Unique | Ensure unique values |
| Default Value | Initial value for new records |
| Searchable | Include in search results |
| Sortable | Allow sorting by this field |

### Type-Specific Options

#### Text Field
- Minimum/Maximum length
- Regular expression validation
- Case sensitivity
- Trim whitespace

#### Number Field
- Minimum/Maximum value
- Decimal places
- Currency format
- Thousand separator

#### Media Field
- Allowed file types
- Maximum file size
- Storage provider
- Image dimensions
- Thumbnail generation

## Validation Rules

Fields can have multiple validation rules:

1. **Built-in Validation**
   - Required field
   - Unique value
   - Minimum/Maximum values
   - Format validation

2. **Custom Validation**
   - Regular expressions
   - Custom functions
   - Complex conditions
   - Cross-field validation

## Best Practices

1. **Field Selection**
   - Choose specific field types over generic ones
   - Consider validation requirements
   - Plan for future data needs

2. **Naming Conventions**
   - Use clear, descriptive names
   - Follow consistent patterns
   - Consider API usage

3. **Performance**
   - Limit number of fields
   - Use appropriate indexes
   - Consider query patterns

4. **User Experience**
   - Provide helpful descriptions
   - Group related fields
   - Use appropriate default values
 -->