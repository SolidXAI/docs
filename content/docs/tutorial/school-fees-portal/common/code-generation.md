---
title: Code Generation
icon: "code"
description: Guide for auto-generating code from your data models
---

## Generating APIs and UI Components

### Overview

- Once the data models are created, use SolidX's App Builder to auto-generate REST APIs and basic UI components for each model.
- The generated APIs will allow you to perform CRUD operations on your models. You can view the API documentation in the Swagger UI provided by SolidX at `/docs` e.g http://localhost:3000/docs
- The generated UI components provide a basic interface for managing your data. You can access them via the admin panel, where menu items for each model are automatically added under the associated module's menu.
- Ensure that the generated APIs and components meet your requirements and customize them as needed.

### Code Generation Steps

1. From the sidebar, navigate to **App Builder** under the **Solid Core** module.
2. Select the **Modules** sub-menu. This opens the module list page.
3. Locate your module in the list, click its context menu (three dots), and select **Generate Code**.
4. Confirm the action in the dialog to start the code generation process.
5. Code generation may take a few minutes as each model in your module is processed sequentially.
6. This process creates or updates files in the `solid-api` folder and updates the UI metadata in the database. The `solid-ui` project itself is not modified — UI components are rendered dynamically based on this metadata.
7. In SolidX dev mode (i.e., using `solidx:dev`), code changes are picked up automatically.
8. Verify the generated REST APIs using Swagger UI at the `/docs` endpoint.
9. Access the generated UI components through the model menu items within your module.
    - For example, the Institute model's list view would be available at `/admin/core/fees-portal/institute/list`, where `fees-portal` is the module name and `institute` is the model name.

> **Generating Code for a Single Model**

> To generate code for a specific model, navigate to the **Model** sub-menu instead within the **App Builder**. Locate the desired model, click its context menu (three dots), and select **Generate Code**.

> Note that any related models (via relations) will also be processed during code generation. This approach might be faster than regenerating the entire module, especially if you have many models in the module and only need to update one or a few of them.
