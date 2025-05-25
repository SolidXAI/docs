---
sidebar_position: 2
---

# Models

SolidX Models represent the structure of your data within a module. Each model defines a specific type of data & its relationships with other fields.
Each model is a semantic, configurable data structure that forms the basis of adding custom business logic.

## Creating a Model

![Model Create Form](/img/admin-docs/module-builder/model-create-form.png)

To create a new model:

1. Navigate to the App Builder, then click on the "Model" menu item.
2. This will show a list of existing models in the system.
2. Click on "Add"
3. To create a model, you'll be prompted to provide the following metadata:

### Model Metadata

| Setting | Description |
|---------|-------------|
| Module | Every model belongs to one module, this is a dropdown of all modules configured in the system. |
| Data Source | SolidX allows you to create models reading / writing data from different data sources. You choose the data source here. |
| Display Name | Display name of the newly created model. |
| Singular Name | Singular name of the model, used for internal purposes like API endpoints etc. |
| Plural Name | Plural name of the model, used for internal purposes like API endpoints etc. |
| Table Name | By default table names are generated automatically based on the singular name of the model, you can choose to specify a different name if required. |
| Enable Soft Delete | If you would like to support soft delete functionality on a model. |
| Is Child | Sometimes you want to create an extension of an existing model, especially in IAM you might want to extend the user model to create your own definition of a user object. |
| Enable Audit Tracking | If you would like to audit all data mutations that happen on this model. |

## Advanced Features

### Soft Delete
Soft delete is a way to "hide" records instead of permanently removing them from the system. When you soft delete something—like a user, form, or entry—it doesn't actually get erased from the database. Instead, it's marked as deleted and no longer shown in the app. This helps prevent accidental data loss and makes it possible to restore deleted items if needed later.

To enable this you simply need to click on the checkbox under "Configurations" 

TODO: Create a link to the soft delete recipe that will include screenshots of how soft delete actually works, mention recovery, querying with soft-deleted records etc..

### Audit Tracking
Audit tracking helps you keep a detailed record of everything that happens to your data. It automatically logs who created, updated, or deleted a record—and when they did it. You can also track important business events using custom audit entries. All this information is easily accessible from the form view of each record, where you can filter by date, user, or event type to see exactly what changed and who made the change. This ensures transparency, accountability, and peace of mind.

To enable this you simply need to click on the checkbox under "Configurations" 

Comprehensive tracking of record changes:
- Creation timestamp and user
- Modification timestamp and user
- Deletion timestamp and user (with soft delete)
- Field-level change history
- Custom audit events

TODO: Create a link to the audit tracking recipe that will include screenshots of how entries are made visible on the chatter window, filtering / searching in chatter, also demonstrate a custom audit event..

### Internationalization

Internationalization lets you manage content in multiple languages within the same model. Each record can have translations linked together—so you can easily create and manage versions of the same entry in different languages. This is especially useful for global apps where users need to see content in their preferred language. Our platform handles the complexity for you, allowing you to switch between languages and manage translations seamlessly from the same interface.

Internationalization supports: 
- Editing content of the model in multiple languages. 
- Fetching this content easily using our API

TODO: Create a link to the internationalization recipe that will include screenshots of how exactly one is supposed to work with internationalization.

## Fields

A core part of defining a model involves defining all the fields that make up the model. SolidX provides a very rich abstraction around how fields are configured against a model. 

Fields in SolidX go beyond basic types like string or integer. 

They support rich semantic types that allow for expressive and dynamic user interfaces out of the box, below are a few examples: 

- one2many, many2one, many2many: Define relationships between models just like you would in a full-stack framework.
- selectionStatic: Create dropdowns using static value lists (e.g. status: [New, In Review, Approved]).
- selectionDynamic: Fetch dropdown options from dynamic sources such as APIs (e.g. countries from a REST endpoint).
- mediaSingle / mediaMultiple: Allow single or multiple file uploads including images, documents, audio, or video.
- richText / markdown / json / expression: Provide advanced content editing, structured data input, or script-based values.


## Generated Code

When a new model is created SolidX generates a bunch of boilerplate code linked to this model. 

To see the impact of what happens when we generate the code linked to a model metadata you can visit this page. TODO: Create the structure of the developer documentation and provide link here. 


## Related Recipes

1. [Additional Datasources](../../recipes/): <br />
   This recipe talks about how you can add additional data sources to your application.
2. [Soft Delete](../../recipes/): <br />
   When you enable soft delete functionality, when a record is deleted from a model it is not actually deleted instead it is still available in the database. 
   This recipe talks about how you can configure your model to be soft delete aware. 
3. [Custom User Model](../../recipes/): <br />
   This recipe talks about a common pattern where you want to create a custom user object for your app while keeping all the features around roles and permissions intact. 
4. [Internationalization](../../recipes/): <br />
   When using SolidX as a headless CMS, if you want to create models meant to store multi-lingual content.
5. [Master Slave](../../recipes/): <br />
   Being an enterprise low code platform we support the ability to have models that read & write from & to separate data sources. 


<!-- 
## Best Practices

1. **Data Modeling**
   - Plan your model structure carefully
   - Consider relationships between models
   - Use appropriate field types

2. **Performance**
   - Enable features selectively
   - Consider indexing requirements
   - Plan for scalability

3. **Data Integrity**
   - Use soft delete when appropriate
   - Enable audit tracking for sensitive data
   - Plan backup strategies

4. **Internationalization**
   - Plan language requirements early
   - Consider regional differences
   - Document translation processes

 -->
