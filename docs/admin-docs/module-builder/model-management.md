---
sidebar_position: 2
---

import { FiTrash2, FiActivity, FiGlobe, FiLayers, FiDatabase, FiCode } from "react-icons/fi";

# Models

SolidX Models represent the structure of your data within a module. Each model defines a specific type of data, all attributes / fields that a model is made of & its relationships with other models.

Each model is a semantic, configurable data structure that forms the basis of adding custom business logic.

## Creating a Model

![Model Create Form](/img/admin-docs/module-builder/model-create-form.png)

To create a new model:

1. Navigate to the App Builder, then click on the "Model" menu item.
2. This will show a list of existing models in the system.
3. Click on "Add"
4. To create a model, you'll be prompted to provide the following metadata:

### Model Metadata

| Setting               | Description                                                                                                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module                | Every model belongs to one module, this is a dropdown of all modules configured in the system.                                                                            |
| Data Source           | SolidX allows you to create models reading / writing data from different data sources. You choose the data source here.                                                   |
| Display Name          | Display name of the newly created model.                                                                                                                                  |
| Singular Name         | Singular name of the model, used for internal purposes like API endpoints etc.                                                                                            |
| Plural Name           | Plural name of the model, used for internal purposes like API endpoints etc.                                                                                              |
| Table Name            | By default table names are generated automatically based on the singular name of the model, you can choose to specify a different name if required.                       |
| Enable Soft Delete    | If you would like to support soft delete functionality on a model.                                                                                                        |
| Is Child              | Sometimes you want to create an extension of an existing model, especially in IAM you might want to extend the user model to create your own definition of a user object. |
| Enable Audit Tracking | If you would like to audit all data mutations that happen on this model.                                                                                                  |

## Advanced Features

<div className="border-box">

  <div className="card-headear-wrapper">
    <FiTrash2 size={25} />
    
### Soft Delete
  </div>

  <p>
    Soft delete is a way to "hide" records instead of permanently removing them from the system. When you soft delete something—like a user, form, or entry—it doesn't actually get erased from the database. Instead, it's marked as deleted and no longer shown in the app. This helps prevent accidental data loss and makes it possible to restore deleted items if needed later.
  </p>

  <p>To enable this you simply need to click on the checkbox under "Configurations"</p>

  <p>TODO: Create a link to the soft delete recipe that will include screenshots of how soft delete actually works, mention recovery, querying with soft-deleted records etc..</p>

</div>

<br/>

<div className="border-box">

  <div className="card-headear-wrapper">
    <FiActivity size={25} />
    ### Audit Tracking
  </div>

  <p>
    Audit tracking helps you keep a detailed record of everything that happens to your data. It automatically logs who created, updated, or deleted a record—and when they did it. You can also track important business events using custom audit entries. All this information is easily accessible from the form view of each record, where you can filter by date, user, or event type to see exactly what changed and who made the change. This ensures transparency, accountability, and peace of mind.
  </p>

  <p>To enable this you simply need to click on the checkbox under "Configurations"</p>

  <p>Comprehensive tracking of record changes:</p>
  <ul>
    <li>Creation timestamp and user</li>
    <li>Modification timestamp and user</li>
    <li>Deletion timestamp and user (with soft delete)</li>
    <li>Field-level change history</li>
    <li>Custom audit events</li>
  </ul>

  <p>TODO: Create a link to the audit tracking recipe that will include screenshots of how entries are made visible on the chatter window, filtering / searching in chatter, also demonstrate a custom audit event..</p>

</div>

<br/>

<div className="border-box">

  <div className="card-headear-wrapper">
    <FiGlobe size={25} />
    ### Internationalization
  </div>

  <p>
    Internationalization lets you manage content in multiple languages within the same model. Each record can have translations linked together—so you can easily create and manage versions of the same entry in different languages. This is especially useful for global apps where users need to see content in their preferred language. Our platform handles the complexity for you, allowing you to switch between languages and manage translations seamlessly from the same interface.
  </p>

  <p>Internationalization supports:</p>
  <ul>
    <li>Editing content of the model in multiple languages.</li>
    <li>Fetching this content easily using our API</li>
  </ul>

  <p>TODO: Create a link to the internationalization recipe that will include screenshots of how exactly one is supposed to work with internationalization.</p>

</div>



## Fields

  <p>
    A core part of defining a model involves defining all the fields that make up the model. SolidX provides a very rich abstraction around how fields are configured against a model.
  </p>

  <p>Fields in SolidX go beyond basic types like string or integer.</p>

  <p>They support rich semantic types that allow for expressive and dynamic user interfaces out of the box, below are a few examples:</p>
  <ul>
    <li> **one2many, many2one, many2many:**  Define relationships between models just like you would in a full-stack framework.</li>
    <li> **selectionStatic:** Create dropdowns using static value lists (e.g. status: [New, In Review, Approved]).</li>
    <li> **selectionDynamic:** Fetch dropdown options from dynamic sources such as APIs (e.g. countries from a REST endpoint).</li>
    <li> **mediaSingle / mediaMultiple:** Allow single or multiple file uploads including images, documents, audio, or video.</li>
    <li> **richText / markdown / json / expression:** Provide advanced content editing, structured data input, or script-based values.</li>
  </ul>


<br/>

<div className="border-box">

  <div className="card-headear-wrapper">
    <FiCode size={25} />
    ### Generated Code
  </div>

  <p>
    When a new model is created SolidX generates a bunch of boilerplate code linked to this model.
  </p>

  <p>
    To see the impact of what happens when we generate the code linked to a model metadata you can view our <a href='../../developer-docs/index.md'>developer documentation</a>.
  </p>

  <p>TODO: Create the structure of the developer documentation and provide link here.</p>

</div>

<br/>

<div className="border-box">

  <div className="card-headear-wrapper">
    <FiDatabase size={25} />

### Related Recipes
  </div>

  <ul>
    <li><a href='../../recipes/'>Additional Datasources</a>: This recipe talks about how you can add additional data sources to your application.</li>
    <li><a href='../../recipes/'>Soft Delete</a>: When you enable soft delete functionality, when a record is deleted from a model it is not actually deleted instead it is still available in the database. This recipe talks about how you can configure your model to be soft delete aware.</li>
    <li><a href='../../recipes/'>Custom User Model</a>: This recipe talks about a common pattern where you want to create a custom user object for your app while keeping all the features around roles and permissions intact.</li>
    <li><a href='../../recipes/'>Internationalization</a>: When using SolidX as a headless CMS, if you want to create models meant to store multi-lingual content.</li>
    <li><a href='../../recipes/'>Master Slave</a>: Being an enterprise low code platform we support the ability to have models that read & write from & to separate data sources.</li>
  </ul>

</div>
