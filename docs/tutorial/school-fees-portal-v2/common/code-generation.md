---
sidebar_position: 3
title: Generating APIs and UI Components
description: Guide for auto-generating code from your data models
---

## Generating APIs and UI Components

### Overview

- Once the data models are created, use SolidX's App Builder to auto-generate REST APIs and basic UI components for each model.
- The generated APIs will allow you to perform CRUD operations on your models. You can view the API documentation in the Swagger UI provided by SolidX at `/docs`.
- The generated UI components will provide a basic interface for managing your data. You can access these components through the model menu items which will be automatically added to the menu within your module.
- Ensure that the generated APIs and components meet your requirements and customize them as needed.

### Code Generation Steps

1. Navigate to the App Builder menu (within the Solid Core Module).
2. Select the Modules sub-menu.
3. Click on the context menu (three dots) for your module and select "Generate Code".
4. Click Yes on the confirmation dialog to start the code generation process.
5. The Code Generation process may take a few minutes. All models within your module will be processed one by one.
6. It can result in creation/updation of multiple files within the `solid-api` folder. SolidX does not make any code changes in the `solid-ui` project, since the UI components are generated dynamically at runtime based on the metadata stored in the database.
7. In dev mode, code changes will be picked up automatically.
8. You can verify the generated REST APIs using Swagger UI at `/docs` endpoint.
9. You can access the generated UI components through the model menu items within your module.

:::tip Generating Code for a Single Model
In case you want to generate code for a single model and your module has many other models, you can choose to generate code for only that specific model by navigating to the Models sub-menu instead.

Select the desired model, and click on the "Generate Code" option from the context menu.

In case this model has relations with other models, those related models will also be processed during code generation.

This approach can help reduce the time taken for code generation.
:::
