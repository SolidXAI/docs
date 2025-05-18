---
sidebar_position: 2
---

# Module Builder

## Intro

The Module Builder is a core module of SolidX that enables you to create and manage your application's data models and user interfaces. With the Module Builder, you can accelerate development, simplify management, and create enterprise applications with minimal coding.

![SolidX Admin Dashboard](/img/admin-docs/module-builder/module-create-form.png)

In SolidX, applications are structured around Modules, which serve as the primary organizational unit in the platform. 

A module represents a self-contained functional area of your app — for example, Admissions, Inventory, or HR. Within each module, you define Models, which represent the core data structures relevant to that domain.

### 🧩 Models — More Than Just Tables

Unlike traditional low-code platforms where models are little more than simple database tables, SolidX models are semantic, configurable, and powerful:

  - Data Source Mapping: A model can be bound to various data sources, including internal databases or external APIs.
  - Soft Delete Support: Enable logical deletion of data by toggling soft delete behavior.
  - Internationalization (i18n): Models can be configured to support multilingual content.
  - Computed Fields & Expressions: Define business logic directly at the model level.
  - Custom Actions & Lifecycle Hooks: Inject custom behavior into your model’s create, update, or delete lifecycle.

### 🧬 Fields — Not Just Name & Type

Fields in SolidX go beyond basic types like string or integer. 

They support rich semantic types that allow for expressive and dynamic user interfaces out of the box, below are a few examples: 

  - one2many, many2one, many2many: Define relationships between models just like you would in a full-stack framework.
  - selectionStatic: Create dropdowns using static value lists (e.g. status: [New, In Review, Approved]).
  - selectionDynamic: Fetch dropdown options from dynamic sources such as APIs (e.g. countries from a REST endpoint).
  - mediaSingle / mediaMultiple: Allow single or multiple file uploads including images, documents, audio, or video.
  - richText / markdown / json / expression: Provide advanced content editing, structured data input, or script-based values.

These fields not only define the data schema but also influence the form layouts, validations, and user experience automatically — reducing the need for hand-coded UI logic.


### 💡 Example

Hypothetically speaking if we think about a School Management system we could have the following structure.
  - Module: Admissions
    - Model: Student
      - name (Text)
      - grade (selectionStatic: Grade 1–12)
      - birth_certificate (mediaSingle)
      - guardian (many2one → Guardian)
    - Model: Guardian
      - name (Text)
      - phone_number (Text)
      - nationality (selectionDynamic → fetch from country API)

<br></br>

<img src="/img/admin-docs/module-builder/module-model-eg-image.png" alt="SolidX Module Diagram" width="300" height="auto" />

<br></br>
<br></br>

This approach gives you a clean, maintainable, and semantically rich model of your domain — without writing any backend code.

Whats more is that SolidX generates a feature rich REST API backend on top of the domain model configuration you have just created, allowing you to then create enterprise workflows on top of your domain model. 



## Key Features

You can now use the below cards to browse through the key functionality exposed by the SolidX module builder. 

### Model Builder
Define and manage your data models through an intuitive interface that simplifies the model creation process. This includes:

  - **Module Management**: Organize your application into logical modules to maintain a clean architecture and facilitate easier updates.
  - **Model Management**: Efficiently define and manage the structure of your application’s data, ensuring it aligns with your business requirements.
  - **Field Management**: Configure various field types to structure your data, ensuring that it meets your application's needs effectively.

### Layout Editor
The models & fields used to define your domain can be arranged to generate a very powerful and feature rich metadata driven admin user interface. Which is highly customisable to accomodate a lot of enterprise use-cases. 

Allowing one to create custom views for your data using list, kanban, and form layouts, allowing for tailored user experiences. This includes:

  - **Menu Items**: Define navigational elements and their structure for your application.
  - **Views**: Create and customize different perspectives for displaying your data, such as List View, Kanban View, and Form View.
  - **Custom Actions**: Implement additional functionalities that can be triggered by user interactions.

<!-- 
## Getting Started

The App Builder consists of three main components that work in harmony to provide a comprehensive development environment:

- [Module Management](./module-management.md) - Organize your application structure
- [Model Management](./model-management.md) - Define your data models
- [Field Management](./field-management.md) - Configure data fields and their properties
- [Menu Items](./menu-items.md) - Define navigation structure
- [Views](./views/index.md) - Create and customize different views for displaying data
- [Custom Actions](./custom-actions.md) - Implement actions based on user interactions

Use the App Builder to construct everything from simple forms to complex data-driven applications, making it a versatile tool for any development project.

## Views

The App Builder supports multiple view types to display and interact with your data:

1. [List View](./views/list-view.md) - Display data in a tabular format for easy comparison and bulk actions.
2. [Kanban View](./views/kanban-view.md) - Visualize and manage data on a kanban board, ideal for task and workflow management.
3. [Form View](./views/form-view.md) - Create and edit individual records efficiently with an intuitive interface for detailed data entry.
 -->