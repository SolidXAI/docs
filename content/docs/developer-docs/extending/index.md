---
title: Extending SolidX
description: Guide to extending SolidX with custom code generation and frontend/backend customization.
summary: This document serves as an overview of SolidX extensibility features, explaining how to build custom functional modules and extend the platform capabilities. It highlights three main customization areas - Generated Code (using the code generation tool to scaffold controllers, services, entities, DTOs, and layout JSON files with default list and form views), Frontend Customization (modifying layout.json for custom list views, form layouts, kanban boards, and UI behaviors), and Backend Customization (extending NestJS backend with custom services, controllers, computed providers, middleware, and business logic).
---

# Extending SolidX

This section outlines how to extend **SolidX** to build your own functional modules, such as a `school-fees-portal`.

SolidX offers a **powerful code generation tool** that enables rapid scaffolding of new modules with all the essential boilerplate. This accelerates your development by letting you focus directly on your specific **business logic**, without worrying about foundational setup.

In addition to scaffolding, SolidX supports **deep customization** across both frontend and backend layers. You can tailor UI components, introduce new features, or adjust the behavior of existing elements to match your application's needs.

## Customization Capabilities

SolidX provides the following extensibility features:

<div>

### Generated Code

- Quickly scaffold new modules using the SolidX code generation tool.
- Auto-generates:
  - Controllers
  - Services
  - Entitities
  - Data Transfer Objects
  - Layout JSON files (for UI configuration)
- The default layout supports:
  - List View
  - Form View

</div>

<div>

### Frontend Customization

- Modify the generated `layout.json` to:
  - Customize list views
  - Tailor form layouts
  - Configure kanban boards
  - Add custom UI behaviors

</div>

<div>

### Backend Customization

- Extend the NestJS backend by adding:
  - Custom services and controllers
  - Computed providers
  - Middleware or interceptors
  - Business-specific logic

</div>

By leveraging these capabilities, you can build modular, scalable, and highly customized applications using the SolidX framework.
